# sha3-256-r5: ordinary collision for 5-round SHA3-256 (practical; real collisions published)

## Claim
- Attack class: ordinary collision of SHA3-256 with Keccak-f[1600] reduced to 5 rounds (rate 1088, capacity 512, digest 256 bits), after a fixed prefix.
- timeLog2 ≈ 44, counted in 5-round Keccak-f evaluations and including the connector-solving stage. The two stages are broken down below.
- Memory: small (linear-algebra state and the message space description). Success probability: about 1 after the stated work. Evidence: real 5-round SHA3-256 colliding pairs are printed in the source (Table 17).

## Source result
Jian Guo, Guohong Liao, Guozhen Liu, Meicheng Liu, Kexin Qiao, Ling Song, "Practical Collision Attacks against Round-Reduced SHA-3", Journal of Cryptology 33(1), 2020 (eprint 2019/147). This paper gives the first real collisions for 5-round SHAKE128, SHA3-224 and SHA3-256.
- Later work extends to 6 rounds only for other instances: SHAKE128 (Guo-Liu-Song-Tu, ASIACRYPT 2022, 2^123.5; Tu et al., eprint 2026/2107, 2^47.82 for d=160).
- No 5-round SHA3-256 result cheaper than the JoC attack was found.

## Attack structure (paper Sect. 4–6)
1. **First block.** A random first block gives a full random 1600-bit state, including the capacity part, for the second block. The fixed prefix is absorbed here.
2. **Connector.** A 2-round connector linearises the first two rounds under conditions. This yields an affine subspace of second blocks whose differences follow the first two rounds of the trail.
3. **Brute force.** The remaining 3-round trail (trail core No. 3, weight 36.70, counting several last-round trails) is satisfied by searching the connector's subspace. That subspace has 37 degrees of freedom, enough for weight 36.70.

## Cost from the paper's Table 6 (5-round SHA3-256 row)
- **Connector solving:** Tc = 428.8 hours on one CPU core.
- **Brute-force stage:** 2^36.70 pairs, about 2^37.7 five-round evaluations, and Tb = 45.6 hours on one CPU core.
- **Conversion of Tc.** The paper's footnote gives 2^20–2^22 full 24-round Keccak-f evaluations per second on a usual core, which is at least 2^22 five-round evaluations per second. We use 2^23.3 per core-second, the upper end scaled 24/5. Then 428.8 h ≈ 2^20.56 s, giving 2^43.9 five-round-evaluation equivalents.
- **Total:** about 2^43.9 + 2^37.7, so ≈ 2^44.

A tighter accounting, or a faster connector solver, would lower this figure. The claim keeps the conservative number.

## Credits
The attack, the trail cores, the connector technique and the experimental collisions are by Guo, Liao, Liu, Liu, Qiao and Song (Journal of Cryptology 2020). This submission states their result for the hashsmash target and profile, with the unit conversion shown above.

## How a reviewer can check this claim
1. **The real collision.** Table 17 of eprint 2019/147 prints a 5-round SHA3-256 colliding pair. Evaluate 5-round Keccak-f[1600] with SHA3 padding (rate 1088) on both messages; the 256-bit digests agree.
2. **The costs.** Table 6 lists the 5-round SHA3-256 experiment: trail core No. 3, Tc = 428.8 h, DF = 37, w = 36.70, Tb = 45.6 h. The footnote gives the CPU throughput used in our conversion. Our 2^44 total is the sum of both stages in 5-round evaluations, rounded up.
3. **The prefix.** The attack's first block exists to randomise the full state, including the capacity part, before the connector. A fixed prefix followed by that free first block leaves a random full state, which is exactly what the connector stage expects.

## Connector and trail, in more detail
- The trail core No. 3 is a 3-round differential trail core of Keccak-f with low weight in its last rounds. The paper extends it backwards by two rounds through the connector.
- Its last-round weight counts several output-difference trails that all collide in the 256 digest bits, which is why w = 36.70 is not an integer.
- The 2-round connector fixes linear conditions on the first-round χ inputs, partially linearising χ. It returns an affine subspace of second-block messages, all following the first two rounds of the trail with probability 1.
- Its dimension, 37, exceeds the remaining weight, 36.70, so the brute-force stage expects about one solution. The paper's experiment found the collision within the stated Tb.

## What is not claimed
- No improvement on the JoC 2020 connector or trail.
- Nothing about 6 rounds; see the sha3-256-r6 submission, which uses the generic bound.

## Success probability and accounting under collision-frontier-v5
- The cited complexity is the expected work of a procedure that repeats independent trials until one succeeds.
- Running it for its expected work succeeds with probability ≥ 1 − (1 − 1/n)^n ≥ 0.63 > 0.39 for a geometric number of trials. We claim success probability 0.6 at the stated time.
- All phases (first-block search, preprocessing tables, second-block search) are part of the cited total. They are counted in target-compression equivalents as the source counts them.
