# 38-step SHA-256 collision with dense-part variants and a table-free row-16 search: 2^97.08020

**Track** sha256-r38-exploratory, target sha256-r38-prefix-v1, cost model collision-frontier-v5 (C = 2728).
**Claim** time_log2 = 97.08020 (exact total 2^97.08020 target compressions), success probability at least 0.39
(bound 0.390000020), memory 2^57 bytes (online 2^22.08), preprocessing 2^70.00282 (allowances and counted build, included in time),
nonuniform advice 2^16 bytes. The attack proper (online work, first-block compressions and the counted
row-16 search) is 2^97.08; the allowances A_C = 2^70, A_S = 2^60, DEV = 2^60 are 2^70.0028 in all.

**What is new.** The dense-part-variant attack of the public packages examines, per first block, about 2^37.5
variant dense parts through lookup tables of 2^80 bytes. This package examines the same variant set with a
table-free split search (Section 5): per (chaining value, A0) and per A2-class, all row-16-passing variants are
found in exactly 2^20 index probes against a 2^16-entry H-index of 2^17 bytes, built once. Everything else
(characteristic, variant sets, success analysis, allowances) is inherited as stated, with declared
dependencies. No table is read by the online program; memory is 2^57 bytes overall (2^22.08 online).

## 1. Target, cost model and machine

Target sha256-r38-prefix-v1: SHA-256 steps 0..37 on every padded block, standard IV once, FIPS 180-4 padding,
feed-forward, all eight digest words. Messages are M0 || M1 and M0 || M1' of two blocks (common first block;
padding appends the same third block) with equal digests. Cost model collision-frontier-v5, C = 2728: one
target compression costs 1 unit, every other primitive word operation 1/C; the machine is a 256-bit word RAM
with 256-bit load/store, addition/subtraction mod 2^256, AND/OR/XOR/NOT, shift/rotation, comparison,
conditional branch and independent uniform random 256-bit words; memory is a reported metric. The counted
program of Section 6 is scalar: every 32-bit value lives one per 256-bit word, low bits, masked clean after
every add, sub and rotation. It charges 1 per executed 256-bit and, or, xor, shr, ld, st, li, comparison;
2 per 32-bit add and sub (operation and mask); 4 per 32-bit rotation (shl, shr, or, mask); 2 per conditional
branch (comparison and branch); 2 per 32-bit rand (rand and mask); 1 unit per target compression (f38).
Hence s0/s1 (rotr, rotr, shr, xor, xor) cost 4 + 4 + 1 + 1 + 1 = 11, S0/S1 (three rotrs) 4 + 4 + 4 + 1 + 1 = 14,
MAJ/CH 3, and a 32-bit counter increment with branch 2 + 2 = 4. Every count below is in these primitives.

## 2. Sources, credit and dependencies

Reused, with credit and declared Yukon dependencies: the 38-step characteristic (Table 3), two-bit conditions
(Table 4) and semi-free-start pair (Table 5) of Li, Zhang, Li, Liu, Qian and Zhu, "Pushing Collision Attacks
on SHA-2 to 39 Steps" (IACR ePrint 2026/1120), as transcribed in Yukon submission 0ae69bcb (0xshikhar, 72.64);
the dense-part variants (A0, A1, A2), the A0 set of 256 values, the 768-value A2 list, the row-16 set G and
the success analysis by groups of the public packages c99df2dc (qkniep) and 0ae69bcb; the work caps and the
exact success bound of submission 44cb527b (Th0rgal, 71.39494). No peer code was executed; peer packages were
read as data, and every reused number used here was rechecked as stated (Sections 3, 11).
New in this package: the split row-16 search (Section 5), the exact ledger (Section 8), and the experiment
(Section 11). The characteristic search, Step-1 solve and development are charged as allowances (H4), as in
the cited packages.

## 3. Characteristic data

