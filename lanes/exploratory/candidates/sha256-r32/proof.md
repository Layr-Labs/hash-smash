# SHA-256/32 ordinary collision: the corrected Step-3 condition count (2^-44), confirmed by measurement, with the 7-lane batch on 64 registers and lazy chaining-value extraction and an itemised table-build audit, on the seven-lane Step-3 route

## 0. Claim

The track is `sha256-r32-exploratory`, profile `sha256-r32-prefix-v1`, cost model `collision-frontier-v5`. One
32-step compression costs 1 unit and every other primitive word operation costs 1/C with C = 2224.

The algorithm is a classical two-block attack. It outputs two distinct 128-byte messages whose complete 32-step
SHA-256 hashes are equal: standard IV, standard padding, all 256 bits. Its bounds:
- success probability >= 0.39 (computed above 0.395000 with the Step-3 rate at its measured 99% lower bound, Section 7);
- time <= 2^40.588 (exact integer ceiling 1,652,533,755,683 has log2 40.5878168800, Section 8);
- preprocessing <= 2^35.8 (C + D = 57,395,177,347 < 2^35.74022, itemised in Section 8);
- memory <= 2^36 bytes (computed below 2^35.861, Section 9);
- nonuniform advice < 2^13 bytes.

**This version.** This package is submission `6e5214dd` (Meganpark980320, 42.745, passed review as
`plausible_not_refuted`) with changes of ours, and the cap and trial count re-optimised for them.

The main change is the corrected condition count (Sections 5.1 and 7). Every package of this line, the base
included, charged `p >= 2^-46` per P4 candidate (`step3-46-conditions`), counting 45 printed conditions plus one. That
count includes the printed relation `W20[4,31] = W20[6,22]`. Our reading of Section 2 already drops it as a misprint: the
published pair violates it, the algorithm never tests it, and no step needs it. Removing it leaves 44 one-bit
conditions, with stage counts 3, 12, 6, 7, 4, 1, 8 and 3. A pre-registered, occurrence-weighted measurement on the real
second block, the real P4 list and real TAB2 records confirms this directly: `p = 2^-44.0004`, 99% interval
`[2^-44.0055, 2^-43.9954]`, and stage exponents equal to the counts. The success bound charges the measured lower
bound `p_L = 2^-44.0055`. The pair term uses the measured co-pass bound, not an independence formula. The conditional
uniformity of `CV1[4..7]` given validity, on which the measurement's reduction rests, is declared as its own heuristic.
T is chosen so that the computed success is at least 0.395 under `p_L`, fifty times the 1e-4 margin of the base.

The other changes are exact accounting (also filed alone as our v10a).

What is ours:
1. **The batch on the 64-register word RAM (Section 8 A).** The cost model's 256-bit word RAM fixes no register count.
   The promoted blake3-r2 package `52bb50ee` and our passed r31 package `028aa8d0` use 64 registers. On that machine
   6e5214dd's optimised batch keeps its lane masks, the 16-word schedule window, the state and the temporaries in
   registers. The replay computes a peak of 53 live values and asserts that, with 8 registers held across the batch,
   it fits 64; the organizer executes the replay on submission. The schedule traffic and the W reloads disappear; the
   16 random words are still stored once, because the winning trial outputs M0. The merged sigma masks of 028aa8d0 make
   sigma1 12 and sigma0 13 operations. The batch's 96-operation reserve is itemised as 16 and charged 24. The register
   count is declared as the premise `register-machine-64`; with 6e5214dd's register use the total would be
   2^40.714717.
2. **Lazy chaining-value extraction (Sections 4, 8 A).** The batch extracts only `CV1[0]` of each lane (the bucket
   key). The other seven words of a lane are extracted from the stored feed-forward vectors only for a trial whose
   bucket is nonempty (an expected fraction at most `N/2^32 < 0.32522` of trials), for 56 operations inside the capped work. 6e5214dd lists this
   as a next step; this package implements and charges it.
3. **Itemised table-build audit (Section 8.1).** The W7 pass PC-4 (94.5% of the previous main-loop operations, 93.2%
   of C) is rewritten with its per-LEFT-row
   work hoisted out of the W7 loop. Three of its predicates do not depend on W7: the conformance of A3 and E7 and the
   sigma0 cancellation are exact per-row predicates, because the signs of W7 are fixed in L7. The remaining body is
   charged at its itemised count. C falls from 303,675,478,130 to 23,035,438,979 units. The replay checks the identities
   on organizer-seeded random rows. A participant run checks the rewrite against an independent literal implementation
   on all 155,008 real LEFT rows and all 524,288 W7 values: identical records and keys, and N = 1,396,774,912
   reproduced.
4. **Cap and trial count** re-optimised by the rule of d8d39011, f807117b and 6e5214dd (smallest T keeping the
   success bound at or above 0.395 with the rate at `p_L`): `W_cap = 96.2 T`, `T = 7,832,802,607,654`.

