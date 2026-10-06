# SHA-256, 31 prefix rounds: two-block differential collision (analytic, from published work)

This package selects `sha256-r31-exploratory`, target `sha256-r31-prefix-v1`, cost model
`collision-frontier-v5` and policy `paired-lanes-v1`. It declares `time_log2 = 50.0`.
The required `baseline_improved` value `sha256-r31-nominal-v2` only names the organiser's
nominal reference, which is 128. This package improves that nominal figure only if the heuristics
below hold. It is not a qualified baseline, a security bound or a computed collision.

## 1. Source and status of the claim

The construction is the published two-block collision attack on 31-step SHA-256 of Li, Liu and
Wang (EUROCRYPT 2024, eprint 2024/349, Section 4.2). It builds on the two-block method of Mendel,
Nad and Schlaeffer (EUROCRYPT 2013). The characteristic below is copied from Table 6 of that paper.
Nothing here is a new attack. The attack was not executed for this package. No experiment manifest
is submitted. The bound rests on the published analysis, and every premise taken from it is declared
as a heuristic in section 7.

## 2. Target

The target is SHA-256 with the standard IV, FIPS 180-4 padding, steps 0 to 30 on every padded block,
full feed-forward after each block, and the full 256-bit digest. Messages are 128 bytes. Block 0 is
the first 64 bytes, block 1 is the next 64 bytes, and block 2 is the fixed padding block for a
1024-bit message. Block 2 is identical for both messages, so equal chaining values after block 1
give equal digests. The two messages must differ. They do, because the second blocks differ in the
words W5 to W9 by construction.

## 3. Algorithm

Notation follows the paper. The state before a block is (A-4..A-1, E-4..E-1). Step i computes

    E_i = A_{i-4} + E_{i-4} + S1(E_{i-1}) + IF(E_{i-1},E_{i-2},E_{i-3}) + K_i + W_i
    A_i = E_i - A_{i-4} + S0(A_{i-1}) + MAJ(A_{i-1},A_{i-2},A_{i-3})

with all additions modulo 2^32. Both blocks use the standard message expansion.