3.1 The Table-5 semi-free-start pair (CV; M member y printed first; M' member x printed second):

```text
CV  cd278980 1b12a052 b87cc8a6 a9e059c5 c9c3db85 6ca4b5b5 63d13ac1 c0329f1e
M   48fc271b 9fca20cd cc89f96f fc40396f 8b328cb4 6b91ef78 97f9b767 e2450045 3b016f58 de9804cb 66a99ea5 0ce30b8d a28cd15a 77a1e994 d28e48a0 9b5f6dbb
M'  48fc271b 9fca20cd cc89f96f fc40396f 8b328cb4 6b91ef78 97f9b767 c2450045 3f416758 fe9804cb 63a88c0f 0ceb1f8d a28cd15a 77a1e994 d28e48a0 9f1f65bb
```

F_38(CV, M) = F_38(CV, M') = 5d9ca5f4 59ace3a3 26c9c26c 4252c585 4c0803b7 1b4d5ccd 25c3ccc0 90645c4d.
The experiment of Section 11 recomputes this equality. The published dense part S* (member x values; member
y differs only where listed) is: A0 b75dae71; A1 da6c35e0; A2 479b4dc8; A3 d374b0d8; A4 df740c96;
A5 1ee5f173; A6 7fd9cecb; E4 627cb061; E5 1e847683; E6 0c1c24b9; E7 e2e9b205/02e9b205;
E8 99352c79/917934e9; E9 c670b71b/c2e0b710; E10 68c3aa97/6882a297; E11 c2f2c1be/e2f2b1ba;
E12 5f9d1216/63be1213; E13 35c13b0d/35c03c77; E14 21966471/29976471; E15 4a9b6b5a/4a9b63da;
W8 3f416758/3b016f58; W9 fe9804cb/de9804cb; W10 63a88c0f/66a99ea5; W11 0ceb1f8d/0ce30b8d;
W12 a28cd15a; W13 77a1e994; W14 d28e48a0; W15 9f1f65bb/9b5f6dbb.

3.2 Row 16 holds iff W16 is in G = {0x35f29010 + any subset of bits 0, 2, 10, 13, 19}, exactly 32 words
(Appendix A lists them; verified by exact set construction in Section 11 code). W7 must lie in F7 = {w : s0(w + d7) - s0(w) = t7} with d7 = 0x20000000 and
t7 = 0x03bff800; |F7| = 287309824 (exact exhaustive count, Appendix E), p2 = |F7| / 2^32 = 2^-3.90197. The online program
tests F7 membership by direct computation (2 s0 + add + sub + compare, 13 operations charged); no F7 table exists.

3.3 The 768 A2 values fall into 96 c9-classes of 8 (Appendix A lists each class with its c9 value;
every one of the 768 recomputed exactly from S* by the c9 formula of Section 4 with K9 = 0x12835b01, all match).
The A0 set is 256 fixed values (Appendix A; transcribed through the cited package lineage) with exact
variant-set sizes summing to SR = 191773672732 = 2^37.48061 (summation rechecked exactly here).

## 4. Dense-part variants

A variant v = (A0, A1, A2) is the published dense part with A0, A1, A2 of both members replaced (rows 0..6
carry no A or E difference, so both members take the same values), A3..A13, E7..E13 and W11..W15 kept, and
E4, E5, E6 and W8, W9, W10 of each member recomputed by E_i = A_i + A_{i-4} - S0(A_{i-1}) -
MAJ(A_{i-1}, A_{i-2}, A_{i-3}) (i = 4, 5, 6) and W_i = E_i - A_{i-4} - E_{i-4} - S1(E_{i-1}) -
CH(E_{i-1}, E_{i-2}, E_{i-3}) - K_i (i = 8, 9, 10). A variant is valid if (i) the E cells of rows 4..8 hold for
both members including the + pairs, and (ii) for i = 8, 9, 10, 11 the pair (W_i^x - W_i^y, s0(W_i^x) - s0(W_i^y))
equals the published value (Appendix B): (043ff800, 01808000), (20000000, fbc00800), (fcfeed6a, 10005f30),
(00081400, 03011296). The charged validity test runs, unconditionally for every (u, A2), the cheap
checks: A1 = u - Y (2), E4,E5,E6 recompute (21 each = 63), E-cell mask/x-value/plus checks rows 4..8
(10 each = 50), W8,W9,W10 recompute (23 each = 69), W8..W11 difference-pair checks (dxor 2, two s0 22,
sub 2, two branches 4 = 30 each = 120): 304 total, envelope 320 per (u, A2). Every (u, A2) passing the cheap
checks (at most 448 per class: same halt as Section 5) additionally gets: steps 8..15 evolution with A16/E16
(9 x 54 = 486), the 12 A/E two-bit conditions keyed at row 16 (A-side operands are S* constants: 9 x 4 = 36;
E16-internal: 3 x 6 = 18; the 6 W16-internal conditions hold for every G word automatically, verified
exhaustively), and the c7/F7 test (48): 588, envelope 600. No variant is ever skipped before its checks.

Lemma 3 (soundness; as in the cited packages). For valid v and any chaining value CV1, the Step-2 words
W0..W7 (E_i = A_i + A_{i-4} - S0(A_{i-1}) - MAJ(A_{i-1}, A_{i-2}, A_{i-3}) for i = 3, 2, 1, 0, then W_i = E_i -
A_{i-4} - E_{i-4} - S1(E_{i-1}) - CH(E_{i-1}, E_{i-2}, E_{i-3}) - K_i for i = 0..7) connect CV1 to the dense
part in both members; rows -4..15 follow every A/E cell, and every modular and s0/s1 difference reaching rows
16 and above equals the published one. Proof: steps 0..7 reproduce A0..A7, E0..E7 by construction of the
Step-2 words; steps 8..10 reproduce E8..E10 and A8..A10 because W8..W10 are solved from them; steps 11..15 are
those of S*; rows 0..3 carry no cells and rows 4..8 hold by validity (i); the expansion terms use W8..W11 with
the published differences by validity (ii), and W12..W15 are published.

For chaining value CV1 = (a, b, c, d, e, f, g, h) and A0, with hh = d - S0(a) - MAJ(a, b, c) and E0 = A0 + hh,
put Y = -S0(A0) - MAJ(A0, a, b) - g - S1(E0) - CH(E0, e, f) - K1 and Z0 = W0 + s1(W14), where W0 is the Step-2
word and W14 the published message word. Y and Z0 depend only on (CV1, A0). With u = Y + A1:

Lemma 5 (row-16 formula). W16^x = s0(u) - u + Y + Z0 + c9(A2), where W9^x = c9(A2) - A1 with c9(A2) = E9 - 2 A5
+ S0(A4) + MAJ(A4, A3, A2) - S1(E8) - CH(E8, E7, E6(A2)) - K9. Hence row 16 holds iff phi(u) + Y + Z0 + c9(A2)
lies in G, with phi(u) = s0(u) - u. Indeed W16 = s1(W14) + W9 + s0(W1) + W0 by expansion, W9 = c9 - A1 by
definition of c9, and W1 = Y + A1 since E1 = A1 + c - S0(A0) - MAJ(A0, a, b) gives W1 = E1 - c - g -
S1(E0) - CH(E0, e, f) - K1 = A1 + Y; substituting u = Y + A1 gives the formula. Checked end to end on the published pair and on 144 independently sampled
valid variants over random chaining values (all match; Section 11 checks the pair).

## 5. Split row-16 search

<!-- E:H6 -->
Fix (CV1, A0) and one c9-class with value c9. Put d = Y + Z0 + c9. Needed: all u with phi(u) + d in G.
Since s0 is GF(2)-linear, write u = H*2^16 + L: s0(u) = s0(H*2^16) XOR s0(L). The low 16 bits of
x = phi(u) + d depend only on L and on P(H) = s0(H*2^16) mod 2^16: with d_lo = d mod 2^16 and sL = s0(L) mod
2^16, x mod 2^16 = ((P(H) XOR sL) - L + d_lo) mod 2^16. G mod 2^16 takes 16 values (bits 0, 2, 10, 13 free).
The H-index maps each 16-bit P to the list of H with P(H) = P: 65537 start-words and 65536 halfword entries
(2^17 bytes, built once in preprocessing). The search loops L over 2^16 values and the 16 x_lo values, forms
P = ((xlo - d_lo + L) mod 2^16) XOR sL, and visits every H in bucket P: exactly 2^20 index probes per class.
Each returned u is verified (phi(u) + d in G) before use.

Per-L charged operations in Section 1 primitives, including all loop control: s0(L) 11 + L counter
increment and branch 4 + 16 x_lo values x (P: sub 2, add 2, and 1, xor 1 = 6; two unpacked start loads = 2;
xlo counter and branch 4; bucket-size branch 2 (at most 2 entries per bucket by the exact P-fiber check, so
the entry loop is one conditional, not a counter); at most 2 bucket entries x (load 1, shift 1, or 1, s0 of
high half 11, xor 1, sub 2, add 2, mask 1, branch-with-compare 2, store 1 = 23)) = 15 + 16 x 60 = 975.
Per class 65536 x 975. Nothing is packed: every 32-bit value lives one per 256-bit word, so plain loads need
no addressing beyond the load itself. Only entries
passing the full check are stored (at most 448 per class: the program halts the group if a 449th solution
appears, and the halt never triggers because phi has max fiber 14 over all 2^32 inputs, cited premise P-MAXFIBER
below, so 32 targets x 14 = 448); the store buffer holds 448 words, and the halt check (counter and branch,
4 per stored solution, at most 1792 per class) is inside the per-class envelope of Section 8.
The H-index has 32768 occupied buckets with at most 2 entries each (exact check over all 2^16 H, Appendix E).

Theorem S (completeness and soundness). For every d, the search returns exactly the u with phi(u) + d in G.
Proof. Every u has a unique (H, L); the loop visits all 2^16 L and, for the x_lo of a solution, computes its P
and visits its bucket, which holds every H with that P by construction of the index; the final check keeps
exactly the solutions. The experiment of Section 11 verifies index integrity (every H in exactly one correct
bucket) and soundness (every returned u checked) on organizer seeds. phi has max fiber 14 over all 2^32 inputs
(cited premise P-MAXFIBER, Section 10), so a class holds at most 32 x 14 = 448 solutions.

## 6. Online algorithm

A group is one full first block M0 (16 fresh uniform random words) and, per A0 value, the
256 A0 blocks below. CV1 = F_38(IV, M0) costs one compression plus 2 rand, 32 extract (shr and and each) and 16 store operations (55 total with group control).
Per (CV1, A0): Step-2 W0..W7, hh, E0, Y, Z0 (384 operations charged: E_i i = 0..3 at 21 each (add 2, sub 2,
S0 14, MAJ 3), W_i i = 0..7 at 23 each (sub 2, sub 2, S1 14, CH 3, sub 2), hh 19 with E0 2, Y 40, Z0 13
(add 2, s1 11); actual 342, margin covers class and A0 loop control). Per c9-class (96): d = Y + Z0 + c9
(4 ops); the split search
(2^20 probes at the Section 5 count of 975 per L);
validity tests (cheap 320 per (u, A2) plus 600 per cheap-pass for all 3584 (u, A2) pairs deterministically, at most 3400000 ops per class including the 448-halt checks, as itemized in Section 4). Per cheap-passed row-16 variant (at most 3584 per class deterministically): c7 and
the direct F7 test (48 ops charged: F7 proper 36 plus c7; NT counts these tests). Per W7 pass: the row-17
cascade, an explicit program: evolve steps 8..16 (9 x 54 = 486; per step T1 25, T2 19, state updates 10),
E17 by formula (21), E17/A17 mask, x-value and plus checks (19), the 8 two-bit conditions keyed at row 17
(40): actual 566, envelope 640. Per
row-17 pass: steps 17..37 evolution (21 x 54 = 1134), E-cell checks rows 18..23 with W23/W25 (70), the 15
remaining two-bit conditions (75): actual about 1280, envelope 8192, plus full two-message verification (second blocks and padding blocks from the common first-block state: 4 compressions), 8192 charged.
Five counters (u-solutions examined NE, W7 tests NT, W7 passes NW, row-17 passes N1, deep passes N2) are compared
with the caps of Section 7 after every group; the program halts unsuccessfully on overflow and halts with the
first verified collision (Lemma 7 of the cited packages: a variant passing all rows yields F_38(CV1, M1) =
F_38(CV1, M1') with M1 != M1', since W7 differs by d7; every output pair is recomputed before return).

## 7. Success analysis

<!-- E:H1 -->
H1 (single-trial chaining value). For one group, the chaining value CV1 = F_38(IV, M0) of a first block M0
built from two fresh uniform random words behaves as a uniform 256-bit value as far as the events of one fixed
variant are concerned: for each A0 the table index (Y, Z0) is uniform, W7 is uniform and independent of
(W0, W1), the first row-17 test passes with probability 2^-10 given a W7 pass, and E[counts] below hold.
Groups use fresh coins and are independent. Nothing is assumed about two variants of one group (H5).
Evidence for the uniformities is the published measurements restated from the cited packages (12 real first
blocks x 256 A0: entries 0.991 and W7 passes 0.99 times expectation; 6 more chaining values: 1.037 and 0.92).

<!-- E:H2 -->
H2 (variant q3). The average over examined variants and uniform chaining values of q3(v) = Pr[rows 16..37 hold
| W7 in F7] is at least q3_model = 2^-101.5. Evidence: two independent preregistered sequential Monte-Carlo
studies (R1: 1024 runs over a uniform 2^20-variant sample, mean 2^-100.99875, 99% bound 2^-101.00146; R2: 4096
runs with one fresh uniform variant each, mean 2^-101.00020, bound 2^-101.00195; 21.9 million tail successes,
every one rebuilt into a verified 38-step semi-free-start pair, 0 failed rebuilds), restated from the cited
packages; the stage factors are the integers -27, -17, -13, -15, -6, -7, -1, -15 given by the per-row condition
counts. q3_model is half a bit below both bounds by preregistered rule.

<!-- E:H5 -->
H5 (pairs in group). With N the successful variants of one group, E[N(N-1)] <= E[N] (delta = 1), so by
Bonferroni Pr[N >= 1] >= E[N]/2 per group. The pair budget is measured, not assumed: around 4400 verified
tail successes from the author's SMC (Section 12), the author measured co-occurrence exactly as in cited
Section 6.5: NEAR (300 successes, all 768 same-(A0,A1) A2 variants each): 3802 other valid, 29 E17-mask passes
(0.097 per success), 0 further successes; OWN-BLOCK (50 successes, true buckets via the split search itself):
690 other entries, 4 E17-mask passes (0.08 per success), 0 further successes; FAR (5 successes x 10 other A0):
248 entries, 0 E17-mask passes. The far term is bounded analytically by the unconditional rate
(E[NW] x 2^-10 per block x 255 blocks = 0.093 per success). The far term models other-A0 blocks as
independent at the unconditional rate (the cited Section 6.5 design; shared-CV1 dependence is not separately
bounded, and 0 passes in 50 measured far blocks are consistent with the model). Statistical upper bounds
(one-sided 99% Poisson: 29 observed gives 44.20, i.e. 0.147 per success; 4 observed gives 11.62, i.e. 0.232
per success cross-checking the near component): point estimates give delta1 <= 0.097 + 0.093 = 0.19
(own-block 0.08 cross-checks the near component), and 0.24 at 99% confidence; the bound uses the envelope
delta = 1 (5x over points, 4x over the 99% upper). No further success
appeared in any of the 400 examined neighborhoods. The cited packages measured 0.23 on the same decomposition.
With S_model = SR x p2 x q3_model = 2^-67.92135 and q_lb = S_model / 2, groups give Pr[no success] <= (1 - q_lb)^NG
<= exp(-NG q_lb). Counters NE (u-solutions validity-tested), NT (W7 tests), NW (W7 passes), N1 (row-17 passes),
N2 (deep passes) have per-group expectations E_NE = 786432, E_NT = 1428.94, E_NW = 95.58, E_N1 = 0.0933,
E_N2 <= E_NW x 2^-10 = 0.0934 (a W7 pass reaches the deep tests only by passing the 10-bit first row-17 test, whose conditional pass rate is exactly bounded by H1; no product over further bits is used, so no independence premise beyond H1 enters) and rigorous per-group maxima
B = 11010048 each (448 u-solutions per class from the max fiber 14 of phi, times 96 classes times 256 A0).
NE_MAX = 230872645036871416730517504. NE is also deterministically bounded by construction; its Chebyshev term (2^-56.1) is retained for uniformity.
By Chebyshev over the independent groups, each counter sum exceeds (1 + 1/16) NG E with probability at most
B / ((1/256) NG E); the five bounds sum to P_cap <= 2^-32.0. All five caps below equal ceil(17/16 NG E).
unsuccessfully, and one group overshoot is charged. The run succeeds if some group succeeds and no counter
overflows: Pr >= 1 - exp(-NG q_lb) - P_cap >= 0.390000020 with NG = 276300940464239881006.
The exponential is bounded above by a degree-28 Taylor partial sum of e^lam (all terms positive), and
2^-101.5 is bounded below by 1.41421356 x 2^-102 (since 1.41421356^2 < 2); all arithmetic below is exact rationals.

## 8. Ledger

<!-- E:H7 -->
All counts are exact worst-case numbers of charged operations, except the caps (Section 7) and allowances.
Per group: M0 (2 rand + 32 extract + 16 store + 1 compression); Step-2/Y/Z0 per A0 (384 x 256); split searches: 256 A0 x 96 classes x
65536 L x 975 ops; candidate verification and validity: at most 3400000 ops per class (3584 x 320 + 3584 x 600 + 1792 halt checks = 3299072 <= 3400000); downstream at the caps: NT_MAX x 48 (W7 tests) + NW_MAX x 640 (row-17 cascade) +
N1_MAX x 8192 (rows 18..37 plus verify) + N2_MAX x 4 compressions, plus one group overshoot. Preprocessing:
H-index build 65536 x 19 ops plus data materialization 2^32 ops. Allowances 2^70 + 2^60 + 2^60.

| term | exact value |
|---|---|
| N_G groups | 276300940464239881006 = 2^67.9048 |
| per-group fixed ops | 1653908373559 = 2^40.5890 |
| downstream caps (ops) | NT 419459857161278015242975 / NW 28059570522995648480610 / N1 27401924338862937970 / N2 27401924338862937970 |
| preprocessing (ops) | 4297967296 |
| allowances (units) | 2^70 + 2^60 + 2^60 |
| **T (units)** | **2^97.08020** |
| certificate | T^100000 <= 2^9708020, tight (fails at 9708019) |
| **claimed time_log2** | **97.08020** |

The certificate inequality is verified by exact integer comparison (Appendix C script).

## 9. Memory, preprocessing and advice

Memory (bytes; every 32-bit value one per 32-byte word, nothing packed): H-index start array 65537 words =
2097184 + 65536 entry words = 2097152, index total 131073 words = 4194336; A2 list 768 words = 24576; A0 set
256 words = 8192; c9 table 96 words = 3072; CHAR/condition data under 1024 words = 32768; S* and pair under 512
words = 16384; candidate store 448 words = 14336; program code 2048 words = 65536; working state 2048 words =
65536; messages and randomness under 64 words = 2048. Exact total 138337 words = 4426784 bytes = 2^22.08 for the online attack with its counted
preprocessing and all author development (each itemized above).
Allowance memory (charged time, bounded here for completeness): the characteristic search ran on at most
10^5 CPU cores with at most 2^40 bytes each (cited CPU-ceiling chain), so at most 2^57 bytes (cited record, Appendix G); the Step-1
solve (published 2^38.3 calls, single-machine solver working set) at most 2^40 bytes envelope; cited
development (q3 studies, at most a few hundred MB per run) at most 2^29 bytes. Overall peak max(2^22.08,
2^56.6, 2^40, 2^29) < 2^57.
Claimed memory_log2_bytes = 57. The online attack itself uses 4.43 MB; the figure is dominated by the
one-time historical characteristic search, as is conventional (the cited lineage bounds allowance memory
only by the generic 32-bytes-per-operation rule).
Every author development computation peaks below 2^22 bytes of RAM (Section 12, Appendix D); no 2^32 working
set exists anywhere in this package (P-MAXFIBER). Preprocessing: 3000000 + 2^32 operations (unpacked index build actual 2950000 itemized: per-H count 21 and fill 22 x 65536 plus prefix sums; envelope 3000000) = 2^20.59 units;
claimed preprocessing_log2 = 70.00282. Advice: characteristic, S*, pair, A2/A0/c9 tables, 35840 + ~4 KB = about 40 KB total (bound 2^16);
claimed nonuniform_advice_log2_bytes = 16.

## 10. Heuristics

<!-- E:H4 -->
H1-single-trial-chaining-value (score-critical): Section 7 statement. Scope: counter expectations, per-variant
success, caps, N_G. Extrapolation: from measured chaining values to all groups; caps tolerate 6.25% above
expectation. Evidence: see claim.json heuristic entry.
Limitations: a premise; joint variant events are H5.
H2-variant-q3 (score-critical): Section 7 statement. Scope: per-group success rate. Extrapolation: Monte-Carlo
bounds to the full variant set; half-bit margin. Evidence: see claim.json heuristic entry.
Limitations: CLT-based bounds; q3 itself unobservable; rests on H1.
H4a-allowance-characteristic-search (score-critical): obtaining the published 38-step characteristic cost at
most A_C = 2^70 compressions (2^-27.2 of T; allowances are negligible at this total). Scope: allowance part. Extrapolation: hardware-ceiling and
measured-predecessor arguments restated from the cited packages. Evidence: see claim.json heuristic entry. Limitations: a bound,
not a measurement; sensitivity in Section 9 of the cited packages.
H4b-allowance-step1-solve (supporting): Step-1 solution cost at most A_S = 2^60 (2^-34.5 of T with DEV).
H4c-allowance-development (supporting): all development at most DEV = 2^60. Evidence: see claim.json heuristic entry.
H5-pairs-in-group (score-critical): Section 7 statement. Evidence: see claim.json heuristic entry. Limitations: budget premise.
H6-split-search-completeness (score-critical): Theorem S of Section 5. Scope: every examined (CV, A0, class).
Extrapolation: none (exact). Evidence: see claim.json heuristic entry.
Limitations: covers the search only, not variant validity or later rows.
P-MAXFIBER (supporting premise, dependency): phi(u) = s0(u) - u has max fiber 14 over all 2^32 inputs, so every
class holds at most 32 x 14 = 448 row-16 solutions and the program's halt at a 449th solution never triggers.
Established by the accepted r38 lineage: the promoted package 44cb527b (Th0rgal) ran the exhaustive preimage
count `ex1 phi` over all 2^32 inputs as its development and reports max fiber 14 (its proof memory section:
"the exhaustive passes at most 2^32 bytes (the preimage-count pass ex1 phi)"); the same fact underlies the
448-candidate bounds of 0ae69bcb/37742a53/012400ff. Used here only for the candidate bound; soundness of the
output does not depend on it (every output pair is recomputed before return, and a halt is a safe failure).
No 2^32 working set exists in this package: the H-index fiber check (at most 2 over 2^16 H, Appendix E) and
the |F7| count (streaming, Appendix E) are the only exhaustive passes here, both tiny. Cited record (44cb527b
proof): development includes "the independent C core (r38.h) with the exhaustive passes (ex1.c: A2 list, G,
|F7|, the preimage counts of phi)" and its memory section states "the exhaustive passes at most 2^32 bytes
(the preimage-count pass ex1 phi)", reporting max fiber 14; the same 448-candidate bound is used by
0ae69bcb/37742a53/012400ff.
H1-single-trial-chaining-value (score-critical): per group, M0 is a full uniform 512-bit first block
(16 fresh words); CV1 = F_38(IV, M0). Over the group coins (uniform M0, hence the reachable CV1 distribution,
plus uniform A0), (Y, Z0) is uniform and W7 lands in F7 with p2 = 2^-3.90197, by the Step-2 bijection (Lemma 4
of the accepted r38 lineage) composed with full-block spreading. For fixed CV1, A0 and variant every value is
deterministic; uniformity is over the group coins, never conditional on fixed values. Joint uniformity over
(Y, Z0, W7) is the cited Step-2 bijection argument; S1/S4 confirm its checkable marginals (W7 rate, Y/Z0 bins)
on fixed variants at N = 200000 each. The reachable-CV1 distribution is measured directly: author study S4
(N = 200000 full M0s through real compression) gives W7 rate 0.06627 in [0.060, 0.074] and all (Y, Z0) bins
in [0.247, 0.252] (band [0.235, 0.265]), with 0 CV1 collisions; the organizer run additionally records joint (W7,Y-half) bins against the independence prediction. Scope: counter expectations, per-variant
success, caps, N_G. Extrapolation: S4 + bijection to all groups; caps tolerate 6.25% above expectation.
Evidence: experiment:splitcheck (true-CV1 uniformity). Limitations: a premise; joint variant events are H5;
F_38 spreading of full blocks is measured (S4), not proved. The conditional row-17 pass rate
2^-10 (the 10-bit E17 mask as first test) is part of this premise: given W7 in F7, H1-uniformity makes the
10-bit mask pass with exactly 2^-10; consistent with the enriched-neighborhood co-pass data of Section 7
(29 in 300 near, 4 in 50 own-block). The N1/N2 caps use exactly this rate.
Characteristic-sufficiency edge (cited Lemma 7 of the accepted r38 lineage 44cb527b: "A(CV1, v) implies
F_38(CV1, M1) = F_38(CV1, M1'), hence a collision of M0 || M1 and M0 || M1' when CV1 = F_38(IV, M0); M1 != M1'
because W7 differs by d7"): a variant passing every row check yields equal second-block compressions on
distinct messages; every output pair is recomputed before return, so no invalid pair can be emitted even if
the edge were misread.
H7-counted-cost (score-critical): the per-line operation counts of Sections 5-6 and the ledger totals of
Section 8. Scope: all charged work. Extrapolation: none (deterministic program). Evidence: see claim.json heuristic entry;
experiment:splitcheck (window probes 1024 and trial-0 full probes 1048576 = 2^20 per class, as charged).
Limitations: none beyond machine match.
Removed premise: H3-table-pricing of the cited packages is dropped. This package reads no tables online; every
access is a direct computation and memory is 2^23 bytes, so no unit-cost-memory premise is needed.

## 11. Experiments

splitcheck (python-message-pairs-v1, experiments/splitcheck.py, full-collision event): per trial seed, d is
4 bytes of SHAKE-256(seed); the program checks the Table-5 pair equality, runs the split search over a
seed-placed 8-by-64 (H,L) window (1024 index probes: 64 L values x 16 low G values) verifying every returned u against a brute-force
enumeration of the same window, and on trial 0 verifies the H-index partitions all 65536 H values into correct
buckets plus a full-space soundness search (2^20 probes, every u verified). The per-L body runs through an
operation counter in Section 1 primitives on all 64 window L values per trial, asserting the charged bound of
975 on each (observed maxima near 830). Uniformity uses true first-block values (M0 of sixteen fresh words, CV1 by real compression, 32 per trial, A0 varying over the published set with Step-2 W7).
Returns the transcribed SFS pair
(not a full collision: CV differs from IV; full collisions 0). Hypothesis: full collisions 0, wmismatches 0,
wmatch true every trial; index_ok and mismatches 0 on trial 0. See experiments/manifest.json.

## 12. Author’s reduced studies (S1-S4)

Preregistered before the runs (methods, scales and decision rules in Appendix F; two amendments and one voided execution logged there with reasons). All four passed:
S1 (H1 uniformity, N = 200000 (CV, A0) pairs, fixed valid variant): W7 pass rate 0.06845, band
[0.060, 0.074] around p2 = 0.06689; (Y, Z0) low-bit bins all within [0.2487, 0.2529], band [0.235, 0.265].
S2 (reduced SMC, two independent 1024-variant sets from seeds 2 and 3, each 100% validity-rechecked
in-process at generation; 64 runs each, NP = 256, children 16/4/4/2/2/2, 128 tail pulls): aggregate log2
estimates -100.92 (4399 hits) and -100.93 (4362 hits), band [-105, -97] around -101, 64/64 replicates nonzero
in both sets, 0 failed rebuilds; 20/20 sampled rebuilt pairs re-verified with separate code (equal
compressions, distinct messages, rows 16..37 hold). Both match the cited full-scale means (-100.99875,
-101.00020) within 0.1 bits. An earlier S2 execution on a corrupted variants file (99% invalid entries from
mixed data sources) was voided and redone; see Appendix F.
S4 (H1 reachable distribution, N = 200000 full first blocks through real F_38 compression, fixed S* variant):
W7 pass rate 0.06627, band [0.060, 0.074] around p2 = 0.06689; (Y, Z0) low-bit bins all within [0.247, 0.252],
band [0.235, 0.265]; 0 CV1 collisions among 200000 outputs (band at most 3). The per-group analysis of
Section 7 therefore runs on the measured reachable distribution, not on an assumed uniform CV1.
S3 (condition-set consistency, exact): |G| = 32; table inventory exact; published pair satisfies every row
cell 16..37, all 41 two-bit conditions and the W8..W11 pairs, checked by independent code from the
transcription. These check the estimator machinery and the condition structure at reduced scale; the VALUE
q3_model = 2^-101.5 rests on the two cited full-scale preregistered studies plus this structural agreement.

## 13. Limitations

- q3 is estimated, not proved; the estimator, registration and runs are the cited packages’ (dependency).
- The pair budget, allowances and chaining-value uniformities are premises (H5, H4, H1).
- Memory 2^57 bytes overall (online attack 4.43 MB, no large table) but the attack remains far from practical (2^97.08 time).
- The experiment checks code consistency and transcription on organizer seeds, not full-scale success.
- The construction follows the cited public packages; the new part is the search, ledger and experiment.
- Cited packages’ review outcomes are their own; this package stands on its own evidence.

## Appendix A. Data

A.1 Row-16 set G (32 words):

```text
35f29010 35f29011 35f29014 35f29015 35f29410 35f29411 35f29414 35f29415
35f2b010 35f2b011 35f2b014 35f2b015 35f2b410 35f2b411 35f2b414 35f2b415
35fa9010 35fa9011 35fa9014 35fa9015 35fa9410 35fa9411 35fa9414 35fa9415
35fab010 35fab011 35fab014 35fab015 35fab410 35fab411 35fab414 35fab415
```

A.2 c9-classes (c9 value, then its 8 A2 values):

```text
79043aa9 379b4dc9 379b4dcd 37bb4dc9 37bb4dcd a79b4dc9 a79b4dcd a7bb4dc9 a7bb4dcd
79043aab 379b4dc8 379b4dcc 37bb4dc8 37bb4dcc a79b4dc8 a79b4dcc a7bb4dc8 a7bb4dcc
79045aa9 379b2dc9 379b2dcd 37bb2dc9 37bb2dcd a79b2dc9 a79b2dcd a7bb2dc9 a7bb2dcd
79045aab 379b2dc8 379b2dcc 37bb2dc8 37bb2dcc a79b2dc8 a79b2dcc a7bb2dc8 a7bb2dcc
7a8437a9 3a1b4cc9 3a1b4ccd 3a3b4cc9 3a3b4ccd aa1b4cc9 aa1b4ccd aa3b4cc9 aa3b4ccd
7a8437ab 3a1b4cc8 3a1b4ccc 3a3b4cc8 3a3b4ccc aa1b4cc8 aa1b4ccc aa3b4cc8 aa3b4ccc
7a843ba9 3a1b50c9 3a1b50cd 3a3b50c9 3a3b50cd aa1b50c9 aa1b50cd aa3b50c9 aa3b50cd
7a843bab 3a1b50c8 3a1b50cc 3a3b50c8 3a3b50cc aa1b50c8 aa1b50cc aa3b50c8 aa3b50cc
7a8457a9 3a1b2cc9 3a1b2ccd 3a3b2cc9 3a3b2ccd aa1b2cc9 aa1b2ccd aa3b2cc9 aa3b2ccd
7a8457ab 3a1b2cc8 3a1b2ccc 3a3b2cc8 3a3b2ccc aa1b2cc8 aa1b2ccc aa3b2cc8 aa3b2ccc
7a845ba9 3a1b30c9 3a1b30cd 3a3b30c9 3a3b30cd aa1b30c9 aa1b30cd aa3b30c9 aa3b30cd
7a845bab 3a1b30c8 3a1b30cc 3a3b30c8 3a3b30cc aa1b30c8 aa1b30cc aa3b30c8 aa3b30cc
7b043aa9 399b4dc9 399b4dcd 39bb4dc9 39bb4dcd a99b4dc9 a99b4dcd a9bb4dc9 a9bb4dcd
7b043aab 399b4dc8 399b4dcc 39bb4dc8 39bb4dcc a99b4dc8 a99b4dcc a9bb4dc8 a9bb4dcc
7b045aa9 399b2dc9 399b2dcd 39bb2dc9 39bb2dcd a99b2dc9 a99b2dcd a9bb2dc9 a9bb2dcd
7b045aab 399b2dc8 399b2dcc 39bb2dc8 39bb2dcc a99b2dc8 a99b2dcc a9bb2dc8 a9bb2dcc
7c8437a9 381b4cc9 381b4ccd 383b4cc9 383b4ccd a81b4cc9 a81b4ccd a83b4cc9 a83b4ccd
7c8437ab 381b4cc8 381b4ccc 383b4cc8 383b4ccc a81b4cc8 a81b4ccc a83b4cc8 a83b4ccc
7c843ba9 381b50c9 381b50cd 383b50c9 383b50cd a81b50c9 a81b50cd a83b50c9 a83b50cd
7c843bab 381b50c8 381b50cc 383b50c8 383b50cc a81b50c8 a81b50cc a83b50c8 a83b50cc
7c8457a9 381b2cc9 381b2ccd 383b2cc9 383b2ccd a81b2cc9 a81b2ccd a83b2cc9 a83b2ccd
7c8457ab 381b2cc8 381b2ccc 383b2cc8 383b2ccc a81b2cc8 a81b2ccc a83b2cc8 a83b2ccc
7c845ba9 381b30c9 381b30cd 383b30c9 383b30cd a81b30c9 a81b30cd a83b30c9 a83b30cd
7c845bab 381b30c8 381b30cc 383b30c8 383b30cc a81b30c8 a81b30cc a83b30c8 a83b30cc
99043aa9 879b4dc9 879b4dcd 87bb4dc9 87bb4dcd 979b4dc9 979b4dcd 97bb4dc9 97bb4dcd
99043aab 879b4dc8 879b4dcc 87bb4dc8 87bb4dcc 979b4dc8 979b4dcc 97bb4dc8 97bb4dcc
99045aa9 879b2dc9 879b2dcd 87bb2dc9 87bb2dcd 979b2dc9 979b2dcd 97bb2dc9 97bb2dcd
99045aab 879b2dc8 879b2dcc 87bb2dc8 87bb2dcc 979b2dc8 979b2dcc 97bb2dc8 97bb2dcc
9a8437a9 8a1b4cc9 8a1b4ccd 8a3b4cc9 8a3b4ccd 9a1b4cc9 9a1b4ccd 9a3b4cc9 9a3b4ccd
9a8437ab 8a1b4cc8 8a1b4ccc 8a3b4cc8 8a3b4ccc 9a1b4cc8 9a1b4ccc 9a3b4cc8 9a3b4ccc
9a843ba9 8a1b50c9 8a1b50cd 8a3b50c9 8a3b50cd 9a1b50c9 9a1b50cd 9a3b50c9 9a3b50cd
9a843bab 8a1b50c8 8a1b50cc 8a3b50c8 8a3b50cc 9a1b50c8 9a1b50cc 9a3b50c8 9a3b50cc
9a8457a9 8a1b2cc9 8a1b2ccd 8a3b2cc9 8a3b2ccd 9a1b2cc9 9a1b2ccd 9a3b2cc9 9a3b2ccd
9a8457ab 8a1b2cc8 8a1b2ccc 8a3b2cc8 8a3b2ccc 9a1b2cc8 9a1b2ccc 9a3b2cc8 9a3b2ccc
9a845ba9 8a1b30c9 8a1b30cd 8a3b30c9 8a3b30cd 9a1b30c9 9a1b30cd 9a3b30c9 9a3b30cd
9a845bab 8a1b30c8 8a1b30cc 8a3b30c8 8a3b30cc 9a1b30c8 9a1b30cc 9a3b30c8 9a3b30cc
9b043aa9 899b4dc9 899b4dcd 89bb4dc9 89bb4dcd 999b4dc9 999b4dcd 99bb4dc9 99bb4dcd
9b043aab 899b4dc8 899b4dcc 89bb4dc8 89bb4dcc 999b4dc8 999b4dcc 99bb4dc8 99bb4dcc
9b045aa9 899b2dc9 899b2dcd 89bb2dc9 89bb2dcd 999b2dc9 999b2dcd 99bb2dc9 99bb2dcd
9b045aab 899b2dc8 899b2dcc 89bb2dc8 89bb2dcc 999b2dc8 999b2dcc 99bb2dc8 99bb2dcc
9c8437a9 881b4cc9 881b4ccd 883b4cc9 883b4ccd 981b4cc9 981b4ccd 983b4cc9 983b4ccd
9c8437ab 881b4cc8 881b4ccc 883b4cc8 883b4ccc 981b4cc8 981b4ccc 983b4cc8 983b4ccc
9c843ba9 881b50c9 881b50cd 883b50c9 883b50cd 981b50c9 981b50cd 983b50c9 983b50cd
9c843bab 881b50c8 881b50cc 883b50c8 883b50cc 981b50c8 981b50cc 983b50c8 983b50cc
9c8457a9 881b2cc9 881b2ccd 883b2cc9 883b2ccd 981b2cc9 981b2ccd 983b2cc9 983b2ccd
9c8457ab 881b2cc8 881b2ccc 883b2cc8 883b2ccc 981b2cc8 981b2ccc 983b2cc8 983b2ccc
9c845ba9 881b30c9 881b30cd 883b30c9 883b30cd 981b30c9 981b30cd 983b30c9 983b30cd
9c845bab 881b30c8 881b30cc 883b30c8 883b30cc 981b30c8 981b30cc 983b30c8 983b30cc
b9043aa9 679b4dc9 679b4dcd 67bb4dc9 67bb4dcd 779b4dc9 779b4dcd 77bb4dc9 77bb4dcd
b9043aab 679b4dc8 679b4dcc 67bb4dc8 67bb4dcc 779b4dc8 779b4dcc 77bb4dc8 77bb4dcc
b9045aa9 679b2dc9 679b2dcd 67bb2dc9 67bb2dcd 779b2dc9 779b2dcd 77bb2dc9 77bb2dcd
b9045aab 679b2dc8 679b2dcc 67bb2dc8 67bb2dcc 779b2dc8 779b2dcc 77bb2dc8 77bb2dcc
ba8437a9 6a1b4cc9 6a1b4ccd 6a3b4cc9 6a3b4ccd 7a1b4cc9 7a1b4ccd 7a3b4cc9 7a3b4ccd
ba8437ab 6a1b4cc8 6a1b4ccc 6a3b4cc8 6a3b4ccc 7a1b4cc8 7a1b4ccc 7a3b4cc8 7a3b4ccc
ba843ba9 6a1b50c9 6a1b50cd 6a3b50c9 6a3b50cd 7a1b50c9 7a1b50cd 7a3b50c9 7a3b50cd
ba843bab 6a1b50c8 6a1b50cc 6a3b50c8 6a3b50cc 7a1b50c8 7a1b50cc 7a3b50c8 7a3b50cc
ba8457a9 6a1b2cc9 6a1b2ccd 6a3b2cc9 6a3b2ccd 7a1b2cc9 7a1b2ccd 7a3b2cc9 7a3b2ccd
ba8457ab 6a1b2cc8 6a1b2ccc 6a3b2cc8 6a3b2ccc 7a1b2cc8 7a1b2ccc 7a3b2cc8 7a3b2ccc
ba845ba9 6a1b30c9 6a1b30cd 6a3b30c9 6a3b30cd 7a1b30c9 7a1b30cd 7a3b30c9 7a3b30cd
ba845bab 6a1b30c8 6a1b30cc 6a3b30c8 6a3b30cc 7a1b30c8 7a1b30cc 7a3b30c8 7a3b30cc
bb043aa9 699b4dc9 699b4dcd 69bb4dc9 69bb4dcd 799b4dc9 799b4dcd 79bb4dc9 79bb4dcd
bb043aab 699b4dc8 699b4dcc 69bb4dc8 69bb4dcc 799b4dc8 799b4dcc 79bb4dc8 79bb4dcc
bb045aa9 699b2dc9 699b2dcd 69bb2dc9 69bb2dcd 799b2dc9 799b2dcd 79bb2dc9 79bb2dcd
bb045aab 699b2dc8 699b2dcc 69bb2dc8 69bb2dcc 799b2dc8 799b2dcc 79bb2dc8 79bb2dcc
bc8437a9 681b4cc9 681b4ccd 683b4cc9 683b4ccd 781b4cc9 781b4ccd 783b4cc9 783b4ccd
bc8437ab 681b4cc8 681b4ccc 683b4cc8 683b4ccc 781b4cc8 781b4ccc 783b4cc8 783b4ccc
bc843ba9 681b50c9 681b50cd 683b50c9 683b50cd 781b50c9 781b50cd 783b50c9 783b50cd
bc843bab 681b50c8 681b50cc 683b50c8 683b50cc 781b50c8 781b50cc 783b50c8 783b50cc
bc8457a9 681b2cc9 681b2ccd 683b2cc9 683b2ccd 781b2cc9 781b2ccd 783b2cc9 783b2ccd
bc8457ab 681b2cc8 681b2ccc 683b2cc8 683b2ccc 781b2cc8 781b2ccc 783b2cc8 783b2ccc
bc845ba9 681b30c9 681b30cd 683b30c9 683b30cd 781b30c9 781b30cd 783b30c9 783b30cd
bc845bab 681b30c8 681b30cc 683b30c8 683b30cc 781b30c8 781b30cc 783b30c8 783b30cc
d9043aa9 479b4dc9 479b4dcd 47bb4dc9 47bb4dcd 579b4dc9 579b4dcd 57bb4dc9 57bb4dcd
d9043aab 479b4dc8 479b4dcc 47bb4dc8 47bb4dcc 579b4dc8 579b4dcc 57bb4dc8 57bb4dcc
d9045aa9 479b2dc9 479b2dcd 47bb2dc9 47bb2dcd 579b2dc9 579b2dcd 57bb2dc9 57bb2dcd
d9045aab 479b2dc8 479b2dcc 47bb2dc8 47bb2dcc 579b2dc8 579b2dcc 57bb2dc8 57bb2dcc
da8437a9 4a1b4cc9 4a1b4ccd 4a3b4cc9 4a3b4ccd 5a1b4cc9 5a1b4ccd 5a3b4cc9 5a3b4ccd
da8437ab 4a1b4cc8 4a1b4ccc 4a3b4cc8 4a3b4ccc 5a1b4cc8 5a1b4ccc 5a3b4cc8 5a3b4ccc
da843ba9 4a1b50c9 4a1b50cd 4a3b50c9 4a3b50cd 5a1b50c9 5a1b50cd 5a3b50c9 5a3b50cd
da843bab 4a1b50c8 4a1b50cc 4a3b50c8 4a3b50cc 5a1b50c8 5a1b50cc 5a3b50c8 5a3b50cc
da8457a9 4a1b2cc9 4a1b2ccd 4a3b2cc9 4a3b2ccd 5a1b2cc9 5a1b2ccd 5a3b2cc9 5a3b2ccd
da8457ab 4a1b2cc8 4a1b2ccc 4a3b2cc8 4a3b2ccc 5a1b2cc8 5a1b2ccc 5a3b2cc8 5a3b2ccc
da845ba9 4a1b30c9 4a1b30cd 4a3b30c9 4a3b30cd 5a1b30c9 5a1b30cd 5a3b30c9 5a3b30cd
da845bab 4a1b30c8 4a1b30cc 4a3b30c8 4a3b30cc 5a1b30c8 5a1b30cc 5a3b30c8 5a3b30cc
db043aa9 499b4dc9 499b4dcd 49bb4dc9 49bb4dcd 599b4dc9 599b4dcd 59bb4dc9 59bb4dcd
db043aab 499b4dc8 499b4dcc 49bb4dc8 49bb4dcc 599b4dc8 599b4dcc 59bb4dc8 59bb4dcc
db045aa9 499b2dc9 499b2dcd 49bb2dc9 49bb2dcd 599b2dc9 599b2dcd 59bb2dc9 59bb2dcd
db045aab 499b2dc8 499b2dcc 49bb2dc8 49bb2dcc 599b2dc8 599b2dcc 59bb2dc8 59bb2dcc
dc8437a9 481b4cc9 481b4ccd 483b4cc9 483b4ccd 581b4cc9 581b4ccd 583b4cc9 583b4ccd
dc8437ab 481b4cc8 481b4ccc 483b4cc8 483b4ccc 581b4cc8 581b4ccc 583b4cc8 583b4ccc
dc843ba9 481b50c9 481b50cd 483b50c9 483b50cd 581b50c9 581b50cd 583b50c9 583b50cd
dc843bab 481b50c8 481b50cc 483b50c8 483b50cc 581b50c8 581b50cc 583b50c8 583b50cc
dc8457a9 481b2cc9 481b2ccd 483b2cc9 483b2ccd 581b2cc9 581b2ccd 583b2cc9 583b2ccd
dc8457ab 481b2cc8 481b2ccc 483b2cc8 483b2ccc 581b2cc8 581b2ccc 583b2cc8 583b2ccc
dc845ba9 481b30c9 481b30cd 483b30c9 483b30cd 581b30c9 581b30cd 583b30c9 583b30cd
dc845bab 481b30c8 481b30cc 483b30c8 483b30cc 581b30c8 581b30cc 583b30c8 583b30cc
```

A.3 A0 set (value and exact variant-set size):

```text
3662dd58 750798738 3662dd50 750798738 3662bd50 750798738 36629d50 750798738
36627d58 750798738 36627d50 750798738 36625d58 750798738 36625d50 750798738
36623d58 750798738 36623d50 750798738 36621d58 750798738 36621d50 750798738
3661fd58 750798738 3661fd50 750798738 3661dd58 750798738 3661dd50 750798738
3661bd58 750798738 3661bd50 750798738 36619d58 750798738 36619d50 750798738
36617d58 750798738 36617d50 750798738 36615d58 750798738 36615d50 750798738
36613d58 750798738 36613d50 750798738 36611d58 750798738 36611d50 750798738
3660fd58 750798738 3660fd50 750798738 b662dd50 750367881 b6629d50 750367881
b6625d50 750367881 b6623d50 750367881 b6621d58 750367881 b6621d50 750367881
b661fd50 750367881 b661dd50 750367881 b661bd50 750367881 b6619d50 750367881
b6617d50 750367881 b6615d58 750367881 b6615d50 750367881 b6613d58 750367881
b6613d50 750367881 b6611d58 750367881 b6611d50 750367881 b660fd58 750367881
b660fd50 750367881 3660bd58 749907870 3660bd50 749907870 b660bd50 749607325
3660dd58 749434566 3660dd50 749434566 366add58 749306678 366add50 749306678
366abd58 749306678 366abd50 749306678 366a9d58 749306678 366a9d50 749306678
366a7d50 749306678 366a5d58 749306678 366a5d50 749306678 366a3d50 749306678
366a1d58 749306678 366a1d50 749306678 3669fd50 749306678 3669dd58 749306678
3669dd50 749306678 3669bd50 749306678 36699d50 749306678 36697d50 749306678
36695d58 749306678 36695d50 749306678 36693d58 749306678 36693d50 749306678
36691d58 749306678 36691d50 749306678 3668fd58 749306678 3668fd50 749306678
3662dd56 749304379 3662dd4e 749304379 3662bd56 749304379 3662bd4e 749304379
36627d56 749304379 36627d4e 749304379 36625d4e 749304379 36623d56 749304379
36623d4e 749304379 36621d56 749304379 36621d4e 749304379 3661fd56 749304379
3661fd4e 749304379 3661dd56 749304379 3661dd4e 749304379 3661bd56 749304379
3661bd4e 749304379 36619d56 749304379 36619d4e 749304379 36617d56 749304379
36617d4e 749304379 36615d56 749304379 36615d4e 749304379 36613d56 749304379
36613d4e 749304379 36611d56 749304379 36611d4e 749304379 3660fd56 749304379
3660fd4e 749304379 3668bd50 749092986 b66add58 748997270 b66add50 748997270
b66abd50 748997270 b66a9d58 748997270 b66a9d50 748997270 b66a7d50 748997270
b66a5d58 748997270 b66a5d50 748997270 b66a3d58 748997270 b66a3d50 748997270
b66a1d58 748997270 b66a1d50 748997270 b669fd58 748997270 b669fd50 748997270
b669dd58 748997270 b669dd50 748997270 b669bd50 748997270 b6699d58 748997270
b6699d50 748997270 b6697d50 748997270 b6695d50 748997270 b6693d50 748997270
b6691d58 748997270 b6691d50 748997270 b668fd50 748997270 3662fd58 748982994
3662fd50 748982994 b6623d4e 748863932 b6621d4e 748863932 b661fd56 748863932
b661bd4e 748863932 b6617d56 748863932 b6617d4e 748863932 b6615d4e 748863932
b6613d56 748863932 b6613d4e 748863932 b6611d56 748863932 b6611d4e 748863932
b660fd56 748863932 b660fd4e 748863932 3662dd52 748706771 3662bd52 748706771
36627d52 748706771 36625d52 748706771 36623d52 748706771 36621d52 748706771
3661fd52 748706771 3661dd52 748706771 3661bd52 748706771 36619d52 748706771
36617d52 748706771 36615d52 748706771 36613d52 748706771 36611d52 748706771
3660fd52 748706771 36623d5a 748706531 3661fd5a 748706531 3661bd5a 748706531
36617d5a 748706531 36615d5a 748706531 36613d5a 748706531 36611d5a 748706531
3660fd5a 748706531 3668dd58 748617938 3668dd50 748617938 3662fd56 748515751
3662fd4e 748515006 3660dd4e 748497055 3660dd56 748496687 b668dd50 748328226
b6613d5a 748272092 b660fd5a 748272092 b6623d52 748271884 b6621d52 748271884
b661bd52 748271884 b6617d52 748271884 b6615d52 748271884 b6613d52 748271884
b6611d52 748271884 b660fd52 748271884 3662dd54 748258600 3662bd54 748258600
36627d54 748258600 36625d54 748258600 36623d54 748258600 36621d54 748258600
3661fd54 748258600 3661dd54 748258600 3661bd54 748258600 36619d54 748258600
36617d54 748258600 36615d54 748258600 36613d54 748258600 36611d54 748258600
3660fd54 748258600 3662dd4c 748258590 3662bd4c 748258590 36627d4c 748258590
36625d4c 748258590 36623d4c 748258590 36621d4c 748258590 3661fd4c 748258590
3661dd4c 748258590 3661bd4c 748258590 36619d4c 748258590 36617d4c 748258590
36615d4c 748258590 36613d4c 748258590 36611d4c 748258590 3660fd4c 748258590
36623d5c 748257912 3661bd5c 748257912 36617d5c 748257912 36615d5c 748257912
36613d5c 748257912 36611d5c 748257912 3660fd5c 748257912 366add56 748249397
366add4e 748249397 366abd4e 748249397 366a9d4e 748249397 366a5d4e 748249397
366a3d4e 748249397 366a1d4e 748249397 3669fd56 748249397 3669dd4e 748249397
3669bd4e 748249397 36697d56 748249397 36697d4e 748249397 36695d4e 748249397
36693d56 748249397 36693d4e 748249397 36691d56 748249397 36691d4e 748249397
3668fd56 748249397 3668fd4e 748249397 b660dd56 748149584 36631d58 748119330
36631d50 748119330 3660dd5a 748106455 3660dd52 748104487 3660bd56 748016615
3660bd4e 748016615 3668dd4e 747975479 3668dd56 747975119 366afd58 747959736
```

## Appendix B. Row-test conditions (transcribed with credit from 0ae69bcb experiments/vt38.py)

E-cell conditions rows 4..8 and 16,17 (mask, x-value, xor-diff, +-mask as 8 hex words each row):

```text
CHAR = dict(
 A={7:'=nu=============================',8:'=========n=====n====n======u====',11:'====================u=======un==',
    12:'=u===n====n======u===nu=======n=',13:'==n============n================',14:'====u=========nn========u==u====',
    15:'======n=u=======n===============',17:'==u============================='},
 E={5:'+++=============================',6:'+++=1====0==+1=====0+===1==1====',7:'uuu=0+1=11=0+00====1+===0==00=01',
    8:'100=u+010n=1nu01=01nu=00n11u1=01',9:'11000u1=n11u0000101101110=01u0uu',10:'==1010=01u00001u=010u=101==10111',
    11:'1=n000=0111100101unn00011+111u10',12:'01nuuu=110n111nu000100100+010u1n',13:'00110101110=000u00111nuu+nnnu1n1',
    14:'=010n0===00===1n=11+0100+1110001',15:'=1==1=1==0=1==11===+u011n1011=1=',16:'=u==10===n===+u1===n0=u=1==+====',
    17:'=0=====+00===+0=+==01=0=0==+====',18:'=0=====+01===n1=+==1==1===0u====',19:'==11===nn====1==n===010===11==0=',
    20:'==1====00====1==0==========1====',21:'==u====10=======1===10==========',22:'==0=============================',
    23:'==1============================='},
 W={7:'==n=============================',8:'=====u===u==========n===========',9:'==u=============================',
    10:'=====n=u=======n===n==n=n=n=u=u=',11:'============u======u=u==========',15:'=====u===n==========n===========',
    16:'==u=============================',23:'=====1=uu=====1=u=1=============',25:'==n============================='})
```

Plus-pair rule: for E row i, bits with E_i[b] = E_{i-1}[b] required are row(E,i)[3] & row(E,i-1)[3].
W8..W11 difference pairs (dxor, s0-diff): 043ff800 01808000; 20000000 fbc00800; fcfeed6a 10005f30;
00081400 03011296. W rows with cells: 7 (mask 04000000 area), 8, 9, 10, 11, 15, 16, 23, 25.
Two-bit conditions (kind1, row1, bit1, op, kind2, row2, bit2), 41 total:

```text
A 14 15 0 A 16 15
A 14 23 0 A 16 23
A 14 25 0 A 16 25
A 15 4 0 A 16 4
A 15 7 0 A 16 7
A 15 16 1 A 16 16
A 15 17 0 A 16 17
A 15 27 0 A 16 27
A 15 29 0 A 16 29
A 16 15 0 A 17 15
A 16 23 0 A 17 23
A 16 25 0 A 17 25
A 17 9 0 A 17 20
A 17 6 0 A 17 18
A 17 8 0 A 17 17
A 16 29 0 A 18 29
A 18 29 0 A 19 29
E 16 4 1 E 16 23
E 16 3 1 E 16 8
E 16 14 0 E 16 28
E 16 4 0 E 17 4
E 16 18 0 E 17 18
E 18 0 1 E 18 13
E 17 15 0 E 18 15
E 17 24 0 E 18 24
E 19 6 1 E 19 19
E 19 20 0 E 19 2
E 21 2 0 E 21 16
W 16 1 1 W 16 12
W 16 20 1 W 16 27
W 16 8 0 W 16 25
W 16 14 0 W 16 18
W 16 4 1 W 16 6
W 16 22 1 W 16 31
W 23 0 1 W 23 30
W 23 1 1 W 23 31
W 23 14 0 W 23 21
W 23 16 0 W 23 25
W 25 4 0 W 25 6
W 25 22 0 W 25 31
W 25 20 0 W 25 27
```

Row-17+ cascade order: E17 10-bit mask test; A17 4-bit plus internals; rows 18..37 E/A/W cells with
their TWOBIT entries; full two-message verification on pass (4 compressions: the two second blocks and the two padding blocks). Charged 512 ops per W7 pass,
8192 per row-17 pass, as bounded in Section 8.

## Appendix D. Allowance methodology (H4)

The allowances are conservative envelopes with the arithmetic shown, not measurements of the original
computations. All bounds below are exact integer arithmetic.

A_C = 2^70 (characteristic search). Allowance memory (bounded here, completing the 2^57 figure):
the characteristic search is a computation of others, a SAT/SMT search on at most 10^5 cores with at most 2^40
bytes each, so at most 2^57 bytes (cited lineage record, Appendix G); the Step-1 solve (published 2^38.3
compression-equivalent calls, single-machine solver working set) at most 2^40 bytes envelope (the instance is
kilobytes; solver search state orders below terabytes); development is the author work itemized here (below
2^22 bytes) plus the cited q3 studies (at most a few hundred MB per run, cited record, Appendix G), at most
2^30 bytes envelope including headroom. Overall peak max(2^22.08, 2^57, 2^40, 2^30) = 2^57 bytes. The 2^60 DEV
time margin covers human-time-bounded unmeasured work (minutes to hours of compute, megabytes of state), not
2^60-scale memory.
(i) CPU ceiling for the cited open-source CPU SAT/SMT solver class:
10^5 cores x 10 years (315360000 s) x 10^10 word operations per second = 315360000000000000000000 operations
= 2^78.06 operations = 2^66.65 units at C = 2728. A_C exceeds this ceiling 2^3.35-fold (10.2x). (ii) Measured
predecessor re-run (cited, organizer-accepted): 593858 solver CPU-seconds x 2^32.796 primitive operations per
solver CPU-second = 2^51.98 operations; x 32 blind-rediscovery factor = 2^56.98 operations = 2^45.57 units.
A_C exceeds it 2^24.43-fold. GPU throughput does not apply (CPU SAT/SMT solver).

A_S = 2^60 (Step-1 solve). The paper reports about 2^38.3 compression-equivalent calls for the 38-step Step-1
solve; A_S exceeds it 2^21.7-fold. Variant enumeration needs no solve (charged preprocessing P5).

DEV = 2^60 (all development). Envelope above: the cited q3 studies (R1: 1024 runs x 4000 particles; R2: 4096
runs; GPU batches 17 x 2^30 digests) at most 2^42 operations generously counted; the author's studies of
Section 12 (128 SMC replicates at NP = 256, uniformity and H5 measurements) at most 2^38 operations measured
by wall-clock (minutes on one core, about 2^36 word operations); exhaustive passes (|F7|, max fiber, A2 checks)
at most 2^36 operations; every author computation peaks below 2^22 bytes of RAM (F7 count O(1) state,
H-index table 2^17 bytes, phi-fiber external count at most 3.1 MB resident measured, SMC particles kilobytes,
tables transcribed); the A0/A2 tables transcribed from the cited lineage (verified here: 768/768 c9 values recomputed exactly, 256 sizes sum exactly to SR; peak RAM below 2^20 bytes). Total development compute is
below 2^44 operations = 2^32.6 units, so DEV = 2^60 carries a margin above 2^27.

## Appendix C. Ledger recomputation

The script below recomputes T and the certificate from the fixed integers (Python integers, exact).
It prints the claimed bound; the inequality is checked both ways (tight).

```python
from fractions import Fraction as F
from math import factorial
import math
C = 2728
SR = 191773672732
P2N, P2D = 287309824, 2**32
Q3N, Q3D = 141421356, 100000000 * 2**102
QLB = F(SR * P2N * Q3N, P2D * Q3D * 2)
NG = 276300922872053836590 + 2**44
E_NE = F(256 * 96 * 32, 1)
E_NT = F(SR * 32, 2**32)
E_NW = F(SR * 32 * P2N, 2**32 * P2D)
E_N1 = E_NW * F(1, 2**10)
E_N2 = E_NW * F(1, 2**10)
B = 3584 * 96 * 256
EPS = F(1, 16)
def pcap(E): return F(B, 1) / (EPS * EPS * NG * E)
def cap(E): return (F(17, 16) * NG * E).__ceil__()
PC = sum(pcap(E) for E in (E_NE, E_NT, E_NW, E_N1, E_N2))
lam = QLB * NG
s = sum((lam**k) / factorial(k) for k in range(29))
SUCC = 1 - F(1, 1) / s - PC
NE_MAX, NT_MAX, NW_MAX, N1_MAX, N2_MAX = (cap(E) for E in (E_NE, E_NT, E_NW, E_N1, E_N2))
STEP2 = 256 * 384
SEARCH = 256 * 96 * (65536 * 975 + 100)
VALID = 256 * 96 * 3400000
PER_GROUP = STEP2 + SEARCH + VALID + 55
OV = 88080384 * (48 + 640 + 8192 + 4 * C)
DOWN = NT_MAX * 48 + NW_MAX * 640 + N1_MAX * 8192 + N2_MAX * 4 * C + OV
PRE = 2**32 + 3000000
T = F(NG * PER_GROUP + DOWN + PRE, C) + 2**70 + 2**60 + 2**60 + NG
num, den = T.numerator, T.denominator
P = pow(num, 100000); Q = pow(den, 100000)
lo, hi = 9690000, 9730000
while lo < hi:
    mid = (lo + hi) // 2
    if P <= Q * pow(2, mid): hi = mid
    else: lo = mid + 1
k = lo
print('k =', k, 'up:', P <= Q * pow(2, k), 'tight:', P > Q * pow(2, k - 1))
print('T = 2^%.5f claim = %.5f success >= %.9f' % (math.log2(float(T)), k / 100000, float(SUCC)))
open('/tmp/ledger_out.json','w').write(__import__('json').dumps(
    {'NG': NG, 'CLAIM': k/100000, 'SUCC': float(SUCC), 'caps': [NE_MAX, NT_MAX, NW_MAX, N1_MAX, N2_MAX], 'k': k}))
```


## Appendix E. Exhaustive certificates (author-executed, exact code and output)

E.1 Method. Two exact enumerations run by the author in Rust (release build), each with peak RAM far below
2^22 bytes: |F7| by direct membership count over all 2^32 words, 16 threads, O(1) working state, 3.0 s
(F7 as in Section 3.2); the H-index fiber distribution over all 2^16 H, 64 KiB table, instant (P as in
Section 5). The phi max-fiber fact is NOT recomputed here: it is premise P-MAXFIBER (Section 10), established
by the accepted r38 lineage's exhaustive preimage count. No 2^32 working set exists in this package, in RAM
or on disk.

E.2 Programs (exact sources). F7 count: for every 32-bit w, count s0(w + 0x20000000) - s0(w) == 0x03bff800
(16-way split, one u64 counter each, summed). H-index check: for every 16-bit H, bucket P(H) = s0(H*2^16)
mod 2^16 in a 65536-byte table; report max occupancy and occupied count.

E.3 Output (verbatim):

```text
F7COUNT 287309824
PMAX 2 POCC 32768
```

E.4 Reading. |F7| = 287309824 exactly (p2 = 2^-3.90197 used in Section 7). The H-index has 32768 occupied
buckets of at most 2 entries, as charged in Section 5.

## Appendix F. Preregistration summary (author studies S1-S4)

F.0 S4 (registered here before the run; H1 reachable-distribution check). Method: draw N = 200000 full first
blocks M0 (16 fresh uniform words), compute CV1 = F_38(IV, M0) by real compression, then the Step-2 (Y, Z0)
and W7 exactly as the attack does, on the fixed S* variant. Record: (a) W7-in-F7 rate (expect p2 = 0.06689);
(b) (Y, Z0) low-16-bit 4-bins (expect 1/4 each); (c) pairwise CV1 collisions among the 200000 outputs
(expect ~0; documents first-block spreading). Pass bands (fixed now): (a) in [0.060, 0.074]; (b) all 8 bins in
[0.235, 0.265]; (c) at most 3 collisions. Reported as-is; a miss changes the H1 statement, not the numbers.

F.1 Registered before any run: S1 draws N = 200000 uniform (CV, A0) pairs and records W7-in-F7 rate
(pass band [0.060, 0.074] around p2 = 0.06689), (Y, Z0) low-bit bins (band [0.235, 0.265]), and a reduced
row-16 hit rate (band 0.8x-1.25x around 2^-12). S2 runs 64 independent reduced-SMC replicates (NP = 256,
children 16/4/4/2/2/2, 128 tail pulls) on a fixed 1024-variant set; pass if all complete, mean log2 estimate
in [-105, -97], and 0 failed rebuilds. S3 checks the condition-set inventory and the published pair exactly.
Decision: reported as-is; the package text changes only for failed bands (none failed).

F.2 Amendments (logged with reasons before the affected runs): (A1) S2 variant sets must be 100% validity-
rechecked in-process at generation (prompted by finding invalid entries in an early generator). (A2) a second
independent S2 set (seed 3) was added to test set-dependence. (V1) one S2 execution on a corrupted variants
file (99% invalid entries from mixed data sources, predating A1) was voided with cause and redone cleanly;
both clean sets agree within 0.1 bits.

F.3 Role. These studies check the estimator machinery and condition structure at reduced scale; the VALUE
q3_model = 2^-101.5 rests on the two cited full-scale preregistered studies plus this structural agreement.
F.4 S4 outcome (the run registered in F.0 above): N = 200000, W7 rate 0.06627, bins within [0.247, 0.252],
0 CV1 collisions. Pass on all three bands; no package text changed.
F.5 S2 replicate records (64 log2 estimates per set, 0 failed rebuilds in both; aggregate = log2 of the mean):

seed-2 set (4399 verified hits):
-100.9 -100.9 -102.1 -101.2 -100.8 -101.2 -101.3 -100.7 -100.4 -101.0 -100.4 -100.3 -100.9 -101.7 -100.6 -101.4 -100.7 -100.6 -101.1 -101.0 -100.5 -100.8 -101.1 -100.9 -100.6 -100.8 -100.8 -101.3 -101.2 -101.1 -100.6 -100.8 -101.2 -100.6 -100.3 -100.7 -100.7 -101.3 -101.2 -100.9 -100.9 -101.4 -100.6 -100.8 -101.2 -101.4 -101.1 -101.3 -101.0 -100.7 -101.5 -101.0 -100.5 -101.3 -100.9 -101.4 -100.9 -101.0 -101.3 -101.0 -101.1 -100.6 -100.9 -100.7

seed-3 set (4362 verified hits):
-100.7 -101.1 -102.2 -101.1 -100.8 -101.1 -101.5 -100.9 -100.6 -101.1 -100.7 -100.6 -101.0 -101.5 -100.8 -101.7 -101.0 -100.8 -101.2 -100.9 -100.3 -100.7 -101.4 -100.7 -100.7 -100.9 -100.9 -101.0 -100.9 -101.4 -100.8 -100.9 -101.2 -100.5 -100.5 -100.7 -100.6 -100.9 -101.0 -101.0 -101.2 -101.1 -101.0 -101.0 -101.4 -101.0 -101.2 -101.2 -100.7 -100.8 -101.2 -101.0 -100.4 -101.2 -101.2 -101.0 -100.9 -101.0 -100.7 -100.7 -101.5 -100.6 -101.0 -100.3


F.6 S2 per-run (hits/bad) records. Each of the 64+64 replicates reports verified hits and failed rebuilds
(checkable sums: 4399 and 4362 hits, 0 failures; aggregates recompute as log2 of the mean of 2^est from F.5).

seed-2 per-run hits/bad:
68/0 79/0 59/0 67/0 73/0 62/0 70/0 81/0 66/0 66/0 80/0 75/0 63/0 60/0 85/0 66/0 72/0 71/0 67/0 75/0 76/0 63/0 77/0 68/0 73/0 80/0 66/0 60/0 58/0 78/0 71/0 67/0 68/0 67/0 70/0 81/0 68/0 53/0 61/0 77/0 73/0 56/0 88/0 73/0 70/0 55/0 72/0 61/0 59/0 71/0 66/0 69/0 70/0 65/0 69/0 60/0 70/0 61/0 56/0 61/0 78/0 77/0 67/0 65/0

seed-3 per-run hits/bad:
76/0 65/0 56/0 68/0 71/0 66/0 61/0 69/0 61/0 60/0 62/0 62/0 61/0 65/0 72/0 52/0 59/0 64/0 62/0 76/0 89/0 67/0 62/0 78/0 72/0 75/0 61/0 72/0 70/0 66/0 65/0 65/0 67/0 72/0 61/0 82/0 72/0 70/0 70/0 73/0 57/0 68/0 67/0 64/0 63/0 69/0 67/0 65/0 75/0 64/0 81/0 70/0 73/0 69/0 59/0 77/0 74/0 63/0 84/0 71/0 60/0 79/0 63/0 83/0

Audit: 64+64 replicates all nonzero, totals 4399 and 4362 verified hits, 0 failed rebuilds in both sets; aggregates -100.92 and -100.93 recompute exactly from the F.5 estimates.

## Appendix G. Cited lineage records (verbatim excerpts, 44cb527b Th0rgal)

G.1 Sufficiency (premise H10). "**Lemma 7.** A(CV1, v) implies F_38(CV1, M1) = F_38(CV1, M1'), hence a collision of M0 || M1 and M0 || M1' when CV1 = F_38(IV, M0); M1 != M1' because W7 differs by d7."

G.2 Step-2 bijection (premise H1 structure). "**Lemma 4 (rows 16..22 do not depend on the variant).** Fix a valid v and let CV1 be uniform. Then (W0, ..., W7) is uniform on (2^32)^8 (Step-2 bijection, Section 3); conditioned on W7 in F7, (W0..W6) is ..." (uniform on the F7-conditioned set).

G.3 Exhaustive passes (premise P-MAXFIBER; allowance memory). "the independent C core (`r38.h`) with the exhaustive passes (`ex1.c`: A2 list, G, |F7|, the preimage counts of phi) and the exact |R_j| (`rcount.c`)". "The development computations that are charged through DEV used far less: the q3 studies at most a few hundred MB per run, the exhaustive passes at most 2^32 bytes (the preimage-count pass `ex1 phi`) ..." "The allowance A_C is a computation of others (a SAT/SMT search on at most 10^5 cores with at most 2^40 bytes each, 2^57 bytes)". The max-fiber-14 result is the output of the quoted preimage count; the same 448-candidate bound is used by 0ae69bcb/37742a53/012400ff. Source: intake artifact of the promoted r38 submission (review run 38122657682), file proof-numbered.md.
