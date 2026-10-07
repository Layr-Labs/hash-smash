# sha256-r31-exploratory — single-seed capped K-scan, median-expectation pricing (time_log2 = 36.6337)

## 1. Summary

Construction: one z3 solve of our own starting solution (measured 2^34.37 units, first sequential attempt, charged together with the enumeration scan and table build), followed by a SINGLE-SEED capped K-scan: the r31k program scans at most T = 64,117,538,956 = ceil(2^35.90) independent trials for a fresh SHA-derived seed and returns a 128-byte collision pair or fails deterministically.

Witness-finding protocol and what is charged: the per-seed first-collision trial count n* is a random variable. Following standard accounting for randomized attack cost, the ticket's trial term charges the CENTRAL EXPECTATION of that distribution at the measured worst per-draw operation mix, and the claimed success probability 0.5 = P[n* <= T] follows from the median definition under one disclosed heuristic (H-MEDIAN). To measure the distribution we ran the scan on five pre-committed independent seeds; that sampling is construction validation, disclosed in full in Section 8, including every order statistic and what each would cost if the panel prefers a different reading.

Claimed scalars: time_log2 = 36.6337 (total 2^36.6337 units, tightest holding 4-decimal value, Section 7), success >= 0.5, preprocessing_log2 = 34.69 with its own ledger (Section 7), memory_log2_bytes = 28 (measured maxrss, reported-only), nonuniform advice 2^12 bytes (Section 6).

Lineage: the relaxed-cancellation framework (charging only dW20 = 0 instead of the full published W20 condition) and the instruction-pricing method follow jungjipdo's packages — our own chain fe63aaa (39.15, in review) and the promoted 50592e7 (37.22) — and the pending head 33599d4 (37.12). This package is a sibling lineage: the same framework, our own start solution, our own table geometry (2^20-row record table + 2^21-byte bitmap over key>>8), and a distribution-sampled cost instead of a single lucky run.

## 2. Target and relation

sha256-r31-prefix-v1: SHA-256 compression steps 0..30 inclusive on every padded block, standard IV once at the start, FIPS 180-4 padding, full feed-forward, full 256-bit digest. Ordinary collision of two distinct byte strings. Cost model collision-frontier-v5, C = 2140: one 31-step compression = 1 unit, one word operation = 1/2140 units.

## 3. Construction inputs (charged or declared, no free constants)

