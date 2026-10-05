# SHA3-256-r6 DP collision search (K0=1.10·2^128, w=34)

Lane: exploratory. Target: `sha3-256-r6-prefix-v1`. Scalar under collision-frontier-v5.
Time ≤ 2^128.17, memory ≤ 2^120, success ≥ 0.39 under **H-RF**. Claim: **128.17**.

Opcount revision of validating `98f34694` @ 128.18: same K0/H-RF evidence, **w=34**
(+4 over frozen tight ≤30).

## 1. Target / step map

SHA3-256 rounds 0..5. `f(x)=SHA3-256-r6(LE32(x))`. One `f` = 1 perm + w ordinary ops.

## 2–4. Model, parameters, algorithm

C=1626. K0=1.10·2^128. θ=2^-32. L=2^40. w=**34**. Single-processor VOW+RELOCATE (unchanged).

## 5. Correctness (unconditional)

RELOCATE + verify ⇒ ordinary collision.

## 6. Success under H-RF

1-exp(-1.10²/2)≈0.4539>0.39 after DP bad-event margin. Same as 128.18.

## 7. Time — frozen w=34

Tight ≤30 (absorb 12, load 4, pad 2, pack 4, DP 3, loop 4, contingency 1).
Claimed w=34 = tight + **4 spare**.

    log2(1.10·2^128·(1+34/1626)) ≈ 128.167360 < 128.17

## 8. Memory

≤2^120 bytes.

## 9. H-RF evidence (unchanged)

sha3r6 n=32 trials=120: k0=1.10→0.4000; 1.12→0.4333; 1.14→0.3917.
RF@0.9944 sha3r6 all n miss 0.39. No new trials.

## 10–11. Limits / provenance

Exploratory only. Replaces 128.18 w=36. Awaiting radix left alone.