The batch is 2,273 operations per 7 trials (6e5214dd: 2,805). The replay checks the 64-register program on every
organizer seed: all seven lanes against scalar C_32, its arithmetic and traffic counts, and its liveness. What is
not changed: the collision route, characteristic and its accounting, certificate, Step 2, Step 3 and the seven-lane sweep
of f807117b, the 32 per-trial lookup operations (re-itemised as 31 under the cost model's 256-bit loads), every other
probability premise (`q`, `valid-tuple-pairs`, the selected-tuple transfer), D and the success analysis apart from its Step-3 factor. The total falls from 6e5214dd's
2^42.7441128 to 2^40.5878168; we claim 40.588.

Inherited text throughout this proof keeps its original voice. In the lineage paragraph, the source list and the
inherited sections (for example Sections 2, 5, 7 and 8.3), "this revision", "this candidate", "our" and "we" refer
to the package that first wrote each sentence. The changes of this version are those listed above; where they occur
they are marked "(this version)".

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
equivalence on organizer-generated inputs in the isolated evaluator container. This version adds the 64-register
program actually charged (`Reg64`: every lane against scalar `C_32`, its arithmetic and traffic counts and its peak
liveness, on every organizer seed) and the lazy extraction check. That replay checks one witness lineage
and finite SWAR functional examples; it does not prove universal circuit identity or validate the different
32-bit-bucket `TAB2` cardinalities, its construction cost, or the
submitted SWAR resource bound.

Sources and credit:
- **Passed Yukon submission `6e5214dd` (Meganpark980320, 42.745).** The exact base of this version: the optimised round
  function of the 7-lane batch (round-0 folding, partial folding in rounds 1-2, three-operation IF and MAJ) and its
  replay check. Every part of this package other than the changes listed in "This version" is taken from it unchanged,
  including the proof text we edit.
- **Passed Yukon submission `f807117b` (Meganpark980320, 42.791).** The seven-lane sweep of Step-3 stages 16-17 with
  the reductions R1 and R2 (Section 8.3), its ledger and validation tool.
- **Passed Yukon submission `d8d39011` (Meganpark980320, 43.001).** Full-key 32-bit TAB2 buckets, the cap/trial-count
  re-optimisation rule, and the straight-line batch traffic and per-trial lookup itemisations.
- **Yukon submission `621d0fb0` (Meganpark980320, 43.262).** f310d44f with the characteristic accounted as public
  algorithm text.
- **The 64-register machine.** The promoted blake3-r2 package `52bb50ee` (proof Section 5, "the 256-bit word RAM of the
  cost model with 64 registers") and our passed r31 package `028aa8d0` (64 registers, merged sigma masks and the
  liveness check, which this version ports to the r32 batch).
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
  SWAR first-block evaluation, `Swar7Counter`, and the 3,232-operation batch; 621d0fb0 is f310d44f with only the
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
   bounds per-trial work, so Bernstein makes cap stop small at `96.2 T`. Taking
   `T = 7,832,802,607,654` (`B_7 = ceil(T/7) = 1,118,971,801,094` batches at `2,273` ops/batch)
   and retaining the full displayed product of the declared
   lower-bound factors gives success above 0.395000 and total cost
   `1,652,533,755,683 = 2^40.5878168800... < 2^40.588` target-compression units without changing the collision
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
compact table uses 26-bit buckets and 609,229,824 entries; this replay is not evidence for the current 32-bit-bucket table's
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
1. Draw M0 as 16 fresh uniform words and compute CV1 = C_32(IV, M0), seven trials per SWAR batch (Section 8 A). The
   batch extracts only `CV1[0]` of each lane. **(This version.)** If the bucket of `CV1[0]` is nonempty, the trial
   then extracts `CV1[1..7]` of its lane from the batch's stored feed-forward vectors; an empty bucket ends the trial
   without them.
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

   **Stages 16 and 17 in 7 lanes (f807117b, Section 8.3).** The decisions of stages 16 and 17 are computed for
   seven P4 candidates at once from a lane-packed copy of P4 built in C, using the exact reductions R1 and R2 of
   Section 8.3. A candidate that passes stage 17 is handed, with its index, to the scalar code above, which re-runs
   stages 16..31 for it unchanged. The set of candidates that reach stage 18, and hence the output, is exactly the
   set the scalar sweep reaches.
4. Once the bucket length is known, the fixed per-trial work reserves the whole `5 * occupancy` scan envelope, plus
   the 56-operation lazy extraction if the bucket is nonempty (this version), with one cap check, rather than checking
   each record. Before every later Step-2 tranche, tuple setup or Step-3 tranche,
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
layout of d8d39011 (Section 4, P3) refines it: every 32-bit bucket lies inside one 27-bit bucket, so its maximum
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

That is 45 printed conditions + 1 = 46. Earlier packages of this line declared that count as the premise
`step3-46-conditions` and charged `p >= 2^-46`. The count includes the printed relation `W20[4,31] = W20[6,22]`, which
our reading of Section 2 drops as a misprint. Section 5.1 removes it from the count, which gives 44, and confirms the
corrected count directly by measurement.

### 5.1 The corrected condition count, confirmed by measurement (this version)

**The relation the route does not require.** The printed relation `W20[4,31] = W20[6,22]` means `W20[4] = W20[6]`
and `W20[31] = W20[22]`. Section 2 reads it as a misprint; what matters here is that the 32-step route does not require
it.
- **The published pair violates both.** In S's 35-step pair, `W20 = 0xe238ad6c` and `W20' = 0xe3b82d6c`. Both words
  have bit 4 = 0, bit 6 = 1, bit 31 = 1 and bit 22 = 0, since `FL(W20)` touches only bits 24, 23 and 15. So
  `W20[4] != W20[6]` and `W20[31] != W20[22]`, which is why Section 2 drops the relation. The certified #227 pair
  (Section 3) happens to satisfy both: `W20 = 0xd260bf0c`, bits 4, 6, 31, 22 = 0, 0, 1, 1. One collision on each side
  is what a relation that is not required looks like. The printed W22 relations with the same indices,
  `W22[4,31] = W22[6,22]`, are required, because W22 carries a bit-29 difference. W20 carries none at bit 29, which
  suggests the W20 copy is a transcription slip.
- **The algorithm never tests them.** Step 3 (Section 4, item 3) states its tests exactly: "require `W'[i] = W[i] xor
  FL(W[i])` and the sign values of W20 and W22; for i <= 22, also require XOR-conformance of A[i] and E[i]". The sign
  values of W20 are its bits at the `n`/`u` positions 24, 23 and 15, and `FL(W20)` has only those bits. No test reads
  bits 4, 6, 22 or 31 of W20 as a relation. The seven-lane sweep of Section 8.3 tests only stages 16 and 17, and the
  stage-17 survivors re-run those same scalar tests. So the algorithm's success event does not contain the relation.
- **No step needs them**, by the algebra below. Among 2,132 sampled full passes (below), 1,065 violate
  `W20[4] = W20[6]` and 1,036 violate `W20[31] = W20[22]`; each holds at 0.5005 and 0.5141. The campaign's end-to-end
  passes are second-block collisions from constructed chaining values, so no complete-message certificate of a
  violating 32-step collision is supplied.

Removing them leaves **44 conditions**: 3, 12, 6, 7, 4, 1, 8 and 3 at stages 16, 17, 18, 19, 20, 21, 22 and 23..31.
Each is a one-bit test, so the corrected count predicts `2^-44` per candidate.

**Algebra of stages 20..31.** After stage 20, `W20' = W20 xor FL(W20)` with `FL(W20) = 0x01808000` and the three W20
signs fixed. `sigma1` is XOR-linear, so `sigma1(W20') xor sigma1(W20) = sigma1(0x01808000)`, which has exactly the
seven bits {30, 28, 14, 13, 7, 6, 4}. Stage 22 needs `W22' - W22 = 2^29` with `W22[29] = 0`. Since
`W22' - W22 = (sigma1(W20') - sigma1(W20)) + (c22' - c22)`, the signs of those seven bits are forced.
`c22' - c22 = s0(W7') - s0(W7) + (W6' - W6) = 0x30005fd0 + 2^29 = 0x50005fd0` for every tuple: `fix(W,7)` and L7's
relations fix every bit on which `s0`'s difference depends (checked over all 524,288 entries of L7), and test (d) fixes
W6's sign. The required difference is then `0xcfffa030`, as on S's pair. These are seven conditions on
`sigma1(W20)`, whose bits are
`W20[15]^W20[17]`, `W20[13]^W20[15]`, `W20[31]^W20[1]^W20[24]`, `W20[30]^W20[0]^W20[23]`, `W20[24]^W20[26]^W20[17]`,
`W20[23]^W20[25]^W20[16]` and `W20[21]^W20[23]^W20[14]`. Given the stage-20 signs, they are exactly the printed
conditions `W20[17] = 0`, `W20[13] = 1`, `W20[26] = 0` and `W20[31,30,25,21] != W20[1,0,16,14]`. With `W22[29] = 0`,
stage 22 has 8 conditions. Next, `sigma1(W22') xor sigma1(W22)` has exactly the bits {19, 12, 10}. W24 needs
`sigma1(W22') - sigma1(W22) = -dW8 = 2^19 + 2^12 - 2^10`, i.e. `sigma1(W22)` bits 19, 12, 10 = 0, 0, 1. These are the
three printed W22 relations `W22[4] = W22[6]`, `W22[31] = W22[22]` and `W22[27] != W22[20]`. W29 then holds
automatically, because `W22' - W22 = 2^29 = -dW13`. The misprinted W20 equalities occur in none of these conditions.

**Direct confirmation: what is measured.** For a valid tuple `J` drawn from the pooled accepted record occurrences of
fresh trials (the occurrence-weighted distribution of Section 7), let `Y` be its number of P4 candidates that pass
stages 16..31. The estimand is `p = E[Y]/196,608`, averaged over that tuple distribution, the 196,608 candidates and the
law of W16..W19. A valid tuple of record `r` arises with probability proportional to its validity weight
`w_r = Pr[r valid | CV1[0] = key(r)]`, so `p = sum_r w_r p_r / sum_r w_r`.

**Reduction to a simulator (proved, given `cv1-conditional-uniformity`; from our earlier package).**
- (a) *Validity reads only `CV1[0..3]`.* Step 2 computes, for a record `r`, `E_i = A[i-4] + A_i - Sigma0(A[i-1]) -
  MAJ(A[i-1], A[i-2], A[i-3])` for `i = 0, 1, 2` and `W_i = E_i - A[i-4] - E[i-4] - Sigma1(E[i-1]) -
  IF(E[i-1], E[i-2], E[i-3]) - K_i` for `i = 0..6`. Tests (a)-(g) read W4..W6, which read CV1 only through E0..E2,
  which read only `A[-1..-4] = CV1[0..3]`.
- (b) *W0..W3 are a triangular bijection of `CV1[4..7]`* given `CV1[0..3]` and the record: `W3 = d3 - E[-1]`,
  `W2 = d2(E[-1]) - E[-2]`, `W1 = d1(E[-1], E[-2]) - E[-3]`, `W0 = d0(E[-1], E[-2], E[-3]) - E[-4]`. Under
  `cv1-conditional-uniformity`, `(W0..W3)` is uniform and independent of every Step-2 event of the trial and of the
  tuple's W4..W15.
- (c) *W16..W19* = `(s1(W14) + W9 + s0(W1) + W0, s1(W15) + W10 + s0(W2) + W1, s1(W16) + W11 + s0(W3) + W2,
  s1(W17) + W12 + s0(W4) + W3)` is again a triangular bijection of `(W0..W3)`, so W16..W19 are uniform and independent
  of those events, and they carry no difference. Steps 16..19 read only the advice, the P4 candidate and W16..W19.
- (d) *Stages 20..31.* From step 20 on the tuple enters only through `c20 = W13 + s0(W5) + W4`,
  `c20' = c20 + D(W20)`, `c22 = s0(W7) + W6`, `c22'` and the fixed differences `dW8` (record) and `dW13` (advice).
  `c21` adds equally to both branches. W23 has no difference by the P3 condition, and W25, W26, W30 and W31 have none
  once the earlier ones vanish. The differences of W27 and W28 are the advice constants `D(W20) + s0(W12') - s0(W12)` and
  `s0(W13') - s0(W13) + W12' - W12`, both 0 (checked). So stages 20..31 are: the W20 XOR and sign test, XOR-conformance
  at steps 20, 21 and 22, the W22 XOR and sign test, `s1(W22') - s1(W22) + dW8 = 0` (W24) and `(W22' - W22) + dW13 = 0`
  (W29).

**Simulator (`condexp.c`, unchanged from our earlier package; Appendix F).** It rebuilds the real two-sided second
block from the advice and the real P4 list (`secondblock.py`, `mkparams.py`: 196,608 rows, S's row among them). Each
history draws a uniform P4 candidate and a uniform W16. Each stage-16 survivor tries 1024 uniform W17 values, each
stage-17 survivor 64 uniform W18 values and each stage-18 survivor one uniform W19, so every history through step 19
carries the weight 1/65,536. For every tuple-constant vector
`(c20, c20', c21, c22, c22', dW8, dW13)` it counts the histories that pass stages 20..31 by (d). The rate of a vector
is its all-pass count over `n16 * 65,536`.

**Campaign (pre-registered before any run; `PREREGISTRATION.md`, sha256 8d3ffe66...; Appendix F).**
- **Table and coverage.** The real TAB2 was rebuilt exactly (`table.py`, `slices.py`: N = 1,396,774,912). Eight key
  slices (top key byte 0x00, 0x20, ..., 0xe0) hold 44,597,904 records, and a `2^-10` Bernoulli sub-sample of them has
  43,528. Records were taken in uniform order until 700 had nonzero validity weight: 1,573 were examined,
  55.5% with weight 0, and all stay in the estimator. Class sizes of the examined records against the population:
  1: 6.4% (population 6.2%), 2: 8.6% (10.2%), 3-4: 28.9% (27.7%), 5-8: 24.5% (25.8%), >= 9: 31.6% (30.1%).
- **Weights.** `w_r` is the fraction of a pool of `2^20` (W4, W5, W6) triples, valid for tests (a)-(d), (f) and (g),
  that passes `r`'s test (e). Nonzero weights lie in 0.302..0.964.
- **Tuples and runs.** 2 tuples per nonzero-weight record give 1,400 vectors. 30 batches of `n16 = 10^10` histories
  gave 73,231,079 histories through step 19 and about 1,117 passes per vector.
- **Estimator.** `p_occ = sum_r w_r p_r / sum_r w_r` over every examined record. The uncertainty combines batches and
  records (linearised). The 99% bounds are the outer of the `t` (0.995, 29 df) and two-way bootstrap bounds. This pooled,
  occurrence-weighted interval is the only quantity used; no maximum over vectors or records enters any bound.
- **Heterogeneity** (Bonferroni at family alpha 0.01): none at alpha 0.01. Vectors X^2 = 1441.6 on 1399 df (p = 0.21); records X^2 = 730.0 on 699 df (p = 0.20); independent even/odd batch halves correlate at 0.021 (vectors) and 0.030 (records), with between-record SD about 0.5% of p; every slice, class-size and weight-half group ratio lies in [0.9963, 1.0049] (largest |z| 2.09 against 3.40); the largest single-record |z| is 3.37 against 4.34. Weight-uniform over occurrence-weighted is 1.0001, and E[p_J^2]/p^2 <= 1.0044 (99%).
- **Co-pass** (`copass.c`, an independent replication with its own seeds): 520,582 full-pass events. Given a pass, 9 of 8.53e9 other candidates of the same W14 group also passed and none of 9.38e10 in other groups; the expected number of other passing candidates is 1.73e-5, with 99% upper bound U = 3.61e-5 = 2^-14.76. The replication rate is 2^-44.0029 (z = -1.12 against the primary). With `U` the 99% upper
  bound on the expected number of other passing candidates of the same tuple given that one passes,
  `E[C(Y_J, 2)] = E[Y_J] c / 2 <= E[Y_J] U / 2`. Candidates of one W14 group share W16, W18 and W20 and co-pass far more
  often than independence predicts, so the bound uses the measured `U` and no independence formula. `U` pools pass
  events over vectors with equal weight rather than by `w_r`; the vector and record homogeneity tests support this.
- **End-to-end.** 200 of 200 dumped full passes were completed into 32-step collisions of complete 128-byte messages in reference SHA-256, with every fixed word matching.

**Results.** Through step 19 the rate is `2^-28.0002` and stages 20..31 pass at `2^-16.0002`
(20|19 = 2^-4.0003, 21|20 = 2^-1.0000, 22|21 = 2^-7.9994, 23..31|22 = 2^-3.0005). The per-stage exponents from all 30 batches are 3.0000, 11.9998, 6.0001, 7.0003, 4.0003,
1.0000, 7.9993 and 3.0005, which equal the corrected counts 3, 12, 6, 7, 4, 1, 8 and 3. Per candidate through stage 31,
**`p = 2^-44.0004`**, with 99% interval **`[2^-44.0055, 2^-43.9954]`** (relative SE 0.109%). The co-pass bound is `U = 0.0000361053`. In
sampled survivors each counted condition is enforced from its stage on and holds at 0.5 before it (largest deviation
z = 2.78 among 197); the misprinted equalities hold at 0.50 even in full passes. The success bound of Section 7
charges the measured lower bound `p_L = 2^-44.0055`, which is slightly below the corrected count's `2^-44`.

**Organizer replay.** An organizer replay of this rate is not feasible within the executor's limits (20 s of Python,
64 KiB of source, 16 observations per trial). A single through-19 history costs about `2^28` candidate steps, and
stages 20..31 then pass at about `2^-16`. We did not embed participant-generated histories, because the organizer could
not verify how they were selected. The certified pair (Section 3) passes every counted condition. The campaign
remains a participant measurement; its scripts are in Appendix F with sha256 lines.

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
it, the total of this version would be 161,065,076,784,931 = 2^47.1946370415 (f310d44f claimed 2^47.2721673216 with
the same E); with M_E at 2^23 and no rediscovery factor, 2^42.5931.

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
- **Corrected Step-3 rate (`step3-44-conditions`).** Draw a valid tuple uniformly from the pooled accepted record
  occurrences of fresh trials, i.e. the occurrence-weighted distribution, and let `Y` be its number of conforming
  candidates. The corrected count of Section 5.1 gives 44 one-bit conditions per candidate, and the measurement of
  Section 5.1 estimates exactly `p = E[Y]/196,608`, with 99% bounds `[2^-44.0055, 2^-43.9954]`. We charge the lower
  bound: `E[Y] >= 196,608 p_L = 1.113335e-8`. Then `r >= E[Y] - E[C(Y,2)]`. The pair term is an upper factorial
  moment. Write `E[C(Y,2)] = E[Y] c / 2`, where `c` is the expected number of other conforming candidates of the same
  tuple given that one conforms. The co-pass measurement bounds `c <= U = 0.0000361053` (99%). Candidates of one W14
  group co-pass about `2^14` times more often than independence predicts, so no independence formula is used. Hence
  `r >= E[Y](1 - U/2) >= 196,608 p_L (1 - U/2)`, with `U/2 = 1.80527e-5 < 2^-15.75`, so `r >= 1.113314e-8`. No independence between candidates, groups or
  conditions is assumed.
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

Let `H = {sum_i X_i <= 96.2 T}`. On `U intersect H`, the capped algorithm reaches that collision, so
`Pr[actual success] >= Pr[U] - Pr[not H]`; no independence between these events is needed. Now
s >= 2^-17.3584 (1 - 2^-5) r = 2^-43.8247672336... (r from step3-44-conditions below). As in
PR #408, the full displayed product is retained rather than discarded in the final rounding. With
T = 7,832,802,607,654 (2^42.83266), it gives sT > 0.502744921027. Subtracting the cap-stop
probability from Section 8 by a union bound gives

**P > 1 - e^-0.502744921027 - 1.3145e-4 > 0.395000 > 0.39 claimed.** T was chosen as the smallest value giving at least
0.395 with the rate at its measured lower 99% bound, so the margin over 0.39 is at least 0.005. Sensitivity at this T,
with the cap-stop term subtracted as above: at the point estimate `2^-44.0004`, 0.3960; at `2^-44.3`, 0.3361; at
`2^-44.5`, far below the lower 99% bound, 0.2999; at the old `2^-46`, 0.1184. At this T the bound stays at or above
0.39 for every rate down to `2^-44.0293`, which is 1.6% below `p_L` and about 18 standard errors of the estimate. The
real-trial evidence for `cv1-conditional-uniformity` cannot by itself resolve a systematic shortfall that small, so
that margin rests on the premise. The calculation depends on
`step3-44-conditions`, `cv1-conditional-uniformity`, the selected-tuple transfer and `valid-tuple-pairs`, all disclosed
below.

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

**A. Fixed work per trial, T = 7,832,802,607,654 trials
(`B_7 = ceil(T/7) = 1,118,971,801,094` batches).** Each batch draws 16 independent uniform 256-bit words (`16` `RAND`
operations) and masks each word with `M` (`16` `AND` operations). Because the seven 32-bit intervals `[36l, 36l+31]`
(`l = 0..6`, `36 * 6 + 31 = 247 < 256`) are disjoint bit slices of each uniform 256-bit word, the `7 * 16 = 112`
lane values form seven mutually independent uniform 512-bit first blocks, with all guard bits `[36l+35 : 36l+32]`
zeroed. The final batch has 4 unused lanes; its full cost is charged and only the first `T` trials enter the
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

**Optimised rounds (6e5214dd; kept here and run on the 64-register machine below).** The same batch with four exact rewrites of the
round function, implemented and counted in `experiments/replay.py` (second `Swar7Counter`, `swar7_opt_*`
observations), which checks every lane against scalar `C_32` on every organizer seed:
- **Round 0.** The state is the IV, so `h + Sigma1(e) + IF(e,f,g) + K0` and `Sigma0(a) + MAJ(a,b,c)` are public
  constants: `t1 = c + W0` (1), `e1 = (d0 + t1) & M` (2), `a1 = (t1 + c') & M` (2): **5** instead of 52.
- **Round 1.** b, c, d, f, g, h are IV words: `IF = g ^ (e & (f ^ g))` with `f ^ g` constant (2), `MAJ = (a & (b ^ c)) ^
  (b & c)` with both constants (2), `h + K1` folded (3 additions): **46**.
- **Round 2.** c, d, g, h are IV words: IF in 3, MAJ as `b ^ ((a ^ b) & (b ^ c))` in 4, `h + K2` folded: **49**.
- **Rounds 3..31.** `IF = g ^ (e & (f ^ g))` (3 instead of 4) and `MAJ = b ^ ((a ^ b) & (b ^ c))` where `b ^ c` of round i
  is the `a ^ b` of round i - 1 (3 instead of 5): **49** each.

Rounds total `5 + 46 + 49 + 29 * 49 = 1,521` (was 1,664); the arithmetic subtotal is **2,193** (32 + 512 + 1,521 +
16 + 112). Every lane sum stays below 5 * 2^32 < 2^36. The ten new lane-broadcast constants (round-0 `c`, `c'` and
`d0`; round-1 `f ^ g`, `g`, `b ^ c`, `b & c`, `h + K1`, `d`; round-2 `h + K2`) are loaded once per batch with one
address operation each: **+20** in the setup row.

6e5214dd's straight-line 7-trial batch, with its lane masks resident and its schedule words stored and reloaded, is
capped at **2,805 operations**. The batch is one fixed straight-line
block with no loop, so its traffic is loads, stores and the address arithmetic that puts each load or store address in
a register; there is no loop control inside it. Each row below counts one address operation per load or store, in
addition to the load or store itself (the convention that only shift counts are immediates):

| Batch overhead | Operations |
|---|---:|
| public vector/mask/IV setup and stores of the 16 random words, plus the ten optimised-round constants (20) | 116 |
| schedule traffic: four source loads, one store and three address operations per new word (unchanged) | 16*8 = 128 |
| round traffic: per round, one `K7[i]` load and one `W[i]` load, each with one address operation | 32*4 = 128 |
| feed-forward: eight IV loads and eight vector-result stores, each with one address operation | 32 |
| 56 scalar-CV stores, each with one address operation | 112 |
| **traffic subtotal; full itemized total** | **516; 2,193 + 516 = 2,709** |

The eight state vectors and round temporaries remain registers, so advancing `(a,b,c,d,e,f,g,h)` is renaming; the
fixed masks and IV vectors load once in the setup row. The cap adds **96 reserve** above the itemized 2,709
(`2,709 + 96 = 2,805`) for base-register setup and the batch's entry and exit. Relative to `1dcd606`/`f310d44f`
(3,232), the round row drops the ten per-round "address/control allowances", which priced loop control that
straight-line code does not execute, and the feed-forward and extraction rows drop allowances beyond one address
operation per access. The replay verifies both the 2,336-operation circuit and the optimised 2,193-operation circuit
that 6e5214dd charges.

**The batch actually charged: 64 registers, merged sigma masks, lazy extraction (this version).** The cost model's
256-bit word RAM lists primitive operations and fixes no register count. The promoted blake3-r2 package `52bb50ee`
states its machine as "the 256-bit word RAM of the cost model with 64 registers", and our passed r31 package `028aa8d0`
uses the same machine with merged sigma masks and a liveness check. This version runs 6e5214dd's optimised batch on it.
- **Registers.** The 20 lane masks (M, the twelve rotation masks of Sigma0 and Sigma1, and the seven masks of the merged
  sigma forms) are loaded once per batch and stay resident. The 16 most recent schedule words, the eight state words
  and the round temporaries are registers. The schedule is interleaved with the rounds: W[i] for i >= 16 is formed just
  before round i, so no schedule word is reloaded. The 16 random words are drawn directly into registers and stored
  once, because the winning trial must output M0. The replay computes the largest set of simultaneously live values of
  the straight-line batch (a value is live from its definition to its last use, and the inputs and output of an
  operation count together): 53. Eight registers are held across the batch: one table base, the batch counter, the
  outer loop's work counter, cap, trial counter, offset-array base and TAB2 base, and one address temporary. The peak
  is therefore **61 of 64**.
- **Merged sigma masks (as in 028aa8d0).** For an input whose guard bits are 0, `v >> r` holds `v`'s bits r..31 at lane
  bits 0..31-r and zeros at 32-r..35-r, and `v << (32 - r)` holds bits 0..r-1 at 32-r..31 and zeros at 28-r..31-r. So
  one mask can serve two shifted copies whose correct and zero regions cover it:
  `sigma1(v) = ((v >> 17 ^ v >> 19) & LO17) ^ ((v << 15 ^ v << 13) & HI19) ^ ((v >> 10) & LO10)` in 12 operations and
  `sigma0(v) = ((v >> 3 ^ v >> 7) & LO3) ^ ((v << 25) & HI7) ^ ((v >> 18) & LO18) ^ ((v << 14) & HI18)` in 13 (was 14
  each). The replay checks the three merged regions bit by bit (`merged_mask_ok`), and every schedule word is reduced
  (AND M) when it is formed.
- **Lazy extraction.** Step 2 of a trial needs `CV1[1..7]` only when the bucket of `CV1[0]` is nonempty, an
  expected fraction at most `E[occupancy] = N/2^32 < 0.32522` of trials. The batch extracts and stores only the seven `CV1[0]` words and stores
  the feed-forward vectors `out[1..7]`. For a nonempty-bucket trial the deferred extraction loads its batch's seven
  vectors (each with one address operation: 14), forms the lane's shift count `36 l = (l << 5) + (l << 2)` (3), shifts and
  masks seven words (14) and stores them for Step 2 (14): 45 operations, charged **56** inside the capped work `B`.

| 64-register batch | Operations |
|---|---:|
| 16 `RAND` + 16 `AND M` | 32 |
| schedule W16..W31: 16 * (sigma1 12 + sigma0 13 + 3 `ADD` + `AND M`) | 464 |
| rounds 0..31 (6e5214dd's optimised rounds, unchanged) | 1,521 |
| feed-forward: 8 * (`ADD` + `AND M`) | 16 |
| extraction of `CV1[0]` for the seven lanes: 7 * (`SHR` + `AND`) | 14 |
| **arithmetic subtotal (`Reg64` sections, asserted)** | **2,047** |
| loads, each with one address operation: 20 lane masks, 13 lane-broadcast constants of rounds 0..2 (round-0 `c`, `c'`, `d0`; round-1 `f`, `e ^ f`, `a ^ b`, `a & b`, `g + K1`, `c`; the IV words `a`, `b`, `e` that enter rounds 2..3 as state; round-2 `f + K2`), 29 `K7[i]` (rounds 3..31), 8 feed-forward IV vectors, the scalar mask `2^32 - 1` | 71 * 2 = 142 |
| stores, each with one address operation: the 16 masked random words (M0, kept for output), 7 `CV1[0]` words and the 7 vectors `out[1..7]` kept for the lazy extraction | 30 * 2 = 60 |
| **traffic subtotal (`Reg64`: 71 loads, 30 stores, 101 address operations, asserted)** | **202** |
| batch entry and exit: the table base register (1), the output-buffer offset (2), batch counter increment, compare and branch (3), and the five constants of the trial loop (1, 7, 56, `2^32 - 1`, the trial bound) loaded with their addresses (10): itemised 16 | **charge 24** |
| **batch** | **2,273** (6e5214dd: 2,805) |

The replay's `Reg64` program is this batch, operation for operation. On every organizer seed it compares all seven
lanes with scalar `C_32` and asserts the arithmetic counts by section, the traffic counts, and a peak liveness that
fits 64 registers together with the 8 persistent ones (`reg64_*` observations). For straight-line code the live
ranges form an interval graph, so registers equal to the peak liveness suffice for an allocation. Every lane addition
is checked carry-free, with the largest lane sum below 2^36. The organizer executes the replay on submission; the
counts above are what it asserts. Of the lazy extraction, the replay checks the 14 shift/AND operations per lane; its
loads and stores are itemised in the text.

Separately, every one of the `T` used trials receives **32** operations for lookup and control, as in 6e5214dd. This
version re-itemises them for the cost model's 256-bit loads, since the offsets are 32-bit cells packed eight per word,
and includes the lazy envelope. With one address operation per memory access:
- load the trial's `CV1[0]` (address, load: 2);
- for each of the cells `k = CV1[0]` and `k + 1` (1 to form `k + 1`): the address `base + 32 (k >> 3)` (shift, shift,
  add: 3), the load (1), the bit position `32 (k & 7)` (AND, shift: 2), and `(word >> pos) & (2^32 - 1)` (2). That is
  8 each and 17 in all;
- the occupancy (1);
- an empty-bucket compare and branch (2), so that an empty bucket stops here and no select is needed;
- the envelope `5 occ + 56` as `(occ << 2) + occ + 56` (3);
- add it to the counter, compare with the cap, branch (3);
- trial counter increment, compare and branch (3).

That is 31; 32 are charged. A zero-length bucket and the cap check itself are both charged. The constants used here
are in registers loaded by the batch's entry row. The seven trials of a batch are processed in lane order; the lane
index is the trial counter, and the final batch's unused lanes are stopped by the trial-count test of the trial loop.
The record address `TAB2_base + 16 off[k]` is formed inside the per-record scan charge of Section 8 B.

**B. Counted work, capped.** Charges:
- each scanned record: 5;
- lazy extraction of `CV1[1..7]`, once per trial with a nonempty bucket (this version): 56;
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

The stage-16 and stage-17 tranches above are now evaluated seven candidates at a time (Section 8.3). Per valid tuple
the charges are: setup **600** (the scalar 300 above plus 300 for the lane-packed sweep: 215 itemised); per pack of
seven candidates (28,092 packs per tuple, 12 W14 groups of 2,341 packs, the last pack of each group with 4 real
lanes) **11** for stage 16; **57** for stage 17, paid by every pack in which at least one lane passes stage 16;
**25** for lane extraction, paid by every pack in which at least one lane passes stage 17; and for every candidate
that passes stage 17, **2 + 2,352**: a hand-off and a full re-run of the unchanged scalar tranches 48 + 256 + 2,048
above. The probability that a pack has a stage-16 pass is bounded by the union bound `7 f16 = 0.882`, which uses
only the existing premise `f16 <= 0.126`; the pack-extraction probability likewise by `7 f17`.

With the 2^32-bucket scan mean N / 2^32 < 0.32522 (Section 5), the measured rates (matches per trial < 0.32522,
Step-2 pass fractions 1/2, 1/16, 1/128, 1/256, q_UCB = 2^-17.3166), and conservative `f16 = 0.126`, `f17 = 2^-14.9`
above, the expected Step-3 work per candidate is

```text
11 * 28,092/196,608 + (7 f16) * 57 * 28,092/196,608 + (7 f17) * 25 * 28,092/196,608 + f17 * (2 + 2,352)
  = 1.571716 + 7.183315 + 0.000818 + 0.076994 = 8.832844,
```

and

E[X] <= 5(0.32522) + 56(0.32522) + 0.32522(192)
       + q_UCB(600 + 196,608 * 8.832844)
     = 1.6261 + 18.2123 + 62.4422 + 10.6423 < 92.923.

(`6e5214dd`, without the lazy extraction and with the scan mean written 0.325212: E[X] < 74.711. The scan mean
`N/2^32 = 0.3252120018...` is bounded here by 0.32522.)

(The scalar sweep of `d8d39011` had the Step-3 term q_UCB(300 + 196,608 * 80.323) = 96.746 and E[X] < 160.82; the
2^27-bucket layout before it had E[X] < 211.3.)

For the cap analysis, let `X_i` be the counterfactual uncapped Step-2/3 work demand of independently pre-sampled
uniform first block i, including its lazy extraction and excluding the fixed batch work, fixed 32 per-trial
operations and final 14-unit allowance. Conditional on the fixed,
successfully built tables, the `X_i` are independent deterministic functions of the independent first blocks.
The cap is **W_cap = 96.2 T**, so its distance above the mean is at least 3.277 T.

The inherited moment calculation gives E[X_i^2] <= 3(E[scan^2] + E[S2^2] + E[S3^2]):
- E[scan^2] <= 61^2 * 936 * 0.32522 (scan plus lazy work `5 occ + 56 [occ >= 1] <= 61 occ`, and
  E[occ^2] <= max occ * E[occ]);
- E[S2^2] <= 1304^2 * 4 * 5.758e9 / 2^32;
- E[S3^2] <= S3_max^2 * q_UCB(1 + 2^-4), with S3_max the worst case below (every pack pays stage 16, stage 17 and
  extraction, and every candidate re-runs the full scalar 2,354); the multiplicity factor is inherited unchanged.

The three terms times 3 are 3,398,084 + 27,355,725 + 4,229,995,526,954 < 4.2301e12; we use
E[X_i^2] <= 4.2301e12. The
inherited full-table participant enumeration reports exact maximum bucket occupancy 936, and the fixed builder below
asserts that bound before prefix construction. The maximum Step-3 demand of one record is

```text
S3_max = 600 + 28,092(11 + 57 + 25) + 196,608(2 + 2,352) = 465,428,388,
M = 5(936) + 56 + 936(1,304 + S3_max) = 435,642,196,448.
```

Thus `0 <= X_i <= M`. Let `m_i = E[X_i]` and `Z_i = X_i - m_i`; then `|Z_i| <= M`,
`sum m_i <= 92.923 T`, and `sum Var(X_i) <= T * 4.2301e12`. A cap stop implies that the counterfactual uncapped
total exceeds `96.2 T`, hence `sum Z_i >= 3.277 T`. One-sided Bernstein gives

```text
Pr[stop at cap]
 <= exp(-(3.277 T)^2 / (2(T*4.2301e12 + M*(3.277 T)/3)))
 < exp(-8.9369893141)
 < 1.3145e-4.
```

Section 7 subtracts it in full. The cap and T were chosen together: over caps on a 0.01 grid above the mean, the
smallest T that keeps the success bound, with the Step-3 rate at its measured lower bound `p_L`, at or above 0.395,
minimising total work (the rule of d8d39011 with the floor raised).

Equality at the cap is allowed; a tranche is rejected only if it would exceed the cap. The occupancy assertion's
success is a score-critical part of `attack-work-moments`; the organizer replay does not validate the full table. If
the fixed table has a bucket above 936, preprocessing aborts and the success claim fails instead of applying Bernstein.

With `B_7 = 1,118,971,801,094`, including all unused slots in its final batch, the complete online bound is

```text
A + B <= (2,273 * B_7 + 32 * T + 96.2 * T) / 2,224 + 14
      = (2,543,422,903,886,662 + 250,649,683,444,928 + 753,515,610,856,314.8) / 2,224 + 14
      = 3,547,588,198,187,904.8 / 2,224 + 14
      < 1,595,138,578,336 < 2^40.536819,
```
where the final 14 covers six target-compression units for output verification and at most eight primitive-operation
charges for the one rejected cap check (overcharged here as whole units).

**C. Precomputation (`precomputation-op-cap`, declared heuristic).** The normative finite pseudocode and
source-level ledger in Section 8.1 cover every P1-P4 loop, both W7 passes, record placement, fixed-size array
administration and the bucket prefix sum. They give at most 671,113,630,622,720 primitive operations, hence
301,759,725,999.4245 target-compression units < 301,759,726,000 < 2^38.134610 for the 2^27-bucket layout.
d8d39011's 2^32-bucket layout adds `2^32 - 2^27` bucket boundaries, each charged the audit's same 1,024 operations
(zeroing and all accesses to both arrays, prefix accumulation, cursor reset and final checks): `+4,260,607,557,632`
operations, for 675,374,238,180,352 in all, i.e. 303,675,466,807.7122 units < 303,675,466,808. The lane-packed
P4 copy of Section 8.3 and its build assertion R1 add 196,608 * 128 + 12 * 1,024 = 25,178,112 operations
(11,322 units, rounded up), for C = 303,675,478,130 < 2^38.143740 in 6e5214dd.

**This version itemises PC-4** (Section 8.1, "PC-4 itemised"): its three w7-independent predicates are hoisted to
the LEFT row, which keeps the old 3,872 per row and pass, and the remaining per-pair body is charged 32 instead of
3,872. PC-4 falls from `3,872 * 2 * 81,268,834,304 = 629,345,852,850,176` to `2(3,872 * 155,008 + 32 * 81,268,834,304) =
5,202,405,777,408` operations. Every other line is unchanged: the 64-operation record action per W7 candidate, the
1,024 per bucket boundary, the auxiliary rows and the lane-packed P4 copy. The ledger becomes
51,230,791,107,584 operations, i.e. 23035427656.2878 units, rounded up to 23,035,427,657, plus the 11,322 units of the lane-packed
P4 copy: **C = 23,035,438,979**. We charge that integer ceiling. The builder's key is `A[-1]` itself.

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
BUCKETS = 1ull << 32;   /* d8d39011: full-key buckets */
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

/* PC-4: the same finite W7 pass, once to count and once to place. This version hoists every predicate that does not
   depend on w7 out of the W7 loop (see "PC-4 itemised" below); the accepted records, their order and keys are those
   of the literal body. */
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
    for (li = 0; li < LEFT_CAP; ++li) {
        (ci,e4_index,w8,e4,a0) = LEFT[li];
        (a1,a2,a3,e5,e6,e7,w9,w10,w11) = COMBO[ci];
        X = e7 - a3 - S1(e6) - IF(e6,e5,e4) - K7;            /* e3 = X - w7 */
        Y = S0(a2) + MAJ(a2,a1,a0) - a3;                      /* am1 = e3 + Y */
        if (!(AeqP_row(3) && EeqP_row(7) && s0(w8 ^ FL_W8) + D_W7 == s0(w8)))
            continue;                                         /* row predicates, independent of w7 */
        for (j = 0; j < L7_CAP; ++j) {
          e3 = X - L7[j];
          if (fix(E,3,e3)) {
            am1 = e3 + Y;
            b = am1;                                          /* the complete A[-1] (d8d39011) */
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
layout; d8d39011 and this version use the key `A[-1]` (2^32 buckets) and charges the extra boundaries in Section 8 C;
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
| PC-4, either pass, per LEFT row (hoisted, this version) | 5 | 74 | 2 | 1,024 | 3,872 |
| PC-4, either pass, per (LEFT row, W7) pair (this version; itemised, not the envelope convention) | - | - | - | - | 32 (16 itemised) |
| PC-5 | 12 | 103 | 4 | 1,024 | 6,256 |

**PC-4 itemised (this version).** The literal PC-4 body evaluates, for every (LEFT row, W7) pair,
`fix(E,3,e3)`, `fix(A,-1,am1)`, `AeqP(3,3)`, `EeqP(7,7)`, the `sigma0` cancellation and `P3_w7_conditions`. Only the
first depends on w7:
- `AeqP(3,3)` evaluates `A3' = E3' - A[-1]' + Sigma0(A2') + MAJ(A2', A1', A0')` with primed inputs `X xor FL(X)`. Rows
  E3 and A[-1] carry no `n`/`u`, so `E3' = E3` and `A[-1]' = A[-1]`. Then
  `A3' - A3 = Sigma0(A2') - Sigma0(A2) + MAJ(A2',A1',A0') - MAJ(A2,A1,A0)`, a function of the LEFT row only
  (`AeqP_row(3)`).
- `EeqP(7,7)` compares `A3' + E3' + Sigma1(E6') + IF(E6',E5',E4') + K7 + W7'` with `E7 xor FL(E7)`. Since
  `E7 = A3 + E3 + Sigma1(E6) + IF(E6,E5,E4) + K7 + W7`, the difference is
  `Sigma1(E6') - Sigma1(E6) + IF(E6',E5',E4') - IF(E6,E5,E4) + (W7' - W7)`. `W7' - W7 = (w7 xor FL_W7) - w7 = D(W7)` for every
  w7 in L7, because `fix(W,7)` fixes the signs at the `n`/`u` positions. So this test is a row predicate (`EeqP_row(7)`).
- The `sigma0` cancellation `s0(w8 xor FL_W8) + (w7 xor FL_W7) = s0(w8) + w7` is `s0(w8') + D(W7) = s0(w8)`, also a row
  predicate.
- `fix(A,-1,am1)` has an empty mask (row A[-1] is all `=`).
- `P3_w7_conditions` is empty: no printed relation of Section 2 involves A[-1] or E3, and the W7 relations are already
  in `W7_conditions` of PC-1.

The hoisted loop therefore accepts exactly the records of the literal loop, in the same (li, j) order and with the
same keys, so the occupancy assertion, N and the table are unchanged. The replay checks the identities
(`l1_pc4_rows_checked`) on organizer-seeded random rows: each predicate's residual is the same for two different
sign-valid w7, and the hoisted `e3`, `am1` equal the literal ones. (`AeqP_row(3)` is in fact always true, because rows
A0..A2 also carry no difference; the EeqP and sigma0 residuals are the informative ones.) A participant run checks the
rewrite on the real table. On all 155,008 LEFT rows and all 524,288 W7 values (81,268,834,304 pairs), v8's
independent literal implementation (`table.py`, `w7_job`) and the hoisted form accept identical records with
identical keys. Every row passes its row predicates, D(W7) = 0x00feef76 throughout, and the accepted total is exactly
N = 1,396,774,912. Charges: per LEFT row and pass, the old full body **3,872** (the row constants X, Y, the three row
predicates and control); per (LEFT row, W7) pair and pass, **32**, for 16 itemised. The 16 are: the 32-bit cell `L7[j]`
read from its packed 256-bit word (address 3, load 1, shift and mask 4: 8), `e3 = X - w7` 2, `fix(E,3)` as AND, compare
and branch 3, and loop counter 3. The record action (am1, key, count or place) is the separate 64-operation charge per
W7 candidate below.

PC-4's explicit cancellation equality evaluates two `sigma0` calls. It is therefore charged as a full 128-operation
equation body rather than a 16-operation predicate body; the 3,872 row includes that conservative reclassification.

Each table row is applied directly to that phase's exact loop count, including rejected paths. Early exits can only
reduce the charge. The phase-specific main-loop sum is

```text
O_main <= 2,096*2^18 + 3,312*2^25 + 7,280*2^32
          + 3,760*(10,240*131,072) + 2*(3,872*155,008 + 32*155,008*524,288)
          + 6,256*(256 + 12*32,768)
        = 41,630,497,558,528 primitive operations
          (665,773,944,631,296 with 6e5214dd's PC-4 charge of 3,872 per pair).
```

This removes only the prior cross-phase padding from multiplying every iteration by 8,192. It preserves every
per-phase equation, predicate, materialization and 1,024-operation control allowance shown in the table. The one
exception is PC-4's per-pair row, which this version charges at its itemised count (16, charged 32) instead of the
envelope convention of the other rows. The record action below is charged 64 for every W7 candidate of one pass. The
`RECORD_CAP` assertions bound the record actions of both passes together by 2 x 1,396,774,912, below that charge.

Let `W = 155,008*524,288 = 81,268,834,304` be one W7 pass and let
`R = 131,072+524,288+10,240+155,008+12+196,608 = 1,017,228` be all retained
non-record rows. In addition to the phase-specific main-loop charges, charge 64 operations for a possible record action at
**every** W7 candidate in one pass, so this term does not rely on the observed `N`; charge 1,024 operations for
each of the `2^27+1` bucket boundaries, covering zeroing and all accesses to both the count/cursor and offset arrays,
the occupancy assertion, prefix accumulation, cursor reset and final checks; and charge
1,024 operations for every retained auxiliary row (fixed-array write/copy and administration). The full integer
ledger is

```text
O_C <= O_main + 64 W + 1,024(2^32+1) + 1,024 R
     = 51,230,791,107,584 primitive operations   (2^32 boundaries: d8d39011; PC-4 itemised: this version)
C = ceil(O_C / 2,224) + 11,322 (lane-packed P4 copy and R1 assertion, Section 8 C)
  = 23,035,427,657 + 11,322 = 23,035,438,979 target-compression units < 2^34.42314.
```

This is a static bound on the displayed no-sort, two-pass implementation, not a native instruction count or wall-time
measurement. The exact cardinalities are inherited participant enumeration evidence from #26/#296; changing the
predicates, capacities, representation or adding a library sort invalidates the audit. The charged integer ceiling
leaves less than one target-compression unit above the ledger and is used below. (6e5214dd's ledger, with the
2^27 + 1 boundaries of the original audit, PC-4 at 3,872 per pair, and the later additions of Section 8 C, gave
303,675,478,130.)

**D. Starting solution.** The exact fixed Step-1 solution used to build the submitted TAB2 is charged directly at
**2^35 = 34,359,738,368** units. Under the 35-step-compression interpretation, the converted source report is
`ceil(2^34.3 * 2476/2224) = 23,547,494,749`, so the charge leaves a factor `1.459...` (Section 6). The 908.8 CPU-s
local measurement concerns different solutions and is corroboration only.

**Characteristic.** Public algorithm text (Section 6.1); no term. Fallback E = 159,412,543,029,248 (Section 6.2).

Round the noninteger online aggregate and preprocessing components upward to whole target-compression units:
`A+B < 1,595,138,578,336`, `C <= 23,035,438,979`, and `D = 2^35 = 34,359,738,368`. Then

```text
Total = A + B + C + D
 <= 1,595,138,578,336 + 23,035,438,979 + 34,359,738,368
 = 1,652,533,755,683
 = 2^40.5878168800... < 2^40.588        (exact: Total^1000 <= 2^40588 and Total^1000 > 2^40587)

Preprocessing = C + D
 <= 23,035,438,979 + 34,359,738,368
 = 57,395,177,347
 < 2^35.74022 < 2^35.8.
```

We claim **40.588** total and **35.8** preprocessing. There are no restarts.

### 8.2 What this version changes, and the sensitivity of each change

Earlier changes (from 621d0fb0, 43.262, to d8d39011, 43.001), each total computed against the d8d39011 ledger:

| change from 621d0fb0 (43.262) | effect | total if reverted alone |
|---|---|---|
| TAB2 bucketed by all 32 bits of A[-1] (scan mean 0.325212 instead of 10.41); 2^32 - 2^27 extra boundaries charged in C | E[X] 211.3 -> 160.82 | (scan 10.41, cap 214 T, T = 30,693,534,036,259) 2^43.1117 |
| cap 162.5 T and T = 30,702,387,450,972, jointly minimal at success >= 0.3901 | cap-stop 5.561e-5 | (cap 214 T) see row above |
| batch traffic itemised for straight-line code: 2,928 per 7 trials | -304 per batch | batch 3,232: 2^43.0954 |
| per-trial lookup/control itemised: 32 | -32 per trial | 64: 2^43.0709 |
| both itemisations reverted | | 2^43.1616 |

The collision route, every rate premise, the success product, D, the builder's per-phase charges and the
characteristic accounting are those of 621d0fb0.

**This version (from 6e5214dd, 42.745).** Each row applies one change to 6e5214dd and re-optimises the cap and T by the
same rule:

| change from `6e5214dd` | effect | total with only this change |
|---|---|---|
| lazy extraction of `CV1[1..7]` | batch 2,805 -> 2,609; E[X] +18.21 | 2^42.717403 |
| 64-register batch with merged sigma masks (reserve unchanged) | batch 2,805 -> 2,527 | 2^42.632531 |
| batch reserve itemised (96 -> 24) | batch -72 | 2^42.716031 |
| itemised table-build audit (PC-4 hoisted; C 23,035,438,979) | C -92.4% | 2^42.688076 |
| corrected Step-3 count (2^-44), charged at the measured p_L, success >= 0.395 | T 30,702,858,922,613 -> 7,832,802,607,654 | 2^40.958517 |
| all (claimed) | batch 2,273, cap 96.2 T | 2^40.587816 |

Reverting single items of the claim: batch reserve 96 instead of 16, 2^40.619100; 6e5214dd's register use instead of
`register-machine-64` (the batch with lazy extraction and merged masks on 6e5214dd's register use: 2,047 arithmetic, 432
traffic, namely 6e5214dd's 516 less its 112 scalar-CV stores plus 14 `CV1[0]` stores and 14 loads of the seven merged
masks, and the 96 reserve: 2,575 operations), 2^40.714717. Without the itemised table-build audit (C = 303,675,478,130): 2^40.814108.

f807117b (from d8d39011, 43.001): Step 3 stages 16-17 in seven lanes (Section 8.3), with E[X] 160.82 -> 74.711,
cap 162.5 T -> 76.4 T, T 30,702,387,450,972 -> 30,702,858,922,613 and C +11,322 units: total 2^43.0002 -> 2^42.7909.
Alternatives for the new step, each re-optimised the same way (computed in `step3_swar.py`, Appendix E):

| variant | E[X] bound | best cap | total |
|---|---:|---:|---:|
| **f807117b as claimed: R1 reduction, union bound 7 f16 for a pack's stage-16 pass, rotation masks reloaded for stage 17** | 74.711 | 76.4 T | **2^42.7909** |
| no R1 (literal four-addition stage 16), union bound, masks reloaded | 76.321 | 78.0 T | 2^42.7951 |
| exact pack probability for a layout sorted by `oE mod 2^26` under uniform W16 (not claimed) | 67.227 | 68.9 T | 2^42.7711 |
| scalar Step 3 (d8d39011) | 160.82 | 162.5 T | 2^43.0003 |

These four rows use the 2,928-operation batch of f807117b. 6e5214dd's optimised rounds (2,805 per batch) move the
claimed row from 2^42.7909 to **2^42.7441**; with the 2,336-operation rounds of f807117b instead, the total is
f807117b's 2^42.7909.

The online and table terms descend from passed f310d44f (official 47.275), whose base is the validated commit
`1dcd6067452b0263c2dfb0812c78528686e71c76` (official 47.29). Relative to that base, f310d44f replaced the 8-lane
carry-save SWAR first-block evaluation (`3,712 + 800 + 96 = 4,608` ops per 8-trial batch, `576` ops/trial) with the
7-lane 36-bit guard-bit SWAR first-block evaluation (`2,336` counted arithmetic/randomness ops + `800` itemized
traffic/control + `96` reserve = `3,232` ops per 7-trial batch, `461.71` ops/trial); 621d0fb0 then changed only the
characteristic accounting (Section 6.1); d8d39011, f807117b and 6e5214dd then made the changes listed in Section 8.2,
and this version makes the changes of its "This version" table.

### 8.3 Step 3: stages 16 and 17 for seven candidates at once

**P4 and the two reductions.** Unprimed values are the advice branch and primed values are `X' = X xor FL(X)`. W0,
W1, W2, W9, W10 and W14..W17 have zero difference; rows A13, A15, A16, A17, E14 and E17 are all `=`;
FL(A14) = 2^29, FL(E15) = bits {18, 4}, FL(E16) = bits {25, 23, 15} (u, n, n), so D(E16) = -2^25 + 2^23 + 2^15.
Each P4 row stores the offsets `oE = E16 - W16`, `oE' = E16' - W16`, `oA = A16 - E16`, `oA' = A16' - E16'`.

- **R1 (asserted by the builder for all 196,608 rows).** `oE' - oE = D(E16)` and `(oE' - oE) + (oA' - oA) = 0 (mod
  2^32)`. Because `W16' = W16`, for every tuple `E16' - E16 = D(E16)` and `A16' - A16 = 0`. Hence the A16 test of
  stage 16 always holds, and the E16 test `E16' = E16 xor FL(E16)` holds iff `E16[25] = 1`, `E16[23] = 0` and
  `E16[15] = 0` (unique signed-digit representation over distinct positions below 31). Stage 16 is therefore
  `((oE + W16) xor 2^25) & FL(E16) = 0`. The builder checks R1 on every row and fails otherwise (charged in C).
  f807117b's own enumeration of P4 from the advice and Fig. 6 gives exactly 12 groups of 16,384 rows, R1 holds on all of
  them, and the measured stage-16 fraction is exactly 1/8, as #296 measured.
- **R2 (algebra, no assertion).** On a stage-16 survivor, W17 and K17 cancel (W17' = W17), so the E17 test is
  `Sigma1(E16) + IF(E16, E15, E14) + DC = Sigma1(E16') + IF(E16', E15', E14) (mod 2^32)` with
  `DC = (A13 + E13) - (A13' + E13')`, and `Sigma1(E16') = Sigma1(E16) xor Sigma1(FL(E16))` because Sigma1 is linear over
  XOR. Given `E17' = E17`, `A16' = A16`, `A13' = A13`, `A15' = A15` and `A14' = A14 xor 2^29`, the A17 test is
  `MAJ(A16, A15, A14) = MAJ(A16, A15, A14 xor 2^29)`, i.e. `A16[29] = A15[29]`. Stage 17 needs no message word.

**Layout (built once, charged in C).** Each W14 group is padded to 2,341 packs of seven rows (the last with 4 real
lanes; the 3 dummy lanes are forced to fail by OR-ing a lane mask), 28,092 packs in all. Lane l is bits 36l..36l+35
with zero guard bits. A pack stores three lane-packed words: `oE`, `E15 xor E14`, and
`((oE + oA) mod 2^32) + A15[29] 2^29`; each group stores `sigma1(W14)` and `E14` broadcast.

**Per tuple and per pack (every primitive counted by `step3_swar.py`, one address operation per load).**

| block | when | ops |
|---|---|---:|
| tuple setup | per valid tuple | 600 (scalar 300 + 300; 215 itemised: 14 constant loads, c16 broadcast 7, per group W16 broadcast-add, E14 broadcast, control and cap reserve, dummy-lane mask) |
| stage 16 | every pack | 11: load `oE` (2), `S = W16 + oE` (1), `(S xor V16) & FL16` (2), per-lane zero test `(T + M) & G` (2), compare and branch (2), pack loop (2) |
| stage 17 | pack with a stage-16 pass | 57: the 45 itemised (cap check, Sigma1 of the masked E16, the two IFs, the E17 comparison, the A16[29] test, combination with the stage-16 result, per-lane zero test, branch) plus 12 to reload the six rotation masks |
| extraction | pack with a stage-17 pass | 25: cap check, pass mask, 7 x (shift, AND, branch) |
| survivor | each candidate passing stage 17 | 2 + 2,352: hand-off, then the unchanged scalar tranches 48 + 256 + 2,048 from stage 16 |

A pack's stage-16 pass probability is bounded by `7 f16 = 0.882` and its stage-17 pass probability by `7 f17`; the
survivors are exactly the scalar sweep's stage-17 survivors, so they occur at rate `f17` per candidate. No lane sum
reaches 2^34 (checked on every executed addition).

**Validation (`step3_swar.py`, Appendix E).**
- 40 random tuples plus the two real tuples (the #227 certified pair and S's pair, both of whose (W14, W15) are in P4
  and pass stages 16 and 17), all 196,608 candidates each, in three configurations: **49,545,216 lane decisions
  (stage 16 and cumulative stage 17) compared with a scalar reference that evaluates both branches from the full step
  equations and never uses the stored offsets: 0 mismatches.**
- 20,000 targeted packs with one lane forced through stage 16: 279,946 lane decisions, 10,044 forced stage-17
  passes: 0 mismatches.
- On 589,824,000 lanes of uniform random tuples the stage-16 fraction is 0.1249994 and the cumulative stage-17 rate
  2^-15.013 (+-1.5%), consistent with the measured 2^-3.000 and 2^-15.000 and inside `f16 <= 0.126`,
  `f17 <= 2^-14.9`. These test the arithmetic only; the real-tuple rates remain the credited measurements.

Sensitivity. As claimed (characteristic public): **40.588**. If a reviewer instead charges the characteristic search,
the total `time_log2` across `kappa` and the route-search multiplier is (rounded upward to two decimals):

| kappa (units per CPU-s) | margin 8 | margin 32 | margin 64 |
|---|---:|---:|---:|
| 2^23 | 45.24 | 47.20 | 48.19 |
| 2^24 | 46.21 | 48.19 | 49.19 |
| 2^25 | 47.20 | 49.19 | 50.19 |

**Comparison with #227.** Its 2^61.9 is a prospective cap (8,192 x 2^36 first-block slots at 2^24 ops each), not a
cost; its observed run used 2^41.1 first blocks and 2^41.35 tuple-tail pairs for one success, consistent with
the corrected rate 2^-44 of Section 5.1. Its 2^64 term is S's 2^48.335 inflated by C, with no search measurement.

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
total is < 62,384,021,508 < 2^35.861 (the 2^32-cell offset and count arrays of d8d39011 account for the increase
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
- `step3-44-conditions` (score-critical, replaces `step3-46-conditions`): for the occurrence-weighted valid tuple,
  each P4 candidate passes stages 16..31 with probability at least `p_L = 2^-44.0055`, and the size-biased co-pass
  mean is at most `0.0000361053`. Evidence: the corrected count of 44 one-bit conditions (Section 5.1: the printed
  misprint `W20[4,31] = W20[6,22]` removed, with the late conditions derived algebraically), and the pre-registered
  measurement on the real second block, the real P4 list and real TAB2 records. That measurement gives the point
  `2^-44.0004`, stage exponents equal to the counts, every counted condition enforced from its stage and at 0.5 before
  it, no heterogeneity, an independent replication, and 200 of 200 dumped passes completed into real collisions.
  Coverage: 8 key slices, 1,573 records examined and 700 weighted, 1,400 tuple vectors, 73.2M histories through step 19.
- `cv1-conditional-uniformity` (score-critical, new): for a uniform first block and every event determined by
  `CV1[0..3]` (in particular the validity of any set of TAB2 records), `CV1[4..7]` is uniform and independent of that
  event. Hence `W0..W3` and `W16..W19` of every valid tuple are uniform and independent of the trial's Step-2 events
  and of the tuple's `W4..W15`. Evidence and scope in Section 5.1.
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
  r31 package 50592e75 uses the same convention. If rejected, the total is 2^47.1946370415 (Section 6.2).
- `route-search-measured` (supporting; fallback only, not in the claimed total): the completed 59-call run uses 593,858 solver CPU-s and outputs Fig. 6
  exactly. The charged x32 factor prices blind rediscovery from the measured timeout ledger, solver variance and the
  exploratory model/nabla-W choice. Steps 2-4 were conditioned on S's nabla W, 76 was not proved optimal, and the
  x32 factor was not itself executed.
- `cpu-second-pricing` (supporting; fallback only): 1 solver CPU-s <= 2^23 units (`2^34.12` primitive 256-bit word-RAM ops, `17.0`
  ops per retired instruction, as in #134), with sensitivity up to `2^25` in Section 8.
- `valid-tuple-pairs` (score-critical): E[C(V,2)] <= q * 2^-5; the unobserved cross-part term is extrapolated.
- `register-machine-64` (score-critical, new in this version): the first-block batch is charged as the explicit
  straight-line program of Section 8 A on the cost model's 256-bit word RAM with 64 registers, the machine of the
  promoted blake3-r2 package 52bb50ee and of our passed r31 package 028aa8d0. Its 53 simultaneously live values plus 8
  registers held across the batch fit 64. The replay asserts the program's results, operation counts and liveness. The
  cost model fixes no register count. With 6e5214dd's register use (masks resident, schedule words and W reloaded) the
  batch would be 2,575 and the total 2^40.714717.
- `attack-work-moments` (score-critical): the existing stage-ordered early abort is charged with
  `f16 <= 0.126` and `f17 <= 2^-14.9` (above the measured `0.1250002` and cumulative
  `2^-14.999972...`), giving, with the 2^32-bucket scan mean `N/2^32 < 0.32522`, this version's lazy extraction (56 per
  nonempty-bucket trial) and the seven-lane stages 16-17 of Section 8.3 (pack stage-16 pass bounded by 7 f16),
  E[X] <= 92.923 and E[X^2] <= 4.2301e12. The
  builder's asserted maximum occupancy (936 for 27-bit buckets, hence for their 32-bit refinements) gives
  X <= 435,642,196,448; independent per-trial work variables then support the Bernstein cap-stop bound in Section 8.
  The moment and support inputs are inherited participant measurements and extrapolations; the organizer replay does
  not validate attack cost or these distributions.
- `precomputation-op-cap` (score-critical): Section 8.1 gives finite no-sort control flow with explicit helper
  semantics, expands the
  word-RAM cost of its helpers, links every P1-P4 phase to a per-body envelope, and separately charges worst-case
  record placement, all `2^27+1` counter/offset cells and every retained auxiliary row; d8d39011 adds the
  `2^32 - 2^27` further cells at the same 1,024 each, and this version itemises PC-4's per-pair body (Section 8.1).
  Its exact integer ledger is 51,230,791,107,584 primitive operations, plus 25,178,112 for the lane-packed P4 copy and its
  R1 assertion: at most 23,035,438,979 target-compression units. The table cardinalities
  remain inherited participant enumeration evidence; this is a static source audit, not native timing or organizer
  execution, and any implementation with a sort, dynamic growth or different predicates falls outside the bound.
- `starting-solution-cost` (score-critical): the scored algorithm uses the exact Step-1 solution from which S builds
  TAB2 and the published pair. S reports about 2^34.3 for finding that solution; D = 2^35 charges that exact source
  construction directly and covers its 35-step-to-32-step conversion by a factor 1.459. The source unit and historical
  execution remain unverified. The locally timed alternate solutions are not substituted and establish no transfer.
- `search-peak-memory` (supporting): the route search's peak memory is below 2^33 bytes (Section 9).

## Appendix E. `step3_swar.py` (participant tool)

sha256 b23bcd728ba2d1ce0c51e8004f03efd13751c0a8a4148a2205b5f2882e80c4b6  step3_swar.py

Run as `python3 -I step3_swar.py` next to the organizer's `verifier/hash_functions.py` (and `numpy`); it rebuilds P4,
checks R1, validates the seven-lane stages 16-17 against the scalar reference and computes the ledger variants. It
is a participant tool, not an organizer experiment.

```python
#!/usr/bin/env python3
"""Step-3 stages 16..17 in 7 lanes of 36 bits: P4 rebuild, scalar reference, SWAR kernel, validation, ledger.

Run:  python3 -I step3_swar.py [--tuples N] [--targeted N] [--seed S] [--skip-opt]

Everything is self-contained (SHA-256 helpers copied from replay_base.py).  Sections:
  1. Fig. 6 rows, advice, FL masks; advice self-check.
  2. P4 rebuilt from Section 4 (P4) / Section 8.1 PC-5; asserts 12 groups x 2^14; witness membership.
  3. Twelve-word P4 rows exactly as the proof stores them, plus the two row identities used by the
     reduced stage-16 test (asserted for every row, i.e. a build-time assertion).
  4. Scalar reference of stages 16 and 17 from the full step equations (pure Python, and a numpy
     vectorisation cross-checked against it).
  5. SWAR kernel (Ops counts every primitive 256-bit operation), two variants:
       'reduced' : stage 16 = 3-bit E16 test (exact by the asserted row identities), 3 packed fields;
       'general' : stage 16 forms E16, E16', A16, A16' and tests both XOR-conformances, 5 packed fields.
     Stage 17 is the same in both and evaluates all 7 lanes of a pack in which any lane passed 16.
  6. Validation against the scalar reference (random tuples, all packs, + targeted stage-17 cases,
     + the two real conforming pairs).
  7. Exact pack-any-pass probability under uniform W16 (interval measure), natural and sorted layouts;
     worst-case stage-16 survivors per group (sweep).
  8. Cost ledger and the (w, T) re-optimisation with mpmath (60 digits).
"""
from __future__ import annotations

import argparse
import json
import math
import random
import sys
import time

import numpy as np

M32 = 0xFFFFFFFF
K = (
    0x428A2F98, 0x71374491, 0xB5C0FBCF, 0xE9B5DBA5, 0x3956C25B, 0x59F111F1, 0x923F82A4, 0xAB1C5ED5,
    0xD807AA98, 0x12835B01, 0x243185BE, 0x550C7DC3, 0x72BE5D74, 0x80DEB1FE, 0x9BDC06A7, 0xC19BF174,
    0xE49B69C1, 0xEFBE4786, 0x0FC19DC6, 0x240CA1CC, 0x2DE92C6F, 0x4A7484AA, 0x5CB0A9DC, 0x76F988DA,
    0x983E5152, 0xA831C66D, 0xB00327C8, 0xBF597FC7, 0xC6E00BF3, 0xD5A79147, 0x06CA6351, 0x14292967,
)


def require(cond: bool, msg: str) -> None:
    if not cond:
        raise SystemExit("FAIL: " + msg)


def ror(x, r):
    return ((x >> r) | (x << (32 - r))) & M32


def S0(x):
    return ror(x, 2) ^ ror(x, 13) ^ ror(x, 22)


def S1(x):
    return ror(x, 6) ^ ror(x, 11) ^ ror(x, 25)


def s0(x):
    return ror(x, 7) ^ ror(x, 18) ^ (x >> 3)


def s1(x):
    return ror(x, 17) ^ ror(x, 19) ^ (x >> 10)


def IF(e, f, g):
    return ((e & f) ^ (~e & g)) & M32


def MAJ(a, b, c):
    return (a & b) ^ (a & c) ^ (b & c)


# ---------------------------------------------------------------------------------------------
# 1. Fig. 6 (rows 0..22; position k is bit 31-k), advice
# ---------------------------------------------------------------------------------------------
EQ = "=" * 32
FIG6 = {  # i: (A row, E row, W row)
    0: (EQ, EQ, EQ), 1: (EQ, EQ, EQ), 2: (EQ, EQ, EQ),
    3: (EQ, "=====1=====011======0======0====", EQ),
    4: ("==n=============================", "==n0=0=1===100=0==0=1===0==1=0=1", "==n============================="),
    5: ("=====n===n===n=u====n===u==u====", "01011u001n=nuu=11000n=1=101u=100", "=====u===u==========n==========="),
    6: (EQ, "101n=0=1=1=n1111==n0u===n=0n=n=u", "==n============================="),
    7: (EQ, "10u0=1=101==00=n==0=0===0==0=0=0", "=======n=======u===u====u=1=u=u="),
    8: (EQ, "uuu1=0=111=0=0=01=1=01==1==1=1=0", "============u=======uu=========="),
    9: ("==========u====================u", "11=10n0nuuu00n0u101=n11=u01u=unn", EQ),
    10: (EQ, "un111111001001111=010u=u0=001100", EQ),
    11: ("====n=========u=u=======u==n====", "1011n111100010u1u0111111u=nu1001", EQ),
    12: ("=un===u=n=======n===============", "001uuu11uuuuuuuu11n1000n1uuu1001", "=====n===n==========u==========="),
    13: (EQ, "=n1111uu1n00000u1u0=nnn01111010n", "==u============================="),
    14: ("==u=============================", "=0=100110000000=101=0000=110===0", EQ),
    15: (EQ, "=1====0011===u10001=011===0n===1", EQ),
    16: (EQ, "======u=n====1==n=====0===01====", EQ),
    17: (EQ, "======0=0====1==0==========1====", EQ),
    18: (EQ, "==u===1=0=======1====1==========", EQ),
    19: (EQ, "==0=============================", EQ),
    20: (EQ, "==1=============================", "=====0=nn=====0=u=1============="),
    21: (EQ, EQ, EQ),
    22: (EQ, EQ, "==n============================="),
}


def row(kind: str, i: int) -> str:
    return FIG6[i]["AEW".index(kind)] if i in FIG6 else EQ


def FL(kind, i):
    return sum(1 << (31 - k) for k, c in enumerate(row(kind, i)) if c in "nu")


def Dsigned(kind, i):  # primed - unprimed, n: 0->1 (+), u: 1->0 (-)
    return sum((1 if c == "n" else -1) << (31 - k) for k, c in enumerate(row(kind, i)) if c in "nu")


def fixmask(kind, i):
    m = v = 0
    for k, c in enumerate(row(kind, i)):
        b = 1 << (31 - k)
        if c in "nu01":
            m |= b
            if c in "u1":
                v |= b
    return m, v


def free_bits(kind, i):
    return sorted(31 - k for k, c in enumerate(row(kind, i)) if c == "=")


def expand(kind, i, k):
    """Deposit bit t of k into the t-th lowest '=' position; fixed positions get the unprimed sign value."""
    x = fixmask(kind, i)[1]
    for t, b in enumerate(free_bits(kind, i)):
        if (k >> t) & 1:
            x |= 1 << b
    return x


def bit(x, i):
    return (x >> i) & 1


ADV_A = dict(zip(range(4, 14), (0x98560DBB, 0x633B16BA, 0x9BCF7BBE, 0xF8677AD6, 0x4A299906, 0x44F24AB5,
                                0x39781650, 0x6422EDC8, 0x574542B8, 0x0508C8F0)))
ADV_E = dict(zip(range(8, 14), (0xF1CAE594, 0xD0E1B7B4, 0xBF27D74C, 0xB78BBFD9, 0x3FFFD0F9, 0xBF81C0F4)))
A, E = ADV_A, ADV_E
Ap = {i: A[i] ^ FL("A", i) for i in A}
Ep = {i: E[i] ^ FL("E", i) for i in E}
FLW = [FL("W", i) for i in range(32)]

for i in range(4, 14):
    m, v = fixmask("A", i)
    require(A[i] & m == v, f"advice A{i} violates its row")
for i in range(8, 14):
    m, v = fixmask("E", i)
    require(E[i] & m == v, f"advice E{i} violates its row")
for i in (0, 1, 2, 9, 10, 14, 15, 16, 17):
    require(FLW[i] == 0, f"W{i} has a difference")
require(FL("E", 14) == 0 and FL("A", 13) == 0 and FL("A", 15) == 0 and FL("A", 16) == 0
        and FL("A", 17) == 0 and FL("E", 17) == 0, "zero-difference rows used by the reduction")
require(FL("A", 14) == 1 << 29, "A14 difference is exactly bit 29")

FL15, FL16 = FL("E", 15), FL("E", 16)
D16 = Dsigned("E", 16) % (1 << 32)
V16 = sum(1 << (31 - k) for k, c in enumerate(row("E", 16)) if c == "u")  # unprimed 1 at u positions
KS = S1(FL16)                                         # Sigma1 is XOR-linear
DC = (A[13] + E[13] - Ap[13] - Ep[13]) & M32         # (A13+E13) - (A13'+E13')

# ---------------------------------------------------------------------------------------------
# 2./3. P4 rebuild and twelve-word rows
# ---------------------------------------------------------------------------------------------
FIELDS = ("W14", "W15", "s1W14", "s1W15", "oE", "oEp", "oA", "oAp", "A14", "A15", "E14", "E15")


def build_p4():
    p14 = []
    m14, v14 = fixmask("A", 14)
    for i in range(256):
        e14 = expand("E", 14, i)
        a14 = (e14 - A[10] + S0(A[13]) + MAJ(A[13], A[12], A[11])) & M32
        w14 = (e14 - A[10] - E[10] - S1(E[13]) - IF(E[13], E[12], E[11]) - K[14]) & M32
        ok = (a14 & m14) == v14 and bit(a14, 9) == bit(a14, 20)
        ok = ok and bit(a14, 18) != bit(a14, 6) and bit(a14, 8) != bit(a14, 17)
        ok = ok and all(bit(A[13], j) == bit(a14, j) for j in (30, 25, 23)) and bit(A[13], 15) != bit(a14, 15)
        if ok:
            p14.append((e14, a14, w14))
    require(len(p14) == 12, f"P14 has {len(p14)} rows, expected 12")
    rows, groups = [], []
    m15, v15 = fixmask("A", 15)
    for g, (e14, a14, w14) in enumerate(p14):
        start = len(rows)
        e14p, a14p = e14 ^ FL("E", 14), a14 ^ FL("A", 14)
        for j in range(1 << 15):
            e15 = expand("E", 15, j)
            a15 = (e15 - A[11] + S0(a14) + MAJ(a14, A[13], A[12])) & M32
            w15 = (e15 - A[11] - E[11] - S1(e14) - IF(e14, E[13], E[12]) - K[15]) & M32
            if (a15 & m15) != v15 or bit(A[13], 29) == bit(a15, 29):
                continue
            e15p, a15p = e15 ^ FL15, a15 ^ FL("A", 15)
            ok = ((Ap[10] + Ep[10] + S1(Ep[13]) + IF(Ep[13], Ep[12], Ep[11]) + K[14] + w14) & M32) == e14p
            ok &= ((e14p - Ap[10] + S0(Ap[13]) + MAJ(Ap[13], Ap[12], Ap[11])) & M32) == a14p
            ok &= ((Ap[11] + Ep[11] + S1(e14p) + IF(e14p, Ep[13], Ep[12]) + K[15] + w15) & M32) == e15p
            ok &= ((e15p - Ap[11] + S0(a14p) + MAJ(a14p, Ap[13], Ap[12])) & M32) == a15p
            if not ok:
                continue
            # step16_constants_both: E16-W16, E16'-W16, A16-E16, A16'-E16'
            oE = (A[12] + E[12] + S1(e15) + IF(e15, e14, E[13]) + K[16]) & M32
            oEp = (Ap[12] + Ep[12] + S1(e15p) + IF(e15p, e14p, Ep[13]) + K[16]) & M32
            oA = (-A[12] + S0(a15) + MAJ(a15, a14, A[13])) & M32
            oAp = (-Ap[12] + S0(a15p) + MAJ(a15p, a14p, Ap[13])) & M32
            rows.append((w14, w15, s1(w14), s1(w15), oE, oEp, oA, oAp, a14, a15, e14, e15))
        groups.append((start, len(rows)))
        require(len(rows) - start == 1 << 14, f"group {g} has {len(rows) - start} rows")
    require(len(rows) == 196608, "P4 size")
    return rows, groups


# ---------------------------------------------------------------------------------------------
# 4. Scalar reference (full step equations, both branches)
# ---------------------------------------------------------------------------------------------
def ref_stage16_17(w: list[int], r: tuple) -> tuple[bool, bool]:
    """w = unprimed W0..W15 of the candidate (W14, W15 from the P4 row); r = 12-word P4 row.
    Returns (stage-16 pass, stage-16-and-17 pass) of Section 4 Step 3."""
    wp = [w[i] ^ FLW[i] for i in range(16)]
    W14, W15, _, _, _, _, _, _, a14, a15, e14, e15 = r
    st = {"A": {12: A[12], 13: A[13], 14: a14, 15: a15}, "E": {12: E[12], 13: E[13], 14: e14, 15: e15}}
    stp = {"A": {i: v ^ FL("A", i) for i, v in st["A"].items()},
           "E": {i: v ^ FL("E", i) for i, v in st["E"].items()}}
    ok = [True, True]
    for i in (16, 17):
        Wi = (s1(w[i - 2]) + w[i - 7] + s0(w[i - 15]) + w[i - 16]) & M32
        Wpi = (s1(wp[i - 2]) + wp[i - 7] + s0(wp[i - 15]) + wp[i - 16]) & M32
        w.append(Wi)
        wp.append(Wpi)
        res = []
        for s, ww in ((st, w), (stp, wp)):
            a, e = s["A"], s["E"]
            e[i] = (a[i - 4] + e[i - 4] + S1(e[i - 1]) + IF(e[i - 1], e[i - 2], e[i - 3]) + K[i] + ww[i]) & M32
            a[i] = (e[i] - a[i - 4] + S0(a[i - 1]) + MAJ(a[i - 1], a[i - 2], a[i - 3])) & M32
        good = (Wpi == Wi ^ FLW[i] and stp["E"][i] == st["E"][i] ^ FL("E", i)
                and stp["A"][i] == st["A"][i] ^ FL("A", i))
        ok[i - 16] = good
        if not good:
            break
    w[:] = w[:16]
    return ok[0], ok[0] and ok[1]


class NpRef:
    """numpy vectorisation of ref_stage16_17 over all P4 rows (natural order)."""

    def __init__(self, rows):
        a = np.array(rows, dtype=np.uint64).astype(np.uint32)
        self.c = {f: a[:, k] for k, f in enumerate(FIELDS)}

    @staticmethod
    def _ror(x, r):
        return (x >> np.uint32(r)) | (x << np.uint32(32 - r))

    def S1(self, x):
        return self._ror(x, 6) ^ self._ror(x, 11) ^ self._ror(x, 25)

    def S0(self, x):
        return self._ror(x, 2) ^ self._ror(x, 13) ^ self._ror(x, 22)

    def s1(self, x):
        return self._ror(x, 17) ^ self._ror(x, 19) ^ (x >> np.uint32(10))

    def run(self, w: list[int]):
        with np.errstate(over="ignore"):
            return self._run(w)

    def _run(self, w: list[int]):
        u = np.uint32
        c = self.c
        W14, W15 = c["W14"], c["W15"]
        a14, a15, e14, e15 = c["A14"], c["A15"], c["E14"], c["E15"]
        out = []
        for prime in (0, 1):
            fa = (lambda i: u(FL("A", i))) if prime else (lambda i: u(0))
            fe = (lambda i: u(FL("E", i))) if prime else (lambda i: u(0))
            ww = [x ^ (FLW[i] if prime else 0) for i, x in enumerate(w[:14])]
            W16 = self.s1(W14) + u(ww[9]) + u(s0(ww[1])) + u(ww[0])
            W17 = self.s1(W15) + u(ww[10]) + u(s0(ww[2])) + u(ww[1])
            A12, A13, E12, E13 = u(A[12]) ^ fa(12), u(A[13]) ^ fa(13), u(E[12]) ^ fe(12), u(E[13]) ^ fe(13)
            A14, A15, E14, E15 = a14 ^ fa(14), a15 ^ fa(15), e14 ^ fe(14), e15 ^ fe(15)
            E16 = A12 + E12 + self.S1(E15) + ((E15 & E14) ^ (~E15 & E13)) + u(K[16]) + W16
            A16 = E16 - A12 + self.S0(A15) + ((A15 & A14) ^ (A15 & A13) ^ (A14 & A13))
            E17 = A13 + E13 + self.S1(E16) + ((E16 & E15) ^ (~E16 & E14)) + u(K[17]) + W17
            A17 = E17 - A13 + self.S0(A16) + ((A16 & A15) ^ (A16 & A14) ^ (A15 & A14))
            out.append((W16, W17, E16, A16, E17, A17))
        (W16, W17, E16, A16, E17, A17), (W16p, W17p, E16p, A16p, E17p, A17p) = out
        p16 = (W16p == W16) & (E16p == (E16 ^ u(FL16))) & (A16p == A16)
        p17 = p16 & (W17p == W17) & (E17p == E17) & (A17p == A17)
        return p16, p17


# ---------------------------------------------------------------------------------------------
# 5. SWAR: 7 lanes x 36 bits, guard bits 32..35
# ---------------------------------------------------------------------------------------------
L7, LB = 7, 36
M256 = (1 << 256) - 1


def bc(v):  # lane broadcast of a constant (built once, public)
    return sum((v & ((1 << LB) - 1)) << (LB * l) for l in range(L7))


Mb, Gb = bc(M32), bc(1 << 32)
FL16b, V16b, FL15b, KSb, DCb, B29b = bc(FL16), bc(V16), bc(FL15), bc(KS), bc(DC), bc(1 << 29)
ROT = {}
for _r in (6, 11, 25):
    lo = (1 << (32 - _r)) - 1
    ROT[_r] = (bc(lo), bc(M32 ^ lo))


def dummy_mask(nreal):
    return sum(1 << (LB * l) for l in range(nreal, L7))


class Ops:
    """Counts primitive 256-bit word-RAM operations per block; optional lane-overflow audit."""

    def __init__(self, audit=False):
        self.n = {}
        self.blk = "setup"
        self.audit = audit
        self.max_lane = 0

    def _c(self, k=1):
        self.n[self.blk] = self.n.get(self.blk, 0) + k

    def _r(self, v):
        self._c()
        return v & M256

    def add(self, a, b):
        # Lane-overflow audit: every 256-bit addition must be carry-free across 36-bit lanes,
        # i.e. for every lane l the exact lane sum a_l + b_l is below 2^36.
        if self.audit:
            for l in range(L7):
                lv = ((a >> (LB * l)) & ((1 << LB) - 1)) + ((b >> (LB * l)) & ((1 << LB) - 1))
                if lv > self.max_lane:
                    self.max_lane = lv
        return self._r(a + b)

    def xor(self, a, b):
        return self._r(a ^ b)

    def and_(self, a, b):
        return self._r(a & b)

    def or_(self, a, b):
        return self._r(a | b)

    def shr(self, a, k):
        return self._r(a >> k)

    def shl(self, a, k):
        return self._r(a << k)

    def load(self, arr, i):  # one address op + one load
        self._c(2)
        return arr[i]

    def cmp(self):
        self._c()

    def br(self):
        self._c()

    def capcheck(self):  # work counter += constant envelope, compare with W_cap, branch
        self._c(3)

    def rotr(self, x, r):
        m_lo, m_hi = ROT[r]
        return self.or_(self.and_(self.shr(x, r), m_lo), self.and_(self.shl(x, 32 - r), m_hi))

    def Sigma1(self, x):
        return self.xor(self.xor(self.rotr(x, 6), self.rotr(x, 11)), self.rotr(x, 25))


class Layout:
    """Lane-packed P4: each W14 group padded to 2341 packs (last pack: 4 real lanes)."""

    def __init__(self, rows, groups, order_key=None):
        self.packs_per_group = -(-(1 << 14) // L7)  # 2341
        self.idx, self.real = [], []
        self.grp = []
        for g, (s, e) in enumerate(groups):
            ids = list(range(s, e))
            if order_key is not None:
                ids.sort(key=lambda r: order_key(rows[r]))
            for p in range(self.packs_per_group):
                lane_ids = ids[p * L7:(p + 1) * L7]
                self.idx.append(lane_ids)
                self.real.append(len(lane_ids))
                self.grp.append(g)
        self.np = len(self.idx)
        f = {k: [] for k in ("OFFE", "OFFEA29", "P", "OFFEp", "OFFA29", "OFFAp29")}
        for lane_ids in self.idx:
            acc = {k: 0 for k in f}
            for l, r in enumerate(lane_ids):
                w = dict(zip(FIELDS, rows[r]))
                a15b = bit(w["A15"], 29) << 29
                vals = {
                    "OFFE": w["oE"],
                    "OFFEA29": ((w["oE"] + w["oA"]) & M32) + a15b,      # < 2^32 + 2^29
                    "P": w["E15"] ^ w["E14"],
                    "OFFEp": w["oEp"],
                    "OFFA29": w["oA"] + a15b,                            # < 2^33
                    "OFFAp29": w["oAp"] + a15b,
                }
                for k, v in vals.items():
                    require(v < 1 << LB, "field exceeds lane")
                    acc[k] |= v << (LB * l)
            for k in f:
                f[k].append(acc[k])
        self.f = f
        g0 = [rows[s] for s, _ in groups]
        self.S1W14b = [bc(dict(zip(FIELDS, r))["s1W14"]) for r in g0]
        self.E14b = [bc(dict(zip(FIELDS, r))["E14"]) for r in g0]


def bcast_ops(ops, x):  # scalar < 2^32 in lane 0 -> all 7 lanes: 3 shift + 3 OR + 1 AND
    y = ops.or_(x, ops.shl(x, 36))
    y = ops.or_(y, ops.shl(y, 72))
    y = ops.or_(y, ops.shl(y, 144))
    return ops.and_(y, Mb)


def swar_tuple(lay: Layout, c16: int, ops: Ops, variant="reduced", full17=False):
    """Run stages 16..17 for every pack of one valid tuple.

    Returns (pass16 bitmask list per pack, pass17 bitmask list per pack, stats).
    full17=True evaluates the stage-17 block on every pack (validation of all lane decisions);
    full17=False is the algorithm (stage 17 only if some lane passed stage 16)."""
    ops.blk = "setup"
    # constants into registers (Mb, Gb, FL16b, V16b, FL15b, KSb, DCb, B29b, 6 rot masks): 14 loads
    for _ in range(14):
        ops.load([0], 0)
    c16b = bcast_ops(ops, c16)
    p16m, p17m = [], []
    stats = {"packs": 0, "packs_any16": 0, "packs_any17": 0, "passers17": 0}
    f = lay.f
    ppg = lay.packs_per_group
    for g in range(len(lay.S1W14b)):
        ops.blk = "setup"
        W16b = ops.add(c16b, ops.load(lay.S1W14b, g))  # < 2^33 per lane (unreduced)
        E14b = ops.load(lay.E14b, g)
        for _ in range(4):  # group pointer/bound setup, group loop compare+branch
            ops._c()
        ops.capcheck()  # reserve the deterministic stage-16 envelope of all 2341 packs of the group
        for p in range(g * ppg, (g + 1) * ppg):
            stats["packs"] += 1
            ops.blk = "st16"
            if variant == "reduced":
                S = ops.add(W16b, ops.load(f["OFFE"], p))
                T16 = ops.and_(ops.xor(S, V16b), FL16b)
                A16x = None
            else:
                S = ops.add(W16b, ops.load(f["OFFE"], p))
                Sp = ops.add(W16b, ops.load(f["OFFEp"], p))
                A16x = ops.add(S, ops.load(f["OFFA29"], p))
                A16px = ops.add(Sp, ops.load(f["OFFAp29"], p))
                x = ops.xor(ops.xor(S, Sp), FL16b)
                T16 = ops.and_(ops.or_(x, ops.xor(A16x, A16px)), Mb)
            if lay.real[p] < L7:
                ops.blk = "setup"  # peeled last pack of the group: force dummy lanes to fail
                T16 = ops.or_(T16, ops.load([dummy_mask(lay.real[p])], 0))
                ops.blk = "st16"
            N16 = ops.and_(ops.add(T16, Mb), Gb)
            ops.cmp()
            ops.br()
            any16 = N16 != Gb
            p16m.append(((N16 ^ Gb) >> 32))
            ops.cmp()  # loop control: pointer bound compare + branch (pointer bump = address ops)
            ops.br()
            if not any16 and not full17:
                p17m.append(0)
                continue
            if any16:
                stats["packs_any16"] += 1
            ops.blk = "st17" if any16 else "st17_validation_only"
            ops.capcheck()
            E16m = ops.and_(S, Mb)
            sg = ops.Sigma1(E16m)
            sgp = ops.xor(sg, KSb)
            P = ops.load(f["P"], p)
            IFu = ops.xor(E14b, ops.and_(E16m, P))
            E16pm = ops.xor(E16m, FL16b) if variant == "reduced" else ops.and_(Sp, Mb)
            Pp = ops.xor(P, FL15b)
            IFp = ops.xor(E14b, ops.and_(E16pm, Pp))
            Lv = ops.add(ops.add(sg, IFu), DCb)
            Rv = ops.add(sgp, IFp)
            D17 = ops.and_(ops.xor(Lv, Rv), Mb)
            if variant == "reduced":
                A16x = ops.add(W16b, ops.load(f["OFFEA29"], p))
            X29 = ops.and_(A16x, B29b)
            Z = ops.or_(ops.or_(D17, X29), T16)
            N17 = ops.and_(ops.add(Z, Mb), Gb)
            ops.cmp()
            ops.br()
            p17m.append(((N17 ^ Gb) >> 32))
            if N17 != Gb:
                stats["packs_any17"] += 1
                ops.blk = "extract"
                ops.capcheck()
                PM = ops.xor(N17, Gb)
                for l in range(L7):
                    t = ops.and_(ops.shr(PM, LB * l + 32), 1)
                    ops.br()
                    if t:
                        stats["passers17"] += 1
                        ops._c(2)  # candidate index = pack base + l, hand-off
                        ops.blk = "scalar_tail"
                        ops._c(48 + 256 + 2048)  # unchanged scalar Step-3 code from stage 16 on
                        ops.blk = "extract"
    return p16m, p17m, stats


def lane_bits(mask_list, lay: Layout):
    """Per-row decisions (natural row index) from per-pack lane masks (bit 36l set = pass)."""
    out = np.zeros(196608, dtype=bool)
    for p, m in enumerate(mask_list):
        if m:
            for l, r in enumerate(lay.idx[p]):
                if (m >> (LB * l)) & 1:
                    out[r] = True
    return out


# ---------------------------------------------------------------------------------------------
# 7. Exact Pr[some lane of a pack passes stage 16] for uniform W16 mod 2^26 (interval measure)
# ---------------------------------------------------------------------------------------------
def pack_any16_exact(lay: Layout, rows):
    """Pass16 <=> (W16 + oE) mod 2^26 lies in S = {y: y25=1, y23=0, y15=0} = 256 intervals of 2^15.
    For each pack, the measure of {t mod 2^26 : some real lane passes} / 2^26."""
    MOD, LEN = 1 << 26, 1 << 15
    starts = np.array([(1 << 25) + (((b & 0x7F) << 16) | ((b >> 7) << 24)) for b in range(256)], dtype=np.int64)
    for s in starts:  # sanity: interval [s, s+2^15) is inside S and they partition S
        require(bit(int(s), 25) == 1 and bit(int(s), 23) == 0 and bit(int(s), 15) == 0 and int(s) & 0x7FFF == 0, "S")
    oE = np.array([r[4] for r in rows], dtype=np.int64) % MOD
    res = np.zeros(lay.np)
    for p, ids in enumerate(lay.idx):
        t = ((starts[None, :] - oE[ids][:, None]) % MOD).ravel()
        t.sort()
        gaps = np.diff(np.concatenate([t, [t[0] + MOD]]))
        res[p] = np.minimum(gaps, LEN).sum() / MOD
    return res


def max_survivors16(groups, rows):
    """For each group, max over W16 of the number of rows passing stage 16 (sweep over 2^26 shifts)."""
    MOD, LEN = 1 << 26, 1 << 15
    starts = np.array([(1 << 25) + (((b & 0x7F) << 16) | ((b >> 7) << 24)) for b in range(256)], dtype=np.int64)
    out = []
    for s, e in groups:
        oE = np.array([rows[r][4] for r in range(s, e)], dtype=np.int64) % MOD
        enter = ((starts[None, :] - oE[:, None]) % MOD).ravel()
        leave = (enter + LEN) % MOD
        ev_t = np.concatenate([enter, leave])
        ev_d = np.concatenate([np.ones_like(enter), -np.ones_like(leave)])
        order = np.lexsort((ev_d, ev_t))  # at equal t: leave (-1) before enter (+1); intervals are [enter, leave)
        ev_d = ev_d[order]
        init = int((enter >= MOD - LEN).sum())  # intervals containing t = -1 (mod 2^26)
        cs = init + np.cumsum(ev_d)
        out.append(int(cs.max()))
    return out


# ---------------------------------------------------------------------------------------------
# 8. Ledger and optimisation
# ---------------------------------------------------------------------------------------------
def optimise(EXb, V, Mbound, C_units, label, w_lo=None, w_hi=None, verbose=False, target="0.3901"):
    import mpmath as mp
    mp.mp.dps = 60
    s = mp.power(2, mp.mpf("-45.8192425647"))
    D = 2 ** 35

    def P(T, w):
        d = mp.mpf(w) - mp.mpf(EXb)
        T = mp.mpf(T)
        return 1 - mp.e ** (-s * T) - mp.e ** (-(d * T) ** 2 / (2 * (T * V + Mbound * d * T / 3)))

    def total(T, w):
        num = mp.mpf(2928 * (-(-T // 7)) + 32 * T) + mp.mpf(w) * T
        return int(mp.ceil(num / 2224 + 14)) + C_units + D

    best = None
    w = mp.mpf(w_lo) if w_lo is not None else mp.ceil((mp.mpf(EXb) + mp.mpf("0.1")) * 10) / 10
    w_hi = mp.mpf(w_hi) if w_hi is not None else mp.mpf(EXb) + 12
    rows = []
    while w <= w_hi:
        lo, hi = 1, 1 << 46
        if P(hi, w) < mp.mpf(target):
            w += mp.mpf("0.1")
            continue
        while hi - lo > 1:
            mid = (lo + hi) // 2
            if P(mid, w) >= mp.mpf(target):
                hi = mid
            else:
                lo = mid
        tot = total(hi, w)
        rows.append((float(w), hi, tot))
        if best is None or tot < best[2]:
            best = (mp.nstr(w, 6), hi, tot, float(mp.log(tot, 2)), float(P(hi, w)))
        w += mp.mpf("0.1")
    if verbose:
        print(label, "best", best)
    return best, rows


def ledger(p16any_mean, p16any_label, f16=0.126, f17=2 ** -14.9, variant="reduced", s3max_override=None,
           extra_C_ops=0, c16_override=None, c17_override=None):
    NP = 12 * 2341
    q = 2 ** -17.3166
    c16 = 11 if variant == "reduced" else 23
    if c16_override is not None:
        c16 = c16_override
    c17 = 45 if variant == "reduced" else 42
    if c17_override is not None:
        c17 = c17_override
    cext, chand, ctail = 25, 2, 48 + 256 + 2048
    setup = 600  # inherited 300 (unchanged) + 300 allowance for the new per-tuple SWAR setup (215 counted)
    # expected Step-3 demand per valid tuple
    e_any17 = min(1.0, 7 * f17)
    S3E = setup + NP * (c16 + p16any_mean * c17) + NP * e_any17 * cext + 196608 * f17 * (chand + ctail)
    S3max = setup + NP * (max(c16, 11) + c17 + cext) + 196608 * (chand + ctail)
    if s3max_override is not None:
        S3max = s3max_override
    step3 = q * S3E
    EX = 5 * 0.325212 + 0.32522 * 192 + step3
    EXb = math.ceil(EX * 1000) / 1000
    Mbound = 5 * 936 + 936 * (1304 + S3max)
    EX2 = 3 * (25 * 936 * 0.325212 + 1304 ** 2 * 4 * 5.758e9 / 2 ** 32 + S3max ** 2 * q * (1 + 2 ** -4))
    V = math.ceil(EX2 / 1e8) * 1e8
    C_units = 303675466808 + math.ceil(extra_C_ops / 2224)
    comp = dict(st16=NP * c16 / 196608, st17=NP * p16any_mean * c17 / 196608, extract=NP * e_any17 * cext / 196608,
                tail=f17 * (chand + ctail), c16=c16, c17=c17, cext=cext, setup=setup)
    return dict(components=comp, variant=variant, p16any=p16any_mean, p16any_label=p16any_label, per_tuple_S3E=S3E,
                per_candidate=(S3E - setup) / 196608, step3_term=step3, EX=EX, EXb=EXb, S3max=S3max,
                per_candidate_max=(S3max - setup) / 196608, M=Mbound, EX2=EX2, V=V, C_units=C_units)


# ---------------------------------------------------------------------------------------------
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--tuples", type=int, default=40, help="random tuples, all 196,608 candidates each")
    ap.add_argument("--targeted", type=int, default=20000, help="targeted stage-17 pack tests")
    ap.add_argument("--seed", type=int, default=20261008)
    ap.add_argument("--skip-opt", action="store_true")
    ap.add_argument("--f17-mc", type=int, default=0,
                    help="extra numpy-reference Monte Carlo of stage-16/17 rates over N uniform tuples (~27 ms each)")
    args = ap.parse_args()
    rng = random.Random(args.seed)
    report = {}
    t0 = time.time()

    rows, groups = build_p4()
    report["P4"] = {"rows": len(rows), "groups": [e - s for s, e in groups],
                    "W14": sorted({f"{r[0]:08x}" for r in rows})}
    print(f"[P4] {len(rows)} rows in {len(groups)} groups of {groups[0][1]-groups[0][0]} ({time.time()-t0:.1f}s)")

    # Row identities (build-time assertions used by the 'reduced' variant)
    for r in rows:
        w = dict(zip(FIELDS, r))
        delta = (w["oEp"] - w["oE"]) & M32
        require(delta == D16, "row identity 1: E16'-E16 == D(E16)")
        require((delta + w["oAp"] - w["oA"]) & M32 == 0, "row identity 2: A16'-A16 == 0")
    for g, (s, e) in enumerate(groups):
        require(len({rows[r][0] for r in range(s, e)}) == 1 and len({rows[r][10] for r in range(s, e)}) == 1,
                "W14/E14 constant within group")
    print("[P4] row identities hold for all 196,608 rows: E16'-E16 == D(E16) = %08x, A16'-A16 == 0" % D16)

    # Witnesses: the #227 certified pair and S's Table 3 pair (unprimed = the advice branch)
    witnesses = {
        "#227": ((0xE890C4BA, 0x6BCE94E6, 0x47A0B812, 0xC5EF36B2, 0xEC7B7814, 0x91CF09DF, 0xA9717904, 0x494BC86F),
                 [0xE37CAB30, 0x5F4048FD, 0x95CAA0FC, 0x87591D98, 0xDB8464A3, 0x3DDCC0F3, 0x4C91C8C4, 0x7C619FBE,
                  0x4EEB7E52, 0x58E49D82, 0x10746273, 0xA96CE154, 0x41B22A2C, 0x6D12F88A, 0xD2701ECE, 0x17D9748F]),
        "S Table 3": ((0xC4369610, 0xC91F70A7, 0x87E430E6, 0xA5E58128, 0xD29CB97B, 0x9AB268D1, 0x8788F401, 0x629F6CB2),
                      [0xC0008214, 0xAE65F3BF, 0xE93C006A, 0x5F195AA9, 0x84D6CD0F, 0x25C114EC, 0xCA897317, 0xDA9FD6EF,
                       0x6EC97E18, 0x5100DA8A, 0x0912E57B, 0xA96B2054, 0x41B22A2C, 0x6D12F88A, 0xD2701ECC, 0x140976D1]),
    }
    row_index = {(r[0], r[1]): k for k, r in enumerate(rows)}
    wit_rows = {}
    for name, (cv, w) in witnesses.items():
        k = row_index.get((w[14], w[15]))
        require(k is not None, f"{name}: (W14, W15) not in P4")
        # full trace of both branches through step 17
        for prime in (0, 1):
            ww = [x ^ (FLW[i] if prime else 0) for i, x in enumerate(w)]
            for i in range(16, 18):
                ww.append((s1(ww[i - 2]) + ww[i - 7] + s0(ww[i - 15]) + ww[i - 16]) & M32)
            a = {-4: cv[3], -3: cv[2], -2: cv[1], -1: cv[0]}
            e = {-4: cv[7], -3: cv[6], -2: cv[5], -1: cv[4]}
            for i in range(18):
                e[i] = (a[i - 4] + e[i - 4] + S1(e[i - 1]) + IF(e[i - 1], e[i - 2], e[i - 3]) + K[i] + ww[i]) & M32
                a[i] = (e[i] - a[i - 4] + S0(a[i - 1]) + MAJ(a[i - 1], a[i - 2], a[i - 3])) & M32
            fa = (lambda i: FL("A", i)) if prime else (lambda i: 0)
            fe = (lambda i: FL("E", i)) if prime else (lambda i: 0)
            for i in range(4, 14):
                require(a[i] == A[i] ^ fa(i), f"{name}: A{i} != advice")
            for i in range(8, 14):
                require(e[i] == E[i] ^ fe(i), f"{name}: E{i} != advice")
            rr = dict(zip(FIELDS, rows[k]))
            require((a[14], a[15], e[14], e[15]) == (rr["A14"] ^ fa(14), rr["A15"], rr["E14"], rr["E15"] ^ fe(15)),
                    f"{name}: step-14/15 states != P4 row")
            if prime == 0:
                tr0 = (a[16], e[16], a[17], e[17], ww[16])
            else:
                tr1 = (a[16], e[16], a[17], e[17], ww[16])
        require(tr1[0] == tr0[0] and tr1[1] == tr0[1] ^ FL16 and tr1[2] == tr0[2] and tr1[3] == tr0[3],
                f"{name}: trace does not conform at 16/17")
        require(ref_stage16_17(list(w), rows[k]) == (True, True), f"{name}: reference rejects the witness")
        require((tr0[4] + rows[k][4]) & M32 == tr0[1], f"{name}: stored E16-W16 offset mismatch")
        wit_rows[name] = (k, w)
    print("[witness] both published pairs: (W14,W15) in P4, states 4..15 match, trace conforms at 16..17, "
          "reference accepts")
    report["witness_rows"] = {n: v[0] for n, v in wit_rows.items()}

    # Layouts
    lay_nat = Layout(rows, groups)
    lay_srt = Layout(rows, groups, order_key=lambda r: r[4] % (1 << 26))
    print(f"[layout] {lay_nat.np} packs ({lay_nat.packs_per_group} per group) ({time.time()-t0:.1f}s)")

    npref = NpRef(rows)

    def c16_of(w):
        return (w[9] + s0(w[1]) + w[0]) & M32

    # ---- 6. validation
    val = {"tuples": 0, "lane_decisions_compared": 0, "mismatches": 0, "py_ref_rows_checked": 0,
           "pass16": 0, "pass17": 0, "lanes": 0, "packs_any16": {}, "max_lane_sum_bits": 0}
    configs = [("reduced", lay_nat, "natural"), ("reduced", lay_srt, "sorted"), ("general", lay_nat, "natural")]
    any16_counts = {f"{v}/{n}": [0, 0] for v, _, n in configs}
    tuples = [("witness #227", wit_rows["#227"][1][:14]), ("witness S", wit_rows["S Table 3"][1][:14])]
    for _ in range(args.tuples):
        tuples.append(("random", [rng.getrandbits(32) for _ in range(14)]))
    for ti, (kind, w14) in enumerate(tuples):
        r16, r17 = npref.run(w14)
        # pure-Python reference on a random subsample (+ every numpy-positive stage-17 row)
        sub = rng.sample(range(196608), 1500) + list(np.nonzero(r17)[0])
        for k in sub:
            ww = list(w14) + [rows[k][0], rows[k][1]]
            require(ref_stage16_17(ww, rows[k]) == (bool(r16[k]), bool(r17[k])), "numpy vs pure-Python reference")
        val["py_ref_rows_checked"] += len(sub)
        c16 = c16_of(w14)
        for variant, lay, lname in configs:
            ops = Ops(audit=(ti == 2))
            p16m, p17m, st = swar_tuple(lay, c16, ops, variant, full17=True)
            if ops.audit:
                val["max_lane_sum_bits"] = max(val["max_lane_sum_bits"], ops.max_lane.bit_length())
                require(ops.max_lane < 1 << LB, "lane overflow")
            s16, s17 = lane_bits(p16m, lay), lane_bits(p17m, lay)
            mism = int((s16 != r16).sum() + (s17 != r17).sum())
            val["mismatches"] += mism
            val["lane_decisions_compared"] += 2 * 196608
            any16_counts[f"{variant}/{lname}"][0] += st["packs_any16"]
            any16_counts[f"{variant}/{lname}"][1] += st["packs"]
            require(mism == 0, f"SWAR mismatch tuple {ti} {variant}/{lname}: {mism}")
        val["tuples"] += 1
        if kind == "random":
            val["pass16"] += int(r16.sum())
            val["pass17"] += int(r17.sum())
            val["lanes"] += 196608
        else:
            k = wit_rows["#227" if ti == 0 else "S Table 3"][0]
            require(bool(r17[k]), "witness candidate must pass 17")
        print(f"[val] tuple {ti} ({kind}): stage16 {int(r16.sum())}, stage17 {int(r17.sum())}, "
              f"0 mismatches x {len(configs)} configs ({time.time()-t0:.1f}s)")
    val["packs_any16"] = {k: v[0] / v[1] for k, v in any16_counts.items()}

    # targeted stage-17 cases: force a chosen lane through stage 16 (and E16's printed conditions)
    tgt = {"packs": 0, "lane_decisions_compared": 0, "mismatches": 0, "forced_lane_pass17": 0}
    for _ in range(args.targeted):
        variant, lay, lname = configs[rng.randrange(3)]
        p = rng.randrange(lay.np)
        l = rng.randrange(lay.real[p])
        k = lay.idx[p][l]
        e16 = rng.getrandbits(32)
        e16 = (e16 & ~FL16) | V16
        e16 = (e16 & ~((1 << 18) | (1 << 9) | (1 << 5) | (1 << 4))) | (1 << 18) | (1 << 4)
        for x, y in ((1, 28), (7, 20), (2, 20), (11, 6)):  # E16[28,20,20,6] = E16[1,7,2,11]
            e16 = (e16 & ~(1 << x)) | (bit(e16, y) << x)
        for x, y in ((12, 30), (10, 28)):                   # E16[30,28] != E16[12,10]
            e16 = (e16 & ~(1 << x)) | ((bit(e16, y) ^ 1) << x)
        e16 = (e16 & ~(1 << 29)) | ((bit(e16, 10) ^ 1) << 29)  # E16[10] != E16[29]
        W16 = (e16 - rows[k][4]) & M32
        w14 = [rng.getrandbits(32) for _ in range(14)]
        w14[0] = (W16 - rows[k][2] - w14[9] - s0(w14[1])) & M32  # c16 = W16 - s1(W14)
        c16 = c16_of(w14)
        # SWAR on this single pack only
        sub = Layout.__new__(Layout)
        sub.packs_per_group, sub.np = 1, 1
        sub.idx, sub.real, sub.grp = [lay.idx[p]], [lay.real[p]], [0]
        sub.f = {kk: [vv[p]] for kk, vv in lay.f.items()}
        g = lay.grp[p]
        sub.S1W14b, sub.E14b = [lay.S1W14b[g]], [lay.E14b[g]]
        ops = Ops(audit=True)
        p16m, p17m, _ = swar_tuple(sub, c16, ops, variant, full17=True)
        require(ops.max_lane < 1 << LB, "lane overflow (targeted)")
        for ll, kk in enumerate(lay.idx[p]):
            ww = list(w14) + [rows[kk][0], rows[kk][1]]
            a, b = ref_stage16_17(ww, rows[kk])
            sa, sb = bool((p16m[0] >> (LB * ll)) & 1), bool((p17m[0] >> (LB * ll)) & 1)
            tgt["lane_decisions_compared"] += 2
            tgt["mismatches"] += (a != sa) + (b != sb)
            require(a == sa and b == sb, "targeted mismatch")
            if ll == l:
                require(a, "forced lane must pass stage 16")
                tgt["forced_lane_pass17"] += b
        tgt["packs"] += 1
    val["targeted"] = tgt
    print(f"[val] targeted: {tgt} ({time.time()-t0:.1f}s)")
    report["validation"] = val
    if args.f17_mc:
        n16 = n17 = 0
        per = []
        for _ in range(args.f17_mc):
            a, b = npref.run([rng.getrandbits(32) for _ in range(14)])
            n16 += int(a.sum())
            per.append(int(b.sum()))
        n17 = sum(per)
        mean = n17 / len(per)
        sd = math.sqrt(sum((x - mean) ** 2 for x in per) / max(1, len(per) - 1))
        report["rate_mc"] = {"tuples": args.f17_mc, "f16": n16 / (196608 * args.f17_mc), "pass17": n17,
                             "log2_f17": math.log2(n17 / (196608 * args.f17_mc)) if n17 else None,
                             "rel_se_tuple_clustered": sd / math.sqrt(len(per)) / mean if n17 else None}
        print("[mc]", report["rate_mc"])

    # algorithm-mode op counts on a few tuples (early abort), checked against the ledger formula
    counts = {}
    for variant, lay, lname in configs:
        tot = {}
        nt = 4
        for _ in range(nt):
            w14 = [rng.getrandbits(32) for _ in range(14)]
            ops = Ops()
            _, _, st = swar_tuple(lay, c16_of(w14), ops, variant, full17=False)
            for kk, vv in ops.n.items():
                tot[kk] = tot.get(kk, 0) + vv
            tot["packs_any16"] = tot.get("packs_any16", 0) + st["packs_any16"]
        counts[f"{variant}/{lname}"] = {kk: vv / nt for kk, vv in tot.items()}
    report["algorithm_mode_mean_ops_per_tuple"] = counts
    print("[ops] mean per tuple:", json.dumps(counts, indent=None))

    # ---- 7. exact pack-any probabilities and worst-case survivors
    pa_nat = pack_any16_exact(lay_nat, rows)
    pa_srt = pack_any16_exact(lay_srt, rows)
    surv = max_survivors16(groups, rows)
    report["pack_any16_exact_uniformW16"] = {"natural": float(pa_nat.mean()), "sorted": float(pa_srt.mean()),
                                            "independent_lanes_1-(7/8)^7": 1 - (7 / 8) ** 7,
                                            "union_bound_7*0.126": 7 * 0.126}
    report["max_stage16_survivors_per_group"] = surv
    report["max_stage16_survivors_total"] = sum(surv)
    print(f"[exact] Pr[pack any16] natural {pa_nat.mean():.6f} sorted {pa_srt.mean():.6f}; "
          f"max stage-16 survivors/group {surv} ({time.time()-t0:.1f}s)")

    # ---- 8. ledger + optimisation
    extra_C_relayout = 196608 * 128 + 12 * 1024
    extra_C_sort = 196608 * 1024
    extra_C_sweep = 12 * (1 << 23) * 256
    scen = {
        "A_reduced_sorted_exact": ledger(pa_srt.mean() * 0.126 / 0.125, "sorted exact x1.008", variant="reduced",
                                         extra_C_ops=extra_C_relayout + extra_C_sort),
        "B_reduced_natural_exact": ledger(pa_nat.mean() * 0.126 / 0.125, "natural exact x1.008", variant="reduced",
                                          extra_C_ops=extra_C_relayout),
        "C_reduced_union_bound": ledger(min(1.0, 7 * 0.126), "union bound 7 f16", variant="reduced",
                                        extra_C_ops=extra_C_relayout),
        "D_general_union_bound": ledger(min(1.0, 7 * 0.126), "union bound 7 f16", variant="general",
                                        extra_C_ops=extra_C_relayout),
    }
    s3max_sweep = 600 + 12 * 2341 * (11 + 45 + 25) + sum(surv) * (2 + 48 + 256 + 2048)
    scen["E_A_plus_sweep_worstcase"] = ledger(pa_srt.mean() * 0.126 / 0.125, "sorted exact x1.008",
                                              variant="reduced", s3max_override=s3max_sweep,
                                              extra_C_ops=extra_C_relayout + extra_C_sort + extra_C_sweep)
    scen["F_A_unrolled_no_loop_control"] = ledger(pa_srt.mean() * 0.126 / 0.125, "sorted exact x1.008",
                                                  variant="reduced", c16_override=9,
                                                  extra_C_ops=extra_C_relayout + extra_C_sort)
    scen["G_A_rotation_masks_reloaded_per_stage17"] = ledger(pa_srt.mean() * 0.126 / 0.125, "sorted exact x1.008",
                                                            variant="reduced", c17_override=45 + 12,
                                                            extra_C_ops=extra_C_relayout + extra_C_sort)
    scen["H_most_conservative_general_union_masks_reloaded"] = ledger(min(1.0, 7 * 0.126), "union bound 7 f16",
                                                              variant="general", c17_override=42 + 12,
                                                              extra_C_ops=extra_C_relayout)
    report["extra_C_ops"] = {"relayout": extra_C_relayout, "sort": extra_C_sort, "sweep_assert": extra_C_sweep}
    if not args.skip_opt:
        # reproduce the base proof's optimum as a self-check of the optimiser
        base_best, _ = optimise(160.82, 4.18e12, 432828513000, 303675466808, "base", w_lo="162.5", w_hi="162.5")
        report["base_check"] = base_best
        print("[opt] base check (w=162.5):", base_best)
        for name, L in scen.items():
            best, _ = optimise(L["EXb"], L["V"], L["M"], L["C_units"], name)
            L["best"] = best
            import mpmath as mp
            mp.mp.dps = 60
            w_, T_ = mp.mpf(best[0]), best[1]
            d_ = w_ - mp.mpf(L["EXb"])
            sT = mp.power(2, mp.mpf("-45.8192425647")) * T_
            cap = mp.e ** (-(d_ * T_) ** 2 / (2 * (T_ * L["V"] + L["M"] * d_ * T_ / 3)))
            B7 = -(-T_ // 7)
            AB = int(mp.ceil((mp.mpf(2928 * B7 + 32 * T_) + w_ * T_) / 2224 + 14))
            L["detail"] = dict(w=best[0], T=T_, log2T=float(mp.log(T_, 2)), B7=B7, d=float(d_), sT=float(sT),
                               cap_stop=float(cap), P=float(1 - mp.e ** (-sT) - cap), AB_units=AB,
                               C_units=L["C_units"], D_units=2 ** 35, total=AB + L["C_units"] + 2 ** 35,
                               log2_total=float(mp.log(AB + L["C_units"] + 2 ** 35, 2)))
            require(L["detail"]["total"] == best[2], "total recomputation")
            print(f"[opt] {name}: EX {L['EX']:.4f} (bound {L['EXb']}), V {L['V']:.4e}, M {L['M']:.6e}, "
                  f"best w,T,total,log2,P = {best}")
    report["scenarios"] = scen
    report["seconds"] = time.time() - t0
    with open("step3_swar_results.json", "w") as fh:
        json.dump(report, fh, indent=1, default=str)
    print(json.dumps({k: report[k] for k in ("validation", "pack_any16_exact_uniformW16")}, indent=1))
    print(f"done in {time.time()-t0:.1f}s")


if __name__ == "__main__":
    main()
```

## Appendix F. The measurement's tools (participant tools)

The simulator, builders, sampler, analysis and condition-count scripts of Section 5.1, with sha256. The
pre-registration is listed first. Raw outputs (run logs, samples, the rebuilt table slices) are not
included; their sha256 values are in the campaign's SHA256SUMS, whose own sha256 is listed below. The
embedded files are hash-pinned and cite 'Section 9.1' of our earlier package; that material is Section 5.1
here. The two
job scripts and the copy script only set local directories and run the listed programs under a resource
guard; they are listed by sha256 only.

sha256 8d3ffe66a2671cc99cd8150491f32e42d1a4bc910f3bd96e2af3e2278bec0cdf  PREREGISTRATION.md
sha256 8ea0d2c6f2faf9f33984df64fcc8e70c078e9970a72d49b7d78c54234e394065  condexp.c
sha256 a1a35956567149c95e50aa8d7f0269437a7735148bb86dea74520bdbea4281a3  copass.c
sha256 ddce6d9112e5e14e72fb1dcc6644c43486e1eae93838711969d8f220b123adfc  params.h
sha256 0cbd2c4843d8694e90533b2b091d85bffff3f6031d98d8b136d36a67d2e4062a  mkparams.py
sha256 5b0d1aefa2780b18f1b5b5e9ec3a260d35aefe9cc2a273e0743f00f8fefbffe1  secondblock.py
sha256 21f5147a06f3e327310d4c050b2860e87133f363bee8f772ca99a75c029ab5e4  step3ref.py
sha256 fa61c384ba96ec32547c5233a7525113a8d901d7869d3b9625d37f8c98155513  check_route.py
sha256 17faeb7737d929a54bfcf06df06935eb3c5913daaf42d46f3d34322e6f0e6a33  table.py
sha256 0a5071cedfc21fea2573dde7c644ae54e7e9fdaaf1c719dcd02a39474ea3e941  slices.py
sha256 de6aecbc69d450b62afc477774632d6d5ed49becce3e7842f6ac0eabb1c9361d  sample.py
sha256 5340566812ebeb737ba6332f7a30aefb88a740059062e012d684c39637ff8d89  analyse_m.py
sha256 ea0449483faa64d84234a2dc2a9505a0c46de09c2377e2dcbc07cf15b2067f7c  e2e.py
sha256 1aff7056da5aa5132c85b70745e23da28e189334d4efe48e817d872a106ecc77  conddump.c
sha256 07a854cd426c9c73bb799ee5074bd64d86ebce9f31f5bd7d39df40de7e5056d1  conds.py
sha256 3d830b80605a881ae796d04b128efe98b106f061c7062ef4e0ef46fd085ab7f8  CONDITIONS.md
sha256 de611ccf7a235ce87a76480039ea8a4423b0673c664a863037614c6fa61ebf91  job1.sh
sha256 580d10577508369f90d01b70b84c6f39766ce3c4a81166ee0c85a961b805f8e4  job2.sh
sha256 62310bd4e5d66c4ade8c52969f2980912e9a14578605a407aa9298f80b767f9d  finalize.py
sha256 e2b26106b7653acf5ff278895c30869a7bb963e087688dc4a4ef2bb870d1e63b  SHA256SUMS

### F.1 `PREREGISTRATION.md`

```
# Pre-registered design: per-candidate Step-3 rate of sha256-r32 (stages 16..31)

Written 2026-10-08 14:58 KST, before any run of this campaign. The file is not edited after the first run. Any
departure is listed under "Deviations" in README.md.

## Estimand

p = Pr[a P4 candidate passes stages 16..31], averaged over the valid tuples that real trials produce
(occurrence-weighted) and over uniform P4 entries and uniform W16..W19 (their law for a valid tuple, proof Section 9.1).
A valid tuple of record r arises with probability proportional to r's validity weight w_r = Pr[r valid | CV1[0] =
key(r)], so p = sum_r w_r p_r / sum_r w_r, where p_r is the mean rate over r's valid tuples.

## Sample

- Table: real TAB2 records (P1-P3 of table.py, unchanged predicates), keys with top byte in
  {0x00, 0x20, 0x40, 0x60, 0x80, 0xa0, 0xc0, 0xe0} (8 slices, 1/32 of the key space, singleton classes included).
  The total record count must equal the published N = 1,396,774,912.
- Sub-sample: each record of those slices kept with probability 2^-10 (generator seeded with (31001, chunk index),
  chunks of 512 P3 pairs). Class sizes come from all keys of the slices.
- Records: uniform random order of the sub-sample (seed 31002, same generator as the pool), examined until 700
  records with nonzero weight are found. Every examined record is listed, weight 0 included.
- Weight: a pool of 2^20 uniform W-valid triples (sign bits fixed, other bits uniform, kept when tests (a)-(d), (f),
  (g) pass; seed 31002). w_r = fraction of the pool that passes r's test (e). Records with no accepted entry get 0.
- Tuples: 2 per nonzero-weight record, uniform without reuse among its accepted pool entries: 1,400 tuple-constant
  vectors (condexp.c's MAXC).
- The 520 single-event vectors of v8 are not used: they were selected through pair events and their record
  identities were not kept, so no weight can be attached.

## Runs

- Primary: condexp.c (unchanged from v8) on the 1,400 vectors, 30 batches, seeds 4000-4029, n16 = 10^10 each,
  M17 = 1024, M18 = 64, M19 = 1. Job 1 runs seeds 4000-4009, job 2 seeds 4010-4029.
- Co-pass and replication: copass.c, seeds 6000-6009, n16 = 10^10, same M, K19 = 1024, first 20 full passes of each
  process dumped.
- End-to-end: e2e.py on every dumped pass.

## Analysis (analyse_m.py)

Notation: n_bc = all-pass count of vector c in batch b; H_b = n16 * M17 * M18 * M19; p_c = sum_b n_bc / sum_b H_b;
p_r = mean of p_c over r's vectors; w_r = estimated weight.

1. Point estimates: p_occ = sum_r w_r p_r / sum_r w_r over examined records; p_unif = mean of p_r over nonzero-weight
   records; r19 = sum c19 / sum H (through step 19); r_late = p_occ / r19 (stages 20..31), with the stage-wise
   conditionals 20|19, 21|20, 22|21, 23..31|22.
2. Uncertainty: SE_batch from the 30 per-batch values of p_occ; SE_rec by linearization over all examined records,
   z_r = w_r (p_r - p_occ), SE_rec^2 = n/(n-1) sum z_r^2 / (sum w_r)^2; SE = sqrt(SE_batch^2 + SE_rec^2).
   Bounds: p_occ -+ 2.756 SE (t, 0.995, 29 df) and -+ 3 SE. Two-way bootstrap, 4000 replicates, seed 7001
   (records and batches resampled with replacement), 0.5% and 99.5% percentiles.
   p_L = smaller of the t and bootstrap lower bounds; p_U = larger of the upper bounds.
3. Heterogeneity, each at alpha = 0.01:
   - vectors: X^2 = sum_c (n_c - mean)^2 / mean, df = C - 1;
   - records: X^2 = sum_r (n_r - k_r mean)^2 / (k_r mean), df = R - 1;
   - split halves (even and odd batches, independent histories): Pearson correlation of per-vector and of per-record
     rates, permutation p-value (10,000 permutations, seed 7002); between-unit variance tau^2 = covariance of the two
     halves, reported as tau / p;
   - groups: slice (8), class size (1, 2, 3-4, 5-8, >= 9), weight below or above the median nonzero weight; ratio of
     the group's p_occ to the overall, z-test with SE from records and Poisson; Bonferroni over all groups at family
     alpha = 0.01. Material = ratio outside [0.95, 1.05] and significant;
   - single records: largest |z_r| against the Bonferroni threshold for R records.
4. Second moment: m2 = sum_c omega_c p_c(even) p_c(odd) with omega_c = w_r / k_r normalized (unbiased for the
   occurrence-weighted mean of p_J^2); m2 / p^2 with bootstrap 99% upper bound; p_U2 = sqrt(upper bound of m2).
5. Co-pass: E[number of other entries of the same tuple that pass | an entry passes] = (passes found) / (events),
   99% Poisson upper bound, split by same and other W14 group; through-19 conditional rate over r19, same and other
   group. E[C(Y_J, 2)] <= E[Y_J] * U / 2, U the upper bound.
6. Checks: copass.c's own per-vector counts (seeds 6000-6009) give an independent p_occ that must agree with the
   primary within 3 SE (not pooled). Every dumped pass must give a 32-step collision with all fixed words matching.
```

### F.2 `condexp.c`

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

### F.3 `copass.c`

```c
/* Co-passing P4 entries of one tuple. For a fixed tuple and chaining value every P4 entry e gets its own W16..W19,
 * and the words of two entries differ by known amounts, since W0..W13 are shared:
 *   W16' = W16 + s1(W14') - s1(W14),  W17' = W17 + s1(W15') - s1(W15),
 *   W18' = W18 + s1(W16') - s1(W16),  W19' = W19 + s1(W17') - s1(W17).
 * Entries with the same W14 share W16, W18 and W20. Histories of a uniform entry are sampled with condexp.c's scheme
 * (the extra draws for K19 make the random streams differ from condexp.c's for the same seed). For every history through step 19, K19 other entries of the same W14 group and K19
 * entries of other groups are tested through step 19. For every full pass (history, tuple vector), every other entry
 * is tested through stage 31 with the same vector. The first MAXDUMP full passes are written to DUMP for an
 * end-to-end check. Per-vector counts are printed in condexp.c's format.
 * usage: copass p4.bin cvec.txt seed n16 M17 M18 M19 K19 DUMP MAXDUMP
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

typedef struct { uint32_t A[23], E[23]; } side;

static inline void step(side *x, int i, uint32_t w) {
    x->E[i] = x->A[i - 4] + x->E[i - 4] + BS1(x->E[i - 1]) + IFF(x->E[i - 1], x->E[i - 2], x->E[i - 3]) + K[i] + w;
    x->A[i] = x->E[i] - x->A[i - 4] + BS0(x->A[i - 1]) + MAJ(x->A[i - 1], x->A[i - 2], x->A[i - 3]);
}
static inline int conf(const side *u, const side *p, int i) {
    return ((u->A[i] ^ p->A[i]) == FLA[i]) && ((u->E[i] ^ p->E[i]) == FLE[i]);
}

#define MAXC 1400
static uint32_t *P; static int n4;
static side u0, p0;
static uint32_t C[MAXC][7];

static inline void load(int e, side *u, side *p) {
    const uint32_t *x = P + 10 * e;
    *u = u0; *p = p0;
    u->E[14] = x[0]; u->A[14] = x[1]; p->E[14] = x[2]; p->A[14] = x[3];
    u->E[15] = x[4]; u->A[15] = x[5]; p->E[15] = x[6]; p->A[15] = x[7];
}
/* Stages 16..19 of entry e with words W[0..3] = W16..W19; on success leaves the states in *u, *p. */
static inline int thru19(int e, const uint32_t *W, side *u, side *p) {
    load(e, u, p);
    for (int i = 16; i < 20; i++) {
        step(u, i, W[i - 16]); step(p, i, W[i - 16]);
        if (!conf(u, p, i)) return 0;
    }
    return 1;
}
/* Stages 20..31 with vector c from states after step 19; W = W16..W19, w14/w15 of the entry. */
static inline int late(int c, const side *u19, const side *p19, const uint32_t *W, uint32_t W14, uint32_t W15) {
    side a = *u19, b = *p19;
    uint32_t W20 = SS1(W[2]) + C[c][0], W20p = SS1(W[2]) + C[c][1];
    if ((W20 ^ W20p) != FLW20 || (W20 & SGM20) != SGV20) return 0;
    step(&a, 20, W20); step(&b, 20, W20p);
    if (!conf(&a, &b, 20)) return 0;
    uint32_t W21 = SS1(W[3]) + W14 + C[c][2];
    step(&a, 21, W21); step(&b, 21, W21);
    if (!conf(&a, &b, 21)) return 0;
    uint32_t W22 = SS1(W20) + W15 + C[c][3], W22p = SS1(W20p) + W15 + C[c][4];
    if ((W22 ^ W22p) != FLW22 || (W22 & SGM22) != SGV22) return 0;
    step(&a, 22, W22); step(&b, 22, W22p);
    if (!conf(&a, &b, 22)) return 0;
    uint32_t d24 = SS1(W22p) - SS1(W22) + C[c][5], d29 = (W22p - W22) + C[c][6];
    return d24 == 0 && d29 == 0;
}
static inline void other_words(int e, int f, const uint32_t *W, uint32_t *V) {
    const uint32_t *x = P + 10 * e, *y = P + 10 * f;
    V[0] = W[0] + SS1(y[8]) - SS1(x[8]);
    V[1] = W[1] + SS1(y[9]) - SS1(x[9]);
    V[2] = W[2] + SS1(V[0]) - SS1(W[0]);
    V[3] = W[3] + SS1(V[1]) - SS1(W[1]);
}

int main(int argc, char **argv) {
    if (argc < 11) { fprintf(stderr, "usage\n"); return 1; }
    FILE *f = fopen(argv[1], "rb");
    fseek(f, 0, SEEK_END); long nb = ftell(f); fseek(f, 0, SEEK_SET);
    n4 = (int)(nb / 40);
    P = malloc(nb);
    if (fread(P, 1, nb, f) != (size_t)nb) return 2;
    fclose(f);
    int nc = 0;
    f = fopen(argv[2], "r");
    while (nc < MAXC && fscanf(f, "%x %x %x %x %x %x %x", &C[nc][0], &C[nc][1], &C[nc][2], &C[nc][3], &C[nc][4],
                               &C[nc][5], &C[nc][6]) == 7) nc++;
    fclose(f);
    uint64_t seed = strtoull(argv[3], 0, 10), n16 = strtoull(argv[4], 0, 10);
    int M17 = atoi(argv[5]), M18 = atoi(argv[6]), M19 = atoi(argv[7]), K19 = atoi(argv[8]), maxdump = atoi(argv[10]);
    FILE *dump = fopen(argv[9], "w");
    /* W14 groups */
    int *grp = malloc(sizeof(int) * n4), ng = 0, *gsize = calloc(n4, sizeof(int)), **members = calloc(n4, sizeof(int *));
    uint32_t gw[64];
    for (int e = 0; e < n4; e++) {
        int g = 0;
        while (g < ng && gw[g] != P[10 * e + 8]) g++;
        if (g == ng) { if (ng == 64) return 3; gw[ng++] = P[10 * e + 8]; }
        grp[e] = g;
    }
    for (int e = 0; e < n4; e++) gsize[grp[e]]++;
    for (int g = 0; g < ng; g++) { members[g] = malloc(sizeof(int) * gsize[g]); gsize[g] = 0; }
    for (int e = 0; e < n4; e++) members[grp[e]][gsize[grp[e]]++] = e;

    for (int k = 0; k < 4; k++) s[k] = splitmix(&seed);
    uint64_t c16 = 0, c17 = 0, c18 = 0, c19 = 0, p20[MAXC] = {0}, p21[MAXC] = {0}, p22[MAXC] = {0}, pall[MAXC] = {0};
    uint64_t t19[2] = {0, 0}, h19[2] = {0, 0};            /* [same group, other group]: tested, passed through 19 */
    uint64_t ev = 0, tall[2] = {0, 0}, a19[2] = {0, 0}, aall[2] = {0, 0};  /* conditional on a full pass */
    int ndump = 0;
    u0.A[12] = A12; u0.A[13] = A13; u0.E[12] = E12; u0.E[13] = E13;
    p0.A[12] = AP12; p0.A[13] = AP13; p0.E[12] = EP12; p0.E[13] = EP13;
    for (uint64_t t = 0; t < n16; t++) {
        uint64_t r = next();
        int e = (int)((uint32_t)(r >> 32) % (uint32_t)n4);
        const uint32_t *x = P + 10 * e;
        side u, p;
        load(e, &u, &p);
        uint32_t W14 = x[8], W15 = x[9];
        uint32_t W16 = (uint32_t)r;
        step(&u, 16, W16); step(&p, 16, W16);
        if (!conf(&u, &p, 16)) continue;
        c16++;
        {
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
                    uint32_t W[4] = {W16, W17, W18, W19}, V[4];
                    side a, b;
                    int g = grp[e];
                    for (int k = 0; k < K19; k++) {          /* same W14 group */
                        int f2 = members[g][(uint32_t)next() % (uint32_t)gsize[g]];
                        if (f2 == e) continue;
                        other_words(e, f2, W, V);
                        t19[0]++; h19[0] += thru19(f2, V, &a, &b);
                    }
                    for (int k = 0; k < K19; k++) {          /* other groups */
                        int f2 = (int)((uint32_t)next() % (uint32_t)n4);
                        if (grp[f2] == g) continue;
                        other_words(e, f2, W, V);
                        t19[1]++; h19[1] += thru19(f2, V, &a, &b);
                    }
                    for (int c = 0; c < nc; c++) {
                        side aa = u19, bb = p19;
                        uint32_t W20 = SS1(W18) + C[c][0], W20p = SS1(W18) + C[c][1];
                        if ((W20 ^ W20p) != FLW20 || (W20 & SGM20) != SGV20) continue;
                        step(&aa, 20, W20); step(&bb, 20, W20p);
                        if (!conf(&aa, &bb, 20)) continue;
                        p20[c]++;
                        uint32_t W21 = SS1(W19) + W14 + C[c][2];
                        step(&aa, 21, W21); step(&bb, 21, W21);
                        if (!conf(&aa, &bb, 21)) continue;
                        p21[c]++;
                        uint32_t W22 = SS1(W20) + W15 + C[c][3], W22p = SS1(W20p) + W15 + C[c][4];
                        if ((W22 ^ W22p) != FLW22 || (W22 & SGM22) != SGV22) continue;
                        step(&aa, 22, W22); step(&bb, 22, W22p);
                        if (!conf(&aa, &bb, 22)) continue;
                        p22[c]++;
                        uint32_t d24 = SS1(W22p) - SS1(W22) + C[c][5], d29 = (W22p - W22) + C[c][6];
                        if (!(d24 == 0 && d29 == 0)) continue;
                        pall[c]++;
                        if (!late(c, &u19, &p19, W, W14, W15)) return 4;   /* the helper must agree */
                        ev++;
                        if (ndump < maxdump) {
                            fprintf(dump, "%d %08x %08x %08x %08x %d\n", e, W16, W17, W18, W19, c);
                            ndump++;
                        }
                        for (int f2 = 0; f2 < n4; f2++) {    /* every other entry, same vector */
                            if (f2 == e) continue;
                            int sg = grp[f2] == g ? 0 : 1;
                            other_words(e, f2, W, V);
                            tall[sg]++;
                            if (!thru19(f2, V, &a, &b)) continue;
                            a19[sg]++;
                            aall[sg] += late(c, &a, &b, V, P[10 * f2 + 8], P[10 * f2 + 9]);
                        }
                    }
                }
            }
        }
    }
    fclose(dump);
    printf("n16 %llu c16 %llu c17 %llu c18 %llu c19 %llu M %d %d %d\n", (unsigned long long)n16,
           (unsigned long long)c16, (unsigned long long)c17, (unsigned long long)c18, (unsigned long long)c19, M17, M18, M19);
    printf("groups %d K19 %d\n", ng, K19);
    printf("given19 same tested %llu passed19 %llu other tested %llu passed19 %llu\n", (unsigned long long)t19[0],
           (unsigned long long)h19[0], (unsigned long long)t19[1], (unsigned long long)h19[1]);
    printf("givenall events %llu same tested %llu passed19 %llu passedall %llu other tested %llu passed19 %llu passedall %llu\n",
           (unsigned long long)ev, (unsigned long long)tall[0], (unsigned long long)a19[0], (unsigned long long)aall[0],
           (unsigned long long)tall[1], (unsigned long long)a19[1], (unsigned long long)aall[1]);
    for (int c = 0; c < nc; c++)
        printf("c %d %llu %llu %llu %llu\n", c, (unsigned long long)p20[c], (unsigned long long)p21[c],
               (unsigned long long)p22[c], (unsigned long long)pall[c]);
    return 0;
}
```

### F.4 `params.h`

```c
/* generated by mkparams.py */
#define A12 0x574542b8u
#define A13 0x0508c8f0u
#define E12 0x3fffd0f9u
#define E13 0xbf81c0f4u
#define AP12 0x35c5c2b8u
#define AP13 0x0508c8f0u
#define EP12 0x2300f189u
#define EP13 0xfcc08ef5u
#define FLA16 0x00000000u
#define FLE16 0x02808000u
#define FLA17 0x00000000u
#define FLE17 0x00000000u
#define FLA18 0x00000000u
#define FLE18 0x20000000u
#define FLA19 0x00000000u
#define FLE19 0x00000000u
#define FLA20 0x00000000u
#define FLE20 0x00000000u
#define FLA21 0x00000000u
#define FLE21 0x00000000u
#define FLA22 0x00000000u
#define FLE22 0x00000000u
#define FLW20 0x01808000u
#define SGM20 0x01808000u
#define SGV20 0x00008000u
#define FLW22 0x20000000u
#define SGM22 0x20000000u
#define SGV22 0x00000000u
```

### F.5 `mkparams.py`

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

### F.6 `secondblock.py`

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

### F.7 `step3ref.py`

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

### F.8 `check_route.py`

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

### F.9 `table.py`

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

### F.10 `slices.py`

```python
"""Uniform sample of real TAB2 records from several key slices, in one pass over P3 x L7 (proof Section 4).

P1, P2 and P3 come from table.py; the per-record predicates below are those of table.py's w7_job. Every record whose
key has its top byte in BYTES is kept as a key (to give its class size). Each such record also enters the sample with
probability 2^-SUBLOG2, decided by a generator seeded with (SEED, chunk index), so the sample does not depend on the
number of processes. Checks: the total record count must equal the published N = 1,396,774,912.
usage: slices.py NPROC SEED SUBLOG2 OUT.npz BYTE [BYTE ...]
"""
import sys, time, warnings
import numpy as np
from multiprocessing import Pool
warnings.filterwarnings('ignore')
import table as T
from secondblock import S0, S1, s0, IF, MAJ, K

CHUNK = 512
N_PUBLISHED = 1396774912
G = {}

def init(comb, pairs, L7, keep, seed, sublog2):
    G.update(comb=comb, pairs=pairs, L7=L7, keep=keep, seed=seed, sublog2=sublog2)

def job(ci):
    comb, pairs, L7, keep, R = G['comb'], G['pairs'], G['L7'], G['keep'], T.R
    rng = np.random.default_rng([G['seed'], ci])
    thr = 2.0 ** -G['sublog2']
    keys, sub, counts = [], [], np.zeros(256, dtype=np.int64)
    for pi in range(ci * CHUNK, min((ci + 1) * CHUNK, len(pairs))):
        cj, e4, a0, w8 = pairs[pi]
        e5, e6, e7, a1, a2, a3 = comb[cj][:6]
        w7 = L7
        e3 = e7 - a3 - w7 - S1(e6) - IF(e6, e5, e4) - K[7]                       # table.py w7_job, unchanged
        key = e3 - a3 + S0(a2) + MAJ(a2, a1, a0)
        ok = T.fix_ok('E', 3, e3)
        w7p, w8p = w7 ^ R.fl('W', 7), w8 ^ R.fl('W', 8)
        ok &= (s0(w8p) + w7p) == (s0(w8) + w7)
        e3p = e3 ^ R.fl('E', 3)
        a3p = a3 ^ R.fl('A', 3)
        e4p, e5p, e6p, e7p = e4 ^ R.fl('E', 4), e5 ^ R.fl('E', 5), e6 ^ R.fl('E', 6), e7 ^ R.fl('E', 7)
        e7c = a3p + e3p + S1(e6p) + IF(e6p, e5p, e4p) + K[7] + w7p
        ok &= e7c == e7p
        a3c = e3p - key + S0(a2 ^ R.fl('A', 2)) + MAJ(a2 ^ R.fl('A', 2), a1 ^ R.fl('A', 1), a0 ^ R.fl('A', 0))
        ok &= a3c == a3p
        k, e3k, w7k = key[ok], e3[ok], w7[ok]
        top = (k >> np.uint32(24)).astype(np.int64)
        counts += np.bincount(top, minlength=256)
        m = keep[top]
        keys.append(k[m])
        sel = m & (rng.random(len(k)) < thr)
        n = int(sel.sum())
        if n:
            sub.append(np.stack([np.full(n, pi, dtype=np.uint32), w7k[sel], e3k[sel], k[sel]], axis=1))
    return (np.concatenate(keys) if keys else np.zeros(0, np.uint32),
            np.concatenate(sub) if sub else np.zeros((0, 4), np.uint32), counts)

if __name__ == '__main__':
    nproc, seed, sublog2, outp = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]), sys.argv[4]
    bytes_ = sorted(int(b, 0) for b in sys.argv[5:])
    keep = np.zeros(256, dtype=bool); keep[bytes_] = True
    t = time.time()
    L4, L7 = T.p1(); comb = T.p2(); pairs = T.p3_pairs(comb, L4)
    print('|L4|', len(L4), '|L7|', len(L7), 'combinations', len(comb), 'pairs', len(pairs), round(time.time() - t), 's',
          flush=True)
    nchunks = (len(pairs) + CHUNK - 1) // CHUNK
    with Pool(nproc, initializer=init, initargs=(comb, pairs, L7, keep, seed, sublog2)) as pool:
        res = pool.map(job, range(nchunks), chunksize=1)
    counts = sum(r[2] for r in res)
    N = int(counts.sum())
    print('records (all keys)', N, round(time.time() - t), 's', flush=True)
    assert N == N_PUBLISHED, N
    keys = np.concatenate([r[0] for r in res])
    sub = np.concatenate([r[1] for r in res])
    keys.sort()
    lo = np.searchsorted(keys, sub[:, 3], 'left'); hi = np.searchsorted(keys, sub[:, 3], 'right')
    sub_cls = (hi - lo).astype(np.int64)
    _, cnt = np.unique(keys, return_counts=True)
    first = keys[np.r_[0, np.flatnonzero(np.diff(keys)) + 1]] if len(keys) else keys
    cls_top = (first >> np.uint32(24)).astype(np.int64)
    cls_hist = {int(b): np.bincount(np.minimum(cnt[cls_top == b], 64), minlength=65).tolist() for b in bytes_}
    print('kept slices', [hex(b) for b in bytes_], 'records in them', len(keys), '| sample', len(sub), flush=True)
    for b in bytes_:
        print(f'  slice 0x{b:02x}: records {int(counts[b])}, sample {int(((sub[:, 3] >> np.uint32(24)) == b).sum())}',
              flush=True)
    np.savez(outp, comb=comb, pairs=pairs, sub=sub, sub_cls=sub_cls, counts=counts, bytes=np.array(bytes_),
             L4=L4, L7=L7, N=N, cls_hist=np.array([cls_hist[b] for b in bytes_]))
    print('done', round(time.time() - t), 's', flush=True)
```

### F.11 `sample.py`

```python
"""Records drawn uniformly from the slice sample, their Step-2 validity weights, and uniform valid tuples.

For a record r with key k, a uniform CV1 with CV1[0] = k makes (W4, W5, W6) uniform (the bijection of proof
Section 9.1), so Pr[r valid | CV1[0] = k] = Pr[sign bits] * Pr[tests (a)-(d), (f), (g) | signs] * Pr[test (e) | W-valid].
Only the last factor depends on r. A pool of 2^POOLLOG2 uniform W-valid triples (sign bits fixed, other bits uniform,
kept when the record-free tests pass) is drawn once. A record's weight is the fraction of the pool that passes its
test (e); its tuples are drawn uniformly, without reuse across records, from those pool entries.
Records are examined in a uniformly random order until NVALID records with nonzero weight are found; every examined
record (weight 0 included) is listed.
usage: sample.py slices.npz SEED NVALID PER POOLLOG2 OUTPREFIX   (writes OUTPREFIX.cvec.txt and OUTPREFIX.records.json)
"""
import json, sys, time, warnings
import numpy as np
warnings.filterwarnings('ignore')
ARGS = sys.argv[1:]
import pairexp as PX

def pool_w_valid(rng, n):
    got, total = [], 0
    draws = 0
    while total < n:
        b = 1 << 22
        w = [rng.integers(0, 2 ** 32, b, dtype=np.uint64).astype(np.uint32) for _ in range(3)]
        for i, x in zip((4, 5, 6), w):
            m, v = PX.SG[i]
            x &= ~m; x |= v
        ok = PX.w_tests(*w)
        draws += b
        got.append(np.stack([x[ok] for x in w], axis=1)); total += int(ok.sum())
    return np.concatenate(got)[:n], draws

if __name__ == '__main__':
    path, seed, nvalid, per, poollog2, outp = ARGS[0], int(ARGS[1]), int(ARGS[2]), int(ARGS[3]), int(ARGS[4]), ARGS[5]
    t = time.time()
    d = np.load(path)
    comb, pairs, sub, sub_cls = d['comb'], d['pairs'], d['sub'], d['sub_cls']
    rng = np.random.default_rng(seed)
    pool, draws = pool_w_valid(rng, 1 << poollog2)
    w4, w5, w6 = pool[:, 0], pool[:, 1], pool[:, 2]
    print('pool', len(pool), 'W-valid of', draws, 'sign-fixed draws', round(time.time() - t), 's', flush=True)
    used = np.zeros(len(pool), dtype=bool)
    order = rng.permutation(len(sub))
    records, lines = [], []
    for idx in order:
        if sum(1 for r in records if r['accepted'] > 0) >= nvalid:
            break
        row = sub[idx]
        r = PX.record(comb, pairs, row)
        e0, e1, e2, *_ = PX.from_w(r, r['key'], w4, w5, w6)
        acc = PX.e_test(r, e0, e1, e2, w4, w5, w6)
        k = int(acc.sum())
        rec = dict(sample_index=int(idx), pair_index=int(row[0]), W7=int(row[1]), E3=int(row[2]), key=int(row[3]),
                   slice=int(row[3]) >> 24, class_size=int(sub_cls[idx]), accepted=k, pool=len(pool),
                   weight=k / len(pool), vectors=[], tuples=[])
        if k:
            free = np.flatnonzero(acc & ~used)
            pick = rng.choice(free, size=min(per, len(free)), replace=False)
            used[pick] = True
            for j in pick:
                vec = PX.cvec(r, w4[j], w5[j], w6[j])
                rec['vectors'].append(len(lines))
                rec['tuples'].append([int(w4[j]), int(w5[j]), int(w6[j])])
                lines.append(' '.join(f'{int(x) & 0xFFFFFFFF:08x}' for x in vec))
        records.append(rec)
    nv = sum(1 for r in records if r['accepted'] > 0)
    print('examined', len(records), 'records, nonzero weight', nv, 'vectors', len(lines), round(time.time() - t), 's',
          flush=True)
    assert nv == nvalid and len(lines) <= 1400
    open(outp + '.cvec.txt', 'w').write('\n'.join(lines) + '\n')
    json.dump(dict(seed=seed, nvalid=nvalid, per=per, pool=len(pool), pool_draws=draws, records=records),
              open(outp + '.records.json', 'w'))
```

### F.12 `analyse_m.py`

```python
"""Analysis of the pre-registered Step-3 rate campaign (PREREGISTRATION.md, section Analysis).
usage: analyse_m.py RECORDS.json SLICES.npz E2E.json --primary out... [--copass out...]   (JSON on stdout)"""
import json, math, sys, warnings
import numpy as np
warnings.filterwarnings('ignore', message='.*encountered in matmul')   # spurious BLAS flags on macOS

T_995 = {9: 3.250, 19: 2.861, 29: 2.756, 39: 2.708}   # t quantiles at 0.995 by degrees of freedom

def t995(df):
    z = 2.5758
    return T_995.get(df, z + (z ** 3 + z) / (4 * df))
Z_995 = 2.5758

def parse(path):
    lines = open(path).read().split('\n')
    h = lines[0].split()
    out = dict(n16=int(h[1]), c19=int(h[9]), M=[int(x) for x in h[11:14]], vec=[], extra={})
    for l in lines[1:]:
        f = l.split()
        if not f: continue
        if f[0] == 'c':
            out['vec'].append([int(x) for x in f[2:6]])
        elif f[0] == 'given19':
            out['extra']['t19'] = [int(f[3]), int(f[8])]; out['extra']['h19'] = [int(f[5]), int(f[10])]
        elif f[0] == 'givenall':
            out['extra'].update(events=int(f[2]), tall=[int(f[5]), int(f[12])], a19=[int(f[7]), int(f[14])],
                                aall=[int(f[9]), int(f[16])])
    out['vec'] = np.array(out['vec'], dtype=np.int64)
    out['H'] = out['n16'] * out['M'][0] * out['M'][1] * out['M'][2]
    return out

def chi2_upper_p(x, df):
    """Wilson-Hilferty upper tail of chi-square."""
    z = ((x / df) ** (1 / 3) - (1 - 2 / (9 * df))) / math.sqrt(2 / (9 * df))
    return 0.5 * math.erfc(z / math.sqrt(2))

def z_quantile(q):
    lo, hi = -40.0, 40.0
    for _ in range(200):
        mid = (lo + hi) / 2
        if 0.5 * math.erfc(-mid / math.sqrt(2)) < q: lo = mid
        else: hi = mid
    return (lo + hi) / 2

def poisson_upper(k, conf=0.99):
    """One-sided upper bound on a Poisson mean (chi-square with 2k+2 df, Wilson-Hilferty)."""
    df = 2 * k + 2; z = z_quantile(conf)
    return 0.5 * df * (1 - 2 / (9 * df) + z * math.sqrt(2 / (9 * df))) ** 3

def lg(x): return math.log2(x) if x > 0 else None

def weighted_rate(w, rate):
    return float((w * rate).sum() / w.sum())

def lin_se(w, rate, p):
    n = len(w)
    z = w * (rate - p)
    return math.sqrt(n / (n - 1) * (z ** 2).sum()) / w.sum()

if __name__ == '__main__':
    args = sys.argv[1:]
    recf, slf, e2ef = args[0], args[1], args[2]
    i_p = args.index('--primary'); i_c = args.index('--copass') if '--copass' in args else len(args)
    prim = [parse(p) for p in args[i_p + 1:i_c]]
    cop = [parse(p) for p in args[i_c + 1:]] if i_c < len(args) else []
    R = json.load(open(recf))
    recs = R['records']
    n_exam = len(recs)
    w = np.array([r['weight'] for r in recs])
    k = np.array([len(r['vectors']) for r in recs])
    C = int(k.sum())
    vec_rec = np.zeros(C, dtype=np.int64)
    for i, r in enumerate(recs):
        for v in r['vectors']: vec_rec[v] = i
    B = len(prim)
    H = np.array([o['H'] for o in prim], dtype=float)
    NB = np.stack([o['vec'][:C, 3] for o in prim])            # all-pass counts [batch, vector]
    S20 = np.stack([o['vec'][:C, 0] for o in prim]); S21 = np.stack([o['vec'][:C, 1] for o in prim])
    S22 = np.stack([o['vec'][:C, 2] for o in prim])
    c19 = np.array([o['c19'] for o in prim], dtype=float)

    def rec_matrix(X):           # per-record mean over its vectors, [records, batches]
        M = np.zeros((n_exam, X.shape[0]))
        np.add.at(M, vec_rec, X.T)
        return M / np.maximum(k, 1)[:, None]
    CR = rec_matrix(NB)
    rate_r = CR.sum(1) / H.sum()
    p_occ = weighted_rate(w, rate_r)
    nz = k > 0
    p_unif = float(rate_r[nz].mean())
    r19 = float(c19.sum() / H.sum())
    stage = {}
    for nm, X in (('20', S20), ('21', S21), ('22', S22)):
        stage[nm] = weighted_rate(w, rec_matrix(X).sum(1) / H.sum())
    cond = {'20|19': stage['20'] / r19, '21|20': stage['21'] / stage['20'], '22|21': stage['22'] / stage['21'],
            '23..31|22': p_occ / stage['22']}

    # uncertainty
    pb = np.array([weighted_rate(w, CR[:, b] / H[b]) for b in range(B)])
    se_batch = float(pb.std(ddof=1) / math.sqrt(B))
    se_rec = lin_se(w, rate_r, p_occ)
    se = math.sqrt(se_batch ** 2 + se_rec ** 2)
    rng = np.random.default_rng(7001)
    boot = np.empty(4000)
    for t in range(4000):
        rc = np.bincount(rng.integers(0, n_exam, n_exam), minlength=n_exam)
        bc = np.bincount(rng.integers(0, B, B), minlength=B)
        bcf = bc.astype(float)
        rr = CR @ bcf / (H @ bcf)
        boot[t] = (rc * w * rr).sum() / (rc * w).sum()
    assert np.isfinite(boot).all()
    b_lo, b_hi = float(np.quantile(boot, 0.005)), float(np.quantile(boot, 0.995))
    t_lo, t_hi = p_occ - t995(B - 1) * se, p_occ + t995(B - 1) * se
    p_L, p_U = min(t_lo, b_lo), max(t_hi, b_hi)
    r19_b = c19 / H
    se19 = float(r19_b.std(ddof=1) / math.sqrt(B))

    # heterogeneity
    n_c = NB.sum(0).astype(float); mean_c = n_c.mean()
    X2v = float(((n_c - mean_c) ** 2 / mean_c).sum())
    n_r = np.zeros(n_exam); np.add.at(n_r, vec_rec, n_c)
    E_r = k * mean_c
    X2r = float(((n_r[nz] - E_r[nz]) ** 2 / E_r[nz]).sum())
    even, odd = np.arange(0, B, 2), np.arange(1, B, 2)
    pe = NB[even].sum(0) / H[even].sum(); po = NB[odd].sum(0) / H[odd].sum()
    rng2 = np.random.default_rng(7002)
    def split(xe, xo):
        r = float(np.corrcoef(xe, xo)[0, 1])
        perm = np.array([np.corrcoef(xe, rng2.permutation(xo))[0, 1] for _ in range(10000)])
        tau2 = float(np.cov(xe, xo)[0, 1])
        return dict(pearson=r, perm_p=float((np.abs(perm) >= abs(r)).mean()), tau2=tau2,
                    tau_over_p=math.sqrt(max(tau2, 0)) / p_occ, tau2_over_p2=tau2 / p_occ ** 2)
    re = rec_matrix(NB[even]).sum(1)[nz] / H[even].sum(); ro = rec_matrix(NB[odd]).sum(1)[nz] / H[odd].sum()
    split_v, split_r = split(pe, po), split(re, ro)

    def group_test(name, labels):
        out = []
        for g in sorted(set(labels[nz].tolist())):
            m = labels == g
            mg, mc = m, ~m
            if (w[mg] > 0).sum() < 2 or (w[mc] > 0).sum() < 2: continue
            pg, pc = weighted_rate(w[mg], rate_r[mg]), weighted_rate(w[mc], rate_r[mc])
            sg, sc = lin_se(w[mg], rate_r[mg], pg), lin_se(w[mc], rate_r[mc], pc)
            z = (pg - pc) / math.sqrt(sg ** 2 + sc ** 2)
            out.append(dict(group=name, value=g, records=int((w[mg] > 0).sum()), examined=int(mg.sum()),
                            ratio=pg / p_occ, ratio_vs_rest=pg / pc, z=z))
        return out
    sl = np.array([r['slice'] for r in recs])
    cs = np.array([r['class_size'] for r in recs])
    csb = np.select([cs == 1, cs == 2, cs <= 4, cs <= 8], ['1', '2', '3-4', '5-8'], '>=9')
    medw = float(np.median(w[nz]))
    wb = np.where(w > medw, 'above', 'at_or_below')
    groups = group_test('slice', sl) + group_test('class_size', csb) + group_test('weight', wb)
    zcrit = z_quantile(1 - 0.005 / len(groups))
    for g in groups:
        g['significant'] = abs(g['z']) > zcrit
        g['material'] = g['significant'] and not (0.95 <= g['ratio'] <= 1.05)
    zr = (n_r[nz] - E_r[nz]) / np.sqrt(E_r[nz])
    zrcrit = z_quantile(1 - 0.005 / int(nz.sum()))

    # second moment
    om = (w[vec_rec] / k[vec_rec]); om = om / om.sum()
    m2 = float((om * pe * po).sum())
    m2b = np.empty(4000)
    for t in range(4000):
        rc = np.bincount(rng.integers(0, n_exam, n_exam), minlength=n_exam)
        ov = om * rc[vec_rec]
        if ov.sum() == 0: m2b[t] = np.nan; continue
        m2b[t] = (ov * pe * po).sum() / ov.sum()
    m2_hi = float(np.nanquantile(m2b, 0.995))

    out = dict(
        design='PREREGISTRATION.md', batches=B, histories_through19=int(c19.sum()), H=float(H.sum()),
        records_examined=n_exam, records_nonzero_weight=int(nz.sum()), vectors=C,
        weight=dict(nonzero_mean=float(w[nz].mean()), nonzero_min=float(w[nz].min()), nonzero_max=float(w[nz].max()),
                    pool=R['pool'], binomial_sd=math.sqrt(w[nz].mean() * (1 - w[nz].mean()) / R['pool']),
                    zero_fraction=float((~nz).mean())),
        p_occ=p_occ, log2_p_occ=lg(p_occ), p_unif=p_unif, log2_p_unif=lg(p_unif), unif_over_occ=p_unif / p_occ,
        se_batch=se_batch, se_records=se_rec, se=se, rel_se=se / p_occ,
        t99=[t_lo, t_hi], boot99=[b_lo, b_hi], three_sigma=[p_occ - 3 * se, p_occ + 3 * se],
        p_L=p_L, log2_p_L=lg(p_L), p_U=p_U, log2_p_U=lg(p_U),
        through19=dict(rate=r19, log2=lg(r19), rel_se=se19 / r19),
        stages20_31=dict(rate=p_occ / r19, log2=lg(p_occ / r19), conditionals={k_: [v, lg(v)] for k_, v in cond.items()}),
        heterogeneity=dict(
            vectors=dict(X2=X2v, df=C - 1, p=chi2_upper_p(X2v, C - 1), mean_count=mean_c),
            records=dict(X2=X2r, df=int(nz.sum()) - 1, p=chi2_upper_p(X2r, int(nz.sum()) - 1)),
            split_vectors=split_v, split_records=split_r,
            groups=groups, group_z_critical=zcrit,
            max_abs_record_z=float(np.abs(zr).max()), record_z_critical=zrcrit,
            records_beyond_critical=int((np.abs(zr) > zrcrit).sum())),
        second_moment=dict(m2=m2, m2_over_p2=m2 / p_occ ** 2, m2_upper99=m2_hi, m2_upper_over_p2=m2_hi / p_occ ** 2,
                           p_U2=math.sqrt(m2_hi), log2_p_U2=lg(math.sqrt(m2_hi))),
    )
    sd = np.load(slf)
    cnt = sd['counts']; bys = [int(b) for b in sd['bytes']]
    ch = sd['cls_hist']
    pop = {}
    for lab, lo, hi in (('1', 1, 1), ('2', 2, 2), ('3-4', 3, 4), ('5-8', 5, 8), ('>=9', 9, 64)):
        pop[lab] = float(sum(s * ch[:, s].sum() for s in range(lo, hi + 1)) / sum(s * ch[:, s].sum() for s in range(1, 65)))
    out['coverage'] = dict(slices=[f'0x{b:02x}' for b in bys], records_per_slice=[int(cnt[b]) for b in bys],
                           N=int(sd['N']), sub_sample=int(len(sd['sub'])),
                           class_size_share_population=pop,
                           class_size_share_examined={g: float((csb == g).mean()) for g in pop},
                           examined_per_slice={f'0x{b:02x}': int((sl == b).sum()) for b in bys})
    if cop:
        ex = {key: np.sum([o['extra'][key] for o in cop], axis=0).tolist() for key in ('t19', 'h19', 'tall', 'a19', 'aall')}
        ev = int(sum(o['extra']['events'] for o in cop))
        Hc = float(sum(o['H'] for o in cop)); r19c = sum(o['c19'] for o in cop) / Hc
        found = ex['aall'][0] + ex['aall'][1]
        U = poisson_upper(found)
        cp = dict(events=ev, r19=r19c,
                  given19=[dict(relation=rel, tested=ex['t19'][j], passed19=ex['h19'][j],
                                ratio_to_r19=ex['h19'][j] / ex['t19'][j] / r19c,
                                ratio_upper99=poisson_upper(ex['h19'][j]) / ex['t19'][j] / r19c)
                           for j, rel in enumerate(('same_W14', 'other_W14'))],
                  givenall=[dict(relation=rel, tested=ex['tall'][j], passed19=ex['a19'][j], passedall=ex['aall'][j],
                                 ratio19_to_r19=ex['a19'][j] / ex['tall'][j] / r19c)
                            for j, rel in enumerate(('same_W14', 'other_W14'))],
                  others_per_pass=found / ev, others_per_pass_upper99=U / ev,
                  log2_others_per_pass_upper99=lg(U / ev))
        NBc = np.stack([o['vec'][:C, 3] for o in cop]); Hc_b = np.array([o['H'] for o in cop], float)
        CRc = rec_matrix(NBc)
        p_rep = weighted_rate(w, CRc.sum(1) / Hc)
        pbc = np.array([weighted_rate(w, CRc[:, b] / Hc_b[b]) for b in range(len(cop))])
        se_rep = float(pbc.std(ddof=1) / math.sqrt(len(cop)))
        cp['replication'] = dict(p_occ=p_rep, log2=lg(p_rep), se_batch=se_rep,
                                 z_vs_primary=(p_rep - p_occ) / math.sqrt(se_rep ** 2 + se_batch ** 2))
        out['copass'] = cp
    out['e2e'] = json.load(open(e2ef)) if e2ef != '-' else None
    print(json.dumps(out, indent=1, default=lambda o: o.item() if hasattr(o, 'item') else str(o)))
```

### F.13 `e2e.py`

```python
"""End-to-end check of simulated full passes: each dumped pass (entry, W16..W19, vector) of copass.c is turned into a
chaining value CV1 and a second-block message pair for the vector's real TAB2 record and tuple, and the two 32-step
compressions from CV1 are computed with the reference SHA-256 of check_route.py. A pass must give equal outputs.

Construction (proof Section 9.1): W4..W6 from the tuple, W7, W8 from the record, W9..W11 from its P2 combination,
W12, W13 from the advice, W14, W15 from the P4 entry; W3, W2, W1, W0 from W19, W18, W17, W16 (triangular);
CV1[0..3] from the record's key and the inverse Step-2 map; CV1[4..7] = E[-1..-4] from W3, W2, W1, W0 (triangular).
The primed message is W_i xor FL(W, i). Every A/E word the record, the advice and the entry fix is also compared.
usage: e2e.py sample.records.json slices.npz p4.bin dump.0 [dump.1 ...]
"""
import json, sys, warnings
import numpy as np
warnings.filterwarnings('ignore')
ARGS = sys.argv[1:]
from step3ref import ref, fl, M
import pairexp as PX
from secondblock import ADVICE_A, ADVICE_E, ADVICE_W

S0, S1, s0, s1, IF, MAJ, K = ref['S0'], ref['S1'], ref['s0'], ref['s1'], ref['IF'], ref['MAJ'], ref['K']
recs = json.load(open(ARGS[0]))['records']
d = np.load(ARGS[1]); comb, pairs = d['comb'], d['pairs']
P4 = np.fromfile(ARGS[2], dtype='<u4').reshape(-1, 10)
by_vec = {v: (r, k) for r in recs for k, v in enumerate(r['vectors'])}

def build(rec, tup, e, w16_19):
    rn = PX.record(comb, pairs, np.array([rec['pair_index'], rec['W7'], rec['E3'], rec['key']], dtype=np.uint32))
    r = {k: int(v) for k, v in rn.items()}
    ci = int(pairs[rec['pair_index']][0])
    W = [0] * 16
    W[4], W[5], W[6] = tup
    W[7], W[8] = r['W7'], r['W8']
    W[9], W[10], W[11] = (int(x) for x in comb[ci][6:9])
    W[12], W[13] = ADVICE_W[12], ADVICE_W[13]
    x = [int(v) for v in P4[e]]
    W[14], W[15] = x[8], x[9]
    W16, W17, W18, W19 = w16_19
    W[3] = (W19 - s1(W17) - W[12] - s0(W[4])) & M
    W[2] = (W18 - s1(W16) - W[11] - s0(W[3])) & M
    W[1] = (W17 - s1(W[15]) - W[10] - s0(W[2])) & M
    W[0] = (W16 - s1(W[14]) - W[9] - s0(W[1])) & M
    u = np.uint32
    e0, e1, e2, am2, am3, am4 = (int(v) for v in PX.from_w(rn, rn['key'], u(W[4]), u(W[5]), u(W[6])))
    A = {-1: r['key'], -2: am2, -3: am3, -4: am4, 0: r['A0'], 1: r['A1'], 2: r['A2'], 3: r['A3']}
    E = {0: e0, 1: e1, 2: e2, 3: r['E3']}
    E[-1] = (E[3] - A[-1] - S1(E[2]) - IF(E[2], E[1], E[0]) - K[3] - W[3]) & M
    E[-2] = (E[2] - A[-2] - S1(E[1]) - IF(E[1], E[0], E[-1]) - K[2] - W[2]) & M
    E[-3] = (E[1] - A[-3] - S1(E[0]) - IF(E[0], E[-1], E[-2]) - K[1] - W[1]) & M
    E[-4] = (E[0] - A[-4] - S1(E[-1]) - IF(E[-1], E[-2], E[-3]) - K[0] - W[0]) & M
    cv1 = [A[-1], A[-2], A[-3], A[-4], E[-1], E[-2], E[-3], E[-4]]
    fixed = {('A', i): v for i, v in ADVICE_A.items()}
    fixed.update({('E', i): v for i, v in ADVICE_E.items()})
    fixed.update({('A', 0): r['A0'], ('A', 1): r['A1'], ('A', 2): r['A2'], ('A', 3): r['A3'], ('E', 3): r['E3'],
                  ('E', 4): r['E4'], ('E', 5): r['E5'], ('E', 6): r['E6'], ('E', 7): r['E7'],
                  ('E', 14): x[0], ('A', 14): x[1], ('E', 15): x[4], ('A', 15): x[5]})
    fixedp = {('E', 14): x[2], ('A', 14): x[3], ('E', 15): x[6], ('A', 15): x[7]}
    return cv1, W, fixed, fixedp

if __name__ == '__main__':
    n = ok = 0
    bad = []
    for path in ARGS[3:]:
        for line in open(path):
            f = line.split()
            if len(f) != 6: continue
            e, w16_19, c = int(f[0]), [int(v, 16) for v in f[1:5]], int(f[5])
            rec, k = by_vec[c]
            cv1, W, fixed, fixedp = build(rec, rec['tuples'][k], e, w16_19)
            Wp = [w ^ fl('W', i) for i, w in enumerate(W)]
            A, E, Wx = ref['trace'](cv1, W, 32)
            Ap, Ep, Wpx = ref['trace'](cv1, Wp, 32)
            checks = [Wx[16:20] == w16_19]
            checks += [(A if col == 'A' else E)[i] == v for (col, i), v in fixed.items()]
            checks += [(Ap if col == 'A' else Ep)[i] == v for (col, i), v in fixedp.items()]
            checks += [Ap[i] ^ A[i] == fl('A', i) and Ep[i] ^ E[i] == fl('E', i) for i in range(32)]
            checks += [Wpx[i] ^ Wx[i] == fl('W', i) for i in range(32)]
            coll = ref['compress'](cv1, W, 32) == ref['compress'](cv1, Wp, 32)
            n += 1
            if all(checks) and coll:
                ok += 1
            else:
                bad.append(dict(line=line.strip(), collision=coll, failed_checks=[j for j, x in enumerate(checks) if not x]))
    print(json.dumps(dict(events=n, collisions_and_all_checks=ok, failures=bad[:10])))
```

### F.14 `conddump.c`

```c
/* Survivor samples for the condition count (CONDITIONS.md). Histories are drawn with condexp.c's scheme; a history
 * (and, from stage 20, a tuple vector) that survives stage s is written with probability 2^-K[s] as
 * "s entry W16 W17 W18 W19 c" (s = 15 for every sampled entry before stage 16, 31 for a full pass). Words not yet
 * drawn at stage s are drawn fresh and uniform; below stage 20 c is a uniform vector index.
 * usage: conddump p4.bin cvec.txt seed n16 M17 M18 M19 k15 k16 k17 k18 k19 k20 k21 k22 k31
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
static FILE *out;
static int kk[32];
static inline int pick(int st) { return kk[st] == 0 || (next() >> (64 - kk[st])) == 0; }
static inline void dump(int st, int e, uint32_t a, uint32_t b, uint32_t c, uint32_t d, int v) {
    fprintf(out, "%d %d %08x %08x %08x %08x %d\n", st, e, a, b, c, d, v);
}
int main(int argc, char **argv) {
    if (argc < 17) { fprintf(stderr, "usage\n"); return 1; }
    FILE *f = fopen(argv[1], "rb");
    fseek(f, 0, SEEK_END); long nb = ftell(f); fseek(f, 0, SEEK_SET);
    int n4 = (int)(nb / 40);
    uint32_t *P = malloc(nb);
    if (fread(P, 1, nb, f) != (size_t)nb) return 2;
    fclose(f);
    static uint32_t C[MAXC][7]; int nc = 0;
    f = fopen(argv[2], "r");
    while (nc < MAXC && fscanf(f, "%x %x %x %x %x %x %x", &C[nc][0], &C[nc][1], &C[nc][2], &C[nc][3], &C[nc][4],
                               &C[nc][5], &C[nc][6]) == 7) nc++;
    fclose(f);
    uint64_t seed = strtoull(argv[3], 0, 10), n16 = strtoull(argv[4], 0, 10);
    int M17 = atoi(argv[5]), M18 = atoi(argv[6]), M19 = atoi(argv[7]);
    int st[10] = {15, 16, 17, 18, 19, 20, 21, 22, 31};
    for (int j = 0; j < 9; j++) kk[st[j]] = atoi(argv[8 + j]);
    out = stdout;
    for (int k = 0; k < 4; k++) s[k] = splitmix(&seed);
    side u0, p0;
    u0.A[12] = A12; u0.A[13] = A13; u0.E[12] = E12; u0.E[13] = E13;
    p0.A[12] = AP12; p0.A[13] = AP13; p0.E[12] = EP12; p0.E[13] = EP13;
    for (uint64_t t = 0; t < n16; t++) {
        uint64_t r = next();
        int e = (int)((r >> 32) % (uint64_t)n4);
        const uint32_t *x = P + 10 * e;
        side u = u0, p = p0;
        u.E[14] = x[0]; u.A[14] = x[1]; p.E[14] = x[2]; p.A[14] = x[3];
        u.E[15] = x[4]; u.A[15] = x[5]; p.E[15] = x[6]; p.A[15] = x[7];
        uint32_t W14 = x[8], W15 = x[9];
        uint32_t W16 = (uint32_t)r;
        if (pick(15)) dump(15, e, W16, (uint32_t)next(), (uint32_t)next(), (uint32_t)next(), (int)(next() % nc));
        step(&u, 16, W16); step(&p, 16, W16);
        if (!conf(&u, &p, 16)) continue;
        if (pick(16)) dump(16, e, W16, (uint32_t)next(), (uint32_t)next(), (uint32_t)next(), (int)(next() % nc));
        {
            side u17 = u, p17 = p;
            step(&u17, 17, 0); step(&p17, 17, 0);
            if (!conf(&u17, &p17, 17)) continue;
        }
        for (int j17 = 0; j17 < M17; j17++) {
            uint32_t W17 = (uint32_t)next();
            side u17 = u, p17 = p;
            step(&u17, 17, W17); step(&p17, 17, W17);
            if (!conf(&u17, &p17, 17)) continue;
            if (pick(17)) dump(17, e, W16, W17, (uint32_t)next(), (uint32_t)next(), (int)(next() % nc));
            for (int j18 = 0; j18 < M18; j18++) {
                uint32_t W18 = (uint32_t)next();
                side u18 = u17, p18 = p17;
                step(&u18, 18, W18); step(&p18, 18, W18);
                if (!conf(&u18, &p18, 18)) continue;
                if (pick(18)) dump(18, e, W16, W17, W18, (uint32_t)next(), (int)(next() % nc));
                for (int j19 = 0; j19 < M19; j19++) {
                    uint32_t W19 = (uint32_t)next();
                    side u19 = u18, p19 = p18;
                    step(&u19, 19, W19); step(&p19, 19, W19);
                    if (!conf(&u19, &p19, 19)) continue;
                    if (pick(19)) dump(19, e, W16, W17, W18, W19, (int)(next() % nc));
                    for (int c = 0; c < nc; c++) {
                        side a = u19, b = p19;
                        uint32_t W20 = SS1(W18) + C[c][0], W20p = SS1(W18) + C[c][1];
                        if ((W20 ^ W20p) != FLW20 || (W20 & SGM20) != SGV20) continue;
                        step(&a, 20, W20); step(&b, 20, W20p);
                        if (!conf(&a, &b, 20)) continue;
                        if (pick(20)) dump(20, e, W16, W17, W18, W19, c);
                        uint32_t W21 = SS1(W19) + W14 + C[c][2];
                        step(&a, 21, W21); step(&b, 21, W21);
                        if (!conf(&a, &b, 21)) continue;
                        if (pick(21)) dump(21, e, W16, W17, W18, W19, c);
                        uint32_t W22 = SS1(W20) + W15 + C[c][3], W22p = SS1(W20p) + W15 + C[c][4];
                        if ((W22 ^ W22p) != FLW22 || (W22 & SGM22) != SGV22) continue;
                        step(&a, 22, W22); step(&b, 22, W22p);
                        if (!conf(&a, &b, 22)) continue;
                        if (pick(22)) dump(22, e, W16, W17, W18, W19, c);
                        uint32_t d24 = SS1(W22p) - SS1(W22) + C[c][5], d29 = (W22p - W22) + C[c][6];
                        if (d24 == 0 && d29 == 0 && pick(31)) dump(31, e, W16, W17, W18, W19, c);
                    }
                }
            }
        }
    }
    return 0;
}
```

### F.15 `conds.py`

```python
"""Which printed Step-3 conditions does each stage enforce? Reads conddump.c output and, for every condition of Fig. 6
rows 16..22 (single-bit symbols, the two-bit relations as printed, A15[29] = A16[29] and the unprinted
E16[29] = E17[29]), the fraction of stage-s survivors that satisfy it, for s = 15 (all sampled entries) .. 31.
usage: conds.py cvec.txt p4.bin dump...   (JSON on stdout)"""
import json, sys
import numpy as np
ARGS = sys.argv[1:]
from step3ref import ref, fl, R, M, s1
from secondblock import ADVICE_A, ADVICE_E

S0, S1, IF, MAJ, K = ref['S0'], ref['S1'], ref['IF'], ref['MAJ'], ref['K']
C = [[int(x, 16) for x in l.split()] for l in open(ARGS[0]) if l.strip()]
P4 = np.fromfile(ARGS[1], dtype='<u4').reshape(-1, 10)

def bit(x, j): return (x >> j) & 1

CONDS = []                                   # (name, group, function of (A, E, W) unprimed dicts)
for col in 'AEW':
    for i in range(16, 23):
        for k, ch in enumerate(R(col, i)):
            if ch in '01nu':
                j, v = 31 - k, 1 if ch in '1u' else 0
                kind = 'sign' if ch in 'nu' else 'value'
                CONDS.append((f'{col}{i}[{j}]={v} ({ch})', f'{col}{i} {kind}',
                              lambda A, E, W, col=col, i=i, j=j, v=v: bit({'A': A, 'E': E, 'W': W}[col][i], j) == v))
def rel(name, group, x, a, y, b, eq):
    CONDS.append((name, group, lambda A, E, W: (bit({'A': A, 'E': E, 'W': W}[x[0]][x[1]], a) ==
                                                 bit({'A': A, 'E': E, 'W': W}[y[0]][y[1]], b)) == eq))
for a, b in ((28, 1), (20, 7), (20, 2), (6, 11)):
    rel(f'E16[{a}]=E16[{b}]', 'E16 two-bit', ('E', 16), a, ('E', 16), b, True)
for a, b in ((30, 12), (28, 10), (10, 29)):
    rel(f'E16[{a}]!=E16[{b}]', 'E16 two-bit', ('E', 16), a, ('E', 16), b, False)
rel('E18[24]!=E18[11]', 'E18 two-bit', ('E', 18), 24, ('E', 18), 11, False)
rel('E18[2]=E18[16]', 'E18 two-bit', ('E', 18), 2, ('E', 18), 16, True)
for a, b in ((31, 1), (30, 0), (25, 16), (21, 14)):
    rel(f'W20[{a}]!=W20[{b}]', 'W20 two-bit', ('W', 20), a, ('W', 20), b, False)
for a, b in ((4, 6), (31, 22)):
    rel(f'W20[{a}]=W20[{b}] (printed; dropped in v8 as a misprint)', 'W20 two-bit dropped', ('W', 20), a, ('W', 20), b, True)
for a, b in ((4, 6), (31, 22)):
    rel(f'W22[{a}]=W22[{b}]', 'W22 two-bit', ('W', 22), a, ('W', 22), b, True)
rel('W22[27]!=W22[20]', 'W22 two-bit', ('W', 22), 27, ('W', 22), 20, False)
rel('A15[29]=A16[29] (printed as A6[29])', 'A16 two-bit', ('A', 15), 29, ('A', 16), 29, True)
rel('E16[29]=E17[29] (unprinted, #26)', 'unprinted', ('E', 16), 29, ('E', 17), 29, True)
REF = [('A16 xor-conformant (R1)', lambda A, E, W, Ap, Ep: A[16] ^ Ap[16] == fl('A', 16))]

A0 = {i: ADVICE_A[i] for i in (12, 13)}; E0 = {i: ADVICE_E[i] for i in (12, 13)}
def history(e, w, c):
    x = [int(v) for v in P4[e]]
    cv = C[c]
    sides = []
    for prim in (0, 1):
        A = {i: v ^ (fl('A', i) if prim else 0) for i, v in A0.items()}
        E = {i: v ^ (fl('E', i) if prim else 0) for i, v in E0.items()}
        E[14], A[14], E[15], A[15] = (x[2], x[3], x[6], x[7]) if prim else (x[0], x[1], x[4], x[5])
        W = {14: x[8], 15: x[9], 16: w[0], 17: w[1], 18: w[2], 19: w[3]}
        W[20] = (s1(W[18]) + cv[1 if prim else 0]) & M
        W[21] = (s1(W[19]) + W[14] + cv[2]) & M
        W[22] = (s1(W[20]) + W[15] + cv[4 if prim else 3]) & M
        for i in range(16, 23):
            E[i] = (A[i - 4] + E[i - 4] + S1(E[i - 1]) + IF(E[i - 1], E[i - 2], E[i - 3]) + K[i] + W[i]) & M
            A[i] = (E[i] - A[i - 4] + S0(A[i - 1]) + MAJ(A[i - 1], A[i - 2], A[i - 3])) & M
        sides.append((A, E, W))
    return sides

if __name__ == '__main__':
    STAGES = [15, 16, 17, 18, 19, 20, 21, 22, 31]
    n = {s: 0 for s in STAGES}
    hold = {s: np.zeros(len(CONDS) + len(REF), dtype=np.int64) for s in STAGES}
    for path in ARGS[2:]:
        for line in open(path):
            f = line.split()
            st, e, w, c = int(f[0]), int(f[1]), [int(v, 16) for v in f[2:6]], int(f[6])
            (A, E, W), (Ap, Ep, Wp) = history(e, w, c)
            n[st] += 1
            hold[st][:len(CONDS)] += [bool(fn(A, E, W)) for _, _, fn in CONDS]
            hold[st][len(CONDS):] += [bool(fn(A, E, W, Ap, Ep)) for _, fn in REF]
    names = [(nm, g) for nm, g, _ in CONDS] + [(nm, 'reference') for nm, _ in REF]
    table = []
    for j, (nm, g) in enumerate(names):
        fr = {s: hold[s][j] / n[s] for s in STAGES if n[s]}
        enforced = next((s for s in STAGES if n[s] and hold[s][j] == n[s]), None)
        table.append(dict(condition=nm, group=g, enforced_from_stage=enforced,
                          fraction={str(s): round(v, 4) for s, v in fr.items()}))
    print(json.dumps(dict(samples={str(s): v for s, v in n.items()}, conditions=table), indent=1))
```

### F.16 `CONDITIONS.md`

```
# Step-3 conditions against the measured stage rates

The measured per-candidate rate is 2^-44.00. The count used in v8 and in Meganpark's lineage is 46: "45 printed by S
for steps 16-22 and W20/W22, plus the unprinted E16[29] = E17[29]". This note shows where the difference of 2 comes
from.

**Finding.** None of the 46 counted conditions holds automatically. Two of them are not conditions of the route:
the printed relation **W20[4,31] = W20[6,22]**, that is **W20[4] = W20[6]** and **W20[31] = W20[22]**. The published
pair violates both (W20 = 0xe238ad6c: bits 4, 6 = 0, 1 and bits 31, 22 = 1, 0), which is why v8 Section 2 drops them
as a misprint. Among 2,132 sampled full passes (stage 31) they hold at rates 0.5005 and 0.5141, so neither the
printed equality nor its negation is required. The other 44 conditions each hold in every survivor from one stage on, and in
about half of the survivors of the stage before. The stage costs are the counts of those conditions, to 4 decimals.
The A16 test is always passed, as Meganpark's R1 states. It holds on all 11,991 sampled entries before stage 16, but
row A16 is all `=`, so it was never one of the 46.

## Method

1. `conddump.c` samples histories with condexp.c's scheme (seed 8100, n16 = 4 * 10^8, the 1,400 vectors of this
   campaign) and writes random survivors of each stage s. s = 15 means every sampled entry; s = 31 means a full pass.
2. `conds.py` recomputes both branches from the advice, the P4 entry, W16..W19 and the vector. For each condition it
   reports the fraction of stage-s survivors that satisfy it. The conditions are:
   - every `0/1/n/u` symbol of rows A, E, W 16..22, read on the unprimed word;
   - the printed two-bit relations on E16, E18, W20 and W22;
   - A15[29] = A16[29] (printed "A6[29]");
   - E16[29] = E17[29].
3. A condition is *enforced from* stage s when every sampled stage-s survivor satisfies it. Before that stage, every
   fraction is 0.5 within sampling error: the largest of 197 deviations is z = 2.78. Samples per stage range from
   11,991 to 17,146; stage 22 has 4,125 and stage 31 has 2,132.

## Per stage

The measured exponents come from all 30 primary batches. Through stage 19 they are per history; from stage 20 on they
are per (history, vector).

| stage | measured | newly enforced conditions | count |
|---|---:|---|---:|
| 16 | 2^-3.0000 | E16[25]=1 (u), E16[23]=0 (n), E16[15]=0 (n) | 3 |
| 17 | 2^-11.9998 | E16[18]=1, E16[9]=0, E16[5]=0, E16[4]=1; E16[28]=E16[1], E16[20]=E16[7], E16[20]=E16[2], E16[6]=E16[11], E16[30]!=E16[12], E16[28]!=E16[10], E16[10]!=E16[29]; A15[29]=A16[29] | 12 |
| 18 | 2^-6.0001 | E17[25]=0, E17[23]=0, E17[18]=1, E17[15]=0, E17[4]=1; E18[29]=1 (u) | 6 |
| 19 | 2^-7.0003 | E18[25]=1, E18[23]=0, E18[15]=1, E18[10]=1; E18[24]!=E18[11], E18[2]=E18[16]; E16[29]=E17[29] (unprinted) | 7 |
| 20 | 2^-4.0003 | E19[29]=0; W20[24]=0 (n), W20[23]=0 (n), W20[15]=1 (u) | 4 |
| 21 | 2^-1.0000 | E20[29]=1 | 1 |
| 22 | 2^-7.9993 | W20[26]=0, W20[17]=0, W20[13]=1; W20[31]!=W20[1], W20[30]!=W20[0], W20[25]!=W20[16], W20[21]!=W20[14]; W22[29]=0 (n) | 8 |
| 23..31 | 2^-3.0005 | W22[4]=W22[6], W22[31]=W22[22], W22[27]!=W22[20] | 3 |
| never | - | W20[4]=W20[6], W20[31]=W20[22] (printed; full-pass rates 0.5005, 0.5141) | 0 |
| total | 2^-44.00 | | 44 |

Breakdown of the 46-count against these stages:
- 26 single-bit symbols, from E16 (7), E17 (5), E18 (5), E19 (1), E20 (1), W20 (6) and W22 (1);
- 19 printed relations, from E16 (7), E18 (2), W20 (4 + 2), W22 (3) and A15/A16 (1);
- 1 unprinted relation.

The 13 "late W20/W22 carry conditions" of v8 are therefore 9 + 4. Only 7 + 4 = 11 of them exist, and the measured
stages 22 and 23..31 cost 8 + 3 = 11 bits. Every enforced condition costs exactly one bit, so p = 2^-44 is the
characteristic's own condition count once the misprint is removed. It is not an empirical accident.

Stage boundaries agree with Meganpark's mapping, except that their "step 18 conforms iff E18[29] = 1" is the u-sign of
E18 together with the five E17 conditions. The E17 conditions are enforced at stage 18, where IF(E17, E16, E15)
absorbs E16's differences.

Files: `conddump.c`, `conds.py`, `cond/dump.8100` (raw samples), `cond/conds.json` (all fractions),
`cond/stage_rates.json` (measured exponents).
```

## Appendix G. The ledger, cap and success arithmetic (participant tool)

Every number of Sections 7 and 8 (E[X], E[X^2], M, the Bernstein exponent, the (w, T) search, success, A + B, C, D
and the total) is computed at 80-digit precision by these two files. The claimed values come from
`final_v10.solve(floor="0.3950005", success_model="measured", batch_ops=2273, per_trial_fixed=32, c_units_override=23035438979)  with MEAS = pL_log2 -44.0055, pU_log2 -43.9954, copass_U 3.61053e-5`, followed by `arith.evaluate` on the result.
The same functions reproduce 621d0fb0, d8d39011, f807117b and 6e5214dd exactly (`arith.BASE_621D0FB0`,
`arith.D8D39011`, `arith.F807117B`, `arith.E6E5214DD`). C enters as `c_units_override` (Section 8 C computes it);
the tool's own `O_C` and `C_exact` fields then refer to the default ledger and are not used. The defaults of
`final_v10.MEAS` belong to our measured-rate filing; the call above passes the success model explicitly.

sha256 f318edcf7b56a2d1d8c5a1ad92e6fdbddc5a66bad87b99a920fb8bab48faba01  arith.py
sha256 7e635a6bb0090acb8dd32f3f60bbdd72d43301713c7f6092c517d353528e9bde  final_v10.py

### G.1 `arith.py`

```python
"""Parameterized ledger, cap and success arithmetic for the SHA-256/32 package line.

Every derived number (T, E[X], E[X^2], support M, Bernstein, A+B, C, total, success)
recomputes from the parameters below. Run with no arguments for v9 and for the
621d0fb0 base reproduction; import `evaluate` to vary T, p, cap and charges.
"""
from __future__ import annotations

import argparse
import json
from dataclasses import dataclass, field, asdict
from decimal import Decimal as D, ROUND_CEILING, ROUND_FLOOR, getcontext

getcontext().prec = 80
LN2 = D(2).ln()


def p2(x) -> D:
    return (D(x) * LN2).exp()


def lg(x) -> D:
    return D(x).ln() / LN2


def ceil_int(x: D) -> int:
    return int(D(x).to_integral_value(rounding=ROUND_CEILING))


@dataclass
class Params:
    name: str = "v9"
    # trial count and probability premises
    t_log2: str = "44.803"            # T = ceil(2^t_log2) unless T is given
    T: int = 0                        # explicit trial count (overrides t_log2)
    q_lcb_log2: str = "-17.3584"      # declared q lower bound
    q_ucb_log2: str = "-17.3166"      # q upper bound used in work moments
    pair_factor_log2: int = -5        # E[C(V,2)] <= q 2^pair_factor_log2
    p_log2: str = "-46"               # per-candidate Step-3 conformance rate (condition-count model)
    success_model: str = "condition-count"   # or "measured" (v10)
    pL_log2: str = "-44.2"            # measured: 99% lower bound on the occurrence-weighted rate
    pU_log2: str = "-43.9"            # measured: 99% upper bound
    copass_U: str = "0.00390625"      # measured: 99% upper bound on E[other passing entries | an entry passes]
    groups: int = 12
    group_size: int = 1 << 14
    w20_group_conditions: int = 12    # conditions common to one W14 group
    r_loss_log2: int = -20            # displayed rounding: r >= E[Y](1 - 2^r_loss_log2)
    # Step-2/3 rates used in work
    scan_mean: str = "0.32522"        # exact 32-bit buckets: N/2^32 < 0.32522 (621d0fb0: 10.41)
    lazy_cv: int = 56                 # lever 3: per nonempty-bucket trial charge for deferred CV1[1..7]
    match_rate: str = "0.32522"
    step2_mean_per_match: int = 192
    step2_max_per_match: int = 1304
    f16: str = "0.126"
    f17_log2: str = "-14.9"
    max_occupancy: int = 936
    sumsq_parts: str = "5.758e9"
    # Step-3 charges
    tuple_setup: int = 300
    stage16_mode: str = "swar1617"    # "swar1617" (v9 lever 2), "swar" (stage 16 only) or "scalar" (base)
    s1617_group: int = 48
    s16_word: int = 40
    s17_word: int = 160
    s17_pass: int = 96
    # f807117b seven-lane sweep (mode "f807"): per pack stage 16, stage 17 (on a stage-16 pass), extraction
    pk16: int = 11
    pk17: int = 57
    pkx: int = 25
    survivor: int = 2 + 2352
    stage16_scalar: int = 48
    stage16_group: int = 32
    stage16_word: int = 64
    lanes: int = 7
    extract: int = 32                 # per stage-16 pass (SWAR only)
    stage17: int = 256
    stage18_31: int = 2048
    # online fixed work
    batch_ops: int = 2732
    per_trial_fixed: int = 32
    final_units: int = 14
    # cap and moments
    cap: str = "122"
    ex_bound: str = "118.9"
    ex2_bound: str = "4.152e12"
    # preprocessing
    o_c: int = 671113630622720 + 1024 * ((1 << 32) - (1 << 27)) + 1024 * (12 * 2341 * 10)
    d_units: int = 1 << 35
    c_units_override: int = 0         # use a base's separately rounded C when given
    cost_c: int = 2224


def evaluate(pp: Params) -> dict:
    out: dict = {"params": asdict(pp)}
    C = pp.cost_c
    T = pp.T or ceil_int(p2(pp.t_log2))
    B7 = -(-T // pp.lanes)
    P4 = pp.groups * pp.group_size
    q_ucb = p2(pp.q_ucb_log2)
    f16, f17 = D(pp.f16), p2(pp.f17_log2)
    out.update(T=T, B7=B7, P4=P4)

    # ---- Step-3 per-tuple charges
    if pp.stage16_mode == "f807":
        words = -(-pp.group_size // pp.lanes)
        packs = pp.groups * words
        percand = (D(pp.pk16 * packs) / P4 + 7 * f16 * pp.pk17 * packs / P4 + 7 * f17 * pp.pkx * packs / P4
                   + f17 * pp.survivor)
        out["per_candidate"] = str(percand)
        step3_mean = pp.tuple_setup + P4 * percand
        s3_max = pp.tuple_setup + packs * (pp.pk16 + pp.pk17 + pp.pkx) + P4 * pp.survivor
        s16_tuple = None
    elif pp.stage16_mode == "swar1617":
        words = -(-pp.group_size // pp.lanes)
        fixed = pp.groups * (pp.s1617_group + words * pp.s16_word)
        out["stage16_words_per_group"] = words
        out["stage1617_fixed_per_tuple"] = fixed
        step3_mean = (pp.tuple_setup + fixed + P4 * (pp.s17_word * f16 + (pp.s17_pass + pp.stage18_31) * f17))
        s3_max = (pp.tuple_setup + fixed + pp.groups * words * pp.s17_word
                  + P4 * (pp.s17_pass + pp.stage18_31))
        s16_tuple = None
    elif pp.stage16_mode == "swar":
        words = -(-pp.group_size // pp.lanes)
        s16_tuple = pp.groups * (pp.stage16_group + words * pp.stage16_word)
        pass_charge = pp.extract + pp.stage17
        out["stage16_words_per_group"] = words
    else:
        s16_tuple = P4 * pp.stage16_scalar
        pass_charge = pp.stage17
    if s16_tuple is not None:
        out["stage16_per_tuple"] = s16_tuple
        out["stage16_per_candidate"] = str(D(s16_tuple) / P4)
        step3_mean = pp.tuple_setup + s16_tuple + P4 * (pass_charge * f16 + pp.stage18_31 * f17)
        s3_max = pp.tuple_setup + s16_tuple + P4 * (pass_charge + pp.stage18_31)
    out["step3_mean_per_tuple"] = str(step3_mean)
    scan, match = D(pp.scan_mean), D(pp.match_rate)
    ex_terms = {"scan": 5 * scan, "lazy_cv": pp.lazy_cv * scan,
                "step2": match * pp.step2_mean_per_match, "step3": q_ucb * step3_mean}
    ex = sum(ex_terms.values())
    out["EX_terms"] = {k: str(v) for k, v in ex_terms.items()}
    out["EX"] = str(ex)
    assert ex < D(pp.ex_bound), (ex, pp.ex_bound)

    M = 5 * pp.max_occupancy + pp.lazy_cv + pp.max_occupancy * (pp.step2_max_per_match + s3_max)
    ex2_terms = {
        "scan2": (5 + pp.lazy_cv) ** 2 * pp.max_occupancy * scan,
        "step2_2": D(pp.step2_max_per_match) ** 2 * 4 * D(pp.sumsq_parts) / D(2) ** 32,
        "step3_2": D(s3_max) ** 2 * q_ucb * (1 + p2(pp.pair_factor_log2 + 1)),
    }
    ex2 = 3 * sum(ex2_terms.values())
    assert ex2 < D(pp.ex2_bound), (ex2, pp.ex2_bound)
    out.update(S3_max=s3_max, M=M, EX2=f"{ex2:.10e}",
               EX2_terms={k: f"{v:.10e}" for k, v in ex2_terms.items()},
               EX2_terms_exact={k: str(v) for k, v in ex2_terms.items()})

    excess = D(pp.cap) - D(pp.ex_bound)
    V = D(pp.ex2_bound)
    expo = (excess * T) ** 2 / (2 * (T * V + M * excess * T / 3))
    cap_stop = (-expo).exp()
    out.update(cap_excess=str(excess), bernstein_exponent=str(expo), cap_stop=f"{cap_stop:.6e}")

    # ---- success
    q_lcb = p2(pp.q_lcb_log2)
    if pp.success_model == "measured":
        ey_l, ey_u = P4 * p2(pp.pL_log2), P4 * p2(pp.pU_log2)
        # E[C(Y,2)] = E[Y] c/2 with c the size-biased co-pass mean <= U, so r >= E[Y](1 - U/2) >= 196,608 p_L (1 - U/2)
        pair = ey_l * D(pp.copass_U) / 2
        r = ey_l * (1 - D(pp.copass_U) / 2)
        ey = ey_l
        out.update(EY_L=f"{ey_l:.12e}", EY_U=f"{ey_u:.12e}", pair_term_rel=f"{pair:.6e}")  # E_L * U / 2, used only through r
    else:
        p = p2(pp.p_log2)
        ey = P4 * p
        g = pp.group_size
        pair = (pp.groups * D(g * (g - 1) // 2) * p2(-pp.w20_group_conditions)
                * (p2(pp.w20_group_conditions) * p) ** 2 + D(P4 * (P4 - 1) // 2) * p ** 2)
        assert pair <= ey * p2(pp.r_loss_log2), (pair, ey)
        r = ey * (1 - p2(pp.r_loss_log2))
    s = q_lcb * (1 - p2(pp.pair_factor_log2)) * r
    sT = s * T
    success = 1 - (-sT).exp() - cap_stop
    out.update(r=f"{r:.12e}", r_rel_loss_log2=str(lg(pair / ey)) if pair > 0 else None,
               s_log2=str(lg(s)), sT=str(sT), success=str(success))

    # ---- totals
    ab = (D(pp.batch_ops * B7 + pp.per_trial_fixed * T) + D(pp.cap) * T) / C + pp.final_units
    ab_int = ceil_int(ab)
    c_units = pp.c_units_override or ceil_int(D(pp.o_c) / C)
    total = ab_int + c_units + pp.d_units
    out.update(AB=str(ab), AB_ceiling=ab_int, AB_log2=str(lg(ab)), O_C=pp.o_c, C_exact=str(D(pp.o_c) / C),
               C_units=c_units, C_log2=str(lg(c_units)), D=pp.d_units, total=total,
               total_log2=str(lg(total)), preprocessing=c_units + pp.d_units,
               preprocessing_log2=str(lg(c_units + pp.d_units)))
    claim = (lg(total) * 1000).to_integral_value(rounding=ROUND_CEILING) / 1000
    out["claim_time_log2_3dp"] = str(claim)
    out["claim_check"] = D(total) ** 1000 <= D(2) ** int(claim * 1000)
    return out


BASE_621D0FB0 = Params(
    name="base-621d0fb0", scan_mean="10.41", stage16_mode="scalar", cap="214", lazy_cv=0,
    ex_bound="211.3", ex2_bound="4.18e12", o_c=671113630622720, batch_ops=3232, per_trial_fixed=64,
)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--set", nargs="*", default=[], help="field=value overrides for the v9 params")
    ap.add_argument("--base", action="store_true", help="also print the 621d0fb0 reproduction")
    args = ap.parse_args()
    pp = Params()
    for item in args.set:
        key, value = item.split("=", 1)
        cur = getattr(pp, key)
        setattr(pp, key, type(cur)(value) if not isinstance(cur, str) else value)
    runs = ([BASE_621D0FB0] if args.base else []) + [pp]
    for run in runs:
        res = evaluate(run)
        res.pop("params")
        print(run.name, json.dumps(res, indent=1, default=str))


if __name__ == "__main__":
    main()


D8D39011 = Params(
    name="base-d8d39011", T=30702387450972, scan_mean="0.325212", stage16_mode="scalar", cap="162.5", lazy_cv=0,
    ex_bound="160.82", ex2_bound="4.18e12", batch_ops=2928, per_trial_fixed=32,
    o_c=671113630622720 + 1024 * ((1 << 32) - (1 << 27)),
)


def success_at(pp: Params, T: int) -> D:
    old = pp.T
    pp.T = T
    try:
        return D(evaluate(pp)["success"])
    finally:
        pp.T = old


def optimise(pp: Params, floor: str, caps) -> list:
    """For each cap w, the smallest T with success >= floor, and the resulting total."""
    rows = []
    for w in caps:
        pp.cap = str(w)
        if D(pp.cap) <= D(pp.ex_bound):
            continue
        lo, hi = 1 << 40, 1 << 47
        if success_at(pp, lo) >= D(floor):
            raise ValueError("T search range too high")
        if success_at(pp, hi) < D(floor):
            continue
        while hi - lo > 1:
            mid = (lo + hi) // 2
            if success_at(pp, mid) >= D(floor):
                hi = mid
            else:
                lo = mid
        pp.T = hi
        res = evaluate(pp)
        rows.append((res["total"], str(w), hi, res["success"], res["cap_stop"], res["total_log2"]))
        pp.T = 0
    rows.sort()
    return rows


F807117B = Params(
    name="base-f807117b", T=30702858922613, scan_mean="0.325212", stage16_mode="f807", cap="76.4", lazy_cv=0,
    tuple_setup=600, ex_bound="74.711", ex2_bound="4.2301e12", batch_ops=2928, per_trial_fixed=32,
    o_c=671113630622720 + 1024 * ((1 << 32) - (1 << 27)) + 196608 * 128 + 12 * 1024, c_units_override=303675478130,
)


E6E5214DD = Params(
    name="base-6e5214dd", T=30702858922613, scan_mean="0.325212", stage16_mode="f807", cap="76.4", lazy_cv=0,
    tuple_setup=600, ex_bound="74.711", ex2_bound="4.2301e12", batch_ops=2805, per_trial_fixed=32,
    o_c=671113630622720 + 1024 * ((1 << 32) - (1 << 27)) + 196608 * 128 + 12 * 1024, c_units_override=303675478130,
)
```

### G.2 `final_v10.py`

```python
"""v10 = 6e5214dd + lazy CV1[1..7] extraction + measured Step-3 rate. Recomputes every bound from MEAS.

usage: final_v10.py [pL_log2=..] [pU_log2=..] [copass_U=..]
"""
import sys
sys.path.insert(0, ".")
from decimal import Decimal as D, ROUND_CEILING
import math
from arith import Params, evaluate, optimise, lg

FLOOR = "0.3950005"
MEAS = dict(success_model="measured", pL_log2="-44.2", pU_log2="-43.9", copass_U="0.00390625")
BASE = dict(stage16_mode="f807", tuple_setup=600, lazy_cv=56, batch_ops=2609, per_trial_fixed=32,
            scan_mean="0.32522", c_units_override=303675478130,
            o_c=671113630622720 + 1024 * ((1 << 32) - (1 << 27)) + 196608 * 128 + 12 * 1024)


def v10(**kw) -> Params:
    pp = Params(name="v10", **BASE, **MEAS)
    fixed = {k: v for k, v in kw.items() if k not in ("cap", "T")}
    for k, v in fixed.items():
        setattr(pp, k, v)
    pp.T, pp.cap, pp.ex_bound, pp.ex2_bound = 30702858922613, "500", "500", "1e13"
    raw = evaluate(pp)
    pp.ex_bound = str(D(raw["EX"]).quantize(D("0.001"), rounding=ROUND_CEILING))
    mant = (D(raw["EX2"]) / D("1e12")).quantize(D("0.0001"), rounding=ROUND_CEILING)
    pp.ex2_bound = f"{mant}e12"
    pp.T = 0
    for k, v in kw.items():
        setattr(pp, k, v)
    return pp


def solve(floor=FLOOR, **kw):
    pp = v10(**kw)
    lo = D(pp.ex_bound).quantize(D("0.1"), rounding=ROUND_CEILING)
    rows = optimise(pp, floor, [lo + D(i) / 10 for i in range(5, 120)])
    c0 = D(rows[0][1])
    rows = optimise(v10(**kw), floor, [c0 + D(i) / 100 for i in range(-10, 11)])
    cap, T = rows[0][1], rows[0][2]
    return v10(cap=str(cap), T=T, **kw)


def main() -> None:
    for a in sys.argv[1:]:
        k, v = a.split("=", 1)
        MEAS[k] = v
    pp = solve()
    r = evaluate(pp)
    for k in ("T", "B7", "per_candidate", "EX", "EX_terms", "EX2", "EX2_terms", "S3_max", "M", "cap_excess",
              "bernstein_exponent", "cap_stop", "EY_L", "EY_U", "pair_term_rel", "r", "s_log2", "sT", "success", "AB",
              "AB_ceiling", "C_units", "D", "total", "total_log2", "claim_time_log2_3dp", "claim_check",
              "preprocessing", "preprocessing_log2"):
        print(k, r[k])
    print("cap", pp.cap, "ex_bound", pp.ex_bound, "ex2_bound", pp.ex2_bound)
    T = r["T"]
    print("pieces", 2609 * r["B7"], 32 * T, D(pp.cap) * T, 2609 * r["B7"] + 32 * T + D(pp.cap) * T)
    for label, pl in (("p_L", MEAS["pL_log2"]), ("2^-44.3", "-44.3"), ("2^-44.5", "-44.5"), ("2^-46", "-46")):
        rr = evaluate(v10(cap=pp.cap, T=T, pL_log2=pl))
        print("sensitivity", label, "success", rr["success"][:10], "sT", rr["sT"][:12])
    tot = r["total"]
    E = 159412543029248
    print("fallback", tot + E, lg(tot + E), "no-factor", lg(tot + 593858 * 2 ** 23))
    for k in (23, 24, 25):
        print(k, [math.ceil(float(lg(tot + m * 593858 * 2 ** k)) * 100) / 100 for m in (8, 32, 64)])
    # attribution: lazy only (no measured p) with f807 floor rule 0.3901, and measured p without lazy
    a = solve(floor="0.3901", success_model="condition-count")
    print("lazy only (2^-46, floor 0.3901):", evaluate(a)["total_log2"][:10], a.cap, a.T)
    b = solve(lazy_cv=0, batch_ops=2805)
    print("measured p, no lazy:", evaluate(b)["total_log2"][:10], b.cap, b.T)
    c = solve(floor="0.3901")
    print("measured p, lazy, floor 0.3901:", evaluate(c)["total_log2"][:10], c.cap, c.T)


if __name__ == "__main__":
    main()
```