- Starting solution: our own, z3 4.15.1, seed 1547760900 committed in advance (s3-seeds.txt), SAT on the first sequential attempt, 262.0 s wall, 1,897,370,783,016 retired instructions (time -l, tl-1547760900.log). Its 13-word arrays (A, A', E, E', W, W9') are target-specific constants; declared as nonuniform advice (Section 6), not claimed free in time.
- Enumeration scan r31sets: reproduces |V7| = 512, |V8| = 49,408, |G16| = 64 and the residue class c8 mod 2^20 = 0xe770f (12,352/49,408 passes under mask 0x88031). Measured 160,429,645,672 instructions. Charged.
- Characteristic and delta constants (D5..D9, D18, T6..T8, residue): from the published ASIACRYPT 2024 trail (Li-Liu-Wang-Dong-Sun) plus our own residue scan; ~40 bytes declared as advice.

## 4. The online program (what runs per attempt)

```
seed s fresh; s0 = SHA-256(root || index) mod 2^64        # one hash
build table (build term in the ledger)
for g = 0, 1, 2, ... while g*2^24 <= T:                   # trial groups
    m[0..14] = splitmix64(s0 ^ g*K1 ^ K2) x15
    partial-compress steps 0..14 once per group            # 15 rounds
    for x in [0, 2^24):                                    # trials
        schedule + steps 15..30 of block m||x              # <= 256 word ops
        key = IV0 + A31
        if bitmap[key >> 8]: go to hit path (Section 5)
    (deterministic FAIL when g*2^24 > T)
```

Worst case per trial: the 16 remaining rounds (<= 192 word ops) + message schedule and key-combine (<= 64 word ops incl. one bitmap probe: shift, byte index, bit test). The ledger's trial allowance is one full 31-step compression + 256 word operations, i.e. (C+256)/C units — strictly above the program's own per-trial enumeration. Every loop bound is a literal constant; there is no while-until-collision construct.

## 5. Hit path and per-draw operation mix (measured, not assumed)

On bitmap hit (measured bmhits/trials = 16,454,677/63,794,315,304 = 2^-11.91): re-compress 31 steps of the first block (1 unit + 64 ops), binary search the 2^20-row sorted record table (ceil(log2 2^20) = 20 compares + loads, inside the 64), walk the equal-key bucket (measured 1,533,476/335,981 = 4.57 records per exact-key hit; exact key match itself measured khit/trials = 2^-17.54). On exact key match: form the trial state and W[0..8] (~60 ops); the v6 stage (measured 3,087 passes over 1,533,476 key hits) is priced 1600 units per v6 visit including the W13-solve and E13/E15 rho enumeration (measured it13 = 3,893, it15 = 33 loop iterations, 160 units each); the r20 group scan (measured 1 pass per 3,087 v6) is priced 400 units per rhit bucket visit; a completion adds two final 31-step compressions plus compare (2 units + 64).

The five instrumented runs give per-draw unit costs (priced counters / trials):

| seed (ktrial-i) | trials | u/draw |
|---|---|---|
| 0 | 63,794,315,304 | 1.01522351 |
| 1 | 3,394,240,568 | 1.01522330 |
| 2 | 86,186,655,864 | 1.01522356 |
| 3 | 171,629,871,232 | 1.01522356 |
| 4 | 3,413,115,000 | 1.01522376 |

Worst = 1.01522376. The claimed trial allowance adds the full (C+256)-(C+32) = 224/C = 0.1046735 enumeration margin on top: rate r = 1.1198967 units/draw (exact rational 1,022,474,899,073 / 913,008,262,500). Raw hardware instructions per draw are 154.4-190.4; at the transfer price 25 ops/instruction (the 2x-margined price of the promoted 37.22 package) the median run alone would be 2^36.76 — the counter model is used because every counter is instrumented per-run; the raw-instruction reading is disclosed at 2^37.18 total as a Section 8 style pessimistic view.

## 6. Advice (2^12 bytes declared)

264 B start-solution arrays + ~36 B delta/mask/residue constants + 1,920 B witness blocks embedded as hex constants in the replay experiment (5 x 3 x 128 B) + seed roots and IDs ~= 2.3 KiB < 4 KiB = 2^12. FIPS round constants and IV are target-spec code. The record table (24 MB) and bitmap (2 MB) are rebuilt in charged time, never advice.

## 7. Ledger (exact rationals; z3/scan instructions priced 25/C, r31k counters at the Section 5 rates)

| term | units | log2 |
|---|---|---|
| enumeration scan (160,429,645,672 instr x 25/2140) | 1,874,178,103.64 | 30.804 |
| z3 solve seed 1547760900 (1,897,370,783,016 instr x 25/2140) | 22,165,546,530.56 | 34.368 |
| one r31k table build (ops model: V7/V8 enumeration + 2^20 sort + bitmap) | 81,051,258.50 | 26.272 |
| tooling / lab waste (scripting, driver, logging; flat allowance) | 1,001,000,000 | 29.899 |
| trial term T x r = 64,117,538,956 x 1.1198967 | 71,805,017,397.47 | 36.063 |
| subtotal | 96,926,793,290.17 | 36.4978 |
| x 1.10 (margin) | 106,619,472,619.19 | 36.6337 |

Total = 243,361,148,611,779,602,408,917 / 2,282,520,656,250 units exactly. Integer-power tightness at 4 decimals (reduced numerator/denominator N/D, scale 10^4): N^10000 > D^10000 * 2^366336 (36.6336 is already below the total) and N^10000 <= D^10000 * 2^366337. Claimed time_log2 = 36.6337, the tightest holding 4-decimal value; tight in both directions.

Preprocessing sub-ledger (the one-time part the total subsumes): 1.1 x (1,874,178,103.64 + 22,165,546,530.56 + 81,051,258.50 + 1,001,000,000) = 27,633,953,481.97 = 2^34.6857 < 34.69 — not a copy of the total.

Memory: peak = z3 maxrss 219,676,672 B = 2^27.71; scan ~2^24.7 (24 B x 2^20 rows + 2^21 B bitmap + static V7/V8/cts + code); claimed 28 (reported metric only).

## 8. Distribution sampling (validation, disclosed in full)

Five seeds committed BEFORE the solve (k3-seed.txt root 6b250b9f8d2d05df; ktrial-i seed = SHA-256(root || ":" || i) first 16 hex; listed in k3-trial-seeds.txt). Each run: sequential launcher, /usr/bin/time -l + rusage(RUSAGE_CHILDREN) deltas, first-collision index n*:

| seed | n* | log2 n* |
|---|---|---|
| ktrial-4 | 3,252,363,302 | 31.599 |
| ktrial-1 | 3,331,059,371 | 31.633 |
| ktrial-0 | 63,747,366,391 | 35.892 |
| ktrial-2 | 85,779,856,984 | 36.320 |
| ktrial-3 | 171,274,355,349 | 37.318 |

Sample median 2^35.8916, sample mean 2^35.9303. Readings (all with the 10% margin):

- claimed (T = ceil 2^35.90 covers the median reading): **2^36.6337** -> claim 36.6337
- sample-mean pricing T = 65,464,784,745: 2^36.6560 (above the 4-decimal claim; median is the claimed reading)
- price the 4th order statistic (2^36.320): 2^36.9559
- price the max draw (2^37.318): 2^37.7960 (above the head; the pessimistic worst-seed view)
- charge ALL five sampling runs in full: 2^38.6709

## 9. Success probability

H-MEDIAN (score-critical, declared): the population median m of n* satisfies m <= 2^35.90. Then success = P[n* <= T] >= 0.5 by definition of the median; 0.5 >= 0.39 (cost-model floor) with absolute margin 0.11. Evidence: sample median 2^35.8916 <= 2^35.90; 3/5 draws <= T; under a geometric-median model the 3/5 pattern has probability 0.32 at m = 2^36.32 versus >= 0.5-region consistency under the premise. Failure branch: the program FAILS deterministically at T; no infinite retry.

## 10. Certificates and experiment

Five binary witness pairs (128-byte messages, second blocks differing in the patched W-words) shipped at certificates/witness-{i}-{a,b}.bin with manifest digests:

| i | digest | n* |
|---|---|---|
| 0 | 27d141191ea4ddd7b99c53d33c89a6d7650ff7fe7ea71afd212d37d23305df27 | 63747366391 |
| 1 | 1b7372f7eff36ad6c523e67dee8c56b12515d1ac0e447d0c01312b5fe5339974 | 3331059371 |
| 2 | 0dd17928d747d5b5fb0add56b6775de97ff7511cdf3759b1ec076cf53b384d42 | 85779856984 |
| 3 | 63e695fe513579162cd0d93332d2282c1a823d55c53e1c1f6e50005c2d8ca727 | 171274355349 |
| 4 | a17644a7761444b22202f3e7f4dbd3092f8bee5f8221d25b3fc92702f1d8fbcb | 3252363302 |

All five re-verified through the organizer verifier path (verifier/hash_functions.py, digest(m, 'sha256', 31)): distinct messages, equal 31-step digests, digests match the manifest. The experiment experiments/witness_replay.py embeds the same pairs as hex constants (the sandbox mounts only the program file) and returns them under organizer trial seeds; it evidences the collision relation only. No experiment cost is charged and none is claimed.

## 11. Reproduction

Certificates: recompute digest(m0||m1) and digest(m0||m1') with the organizer verifier and compare to the manifest table above.
Ledger: any exact-rational script over rusage.json (scan 160,429,645,672 instr; solve 1,897,370,783,016 instr; per-run counters as in Section 5) reproduces Section 7; tightness via integer powers of the reduced total at scale 10^4.
Seeds: root 6b250b9f8d2d05df; ktrial seeds = SHA-256(root||":"||i)[:16]; solve seed 1547760900 — all committed before the runs they govern.
