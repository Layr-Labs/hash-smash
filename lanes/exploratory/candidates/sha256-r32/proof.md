# SHA-256/32 ordinary collision: published characteristic as public algorithm text, 7-lane 36-bit guard-bit SWAR first-block evaluation, staged early abort and a finite table audit

## 0. Claim

The track is `sha256-r32-exploratory`, profile `sha256-r32-prefix-v1`, cost model `collision-frontier-v5`. One
32-step compression costs 1 unit and every other primitive word operation costs 1/C with C = 2224.

The algorithm is a classical two-block attack. It outputs two distinct 128-byte messages whose complete 32-step
SHA-256 hashes are equal: standard IV, standard padding, all 256 bits. Its bounds:
- success probability >= 0.39 (computed above 0.390096, Section 7);
- time <= 2^43.001 (exact integer ceiling 8,797,560,575,883 has log2 43.0002406814, Section 8);
- preprocessing <= 2^38.3 (C + D = 338,035,205,176 < 2^38.29839, itemised in Section 8);
- memory <= 2^36 bytes (computed below 2^35.861, Section 9);
- nonuniform advice < 2^13 bytes.

**This version.** It starts from our passed submission `621d0fb0` (43.262, `plausible_not_refuted`), which is
Th0rgal's passed `f310d44f` (47.275) with the published characteristic accounted as public algorithm text (Section 6).
This version changes three charges and nothing in the collision route, the rates or the success premises
(Section 8.2 lists them):
1. **Direct addressing of TAB2.** Records are bucketed by all 32 bits of `A[-1]` (2^32 + 1 offset cells) instead of
   the top 27 bits. Memory is not scored, so the larger offset array costs only its build work (charged in C at the
   same 1,024 operations per boundary). The bucket of `CV1[0]` then holds exactly the key-matching records: the mean
   scan falls from 10.41 to N / 2^32 = 0.32521 records per trial, and E[X] from 211.3 to 160.82.
2. **Counter cap and trial count re-optimised** for that mean: `W_cap = 162.5 T`, `T = 30,702,387,450,972`.
3. **Batch traffic and fixed per-trial work itemised for straight-line code:** the 7-trial SWAR batch is charged
   2,928 operations (2,336 counted arithmetic unchanged, 496 itemised traffic, 96 reserve) instead of 3,232, and the
   per-trial lookup/control 32 instead of 64.
The total falls from 2^43.2616 to 2^43.0002; we claim 43.001.