Differential characteristic. The second block pair (M1, M1') uses the characteristic of Table 6.
Nonzero message differences exist only in the expanded words W5, W6, W7, W8, W9, W16 and W18. The
differences in A and E are confined to steps 5 to 13. A local collision in the expansion spans steps 5
to 18. There are no conditions on W0 to W4. The ASCII rows of Table 6 for steps 3 to 18 are the
conditions on (A_i, E_i, W_i). The remaining rows are all `=`.

Phase 1 (preprocessing). Use an SAT/SMT model of the characteristic with the value-transition
constraints on (A_i, E_i, W_i) for 7 <= i <= 10 to find one starting point. A starting point is a
solution of (A_i) for 1 <= i <= 12, (E_i) for 5 <= i <= 12 and (W_i) for 9 <= i <= 12 that satisfies
the conditions of steps 5 to 12. By the paper's analysis the number of admissible (W5, W6, W7, W8) is
2^14, 2^23, 2^27 and 2^25 and, after the conditions on (E3, E4), 2^11 pairs (W7, W8) remain. Enumerate
all 2^14 * 2^23 * 2^11 = 2^48 completions of the starting point. Each yields a valid solution of
(A_i) for -3 <= i <= 12, (E_i) for 1 <= i <= 12 and (W_i) for 5 <= i <= 12. Store the records in a
hash table TAB1 keyed by (A-3, A-2, A-1). Each record keeps at most 128 bytes.

Phase 2 (search). Repeat for at most N = 2^49.3 trials. Draw a fresh first block M0 from independent
uniform random coins and compute one 31-step compression from the IV to get the chaining input
(A-4..A-1, E-4..E-1). Look up (A-3, A-2, A-1) in TAB1. On a match, the record fixes W5 to W12. Then
solve for E0 and W0 to W4 from the chaining input, as in the paper, so that the first five steps
produce the required state. This fixes W0 to W12.

Phase 3 (completion). With W0 to W12 fixed, search the free words (W13, W14, W15) for values that
satisfy the remaining uncontrolled conditions on (E13, E14, E15, W16, W18). By the paper this succeeds
with probability about 2^-1.3 per match. On success output the pair of full messages. On failure go on
with Phase 2. Re-hash both messages fully and verify they are distinct and collide. Stop at the first
verified pair, or after N trials.

## 4. Success probability

Let the random first blocks give matches at rate 2^(ell-96) per trial, where ell = 48 is the log of the
table size. With N = 2^49.3 trials the expected number of matches is 2^(49.3+48-96) = 2^1.3. Each match
completes with probability 2^-1.3, so the expected number of verified collisions is 1. Modelling
matches as Poisson (heuristic H-UNIFORM-POISSON) gives success probability 1 - e^-1 = 0.632. I claim
0.6, which is at least the required 0.39. A failed run is charged in full, since the bound is for the
whole N trials.

## 5. Cost accounting

C = 2140 for sha256-r31, so an ordinary word operation costs 1/2140 of a compression.

| Item | Compressions H | Word operations W |
| --- | --- | --- |
| Phase 2 first-block compressions | N = 2^49.3 | none (the compression is whole) |
| Phase 2 table lookups, at most 40 word operations per trial | none | 40 * 2^49.3 |
| Phase 3 completion, at most 2^1.3 matches times a bounded search | at most 2^40 | at most 2^40 * 2140 |
| Phase 1 table enumeration, charged at one compression per record | 2^48 | none |
| Phase 1 starting point, SAT/SMT allowance | 2^45 | none |
| Final verification, four compressions | 4 | none |

The lookups cost 40 * 2^49.3 / 2140 = 2^49.3 * 0.0187 compressions. Phase 3 is charged at 2^40 in
total, which is loose. Phase 1 enumeration is charged at one full compression per record. The real
cost per record is a few hundred word operations, about 0.1 compressions, so this charge is generous.
The starting point allowance of 2^45 is about 2^13 times the paper's own T_model of 2^31.7 and covers
the time of a SAT/SMT solve measured in compression equivalents, as the paper treats it as negligible.

Total. Take 2^49.3 = 1 unit. Then 2^48 = 0.406, 2^45 = 0.051, the lookups are 0.019, and Phase 3 and
verification are below 0.001. The sum is 1.477 units, so the total is 2^49.3 * 1.477 = 2^49.86. The
claimed bound `time_log2 = 50.0` leaves a margin of 0.14 bits for rounding and unmodelled overhead.
Preprocessing, which is inside the total, is at most 2^48 + 2^45 < 2^48.1, so `preprocessing_log2 = 48.2`.

The paper states its own time as 2^49.8, which is 2^49.3 + 2^48 added in compression equivalents. The
total above agrees with that figure up to the starting point allowance and the lookup charge.

Memory. TAB1 holds 2^48 records of at most 128 bytes, which is 2^55 bytes. Working state and code are
negligible against that. Claimed `memory_log2_bytes = 55`. Memory carries no scalar weight. Nonuniform
advice is zero, and the one-byte bound used in the claim reflects a zero-length advice string.

## 6. Why the construction is a collision

Phase 2 makes the chaining input of block 1 equal to a state whose (A-3, A-2, A-1) coincides with a
stored solution. That solution fixes W5 to W12 and makes the differential conditions on steps 5 to 12
hold for the pair. Phase 3 supplies the remaining conditions at steps 13 to 18. The local collision in
the message expansion then cancels all differences by step 31, so the chaining outputs after
feed-forward are equal. This is the characteristic's design in the paper. This package does not
re-prove it. The check of the output is by complete re-hashing of both messages with the target
definition, so any returned pair is verified independently of the argument.

## 7. Heuristics and limitations

Each premise below is taken from the published analysis, was not re-measured here, and is declared in
`claim.json`.

H-SOLUTION-COUNT. One starting point yields 2^48 valid solutions for steps 5 to 12. Source is the
paper's counts 2^14, 2^23, 2^27, 2^25 and the experimental 2^11 pairs (W7, W8). The 2^11 figure is an
experimental count in the paper. If the true number were 2^47 the table would halve and the trial
count would double, giving a total near 2^50.6, so the bound would fail by about 0.6 bits.

H-GAMMA. Step 3 succeeds with probability 2^-1.3 per match. Source is the paper's estimate gamma of
about 1.3 from 100 tests. A 100-test estimate has a wide error. A true gamma of 2 would raise the cost
by 2^0.7 and break the bound.

H-UNIFORM-POISSON. First-block chaining values give (A-3, A-2, A-1) that behave as uniform 96-bit
values independent of TAB1, and matches are close to Poisson. A deviation changes the success
probability, not the cost. The claim of 0.6 sits well under the 0.632 the model gives.

H-STARTING-POINT. A starting point exists and the SAT/SMT solve for it costs at most 2^45
compression equivalents. Source is the paper, which reports a T_model of 2^31.7 and calls it
negligible. Its unit is not defined here, so the allowance is a judgment, about 2^13 times larger.

Limitations. No experiment is submitted, and none of the figures was reproduced for this package.
The sandbox cannot run an attack of this size. The bound is a transcription of published analysis
with the model's pricing applied, and a reviewer should treat it that way. The paper's Table 6
conditions are reproduced below so the package is self-contained.

## 8. Characteristic (Table 6 of eprint 2024/349)

Rows list the conditions on A_i, E_i and W_i. `=` means no difference, `n`, `u`, `0` and `1` are the
paper's bit conditions. Rows not listed have no conditions.

    3  E: ==========================10====
    4  E: ============0===0=========01===0
    5  A: ===================n=unnnnnnn=n=
       E: 000111010001111110nu=11111unnnu1
       W: ================nuuu=======0=uu=
    6  A: ========n======================u
       E: 101011=11==0n0==u11110==1110011n
       W: ==========u=====u===u======n===u
    7  A: ===u===n==n========n=========n=u
       E: un0u1100n=01u11111001u1=n110u10n
       W: =u=u=======n=====n=nu=n=====nun=
    8  A: =============================n==
       E: 1u01un0u0=1=1=11n=0=u0=001001u0=
       W: =u=nn==========u===u===u==1=====
    9  E: 01100001110=0=010===00=11101u0=1
       W: ================u==========1=u==
    10 A: ================u============u==
       E: =1n1uuuuu0100=1un0=10unnnnnnn010
    11 E: =01u1010uu1==11100===1000001n=0=
    12 E: ==110001=11====1n====0011110n=0=
    13 E: ===0====01======1===============
    14 E: ================u===========0u==
    15 E: ================0============1==
    16 E: ================1============1==
       W: =============unnnunnnnnnnnnnnn==
    18 W: ==============1=n=0==========n==

## 9. Summary of the bound

| Quantity | Value |
| --- | --- |
| time_log2 | 50.0 |
| preprocessing_log2 | 48.2 |
| memory_log2_bytes | 55 |
| success_probability | 0.6 |
| nonuniform advice | none |
| experiments | none |
