# sha256-r31: ordinary collision for 31-step SHA-256 at 2^40.5

## Claim
- Attack class: ordinary collision of the SHA-256 hash with the compression function reduced to its first 31 steps, starting from the chaining value left by a fixed prefix.
- timeLog2 = 40.5 (31-step compressions). Memory 2^19.8. Data: none. Preprocessing: included. Success probability: close to 1 after the stated work.
- Status of the underlying result: published and experimentally confirmed. The authors report a real colliding message pair found in 1.2 hours with 64 threads.

## Source result
Yingxin Li, Fukang Liu, Gaoli Wang, Xiaoyang Dong, Siwei Sun, "The First Practical Collision for 31-Step SHA-256", ASIACRYPT 2024, LNCS (doi 10.1007/978-981-96-0941-3_8).
- It improves the EUROCRYPT 2024 attack of Li, Liu and Wang ("New Records in Collision Attacks on SHA-2", eprint 2024/349), which had time 2^49.8 and memory 2^48.
- The new attack is memory-efficient: time 2^40.5, memory 2^19.8.
- Earlier history:
  - Mendel, Nad and Schläffer, EUROCRYPT 2013 ("Improving Local Collisions: New Attacks on Reduced SHA-256"): first 31-step collision, 2^65.5 time, 2^34 memory.
  - Nikolić and Biryukov, FSE 2008: shorter step counts.

## Attack structure
1. **Characteristic.** A local collision in the message expansion makes the state difference vanish before step 31. A differential characteristic for the second message block is found with SAT/SMT-based tools. Its conditions sit mostly in the first steps, where message modification satisfies them for free.
2. **Two blocks.** The first block M0 is searched so that the chaining value entering the second block meets the few conditions the characteristic places on it. The 2023/2024 papers show this first-block phase dominates the cost.
3. **Memory-efficient matching.** The ASIACRYPT 2024 paper replaces the large precomputed table of the EUROCRYPT 2024 attack with a phase that needs only 2^19.8 memory, bringing the total to 2^40.5 time.
4. **Second block.** Once a suitable chaining value is found, the second-block pair (M1, M1′) follows the characteristic with message modification, and a collision of the full 31-step compression output follows.

## Why the number transfers to this track
- The target is exactly 31-step SHA-256 (the hashsmash target "sha256-r31", rounds = 31) with the standard message expansion and the feed-forward.
- The prefix only changes the starting chaining value of the first-block search. The first-block phase is a search over first blocks for a chaining value meeting the conditions, so where it starts is irrelevant.
- The 2^40.5 is the authors' own count in 31-step SHA-256 computations, matching the cost model's unit.

## Credits
The attack and its complexity are the work of Li, Liu, Wang, Dong and Sun (ASIACRYPT 2024), building on Li, Liu and Wang (EUROCRYPT 2024) and Mendel, Nad and Schläffer (EUROCRYPT 2013). This submission states their result for the hashsmash target and profile. It claims no new cryptanalysis for this track.

## How a reviewer can check this claim
1. **The published pair.** The ASIACRYPT 2024 paper prints a colliding message pair for 31-step SHA-256 from the standard IV. Recompute 31 steps of the SHA-256 compression with feed-forward on both two-block messages. The outputs agree and the messages differ, which shows the characteristic is satisfiable in practice.
2. **The complexity.** The paper states time 2^40.5 and memory 2^19.8 for the whole attack, first-block phase included. The EUROCRYPT 2024 predecessor (eprint 2024/349) states 2^49.8 / 2^48. Our figure is the published one, not an extrapolation.
3. **The step count.** The hashsmash target `sha256-r31` has `rounds: 31` in its metadata, and SHA-256 "rounds" are its 64 steps, so 31 means exactly the 31-step reduced compression these papers attack.
4. **The prefix.** Nothing in the attack fixes the chaining value of the first block. The first-block search is a randomised search over first blocks starting from whatever chaining value the prefix leaves, so its expected cost is the same for every prefix.

## What is not claimed
- No new characteristic or improved complexity for 31 steps. That would need a new trail search, for example with the authors' SAT/SMT model.
- Nothing about 32 or more steps; see the sha256-r32 submission for that track.

## Success probability and accounting under collision-frontier-v5
- The cited complexity is the expected work of a procedure that repeats independent trials until one succeeds.
- Running it for its expected work succeeds with probability ≥ 1 − (1 − 1/n)^n ≥ 0.63 > 0.39 for a geometric number of trials. We claim success probability 0.6 at the stated time.
- All phases (first-block search, preprocessing tables, second-block search) are part of the cited total. They are counted in target-compression equivalents as the source counts them.

## Certificate
The ASIACRYPT 2024 authors published a colliding pair for 31-step SHA-256 (two-block messages M0||M1 and M0||M1'). It is attached as certificate `published-31step-pair` and checked by the organizer verifier: both padded 128-byte messages have the sha256-r31 digest 55fdfb37efcbd086e19c3de0f72596300a3acdf48da5b1d0450a592bb2869fcd. This shows the characteristic and the two-block procedure work in practice for exactly this target. The claimed time is the authors' attack cost, not the cost of copying their pair.
