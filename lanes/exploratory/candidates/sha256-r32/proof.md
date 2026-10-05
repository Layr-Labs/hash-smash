# sha256-r32: ordinary collision for 32-step SHA-256 in 2^55.2 target compressions

## 1. Claim
- Two-block ordinary collision of the complete SHA-256 hash with steps 0–31 on every block, standard IV and FIPS 180-4 padding.
- **time_log2 = 55.2** in 32-step compressions. Success probability 0.6. Memory: small (the source reports negligible memory); we report 2^32 bytes as a safe bound.
- **Basis:** the 36-step SHA-256 collision attack of Yingxin Li, Zhuolong Zhang, Muzhou Li, Fukang Liu, Haifeng Qian and Jinwei Zhu, "Pushing Collision Attacks on SHA-2 to 39 Steps" (IACR ePrint 2026/1120). It has time 2^57 and negligible memory, and the authors give a real 36-step colliding pair (their Table 2). We restrict it to 32 steps (Section 3) and re-price it under collision-frontier-v5 (Section 4).

## 2. The source attack (ePrint 2026/1120, Sect. 3–4, Tables 9–10)
**Characteristic.** Message differences occur only in W5, W6, W7, W8, W9, W13, W14, W21 and W23. Table 9 shows the 36-step characteristic: from step 24 to step 35 every row has zero difference in A, E and W. The last nonzero state difference is at step 21, and the last message difference is in W23.

**Procedure.** It is a memory-efficient two-block meet-in-the-middle:
1. A SAT solver finds a starting solution for the dense part (steps ≤ 15) once. The paper puts this at ≈ 2^39.8 SHA-256 compression calls.
2. Random first blocks M0 are tried until the chaining value CV1 meets the conditions on (E3, W5, W6, W7): 1, 4, 6 and 4 conditions. Measured over 2^40 random M0, the success probability is ≈ 2^−15.
3. For each valid M0, the 2^20 possible values of (W14, W15) are enumerated against the 57 remaining uncontrolled conditions on (A_i, E_i, W_i) for i ≥ 16 (Table 10).
   - This requires 2^(57−20) = 2^37 valid M0, so step 2 costs 2^37 · 2^15 = 2^52 compressions.
   - Step 3 tests 2^37 · 2^20 = 2^57 tail candidates.
   - The paper's total is 2^52 + 2^57 ≈ 2^57, with negligible memory.

## 3. Restriction to 32 steps
- **Zero tail.** All message differences sit at W ≤ W23, and the state difference is zero after step 21. For the 32-step function, the second-block outputs of the pair therefore have zero state difference after step 31, and equal feed-forward inputs give equal 32-step compression outputs. The common padding block keeps them equal.
- **Expansion conditions.** The 36-step characteristic needs expanded words W24..W35 to have zero difference. The 32-step function only uses W24..W31, a subset, so no condition is added. The conditions used in steps 2–3 (E3, W5–W7 and Table 10's (A_i, E_i, W_i) for 16 ≤ i ≤ 23) all lie within the first 32 steps, so none is removed in a way that would change the procedure.
- **First block.** It is now hashed with the 32-step compression. Step 2 is a search over uniformly random first blocks for a chaining value meeting 15 conditions. The per-trial success probability of such a filter on a uniformly distributed chaining value does not depend on whether 32 or 36 steps produced it; we use the paper's 2^−15.
- **Starting solution.** The step-1 SAT solution concerns only the dense part of the second block (steps ≤ 15), which is identical for 32 and 36 steps.

## 4. Pricing under collision-frontier-v5 (C = 2224 word operations per 32-step compression)
- **Step 1:** 2^39.8 compression equivalents, one-time, at the paper's own conversion.
- **Step 2:** 2^52 first-block trials, each one 32-step compression plus a few comparisons: 2^52 · (1 + 16/2224) ≈ 2^52.01.
- **Step 3:** 2^57 tail candidates.
  - Each fixes (W14, W15) and evaluates steps 14–21 incrementally from the fixed dense state at step 13, together with the message-expansion words W16, W18, W20, W21 that W14 and W15 influence. It then checks the step-16..23 conditions, stopping at the first failed condition.
  - That is at most 8 SHA-256 steps of the 32 in a compression, plus 4 expansion words. We charge it as ≤ 1/4 compression, though early abort makes the mean much smaller.
  - Cost: 2^57 · 2^−2 = 2^55.
- **Total:** 2^39.8 + 2^52.01 + 2^55 ≤ 2^55.17. **We claim 55.2.**
- **Success probability.** The search stops at the first candidate meeting all conditions, and each candidate succeeds independently with probability 2^−57 under the source analysis (heuristic H1). Running for the stated expected work succeeds with probability ≥ 1 − e^−1 ≈ 0.63 ≥ 0.6.

## 5. Other routes and why this one
- Zhang, Li, Gao and Wang (EUROCRYPT 2026, ePrint 2026/232): 36 steps at 2^94.4.
- Li, Liu, Wang and Sun (2026), cited in ePrint 2026/1120's Table 1: 36 steps at 2^71.
- ePrint 2026/1120 improves both to 2^57 and confirms it with a real colliding pair for 36-step SHA-256.
- A 32-step-specific characteristic could be cheaper still. That would be new cryptanalysis and is not claimed here.

## 6. Scope and limitations
- The complexity figures, the 2^−15 first-block filter rate and the 2^−57 tail rate are the source's measured and computed values. We restrict and re-price them; we do not re-derive the characteristic.
- The 1/4-compression charge per tail candidate is an upper bound on incremental evaluation of steps 14–21. Charging a full compression per candidate instead would give 57.0.

## Credits
The 36-step characteristic, the memory-efficient attack, its complexity analysis and the 36-step colliding pair are by Li, Zhang, Li, Liu, Qian and Zhu (ePrint 2026/1120). The restriction to 32 steps and the v5 pricing are ours.