This package directly combines public Yukon submissions `8bad82c1-1950-4e17-a025-bacdf5dda6ce`
(source commit `1b538044fb5afa0acad1de30aba770b602645535`, PR #396, official exploratory score 47.60 and
`plausible_not_refuted`) and `c712ea19-84f8-4888-9de4-bb644d4e00fd`
(source commit `8834954861981020a5bd9d8a73e764c5101c0a0c`, PR #400, claim 48.20). The latter adapts
`f15d0743-ef0b-4b1e-83ba-6beae0fb9d9a` (source commit `a9e52a210d65a617fe85fa3e8f7603da46ae596b`,
PR #395, official exploratory score 48.21 and `plausible_not_refuted`), which adapts `a36add2f-5e05-4c9c-a727-eae03adc7be4`
(source commit `778baf4269779053adb51a0ff9cc8bef0f413157`, official exploratory score 48.25), which in turn
adapts `491c0048-2712-407c-beeb-207de0284c89` (source commit
`97c8e8c7040bf76a8f9723c7bcc745510f343b49`, official exploratory score 48.45). This package retains their
collision route, certificate, deterministic replay, table sizes, measured rates, declared probability premises and
source-level table-builder audit. PR #396 extends the characteristic search until its 59-call run outputs Fig. 6;
its predecessors charged the `32 * 593,858` CPU-second envelope; this version keeps that measurement only as fallback
evidence (Section 6.2). Submitted predecessor `aec1f12c-82e6-4d0f-be09-3388665ede9a` retains PR #400's staged Step-3 early
abort while removing its rejected transfer from alternate SAT solutions to the exact fixed starting advice. Passed
submission `9817cce0-89f6-4d0d-848d-e8fa8a4dfda9` (PR #402, official score 47.48) then sets
`T = ceil(2^44.807) = 30,778,752,666,088`, caps counted work at `214 T`, asserts the maximum bucket occupancy and
uses one-sided Bernstein. Passed submission `3d7e1cb6-dc6f-4143-baff-a607db8c88fc` (PR #404, official score 47.47)
replaces rounded display envelopes with exact integer component ceilings. Failed submission
`3bcf49b4-b75f-40b8-9de7-4bed3a5b01f5` (PR #405, claim 47.468) then replaced the table builder's common
8,192-operation envelope by five predecessor phase maxima plus a conservatively reclassified PC-4 maximum. Its cost,
evaluability and experiments reviews found the reconstruction plausible, but its aggregate result was `not_evaluable`
solely because the success proof left the transfer from a pooled valid tuple to the selected valid tuple implicit. Passed
submission `986364bd-7725-4e4f-8d63-485e7f3a6bf4` (PR #406, official 47.468, `plausible_not_refuted`) declares that
premise. Passed submission `1899d9ac-f68a-4e9d-b549-b94358775645` (PR #407, official 47.4668,
`plausible_not_refuted`) then reduces only the finite trial count under the rounded `2^-45.820` bound. Passed submission
`b2a7ac88-682a-424a-8ddc-c9a09b06319e` (PR #408, official 47.4667, `plausible_not_refuted`; validated source commit
`6db1ff496a018301341e51ef672496c6626935a9`) retains every attack premise and charge but uses the full displayed
factor product. Passed submission `f7b8cac4-f0a6-4fb9-a696-ff4e26f75a1c` (PR #419, official 47.46513,
`plausible_not_refuted`; validated source commit `49749c8663fe9e7cfc444079ab10785052f2f3d2`) then changes only the
exact-source starting-solution ceiling from `2^37.83` to `2^35`. Passed submission `9445db88-93d4-4d41-b49b-c3f2d3c1c205`
(PR #425, official 47.30; source `353f254849e5c22a64cc0e98041a687d29c8715f`) and passed submission
`10506300-27a3-45e7-bdce-963e9cbe2b56` (official 47.29; validated commit `1dcd6067452b0263c2dfb0812c78528686e71c76`)
are the exact public base; this revision replaces the 8-lane carry-save SWAR first-block evaluation (`4,608` ops per
8-trial batch, `576` ops/trial) with a **7-lane 36-bit guard-bit SWAR first-block evaluation** (`2,336` counted
arithmetic/randomness ops + `800` traffic/control + `96` reserve = `3,232` ops per 7-trial batch, `461.71` ops/trial).
Historical attack-rate evidence was not rerun.

An organizer-verified 128-byte 32-step collision certificate (`certificates/message-a.bin`, `certificates/message-b.bin`,
common digest `f8a3db111360e5ed2e63041ecfa82b01c95a25882910bc0f21671949296a4e77`) is supplied in
`certificates/manifest.json`, and an organizer-executed deterministic witness reconstruction (`fixed-witness-derivation`
in `experiments/replay.py`) verifies the Step-2 tuple decoding, the retained #227 compact-table
bucket/bitmap/combo/left/v7 slices, Step-3 16-step message-word derivation, and bit-exact 7-lane 36-bit guard-bit SWAR
(with `Swar7Counter` operation counting) and 8-lane SWAR `C_32`
equivalence on organizer-generated inputs in the isolated evaluator container. That replay checks one witness lineage
and finite SWAR functional examples; it does not prove universal circuit identity or validate the different
27-bit-bucket `TAB2` cardinalities, its construction cost, or the
submitted SWAR resource bound.

Sources and credit:
- **Passed Yukon submissions `9445db88-93d4-4d41-b49b-c3f2d3c1c205` (47.30) and `10506300-27a3-45e7-bdce-963e9cbe2b56` (47.29).**
  Validated commit `1dcd6067452b0263c2dfb0812c78528686e71c76` is the exact public base of this revision. It supplies the
  800-operation batch traffic/control audit, `D = 2^35`, and every inherited attack premise, cost and evidence item.
- **Failed Yukon submission `e8bd4c94-067d-49ca-a977-09a81d2dee98`.** PR #420 introduced the 8-lane carry-save SWAR
  evaluator in `replay.py` (which uses two `CSA32x8` and five `ADD32x8` calls = 87 ops per round) while undercharging
  its round line at 56 ops. Both `1dcd606` (which charges the full 87 ops per round in 8 lanes) and this revision
  (which switches to 7 lanes of 36 bits with 4 guard bits per lane, where each modular addition is a single 256-bit
  addition and `Swar7Counter` in `replay.py` verifies the exact 52-op round and 2,336-op batch arithmetic count) resolve
  that discrepancy completely.
- **Public Yukon submission `8bad82c1-1950-4e17-a025-bacdf5dda6ce`.** The score-47.60 package at commit
  `1b538044fb5afa0acad1de30aba770b602645535` supplies the completed 59-call characteristic-search measurement,
  the exact Fig. 6 output comparison, the `32 * 593,858` CPU-second route-search envelope, and the strengthened
  opcode audit. This revision keeps that envelope as fallback evidence (Section 6.2).
- **Passed Yukon submission `f310d44f-a1dc-4241-8b26-cbdad0f6fe72` (Th0rgal, 47.275).** The 7-lane 36-bit guard-bit
  SWAR first-block evaluation, `Swar7Counter`, and the 3,232-operation batch; this package is f310d44f with only the
  characteristic accounting changed.
- **Organizer-accepted SHA-256 r31 package `50592e75` (jungjipdo, 37.22).** The public-characteristic convention.
- **Public Yukon submission `c712ea19-84f8-4888-9de4-bb644d4e00fd`.** The claim-48.20 package at commit
  `8834954861981020a5bd9d8a73e764c5101c0a0c` supplies the staged Step-3 early-abort ledger, `T = ceil(2^44.83)`,
  the `300 T` cap, Chebyshev success subtraction, 12-word P4 layout and static table audit. Its paired review found
  the declared online-rate, work-moment and table-cost premises plausible but returned `not_evaluable` for the
  separate exact-advice timing transfer. The submitted 47.49 predecessor replaces that transfer and the
  characteristic-search term. The passed 47.48 revision tightens the finite stopping analysis and the passed 47.47
  revision uses exact component ceilings. Failed PR #405 sums the phase-specific table-builder charges; passed PR #406
  retains that ledger and declares the selected-valid-tuple transfer; passed PR #407 tightens the finite trial count.
  This revision retains those changes and removes only PR #407's final downward rounding of the success-factor product.
- **Public Yukon submission `f15d0743-ef0b-4b1e-83ba-6beae0fb9d9a`.** The score-48.21 package at
  commit `a9e52a210d65a617fe85fa3e8f7603da46ae596b` supplies the conservative probability rounding, finite
  work-moment stopping rule, source-level table-builder audit, and precise old-table replay boundary.
- **Public Yukon submission `a36add2f-5e05-4c9c-a727-eae03adc7be4`.** The corrected `2^25.02` CPU-second
  search charge, inherited package and `T = 2^45` probability/cost adaptation come from its published candidate
  at commit `778baf4269779053adb51a0ff9cc8bef0f413157`.
- **Public Yukon submission `491c0048-2712-407c-beeb-207de0284c89`.** All route construction, certificates,
  replay, measured campaigns, characteristic-search allowance and CPU calibration below come from its published
  candidate at commit `97c8e8c7040bf76a8f9723c7bcc745510f343b49`. The new table-builder audit is analytical and is not
  attributed to that historical campaign.
- **S.** Y. Li, F. Liu, G. Wang, J. Shi, "Pushing the Limit of Memory-efficient Collision Attack Framework for SHA-2",
  CRYPTO 2026, ePrint 2026/1080. From S we take the 35-step characteristic (Fig. 6), the 35-step pair (Table 3), the
  three-step attack and the four-step characteristic search.
- **The solver model.** Li, Liu, Wang, EUROCRYPT 2024, ePrint 2024/349, public code github.com/Peace9911/sha_2_attack.
- **hash-smash #26/#33 (winglock; commits `ff377db450879d36cbe2a9125ef80580af8603d1` and
  `e571806080ac312a7a2661d8fd5515b417a9bf1a`).** The truncation, the table and the Step-2/3 tests (our Sections 3-5),
  the q prediction method, and the unprinted condition E16[29] = E17[29].
- **hash-smash #296 (mitchuski; commit `a22d18719c48ea71b6b428099cbe4fcb16a0884e`).** The r32 reimplementation,
  cardinalities, attack-rate campaign, and first 57 calls of the measured rerun of the authors' STP + CryptoMiniSat search;
  PR #396 supplies the two later Step-4 calls and completed 59-call ledger.
- **hash-smash #134 (jagnani73).** The callgrind instruction calibration and CPU-second pricing precedent.
- **hash-smash #31 (hybridnoise).** The need to charge the search's memory, and the reading of S's search steps.
- **hash-smash #227 (yudduy; commit `689cb95ecd1538f08b536741a696c74f6fb78ea5`; re-costed in #224 by
  dariolina).** The verified 128-byte 32-step collision witness of this route (Section 3) and its embedded compact-table
  slice derivation (`experiments/replay.py`).

Inherited route evidence and the new parameter choice:
1. **Verified 128-byte 32-step collision certificate (`sha256-r32-record-witness`) + organizer-executed `experiments/replay.py`**
   supply fixed-witness-lineage evidence that was absent from #296 and check bit-exact equivalence and exact primitive
   operation counts (`Swar7Counter`: `2,336` arithmetic/randomness operations per batch) between the replay's 7-lane
   36-bit guard-bit SWAR evaluator and seven scalar `C_32` evaluations on each organizer seed.
2. **The characteristic is public algorithm text (Section 6.1).** Its discovery is not charged; every value-level
   object is. The public re-run of S's search through an exact Fig. 6 output (59 calls, 593,858 CPU-s) is kept as
   fallback evidence: charging it with a factor `32` at `kappa = 2^23` would add `E = 159,412,543,029,248` units.
3. **The exact published starting solution is charged from its source construction.** S builds TAB2 from that single
   Step-1 solution and reports about `2^34.3` for finding it. Interpreting the unstated source unit as a full 35-step
   compression and converting by `2476/2224` fits below `D = 2^35 = 34,359,738,368` units. The source unit remains
   unspecified; alternate locally timed solutions are corroboration only and are never substituted.
4. **This candidate keeps the staged early abort and its finite stopping analysis, while batching seven independent
   first-block evaluations in 36-bit lanes of the 256-bit word RAM.**
   The measured stage-16 fraction is below `0.1250002` and cumulative stage-17 rate is below `2^-14.9999`;
   the work ledger uses the larger `0.126` and `2^-14.9` upper envelopes. An asserted maximum bucket occupancy 936
   bounds per-trial work, so Bernstein makes cap stop small at `162.5 T`. Taking
   `T = 30,702,387,450,972` (`B_7 = ceil(T/7) = 4,386,055,350,139` batches at `2,928` ops/batch)
   and retaining the full displayed product of the declared
   lower-bound factors gives success above 0.390096 and total cost
   `8,797,560,575,883 = 2^43.0002406814... < 2^43.001` target-compression units without changing the collision
   construction, the independent-trial probability space or the event.
   For the lower bound, conditionally on `V >= 1` an analysis-only selector chooses `J` uniformly from the valid tuples;
   its conditional Step-3 rate is a separate declared heuristic, not an independence inference from pooled measurements.
5. **The precomputation charge is rebuilt from explicit finite control flow:** Section 8.1 applies each displayed
   phase-specific maximum to its exact iteration count, then separately charges worst-case record placement,
   bucket-array administration, and retained auxiliary rows.

## 1. Notation

Words are 32-bit and + is mod 2^32. Sigma0, Sigma1, sigma0, sigma1, IF and MAJ are as in FIPS 180-4.
W[i] = M[i] for i < 16, and W[i] = sigma1(W[i-2]) + W[i-7] + sigma0(W[i-15]) + W[i-16] for i >= 16.

For a chaining value CV = (a..h), put A[-1..-4] = (a,b,c,d) and E[-1..-4] = (e,f,g,h). Then

```
E[i] = A[i-4] + E[i-4] + Sigma1(E[i-1]) + IF(E[i-1],E[i-2],E[i-3]) + K[i] + W[i]
A[i] = E[i] - A[i-4] + Sigma0(A[i-1]) + MAJ(A[i-1],A[i-2],A[i-3])
```

C_R(CV,M) = CV + (A[R-1..R-4], E[R-1..R-4]). The target applies C_32 to every padded block. The messages are M0||M1
and M0||M1' (128 bytes each), so the third block is the common padding block P (80000000, 0..0, 00000400).

Signed rows follow S. Position k is bit 31-k, and the rows read: `n` x=0, x'=1; `u` x=1, x'=0; `=` equal; `0`/`1`
equal with that value. FL(X) is the n/u mask and D(X) = sum over n of 2^j - sum over u of 2^j. **XOR-conformance at
step i** means: with every primed input set to x xor FL(x), the step equation on the primed words gives
A'[i] = A[i] xor FL(A[i]) (resp. E). This is an exact 32-bit equality test.

## 2. Characteristic (S, Fig. 6)

Unprimed values are S's M'_1. Rows 23..34 are all `=`.

```
  i   nabla A[i]                        nabla E[i]                        nabla W[i]
-4..-1 all =                            all =
 0-2  ================================  ================================  ================================
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

S prints `+` at two positions of E10 and E11. We write `=` there; both published messages agree on those bits. The
weights are tw = 22, tE = sum_{14..18} H(nabla E) = 6, tA = 21 and tE4 = sum_{4..18} H(nabla E) = 76.

Two-bit conditions printed by S (X[a,b] = Y[c,d] means X[a] = Y[c] and X[b] = Y[d]):

```
W4[1,8]!=W4[12,25] W4[18]=W4[14] W5[0,1,30]=W5[28,18,9] W6[1,8]=W6[12,25] W6[18]!=W6[14]
W7[22,13,23]!=W7[18,9,8] W7[11,14,20]=W7[22,31,31] W8[0,14,21]=W8[28,25,6] W8[31,23,30,15,22,8]!=W8[27,2,15,26,7,4]
W20[4,31]=W20[6,22] W20[31,30,25,21]!=W20[1,0,16,14] W22[4,31]=W22[6,22] W22[27]!=W22[20]
E4[10]!=E4[15] E5[3,21]=E5[8,8] E6[9,27,9,8]!=E6[23,14,14,27] E6[1,1,23,6]=E6[6,15,10,25] E7[21,10]!=E7[3,15]
E16[28,20,20,6]=E16[1,7,2,11] E16[30,28,10]!=E16[12,10,29] E18[24]!=E18[11] E18[2]=E18[16]
A3[29]=A2[29] A3[29]!=A5[29] A3[26,4]=A4[26,4] A3[22,18,16,11,7]!=A4[22,18,16,11,7] A14[9]=A14[20]
A14[18,8]=A14[6,17] A13[30,25,23]=A14[30,25,23] A13[15]!=A14[15] A13[29]!=A15[29] A15[29]=A6[29]
```

We use the reading that is consistent with the published pair (as in #26):
- the E7 relations are read as `=`;
- A14[18,8] != A14[6,17];
- A15[29] = A16[29], since "A6" is a misprint;
- the two W20 equalities are dropped.

This leaves 71 two-bit conditions. They shape the precomputed sets or the online tests of Section 4; every
attack-critical test is an exact equality.

**Check against the pair.** Our recomputation of S's Table 3 pair uses the organizer's
`digest(., 'sha256', 35)` and the public source submission's independent code.
- CV1 = C_35(IV, M0) = c4369610 c91f70a7 87e430e6 a5e58128 d29cb97b 9ab268d1 8788f401 629f6cb2.
- The pair's signed differences equal the rows above: 119 n/u symbols and 360 single-bit conditions, with 0
  mismatches.
- The 35-step digests are equal and the 32-step digests differ. The pair is not a 32-step collision.

M0 = a8850273 c0f4a504 5d3ad7b5 6e5f5026 535cc256 e92ef7a5 436f70df 7d7e236a cadc14e8 d59ac191 6874f1ba 6b83960d
f6dfe9de 6a013df2 f856b739 237894e8;
M1' = c0008214 ae65f3bf e93c006a 5f195aa9 84d6cd0f 25c114ec ca897317 da9fd6ef 6ec97e18 5100da8a 0912e57b a96b2054
41b22a2c 6d12f88a d2701ecc 140976d1;
M1 = M1' xor FL(W): words 4..8 are a4d6cd0f 21811cec ea897317 db9ec665 6ec17218, and words 12..13 are 45f2222c 4d12f88a.

## 3. Truncation to 32 steps

**Lemma 1.** If A[j] = A'[j] and E[j] = E'[j] for j = 19..22, and W[j] = W'[j] for j = 23..31, then
C_32(CV,M) = C_32(CV,M').

*Proof.* By induction on steps 23..31, every input of each step is equal. The feed-forward adds a common CV.

**Lemma 2.** With a common M0, M1 != M1', equal lengths, and C_32(CV1,M1) = C_32(CV1,M1'), the messages M0||M1 and
M0||M1' collide.

*Proof.* The padding block P is the same, and so is the chaining value entering it.

Rows 19..22 of A and E, and rows 23..31 of W, are `=` in Fig. 6. So a second block that conforms through step 22
and in W16..W31 gives a 32-step collision. The 35-step attack's conditions at steps 0..22 and the zero rows W23..W31
are exactly what is needed. Nothing is added. The rows W32..W34 are unused: W32 = sigma1(W30) + W25 +
sigma0(W17) + W16, W33 and W34 contain no difference term. The only change is CV1 = C_32(IV, M0), whose rate is
measured in Section 5.

**Certified 32-step collision witness (`certificates/manifest.json` and `experiments/replay.py`).** We include the
verified 128-byte 32-step colliding message pair (`certificates/message-a.bin`, `certificates/message-b.bin`,
common 32-step SHA-256 digest `f8a3db111360e5ed2e63041ecfa82b01c95a25882910bc0f21671949296a4e77` under
`sha256-r32-prefix-v1`) originally produced by this exact truncated route in hash-smash #227 (yudduy; re-costed in #224
by dariolina). Both messages share `M0 = 04a9b33e 6ea679aa 89f6fb3b f530dfa8 c5828a5e 385388a4 0dbcd14f 77252e33 4fef2ad0 809de1a4 a3b955b6 3a95b0cc 5cadb080 01a17ef2 00000000 801aeced`
with `CV1 = C_32(IV, M0) = e890c4ba 6bce94e6 47a0b812 c5ef36b2 ec7b7814 91cf09df a9717904 494bc86f`, and their second
blocks follow every row of Fig. 6 through step 22 and `W0..W31` (0 mismatches), colliding at `states[1] = 79389eeb 882fc938 62f355f8 3ebb8d51 4d0b99ce a01e12ed 7058785b dae69307`
before the common padding block. In `experiments/replay.py` (`fixed-witness-derivation`), the organizer evaluator
reconstructs this colliding pair directly from the embedded 112-byte tuple record, exact retained #227 compact-table
slices, and 48-byte tail record, verifying both the Step-2/Step-3 derivation and the full 32-step collision. The old
compact table uses 26-bit buckets and 609,229,824 entries; this replay is not evidence for the 27-bit-bucket table's
size, build cost, or matching rate below.

## 4. Algorithm

**Advice.** S's Step 1 finds one valid through-step-13 solution, fixes the state/message words below from that
solution, and builds its TAB2 and published collision pair from it. The scored advice is that exact fixed solution,
recovered as the unprimed values of the published pair at its 35-step CV1; it is not replaced by another SAT output:

```
A4..A13 = 98560dbb 633b16ba 9bcf7bbe f8677ad6 4a299906 44f24ab5 39781650 6422edc8 574542b8 0508c8f0
E8..E13 = f1cae594 d0e1b7b4 bf27d74c b78bbfd9 3fffd0f9 bf81c0f4      W12, W13 = 41b22a2c 6d12f88a
```

Primed fixed words are X xor FL(X). fixX(i) means that X_i satisfies its printed single-bit conditions (0, 1,
n -> 0, u -> 1).

**P1.** L4 is every E4 with fixE(4) and E4[10] != E4[15]. L7 is every W7 with fixW(7) and its six two-bit
conditions.

**P2 (combinations).** For each (E5, E6, E7) with fixE(5..7):
- compute A3 = E7 - A7 + Sigma0(A6) + MAJ(A6,A5,A4), then A2 and A1 likewise from E6 and E5;
- compute W9..W11 from the E-equations of steps 9..11.

Keep the combination iff all of these hold:
- fixA(1..3) and fixW(9..11);
- XOR-conformance of A at steps 5..13 and of E at steps 9..13;
- the two-bit conditions among A1..A13, E5..E13 and W9..W13.

**P3 (TAB2).**
- E4 loop. For each combination and each E4 in L4, compute A0 = E4 - A4 + Sigma0(A3) + MAJ(A3,A2,A1) and
  W8 = E8 - A4 - E4 - Sigma1(E7) - IF(E7,E6,E5) - K8. Require fixW(8), fixA(0), XOR-conformance at A4 and E8, and the
  new two-bit conditions.
- W7 loop. For each W7 in L7, compute E3 = E7 - A3 - W7 - Sigma1(E6) - IF(E6,E5,E4) - K7 and
  A[-1] = E3 - A3 + Sigma0(A2) + MAJ(A2,A1,A0). Require fixE(3), fixA(-1), XOR-conformance at A3 and E7, and
  sigma0(W8') + W7' = sigma0(W8) + W7 (zero W23 difference).
- Storage. A record is 16 bytes: A[-1] and three indices. Records sit in one array bucketed by all 32 bits of
  A[-1]. A counting pass gives the offsets, and a placing pass fills the array in place.

**P4 ((W14, W15) list).**
- Enumerate E14 with fixE(14). Compute A14 = E14 - A10 + Sigma0(A13) + MAJ(A13,A12,A11), and keep it if fixA(14) and
  its two-bit conditions with A13 hold.
- Then enumerate E15 with fixE(15). Keep it if fixA(15), A13[29] != A15[29], and XOR-conformance at steps 14 and 15
  hold.
- W14 and W15 follow from the E-equations.

**Main loop.** T trials and a work cap W_cap (Section 8). In each trial:
1. Draw M0 as 16 fresh uniform words and compute CV1 = C_32(IV, M0).
2. **Step 2.** Scan the bucket of CV1[0]. For each record with A[-1] = CV1[0]:
   - compute E0..E2 from the A-equations (A[-4..-1] from CV1) and W0..W6 from the E-equations;
   - accept, aborting early in this order, iff:
     - (a) W4 has its sign value;
     - (b) sigma0(W4') + W12' = sigma0(W4) + W12;
     - (c) W5 has its three sign values;
     - (d) W6 has its sign value;
     - (e) E is XOR-conformant at steps 0..6 and A at steps 0..2;
     - (f) sigma0(W6') + W5' = sigma0(W6) + W5;
     - (g) (W13' - W13) + (sigma0(W5') - sigma0(W5)) + (W4' - W4) = D(W20).
3. **Step 3.** Subject to the cap checks in item 4, the algorithm evaluates valid tuples in fixed scan order. For each
   valid tuple, spend at most 128 of the 300 setup operations computing the common
   `c16 = W9 + sigma0(W1) + W0`, `c17 = W10 + sigma0(W2) + W1`, and the twelve cached
   `W16 = c16 + sigma1(W14)` values, one for each W14 group; the remaining 172 setup operations cover tuple/P4
   administration. For each P4 entry, set M1 = W0..W15 and
   M1' = M1 xor FL(W). For i = 16..31,
   with early abort:
   - require W'[i] = W[i] xor FL(W[i]) and the sign values of W20 and W22;
   - for i <= 22, also require XOR-conformance of A[i] and E[i]. Steps 14-15 depend only on the advice and the P4
     entry, so each P4 row stores W14, W15, their two `sigma1` values, the four offsets `E16-W16`,
     `E16'-W16`, `A16-E16`, `A16'-E16'`, and the four unprimed states A14, A15, E14, E15: twelve 32-bit words,
     built in P4 and charged in C. The primed step-14/15 states follow by XOR with their fixed difference masks.
     Since W0, W1, W2, W9, W10, W14 and W15 have zero difference, the W16 and W17 row equalities are automatic.
     Stage 16 loads the cached common W16 and forms both E16/A16 branches with four modular additions before the
     two cross-branch A/E tests. A candidate
     that fails stage 16 stops before stage 17, and one that fails stage 17 stops before stages 18..31.
   If everything passes, recompute both full 3-block 32-step digests. If they are equal, output the pair and stop.
4. Once the bucket length is known, the fixed per-trial work reserves the whole `5 * occupancy` scan envelope with
   one cap check, rather than checking each record. Before every later Step-2 tranche, tuple setup or Step-3 tranche,
   the algorithm checks whether the advertised envelope would exceed W_cap. A successful check is included in the
   envelope it authorizes; if a check fails, the algorithm stops before that tranche and charges the one final
   rejected check separately as at most eight operations. The counter therefore never exceeds W_cap. It also stops
   after T trials.

Every output is verified by recomputation, so correctness is unconditional.

## 5. Measured attack rates (public source submission's C code, fresh seeds)

This section reports participant runs on an i5-14400F with gcc -O3. The predicates are those of Section 4.

**Exact counts.** Every count equals the corresponding count in #26:
- L4 = 131,072 and L7 = 524,288;
- combinations = 10,240 of 2^32;
- (combination, E4) pairs = 155,008;
- N = |TAB2| = 1,396,774,912 ≈ 2^30.3795;
- P4 = 196,608 = 12 * 2^14 ≈ 2^17.585.

The 2^27-bucket layout has mean occupancy 10.41 and **maximum occupancy 936**. The A[-1] values repeat. The 2^32-bucket
layout of this version (Section 4, P3) refines it: every 32-bit bucket lies inside one 27-bit bucket, so its maximum
occupancy is also at most 936, and its mean over a uniform key is exactly N / 2^32 = 0.325212. Splitting
TAB2 into four parts by combination index mod 4, the sum over parts of sum_v c_v^2 (c_v = multiplicity of value v)
is 5.758e9.

**Self-test.** The published tuple is in TAB2, and with its 35-step CV1 it passes Step 2, reproducing
W0..W6 = M1'[0..6]. Its (W14, W15) is in P4. Exactly 1 of its 196,608 Step-3 candidates, the published one, passes
every stage.

**Analytic q.** For a fixed tuple, the CV1 words b, c, d make E2, E1, E0 successively uniform. So W4 and W5 are
uniform, and W6 = Y_t - E2 with Y_t = E6 - A2 - Sigma1(E5) - IF(E5,E4,E3) - K6.
Tests (a), (b), (c), (f), (g) pass with probability 1/2, 1/8, 1/8, 1/8, 1/8; step-6 conformance is a property of
the tuple and step-5 conformance depends only on E2[29].

Exact enumeration of TAB2 (#26's method, re-implemented): 609,229,824 tuples pass the step-6 test, and
sum_t Pr[E2[29] = e*(t), W6[29] = 0] = 214,235,406.9. So q_pred = 2^-45 * 214,235,406.9 = 2^-17.3254.

**Measured q.** Four runs, one per table part, each with 2^32 C_32 first blocks (seeds 2026001..4; #26 used other
seeds):

```
part   matches       valid   predicted
0      346,111,249   6,259   6,269.6
1      274,971,829   5,250   5,405.5
2      366,391,076   6,352   6,341.6
3      409,252,134   8,075   8,135.2
```

q (sum of per-part rates) = 2^-17.3373 (rel. sd 0.62%), **99% LCB 2^-17.3583236**, UCB 2^-17.3166. Matches per trial
0.32520; the table-cardinality upper bound used for work is N/2^32 = 0.3252120018... < 0.32522. Pass fractions (a)..(g): 0.5000, 0.1250, 0.1250, 0.4999, 0.3065, 0.1249, 0.1241
(predicted 1/2, 1/8, 1/8, 1/2, 0.3068, 1/8, 1/8). Two valid tuples in one part: 9 of 2^34 part-trials. #26's runs:
2^-17.3337; #227's campaign counts: 14,643,237 tuples / 2.405e12 first blocks = 2^-17.326.

The pooled estimate sums the four part rates, so `q_hat = 25,936 / 2^32`. Treating the four rare-event counts as
independent Poisson counts, the one-sided normal 99% LCB is
`(25,936 - 2.32635 sqrt(25,936)) / 2^32 = 2^-17.3583236`. We round downward and declare **q >= 2^-17.3584**.
This confidence construction and the CV1-uniformity assumption are part of the declared `q-32step-matching-rate` premise.

**Step-3 stage rates.** The 25,936 valid tuples are accepted TAB2 record occurrences pooled across the campaign;
repeated logical values at different record positions count as separate occurrences. Thus 25,936 * 196,608 ≈
2^32.248 candidates. Cumulative passes: st16 2^-3.000, st17 2^-15.000 (155,619), st18
2^-21.03 (2,379), st19 2^-27.79 (22), st20 2^-29.93 (5), st21 2^-32.25 (1), st22 0.
The exact measured stage-17 fraction is
`155,619 / (25,936 * 196,608) = 2^-14.999972...`; the time bound uses the larger upper envelopes
`f16 <= 0.126` and `f17 <= 2^-14.9`. This transfer of the participant campaign to the scored early-abort work is part of the declared
`attack-work-moments` premise.

The condition count predicts 2^-3, -15, -21, -28, -32, -33. The mapping:
- step 17 consumes E16's conditions;
- step 18 conforms iff E18[29] = 1, because IF(E17,E16,E15) absorbs the other differences;
- step 19 needs the unprinted E16[29] = E17[29], which the pair satisfies;
- step 20 needs W20's signs and E19[29] = 0, since D(E16) + D(W20) = 0;
- step 21 needs E20[29] = 1;
- the remaining 9 W20 and 4 W22 carry conditions are tested at stage 22 and in W23..W31.

That is 45 printed conditions + 1. The declared `step3-46-conditions` heuristic premise treats those conditions as
having sufficient uniformity and independence to give **p >= 2^-46 per candidate**. The stage measurements do not
observe a full late-stage pass, so the condition count alone is not a proof of this rate.

## 6. The characteristic: public algorithm text, with the measured search as fallback evidence

### 6.1 What is used, and what is charged

| Input taken from S | Kind | Treatment |
|---|---|---|
| signed rows of Fig. 6 (Section 2) and the two-bit conditions under the stated readings | a table of conditions; no message word, chaining value or state value | public algorithm text, not charged (`public-characteristic`); stored within the 2^13-byte advice bound |
| the exact Step-1 starting solution | value-level advice | charged: D = 2^35 (Section 8) |
| tables P1-P4, first blocks, valid tuples, second blocks | value-level objects | computed and charged: C (Section 8.1), A + B (Section 8) |

**The cost model's omitted-search rule.** collision-frontier-v5 states: "All construction/preprocessing and advice
must be accounted for, including any search omitted from the submitted program." We read the rule as applying to every
object the program stores or consumes as a value: a stored collision, first block, starting solution or table must be
paid for even when the search that produced it is not part of the program. Every such object here is paid for: the
starting solution, the only value-level object taken from S, is charged as D; the tables as C; first blocks, tuples and
second blocks online. The characteristic is not a value the program consumes; it is the specification of the program
(which bits Step 2 and Step 3 test), printed in a peer-reviewed publication and restated in full in Section 2. Charging
the historical research that discovered a published attack specification would equally require charging the discovery
of every published differential, message-modification technique or table layout that any submission uses; the cost
model does not price attack design.

This is the convention of the organizer-accepted SHA-256 r31 package `50592e75` (37.22), at
`lanes/exploratory/candidates/sha256-r31/claim.json` `/heuristics/0` on the organizer branch. Its heuristic
`H1-public-characteristic` states that the published 31-step signed characteristic "is public algorithm text that C may
use without charging its original discovery. It is not a collision and contains no message words, chaining values or
state values", while every value-level object is computed and charged. Same target family, cost model and lane.

The characteristic is also reproducible from public tooling: the completed re-run of S's own procedure below returned
signed rows equal to Fig. 6. Under `public-characteristic` its cost is not part of the claimed total.

### 6.2 The measured re-derivation (fallback evidence only)

S reports no running time for the characteristic search. Public submission `8bad82c1-1950-4e17-a025-bacdf5dda6ce`
(PR #396) continued the measured rerun of S's procedure until it produced S's characteristic. The measurement and
ledger below are credited to that submission; they enter only the fallback figure.

**Tooling and model.** The authors' library Peace9911/sha_2_attack (commit 6a9f35f,
`configuration/unit_function_256.py` unmodified: signed-difference models of the step functions and expansion, and
the exact value model `sha2_value`), with STP 2.3.4 (sha d7008546) + CryptoMiniSat 5.11.21, called as
`stp model.cvc --cryptominisat --threads N` (the authors use 26). Each call ran under `/usr/bin/time -v` (user+system
CPU over all threads, peak RSS). The run re-parametrised the authors' 31-step FunctionModel: steps 4..22, expansion
W16..W34, differences only in W4..W8, W12, W13, W20, W22, zero A/E differences at steps 0..3, zero A at 15..22, zero
E at 19..22, the authors' rule for exact sums (op2 = 1 for E at steps >= 19, op5 = 1 for A at >= 15), the 31-step
hard-coded weights removed, and the objective as `BVPLUS(12, difference bits) <= k`. With every Fig. 6 row asserted,
the calibration model is SAT (29 CPU-s), so it admits S's characteristic.

**Procedure.** S's Steps 1-4: (1) minimise tw; (2) with nabla W fixed, minimise tE; (3) with tE fixed, lower tA
until UNSAT; (4) with tE, tA fixed, minimise tE4. Each lowers a `<=` threshold until UNSAT; a call at its wall cap
is charged and leaves the step unproven. Step 1 descended linearly; Steps 2-4 switched to bisection to fit the window.
The measured Step-1 optimum is a different weight-22 pattern from S's; a relaxation fixing only the weight was
abandoned after 50 minutes and charged. Steps 2-4 therefore fixed nabla W to S's rows. Steps 3-4 ran concurrently
under tE = 6 and tA = 21. Step 2 returned tE = 6, and Step 3 proved tA = 19, below S's 21; S's characteristic is
therefore not the plain Step-3 optimum of this relaxed model. Step 4 kept S's threshold tA <= 21, which admits it.
After the first window, Step 4 was resumed with 8-hour caps: a call at <= 111 (6 threads) timed out, while a call at
<= 76, S's weight, (8 threads) returned SAT.

| Phase | Calls | Results (S = SAT, U = UNSAT, T = timeout, A = abandoned) | CPU-s | Wall s | Peak RSS | Optimum found | Published |
|---|---|---|---|---|---|---|---|
| calibration (Fig. 6 asserted) | 2 | ES | 29 | 27 | 1.96 GiB | - | - |
| Step 1: min sum H(nabla W) | 19 | SSSSSSSSSSSSSSSSSSU | 29,649 | 3,463 | 1.43 GiB | 22 (proved) | 22 |
| Step 2 relaxation (weight only) | 1 | A | 27,613 | 3,022 | 5.25 GiB | - | - |
| Step 2: min tE (nabla W fixed) | 18 | SSSSSSSSSSSSSESUUS | 68,857 | 10,012 | 4.57 GiB | 6 (proved) | 6 |
| thread-count change stub | 1 | A | 2 | 1 | 0.00 GiB | - | - |
| Step 3: lower tA (tE fixed) | 10 | SSSESUSSSU | 35,603 | 10,409 | 2.62 GiB | 19 (proved) | 21 |
| Step 4: min tE4 (tE, tA fixed) | 8 | SETSESTA | 432,105 | 72,708 | 4.26 GiB | 76 (not proved) | 76 |
| **all search calls** | 59 | | **593,858** | 99,644 | 5.25 GiB | | |

Steps 1-2 reached S's optima (22, 6) with proofs; Step 3 proved 19 in the relaxed model; Step 4 at tA <= 21 reached
76, S's value. The <= 78 and <= 111 calls timed out although Fig. 6 satisfies them; they are charged. `M_E` counts
every search call.

**Exact starting solution construction (`starting-solution-cost`).** S Sect. 4 first finds one valid solution
through step 13, then fixes the state and message words based on that solution and constructs TAB2. Its complexity
evaluation reports approximately `2^34.3` for finding this Step-1 solution, and its experimental verification uses
the resulting tuples to obtain the published Table 3 pair. Section 4 above extracts the exact fixed words from that
published lineage. We charge **D = 2^35 = 34,359,738,368 target-compression units**. If the unstated source unit is
one full 35-step compression, collision-frontier-v5 converts the report to
`ceil(2^34.3 * 2476/2224) = 23,547,494,749 < 2^35`, leaving a factor `1.459...`; here
`2476 = 2224 + 3*84` charges the three additional expanded steps. This charge applies directly to the exact fixed
advice used by the scored table and rate measurements. The source does not state its unit or provide the historical
execution trace, so the conversion and its `1.459...` margin remain a declared heuristic.

The two local exact-value-model runs from #296 took 534.1 and 374.7 CPU-s and returned other checked solutions; they
corroborate the task scale only. Their outputs are not substituted for the published fixed solution, and no table
cardinality, matching rate or work distribution is transferred from one starting solution to another.

**CPU-second price kappa = 2^23 units < 2^34.12 primitive operations per CPU-second** (the value accepted in
PR #396 and used in #367, #377 and #134). Its calibration call took 40.42 native CPU-s and retired
44,197,378,388 instructions under callgrind with identical output: **2^30.03 instructions per CPU-second**, so kappa
allows 17 primitive operations per instruction. Opcode mix was divide 0.305%, floating point 0.085%, multiply 0.026%,
unmapped 7.24%, ordinary integer 92.3%. Pricing ordinary and unmapped instructions at 5 operations and
divide/multiply/floating point at 400 gives 6.6 <= 17. The unmapped instructions were identified as ordinary PLT
stubs; the slack is 17/6.6 = 2.57x. The call was repeated three times natively (40.42, 41.07 and 41.10 CPU-s).
It is single-thread while charged calls were multithreaded, whose lower IPC makes this conversion conservative.
The kappa = 2^24 row below is the fallback.

**Result: the search outputs S's characteristic.** The <= 76 call returned
`(tw, tE, tA, tE4) = (22, 6, 21, 76)`, and every signed row A0..A22, E0..E22 and W0..W34 is identical to Fig. 6.
Thus the measured run constructs the characteristic used by the attack, conditioned on S's nabla W and published
thresholds; blind re-derivation is priced below. Its peak was 4.26 GiB. S's 35-step pair and the #227 32-step pair
both conform to this characteristic, and the inherited q and p campaigns were measured for it.

**Fallback price.** E = 32 * M_E * kappa, with M_E = 593,858 CPU-s over all 59 calls. Every calibration, abandoned,
stopped and timed-out call is charged, including the 174,445 CPU-s final Step-4 call and its 172,129 CPU-s timed-out
sibling. CPU-s already sum over threads, so no thread factor is added. The factor 32
(`route-search-measured`) is a blind-rediscovery factor of about 8 times a residual safety factor 4:
- *Rediscovery (about 8 M_E).* The blind arm descending from <= 111 timed out after 172,129 CPU-s. Priced from the
  run ledger at the 8-hour by 8-thread cap (230,400 CPU-s per call), a blind Step 4 at one tA level costs 1.2-1.6M
  CPU-s. Re-deriving tA = 21 after the relaxed optimum 19 requires Step 4 at three tA levels. Adding Steps 1-3 and
  calibration gives 3.8-5.0M CPU-s, or 6.3-8.4 M_E.
- *Residual x4.* A factor 2 covers run-to-run variance of the parallel SAT portfolio (one concurrent Step-4 call
  succeeded while the other timed out at similar CPU); another factor 2 covers S's exploratory models and the
  choice among weight-22 nabla-W patterns (the measured Step 1 found a different one).

The rediscovery factor is priced from the ledger rather than executed; S's own historical time is unpublished, and
76 was reached but not proved optimal. Numerically,
`32 * 593,858 * 2^23 = 159,412,543,029,248 < 2^47.179759` units. This figure is **not** in the claimed total. With
it, the total would be 169,957,495,949,422 = 2^47.2721673216 (f310d44f's claim); with M_E at 2^23 and no rediscovery
factor, 2^43.8198.

## 7. Success probability

Let `s` be the probability that one counterfactual uncapped trial finds a collision. The `T` trial inputs are
independent, so if `U` is the event that at least one of the `T` uncapped trials succeeds, then
`Pr[U] >= 1 - exp(-sT)`. Let `V` be the number of valid tuples in one trial, with `E[V] = q`. The pointwise inequality
`1[V >= 1] >= V - C(V,2)` gives

```text
Pr[V >= 1] >= q - E[C(V,2)] >= q(1 - 2^-5).
```

- **E[C(V,2)] <= q * 2^-5 (`valid-tuple-pairs`).** Within-part pairs were 9 in 2^34 part-trials, i.e. 2^-28.8 per trial, against
  0.75 expected for independent records. Applying that correlation factor (12) to the Cauchy-Schwarz bound on
  cross-part pairs gives 2^-26.8. The charge is more than 20x the total.
  It also supplies relevant, but nonconclusive, support for the selector transfer. Since `1[V >= 2] <= C(V,2)`,
  `Pr[V >= 2 | V >= 1] <= (q/32)/(31q/32) = 1/31`. Since `V 1[V >= 2] <= 2 C(V,2)`, at least `15/16` of the
  occurrence-weighted tuple mass comes from singleton trials. The occurrence- and trial-weighted selectors coincide
  on singleton trials. These bounds cannot exclude concentration of the very rare Step-3 successes in the remaining
  multi-tuple trials, so they support relevance but do not prove the selected-tuple rate.
- **Generic Step-3 rate (`step3-46-conditions`).** Draw a valid tuple uniformly from the pooled accepted record
  occurrences of fresh trials, i.e. the occurrence-weighted distribution, and let `Y` be its number of conforming candidates.
  Then r >= E[Y] - E[C(Y,2)], where `E[Y] = 196,608 * 2^-46 = 3 * 2^-30 = 2^-28.4150375`. Candidates share W14
  in 12 groups of 2^14, and W20's 12 conditions are common within a group. Thus E[C(Y,2)] <=
  12 C(2^14,2) 2^-12 (2^12 p)^2 + C(196,608,2) p^2 <= 2^-49.3, so
  `r >= 3 * 2^-30 (1 - 2^-20)`.
- **Selected-tuple transfer (`selected-valid-tuple-success-transfer`, declared heuristic).** Conditional on `V >= 1`,
  use an analysis-only auxiliary seed sampled independently after the trial to choose `J` uniformly from its `V`
  accepted record occurrences. Define `Y_J = 0` when `V = 0`.
  The declared premise is `Pr[Y_J >= 1 | V >= 1] >= r`: conditioning on tuple existence and making this trial-wise
  selection preserves the generic Step-3 lower bound. Pooled stage measurements do not establish that transfer, and
  tuple multiplicity may correlate with Step-3 success. The selector adds no coins or work to the submitted algorithm. Since
  the counterfactual uncapped trial tests every valid tuple, success through `J` is a subset of uncapped-trial success.
  The premise is score-critical and is not inferred from the pair bound. Under it, with no independence assertion,

```text
s >= Pr[V >= 1 and Y_J >= 1]
  = Pr[V >= 1] Pr[Y_J >= 1 | V >= 1]
  >= q(1 - 2^-5) r.
```

Let `H = {sum_i X_i <= 162.5 T}`. On `U intersect H`, the capped algorithm reaches that collision, so
`Pr[actual success] >= Pr[U] - Pr[not H]`; no independence between these events is needed. Now
s >= 2^-17.3584 (1 - 2^-5) (3 * 2^-30) (1 - 2^-20) = 2^-45.8192425647... > 2^-45.820. This
revision retains the full displayed product rather than discarding it in the final rounding. With
T = 30,702,387,450,972 (2^44.80342), it gives sT > 0.494544934010. Subtracting the cap-stop
probability from Section 8 by a union bound gives

**P > 1 - e^-0.494544934010 - 5.561e-5 > 0.390096 > 0.39 claimed.** This calculation depends on the generic
46-condition Step-3 premise, the explicit selected-tuple transfer and the independence assumptions disclosed below;
one additional independent condition would put this smaller T below the minimum, so that uncertainty is material.
The margin over 0.39 is arithmetic under those premises, not evidence that they are robust.

The deterministic certificate proves an exact collision exists for the fixed route; it does not by itself establish
the fresh-trial probability used here.

## 8. Time (units, C = 2224)

Charges: a load, store, add, logic op, shift, compare or branch is 1 operation; a rotation is 4; Sigma/sigma is 14;
a mod-2^32 add is 2.
In Step 2, Step 3 and table precomputation (`B` and `C`), every counted 32-bit action consumes a full primitive
256-bit word-operation charge with no packing credit. In `A` (first-block evaluation of `C_32(IV, M0)`), the algorithm
packs seven strictly independent uniform trials (`l = 0..6`) into seven 36-bit lanes (`[36l+35 : 36l]`, occupying
`7 * 36 = 252 <= 256` bits) of a 256-bit word, with the low 32 bits `[36l+31 : 36l]` holding the lane's 32-bit value
and the upper 4 bits `[36l+35 : 36l+32]` acting as 4 guard bits that absorb up to 15 modular additions without carry
across a 36-bit lane boundary. Each modular addition in a lane is therefore a **single primitive 256-bit addition
(`1` operation)** rather than a 6-operation MSB-cleared addition, and masking with `M = sum_{l=0}^6 (2^32 - 1) << 36l`
(`1` operation) is needed only once per newly formed schedule word, state update, or feed-forward output before
subsequent right shifts/rotations. `experiments/replay.py` expresses both this 7-lane 36-bit guard-bit construction
(counting every primitive 256-bit operation via `Swar7Counter`) and the 8-lane carry-save construction, checking both
bit-for-bit against scalar `C_32` evaluations on organizer-generated inputs.

**A. Fixed work per trial, T = 30,702,387,450,972 trials
(`B_7 = ceil(T/7) = 4,386,055,350,139` batches).** Each batch draws 16 independent uniform 256-bit words (`16` `RAND`
operations) and masks each word with `M` (`16` `AND` operations). Because the seven 32-bit intervals `[36l, 36l+31]`
(`l = 0..6`, `36 * 6 + 31 = 247 < 256`) are disjoint bit slices of each uniform 256-bit word, the `7 * 16 = 112`
lane values form seven mutually independent uniform 512-bit first blocks, with all guard bits `[36l+35 : 36l+32]`
zeroed. The final batch has four unused lanes; its full cost is charged and only the first `T` trials enter the
success calculation.

The fixed public lane masks (`M`, two shift masks `SHR_MASKS7[k]` for `k in {3, 10}`, and ten rotation mask pairs
`ROTR_MASKS7[r]` for `r in {2, 6, 7, 11, 13, 17, 18, 19, 22, 25}`) and the 36-bit-lane-replicated SHA-256 constants
(`IV7` and `K7`) are loaded during batch setup. For any word `X` whose 36-bit lanes satisfy `0 <= lane < 2^32`
(i.e. guard bits `32..35` are `0`), the submitted word-RAM data path implements:

- `SHR36x7(X, k) = (X >> k) & SHR_MASKS7[k]` in **2 operations** (1 shift, 1 AND), outputting `< 2^32` in every lane.
- `ROTR36x7(X, r) = ((X >> r) & m_lo[r]) | ((X << (32 - r)) & m_hi[r])` in **5 operations** (2 shifts, 2 ANDs, 1 OR),
  outputting `< 2^32` in every lane (with guard bits `32..35` cleared by `m_lo[r]` and `m_hi[r]`).
- Thus `small_sigma0` and `small_sigma1` each cost `5 + 5 + 2 + 2 = 14` operations, and `big_sigma0` and `big_sigma1`
  each cost `5 + 5 + 5 + 2 = 17` operations, with every output satisfying `0 <= lane < 2^32`.
- `IF(e, f, g) = (e & f) ^ ((e ^ M) & g)` in **4 operations** (since `e < 2^32` in each lane, `e ^ M` complements
  bits `0..31` and leaves guard bits `32..35` zero, so no extra mask is needed), and `MAJ(a, b, c) = (a & b) ^ (a & c) ^ (b & c)`
  in **5 operations**, both outputting `< 2^32` in every lane.
- In the message schedule (`i = 16..31`), `W[i] = (small_sigma1(W[i-2]) + W[i-7] + small_sigma0(W[i-15]) + W[i-16]) & M`:
  since the four summands are each `< 2^32`, their sum is `< 4 * 2^32 < 2^34 < 2^36` (never crossing a 36-bit lane
  boundary) and takes **3 additions + 1 `AND M` = 4 operations** after the two small sigmas (`14 + 14 + 4 = 32`
  operations per word, `16 * 32 = 512` operations for `W16..W31`).
- In each compression round (`i = 0..31`), `t1 = h + big_sigma1(e) + IF(e, f, g) + K7[i] + W[i]` is the sum of five
  lane-bounded words (`< 5 * 2^32 < 2^35 < 2^36`, **4 additions**); then `e_new = (d + t1) & M` (`< 6 * 2^32 < 2^36`,
  **1 addition + 1 `AND M` = 2 operations**) and `a_new = (t1 + big_sigma0(a) + MAJ(a, b, c)) & M` (`< 7 * 2^32 < 2^36`,
  **2 additions + 1 `AND M` = 3 operations**). Thus one compression round costs exactly:
  `17 (Sigma1) + 4 (IF) + 17 (Sigma0) + 5 (MAJ) + 4 (t1 adds) + 2 (e_new) + 3 (a_new) = 52 operations`,
  and all 32 rounds cost `32 * 52 = 1,664 operations`.
- In feed-forward (`j = 0..7`), `out[j] = (IV7[j] + state[j]) & M` (`< 2 * 2^32 < 2^36`, **1 addition + 1 `AND M` =
  2 operations per word**, `8 * 2 = 16 operations` in total).
- Extracting the `7 * 8 = 56` scalar 32-bit `CV1` words takes at most `56 * 2 = 112` shift/mask operations.

Every operation above is counted and asserted in `Swar7Counter` inside `experiments/replay.py`:

| SWAR batch component (7 lanes of 36 bits) | Primitive 256-bit word operations (`Swar7Counter`) |
|---|---:|
| 16 independent random words + 16 lane-mask `AND M` ops | 16 `RAND` + 16 `AND` = 32 |
| W16..W31 schedule | 16 * (2*14 sigma + 3 `ADD` + 1 `AND M`) = 16 * 32 = 512 |
| one compression round | 17 Sigma1 + 4 `IF` + 17 Sigma0 + 5 `MAJ` + 7 `ADD` + 2 `AND M` = 52 |
| all 32 compression rounds | 32 * 52 = 1,664 |
| eight feed-forward words | 8 * (1 `ADD` + 1 `AND M`) = 16 |
| extract 56 scalar CV words | 56 * (1 `SHR` + 1 `AND`) = 112 |
| **arithmetic/randomness subtotal** | **2,336** |

The submitted straight-line 7-trial batch is capped at **2,928 operations**. The batch is one fixed straight-line
block with no loop, so its traffic is loads, stores and the address arithmetic that puts each load or store address in
a register; there is no loop control inside it. Each row below counts one address operation per load or store, in
addition to the load or store itself (the convention that only shift counts are immediates):

| Batch overhead | Operations |
|---|---:|
| public vector/mask/IV setup and stores of the 16 random words (unchanged) | 96 |
| schedule traffic: four source loads, one store and three address operations per new word (unchanged) | 16*8 = 128 |
| round traffic: per round, one `K7[i]` load and one `W[i]` load, each with one address operation | 32*4 = 128 |
| feed-forward: eight IV loads and eight vector-result stores, each with one address operation | 32 |
| 56 scalar-CV stores, each with one address operation | 112 |
| **traffic subtotal; full itemized total** | **496; 2,336 + 496 = 2,832** |

The eight state vectors and round temporaries remain registers, so advancing `(a,b,c,d,e,f,g,h)` is renaming; the
fixed masks and IV vectors load once in the setup row. The cap adds **96 reserve** above the itemized 2,832
(`2,832 + 96 = 2,928`) for base-register setup and the batch's entry and exit. Relative to `1dcd606`/`f310d44f`
(3,232), the round row drops the ten per-round "address/control allowances", which priced loop control that
straight-line code does not execute, and the feed-forward and extraction rows drop allowances beyond one address
operation per access. The 2,336 arithmetic count is unchanged and is the one `Swar7Counter` verifies in the replay.

Separately, every one of the `T` used trials receives **32** operations for lookup and control. Itemised, with one
address operation per memory access: load the trial's scalar `CV1[0]` (address, load: 2); form the offset-cell
address `base + 4 CV1[0]` (shift, add: 2); load the two offsets `off[k]`, `off[k+1]` (address, load, address, load:
4); occupancy `off[k+1] - off[k]` (1); the scan envelope `5 * occupancy` (shift, add: 2); add it to the counter,
compare with the cap, branch (3); empty-bucket branch (1); trial counter increment, compare and branch (3). That is
18; 32 are charged. The random words are drawn in the batch (Section 8 A), so the former 34-operation random-word
margin is not needed. A zero-length bucket and the cap check itself are both charged.

**B. Counted work, capped.** Charges:
- each scanned record: 5;
- Step 2 per matching record: 160 (decoding the tuple, E0..E2, W4 and test (a)), +40 if (a) passes, +40 if (b),
  +40 if (c), and <= 1024 if (d) passes (W0..W3, the primed steps 0..6, W20, W21); at most 1304 in total;
- Step 3 per valid tuple: 300. Of this, at most 128 covers `c16`, `c17` and the twelve per-W14-group W16 cache
  entries, and 172 covers all other tuple/P4 administration. The 128-operation part is explicit: the six common
  input loads, two sigma calls, four modular additions and two stores for `c16` and `c17` cost 44; twelve
  sigma-value loads, modular additions and W16 stores cost 48; and 36 remain for group indexing and control. Per
  candidate, the charged envelopes are 48 for stage 16; 256 for stage 17, paid
  only by the fraction `f16` that passes stage 16; and 2048 for stages 18..31 and final candidate tests, paid only
  by the cumulative fraction `f17` that passes stage 17.

The tranche ledger is deliberately scalar and charges both branches:

| Tranche | Audited subtotal and charged envelope |
|---|---:|
| tuple setup/cache | <= 128 cache computation/stores + 172 tuple/P4 administration = 300 |
| stage 16 | 5 cached-word loads + 8 for four modular additions + 10 for two exact A/E row tests + 9 index/control = 32; **charge 48** |
| stage 17 after stage-16 pass | 2 for the common W17 modular addition + 110 for two SHA-256 steps + 10 for two exact A/E row tests + 52 state/P4 traffic + 20 control = 194; **charge 256** |
| stages 18..31 after stage-17 pass | 28 schedule words * 34 + 10 SHA-256 steps * 55 + 24 row tests * 5 + 244 traffic/control = 1866; **charge 2048** |

A schedule word costs at most `14 + 14 + 3*2 = 34` (two small sigmas and three mod-adds). One SHA-256 step costs
at most 55 after expanding the big sigmas, four-operation IF, MAJ, modular additions and state updates. An exact row test receives
five operations. The stage-17 traffic allowance includes loading A14, A15, E14 and E15, deriving their primed
values with the fixed XOR masks, and retaining the stage-16 state. The 244-operation residual in the last tranche
also covers the W20/W22 sign-mask tests. The charged envelopes leave respectively 16, 62 and 182 operations above
the displayed subtotals and take no SIMD, shared-branch, or compiler credit.

With the 2^32-bucket scan mean N / 2^32 = 0.325212 (Section 5), the measured rates (matches per trial < 0.32522,
Step-2 pass fractions 1/2, 1/16, 1/128, 1/256, q_UCB = 2^-17.3166), and conservative `f16 = 0.126`, `f17 = 2^-14.9`
above:

E[X] <= 5(0.325212) + 0.32522(192)
       + q_UCB(300 + 196,608(48 + 256 f16 + 2048 f17))
     = 1.626 + 62.442 + 96.746 < 160.815 < 160.82.

(The 2^27-bucket layout of earlier versions had the scan term 5(10.41) = 52.05 and E[X] < 211.3.) Every Step-2 and
Step-3 charge is unchanged; only the number of scanned records changes, and with full-key buckets every scanned record
is a key match.

For the cap analysis, let `X_i` be the counterfactual uncapped Step-2/3 work demand of independently pre-sampled
uniform first block i, excluding the fixed batch work, fixed 32 per-trial operations and final 14-unit allowance. Conditional on the fixed,
successfully built tables, the `X_i` are independent deterministic functions of the independent first blocks.
The cap is **W_cap = 162.5 T**, so its distance above the mean is at least 1.68 T.

The inherited moment calculation gives E[X_i^2] <= 3(E[scan^2] + E[S2^2] + E[S3^2]):
- E[scan^2] <= 25 * 936 * 0.325212 (E[occ^2] <= max occ * E[occ]);
- E[S2^2] <= 1304^2 * 4 * 5.758e9 / 2^32;
- E[S3^2] <= (300 + 196,608 * 2352)^2 * q_UCB(1 + 2^-4). This deliberately charges every candidate
  the full 48 + 256 + 2048 operations; the multiplicity factor is inherited unchanged.

The displayed terms sum below `4.176e12`; we round upward to E[X_i^2] <= 4.18e12. The inherited full-table
participant enumeration reports exact maximum bucket occupancy 936, and the fixed builder below asserts that bound
before prefix construction. The maximum Step-3 demand of one record is

```text
S3_max = 300 + 196,608(48 + 256 + 2,048) = 462,422,316,
M = 5(936) + 936(1,304 + S3_max) = 432,828,513,000.
```

Thus `0 <= X_i <= M`. Let `m_i = E[X_i]` and `Z_i = X_i - m_i`; then `|Z_i| <= M`,
`sum m_i <= 160.82 T`, and `sum Var(X_i) <= T * 4.18e12`. A cap stop implies that the counterfactual uncapped
total exceeds `162.5 T`, hence `sum Z_i >= 1.68 T`. One-sided Bernstein gives

```text
Pr[stop at cap]
 <= exp(-(1.68 T)^2 / (2(T*4.18e12 + M*(1.68 T)/3)))
 < exp(-9.7972517744)
 < 5.561e-5.
```

This is larger than the 2.33e-11 of the 214 T cap, and Section 7 subtracts it in full. The cap and T were chosen
together: the smallest T that keeps the success bound above 0.3901 at each cap, minimising total work.

Equality at the cap is allowed; a tranche is rejected only if it would exceed the cap. The occupancy assertion's
success is a score-critical part of `attack-work-moments`; the organizer replay does not validate the full table. If
the fixed table has a bucket above 936, preprocessing aborts and the success claim fails instead of applying Bernstein.

With `B_7 = 4,386,055,350,139`, including all unused slots in its final batch, the complete online bound is

```text
A + B <= (2,928 * B_7 + 32 * T + 162.5 * T) / 2,224 + 14
      = (12,842,370,065,206,992 + 982,476,398,431,104 + 4,989,137,960,782,950) / 2,224 + 14
      = 18,813,984,424,421,046 / 2,224 + 14
      < 8,459,525,370,707 < 2^42.943714,
```
where the final 14 covers six target-compression units for output verification and at most eight primitive-operation
charges for the one rejected cap check (overcharged here as whole units).

**C. Precomputation (`precomputation-op-cap`, declared heuristic).** The normative finite pseudocode and
source-level ledger in Section 8.1 cover every P1-P4 loop, both W7 passes, record placement, fixed-size array
administration and the bucket prefix sum. They give at most 671,113,630,622,720 primitive operations, hence
301,759,725,999.4245 target-compression units < 301,759,726,000 < 2^38.134610 for the 2^27-bucket layout. This
version's 2^32-bucket layout adds `2^32 - 2^27` bucket boundaries, each charged the audit's same 1,024 operations
(zeroing and all accesses to both arrays, prefix accumulation, cursor reset and final checks): `+4,260,607,557,632`
operations, for 675,374,238,180,352 in all, i.e. 303,675,466,807.7122 units < **303,675,466,808** < 2^38.143740.
We charge that integer ceiling. The builder's key is `A[-1]` itself instead of `A[-1] >> 5`; nothing else in
Section 8.1 changes.

### 8.1 Source-level table-builder audit

The following C-like pseudocode is the normative finite control flow for term C. It is a direct lowering of P1-P4
in Section 4; it is not presented as a compilable historical source file. All state words are `uint32_t` and every
arithmetic result wraps modulo 2^32. Loop indices and the pass-0 total-record counter are `uint64_t`; the bucket count,
cursor and offset cells are checked `uint32_t` values (the asserted total is below 2^31).

`expand(row,k)` deposits the bits of `k` into the `=` positions of the printed row and inserts the row's fixed
unprimed sign values (`n -> 0`, `u -> 1`, and printed 0/1). `fix(X,i,x)` is the single masked equality
`(x & fixed_mask[X][i]) == fixed_value[X][i]`, with both masks determined by Section 2. `AeqP(lo,hi)` and
`EeqP(lo,hi)` evaluate the displayed primed SHA-256 step equations once for every integer step in the inclusive range,
using `X' = X xor FL(X)`, and compare the result with the prescribed primed word. `P2_conditions` is every printed
relation whose operands lie among A1..A13, E5..E13 and W9..W13. `P3_left_conditions` is every remaining
precomputation relation that becomes decidable after adding A0, E4 and W8; `P3_w7_conditions` is every remaining one
that becomes decidable after adding A[-1], E3 and W7. These are static arrays mechanically selected from the 71
relations printed in Section 2. `list_ok` scans every entry of its passed array, whose operands are all assigned at
that call. Relations whose operands remain unassigned until the online phase are excluded from the precomputation lists.
`push_hard` writes one fixed-width row and fails before exceeding the stated capacity. Thus there is no allocator
growth, comparison sort, hash table, hidden retry, or data-dependent unbounded loop.

```c
/* PC-0: fixed public capacities and counter widths. */
L4_CAP = 131072; L7_CAP = 524288; COMBO_CAP = 10240;
LEFT_CAP = 155008; RECORD_CAP = 1396774912; P14_CAP = 12; P4_CAP = 196608;
BUCKETS = 1u << 27;
uint64_t k, i, j, ci, li, b, pass, total_records, next;
uint32_t count[BUCKETS], offset[BUCKETS+1];

/* PC-1: P1 lists.  expand performs at most 32 fixed/free-bit placements. */
for (k = 0; k < (1u << 18); ++k) {
    e4 = expand(E4_row, k);
    if (fix(E,4,e4) && bit(e4,10) != bit(e4,15)) push_hard(L4, L4_CAP, e4);
}
for (k = 0; k < (1u << 25); ++k) {
    w7 = expand(W7_row, k);
    if (fix(W,7,w7) && list_ok(W7_conditions, w7)) push_hard(L7, L7_CAP, w7);
}
require(len(L4) == L4_CAP && len(L7) == L7_CAP);

/* PC-2: P2.  The 2^32 index is split into the 5, 12 and 15 free bits of E5,E6,E7. */
for (k = 0; k < (1ull << 32); ++k) {
    e5 = expand(E5_row, low5(k));
    e6 = expand(E6_row, mid12(k));
    e7 = expand(E7_row, high15(k));
    a3 = e7 - A7 + S0(A6) + MAJ(A6,A5,A4);
    a2 = e6 - A6 + S0(A5) + MAJ(A5,A4,a3);
    a1 = e5 - A5 + S0(A4) + MAJ(A4,a3,a2);
    w9  = E9  - A5 - e5 - S1(E8)  - IF(E8,e7,e6) - K9;
    w10 = E10 - A6 - e6 - S1(E9)  - IF(E9,E8,e7) - K10;
    w11 = E11 - A7 - e7 - S1(E10) - IF(E10,E9,E8) - K11;
    if (fix(A,1,a1) && fix(A,2,a2) && fix(A,3,a3)
        && fix(W,9,w9) && fix(W,10,w10) && fix(W,11,w11)
        && AeqP(5,13) && EeqP(9,13) && list_ok(P2_conditions,state))
        push_hard(COMBO, COMBO_CAP, (a1,a2,a3,e5,e6,e7,w9,w10,w11));
}
require(len(COMBO) == COMBO_CAP);

/* PC-3: P3 left rows: exactly COMBO_CAP*L4_CAP source iterations. */
for (ci = 0; ci < COMBO_CAP; ++ci) for (j = 0; j < L4_CAP; ++j) {
    (a1,a2,a3,e5,e6,e7,w9,w10,w11) = COMBO[ci];
    e4 = L4[j];
    a0 = e4 - A4 + S0(a3) + MAJ(a3,a2,a1);
    w8 = E8 - A4 - e4 - S1(e7) - IF(e7,e6,e5) - K8;
    if (fix(W,8,w8) && fix(A,0,a0) && AeqP(4,4) && EeqP(8,8)
        && list_ok(P3_left_conditions,state))
        push_hard(LEFT, LEFT_CAP, (ci,j,w8,e4,a0));
}
require(len(LEFT) == LEFT_CAP);

/* PC-4: the same finite W7 body, once to count and once to place. */
zero(count[0..BUCKETS-1]); total_records = 0;
for (pass = 0; pass < 2; ++pass) {
    if (pass == 1) {
        require(total_records == RECORD_CAP);
        offset[0] = 0;
        for (b = 0; b < BUCKETS; ++b) {
            require(count[b] <= 936); /* support bound used by Bernstein */
            next = (uint64_t)offset[b] + count[b];
            require(next <= RECORD_CAP);
            offset[b+1] = (uint32_t)next;
        }
        require(offset[BUCKETS] == RECORD_CAP);
        for (b = 0; b < BUCKETS; ++b) count[b] = offset[b]; /* count is now cursor */
    }
    for (li = 0; li < LEFT_CAP; ++li) for (j = 0; j < L7_CAP; ++j) {
        (ci,e4_index,w8,e4,a0) = LEFT[li];
        (a1,a2,a3,e5,e6,e7,w9,w10,w11) = COMBO[ci];
        w7 = L7[j];
        e3 = e7 - a3 - w7 - S1(e6) - IF(e6,e5,e4) - K7;
        am1 = e3 - a3 + S0(a2) + MAJ(a2,a1,a0);
        if (fix(E,3,e3) && fix(A,-1,am1) && AeqP(3,3) && EeqP(7,7)
            && s0(w8 ^ FL_W8) + (w7 ^ FL_W7) == s0(w8) + w7
            && list_ok(P3_w7_conditions,state)) {
            b = am1 >> 5;
            if (pass == 0) {
                require(total_records < RECORD_CAP && count[b] < RECORD_CAP);
                ++count[b]; ++total_records;
            } else {
                require(count[b] < offset[b+1]);
                records[count[b]++] = (am1,ci,e4_index,j);
            }
        }
    }
}
for (b = 0; b < BUCKETS; ++b) require(count[b] == offset[b+1]);

/* PC-5: P4: hard-cap and assert exactly 12 E14 survivors before their E15 scans. */
for (i = 0; i < 256; ++i) {
    e14 = expand(E14_row, i);
    a14 = e14 - A10 + S0(A13) + MAJ(A13,A12,A11);
    w14 = e14 - A10 - E10 - S1(E13) - IF(E13,E12,E11) - K14;
    if (fix(A,14,a14) && list_ok(A14_conditions,state))
        push_hard(P14, P14_CAP, (e14,a14,w14));
}
require(len(P14) == P14_CAP);
for (i = 0; i < P14_CAP; ++i) {
    (e14,a14,w14) = P14[i];
    group_start = len(P4);
    for (j = 0; j < (1u << 15); ++j) {
        e15 = expand(E15_row, j);
        a15 = e15 - A11 + S0(a14) + MAJ(a14,A13,A12);
        w15 = e15 - A11 - E11 - S1(e14) - IF(e14,E13,E12) - K15;
        if (fix(A,15,a15) && AeqP(14,15) && EeqP(14,15)
            && bit(A13,29) != bit(a15,29))
            push_hard(P4, P4_CAP,
                      (w14,w15,s1(w14),s1(w15),step16_constants_both(w14,w15),
                       e14,a14,e15,a15));
    }
    require(len(P4) - group_start == (1u << 14));
}
require(len(P4) == P4_CAP);
```

This is a prospective reference builder; the historical #296 measurement generator was not included in that
submission. Its correspondence to the algorithm is syntactic: PC-1 is P1, PC-2 is P2, PC-3 and PC-4 are the two
parts of P3, and PC-5 is P4, with the same equations and predicate lists printed in Sections 2 and 4. PC-4 retains
duplicates and stores exactly four 32-bit fields per record. Its key `A[-1] >> 5` is the 27-bit bucket of the audited
layout; this version uses the key `A[-1]` (2^32 buckets) and charges the extra boundaries in Section 8 C;
the main loop scans every record in that bucket and tests the complete `A[-1]`, so order within a bucket is irrelevant
and no sort is performed. Pass 0 counts the retained multiset, the prefix loop assigns disjoint final intervals, and
pass 1 writes each retained record once into its interval, reusing the count array as its placement cursor. The
equality assertions bind the inherited enumerated cardinalities, and the pass-0 assertion binds the inherited exact
maximum bucket occupancy 936 before prefix construction. If a cardinality or occupancy is wrong, this builder returns
failure instead of overrunning a table or silently changing the scored construction.

The helper expansion is fixed: a `Sigma`/`sigma` is charged 14 as above; `IF` is one NOT, two ANDs and one XOR;
`MAJ` is three ANDs and two XORs. An A/E equation has at most eight source loads, one `Sigma`, one `IF`/`MAJ`, six
modular additions, one store, one comparison, one branch and 24 address/control operations, for at most 66. A message
schedule equation has four loads, two `sigma` calls, three modular additions, one store, one comparison, one branch
and 24 address/control operations, for at most 65. Thus 128 covers either equation or a primed-conformance call. A fixed-bit or two-bit
predicate has at most four loads, four shifts/masks, four Boolean operations, a comparison, a branch and two address
operations, hence at most 16. `expand` has exactly 32 bit positions; charging 12 operations per position plus 128
for setup/output gives 512. A fixed-width push or record materialization is smaller and receives the same 512.
`step16_constants_both` returns the four `uint32_t` values `E16-W16`, `E16'-W16`, `A16-E16`, and
`A16'-E16'` specified in #26; W16 is common because its four schedule inputs have zero difference. Together with
W14, W15, their two sigma values and the four unprimed step-14/15 states, each P4 row is twelve words. The primed
states are recovered by XOR with the fixed difference masks after the row's exact A/E conformance tests have passed.
Four additional equation bodies cover the helper and the fixed-width row materialization, with no loop or lookup;
the 512-operation materialization allowance covers all twelve stores. The per-P14 assertion records the twelve
contiguous groups of exactly 2^14 rows used by the online W16 cache; a wrong inherited group count fails the builder.

The longest source path is PC-2. The phase-by-phase maxima below come from the displayed calls; interval calls such
as `AeqP(5,13)` are expanded into one body per integer step. “Other predicates” includes fixed-mask, equality and
simple Boolean tests; PC-4's `sigma0` cancellation is handled separately below. Each maximum charges every relation in that phase's static list plus its displayed worst-case
predicate bodies; none uses an average or an expected early-exit discount.

| source body | equation/conformance bodies | predicate bodies | expand/materialize actions | control allowance | charged maximum |
|---|---:|---:|---:|---:|---:|
| PC-1 L4 | 0 | 3 | 2 | 1,024 | 2,096 |
| PC-1 L7 | 0 | 79 | 2 | 1,024 | 3,312 |
| PC-2 | 20 | 103 | 4 | 1,024 | 7,280 |
| PC-3 | 4 | 75 | 2 | 1,024 | 3,760 |
| PC-4, either pass | 5 | 74 | 2 | 1,024 | 3,872 |
| PC-5 | 12 | 103 | 4 | 1,024 | 6,256 |

PC-4's explicit cancellation equality evaluates two `sigma0` calls. It is therefore charged as a full 128-operation
equation body rather than a 16-operation predicate body; the 3,872 row includes that conservative reclassification.

Each table row is applied directly to that phase's exact loop count, including rejected paths. Early exits can only
reduce the charge. The phase-specific main-loop sum is

```text
O_main <= 2,096*2^18 + 3,312*2^25 + 7,280*2^32
          + 3,760*(10,240*131,072) + 3,872*(2*155,008*524,288)
          + 6,256*(256 + 12*32,768)
        = 665,773,944,631,296 primitive operations.
```

This removes only the prior cross-phase padding from multiplying every iteration by 8,192. It preserves every
per-phase equation, predicate, materialization and 1,024-operation control allowance shown in the table.

Let `W = 155,008*524,288 = 81,268,834,304` be one W7 pass and let
`R = 131,072+524,288+10,240+155,008+12+196,608 = 1,017,228` be all retained
non-record rows. In addition to the phase-specific main-loop charges, charge 64 operations for a possible record action at
**every** W7 candidate in one pass, so this term does not rely on the observed `N`; charge 1,024 operations for
each of the `2^27+1` bucket boundaries, covering zeroing and all accesses to both the count/cursor and offset arrays,
the occupancy assertion, prefix accumulation, cursor reset and final checks; and charge
1,024 operations for every retained auxiliary row (fixed-array write/copy and administration). The full integer
ledger is

```text
O_C <= O_main + 64 W + 1,024(2^27+1) + 1,024 R
     = 671,113,630,622,720 primitive operations.
C = O_C / 2,224
  = 301,759,725,999.4245 target-compression units
  < 301,759,726,000 < 2^38.134610.
```

This is a static bound on the displayed no-sort, two-pass implementation, not a native instruction count or wall-time
measurement. The exact cardinalities are inherited participant enumeration evidence from #26/#296; changing the
predicates, capacities, representation or adding a library sort invalidates the audit. The charged integer ceiling
leaves less than one target-compression unit above the ledger and is used below.

**D. Starting solution.** The exact fixed Step-1 solution used to build the submitted TAB2 is charged directly at
**2^35 = 34,359,738,368** units. Under the 35-step-compression interpretation, the converted source report is
`ceil(2^34.3 * 2476/2224) = 23,547,494,749`, so the charge leaves a factor `1.459...` (Section 6). The 908.8 CPU-s
local measurement concerns different solutions and is corroboration only.

**Characteristic.** Public algorithm text (Section 6.1); no term. Fallback E = 159,412,543,029,248 (Section 6.2).

Round the noninteger online aggregate and preprocessing components upward to whole target-compression units:
`A+B < 8,459,525,370,707`, `C <= 303,675,466,808`, and `D = 2^35 = 34,359,738,368`. Then

```text
Total = A + B + C + D
 <= 8,459,525,370,707 + 303,675,466,808 + 34,359,738,368
 = 8,797,560,575,883
 = 2^43.0002406814... < 2^43.001        (exact: Total^1000 <= 2^43001 and Total^1000 > 2^43000)

Preprocessing = C + D
 <= 303,675,466,808 + 34,359,738,368
 = 338,035,205,176
 < 2^38.29839 < 2^38.3.
```

We claim **43.001** total and **38.3** preprocessing. There are no restarts.

### 8.2 What this version changes, and the sensitivity of each change

| change from 621d0fb0 (43.262) | effect | total if reverted alone |
|---|---|---|
| TAB2 bucketed by all 32 bits of A[-1] (scan mean 0.325212 instead of 10.41); 2^32 - 2^27 extra boundaries charged in C | E[X] 211.3 -> 160.82 | (scan 10.41, cap 214 T, T = 30,693,534,036,259) 2^43.1117 |
| cap 162.5 T and T = 30,702,387,450,972, jointly minimal at success >= 0.3901 | cap-stop 5.561e-5 | (cap 214 T) see row above |
| batch traffic itemised for straight-line code: 2,928 per 7 trials | -304 per batch | batch 3,232: 2^43.0954 |
| per-trial lookup/control itemised: 32 | -32 per trial | 64: 2^43.0709 |
| both itemisations reverted | | 2^43.1616 |

The collision route, every rate premise, the success product, D, the builder's per-phase charges and the
characteristic accounting are those of 621d0fb0.

The online and table terms descend from passed f310d44f (official 47.275), whose base is our validated commit
`1dcd6067452b0263c2dfb0812c78528686e71c76` (official 47.29). Relative to that base, f310d44f replaced the 8-lane
carry-save SWAR first-block evaluation (`3,712 + 800 + 96 = 4,608` ops per 8-trial batch, `576` ops/trial) with the
7-lane 36-bit guard-bit SWAR first-block evaluation (`2,336` counted arithmetic/randomness ops + `800` itemized
traffic/control + `96` reserve = `3,232` ops per 7-trial batch, `461.71` ops/trial); 621d0fb0 then changed only the
characteristic accounting (Section 6.1), and this version makes the changes of Section 8.2.

Sensitivity. As claimed (characteristic public): **43.001**. If a reviewer instead charges the characteristic search,
the total `time_log2` across `kappa` and the route-search multiplier is (rounded upward to two decimals):

| kappa (units per CPU-s) | margin 8 | margin 32 | margin 64 |
|---|---:|---:|---:|
| 2^23 | 45.47 | 47.26 | 48.22 |
| 2^24 | 46.34 | 48.22 | 49.20 |
| 2^25 | 47.26 | 49.20 | 50.19 |

**Comparison with #227.** Its 2^61.9 is a prospective cap (8,192 x 2^36 first-block slots at 2^24 ops each), not a
cost; its observed run used 2^41.1 first blocks and 2^41.35 tuple-tail pairs for one success, consistent with
p >= 2^-46. Its 2^64 term is S's 2^48.335 inflated by C, with no search measurement.

## 9. Memory

| Item | Bytes |
|---|---|
| TAB2, 16N | 22,348,398,592 |
| retained bucket offsets, 4(2^32 + 1) | 17,179,869,188 |
| transient count/cursor array during table build, 4 * 2^32 | 17,179,869,184 |
| other tables, code and state | < 2^25 |
| largest solver peak (search / start) | 5,642,330,112 |

The exact auxiliary arrays in the displayed representation use 15,527,568 bytes: four bytes per L4/L7 row,
9 words per combination, 5 per left row, 3 per P14 row and 12 per P4 row. Code, masks, constants and working state
are below 2^22 bytes, so the `other` row is below 2^25. Even conservatively adding the sequential solver peak, the
total is < 62,384,021,508 < 2^35.861 (the 2^32-cell offset and count arrays of this version account for the increase
over the 2^34.761 of the 2^27-bucket layout; memory is reported, not scored). The route search's memory is pre-declared (supporting heuristic
`search-peak-memory`): the measured peak over all 59 characteristic-search calls and both alternate start runs is
5.25 GiB < 2^33 bytes. The phases run sequentially, so an assumed peak of up to 2^33 bytes for S's historical exact
starting-solution construction keeps the bound at
max(attack 2^35.78, search 2^33) < 2^36. We nevertheless add the measured peaks. We claim 36. The advice
(characteristic, 71 conditions, 18 words, constants) is < 8 KB, so we claim 13.

## 10. Heuristics (IDs exactly as in claim.json)

- `q-32step-matching-rate` (score-critical): q >= 2^-17.3584. Evidence: the exact-enumeration prediction 2^-17.3254,
  the public source submission's 2^34 trials, #26's runs, and #227's campaign counts. Assumption: CV1 words act as
  uniform for the Step-2 tests. The fixed replay verifies one derivation and supplies no q-rate evidence.
- `step3-46-conditions` (score-critical): the declared premise is p >= 2^-46. Evidence: the condition count and stage
  rates measured through step 21. The 13 W20/W22 carry conditions after step 21 are extrapolated. The certified
  witness and fixed replay show one feasible conformance but do not estimate p.
- `selected-valid-tuple-success-transfer` (score-critical): conditional on at least one valid tuple, an analysis-only
  uniform selector chooses one of that trial's tuples and the selected tuple retains the generic Step-3 success lower
  bound `r`. The counterfactual uncapped trial tests every valid tuple; the cap is handled later by the `U intersect H`
  argument. The pair premise bounds multi-tuple trials by `1/31` among nonempty trials and their occurrence mass by
  `1/16`, but pooled measurements do not test the remaining occurrence-weighted versus trial-weighted transfer;
  multiplicity and rare Step-3 success may be correlated. This premise is declared rather than inferred from that bound.
- `public-characteristic` (score-critical): the published signed characteristic (Fig. 6, truncated to 32 steps in
  public hash-smash #26/#33) and its two-bit conditions are public algorithm text, used without charging their
  original discovery (Section 6.1). Every value-level object is charged (D, C, A + B). Evidence: the characteristic is
  printed in S and restated in Section 2; #396's re-run of S's procedure returned the same rows; the organizer-accepted
  r31 package 50592e75 uses the same convention. If rejected, the total is 2^47.2721673216 (Section 6.2).
- `route-search-measured` (supporting; fallback only, not in the claimed total): the completed 59-call run uses 593,858 solver CPU-s and outputs Fig. 6
  exactly. The charged x32 factor prices blind rediscovery from the measured timeout ledger, solver variance and the
  exploratory model/nabla-W choice. Steps 2-4 were conditioned on S's nabla W, 76 was not proved optimal, and the
  x32 factor was not itself executed.
- `cpu-second-pricing` (supporting; fallback only): 1 solver CPU-s <= 2^23 units (`2^34.12` primitive 256-bit word-RAM ops, `17.0`
  ops per retired instruction, as in #134), with sensitivity up to `2^25` in Section 8.
- `valid-tuple-pairs` (score-critical): E[C(V,2)] <= q * 2^-5; the unobserved cross-part term is extrapolated.
- `attack-work-moments` (score-critical): the existing stage-ordered early abort is charged with
  `f16 <= 0.126` and `f17 <= 2^-14.9` (above the measured `0.1250002` and cumulative
  `2^-14.999972...`), giving, with the 2^32-bucket scan mean 0.325212, E[X] <= 160.82 and E[X^2] <= 4.18e12. The
  builder's asserted maximum occupancy (936 for 27-bit buckets, hence for their 32-bit refinements) gives
  X <= 432,828,513,000; independent per-trial work variables then support the Bernstein cap-stop bound in Section 8.
  The moment and support inputs are inherited participant measurements and extrapolations; the organizer replay does
  not validate attack cost or these distributions.
- `precomputation-op-cap` (score-critical): Section 8.1 gives finite no-sort control flow with explicit helper
  semantics, expands the
  word-RAM cost of its helpers, links every P1-P4 phase to a per-body envelope, and separately charges worst-case
  record placement, all `2^27+1` counter/offset cells and every retained auxiliary row; this version adds the
  `2^32 - 2^27` further cells at the same 1,024 each. Its exact integer ledger is 675,374,238,180,352 primitive
  operations, or at most 303,675,466,808 target-compression units. The table cardinalities
  remain inherited participant enumeration evidence; this is a static source audit, not native timing or organizer
  execution, and any implementation with a sort, dynamic growth or different predicates falls outside the bound.
- `starting-solution-cost` (score-critical): the scored algorithm uses the exact Step-1 solution from which S builds
  TAB2 and the published pair. S reports about 2^34.3 for finding that solution; D = 2^35 charges that exact source
  construction directly and covers its 35-step-to-32-step conversion by a factor 1.459. The source unit and historical
  execution remain unverified. The locally timed alternate solutions are not substituted and establish no transfer.
- `search-peak-memory` (supporting): the route search's peak memory is below 2^33 bytes (Section 9).
