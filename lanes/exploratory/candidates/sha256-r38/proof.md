# sha256-r38, the P8 two-block cost bound with the P1 claw found on a chaining-value-independent u-table (time_log2 81.0013, memory 2^27.92, score 88.9213)

This is a cost bound for the target sha256-r38-prefix-v1. It uses the characteristic P8 of dariolina's 1a695f0b (its cells, its 38-step semi-free-start pair and its accepted event), the two-block procedure of ePrint 2026/1120 as used in fb176310 and 9aaf71a2, and the **P1 claw** of the lineage 51613d1c / 09f6ba2d (a row-16 pass is a pair (a0, u) with F(a0) + P(u) in a fixed 160-word set). What is new here is **how the claws are found**: the lineage builds, for every chaining value, a table of 2^27 values F(a0) and scans all 2^32 words u against it; this filing observes that **P(u) = s0(u) - u does not depend on the chaining value**, keeps a table of words u keyed by P(u) (rebuilt only once per epoch of 2^16 chaining values, with a fresh random rotation r that makes the selection exactly uniform, Lemma S), and scans the 2^26 values a0 of the window W9 = [9 x 2^26, 10 x 2^26) of each chaining value against it. Because every u is available, the table is **dense** (one candidate per 32-bit target value), so one 256-bit bucket read finds 1.74 claws on average instead of 0.055, and the claw costs **49.60** word operations instead of 174.82. Everything the bound uses is defined, counted or derived in this file and in `experiments/utab38.py` (own code, standard library; P8 is read from the public proof of 1a695f0b as data; no code of another participant is executed). The records behind the inherited premises (registrations, per-seed values) are in Appendices P, Q, R and H.

Claim: **time_log2 = 81.0013** (N = 6,601,681,020,982,485,524,571,291,632 counted word operations at C = 2,728 per target compression; log2(N / C) = 81.0012641, charged rounded up). Success probability at least 0.39. **Memory 2^27.92 bytes**: the maximum over the counted phases (Section 10) is the signed search that found P8, measured by its author at most 248,000 KB = 2^27.92 (read as KiB, the author's convention for 279,720 KB = 286,433,280 bytes: 2^27.91998; as 1,000-byte units 2^27.886); the online table is 251,658,240 bytes and the full-scale online port peaks at 247,336 KiB = 2^27.9161, below it. Preprocessing 2^78.09276 (the lineage's allowances A_C = 2^78, A_S = 2^74, DEV = 2^70, unchanged, inside the time, Section 11). Score under hashsmash-scalar-tm-v1: 81.0013 + 7.92 = **88.9213**. `python3 experiments/utab38.py ledger` prints every number of the ledger; `selftest` runs the checks.

## 1. Target and output

SHA-256 steps 0..37 on every padded block, the standard IV once, FIPS 180-4 padding, feed-forward, all eight digest words. The procedure outputs two distinct 128-byte messages m = M0||M1 and m' = M0||M1' with a common first block M0 (FIPS padding appends the same third block).

**Lemma 1.** Let cv = F_38(IV, M0). If the second-block computations of M1 and M1' from cv end with equal state words A34..A37, E34..E37, the digests of m and m' are equal. *Proof:* the second-block output is cv plus (A37, A36, A35, A34, E37, E36, E35, E34), and the third block is the same for both. m != m' because M1 and M1' differ in W7. Every output is therefore a collision of the target.

## 2. Data and the P1 pair

- **P8 (1a695f0b, transcribed as data).** The 38-step semi-free-start pair (PCV, PMX, PMY), the cells of rows 7..37 (`CELLS`: for A, E, W the mask of fixed bits, their values and the XOR difference), the '+' pairs (`PQE`, the printed pairs except E18 = E17 at row 18) and the two-bit conditions (`X2`). S denotes the state words of the pair: A2..A15 and E6..E15 of member x (= PMX) and member y (= PMY). The program checks that PCV, PMX, PMY reproduce the pair and that step 3b accepts it (Section 12).
- **The P1 pair.** For a chaining value cv and two free words a0, a1, both members take A0 = a0, A1 = a1, A2..A15 and E6..E15 from S; E0..E5 and W0..W15 follow from the step equations (`variantW_P1`). W10..W15 are S's words; W0..W9 depend on (cv, a0, a1); W0..W6 and E0..E5 are equal in the two members. With a0 = A0, a1 = A1 and cv = PCV this is the P8 pair.
- **Row 16.** W16 = s1(W14) + W9 + s0(W1) + W0, so E16 of member x is E16x = C16 + W0 + s0(W1). From the step equations of steps 0 and 1, W1 = u := a1 + h(a0, cv) and W0 + C16 = F(a0) - u with F(a0) := Cc2 + a0 + k0(cv) + h(a0, cv) (Cc2 = 0x7af32e15; k0, h are written out in `cv_consts`, `hfun`), hence **E16x = F(a0) + P(u), P(u) := s0(u) - u**. S160 is the set of 160 words that pass every row-16 cell and condition of P8: the 20 heads `R16H` (all equal mod 2^13: head j is R16H[0] + 2^13 t_j with 20 distinct t_j < 2^19) plus the 8 offsets OFFS = {0, 1, 4, 5, 1024, 1025, 1028, 1029} (bits 0, 2, 10 free). A **claw** is a pair (a0, u) with F(a0) + P(u) in S160; every claw is a row-16 pass of member x, and a1 = u - h(a0, cv).
- **Post-filters.** For a claw, on the words of the two members: C1: W8y - W8x = D8 (tested as: the top three bits of E5 = a1 + cE5 are 101); C2: s0(W9y) - s0(W9x) = D9s; G: s0(W8y) - s0(W8x) = T8; F7: s0(W7y) - s0(W7x) = F7d (W9y - W9x = D9 and W7y - W7x = D7 always). The constants are those of the P8 pair. C1, C2 read only a1; G reads (a0, a1); F7 reads (a0, a1, cv[0]). A **good pair** is a claw passing all four. The counted chain (`postfilters` in utab38.py: the folded segments of 6, 22, 29, 31 operations of the lineage's A.31, each ending with its counter add) equals these definitions evaluated on the real words (`pf_ref`): 0 mismatches on every claw of every organizer trial and of the selftest.

## 3. The procedure: the u-table

### 3.1 The table and the epoch

The table has **15 columns x 2^19 rows of buckets**, each bucket **one 256-bit word** (15 x 2^19 x 32 = 251,658,240 bytes). A bucket holds **six 42-bit lanes** (6 x 42 = 252 <= 256) and, in bits 252..255, the number of filled lanes:

```
lane L (bits 42L .. 42L+41) = [u: 32 bits][field: 6 bits][spare: 4 bits];   field = tag in 0..7 (filled) or 15 (empty)
```

An **epoch** draws one fresh word from the procedure's random source and takes **r** (13 bits, uniform in [0, 2^13)) and **ustart** (32 bits) from it. For a word u let G(u) = P(u) - r (mod 2^32). u is **covered** iff G(u) mod 2^13 < 120; its bucket is column (G mod 2^13) >> 3 (0..14), row G >> 13 (19 bits), and its tag is G mod 8. The loader resets every bucket to the empty word (every field 15, count 0) and then inserts u = ustart + n (mod 2^32), n = 0 .. 2^32 - 1: a covered u is written into the first empty lane of its bucket if fewer than six are filled, and dropped otherwise. The bucket therefore keeps the **first six covered words in the cyclic order starting at ustart** (the arc law of the lineage's H7, now on words u).

**Exact counts (exhaustive, Section 13).** P is balanced mod 2^13: each of the 8192 residues has exactly 2^19 preimages (`pbal.c`, all 2^32 words). Hence exactly 120 x 2^19 = 62,914,560 words are covered in every epoch, 8 per bucket on average. Over **all 8192 values of r**, the number of retained entries lies in **[44,436,632, 44,543,396]** (mean 44,485,887.33, i.e. 5.6567 filled lanes per bucket; `fillr2.c`, all 2^32 words for each of the 8 residues of r mod 8 and every column offset). This is the bucket-population law of a near-Poisson(8) count capped at six: the bucket counts of P follow the Poisson(8) histogram closely (Section 13).

### 3.2 The scan of one chaining value

For each a0 in W9 = [9 x 2^26, 10 x 2^26), in order:

1. F = F(a0) and y = Hr - F, where Hr = R16H[0] - r is computed once per chaining value.
2. A claw (a0, u) requires G(u) = y + 2^13 t_j + o for a head j and an offset o in OFFS (Lemma C). Writing o = o' + 1024 win with o' in {0,1,4,5}, the low 13 bits of the target are those of yw + o' with yw = y + 1024 win, the same for all 20 heads. The procedure computes q = (y + 5) mod 1024; if q >= 125 no target can be covered and the a0 is done. Otherwise v = ((y + 5) >> 10) mod 8; window win = 0 is probed iff v = 0, window win = 1 iff v = 7; otherwise the a0 is done. At most one window probes.
3. **Probe of a window.** z = yw mod 2^13, c = z >> 3, w = z mod 8, row0 = yw >> 13; the word WB carries 16 - w in every lane's field. For each head j, rowj = (row0 + t_j) mod 2^19, and the procedure reads
   - the **main bucket** (column c, row rowj) if c < 15, testing for tags t with t - w in {0,1,4,5};
   - the **next bucket** if w >= 3: (column c + 1, row rowj) if c + 1 < 15, or (column 0, row rowj + 1 mod 2^19) if c = 1023 (the target crosses into the next 2^13 frame); its test is for tags t with t + 8 - w in {1,4,5}.
4. **The six-lane test** of a bucket word d: Z = ((((d + WB) AND MASK) XOR CONST) + K) AND G, with MASK = bits 1, 3, 4 of every field, CONST = bit 4 (main) or bit 3 (next bucket) of every field, K = 31 in every field, G = bit 5 of every field. **Lemma B'** (below): lane L fires (its bit 5 of Z is 0) iff its field is a filled tag t with t - w in {0,1,4,5} (main) or t + 8 - w in {1,4,5} (next). If Z != G the procedure walks the six lanes and, for each fired lane, reads u (shift, and) and runs the post-filter chain on (a0, u, F); a good pair runs step 3b (the tests of rows 16..21 of both members, then the comparison of the eight output words; Lemma 1); if it accepts, the procedure outputs m, m' and halts.

**Lemma B' (the test is exact).** In each field, r = t + 16 - w with t in 0..7 or 15 and w in 0..7 lies in [9, 31]: the add never leaves the 6-bit field. For t <= 7: t - w in {0,1,4,5} iff r in {16, 17, 20, 21} iff (r AND 0b11010) = 0b10000; t + 8 - w in {1,4,5} iff r in {9, 12, 13} iff (r AND 0b11010) = 0b01000 (r = 8 is impossible). For t = 15, r = 31 - w in [24, 31] has bits 3 and 4 set, so it never equals either constant: an empty lane never fires. x = (r AND MASK) XOR CONST <= 26, so x + 31 <= 57 < 64 sets bit 5 exactly when x != 0, and no carry leaves the field; the u bits and the count bits are cleared by the AND. `probe_exhaustive` executes the 256-bit test on words with random u fields for every kind, w and tag (2,304 lane checks, 0 mismatches; organizer trial `utab-online-r38` 5). QED

**Lemma C (completeness and uniqueness).** For a chaining value, an epoch's table and an a0, the scan outputs exactly the pairs (a0, u) with u retained and F(a0) + P(u) in S160, each once. *Proof.* F + P(u) = R16H[j] + o iff G(u) = y + 2^13 t_j + o (because R16H[j] = R16H[0] + 2^13 t_j and G = P - r). A retained u has G mod 2^13 < 120; with o = o' + 1024 win and z = yw mod 2^13, (z + o') mod 2^13 < 120 forces (z + 5) mod 2^13 < 125, i.e. (y + 5 + 1024 win) mod 2^13 < 125, which is v = 0, q < 125 for win = 0 and v = 7, q < 125 for win = 1 (the two cannot both hold); so step 2 skips only a0 without claws. If z + o' < 2^13 the target lies in column c + [w + o' >= 8] of row (row0 + t_j) mod 2^19 (adding 2^13 t_j does not change the low 13 bits) with tag (w + o') mod 8; the main bucket holds the offsets with w + o' <= 7 (tag t, t - w = o'), the next bucket those with w + o' >= 8 (t = w + o' - 8, t + 8 - w = o' in {1,4,5}), which needs w >= 3; if z + o' >= 2^13 (z >= 8187, c = 1023) the target is in column 0 of row rowj + 1. Uncovered columns hold no entry, so skipping them loses nothing. By Lemma B' a lane fires exactly for these targets. Each retained u sits in exactly one lane, the 160 targets are distinct, so each claw is output once. QED

The organizer trials compare the claw list with an independent search (`ref_claws`: every retained entry indexed by its low 13 bits of G and matched against the 8 low patterns y + o, high part in the 20 t_j) and rebuild the real E16 of member x of every claw: EQUAL and 0 bad on every trial (Section 12), at the binding geometry and at full-frame coverage.

### 3.3 Lemma S: the selection is exactly uniform

**Lemma S.** For every word u, Pr_r[u covered] = 120/8192 exactly, whatever u, the chaining values and a0 are. *Proof.* G(u) mod 2^13 = (P(u) - r) mod 2^13 and r is uniform on [0, 2^13) and drawn independently of everything else. QED

So the covered set is a uniformly random 120/8192 thinning of the 2^32 words, the same for every u; no condition on u, W1 or E16 is imposed by coverage. The only non-uniform effect is **retention** (at most six of the about eight covered words of a bucket are kept); its law is H7 (claim.json): over ustart, whether a covered u is retained depends on the positions of the bucket's covered words in the cyclic order (the arc law), i.e. on the bucket's population and its arc gaps, never on the claw or its post-filter words. Note also that for a fixed r all covered words lie in 120 of the 8192 classes of P(u) mod 2^13; the exact uniformity of Lemma S holds averaged over r, and the success argument (Section 7) uses only that average. H7 is the premise that the acceptance of a good pair is independent of its u's coverage class and retention, averaged over (r, ustart).

### 3.4 Pseudocode

```text
input: N_CV, K = 2^16, V_MAX.  V = 0 (a register: the online operations executed so far)
for e = 1 .. ceil(N_CV / K):                                   # an epoch
    if V > V_MAX: halt (failure)
    draw one random word: r (13 bits), ustart (32 bits)
    reset the 15 x 2^19 buckets to EMPTY; for n = 0 .. 2^32-1: u = ustart + n; insert u (Section 3.1)
    V += the epoch's counted work
    for j = 1 .. K:                                            # a chaining value
        if V > V_MAX: halt (failure)
        draw M0 (16 random words); cv := F_38(IV, M0); the claw scalars of cv; Hr = R16H[0] - r
        V += C + 76 + 2^26 x 35                                 # this chaining value's fixed work
        for a0 in W9: step 1, step 2 (V += 7 when q < 125), probe (V += the probe's counted work), claws (each
                      post-filter segment adds its own cost to V); a good pair runs step 3b; if it accepts: output, halt
halt (failure)
```

The procedure draws only its own first blocks; each costs one compression plus the 76 operations of the chaining value's setup (the lineage's cv_begin 75 plus Hr), inside the fixed part. No other first-block enumeration is executed, so none is charged.

## 4. Pricing (H5')

collision-frontier-v5, 256-bit word RAM, the unit costs of the lineage: load, store, add, sub, and, or, xor, not, shift, immediate, random word 1; compare-and-branch 2; S0, S1, s0, s1 8; CH 3; MAJ 4 (the folded forms below use 2); address 1; one target compression C = 2,728. Every work-counter add (V += k) is one operation and is counted. Word arithmetic on the 32-bit quantities of SHA-256 (adds, sigmas, the scan counter u = ustart + n) is priced as in the lineage, one operation per 32-bit add or logical operation, with the reduction mod 2^32 part of the operation (the convention of the cost model's reference count C, a scalar 32-bit data path). `scan_cv` and `build_table` charge every operation below through the counter `Mach`; the itemisation is the one in the code.

| segment | operations |
|---|---|
| per word u of an epoch: u = ustart + n 1, s0 8, sub 1, - r 1, and 8191 1, loop 3, covered? branch 2 | 17 |
| covered and inserted: column, row, index (shift, add) 4, address + load 2, count 1, full? 2, lane (and, shift, or) 3, lane shift and clear mask from constant tables 2 + 2, and, shift, or, count add 4, address + store 2 | +22 |
| covered and dropped (bucket full) | +9 |
| reset, per bucket (address + store 2, loop 3); epoch setup (random word, split, V add, cap test) | 5; 6 |
| per chaining value: compression C, setup 76 (the lineage's cv_begin 75: first-block words 30, claw and post-filter scalars 38, random word 1, V add 1, cap test 2, loop 3; Hr 1) | C + 76 |
| per a0: a0 1, loop 3, F 26 (E0 1, S0 8, MAJ 2, S1 8, CH 2, F 5: the lineage's line), y 1, q (add, and) 2, branch 2 | 35 |
| per a0 with q < 125 (probability 125/1024): v (shift, and) 2, V add 1, two branches 4 | +7 |
| per probing window: yw 1, s 2, row0 1, c 2, w 1, WB (sub + broadcast) 8, the three path flags 6, two column bases 3, V add 1 | 25 |
| per head: rowj (add t_j, and) | 2 |
| per bucket read: address + load 2, add 1, and 1, xor 1, add 1, and 1, compare-and-branch 2 | 9 |
| lane walk of a read (charged on **every** read, a bound: six lanes x (and 1 + branch 2)) | 18 |
| frame-crossing next bucket: row + 1 (add, and) | +2 |
| per claw: u (shift, and) 2; post-filter chain 6 + 22 x [C1] + 29 x [C1 C2] + 31 x [C1 C2 G] (`postfilters` in utab38.py, each segment ending with its V add; a1 is formed inside the chain); step 3b on a good pair 3,014 | 2 + chain |

Step 3b is charged at its longest path, 3,014 operations (every test passing, counted by `selftest` on the P8 pair). The 256-bit word test of a bucket is five word operations; rotations and the s0 of the scan are the lineage's 8-operation sigma; nothing is bitsliced.

## 5. The ledger

**Per a0 (expectations under H1, Section 6).** y = R16H[0] - r - F(a0) is uniform (F(a0) is uniform for a uniform chaining value: cv[7] enters k0 additively and nothing else), so Pr[q < 125] = 125/1024 and Pr[a window probes] = 2 x 125/8192 = 250/8192. Given a probing window, s = (yw + 5) mod 2^13 is uniform on [0, 125): the main read happens for s >= 5 (120 of 125 values), the next-bucket read for 75 of 125 values (w >= 3 with c <= 13: 14 x 5, plus the 5 frame-crossing values s < 5); so a probe makes 20 x 195/125 = **31.2 reads**, 20 x 5/125 = 0.8 of them frame-crossing.

- probe = 25 + 20 x 2 + 31.2 x (9 + 18) + 0.8 x 2 = **909** operations (the lane walk charged on every read).
- claws per a0 = 160 x E / 2^32, E the number of retained entries (Lemma C and H1: each of the 160 targets is a uniform word independent of the table): **1.655394** at E = 44,436,632 (the least over r: used for success) and **1.659371** at E = 44,543,396 (the largest: used for cost).
- per claw: 2 + (6 + 22/8 + 29 x 53,096,854/2^32 + 31 x 57,726,359,870,197/2^58) + q_pf x 3,014 = 2 + 9.114723 + 0.040380 = **11.155103**.
- **per a0 = 35 + 0.854492 + (250/8192) x 909 + 1.659371 x 11.155103 = 82.105424** operations; per claw 82.105424 / 1.655394 = **49.599** (the lineage: 174.822 per claw, scan and filters, its A.31).

**Per chaining value.** wbar = C + 76 + 2^26 x 82.105424 = **5,510,004,523.8** (an upper bound of the mean work of a chaining value for every table, because the claw term uses the largest E over r and the lane walk is charged on every read). The maximum work of one chaining value: every a0 probes, every head makes two reads (frame-crossing included), every one of the 40 x 6 lanes fires and every claw reaches step 3b: vmax = C + 76 + 2^26 x (35 + 7 + 25 + 20 x (2 + 2) + 40 x (9 + 18) + 240 x (2 + 6 + 22 + 29 + 31 + 3,014)) = **50,075,761,904,372**.

**Per epoch.** build = 6 + 15 x 2^19 x 5 + 2^32 x 17 + E x 22 + (62,914,560 - E) x 9 <= **74,199,060,826** at the largest E: 0.0206% of an epoch's 2^16 chaining values.

| quantity | value |
|---|---|
| N_CV (Section 7) | 1,038,325,756,764,626,587 |
| epochs ceil(N_CV / 2^16) | 15,843,593,700,633 |
| V_MAX = epochs x build + ceil((1 + 2^-16) x N_CV x wbar) | 5,722,442,495,002,867,685,052,165,836 |
| allowances (2^78 + 2^74 + 2^70) x C | 879,238,525,979,567,763,757,203,456 |
| OVER = vmax (one chaining value at its maximum) | 50,075,761,904,372 |
| FIN = 6 C + 1,600 (the two digests of m, m' and their comparison) | 17,968 |
| **N** | **6,601,681,020,982,485,524,571,291,632** |
| **time_log2 = log2(N / 2,728)** | **81.0012641, charged 81.0013** |

**Lemma 2 (the cap).** The cap test reads V at the start of every epoch and of every chaining value; at that moment V equals the online work executed so far. An epoch build started with V <= V_MAX adds at most build <= vmax, a chaining value at most vmax. Hence the executed online work is at most V_MAX + vmax for every execution.

**Lemma 3 (cap halt).** Condition on the tables of all epochs. The epoch builds are then fixed and total at most epochs x build. The works W_j of the chaining values are independent (H1: fresh first blocks; the table is fixed), 0 <= W_j <= vmax and E[W_j | tables] <= wbar for every table. The procedure halts at a cap test only if the sum of the W_j exceeds (1 + 2^-16) N_CV wbar; Var(W_j) <= vmax wbar, so Bernstein's inequality gives a probability at most exp(-2^-32 N_CV wbar / (2 vmax (1 + 2^-16/3))) = exp(-13,300) < 2^-19,000, for every set of tables, hence unconditionally. No variance premise beyond H1 and the deterministic bound vmax is used.

## 6. The post-filter law q_pf (H1-P1)

Exact counts over all 2^32 values (own exhaustive program of the lineage): P(C1) = 1/8; |C1 and C2| = 53,096,854 (C1, C2 read only a1); for a0 in W9 the (a1 in C1 and C2)-summed count of G is 57,726,359,870,197, so P(C1 C2 G) = 57,726,359,870,197 / 2^58; |F7| = 287,309,824. Hence q_pf = 57,726,359,870,197 x 287,309,824 / 2^90 = 2^-16.1877.

**Why these rates bind the claws of the u-table (derived from H1).** For a uniform chaining value, F(a0) = Cc2 + a0 + k0 + h(a0) contains -cv[7] once (in k0) and h(a0) contains -cv[6] once (cv[6] enters k0 only through CH(e, f, g), inside F): so F(a0) and h(a0) are uniform and independent, and cv[0] is uniform given both. The table is fixed by the epoch, the claw's u depends only on F(a0) and the table, so **a1 = u - h(a0) is uniform and independent of the claw event**; C1 and C2 (a1 only) pass at the exact rates; every a0 of W9 has the same expected claw count (y is uniform for every a0), so the G rate of a claw is the W9-summed count above; and W7 = KK7c + MAJ(A2, a1, a0) - CH(E6, E5, E4) with KK7c = E7 - 2 A3 - cv[0] + ... is uniform given (a0, a1), so F7 passes at |F7|/2^32 (the lineage's statement "F7, averaged over a uniform chaining value, has probability |F7|/2^32 for any law of (a0, a1)"). H1-P1 is the premise that these rates hold for the claws the procedure finds; under H1 it is a consequence, and it is measured at full scale: the C port (Section 13) on seven chaining values, 778,357,004 claws, pooled C1 0.124995 (exact 1/8), C2|C1 2^-3.3380 (exact 2^-3.3379), G|C1C2 2^-5.9437 (exact 2^-5.9478), F7|C1C2G 0.0812 (|F7|/2^32 = 0.0669). F7 reads cv[0] and is strongly overdispersed across chaining values (per-chaining-value good-pair counts 605 to 2,495 on equal claw counts), so seven chaining values do not resolve its mean; the lineage's 24-chaining-value panel pooled 0.06618 (Appendix H.1), and the charge uses the exact |F7|/2^32, which holds in expectation over a uniform chaining value as derived above.

## 7. Success probability

Let X_j be the number of good pairs of chaining value j that step 3b accepts, and q3r the probability that a good pair is accepted.

- **H2-P1.** q3r >= q3_P1 x 2^32 / 160 = 2^-71.4010, q3_P1 = 2^-96.0791 = q3_model x 2^min(0, D_LB): q3_model = 2^-96.0133 is the registered accepted-event rate of the A0-variant good pairs before row 16 (Pr[row 16] = 160/2^32), and D_LB = -0.0658 is the registered one-sided 99% lower bound of the paired difference between the P1 family **on the window W9 = [9 x 2^26, 10 x 2^26)** and the A0-variant family (Section 9). This procedure scans exactly W9, so the measured window is the scanned one; no window-transfer premise is used (the lineage's H10 for W11 is not needed).
- **Expectation over the epoch's coins.** Averaged over (r, ustart) and the chaining value, E[X_j] = 2^26 x (160 E-bar / 2^32) x q_pf x q3r, where E-bar is the mean retained count (Lemma C, Section 6, H2-P1 and H7, which states that acceptance is independent of the coverage class and the retention of u when averaged over (r, ustart)); every table has E >= 44,436,632 (the least over all r), which the bound uses. The argument below needs only this average E[p] over tables, not a per-table statement.
- **Within a chaining value (H3-P1).** For a fixed chaining value and table the scan is deterministic and complete (Lemma C): X_j = J, the number of accepted good pairs among all claws of the chaining value. **H3-P1** (Section 8) gives E[J(J-1)] <= 2^-7.5 E[J]; Bonferroni gives Pr[X_j >= 1 | table] >= (1 - 2^-8.5) E[X_j | table].
- **Across chaining values and epochs.** Given its table, the chaining values of an epoch are independent (H1), and the epochs are independent (fresh r, ustart, first blocks). Let p(T) = Pr[X_j >= 1 | T]. Then Pr[an epoch has no success] = E_T[(1 - p(T))^K] <= E_T[exp(-K p(T))] <= 1 - K E[p] + K^2 E[p^2] / 2 <= 1 - K E[p] (1 - K p_max / 2), with p_max any bound on p(T) valid for every table. **The per-table bound is derived, not assumed (Lemma T).** Let a(u) be the acceptance probability of a good pair with W1 = u, averaged over the uniform chaining value and a0 (H1). Let a-bar = 2^-32 sum over all words u of a(u), the average acceptance of good pairs with uniform u, which is the quantity H2-P1 measures. Under H1 every retained word of a table T is equally likely to be the u of a claw (y is uniform), so the acceptance averaged over the good pairs of T is q3*(T) = (1/|U_T|) sum over u in U_T of a(u). Since a(u) >= 0 and |U_T| >= 44,436,632 for every table, q3*(T) <= 2^32 a-bar / |U_T| <= 2^6.595 a-bar. The expected number of good pairs of a chaining value is at most 2^26 x 160 x (6 x 15 x 2^19) / 2^32 x q_pf = 2^10.62 for every table, so p(T) <= 2^10.62 x 2^6.595 a-bar. H2-P1 bounds a-bar from below by q3r = 2^-71.40. For the second-order term it is used only in the weak upper form a-bar <= 2^10 q3r = 2^-61.40 (declared in H2-P1). The one-sided 99% upper readings of the same registered runs (level -96.1964, ratio +0.5959, paired difference +0.0416) give 2^-95.559 x 2^32 / 160 = 2^-70.88, about 9.5 bits inside it. Hence K p_max <= 2^16 x 2^10.62 x 2^6.595 x 2^-61.40 = 2^-28.18, the second-order factor is at least (1 - 2^-29), and the ledger charges (1 - 2^-25). Pr[an epoch has no success] <= exp(-K E[p] (1 - 2^-25)), with E[p] >= (1 - 2^-8.5) x 2^26 x 1.655394 x q_pf x q3r =: lambda.
- **Bound.** N_CV is the least integer with 1 - exp(-N_CV lambda (1 - 2^-25)) - 2^-60 >= 0.39 (exponentials at 90 digits): N_CV = 1,038,325,756,764,626,587, run as ceil(N_CV / 2^16) full epochs (the extra chaining values of the last epoch only add success). With Lemma 3, Pr[output a collision] >= 0.39 - 2^-19,000 >= 0.39 (the 2^-60 term absorbs it; `ledger` prints 0.39000000000000000015).

## 8. H3-P1: group independence within a chaining value

**Statement (the form of the accepted 44870635, H5-group-independence, applied to good pairs).** Good pairs of one chaining value that share no endpoint (neither a0 nor u) are independent trials of the accepted event, each with the probability q3r of H2-P1; good pairs sharing an endpoint form a group, of which one is counted. Consequence used: E[J(J-1)] <= 2^-7.5 E[J].
**Derivation of the consequence.** With K good pairs per chaining value (E[K] = 2^26 x 1.659 x q_pf = 2^10.54 here; 2^15.92 in the lineage's scan) and independent trials of probability q3r, E[J(J-1) | K] = K(K-1) q3r^2 and E[J | K] = K q3r, so E[J(J-1)] / E[J] = q3r E[K(K-1)] / E[K]. K varies with the chaining value only through F7 (C1, C2, G do not read cv); with the measured per-chaining-value spread of the good-pair count (Appendix H: E[K^2]/E[K]^2 = 1.246), E[J(J-1)]/E[J] <= q3r E[K] x 1.246 = 2^-60.5, below 2^-7.5 by a factor 2^53; groups (pairs sharing an endpoint) only lower J. In the u-table scan two claws of one chaining value can share a0 (distinct u) or u (distinct a0); both are endpoint groups of the statement.
**Support (Appendix H, the lineage's C port of the counted claw, 24 seed-drawn chaining values, 2^22 scan words each).** Good pairs sharing an endpoint: 0 of 2124. Across chaining values (dispersion chi-square of the per-value counts against the pooled binomial rate, 23 degrees of freedom): C2|C1 (chi-square 27.3, p = 0.24) and G|C1C2 (chi-square 22.5, p = 0.49) are binomial; F7|C1C2G is overdispersed (chi-square 564.0, p = 1.6e-104), as F7 reads the chaining value, and that spread is the factor 1.246 above; C1 is mildly overdispersed (chi-square 45.9, p = 0.003) because, in the lineage's scan order, claws of nearby scan words share u's high bits. **Measured on components of the accepted event (registered, Appendix H.2).** Part B of the 10-17 registration, run on 10-21: the forced-bit events B_t = ((E_t^x & m_t) == v_t) of rows 17..21, computed on the real compressions of both members of every good pair of one chaining value and of 100 good pairs of each of 200 chaining values. **The registered verdict was DEPENDENCE DETECTED (max |z| 3.77)**, and the population deviated from the registration: ONE had 17,576 good pairs, not the registered 20,000, because the chaining value has no more. The 3.77 and 3.63 come from the registered test (ii), z = (n1 - n2)/sqrt(n1 + n2), which compares raw counts and assumes equal sizes; with N1 = 17,576 and N2 = 20,000 it measures the size difference (E19: 2,244/17,576 = 0.1277 against 2,504/20,000 = 0.1252, rates that agree). The rate comparison, z = (n1/N1 - n2/N2)/sqrt(p(1-p)(1/N1 + 1/N2)), is **post hoc** (not registered): |z| at most 1.57. The registered tests (i) (each count against N p_t: largest |z| 2.43 for ONE, 1.58 for MANY) and (iii) (dispersion of E19, E20, E21 across the 200 chaining values: chi-square 205.2, 190.2, 193.3 on 199 dof, two-sided p 0.734, 0.680, 0.798) show no dependence. We read the registered detection as an artefact of test (ii) under unequal sizes, and report it as registered. The consequence used by H3-P1 holds with a margin of 2^53 (above), so even a large within-chaining-value correlation of these components would not change the bound. Not testable at any sample size and the premise: independence of the rows 17..37 event between good pairs of one chaining value (distinct (W0, W1); acceptance is a function of the pair's W0..W15).

## 9. The q3 of the P1 good pairs (H2-P1)

**The base q3_model = 2^-96.0133** (the A0-variant family on P8, 9aaf71a2): the sum of two one-sided 99% lower bounds, each computed by the rule registered before its run, on real step-0..37 compressions with disjoint seeds: (i) the level of the printed-cell accepted event: 128 fresh seeds (7001..7128) of 2^28 samples, per-seed value L_s = prefix log2 + log2(exact/2^28), mean -96.3123, sd 0.5563, registered bound mean - t(0.99, 127) sd / sqrt(128) = -96.42816; (ii) the ratio of the relaxed accepted event (the printed row-18 relation E18 = E17 not imposed) to that event: 400 seeds (10001..10400), G = log2(sum Xk / sum X0) = 0.50537, jackknife SE 0.03867, registered bound G - 2.34 SE = 0.41488. Sum -96.01328, rounded down to -96.0133; by the union bound the sum holds with confidence at least 98%. Registrations, method and every per-seed value: Appendix Q (per-seed values) and Appendix R.1 (the two runs as recorded in 9aaf71a2).

**The P1 family, measured (registered, paired).** The same tool (`traillab`, the lineage's own C) with the late words W8, W9 drawn from a list of P1 good pairs (a0 uniform in W9 = [9 x 2^26, 10 x 2^26) conditioned on G, a1 uniform over the 53,096,854 values with C1 and C2, W9 = cW9 - a1 and W8 set together) instead of the A0-variant list, on the same seeds as the level run (i): a seed's prefix lineage does not depend on the late words, so each seed gives a paired difference Delta_s = L_s(P1) - L_s(A0). Registered statistic: D = mean Delta_s, D_LB = D - t(0.99, n-1) sd / sqrt(n).

| run (registration) | a0 window | seeds | D (bit) | sd(Delta) | D_LB (99%) | EXACT P1 / A0 |
|---|---|---|---:|---:|---:|---:|
| **R9 (PREREG_P1_Q3_R9, 2026-10-21; declared)** | [9 x 2^26, 10 x 2^26) = W9, this package | 36 (7001..7036) | -0.0121 | 0.1321 | **-0.0658** | 367,978 / 372,469 |
| A25 (PREREG_P1_Q3, 2026-10-17; partial, reported) | [0, 2^25) | 76 (7001..7076) | +0.0022 | 0.1347 | -0.0345 | 780,313 / 782,236 |

Every diagnostic is 0 in every seed of both runs. The package charges q3_P1 = q3_model + min(0, D_LB(R9)) = -96.0133 + (-0.0658) = **-96.0791**, so q3r = 2^-96.0791 x 2^32 / 160 = 2^-71.4010; the confidence of the product of the three registered bounds is at least 97% (union bound). Both families run the same step-3b predicate on S's words W10..W15 and differ only in the law of W0..W9. **The good pairs of the u-table have the measured law:** a0 is every value of W9 (each with the same expected claw count), a1 is uniform and independent of the claw event (Section 6), and the post-filters condition (a0, a1) exactly as the list does; the chaining value is uniform (H1). The one difference is that a good pair's u = W1 is a retained table word: coverage is an exactly uniform thinning (Lemma S) and retention is the arc law of H7, which is the premise that the acceptance does not depend on how many covered words share the bucket of the pair's u.

**Two inherited transfer premises, stated explicitly (part of H2-P1).** (a) *Relaxation transfer.* q3_model is the printed-cell level (-96.42816) plus the gain of the relaxed accepted event (E18 = E17 not imposed, +0.41488), and that gain was measured on the A0-variant family (ratio run F2, Appendix R.1). The paired R9 difference D_LB was measured on the printed-cell event, with E18 = E17 imposed (the 10-17 Part A event, unchanged for R9). Charging q3_model + D_LB therefore assumes that the relaxation gain is the same for the P1 family. The 10-17 registration states this as an assumption (Appendix P, Section 1 of PREREG_P1_Q3); the lineage's filings carried it in the same form. The stated support is that the gain comes from the prefix lineages of rows 17..21 and the tail rows 22..37, which the two families share, and that on the printed event the families differ by only D = -0.0121 (sd 0.1321, 36 seeds). It is not measured on the P1 family. If the gain were entirely absent for P1, time_log2 would rise by about 0.37. (b) *List law.* The R9 list draws a1 uniform over the 53,096,854 C1 and C2 values and then a0 uniform in W9 conditioned on G by rejection, so its a1 marginal is uniform on C1 and C2. In the u-table's good pairs, (a0, a1) is uniform on the joint set (a0 in W9, a1 in C1 and C2, G), which weights a1 by its G count n(a1), the number of a0 of W9 passing G for that a1. Premise: q3 does not depend on this re-weighting of a1. The G count enters only through W8 = cW8 - E40 - chx, a word whose difference is fixed by T8 in both laws.

## 10. Memory (H6) and advice

**Online.** The table is 15 x 2^19 x 32 = 251,658,240 bytes; the epoch state (r, ustart, n), the chaining value's state (M0, cv, the claw scalars, Hr, WB, the masks), the post-filter and step-3b working state (two traces, about 6 KB) and the program are a few KB. The full-scale C port of the epoch build and the scan (`dev/utab/utab.c`, gcc -O3, glibc, the table one anonymous mmap of exactly 251,658,240 bytes in the packed 32-byte format of Section 3.1) peaked at **247,336 KiB = 253,272,064 bytes = 2^27.9161** (getrusage ru_maxrss of two runs, each an epoch build over all 2^32 words followed by three and four chaining values of 2^26 a0: 247,332 and 247,336 KiB; Section 13).

**Preprocessing and advice (inherited, the lineage's Section 10 and Appendix R).** The computations behind the advice, as measured by their author (1a695f0b Section 11, quoted in R.4): the signed search that found P8 at most **248,000 KB = 2^27.92**; the Step-1 solve of P8, re-measured on the byte-identical CNF as two sequential processes at 49,228 KiB = 2^25.5872 (R.5; the author's overlapping 279,720 KB sample is replaced by that measurement of the same computation, as the lineage did and as the track accepted); the class descriptors 2^25.14; the condition tables and the pair below 2^24. The lineage's attempt to replace the signed-search figure by a lower-memory re-run was refused by the board because the re-runs produced other sign assignments (R.6), so the author's 2^27.92 stands and is the largest counted cell. **Every execution of this filing is inside 2^27.92**, whether or not the procedure reads its output: the online port `utab.c` 247,336 KiB, the H7 instrument `h7.c` 247,400 KiB, `fillr2.c` 66,916 KiB, `pbal.c` and the Python experiments and selftest under 41 MB. Superseded first builds of the table-law count (one 2^29-byte array) and of the H7 instrument (255,080 KiB) were re-run within the cell with byte-identical outputs, and their numbers are not used. In particular, the development executions that produce data the procedure uses are below it: `p8fam` 69,496 KiB (R.3), and the table-law counts of Section 13, which fix the constants E_LO, E_HI behind N_CV: `fillr2.c` computes them in slices of 2^26 one-byte counters and peaks at 66,916 KiB = 2^26.03 (ru_maxrss, Section 13; a first, unsliced version used one 2^29-byte array and is superseded by `fillr2.c`, whose output is identical), and `pbal.c` uses 32 KiB. The exhaustive post-filter counts (|C1 and C2|, the W9 G count, |F7|) are the lineage's, used unchanged with the lineage's status. The q3 measurements are evidence for H2, not phases of the procedure (R.3 (c3)).

**The claim is memory_log2_bytes = 27.92 = max(online 2^27.9161, preprocessing 2^27.92).** The preprocessing cell rests on the author's report (R.4): the signed search that found P8 was re-run single-threaded, sequentially, sampled every 0.2 s, at most 248,000 KB (Python 152,868 KB and Kissat 80,816 to 88,096 KB resident together); the premise (H6) is that the search's runs are sequential and each within that figure, as the author's report states for the computation behind P8. Advice inventory (bytes): A2..A15 and E6..E15 of both members, 48 words, 192; the cells of rows 16..21 (54 words) 216, their '+' pairs (6 words) 24 and the 35 two-bit conditions 140; the 20 heads 80 and the 20 t_j 80; 19 post-filter and claw constants 76; K and IV (46 words) 184; the lane masks 4 x 32 = 128: in all 1,120 bytes, under 2^11, inside the declared 2^13.

## 11. Allowances and development (H4a, H4b, H4c)

A_C = 2^78 (the characteristic search behind P8), A_S = 2^74 (its Step-1 solve) and DEV = 2^70 (all development) are the lineage's charged allowances, **unchanged**: upper bounds charged in full, preprocessing = log2(2^78 + 2^74 + 2^70) = 78.09276, 13.3% of N. Their support is the lineage's (Appendix R.2 Part A, the basis of A_C = 2^78: the published and measured costs of the same kind of search, all at most 2^39.15 units, and the margin left for the dense characteristic of [LZLLQZ26], whose search has no log; R.4: the author's own report of under 2^21 core-seconds for the search for P8, S, its class data and all its development). **DEV** covers the lineage's recorded development (at most 68 threads and one GPU for 17 days: under 2^56.7 compressions), the A0-variant line's (R.3, below 2 x 10^5 CPU-seconds) and this filing's development (one 4-vCPU machine for under two days: under 2^40 x 4 x 2^17.4 = 2^59.4 operations = 2^48 compressions, including the exhaustive table-law counts and the full-scale ports of Section 13), in all under 2^57.1 compressions, inside 2^70. **Sensitivity (not claimed):** with A_C = A_S = DEV = 2^60 the same ledger gives 80.7951 (`ledger-reduced`).

## 12. Checks

- `selftest`: the S-pair constants; |S160| = 160; step 3b on the P8 pair accepts in 3,014 operations; the six-lane test against its scalar definition (Lemma B', 2,304 lane checks, 0 mismatches); two binding-geometry runs and two full-frame runs: claws EQUAL the independent search, every claw's real E16 of member x in S160 at the head and offset the scan named, post-filter flags equal the real-word definitions; retention (first six in insertion order) and the empty-lane marking on forced buckets; the counted scan operations at most the itemised charge of Section 4; the ledger and the success bound.
- Organizer experiment `utab-online-r38` (reduced size, not success-probability evidence): trials 0..3 draw a chaining value, r and ustart from the seed, build the binding-geometry table from 2^17 consecutive words u, and scan 2^17 consecutive a0 of W9 with the counted procedure including step 3b on every good pair; every claw is checked against the independent search (`claws_equal_ref`), by rebuilding the real E16 (`claw_e16_bad = 0`), and by evaluating the post-filters on the real words (`postfilter_ref_mismatch = 0`); a pair is returned only if step 3b accepts (none is expected at this size). Trial 4 runs step 3b on the P8 pair (accepts, 3,014 operations); trial 5 executes Lemma B' exhaustively.
- Organizer experiment `utab-rows-r38`: trials 0..3 use full-frame coverage (every scanned u covered, both windows probed; 2^15 words, 2^12 a0) so that claws are frequent, check them as above, and apply the tests of rows 16..21 of step 3b to both members of every claw (cumulative counts rows_le16..rows_le21; rows_le16 = claws). Trial 4 runs step 3b on the P8 pair.

## 13. Full-scale development record of the u-table

Own C, gcc 13.3 -O3 on a 4-vCPU Linux machine; the constants are generated mechanically from `utab38.py` (no transcription). Not executed by the procedure; they measure its table law and its full-scale behaviour.

- `pbal.c` (all 2^32 words): **P mod 2^13 class sizes: min 524,288, max 524,288** (every residue has exactly 2^19 preimages).
- `fillr2.c` (all 2^32 words for each residue of r mod 8, counted in eight slices of 2^26 windows; every one of the 8192 values of r evaluated; peak resident set 66,916 KiB per process): **retained entries over all r: min 44,436,632, max 44,543,396, mean 44,485,887.327 (5.6566731 per bucket; min 5.6504100)**. Bucket populations of P over the aligned 8-windows (r = 0, all 2^29 windows): 0: 170,225; 1: 1,371,786; 2: 5,556,846; 3: 14,984,836; 4: 30,290,332; 5: 48,918,563; 6: 65,681,868; 7: 75,456,084; 8: 75,636,913; 9: 67,273,527; 10: 53,694,267; 11: 38,863,425; 12: 25,710,985 (Poisson(8) x 2^29: 180,100; 1,440,801; 5,763,204; 15,368,544; 30,737,088; 49,179,341; 65,572,455; 74,939,949; 74,939,949; 66,613,288; 53,290,630; 38,756,822; 25,837,881; P is slightly less dispersed than Poisson, which raises the retained count above the Poisson value 8 x 2^29 x E[min(X,6)]/E[X] = 5.6500 per bucket).
- `utab.c` (the packed 32-byte table of Section 3.1, the epoch build over all 2^32 words, then 2^26 a0 of W9 for each chaining value, every claw's E16 = F + P(u) checked in S160 at the scan's head and offset, operations counted with the charges of Section 4):

```text
epoch r=663 ustart=ff5baf92 entries=44486246 dropped=18428314 per-bucket=5.656719
cv 0: probes/a0=0.030517 buckets/probe=31.2007 fired/probe=25.4504 claws=111218584 claws/a0=1.657286 bad=0 ref=111218584 c1=13890777 c12=1373597 c12g=22522 all4=1878
cv 1: probes/a0=0.030512 buckets/probe=31.2130 fired/probe=25.4558 claws=111210310 claws/a0=1.657163 bad=0 ref=111210310 c1=13917832 c12=1375844 c12g=22336 all4=1719
cv 2: probes/a0=0.030514 buckets/probe=31.2052 fired/probe=25.4494 claws=111205388 claws/a0=1.657089 bad=0 ref=111205388 c1=13902865 c12=1374425 c12g=22226 all4=2301
maxrss_kib=247332 table_bytes=251658240
epoch r=2093 ustart=a026297d entries=44475137 dropped=18439423 per-bucket=5.655306
cv 0: ops/a0=78.818552 (lane walk on fired reads only; on every read: 81.967389) probes/a0=0.030512 buckets/probe=31.1977 fired/probe=25.4644 claws/a0=1.656662 bad=0 c1=13886233 c12=1374061 c12g=22456 all4=2040
cv 1: ops/a0=78.760512 (on every read: 81.912121) probes/a0=0.030514 buckets/probe=31.1996 fired/probe=25.4616 claws/a0=1.656690 bad=0 c1=13902142 c12=1375273 c12g=22268 all4=605
cv 2: ops/a0=78.864541 (on every read: 82.017365) probes/a0=0.030522 buckets/probe=31.2108 fired/probe=25.4722 claws/a0=1.657092 bad=0 c1=13905183 c12=1373327 c12g=22353 all4=2495
cv 3: ops/a0=78.803355 (on every read: 81.954230) probes/a0=0.030518 buckets/probe=31.1988 fired/probe=25.4628 claws/a0=1.656441 bad=0 c1=13885935 c12=1374723 c12g=22150 all4=1653
maxrss_kib=247336 table_bytes=251658240
```

The measured claws per a0 equal 160 x E / 2^32 for the table's own E (1.657286 at E = 44,486,246: 160 x 44,486,246 / 2^32 = 1.657216; 1.656662 at E = 44,475,137: 1.656803); probes per a0 0.030517 against 250/8192 = 0.030518 and reads per probe 31.20 against 31.2. The counted operations per a0 with the lane walk on every read average 81.963 over the four chaining values against the ledger's 82.105 (the port's counter omits the V add of step 2, 0.122 per a0, which the ledger charges; the ledger's claw term uses the largest E over r; single chaining values scatter by about 0.05 around the mean, from the probe count and from the step-3b term, whose good-pair rate is overdispersed through F7). `ref` counts every lane of every probed bucket that matches a target by direct comparison of G; it checks the lane test, not completeness across buckets (completeness is Lemma C, and the organizer trials and `selftest` check it against an independent search over all retained entries). The port evaluates the six lanes of a bucket one by one with the scalar predicate of Lemma B'; the packed 256-bit test itself is executed by `utab38.py` (`probe_exhaustive`, trial 5 of `utab-online-r38`). Pooled over the seven chaining values: 778,357,004 claws, 0 bad; C1 97,290,967 (0.124995), C1C2 9,621,250, C1C2G 156,311, all four 12,691.

**H7 measured on acceptance components (`h7.c`, Appendix D: `utab.c` plus a one-bit overflow mark per bucket, kept in a spare lane bit, and, for every claw, the real trace of member x through step 21).** Two further epochs (r = 138 and r = 5651), three chaining values each, 2^26 a0 per chaining value: 667,218,763 claws (0 bad) and 9,185 good pairs. For every claw the forced-bit events B_t = ((E_t^x & m_t) == v_t) of rows 17..21 (the value cells of E17..E21, rates 2^-7, 2^-7, 2^-3, 2^-5, 2^-4, the events of the registered Part B, Appendix H.2) are counted, split by whether the claw's bucket had at most six covered words (every covered word retained: retention probability 1) or more than six (retention below 1, the arc law acting):

```text
                         n             E17       E18       E19        E20       E21
claws, population <= 6   179,561,482   1,402,272 1,404,217 22,448,093 5,607,695 11,226,649
claws, population  > 6   487,657,281   3,811,338 3,808,966 60,956,690 15,237,408 30,479,422
good pairs, pop <= 6     2,457         24        20        336        71        157
good pairs, pop  > 6     6,728         48        61        882        199       451
```

z against the expected rate, claws: E17 -0.47 / +0.78, E18 +1.18 / -0.44, E19 +0.66 / -0.06, E20 -1.54 / -0.49, E21 +1.25 / +0.16 (population <= 6 / > 6); between the two groups (two-proportion z): -0.80, +1.24, +0.59, -1.07, +0.99. Good pairs, between the groups: +1.27, -0.42, +0.71, -0.17, -0.53 (against the expected rate at most |z| = 1.76). Retention (the bucket's population, which sets the retention probability of its words) shows no association with these acceptance components at the 10^-4 level for claws (relative standard error of the E19 rate 2 x 10^-4) and none detectable for good pairs; the rates are also those of the lineage's Part B on uniformly drawn good pairs. This tests H7 on the shallow rows 17..21 only; the deep event is not measurable. The instrument's peak resident set is 247,400 KiB (the two runs: 247,400 and 247,140 KiB), inside the memory cell. A first build that kept the population in a separate 7.9 MB array peaked at 255,080 KiB. It was replaced by this build, which produces byte-identical counts on the same seeds; the first build is not a phase of the procedure and produced no data the procedure reads.

## 14. What changed against the lineage, and credits

The parent is 09f6ba2d (sraiw, 90.7274) on 51613d1c (newjordan, 90.7352): their P1 claw predicate, post-filter chain (A.31 folds), step 3b, q3 evidence (H2-P1 with the R9 run), H3-P1 and the records of Appendices P, Q, R, H are used unchanged. Their seven-lane bucket table over 2^27 candidates a0 of W9 and W11, rebuilt for every chaining value and scanned with all 2^32 words u, is **replaced** by the u-table of Section 3: built once per epoch from the chaining-value-independent P(u), dense (every word is a candidate), scanned with the 2^26 a0 of W9 only. Consequences: per claw 49.60 operations instead of 174.82; the W11 window and its transfer premise (H10), the side array, the fused resolver (H9) and the empty-lane chain law (H8) are gone (an empty lane cannot fire, Lemma B'); the claw selection is exactly uniform (Lemma S). The memory is the inherited preprocessing cell 2^27.92 instead of the lineage's online table 2^28.0447. The allowances are the lineage's, unchanged. The superseded appendices of the lineage (A.13 to A.31, the packed-slot and seven-lane machines) are not reproduced: the costs this filing takes from them (the folded post-filter segments 6, 22, 29, 31 of the lineage's A.31) are re-derived in `postfilters` of utab38.py and itemised in Section 4.

## Appendix A. The ledger, term by term

| term (operations) | value |
|---|---|
| allowances (A_C + A_S + DEV) x C = (2^78 + 2^74 + 2^70) x 2,728 | 879,238,525,979,567,763,757,203,456 |
| epoch builds, 15,843,593,700,633 x 74,199,060,826 (charged at the largest E) | inside V_MAX |
| online work cap V_MAX (charged in full; includes the N_CV first blocks and every epoch build) | 5,722,442,495,002,867,685,052,165,836 |
| overshoot OVER (one chaining value at its maximum) | 50,075,761,904,372 |
| final verification FIN = 6 C + 1,600 | 17,968 |
| **N** | **6,601,681,020,982,485,524,571,291,632** |

N / C = 2^81.0012641; charged 81.0013; score 81.0013 + 7.92 = 88.9213.

## Appendix D. The development sources of Section 13 (not shipped as experiments; reproduced so the full-scale measurements can be audited)

Built with `gcc -O3 -march=native`; `consts.h` is the output of `gen_h.py`. `fillr2.c` is run once per residue j = 0..7 and its eight outputs S_j[c] are combined as retained(8m + j) = sum over c = m .. m+14 of S_j[c mod 1024].

### `utab.c`: the full-scale port of the epoch build and the scan (Section 13; the r = 663 run used the same file without the operation counters)

```c
// utab.c - full-scale development port of the u-table claw machine (sha256-r38, P8/P1 claw), own code.
// usage: utab <seed> <ncv> [ref] ; builds one epoch table over all 2^32 u, then scans a0 in W9 for ncv chaining values.
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>
#include <sys/mman.h>
#include <sys/resource.h>
#include "consts.h"
#define M32 0xffffffffu
static inline uint32_t ror(uint32_t x,int n){return (x>>n)|(x<<(32-n));}
static inline uint32_t S0(uint32_t x){return ror(x,2)^ror(x,13)^ror(x,22);}
static inline uint32_t S1(uint32_t x){return ror(x,6)^ror(x,11)^ror(x,25);}
static inline uint32_t s0(uint32_t x){return ror(x,7)^ror(x,18)^(x>>3);}
static inline uint32_t s1(uint32_t x){return ror(x,17)^ror(x,19)^(x>>10);}
static inline uint32_t CH(uint32_t x,uint32_t y,uint32_t z){return (x&y)^(~x&z);}
static inline uint32_t MAJ(uint32_t x,uint32_t y,uint32_t z){return (x&y)^(x&z)^(y&z);}
static uint64_t rs=0x9E3779B97F4A7C15ull;
static uint64_t rnd64(void){rs^=rs<<13;rs^=rs>>7;rs^=rs<<17;return rs;}
static void compress38(const uint32_t cv[8],const uint32_t w16[16],uint32_t out[8]){
  uint32_t W[38]; for(int i=0;i<16;i++)W[i]=w16[i];
  for(int i=16;i<38;i++)W[i]=s1(W[i-2])+W[i-7]+s0(W[i-15])+W[i-16];
  uint32_t a=cv[0],b=cv[1],c=cv[2],d=cv[3],e=cv[4],f=cv[5],g=cv[6],h=cv[7];
  for(int i=0;i<38;i++){uint32_t t1=h+S1(e)+CH(e,f,g)+K[i]+W[i]; uint32_t t2=S0(a)+MAJ(a,b,c);
    h=g;g=f;f=e;e=d+t1;d=c;c=b;b=a;a=t1+t2;}
  out[0]=cv[0]+a;out[1]=cv[1]+b;out[2]=cv[2]+c;out[3]=cv[3]+d;out[4]=cv[4]+e;out[5]=cv[5]+f;out[6]=cv[6]+g;out[7]=cv[7]+h;}
typedef struct {uint32_t k0,E0base,PP,QQ,EF,FF,KF,K2, a,b,g;} CO;
typedef struct {uint32_t cE5,K2E5,KW9,cW9,cE4,mA,mB,KW8,cW8,cA,cB,A2,E6,KK7c,D7c;} PF;
static void cvc(const uint32_t cv[8],CO*o){uint32_t a=cv[0],b=cv[1],c=cv[2],d=cv[3],e=cv[4],f=cv[5],g=cv[6],h=cv[7];
  o->k0=-S0(a)-MAJ(a,b,c)-h-S1(e)-CH(e,f,g)-K[0]; o->E0base=d-S0(a)-MAJ(a,b,c);
  o->PP=a&b;o->QQ=a|b;o->EF=e^f;o->FF=f;o->KF=o->k0+CC2-g-K[1];o->K2=CC2+o->k0;o->a=a;o->b=b;o->g=g;}
static inline uint32_t Ff(const CO*o,uint32_t a0){uint32_t E0=a0+o->E0base;
  return a0+o->KF-S0(a0)-(o->PP|(a0&o->QQ))-S1(E0)-(o->FF^(E0&o->EF));}
static inline uint32_t hf(const CO*o,const uint32_t cv[8],uint32_t a0){uint32_t E0=a0+o->E0base;
  return -S0(a0)-MAJ(a0,cv[0],cv[1])-cv[6]-S1(E0)-CH(E0,cv[4],cv[5])-K[1];}
static void pfc(const uint32_t cv[8],const CO*co,PF*p){
  uint32_t A2=SAx[2],A3=SAx[3],A4=SAx[4],A5=SAx[5],E6=SEx[6],E7=SEx[7],E8=SEx[8],E9=SEx[9];
  p->cE5=A5-S0(A4)-MAJ(A4,A3,A2); p->K2E5=co->K2+p->cE5; p->KW9=E9-A5-S1(E8)-CH(E8,E7,E6)-K[9]; p->cW9=p->KW9-p->cE5;
  p->cE4=A4-S0(A3); p->mA=A3&A2; p->mB=A3|A2; p->KW8=E8-A4-S1(E7)-K[8]; p->cW8=p->KW8-p->cE4; p->cA=E7&E6; p->cB=~E7;
  p->A2=A2;p->E6=E6;p->KK7c=E7-2*A3-cv[0]+S0(A2)-S1(E6)-K[7]; p->D7c=SEy[7]-SEx[7];}
static uint64_t pfops=0; static uint64_t st[4];
static int postf(const PF*p,uint32_t a0,uint32_t u,uint32_t F){
  uint32_t E5=(u-F)+p->K2E5+a0; pfops+=6;
  if((E5&0xE0000000u)!=0xA0000000u) return 0; st[0]++;
  uint32_t w9=p->KW9-E5, w9y=w9+SPC_D9; pfops+=22;
  if((s0(w9y)-s0(w9))!=SPC_D9s) return 1; st[1]++;
  uint32_t a1=E5-p->cE5, maj1=p->mA|(a1&p->mB), E40=a0-maj1, chx=p->cA^(p->cB&E5), w8=(p->cW8-E40)-chx, w8y=w8+SPC_D8; pfops+=29;
  if((s0(w8y)-s0(w8))!=SPC_T8) return 2; st[2]++;
  uint32_t E4=E40+p->cE4, maj2=MAJ(p->A2,a1,a0), ch2=CH(p->E6,E5,E4), w7=(p->KK7c+maj2)-ch2, w7y=w7+p->D7c; pfops+=31;
  if((s0(w7y)-s0(w7))!=SPC_F7d) return 3; st[3]++; pfops+=3014; return 4;}
static inline int r16ok(uint32_t e){uint32_t x=e&~0x405u; for(int i=0;i<20;i++) if(x==R16H[i]) return 1; return 0;}
// ---- table: NCOL columns x 2^19 rows of 256-bit words (4 x u64), 6 lanes of 42 bits [u:32][field:6][spare:4], count in bits 252..255
#define NCOL 15
#define ROWS (1u<<19)
#define LANES 6
#define STRIDE 42
typedef struct {uint64_t w[4];} W256;
static W256 *T;
static inline uint64_t getbits(const W256*x,int pos,int n){int li=pos>>6,sh=pos&63; unsigned __int128 v=x->w[li]; if(li<3) v|=((unsigned __int128)x->w[li+1])<<64; return (uint64_t)(v>>sh)&((n==64)?~0ull:((1ull<<n)-1));}
static inline void setbits(W256*x,int pos,int n,uint64_t val){for(int i=0;i<n;i++){int p=pos+i; uint64_t bit=(val>>i)&1; x->w[p>>6]=(x->w[p>>6]&~(1ull<<(p&63)))|(bit<<(p&63));}}
static inline int cnt(const W256*x){return (int)(x->w[3]>>60);}
int main(int argc,char**argv){
  uint64_t seed=argc>1?strtoull(argv[1],0,0):1; int ncv=argc>2?atoi(argv[2]):1; int ref=argc>3?atoi(argv[3]):0;
  rs^=seed*0x2545F4914F6CDD1Dull; for(int i=0;i<10;i++)rnd64();
  size_t tb=(size_t)NCOL*ROWS*sizeof(W256);
  T=mmap(0,tb,PROT_READ|PROT_WRITE,MAP_PRIVATE|MAP_ANONYMOUS,-1,0);
  uint32_t r=rnd64()&8191, ustart=(uint32_t)rnd64();
  // reset: every lane empty = field tag 15, u 0; count 0
  W256 E; memset(&E,0,sizeof E); for(int L=0;L<LANES;L++) setbits(&E,STRIDE*L+32,6,15);
  for(size_t i=0;i<(size_t)NCOL*ROWS;i++) T[i]=E;
  uint64_t ent=0, full=0;
  for(uint64_t n=0;n<(1ull<<32);n++){uint32_t u=ustart+(uint32_t)n; uint32_t g=s0(u)-u-r; uint32_t lo=g&8191;
    if(lo<NCOL*8){W256*x=&T[(size_t)(lo>>3)*ROWS+(g>>13)]; int c=cnt(x); if(c<LANES){
      uint64_t lane=(uint64_t)u|((uint64_t)(g&7)<<32); setbits(x,STRIDE*c,38,lane); x->w[3]=(x->w[3]&~(15ull<<60))|((uint64_t)(c+1)<<60); ent++;} else full++;}}
  printf("epoch r=%u ustart=%08x entries=%llu dropped=%llu per-bucket=%.6f\n",r,ustart,(unsigned long long)ent,(unsigned long long)full,(double)ent/((double)NCOL*ROWS));
  fflush(stdout);
  for(int cvi=0;cvi<ncv;cvi++){
    uint32_t M0[16],cv[8]; for(int i=0;i<16;i++)M0[i]=(uint32_t)rnd64(); compress38(IV,M0,cv);
    CO co; cvc(cv,&co); PF pf; pfc(cv,&co,&pf);
    uint32_t Hr=R16H[0]-r;
    uint64_t probes=0,bkt=0,fired=0,claws=0,refclaws=0,bad=0,good=0,ops=0,res=0,xc=0; memset(st,0,sizeof st); pfops=0;
    for(uint32_t i=0;i<(1u<<26);i++){uint32_t a0=(9u<<26)|i; uint32_t F=Ff(&co,a0); uint32_t y=Hr-F; ops+=35; if(((y+5)&1023)<125){ops+=6;res++;}
      for(int win=0;win<2;win++){uint32_t yw=y+(win?1024u:0u); uint32_t q=(yw+5)&8191; if(q>=NCOL*8+5) continue;
        probes++; ops+=25;
        uint32_t row0=yw>>13, c=(yw&8191)>>3, w=yw&7;
        for(int j=0;j<20;j++){uint32_t rowj=(row0+T20[j])&(ROWS-1); ops+=2;
          // main bucket (if covered) and straddle (next bucket) if w>=3
          for(int s=0;s<2;s++){uint32_t cc,rr;
            if(s==0){ if(q<5) continue; cc=c; rr=rowj; }
            else { if(w<3) break; if(q<5){cc=0; rr=(rowj+1)&(ROWS-1); ops+=2; xc++;} else {cc=c+1; rr=rowj; if(cc>=NCOL) break;} }
            W256*x=&T[(size_t)cc*ROWS+rr]; bkt++; int any=0; ops+=9;
            for(int L=0;L<LANES;L++){uint64_t lane=getbits(x,STRIDE*L,38); uint32_t u=(uint32_t)lane; uint32_t t=(uint32_t)(lane>>32)&15;
              uint32_t rfield=t+16-w; uint32_t a=rfield&0x1A; int pass = s==0 ? (a==0x10) : (a==0x08);
              if(pass){any=1; claws++; ops+=2;
                uint32_t e16=F+s0(u)-u; if(!r16ok(e16)) bad++;
                // the claw's head and offset: e16 - R16H[j] - win*1024 in {0,1,4,5}
                uint32_t d=e16-R16H[j]-(win?1024u:0u); if(!(d==0||d==1||d==4||d==5)) bad++;
                if(postf(&pf,a0,u,F)==4) good++; }
              if(ref && t!=15){ uint32_t gg=s0(u)-u-r; for(int o=0;o<6;o++){ if(o==2||o==3) continue; if(gg==yw+((uint32_t)T20[j]<<13)+o) refclaws++; } } }
            fired+=any; if(any) ops+=18; } } } }
    ops+=pfops; printf("ops/a0=%.6f (walk on fired only; +walk on all reads: %.6f) res/a0=%.6f xc=%llu\n",(double)ops/(1<<26),(double)(ops+18*(bkt-fired))/(1<<26),(double)res/(1<<26),(unsigned long long)xc);
    printf("cv %d: probes/a0=%.6f buckets/probe=%.4f fired/probe=%.4f claws=%llu claws/a0=%.6f bad=%llu ref=%llu stages c1=%llu c12=%llu c12g=%llu all4=%llu pfops/claw=%.4f\n",
      cvi,(double)probes/(1<<26),(double)bkt/probes,(double)fired/probes,(unsigned long long)claws,(double)claws/(1<<26),(unsigned long long)bad,(unsigned long long)refclaws,
      (unsigned long long)st[0],(unsigned long long)st[1],(unsigned long long)st[2],(unsigned long long)st[3],(double)pfops/claws);
    fflush(stdout);
  }
  struct rusage ru; getrusage(RUSAGE_SELF,&ru); printf("maxrss_kib=%ld table_bytes=%zu\n",ru.ru_maxrss,tb);
  return 0;}
```

### `h7.c`: utab.c plus a one-bit overflow mark per bucket and the rows 17..21 forced-bit events of every claw (Section 13, H7)

```c
// utab.c - full-scale development port of the u-table claw machine (sha256-r38, P8/P1 claw), own code.
// usage: utab <seed> <ncv> [ref] ; builds one epoch table over all 2^32 u, then scans a0 in W9 for ncv chaining values.
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>
#include <sys/mman.h>
#include <sys/resource.h>
#include "consts.h"
#define M32 0xffffffffu
static inline uint32_t ror(uint32_t x,int n){return (x>>n)|(x<<(32-n));}
static inline uint32_t S0(uint32_t x){return ror(x,2)^ror(x,13)^ror(x,22);}
static inline uint32_t S1(uint32_t x){return ror(x,6)^ror(x,11)^ror(x,25);}
static inline uint32_t s0(uint32_t x){return ror(x,7)^ror(x,18)^(x>>3);}
static inline uint32_t s1(uint32_t x){return ror(x,17)^ror(x,19)^(x>>10);}
static inline uint32_t CH(uint32_t x,uint32_t y,uint32_t z){return (x&y)^(~x&z);}
static inline uint32_t MAJ(uint32_t x,uint32_t y,uint32_t z){return (x&y)^(x&z)^(y&z);}
static uint64_t rs=0x9E3779B97F4A7C15ull;
static uint64_t rnd64(void){rs^=rs<<13;rs^=rs>>7;rs^=rs<<17;return rs;}
static void compress38(const uint32_t cv[8],const uint32_t w16[16],uint32_t out[8]){
  uint32_t W[38]; for(int i=0;i<16;i++)W[i]=w16[i];
  for(int i=16;i<38;i++)W[i]=s1(W[i-2])+W[i-7]+s0(W[i-15])+W[i-16];
  uint32_t a=cv[0],b=cv[1],c=cv[2],d=cv[3],e=cv[4],f=cv[5],g=cv[6],h=cv[7];
  for(int i=0;i<38;i++){uint32_t t1=h+S1(e)+CH(e,f,g)+K[i]+W[i]; uint32_t t2=S0(a)+MAJ(a,b,c);
    h=g;g=f;f=e;e=d+t1;d=c;c=b;b=a;a=t1+t2;}
  out[0]=cv[0]+a;out[1]=cv[1]+b;out[2]=cv[2]+c;out[3]=cv[3]+d;out[4]=cv[4]+e;out[5]=cv[5]+f;out[6]=cv[6]+g;out[7]=cv[7]+h;}
typedef struct {uint32_t k0,E0base,PP,QQ,EF,FF,KF,K2, a,b,g;} CO;
typedef struct {uint32_t cE5,K2E5,KW9,cW9,cE4,mA,mB,KW8,cW8,cA,cB,A2,E6,KK7c,D7c;} PF;
static void cvc(const uint32_t cv[8],CO*o){uint32_t a=cv[0],b=cv[1],c=cv[2],d=cv[3],e=cv[4],f=cv[5],g=cv[6],h=cv[7];
  o->k0=-S0(a)-MAJ(a,b,c)-h-S1(e)-CH(e,f,g)-K[0]; o->E0base=d-S0(a)-MAJ(a,b,c);
  o->PP=a&b;o->QQ=a|b;o->EF=e^f;o->FF=f;o->KF=o->k0+CC2-g-K[1];o->K2=CC2+o->k0;o->a=a;o->b=b;o->g=g;}
static inline uint32_t Ff(const CO*o,uint32_t a0){uint32_t E0=a0+o->E0base;
  return a0+o->KF-S0(a0)-(o->PP|(a0&o->QQ))-S1(E0)-(o->FF^(E0&o->EF));}
static inline uint32_t hf(const CO*o,const uint32_t cv[8],uint32_t a0){uint32_t E0=a0+o->E0base;
  return -S0(a0)-MAJ(a0,cv[0],cv[1])-cv[6]-S1(E0)-CH(E0,cv[4],cv[5])-K[1];}
static void pfc(const uint32_t cv[8],const CO*co,PF*p){
  uint32_t A2=SAx[2],A3=SAx[3],A4=SAx[4],A5=SAx[5],E6=SEx[6],E7=SEx[7],E8=SEx[8],E9=SEx[9];
  p->cE5=A5-S0(A4)-MAJ(A4,A3,A2); p->K2E5=co->K2+p->cE5; p->KW9=E9-A5-S1(E8)-CH(E8,E7,E6)-K[9]; p->cW9=p->KW9-p->cE5;
  p->cE4=A4-S0(A3); p->mA=A3&A2; p->mB=A3|A2; p->KW8=E8-A4-S1(E7)-K[8]; p->cW8=p->KW8-p->cE4; p->cA=E7&E6; p->cB=~E7;
  p->A2=A2;p->E6=E6;p->KK7c=E7-2*A3-cv[0]+S0(A2)-S1(E6)-K[7]; p->D7c=SEy[7]-SEx[7];}
static uint64_t pfops=0; static uint64_t st[4];
static int postf(const PF*p,uint32_t a0,uint32_t u,uint32_t F){
  uint32_t E5=(u-F)+p->K2E5+a0; pfops+=6;
  if((E5&0xE0000000u)!=0xA0000000u) return 0; st[0]++;
  uint32_t w9=p->KW9-E5, w9y=w9+SPC_D9; pfops+=22;
  if((s0(w9y)-s0(w9))!=SPC_D9s) return 1; st[1]++;
  uint32_t a1=E5-p->cE5, maj1=p->mA|(a1&p->mB), E40=a0-maj1, chx=p->cA^(p->cB&E5), w8=(p->cW8-E40)-chx, w8y=w8+SPC_D8; pfops+=29;
  if((s0(w8y)-s0(w8))!=SPC_T8) return 2; st[2]++;
  uint32_t E4=E40+p->cE4, maj2=MAJ(p->A2,a1,a0), ch2=CH(p->E6,E5,E4), w7=(p->KK7c+maj2)-ch2, w7y=w7+p->D7c; pfops+=31;
  if((s0(w7y)-s0(w7))!=SPC_F7d) return 3; st[3]++; pfops+=3014; return 4;}

static const uint32_t BM[5]={0x40421a80u,0x40461210u,0x01808000u,0x01848010u,0x21808000u};
static const uint32_t BV[5]={0x00000800u,0x00421200u,0x00008000u,0x00040010u,0x21008000u};
static uint64_t NB[2][2], HB[2][2][5];   // [all claws / good pairs][pop<=6 / pop>6]
static void varW(const uint32_t cv[8],uint32_t a0,uint32_t a1,const uint32_t*SA,const uint32_t*SE,uint32_t W[16]){
  uint32_t A[20],Ee[20]; // index i+4
  A[3]=cv[0];A[2]=cv[1];A[1]=cv[2];A[0]=cv[3]; Ee[3]=cv[4];Ee[2]=cv[5];Ee[1]=cv[6];Ee[0]=cv[7];
  A[4]=a0;A[5]=a1; for(int i=2;i<16;i++)A[i+4]=SA[i];
  for(int i=0;i<6;i++) Ee[i+4]=A[i+4]+A[i]-S0(A[i+3])-MAJ(A[i+3],A[i+2],A[i+1]);
  for(int i=6;i<16;i++) Ee[i+4]=SE[i];
  for(int i=0;i<16;i++) W[i]=Ee[i+4]-A[i]-Ee[i]-S1(Ee[i+3])-CH(Ee[i+3],Ee[i+2],Ee[i+1])-K[i];}
static void ebits(const uint32_t cv[8],uint32_t a0,uint32_t a1,int good,int big){
  uint32_t W[22]; varW(cv,a0,a1,SAx,SEx,W); for(int i=16;i<22;i++)W[i]=s1(W[i-2])+W[i-7]+s0(W[i-15])+W[i-16];
  uint32_t a=cv[0],b=cv[1],c=cv[2],d=cv[3],e=cv[4],f=cv[5],g=cv[6],h=cv[7];
  for(int i=0;i<22;i++){uint32_t t1=h+S1(e)+CH(e,f,g)+K[i]+W[i]; uint32_t t2=S0(a)+MAJ(a,b,c); h=g;g=f;f=e;e=d+t1;d=c;c=b;b=a;a=t1+t2;
    if(i>=17){ for(int k=0;k<=good;k++){ if((e&BM[i-17])==BV[i-17]) HB[k][big][i-17]++; } } }
  for(int k=0;k<=good;k++) NB[k][big]++;}
static inline int r16ok(uint32_t e){uint32_t x=e&~0x405u; for(int i=0;i<20;i++) if(x==R16H[i]) return 1; return 0;}
// ---- table: NCOL columns x 2^19 rows of 256-bit words (4 x u64), 6 lanes of 42 bits [u:32][field:6][spare:4], count in bits 252..255
#define NCOL 15
#define ROWS (1u<<19)
#define LANES 6
#define STRIDE 42
typedef struct {uint64_t w[4];} W256;
static W256 *T;   // bit 38 of lane 0 (a spare bit) marks a bucket that received more than six covered words
static inline uint64_t getbits(const W256*x,int pos,int n){int li=pos>>6,sh=pos&63; unsigned __int128 v=x->w[li]; if(li<3) v|=((unsigned __int128)x->w[li+1])<<64; return (uint64_t)(v>>sh)&((n==64)?~0ull:((1ull<<n)-1));}
static inline void setbits(W256*x,int pos,int n,uint64_t val){for(int i=0;i<n;i++){int p=pos+i; uint64_t bit=(val>>i)&1; x->w[p>>6]=(x->w[p>>6]&~(1ull<<(p&63)))|(bit<<(p&63));}}
static inline int cnt(const W256*x){return (int)(x->w[3]>>60);}
int main(int argc,char**argv){
  uint64_t seed=argc>1?strtoull(argv[1],0,0):1; int ncv=argc>2?atoi(argv[2]):1; int ref=argc>3?atoi(argv[3]):0;
  rs^=seed*0x2545F4914F6CDD1Dull; for(int i=0;i<10;i++)rnd64();
  size_t tb=(size_t)NCOL*ROWS*sizeof(W256);
  T=mmap(0,tb,PROT_READ|PROT_WRITE,MAP_PRIVATE|MAP_ANONYMOUS,-1,0);
  uint32_t r=rnd64()&8191, ustart=(uint32_t)rnd64();
  // reset: every lane empty = field tag 15, u 0; count 0
  W256 E; memset(&E,0,sizeof E); for(int L=0;L<LANES;L++) setbits(&E,STRIDE*L+32,6,15);
  for(size_t i=0;i<(size_t)NCOL*ROWS;i++) T[i]=E;
  uint64_t ent=0, full=0;
  for(uint64_t n=0;n<(1ull<<32);n++){uint32_t u=ustart+(uint32_t)n; uint32_t g=s0(u)-u-r; uint32_t lo=g&8191;
    if(lo<NCOL*8){W256*x=&T[(size_t)(lo>>3)*ROWS+(g>>13)]; int c=cnt(x); if(c<LANES){
      uint64_t lane=(uint64_t)u|((uint64_t)(g&7)<<32); setbits(x,STRIDE*c,38,lane); x->w[3]=(x->w[3]&~(15ull<<60))|((uint64_t)(c+1)<<60); ent++;} else {full++; x->w[0]|=1ull<<38;}}}
  printf("epoch r=%u ustart=%08x entries=%llu dropped=%llu per-bucket=%.6f\n",r,ustart,(unsigned long long)ent,(unsigned long long)full,(double)ent/((double)NCOL*ROWS));
  fflush(stdout);
  for(int cvi=0;cvi<ncv;cvi++){
    uint32_t M0[16],cv[8]; for(int i=0;i<16;i++)M0[i]=(uint32_t)rnd64(); compress38(IV,M0,cv);
    CO co; cvc(cv,&co); PF pf; pfc(cv,&co,&pf);
    uint32_t Hr=R16H[0]-r;
    uint64_t probes=0,bkt=0,fired=0,claws=0,refclaws=0,bad=0,good=0,ops=0,res=0,xc=0; memset(st,0,sizeof st); pfops=0;
    for(uint32_t i=0;i<(1u<<26);i++){uint32_t a0=(9u<<26)|i; uint32_t F=Ff(&co,a0); uint32_t y=Hr-F; ops+=35; if(((y+5)&1023)<125){ops+=6;res++;}
      for(int win=0;win<2;win++){uint32_t yw=y+(win?1024u:0u); uint32_t q=(yw+5)&8191; if(q>=NCOL*8+5) continue;
        probes++; ops+=25;
        uint32_t row0=yw>>13, c=(yw&8191)>>3, w=yw&7;
        for(int j=0;j<20;j++){uint32_t rowj=(row0+T20[j])&(ROWS-1); ops+=2;
          // main bucket (if covered) and straddle (next bucket) if w>=3
          for(int s=0;s<2;s++){uint32_t cc,rr;
            if(s==0){ if(q<5) continue; cc=c; rr=rowj; }
            else { if(w<3) break; if(q<5){cc=0; rr=(rowj+1)&(ROWS-1); ops+=2; xc++;} else {cc=c+1; rr=rowj; if(cc>=NCOL) break;} }
            W256*x=&T[(size_t)cc*ROWS+rr]; bkt++; int any=0; ops+=9;
            for(int L=0;L<LANES;L++){uint64_t lane=getbits(x,STRIDE*L,38); uint32_t u=(uint32_t)lane; uint32_t t=(uint32_t)(lane>>32)&15;
              uint32_t rfield=t+16-w; uint32_t a=rfield&0x1A; int pass = s==0 ? (a==0x10) : (a==0x08);
              if(pass){any=1; claws++; ops+=2;
                uint32_t e16=F+s0(u)-u; if(!r16ok(e16)) bad++;
                // the claw's head and offset: e16 - R16H[j] - win*1024 in {0,1,4,5}
                uint32_t d=e16-R16H[j]-(win?1024u:0u); if(!(d==0||d==1||d==4||d==5)) bad++;
                int big=(int)((x->w[0]>>38)&1); int gp=postf(&pf,a0,u,F)==4; if(gp) good++; ebits(cv,a0,u-hf(&co,cv,a0),gp,big); }
              if(ref && t!=15){ uint32_t gg=s0(u)-u-r; for(int o=0;o<6;o++){ if(o==2||o==3) continue; if(gg==yw+((uint32_t)T20[j]<<13)+o) refclaws++; } } }
            fired+=any; if(any) ops+=18; } } } }
    ops+=pfops; printf("ops/a0=%.6f (walk on fired only; +walk on all reads: %.6f) res/a0=%.6f xc=%llu\n",(double)ops/(1<<26),(double)(ops+18*(bkt-fired))/(1<<26),(double)res/(1<<26),(unsigned long long)xc);
    printf("cv %d: probes/a0=%.6f buckets/probe=%.4f fired/probe=%.4f claws=%llu claws/a0=%.6f bad=%llu ref=%llu stages c1=%llu c12=%llu c12g=%llu all4=%llu pfops/claw=%.4f\n",
      cvi,(double)probes/(1<<26),(double)bkt/probes,(double)fired/probes,(unsigned long long)claws,(double)claws/(1<<26),(unsigned long long)bad,(unsigned long long)refclaws,
      (unsigned long long)st[0],(unsigned long long)st[1],(unsigned long long)st[2],(unsigned long long)st[3],(double)pfops/claws);
    fflush(stdout);
  }
  for(int k=0;k<2;k++) for(int bg=0;bg<2;bg++){ printf("%s pop%s n=%llu",k?"goodpairs":"claws",bg?">6":"<=6",(unsigned long long)NB[k][bg]);
    for(int t=0;t<5;t++) printf(" E%d=%llu",17+t,(unsigned long long)HB[k][bg][t]); printf("\n"); }
  struct rusage ru; getrusage(RUSAGE_SELF,&ru); printf("maxrss_kib=%ld table_bytes=%zu\n",ru.ru_maxrss,tb);
  return 0;}
```

### `fillr2.c`: the retained-entry count over all 8192 values of r, in 2^26-byte slices (Sections 3.1, 10, 13)

```c
// fillr2.c - the retained-entry count of the u-table for every r, in slices: one residue j = r mod 8 per process,
// the 2^29 aligned 8-windows of P - j counted 2^26 at a time (64 MiB resident); prints S_j[c], c = 0..1023.
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>
#include <sys/resource.h>
static inline uint32_t ror(uint32_t x,int n){return (x>>n)|(x<<(32-n));}
static inline uint32_t s0(uint32_t x){return ror(x,7)^ror(x,18)^(x>>3);}
int main(int argc,char**argv){
  int j=atoi(argv[1]), LANES=6; uint8_t *h=malloc(1u<<26); double S[1024]; memset(S,0,sizeof S);
  for(int sl=0;sl<8;sl++){ memset(h,0,1u<<26);
    for(uint64_t uu=0;uu<(1ull<<32);uu++){uint32_t u=uu; uint32_t b=(s0(u)-u-(uint32_t)j)>>3; if((b>>26)==(uint32_t)sl){uint32_t i=b&((1u<<26)-1); if(h[i]<255)h[i]++;}}
    for(uint32_t i=0;i<(1u<<26);i++){int x=h[i]; S[i&1023]+=x<LANES?x:LANES;} }
  struct rusage ru; getrusage(RUSAGE_SELF,&ru);
  printf("j %d maxrss_kib %ld\n",j,ru.ru_maxrss); for(int c=0;c<1024;c++) printf("%.0f\n",S[c]); return 0;}
```

### `pbal.c`: the class sizes of P mod 2^13 (Section 3.1, 13)

```c
#include <stdio.h>
#include <stdint.h>
#include <stdlib.h>
static inline uint32_t ror(uint32_t x,int n){return (x>>n)|(x<<(32-n));}
static inline uint32_t s0(uint32_t x){return ror(x,7)^ror(x,18)^(x>>3);}
int main(){uint32_t *c=calloc(8192,4); for(uint64_t u=0;u<(1ull<<32);u++){uint32_t x=u; c[(s0(x)-x)&8191]++;}
 uint32_t mn=~0u,mx=0; for(int i=0;i<8192;i++){if(c[i]<mn)mn=c[i]; if(c[i]>mx)mx=c[i];} printf("P mod 2^13 class sizes: min %u max %u (2^19 = %u)\n",mn,mx,1u<<19); return 0;}
```

### `gen_h.py`: writes consts.h from utab38.py (no transcription)

```python
import sys
src=open('utab38.py').read().split('def main')[0]
exec(src)
o=[]
o.append('static const uint32_t K[38]={%s};'%','.join('0x%08xu'%k for k in K))
o.append('static const uint32_t IV[8]={%s};'%','.join('0x%08xu'%k for k in IV))
o.append('static const uint32_t R16H[20]={%s};'%','.join('0x%08xu'%k for k in R16H))
o.append('static const uint32_t T20[20]={%s};'%','.join('%du'%k for k in T20))
o.append('#define CC2 0x%08xu'%Cc2)
for k in ('D7','D8','D9','T8','F7d','D9s'): o.append('#define SPC_%s 0x%08xu'%(k,SPC[k]))
o.append('static const uint32_t SAx[16]={%s};'%','.join('0x%08xu'%k for k in SAx))
o.append('static const uint32_t SEx[16]={%s};'%','.join('0x%08xu'%k for k in SExF))
o.append('static const uint32_t SAy[16]={%s};'%','.join('0x%08xu'%k for k in SAy))
o.append('static const uint32_t SEy[16]={%s};'%','.join('0x%08xu'%k for k in SEyF))
open('consts.h','w').write('\n'.join(o)+'\n')
print('ok')
```

## Appendix P. The paired P1 q3 runs (Section 9): registrations, runs, per-seed values

Tool: `traillab` (our own C; the tool of Appendix R.1) with one addition, a joint list variable (`--var "W8 pairlist W9 @FILE late"`: one list index per late redraw sets W8 and W9 together); regression before the 10-17 registration: the A0 baseline command reproduces the declared seed-7001 log except the thread count; regression before the 10-21 registration: the 10-21 build reproduces the 10-17 A25 seed-7001 log line for line. Model file `chi38p8_a1.txt` = `chi38p8.txt` with the line `except W7 W8 W9`. Lists: `gen_pairs.c` (own code; a1 uniform over the C1&C2 values enumerated exhaustively, a0 uniform in the window conditioned on G by rejection; with R = 0 it reproduces the 10-17 list `pairs25.txt`, SHA-256 6f0ab553...). The baseline per-seed logs are those of the declared level run (Appendix Q, seeds 7001..7128), paired by seed.

**The 10-17 registration** (`PREREG_P1_Q3.md`; SHA-256 and time recorded before its first seed: `efb3100bc19eaf52167cfdcd903dbd496182154d4eea68da070f42b92afc20ff  PREREG_P1_Q3.md
2026-10-17T14:05:12-06:00`), Part A (Part B was not run):

```text
# PREREG_P1_Q3: q3 of the A1-variant family (r38 P1, row-16 sum-claw with A1 free) and pass independence within one chaining value
Written 2026-10-17 (MDT) by the claw_place session on the coordinator's GO, BEFORE the first counted seed; hashed (SHA-256 recorded in prereg_hash.txt with the time) before the run script is started.
Nothing here stages, files or submits anything. Our own code only (traillab is ours; no rival code run, read for execution or compiled).

## 1. Quantity
q3_A1 = the average over the A1-variant family of Pr[accepted event | good pair], where
- a good pair is a chaining value CV1 and (a0, a1) with C1 (top three bits of E5 = a1 + cE5 equal 101b), C2 (W9x = cW9 - a1 in F9), G (W8x = X1(a1) - a0 in G'), and W7x in F7 (F7 enters through the late variable W7, uniform in F7, exactly as in the current attack); a0 uniform in a window [0, 2^LS) (the table of the claw, top bits fixed to 0), a1 uniform over the 53,096,854 values with C1 and C2;
- the event is the one of PREREG_Q3P8_B.md, unchanged: the printed-cell event of chi38p8.txt (rows 16..21 cells, '+' pairs, two-bit conditions, row 19 on signed differences, the relation E18 = E17 INCLUDED), and zero output difference after step 37.
The reference is the declared value of the current attack, q3_base = 2^-96.4282 (mean -96.3123, 128 seeds 7001..7128, PREREG_Q3P8_B.md, SHA-256 eb3310e43e0308e5658631226e09e9ab7d0403de9470dcd3b36545f9fee00f5a), whose per-seed logs are copied in base_logs/ (recomputed here: mean -96.3123, sd 0.5563, bound -96.42814).
The relaxation gain of the current filing (0.4149 bit, E18 = E17 not imposed) is NOT re-measured for the A1 family; it is assumed to transfer (it comes from the prefix lineages and the tail, which are the same objects); this is stated as an assumption in the result.

## 2. Tool and inputs (all hashed in out/hashes_A.txt before the first seed)
- `traillab_p1` = traillab with ONE addition (tl_diff.txt): a joint list variable. `--var "W8 pairlist W9 @FILE late"`: the file holds pairs (W8x, W9x) in hex; one list index is drawn per late redraw by the same single `tl_below` draw as a plain list on W8, and W8, W9 are set together. Everything else is the source of the tool of PREREG_Q3P8_B.md (smc.c, main.c, diff.c byte-identical; traillab.c and traillab.h differ by tl_diff.txt).
- Regression (done before this registration; development, not a counted seed): the baseline command of PREREG_Q3P8_B.md on seed 7001 with the unmodified sources and with traillab_p1 gives output identical to the declared seed_7001.log except the thread count in the header line (reg_diff_base.txt is that one line; traillab_p1 against the unmodified build: reg_diff_p1.txt, 0 lines); 23 s per seed with 8 threads, peak RSS 188 MB.
- `chi/chi38p8_a1.txt` = chi38p8.txt (c47e5ec6...) with the single line `except W7 W8 W9` (W9's printed cell is not a requirement of the path: only its modular difference and ds0(W9) are, and C2 keeps both).
- Lists `lists/pairs25.txt` (a0 window 2^25, n0 = 2^25) and `lists/pairs26.txt` (window 2^26): 1,048,576 pairs each from gen_pairs.c (a1 uniform over the C1&C2 values, a0 uniform in the window conditioned on G by rejection; acceptance 2^-5.995 and 2^-5.981, equal to the exact enumeration 2^-5.9959 and 2^-5.9806). SHA-256: pairs25 6f0ab553..., pairs26 87ebf10c...
- Model = family (famcheck.c, 200,000 draws per list, 0 failures): for every drawn sample the pair rebuilt by traillab (W0..W5 and the chaining value by inverse expansion and step inversion) has A1 = cW9 - W9, A0 = X1(A1) - W8 inside the window, A2..A15 equal to S's in both members, equal chaining values for x and y, and the scouts' construction variantW(CV, A0, A1) (own port) reproduces all 16 message words of both members.
- Development pilot (not counted): dev seed 31001, list 25, full configuration: all diagnostics 0, 23.2 s, peak RSS 192,748 kB.

## 3. Part A: the q3 runs
Command per seed s (one process per seed, one process at a time; the generator streams are indexed by the seed):
`window --chi chi/chi38p8_a1.txt --rows 22 37 --event out --np 8192 --mt 32768 --seeds s --threads 8 --autolist --var "W8 pairlist W9 @lists/pairsLS.txt late"`
Machine rules (coordinator): the cloud box (address redacted), own folder /root/p1q3, `prlimit --as=268435456` (2^28), `nice -n 10`, `ulimit -s 2048`, `MALLOC_ARENA_MAX=1`, 8 threads, one process at a time, the cores of the r39 tail run left alone (no pinning, no oversubscription), only own processes are started or stopped.
Runs: A25 = list 25, seeds 7001..7128 (the SAME seeds as the declared baseline run, deliberately: the prefix of a seed does not depend on the variant (its random streams and acceptance are independent of the late words), so the baseline and A1 values of a seed share the prefix lineage and the comparison is paired); then A26 = list 26, seeds 7001..7128. Execution order: A25 seeds ascending, then A26 seeds ascending.
Per-seed value L_s = prefix log2 P(rows 7..21) + log2(EXACT / samples) from the log (a dead seed or 0 EXACT counts as -128).
Diagnostics required 0 in every seed (prefix broken by redraw, y-anchor inconsistent, replay mismatches); a non-zero diagnostic in any seed of a run voids that run (reported, not replaced). No look at L values or EXACT counts before all seeds of a run are finished (only rc, diagnostics, timing and memory are monitored); no stopping rule other than the time limit below.
Time limit: the coordinator's 6 h from the GO (13:55 MDT): no new seed is started after 19:20 MDT; the seeds finished in ascending order are used and the run is reported as partial with its n (the one-sided bound then uses t(0.99, n-1)).

Statistics (per run X in {A25, A26}, n seeds):
- Declared stand-alone value q3_X = floor_4dec(mean L - t sd(L)/sqrt(n)), t = 2.3556 for n = 128 (exact quantile t(0.99,127) = 2.3561; the registered value is used, and the exact one is also printed), to be compared with the declared -96.4282.
- Paired difference D_X = mean over seeds of (L_s(X) - L_s(base)) with sd(Delta); D_X^LB = D_X - t sd(Delta)/sqrt(n), D_X^UB = D_X + t sd(Delta)/sqrt(n) (one-sided 99% each); halves 7001..7064 / 7065..7128.
Break-even factors (P1_TEST.md, exact ops): the gain of the claw over the current filter, in bit, for design d at table size n0 is g(d, n0); P1 keeps a gain iff D > -g.
  n0 = 2^25: D2 per-head straddle test, flat 32-bit words 1.179; D2 generic flat 0.993; D2 per-head packed 0.714; D2 generic packed 0.577.
  n0 = 2^26: 2.035; 1.866; 1.594; 1.467.
Decision rules (registered): for the best design of its size (per-head, flat): ALIVE iff D_X^LB > -g_best; DEAD iff D_X^UB < -g_best; otherwise INCONCLUSIVE. The projected r38 score for a design is 93.52785 - g(d, n0) - D_X^LB (declared, conservative) and 93.52785 - g(d, n0) - D_X (mean); it is reported for D2 at n0 = 2^25 (A25) and 2^26 (A26), flat and packed. (time_log2 of the package = 85.43385, score 93.52785, memory unchanged.)
```

Run A25 (cloud machine): files hashed at its start (`2026-10-17T20:05:20+00:00`):

```text
c90989f073c4015cb38d1e64108e0261adff2ca8a47541cab09bb93820ca5e66  traillab_p1
7b396bae063122610e2f277af8b2931d7a6829ff6251d468f4df0ad514f392a0  chi/chi38p8_a1.txt
6f0ab55333ffd1c832d49f9f2c421abf7e75a1463f30215adf602622058802fc  lists/pairs25.txt
87ebf10cc3086da1c5abce88933295075e74a71a33c782c69f3bf9c2b49846ee  lists/pairs26.txt
ff582e64e060db2807d85fbe31b054ef04eea26ed00b46dbcafb66b2c36a7138  sel_members.txt
efb3100bc19eaf52167cfdcd903dbd496182154d4eea68da070f42b92afc20ff  PREREG_P1_Q3.md
```

The run log ends at seed 7076 (`A25 seed 7076 rc=0 rss_kb=192952 2026-10-17T20:32:24+00:00`); seed 7077 has no complete log and A26 never started: the run was stopped on 2026-10-17 at 14:32 MDT, before its registered time limit, for a reason not recorded in the run directory, and the cloud machine was later removed. By the registered rule the seeds finished in ascending order are used, n = 76. Its per-seed L values were first computed on 2026-10-21 from the backed-up logs (no earlier analysis output of A25 exists). It is reported, not used in the charge (its window is [0, 2^25), not this package's).

**The 10-21 registration** (`PREREG_P1_Q3_R9.md`; SHA-256 and time recorded before its first seed: `63f36447ed45ca48fab6cdd0adc4bda52378166a4277f5c0b033a496ae9e44b3 *PREREG_P1_Q3_R9.md
2026-10-21T11:29:42-06:00`):

```text
# PREREG_P1_Q3_R9: paired q3 of the P1 family on the package's own a0 window (LS = 26, R = 9)
Written 2026-10-21 (MDT) before the first counted seed; its SHA-256 and the time are recorded in prereg_hash.txt before run_R9.sh starts. Own code only.

## Quantity
Delta_s = L_s(R9) - L_s(base) per seed s, where L_s = prefix log2 P(rows 7..21) + log2(EXACT / samples) from the traillab log, as in PREREG_P1_Q3.md (10-17, SHA-256 efb3100b...) Part A, with one change: the pair list is lists/pairs26r9.txt (1,048,576 pairs from gen_pairs.c LS = 26, seed 3, R = 9: a0 uniform in [9 x 2^26, 10 x 2^26) conditioned on G, a1 uniform over the C1&C2 values). L_s(base) is the declared 10-17 baseline log of the same seed (levers_1017/claw_place/p1_q3/base_logs/seed_s.log, A0-variant family, 196,608 selected variants).
Tool: traillab_p1 built from the 10-17 sources (byte-identical to the cloud copy that ran A25); regression before this registration (development, not a counted seed): seed 7001 on lists/pairs25.txt reproduces the 10-17 A25_7001.log line for line (out/regress_A25_7001.log). gen_pairs with R = 0 reproduces pairs25.txt (SHA-256 6f0ab553...).

## Run
Seeds 7001, 7002, ... ascending, one process at a time, the A25 command with the R9 list, 8 threads, nice 10, address-space cap 2^28. Hard time limit: no new seed is started 18 minutes after the first seed starts; the seeds finished in ascending order are used (n reported). No L value or EXACT count is looked at before the run ends; only rc, diagnostics and timing are monitored. A non-zero diagnostic in any seed voids the run.

## Statistic (registered)
D = mean Delta_s, sd over seeds, D_LB = D - t(0.99, n-1) sd / sqrt(n) (one-sided 99%). The package charges q3_P1 = q3_model + min(0, D_LB), q3_model = -96.0133 (the registered bound of 9aaf71a2's studies). The 10-17 partial A25 run (76 seeds, a0 window [0, 2^25)) is reported beside it, not pooled.
```

Run R9 (our workstation, WSL, 8 threads, nice 10, `prlimit --as=2^28`): files hashed at its start (`2026-10-21T11:29:46-06:00`):

```text
91751b9a854796626eef34f9db536350e7d94c150ba1c311f6a4240440660abc  traillab_p1
7b396bae063122610e2f277af8b2931d7a6829ff6251d468f4df0ad514f392a0  chi/chi38p8_a1.txt
98994e0a62c423e59a909373356ad7c95aff05ca364acd14241bb9ac18ff11e0  lists/pairs26r9.txt
63f36447ed45ca48fab6cdd0adc4bda52378166a4277f5c0b033a496ae9e44b3  PREREG_P1_Q3_R9.md
```

Run end: `time limit before seed 7037`. Seeds used n = 36, every diagnostic 0, peak resident set of a seed process 198,568 KiB (`/usr/bin/time -v`), under the cap 2^28.

Registered statistic: R9 D = -0.0121, sd 0.1321, t(0.99, 35) = 2.4377, D_LB = -0.0658; A25 D = +0.0022, sd 0.1347, t(0.99, 75) = 2.3771, D_LB = -0.0345.

Per seed (prefix log2 is shared by the pair; L = prefix_log2 + log2(exact / 2^28); Delta = L_P1 - L_A0):

```text
# R9: seed prefix_log2 exact_P1 exact_A0 L_P1 L_A0 Delta
7001 -81.3715 10412 10961 -96.0255 -95.9514 -0.0741
7002 -81.2237 10100 10634 -95.9216 -95.8473 -0.0743
7003 -83.0084 10909 10241 -97.5952 -97.6863 +0.0912
7004 -81.2120 10351 10754 -95.8745 -95.8194 -0.0551
7005 -81.5989 10208 9338 -96.2815 -96.4100 +0.1285
7006 -82.2860 10067 7820 -96.9887 -97.3530 +0.3644
7007 -81.5131 10370 10944 -96.1730 -96.0952 -0.0777
7008 -81.8333 10157 10129 -96.5231 -96.5271 +0.0040
7009 -81.0088 9947 10498 -95.7288 -95.6510 -0.0778
7010 -81.5667 10457 11613 -96.2145 -96.0632 -0.1513
7011 -81.4103 10243 9980 -96.0879 -96.1255 +0.0375
7012 -81.3556 9831 9642 -96.0925 -96.1205 +0.0280
7013 -82.1290 10291 9618 -96.7999 -96.8975 +0.0976
7014 -81.4070 10392 11402 -96.0638 -95.9300 -0.1338
7015 -81.6177 10511 10500 -96.2581 -96.2596 +0.0015
7016 -81.7261 9637 10178 -96.4917 -96.4129 -0.0788
7017 -81.7814 9898 9674 -96.5085 -96.5415 +0.0330
7018 -81.1822 10076 9640 -95.8836 -95.9474 +0.0638
7019 -81.4372 10290 10442 -96.1082 -96.0871 -0.0212
7020 -81.0970 10716 10744 -95.7095 -95.7058 -0.0038
7021 -81.3129 10628 8978 -95.9373 -96.1807 +0.2434
7022 -82.2707 10132 9334 -96.9641 -97.0824 +0.1184
7023 -81.1573 9913 10671 -95.8822 -95.7759 -0.1063
7024 -81.1519 10129 11133 -95.8457 -95.7093 -0.1364
7025 -82.0565 10451 12864 -96.7051 -96.4054 -0.2997
7026 -81.7341 10408 11518 -96.3887 -96.2425 -0.1462
7027 -81.0770 9932 9480 -95.7991 -95.8663 +0.0672
7028 -81.7966 10765 9340 -96.4025 -96.6074 +0.2049
7029 -81.9692 10429 10411 -96.6209 -96.6234 +0.0025
7030 -81.8644 10077 11262 -96.5656 -96.4052 -0.1604
7031 -81.8492 10120 9848 -96.5443 -96.5836 +0.0393
7032 -81.0318 10026 10254 -95.7403 -95.7079 -0.0324
7033 -80.8443 9718 11249 -95.5979 -95.3868 -0.2111
7034 -80.7981 10315 10835 -95.4656 -95.3947 -0.0710
7035 -81.8896 9735 9120 -96.6406 -96.7348 +0.0941
7036 -82.1805 10337 11420 -96.8450 -96.7012 -0.1437
# A25: seed prefix_log2 exact_P1 exact_A0 L_P1 L_A0 Delta
7001 -81.3715 10255 10961 -96.0475 -95.9514 -0.0961
7002 -81.2237 10134 10634 -95.9168 -95.8473 -0.0695
7003 -83.0084 10752 10241 -97.6161 -97.6863 +0.0702
7004 -81.2120 10263 10754 -95.8868 -95.8194 -0.0674
7005 -81.5989 10408 9338 -96.2535 -96.4100 +0.1565
7006 -82.2860 10174 7820 -96.9734 -97.3530 +0.3796
7007 -81.5131 10453 10944 -96.1615 -96.0952 -0.0662
7008 -81.8333 10291 10129 -96.5042 -96.5271 +0.0229
7009 -81.0088 9903 10498 -95.7352 -95.6510 -0.0842
7010 -81.5667 10513 11613 -96.2068 -96.0632 -0.1436
7011 -81.4103 10180 9980 -96.0969 -96.1255 +0.0286
7012 -81.3556 10076 9642 -96.0570 -96.1205 +0.0635
7013 -82.1290 10309 9618 -96.7974 -96.8975 +0.1001
7014 -81.4070 10544 11402 -96.0429 -95.9300 -0.1129
7015 -81.6177 10561 10500 -96.2512 -96.2596 +0.0084
7016 -81.7261 9558 10178 -96.5036 -96.4129 -0.0907
7017 -81.7814 9944 9674 -96.5018 -96.5415 +0.0397
7018 -81.1822 9871 9640 -95.9132 -95.9474 +0.0342
7019 -81.4372 10335 10442 -96.1019 -96.0871 -0.0149
7020 -81.0970 10700 10744 -95.7117 -95.7058 -0.0059
7021 -81.3129 10828 8978 -95.9104 -96.1807 +0.2703
7022 -82.2707 10146 9334 -96.9621 -97.0824 +0.1203
7023 -81.1573 9887 10671 -95.8860 -95.7759 -0.1101
7024 -81.1519 10167 11133 -95.8403 -95.7093 -0.1309
7025 -82.0565 10433 12864 -96.7076 -96.4054 -0.3022
7026 -81.7341 10529 11518 -96.3720 -96.2425 -0.1295
7027 -81.0770 9842 9480 -95.8123 -95.8663 +0.0541
7028 -81.7966 10626 9340 -96.4213 -96.6074 +0.1861
7029 -81.9692 10382 10411 -96.6274 -96.6234 -0.0040
7030 -81.8644 9896 11262 -96.5918 -96.4052 -0.1865
7031 -81.8492 10261 9848 -96.5243 -96.5836 +0.0593
7032 -81.0318 10231 10254 -95.7111 -95.7079 -0.0032
7033 -80.8443 9901 11249 -95.5709 -95.3868 -0.1842
7034 -80.7981 10236 10835 -95.4767 -95.3947 -0.0820
7035 -81.8896 9814 9120 -96.6290 -96.7348 +0.1058
7036 -82.1805 10291 11420 -96.8514 -96.7012 -0.1502
7037 -81.5903 9593 9109 -96.3625 -96.4372 +0.0747
7038 -82.0164 10177 10574 -96.7034 -96.6482 -0.0552
7039 -82.0059 9894 8447 -96.7336 -96.9617 +0.2281
7040 -82.6270 10814 10207 -97.2264 -97.3097 +0.0833
7041 -81.9544 10442 10134 -96.6043 -96.6475 +0.0432
7042 -82.2741 10663 10330 -96.8938 -96.9395 +0.0458
7043 -82.6407 9950 10059 -97.3602 -97.3445 -0.0157
7044 -80.4355 10068 10409 -95.1380 -95.0900 -0.0481
7045 -82.3630 10201 11770 -97.0466 -96.8402 -0.2064
7046 -81.6353 9787 9294 -96.3786 -96.4532 +0.0746
7047 -81.0005 10327 9730 -95.6664 -95.7523 +0.0859
7048 -82.6376 10130 12409 -97.3313 -97.0385 -0.2928
7049 -81.4655 11015 9077 -96.0383 -96.3175 +0.2792
7050 -81.6089 10067 8522 -96.3116 -96.5519 +0.2404
7051 -81.7793 11014 10786 -96.3522 -96.3824 +0.0302
7052 -81.4855 10492 9271 -96.1285 -96.3070 +0.1785
7053 -82.5840 10380 9961 -97.2425 -97.3019 +0.0594
7054 -81.1668 9675 9574 -95.9268 -95.9419 +0.0151
7055 -82.2990 9504 8608 -97.0847 -97.2275 +0.1429
7056 -82.3064 9795 11499 -97.0486 -96.8172 -0.2314
7057 -80.8095 10415 9895 -95.4631 -95.5370 +0.0739
7058 -81.0654 10435 11129 -95.7163 -95.6234 -0.0929
7059 -81.5981 10252 9695 -96.2745 -96.3551 +0.0806
7060 -81.6180 10819 9934 -96.2167 -96.3398 +0.1231
7061 -81.2075 10266 10783 -95.8819 -95.8110 -0.0709
7062 -82.0255 9784 9999 -96.7693 -96.7379 -0.0314
7063 -80.8514 10470 10990 -95.4974 -95.4275 -0.0699
7064 -81.5843 10261 9838 -96.2594 -96.3202 +0.0607
7065 -81.8012 10664 12344 -96.4207 -96.2097 -0.2111
7066 -82.2935 10623 10158 -96.9186 -96.9832 +0.0646
7067 -81.6483 10367 11042 -96.3086 -96.2176 -0.0910
7068 -81.6822 10816 11170 -96.2813 -96.2349 -0.0465
7069 -81.4176 10536 9738 -96.0546 -96.1682 +0.1136
7070 -81.7532 10503 10521 -96.3947 -96.3922 -0.0025
7071 -81.1694 10423 9811 -95.8219 -95.9092 +0.0873
7072 -81.9733 9602 8147 -96.7442 -96.9812 +0.2371
7073 -81.4528 10724 12212 -96.0642 -95.8768 -0.1875
7074 -81.3789 10417 10598 -96.0322 -96.0074 -0.0249
7075 -81.3163 9796 11188 -96.0583 -95.8666 -0.1917
7076 -81.3546 10458 10805 -96.0023 -95.9552 -0.0471
```

## Appendix H. The H3-P1 panel (Section 8)

### H.1 Post-filter panel

Own C port of the counted claw (`p1h3.c` = `p1claw.c` of the development runs plus uncounted statistics), window R = 9, the parent's 2^26-slot loading (the stage rates are per-claw functions of the words and do not read the table), 2^22 scan words, per-head two-window probing, one chaining value per seed (seeds 201..224, drawn from the seed by the port's xorshift); every claw checked against S160 and its real E16 (0 bad in every chaining value). Per chaining value: claws, claws/expected, c1, c1c2, c1c2g, all4 (good pairs), good pairs sharing a0 / sharing u, consecutive-claw pairs with C1 on both / pairs.

```text
201 6628654 0.99991 827510 81689 1318 128 0/0 302427/6628653
202 6630952 1.00034 827579 81945 1319 57 0/0 302899/6630951
203 6626709 0.99971 828260 82029 1327 58 0/0 302537/6626708
204 6624032 0.99936 828399 82123 1395 31 0/0 302744/6624031
205 6629301 1.00019 827356 81873 1345 112 0/0 302427/6629300
206 6617535 0.99837 826944 82326 1307 26 0/0 302146/6617534
207 6631055 1.00050 831255 81940 1351 149 0/0 303977/6631054
208 6632574 1.00032 827515 82299 1338 133 0/0 302252/6632573
209 6632019 1.00041 829099 81621 1320 123 0/0 303312/6632018
210 6630528 1.00034 831155 82701 1401 33 0/0 304514/6630527
211 6634502 1.00084 829229 82007 1278 30 0/0 302983/6634501
212 6629415 0.99993 827229 81883 1350 82 0/0 302001/6629414
213 6630076 1.00016 828498 82155 1384 53 0/0 302855/6630075
214 6625587 0.99950 827465 81391 1333 64 0/0 302148/6625586
215 6629162 0.99993 829059 81972 1365 185 0/0 303292/6629161
216 6625254 0.99930 826302 81516 1380 71 0/0 301815/6625253
217 6631400 1.00029 827845 82166 1313 147 0/0 302381/6631399
218 6627704 0.99978 828096 81756 1360 70 0/0 303083/6627703
219 6627623 0.99967 829233 82021 1301 145 0/0 303156/6627622
220 6629981 1.00025 828941 82357 1352 83 0/0 303101/6629980
221 6630931 1.00025 827999 81276 1325 130 0/0 302464/6630930
222 6629148 1.00008 829622 82322 1375 92 0/0 304229/6629147
223 6630633 1.00024 830893 82339 1259 58 0/0 304091/6630632
224 6625932 0.99968 829184 81997 1299 64 0/0 303065/6625931
```

Dispersion across the 24 chaining values (chi-square of the per-value counts against the pooled binomial rate, 23 degrees of freedom): C1 of claws 45.9 (p = 0.003), C2 of C1 27.3 (p = 0.243), G of C1C2 22.5 (p = 0.490), F7 of C1C2G 564.0 (p = 1.6e-104). Spread of the good-pair rate per claw: E[r^2]/E[r]^2 = 1.246 (r = all4/claws per chaining value; Poisson noise included, so an upper estimate).

### H.2 Part B: rows 17..21 forced-bit events within one chaining value (registered)

Registration of the run (SHA-256 and time recorded before the first counted pass: `da3a88cb4efe43e0c73100a0612b37cebeaa14605477d6c88edd74dcd8f917cb *PREREG_P1_PARTB_1021.md
2026-10-21T12:11:24-06:00`); Part B's text is Section 4 of PREREG_P1_Q3.md, reproduced in Appendix P.

```text
# PREREG_P1_PARTB_1021: Part B of PREREG_P1_Q3.md (10-17, SHA-256 efb3100b...), run on 2026-10-21
Written and hashed before the first counted pass. Part B was registered on 10-17 and never run (the cloud machine stopped during Part A). This run uses Part B's population, events, tests and decision rule UNCHANGED (PREREG_P1_Q3.md Section 4): ONE = cv seed 5001, 20,000 good pairs; MANY = cv seeds 6001..6200, 100 good pairs each; n0 = 2^25, window R = 0; tools p1pass.c (SHA-256 1327337a...) and p1ana.c (17d7e44d...), byte-identical to the 10-17 copies; every pass re-verified by p1ana (one failure voids the part).
Changes, all non-statistical: machine (our workstation, WSL, 8 threads, nice 10, prlimit --as=2^28) and date; time limit: each part under `timeout 1080` s (a part that times out is reported as not run).
Development before this text (not counted): one 500-pass run of p1pass on dev cv seed 31001 (timing, 6 s), analysed by p1ana (0 bad).
Tests (as registered): (i) each B_t count of ONE and of MANY against N p_t, z = (n - Np)/sqrt(Np(1-p)); (ii) ONE against MANY, z = (n1 - n2)/sqrt(n1 + n2); (iii) over-dispersion across the 200 chaining values of MANY for t = 19, 20, 21, chi2 = sum_i (n_i - 100p)^2/(100p(1-p)), 199 dof, two-sided p. Dependence DETECTED iff any |z| > 3.5 (15 tests) or any dispersion p < 0.001 or > 0.999.
```

Files hashed at the start (`2026-10-21T12:11:27-06:00`):

```text
1327337a2f59de317b87f6e68953346f99b9d0360786ba2dcf36eaa22b98e8f1  p1pass.c
17d7e44de5a8c9c2804529febbb28b6ffd1743ef99ab42715142d761ed37bd72  p1ana.c
a67db508dbd5a45de261d76c869413dcf62fabf8fa535ac62e073283c9937bed  sconsts.h
c47e5ec605a25ae03df29ada92f68c3462468262dc30730a1e201de335c8a14d  chi/chi38p8.txt
da3a88cb4efe43e0c73100a0612b37cebeaa14605477d6c88edd74dcd8f917cb  PREREG_P1_PARTB_1021.md
```

Run records: `ONE rc=0 132908 kB 2026-10-21T12:20:59-06:00; MANY rc=0 132716 kB 2026-10-21T12:30:40-06:00`.

Registered tests (p1ana output, `tests_B.txt`):

```text
ONE passes 17576 bad 0 | MANY passes 20000 bad 0, chaining values 200
E17: ONE 139 (exp 137.3, z +0.14) MANY 156 (exp 156.2, z -0.02) ONE-MANY z -0.99
E18: ONE 109 (exp 137.3, z -2.43) MANY 151 (exp 156.2, z -0.42) ONE-MANY z -2.60
E19: ONE 2244 (exp 2197.0, z +1.07) MANY 2504 (exp 2500.0, z +0.09) ONE-MANY z -3.77
E20: ONE 584 (exp 549.2, z +1.51) MANY 649 (exp 625.0, z +0.98) ONE-MANY z -1.85
E21: ONE 1125 (exp 1098.5, z +0.83) MANY 1304 (exp 1250.0, z +1.58) ONE-MANY z -3.63
E19 dispersion chi2 205.2 on 199 dof, two-sided p 0.734
E20 dispersion chi2 190.2 on 199 dof, two-sided p 0.680
E21 dispersion chi2 193.3 on 199 dof, two-sided p 0.798
max |z| 3.77; RESULT: DEPENDENCE DETECTED
```

ONE against MANY on rates, z = (n1/N1 - n2/N2) / sqrt(p(1-p)(1/N1 + 1/N2)): E17 +0.12, E18 -1.57, E19 +0.72, E20 +0.42, E21 -0.47.

## Appendix Q. Per-seed values of the base q3 runs (Section 9) and their registrations

- Level run, seeds 7001..7128: PREREG_Q3P8_B.md eb3310e43e0308e5658631226e09e9ab7d0403de9470dcd3b36545f9fee00f5a (hashed 2026-10-17 17:02:24 UTC; first seed 17:02:44 UTC); it references PREREG_Q3P8.md b1a2d290a3aad1b2c224be407ec9796e1fbf55d9ff2ea9bec9783aab76c0ae97. Tool traillab 17425aaa624561ceeb641977d72d86f6f4c1b8e57c6a05b7c82ad9ed1d12d485.
- Ratio run F2, seeds 10001..10400: PREREG_X1.md (Amendment 5) 628921f950e45c2c72f67c0d76af6011d664a4ca28ee0fe33813bde23f5dfd30 (hashed 2026-10-17 12:16:41 UTC; first seed 12:16:56 UTC).

Level: L_s = prefix_log2 + log2(exact_count / 2^28); registered bound mean(L) - t(0.99, 127) sd(L) / sqrt(128) = -96.42816. Ratio: G = log2(sum Xk / sum X0) = 0.50537, jackknife SE 0.03867, registered bound G - 2.34 SE = 0.41488.

~~~
# level run (PREREG_Q3P8_B): seed,prefix_log2,exact_count  (samples 2^28 per seed; L = prefix_log2 + log2(exact_count/2^28))
L,7001,-81.3715,10961
L,7002,-81.2237,10634
L,7003,-83.0084,10241
L,7004,-81.212,10754
L,7005,-81.5989,9338
L,7006,-82.286,7820
L,7007,-81.5131,10944
L,7008,-81.8333,10129
L,7009,-81.0088,10498
L,7010,-81.5667,11613
L,7011,-81.4103,9980
L,7012,-81.3556,9642
L,7013,-82.129,9618
L,7014,-81.407,11402
L,7015,-81.6177,10500
L,7016,-81.7261,10178
L,7017,-81.7814,9674
L,7018,-81.1822,9640
L,7019,-81.4372,10442
L,7020,-81.097,10744
L,7021,-81.3129,8978
L,7022,-82.2707,9334
L,7023,-81.1573,10671
L,7024,-81.1519,11133
L,7025,-82.0565,12864
L,7026,-81.7341,11518
L,7027,-81.077,9480
L,7028,-81.7966,9340
L,7029,-81.9692,10411
L,7030,-81.8644,11262
L,7031,-81.8492,9848
L,7032,-81.0318,10254
L,7033,-80.8443,11249
L,7034,-80.7981,10835
L,7035,-81.8896,9120
L,7036,-82.1805,11420
L,7037,-81.5903,9109
L,7038,-82.0164,10574
L,7039,-82.0059,8447
L,7040,-82.627,10207
L,7041,-81.9544,10134
L,7042,-82.2741,10330
L,7043,-82.6407,10059
L,7044,-80.4355,10409
L,7045,-82.363,11770
L,7046,-81.6353,9294
L,7047,-81.0005,9730
L,7048,-82.6376,12409
L,7049,-81.4655,9077
L,7050,-81.6089,8522
L,7051,-81.7793,10786
L,7052,-81.4855,9271
L,7053,-82.584,9961
L,7054,-81.1668,9574
L,7055,-82.299,8608
L,7056,-82.3064,11499
L,7057,-80.8095,9895
L,7058,-81.0654,11129
L,7059,-81.5981,9695
L,7060,-81.618,9934
L,7061,-81.2075,10783
L,7062,-82.0255,9999
L,7063,-80.8514,10990
L,7064,-81.5843,9838
L,7065,-81.8012,12344
L,7066,-82.2935,10158
L,7067,-81.6483,11042
L,7068,-81.6822,11170
L,7069,-81.4176,9738
L,7070,-81.7532,10521
L,7071,-81.1694,9811
L,7072,-81.9733,8147
L,7073,-81.4528,12212
L,7074,-81.3789,10598
L,7075,-81.3163,11188
L,7076,-81.3546,10805
L,7077,-80.6791,9328
L,7078,-80.8915,11047
L,7079,-81.4507,9590
L,7080,-82.0555,14439
L,7081,-80.9598,11567
L,7082,-81.7905,10128
L,7083,-81.679,10807
L,7084,-81.9692,9793
L,7085,-81.6493,10218
L,7086,-82.2675,12192
L,7087,-81.8574,10311
L,7088,-81.8021,10686
L,7089,-82.1201,10557
L,7090,-82.0163,10293
L,7091,-82.0332,9893
L,7092,-82.596,10243
L,7093,-81.966,9400
L,7094,-82.0325,10797
L,7095,-81.0504,10307
L,7096,-81.7908,11427
L,7097,-80.9781,9547
L,7098,-81.7915,10918
L,7099,-81.1962,10154
L,7100,-81.5516,11064
L,7101,-81.2837,10561
L,7102,-81.6309,10878
L,7103,-83.0446,7809
L,7104,-80.5101,11040
L,7105,-81.2544,10202
L,7106,-80.9157,11310
L,7107,-82.1957,11088
L,7108,-80.5423,10580
L,7109,-81.0267,10121
L,7110,-82.5614,13019
L,7111,-81.806,9196
L,7112,-80.6369,10583
L,7113,-81.8203,9696
L,7114,-81.6757,11446
L,7115,-81.3278,11038
L,7116,-82.0319,11295
L,7117,-81.8272,9505
L,7118,-81.5061,9582
L,7119,-81.2448,10519
L,7120,-82.0173,10523
L,7121,-81.6134,10193
L,7122,-81.1283,10174
L,7123,-81.7614,8065
L,7124,-82.6067,10212
L,7125,-81.5096,10874
L,7126,-81.5263,10348
L,7127,-82.6019,11354
L,7128,-82.0752,8305
# ratio run F2 (PREREG_X1 Amendment 5): seed,X0,Xk  (linear per-seed estimates x 2^96 of the base and relaxed events; dead seed = 0)
R,10001,0,0.9281277
R,10002,1.006835,1.006835
R,10003,0,0
R,10004,2.442087,2.442087
R,10005,0,0
R,10006,0.6885427,0.6885427
R,10007,0,0.7482195
R,10008,1.245815,2.294923
R,10009,0,1.183819
R,10010,1.862596,1.862596
R,10011,0,0
R,10012,1.151722,1.151722
R,10013,1.94911,2.479701
R,10014,1.325574,2.833167
R,10015,0,0
R,10016,0.8232038,0.8232038
R,10017,0.6216205,0.6216205
R,10018,0,0
R,10019,1.495375,1.495375
R,10020,0.6288989,1.459242
R,10021,1.571213,2.901789
R,10022,0,0
R,10023,0.9025339,1.785012
R,10024,2.00611,2.00611
R,10025,0,0.3887652
R,10026,0.7026895,0.7026895
R,10027,0.3110605,0.3110605
R,10028,0,0.951372
R,10029,1.429517,2.694451
R,10030,0,0.5839011
R,10031,1.341414,2.534174
R,10032,0,0
R,10033,0.5726884,2.013086
R,10034,0,0
R,10035,1.50335,1.50335
R,10036,0,0
R,10037,2.556076,2.556076
R,10038,0,0
R,10039,1.212667,1.212667
R,10040,2.064467,2.064467
R,10041,0,1.388778
R,10042,1.054881,1.708392
R,10043,0.4714009,0.4714009
R,10044,0.9854011,1.305656
R,10045,1.351585,2.391001
R,10046,2.249487,2.249487
R,10047,0,0.9651581
R,10048,0.7392302,0.7392302
R,10049,1.118467,1.118467
R,10050,0,0
R,10051,0,0
R,10052,0,0
R,10053,0,0
R,10054,0,0
R,10055,0,0
R,10056,0.7389259,1.218363
R,10057,0,1.07037
R,10058,1.886001,1.886001
R,10059,0,0
R,10060,1.570131,2.492149
R,10061,1.636427,1.636427
R,10062,0,0
R,10063,1.085199,1.085199
R,10064,0.8541374,0.8541374
R,10065,0,0
R,10066,2.885537,2.885537
R,10067,0.9890864,0.9890864
R,10068,0,0.8081806
R,10069,0,0
R,10070,1.052451,1.052451
R,10071,0,0.6342957
R,10072,0.5469453,0.5469453
R,10073,3.244172,3.244172
R,10074,1.279995,1.279995
R,10075,2.1942,2.1942
R,10076,1.020947,1.020947
R,10077,0,0
R,10078,3.151282,3.151282
R,10079,0,0
R,10080,0,0
R,10081,2.201495,2.89953
R,10082,0.5322888,1.337605
R,10083,0,0.8123574
R,10084,0,0
R,10085,2.64376,3.594222
R,10086,0,0.7097606
R,10087,0.7130816,1.124734
R,10088,1.391683,2.205282
R,10089,1.329652,1.329652
R,10090,0,0
R,10091,1.298209,1.298209
R,10092,0,0
R,10093,0,0
R,10094,0,0
R,10095,1.591822,1.959952
R,10096,3.2257,3.2257
R,10097,0,0.6350302
R,10098,0,0.970039
R,10099,0.6547256,1.521203
R,10100,1.154524,1.154524
R,10101,1.020515,1.583899
R,10102,0,0
R,10103,0.9602013,0.9602013
R,10104,0.7797537,1.716424
R,10105,1.538413,1.538413
R,10106,3.458623,5.426605
R,10107,2.434904,2.434904
R,10108,1.023864,2.370468
R,10109,0.9788162,1.630528
R,10110,0.7121826,1.808033
R,10111,0,1.930493
R,10112,1.639378,2.329072
R,10113,0.4325059,0.4325059
R,10114,2.794344,2.794344
R,10115,1.900645,2.916681
R,10116,0.7634711,2.406752
R,10117,0.5696623,0.5696623
R,10118,0,0
R,10119,0,0
R,10120,2.87533,3.38362
R,10121,1.796416,1.796416
R,10122,0,0.8290385
R,10123,0,0
R,10124,0.8308606,0.8308606
R,10125,2.060964,2.997765
R,10126,0.9226925,0.9226925
R,10127,2.332842,2.332842
R,10128,1.282092,2.54916
R,10129,0.8846184,1.6155
R,10130,0,0
R,10131,0,0
R,10132,2.3076,2.772958
R,10133,0.4514547,3.235425
R,10134,0,0
R,10135,0.8592967,0.8592967
R,10136,0,0.3811694
R,10137,0,0
R,10138,0,0
R,10139,0,0.6220679
R,10140,0.5361133,1.337548
R,10141,0.6334565,2.556449
R,10142,0.7898796,0.7898796
R,10143,1.265516,1.265516
R,10144,0.7144834,0.7144834
R,10145,0,0
R,10146,1.364234,1.364234
R,10147,1.272447,1.272447
R,10148,1.282024,1.282024
R,10149,1.014554,1.014554
R,10150,0,0
R,10151,2.364591,2.364591
R,10152,0.997314,0.997314
R,10153,0.898366,0.898366
R,10154,0,0
R,10155,2.316413,2.316413
R,10156,0,0
R,10157,1.609583,1.609583
R,10158,0.4877785,0.4877785
R,10159,0,0.4124104
R,10160,1.639941,1.639941
R,10161,0.645703,0.645703
R,10162,0.6496905,0.6496905
R,10163,1.175697,1.175697
R,10164,1.117999,1.117999
R,10165,1.990315,2.954545
R,10166,0,0.7581706
R,10167,0.45893,1.506102
R,10168,0.822564,1.512529
R,10169,0.9417453,0.9417453
R,10170,0.8425465,0.8425465
R,10171,0.6311242,1.893373
R,10172,0.8915027,0.8915027
R,10173,0.3543698,0.7273906
R,10174,1.550933,2.288198
R,10175,1.291029,1.291029
R,10176,1.588314,2.155809
R,10177,1.004757,2.561424
R,10178,0,1.485154
R,10179,0,1.579497
R,10180,0,0
R,10181,0.4121239,0.8725833
R,10182,0.6859813,0.6859813
R,10183,0,1.071299
R,10184,1.250952,1.250952
R,10185,1.015728,1.764917
R,10186,0.9319799,0.9319799
R,10187,0,0.9663574
R,10188,0.8575195,1.560736
R,10189,1.698156,1.698156
R,10190,0.7354357,0.7354357
R,10191,0,0
R,10192,0.9995321,0.9995321
R,10193,0,0
R,10194,0.5484237,0.5484237
R,10195,0,0
R,10196,0,0.8796423
R,10197,0.4949941,0.4949941
R,10198,0,0.8647544
R,10199,0.7214206,1.655423
R,10200,1.070582,1.070582
R,10201,0.869085,0.869085
R,10202,0.6591974,1.576126
R,10203,1.779813,1.779813
R,10204,2.702336,3.149586
R,10205,0,0
R,10206,0.9042895,1.829131
R,10207,0,0
R,10208,0,0
R,10209,0.3365096,0.3365096
R,10210,1.012305,1.012305
R,10211,0.5767287,0.5767287
R,10212,0,0
R,10213,0.6680543,0.6680543
R,10214,0.6922278,0.6922278
R,10215,0.9099687,1.420616
R,10216,0,1.38764
R,10217,0,0
R,10218,1.496756,1.496756
R,10219,0,0
R,10220,0.9929262,0.9929262
R,10221,0,0.6654608
R,10222,1.923922,1.923922
R,10223,0.7430274,1.21219
R,10224,0,0.5555327
R,10225,0,0.4499109
R,10226,0.8496979,0.8496979
R,10227,0,0
R,10228,2.269728,3.547865
R,10229,0,0
R,10230,1.94005,2.69329
R,10231,0.7683553,2.180666
R,10232,0,0
R,10233,1.958021,1.958021
R,10234,1.400893,1.400893
R,10235,0.7864194,1.795363
R,10236,1.055981,1.055981
R,10237,0,1.328123
R,10238,0.8052687,0.8052687
R,10239,0.656664,0.656664
R,10240,1.424754,1.424754
R,10241,0,0
R,10242,1.072733,1.072733
R,10243,0,0
R,10244,1.816788,2.488107
R,10245,0,0
R,10246,2.877305,2.877305
R,10247,0,0.6983921
R,10248,1.90508,1.90508
R,10249,3.109547,3.616943
R,10250,1.527085,2.03363
R,10251,1.018428,1.018428
R,10252,1.189139,1.596345
R,10253,2.12171,2.704482
R,10254,2.05652,2.05652
R,10255,1.780576,2.506531
R,10256,1.420919,1.420919
R,10257,0,0
R,10258,0,0
R,10259,0,1.443166
R,10260,0,0
R,10261,2.95313,2.95313
R,10262,1.794076,2.755849
R,10263,1.092247,1.092247
R,10264,1.456213,1.456213
R,10265,2.334258,2.334258
R,10266,1.210093,2.006017
R,10267,0.8712293,0.8712293
R,10268,0,0
R,10269,0.8064632,0.8064632
R,10270,1.860444,1.860444
R,10271,1.851992,2.791298
R,10272,1.722623,3.829385
R,10273,0,0
R,10274,0,0.8632901
R,10275,0,0
R,10276,0.7539742,0.7539742
R,10277,1.716739,1.716739
R,10278,1.106052,1.106052
R,10279,0.5252586,1.099981
R,10280,0.9213367,0.9213367
R,10281,0,0
R,10282,0,0
R,10283,0,0
R,10284,0,0
R,10285,2.187207,2.187207
R,10286,0.6482929,0.6482929
R,10287,0,0.6342823
R,10288,1.194657,2.577183
R,10289,0,0
R,10290,0,0
R,10291,0,0.8552015
R,10292,0.5968955,0.5968955
R,10293,0,0
R,10294,0.6249789,0.6249789
R,10295,0,0
R,10296,0.5325172,1.549792
R,10297,0.8903379,1.56663
R,10298,0.8646637,1.388403
R,10299,1.673583,1.673583
R,10300,0,0
R,10301,0.8582208,0.8582208
R,10302,0,0
R,10303,0,0
R,10304,1.566598,1.566598
R,10305,0,0.3820462
R,10306,1.923467,3.827455
R,10307,1.621908,2.13469
R,10308,1.144444,2.624871
R,10309,0.6941518,1.775121
R,10310,2.04408,2.765306
R,10311,1.011446,1.769069
R,10312,1.272745,1.272745
R,10313,0,0
R,10314,3.019173,3.575648
R,10315,2.327982,2.327982
R,10316,0.6296267,0.6296267
R,10317,1.577948,1.577948
R,10318,1.771852,1.771852
R,10319,0,0.4219317
R,10320,0,0
R,10321,1.728547,1.728547
R,10322,0,2.723642
R,10323,0,0.9323999
R,10324,0,0
R,10325,0.6485064,0.6485064
R,10326,0.5688346,1.57504
R,10327,0,0
R,10328,0,0
R,10329,1.51718,2.128316
R,10330,2.833669,2.833669
R,10331,0.711626,0.711626
R,10332,1.726907,1.726907
R,10333,3.083568,3.083568
R,10334,0,0
R,10335,0.6742766,0.6742766
R,10336,1.481735,3.825395
R,10337,1.532606,2.198957
R,10338,1.065839,1.756073
R,10339,2.267965,2.267965
R,10340,0,0.45208
R,10341,2.279857,3.116672
R,10342,1.068132,1.786737
R,10343,0,0
R,10344,0,1.41416
R,10345,0.9472289,1.703616
R,10346,1.281463,1.281463
R,10347,0,0.6487455
R,10348,1.08904,1.08904
R,10349,0,1.039966
R,10350,0.7064984,1.530331
R,10351,0,0
R,10352,2.816989,2.816989
R,10353,0,0.6575495
R,10354,0,0.7888445
R,10355,0.9892791,0.9892791
R,10356,0.611843,0.611843
R,10357,0.6763418,1.578131
R,10358,1.198657,1.198657
R,10359,1.540558,3.195618
R,10360,1.151237,1.151237
R,10361,1.692953,1.692953
R,10362,0,0
R,10363,0.9422333,0.9422333
R,10364,1.244869,1.244869
R,10365,0,0
R,10366,0,0.6058029
R,10367,1.231212,1.776718
R,10368,0.7100559,0.7100559
R,10369,1.334651,2.026511
R,10370,0,0
R,10371,0.9955977,1.519359
R,10372,0.806232,2.539254
R,10373,0,0
R,10374,0.6464383,0.6464383
R,10375,0,0
R,10376,3.111893,3.111893
R,10377,0.9036278,1.486385
R,10378,1.23934,1.23934
R,10379,0.8546721,0.8546721
R,10380,1.022096,1.753287
R,10381,0,0
R,10382,0,0
R,10383,0.9909144,0.9909144
R,10384,0,1.019004
R,10385,1.877494,1.877494
R,10386,2.059244,2.059244
R,10387,1.554703,1.554703
R,10388,0,0
R,10389,0,0
R,10390,1.594233,1.594233
R,10391,0,0
R,10392,0,1.4196
R,10393,0,1.519391
R,10394,0.9854348,0.9854348
R,10395,0.6165324,1.37731
R,10396,0,0.8508295
R,10397,0,0
R,10398,0,0
R,10399,2.015821,2.015821
R,10400,0,0.7052653
~~~

## Appendix R. Records of the A0-variant line (reproduced from the proof of our 9aaf71a2; section numbers inside refer to that proof; script sources omitted; in R.1 to R.3 the word procedure is replaced by procedure)

*Reading note for this filing.* Appendices P, Q, H and R are records reproduced verbatim from the lineage (9aaf71a2, 51613d1c, 09f6ba2d). Their section, appendix, experiment and program references (for example the lineage's Sections 13-14, its A.9-A.14 and R.8, its organizer experiments `a0-online-r38`, its memory claims 27.069 and 28.094, its allowance discussion) refer to those filings and are not part of this filing's claim; the binding statements are Sections 1-14 above.

### R.1 The q3 runs of q3_model (9aaf71a2 Sections 7.4, 7.5, Appendices A.11, A.12)

### 7.4 The preregistered measurement of q3 (H2's declared value)

*Tool.* `traillab` (our own C program, written in this project with Claude Code; the tool that measured fb176310's declared value; not shipped: the experiment sources are limited to 65,536 bytes) estimates rates of a 38-step characteristic by sequential Monte Carlo on real compressions: every sample is a chaining value and W0..W15 of both members with the real message expansion, the state is replayed from the words (0 replay mismatches are required), rows 16..21 are the prefix (E-driven: E_t^x chosen, W_t from it, W0..W5 solved by the inverse expansion; 8,192 particles, 256 proposals per particle per row) and rows 22..37 the window, with the late words of the procedure redrawn for every window sample (W6 uniform, W7 uniform in F7, W8 from a list). For each window sample it counts EXACT (zero output difference after step 37). With `--autolist` the row-16 stage is exact: the tool enumerates the E16 values that pass row 16 under the prefix conditions (160 values, enumerated over 2^24 candidates; the same set as Section 6) and weights the stage 160/2^32. Its model of P8 is our transcription `chi38p8.txt` (the cells of Section 3; anchor row 15: S's rows 12..15 held); its prefix conditions are exactly the tests of rows 16..21 of the accepted event (cells, '+' pairs, two-bit conditions keyed at the larger row; row 19 signed only). Per seed, log2 q3 = prefix log2 P(rows 16..21) + log2 rate(EXACT) (the tool labels its prefix "rows 7..21", from the lowest row with a condition; rows 7..15 are held at S and pass with probability 1, so the prefix is rows 16..21). The tool reproduces fb176310's preregistered value exactly with the same seeds (2^-97.6619 for the published characteristic) and passed its validation suite (48 of 48 quick known-answer tests: exact counts of the row-16 sets and of F7, the flip tables, digests of the pairs).

*Preregistration of the declared run* (`PREREG_Q3P8_B.md`, Appendix A.12; written and hashed, SHA-256 eb3310e43e0308e5658631226e09e9ab7d0403de9470dcd3b36545f9fee00f5a, 2026-10-17 11:02:24 MDT, before the first seed, which started at 11:02:44 MDT): the quantity, the tool and the inputs of the earlier run below (binary 17425aaa..., `chi38p8.txt` c47e5ec6..., `sel_members.txt` ff582e64...); 128 fresh seeds 7001..7128, each 2^28 window samples (8,192 particles x 32,768), one process per seed (the generator streams are indexed by the seed, so a seed gives the same counts in one process or in a multi-seed process), W8 drawn from the list of the 196,608 selected variants (`--var "W8 a0list @sel_members.txt late"`), row 16 exact. Per-seed value L_s as above (a dead seed or 0 EXACT counts as -128); declared value q3_base = the one-sided 99% Student lower bound over the 128 values, mean - t sd / sqrt(128) with t = 2.3556 as registered, rounded down to 4 decimals (the seed is the cluster), over these 128 seeds only (the seeds of the earlier run are not pooled); halves 7001..7064 / 7065..7128; diagnostics required 0 (a non-zero diagnostic in any seed voids the run); no interim look, no stopping rule, all 128 seeds used. Use rule: if the run is not void and q3_base > -96.5755, the next filing uses q3_model = q3_base x 2^0.4149 (the gain of Section 7.5, unchanged); otherwise nothing changes.

*Results* (cloud machine, 2026-10-17 17:02:44 to 17:45:42 UTC; every diagnostic 0: prefix broken by the redraw 0, y-anchor inconsistent 0, replay mismatches 0; dead seeds 0; 1,326,458 EXACT events, at least 7,809 per seed):

| run | statistic (log2) | mean | seed sd | declared 99% lower bound | half 1 / half 2 |
|---|---|---:|---:|---:|---|
| **128 seeds 7001..7128 (declared)** | q3 (rows 16..21 prefix + EXACT) | -96.3123 | 0.5563 | **-96.4282** | -96.3328 / -96.2918 |
| 32 seeds 5001..5032 (earlier run, Appendix A.9) | q3 (rows 16..21 prefix + EXACT) | -96.3251 | 0.5774 | -96.5755 | -96.3137 / -96.3365 |

The 128 per-seed values, the script that computes the declared value from the logs and its output are in Appendix A.12. With the exact Student quantile t(0.99, 127) = 2.3561 (the registered value is 2.3556) the bound is -96.42816, which rounds down to the same -96.4282.

*The earlier run* (`PREREG_Q3P8.md`, Appendix A.9; hashed with its run script before its first seed, 2026-10-14 15:00:08 MDT): 32 fresh seeds 5001..5032 of the same tool, inputs and command, declared bound over its 32 values with t(0.99, 31) = 2.4528: mean -96.3251, bound -96.5755, 326,084 EXACT events, every diagnostic 0. It was repeated under an address-space cap of 2^28 bytes (Section 13.4) and every per-seed output is identical. The 128-seed run was registered after it, with the use rule above (its bound replaces the earlier one if it is higher); The 32 seeds are not used in the bound below (one multi-seed process; pooled with the 128 seeds the bound would move by +0.0075 bit).

*Estimator and bound (analysis of the registered run; the registered statistic, the Student bound of the mean of L_s, is 2^-96.4282 and stays in the table).* The value of a seed is an estimate of q3 that is unbiased on the linear scale: the prefix is the product of the stage means of a sequential Monte-Carlo sampler with a fixed schedule and multinomial resampling of equally weighted children (the stage-16 factor 160/2^32 is exact), the last factor is the fraction of the seed's 2^28 window samples with zero output difference, drawn from the resampled particles, and a seed whose population dies counts 0 (none of the 128 did). The quantity bounded is q3, so the statistic is the arithmetic mean of the 128 values 2^(L_s) (the mean of L_s is lower by the Jensen gap 0.1035 bit). Result: mean 2^-96.2088, coefficient of variation 0.3820, standard error 0.0487 bit; one-sided 99% Student lower bound (t = 2.3561) 2^-96.3285 (rounded down). Bootstrap-t 2^-96.3210, BCa 2^-96.3193 and the lognormal (Cox) interval 2^-96.3252 agree within 0.01 bit; the L_s are normal (Shapiro p = 0.72) and a simulated lognormal population with this spread gives the Student bound a coverage of 99.5%. The level is confirmed by estimators that do not share its seeds: the 400 seeds of Section 7.5 give 2^-96.2567 (standard error 0.072 bit) for the same event with a different sampler structure; the replica of Section 7.3 (a lower-bound estimator) has mean 2^-96.3095; 1a695f0b's estimator gave 2^-96.3683.

### 7.5 The relation E18 = E17 is not imposed: the measurement of the gain (F2)

**What changes.** Besides the cells, the accepted event of Section 6.1 used to impose the '+' relation of the printed row 18, E18 = E17 on bits 24, 23, 15 (mask 01808000; `PQ[18]`). This filing does not test it: the event uses `PQE`, which equals `PQ` except `PQE[18] = 0`. Every pair the earlier event accepts is still accepted (one test was removed), every accepted pair is still a collision (Lemma 6.1), and the cost does not rise: the counted path of step 3b loses the 4 operations of the removed test, 2,825 operations per row-16 pass instead of 2,829, and the ledger charges every row-16 pass at this longest path (Section 11).

**Why it adds collisions.** The output difference of E20 must vanish: dE20 = dE16 + dS1(E19) + dCH(E19, E18, E17) (dW18 = dW20 = 0 on the path). E19 differs at bits 24, 23, 15, and CH(E19, E18, E17) is then the same for both members at those bits exactly when E18 = E17 there; that is the printed relation. If E17[24,23] = 10 and E18[24,23] = 01 instead, dCH changes by -2^24 + 2^23 = -2^23, and dS1(E19), a signed sum of the nine powers 2^b, b in {31, 30, 22, 18, 17, 13, 12, 9, 4} (the sign of each is a bit of S1(E19x)), absorbs it through the other sign of its term 2^22, a change of 2^23. Example, one sample of the tool (it rebuilds every sample from the 16 message words and the chaining value and replays both members, Section 7.4): E16x = cb3ad724, E17x = 2b08cc08, E18x = 02dbd786, E18y = 02dfd796, E19x = e65badfa, E19y = e7db2dfa, E20x = E20y; dE16 = c03dee00, dS1(E19) = 404211f0, dCH = ff800010, and the three add to 0 mod 2^32 (checked in Python). The extra patterns need particular values of the E17 bits, which the printed row 17 leaves free, so the added mass differs from lineage to lineage; the gain below is the mean over the lineages that the sampler draws.

**Estimator and its check.** `traillab window --rows 17 21 --event out --relax NAME=OPS` (the tool of Section 7.4, binary 17425aaa...) proposes E17..E21 uniformly inside the union of the cell events of the printed set and of the named relaxation (the relaxation contains the printed set), builds every final sample from message words, replays both members, and counts on the SAME samples J0 = (zero output difference after step 37 and the printed cells and relations of rows 17..21) and Jk = (zero output difference and the relaxed cells of rows 17..21). Prefix and carrier are common, so q3(relaxed event) / q3(printed event) = sum_s w_s Jk_s / sum_s w_s J0_s with the seed weights w_s = 2^(prefix_s + carrier_s) printed on the "prefix log2 ... window carrier log2 ..." line of each seed. Check on a known answer, run first (V0, seeds 9001..9008, 2^27 final samples each): fb176310's law (chi38.txt) with the arm A of D250 (the four E19 patterns and the E20 tie) gives 1.9917 bit (jackknife SE 0.0835), against +2.0368 bit measured separately by paired prefix arms (D250, 32 seeds): 0.045 bit apart.

**Scan of the other relaxations of rows 17..21.** Nine more relaxations were measured alone on four seeds (9401..9404, 2^23 final samples each): the value-only cells of E17 (7 bits), E18 (5), E20 (5), E21 (3), the relations E17 = E16 and E20 = E19, the two-bit conditions of A17, E18 and E21. In every one the EXACT samples of the relaxation were exactly the EXACT samples of the printed set (J0 = Jk in every seed, 143 to 1,360 EXACT samples per arm; the added regions of E20 = E19 (half of the mass) and of E21 (7/8 of the mass) hold no EXACT sample among about 4 million samples per seed). Only the relation E18 = E17 adds collisions, and only through its bits 24 and 23 (in F2 the bits 24 and 23 alone give the same counts as all three, and bit 15 alone adds none; in the 19 seeds of the second launch of the earlier 32-seed design, bit 24 alone and bit 23 alone added none either).

**Preregistration and result (F2).** `PREREG_X1.md` (SHA-256 of the registered text and of the scripts in Appendix A.11), written before the first seed of the run, fixes: 400 fresh seeds 10001..10400, `--np 8192 --mt 2048` (2^24 final samples per seed), one process per seed, `prlimit --as=2^28`, `MALLOC_ARENA_MAX=1`, 2 MiB thread stacks, 8 threads, nice 10, on the cloud machine; the statistic G = log2(sum_s w_s Jk_s / sum_s w_s J0_s) with a delete-one-seed jackknife standard error over all 400 listed seeds (a seed whose population dies at a window stage is an entry with zero weight, not dropped); the rule: if LB99 = G - 2.34 SE exceeds 0.10 bit the declared gain is LB99 rounded down to 4 decimals. Three earlier launches of a first design (32 seeds at 2^27 samples each) preceded it: the first two crashed in the tool in the seed after the first dead seed (a defect of the tool, worked around by one process per seed), the third (one process per seed) was stopped after 19 seeds because the lineage lottery, not the sample count, limits the precision (its pooled gain over the 19 seeds was +0.75 bit, SE 0.37); the design was changed to many small seeds before any F2 seed was run, and the numbers of those launches are not used.
Result: of 400 seeds 306 had a live population (94 died at stage 20, as in the printed-cell runs), all diagnostics 0 (prefix broken by redraw, y-anchor inconsistent, replay mismatches); pooled J0 = 143169 and Jk = 203960 EXACT samples; **G = 0.5054 bit (ratio 1.420), jackknife SE 0.0387, LB99 = 0.4149 bit**; the unweighted pooled value is 0.5106. Seeds with J0 = 0 and Jk > 0: 53; with Jk = J0 > 0: 154; with Jk > J0 > 0: 99. The arm with bits 24 and 23 only has the same counts as the arm with all three bits (J0 143169, Jk 203960); the arm with bit 15 alone has Jk = J0 (143169 against 143169). Peak resident memory of a seed process: at most 219,048 KiB = 2^27.74 bytes under the cap 2^28.
**Declared gain 0.4149 bit.**

**Use.** log2 q3_model = log2 q3_base + log2 R, with q3_base the level of Section 7.4 (seeds 7001..7128) and R the ratio of this section (seeds 10001..10400). The two estimates come from different runs and seeds, so their errors are independent and the standard error of the sum is the root of the sum of squares. Estimate -96.2088 + 0.5054 = -95.7035; standard error sqrt(0.0487^2 + 0.0387^2) = 0.0622 bit; one-sided 99% lower bound -95.7035 - 2.34 x 0.0622 = -95.8491 (rounded down; 2.34 is t(0.99) at the about 300 effective degrees of freedom). **q3_model = 2^-95.8491.** Checks: a joint bootstrap over the seeds of both runs (200,000 draws) has its 1% quantile at -95.8467; in bootstrap worlds built on the observed seeds the rule covers 99.1%; the two separate 99% bounds multiplied (2^-96.3285 x 2^0.4149 = 2^-95.9136, confidence at least 98%) are shown for comparison; the 400 seeds of this section also estimate q3 of the relaxed event directly, 2^-95.7513 (standard error 0.060 bit, one-sided 99% Student bound 2^-95.8982). The H3 measurement of Section 13.5, the replica of Section 7.3 and its calibration are those of the printed-cell event, as before.

**Not covered.** (a) H3 was not re-measured on successes with E18 different from E17: its successes come from the replica, which does not propose them; the premise counts row-16 passes only. (b) The ratio is a ratio of two Monte-Carlo estimates of one tool over the lineages that tool draws (a few clusters per seed); its precision is that of the 400 seeds. (c) The extra patterns were measured with W8 from the 196,608 selected variants and the real message expansion, like q3 itself; no collision was built by the counted program in a run (none is expected at our scale). (d) The relaxations of other rows were measured on four seeds each (the scan above), at the power stated there.


### A.11 The shared-carrier measurement of Section 7.5: registration, scripts and counts

Files of the run, in the order they were written (SHA-256 recorded in `prereg_x1_hashes.txt` at the time of writing; the line after each file name is the hash of the file as it stands here; the registered text `PREREG_X1.md` is below with its amendments, each dated before the runs it governs; clock times are MDT, 2026-10-17):

```text
628921f950e45c2c72f67c0d76af6011d664a4ca28ee0fe33813bde23f5dfd30  PREREG_X1.md
516e6141e9bb080cfa5a274b739925056b8f6988356b44de58c0856872e3e035  run_x1.sh
e3f1f0c71f21ff46a8a2f663ee76f6a516a04589c95d12c9a3705d66960ce386  run_x1b.sh
d5ab95030d741acb66382787b09f4cb8d6d4d1298f11bf39cfb8594a0e6b4e57  run_x1c.sh
84127cca6451b33e29951f7ee77417f66725b225d8c8236037d2fb363497b41c  run_x1e.sh
572d9d25cb7b9281306649643b9e19b0f0a9a01012a37c0d38f641c7f2440a50  run_x2.sh
131f93f1f062581758c4375ab1e14e1508cac53d2a0d0b0560d30cd69863a4eb  anal_x1.py
f75225137f48d435c671089026f7407acc4e79d85cde20471546e78e3d12739a  anal_x2.py
```

The binary is the one of Appendix A.9 (SHA-256 17425aaa624561ceeb641977d72d86f6f4c1b8e57c6a05b7c82ad9ed1d12d485), the model file `chi38p8.txt` (c47e5ec6...), `chi38.txt` (0ad7712e...) and `sel_members.txt` (ff582e64...) those of Section 13.4, on the cloud machine in `/root/r38x`. `run_x1.sh` ran the stage-M part (its ratio-stage part was cancelled, see the amendments), `run_x1b.sh` ran V0 (its F1 launch crashed), `run_x1c.sh` and `run_x1e.sh` are the crashed and the stopped launches, `run_x2.sh` is F2.

#### A.11.1 The registered text with its amendments (`PREREG_X1.md`)

```text
# PREREG_X1: P8 value-cell relaxations of rows 17..21 by the shared-carrier ratio (written before any counted seed)

Written 2026-10-17 05:53 MDT (11:53 UTC) by the R38X session; the first run started 05:55:16 MDT. Nothing here stages, files or submits anything.

## Why

The package d7fdf556 (R38P8S, a0hoist38.py) already has the exact collision event of R37R: `row_check` returns True for every row >= 22 (a0hoist38.py line ~499),
step3b computes rows 16..37 and accepts iff the eight words A34..A37, E34..E37 of the two members are equal, and the preregistered q3 of Section 7.4 counts
"zero output difference after step 37" on the prefix of rows 16..21 (the log lines "cells rows 22..37 ... rate 0.5" and "EXACT" of Appendix A.9 show it).
D783-STACK (A: four E19 patterns + E20 tie, B: exact output event over the rows 22..37 cells) was measured on chi38 (fb176310's law). On P8 its B part is already in
the event and its A part is the identity: P8's row 19 is signed differences only (no value-only bit) and its E20 '+' pair is the tie. So no D783 factor transfers.
What the exact-event idea still allows for P8 is to stop checking value-only cells of rows 17..21 (the "last checked row" idea of R37R, applied to cells instead of rows):
a dropped cell adds mass to the prefix and may or may not keep colliding. Earlier tests (F2-1014-R38-P8-ROW20-21-RELAX: r20 -0.066 +- 0.162, r21 -0.027 +- 0.013;
F3-1014-R38-P8-ROW18-RELAX: +0.77 +- 0.70) used separate prefix arms and were limited by SMC noise (sd 0.3 to 1.4 per seed). This run uses the tool's own
shared-carrier mode, which counts the base cells and each relaxation on the SAME samples, so the prefix noise cancels in the ratio.

## Estimator (traillab, our own C; binary sha256 17425aaa624561ceeb641977d72d86f6f4c1b8e57c6a05b7c82ad9ed1d12d485, the one of Appendix A.9)

`window --rows a 21 --event out --relax "<name>=<ops>"`: the E-driven window stages a..21 propose E_t uniformly inside the union of the cell events of the base and of the named relaxation(s)
(the relaxations only drop conditions, so the base cells are contained in every relaxation); every final sample is checked against the base cells and against each relaxation
on rows a..21 and against "zero output difference after step 37". With J0 = samples that are EXACT and follow the base cells on rows a..21 and Jk = samples that are EXACT and follow relaxation k on rows a..21:
**q3(relaxation k) / q3(base) = Jk / J0** (same prefix, same carrier, the carrier mass cancels), so the gain in bits is log2(Jk / J0). Window rows a..21 carry the base cells of the printed model
(chi38p8.txt; rows 22..37 carry only the cell E22[29] = 0, which is not part of the counted event and is not tested here).

## Validation on a known answer (must pass before any P8 number is used)

V0: chi38.txt (fb176310's characteristic), `--rows 19 21`, relaxation A = "dropv E19 30040e32 ; dropv E20 20000000 ; lin E20[29]^E19[29]=0" (the arm of D250, research/prereg_D250_r38.md,
whose separately-run paired value is +2.0368 bit, 99% lower bound +1.9534). Seeds 9001..9008, np 8192, mt 16384 (2^27 final samples per seed), 8 threads.
Rule: V0 passes iff the pooled gain log2(sum JA / sum J0) is within 0.35 bit of +2.0368 (the jackknife standard error is reported). If it does not pass, the shared-carrier ratio is not used for P8 and the scan is void.

## Stage M, the mass screen (added 05:54 MDT, before any counted seed; the second smoke below motivated it)

Disclosed smoke 2 (P8, rows 18..21, arm r18v, seed 1, np 8192, mt 1024, 8,388,608 final samples, 328 EXACT): EVERY final sample follows the base cells ("cells rate 1.000000", J0 = Jk = 328),
although the carrier accepts E18 on the union of base and r18v: the relaxed-only E18 values die at rows 19..21, so the five value-only bits of E18 add no surviving mass in this seed.
Stage M runs each arm ALONE, seeds 9401..9404, np 8192, mt 1024 (2^23 final samples per seed), 8 threads, the flags below, and records the base fraction b = (final samples following the base cells) / (final samples)
and J0, Jk. It is a quick look only (about 5 minutes) and decides nothing: **all ratio runs below are executed for every arm whatever stage M shows** (about 40 minutes), because the closure criterion
is the one that uses the collisions themselves: Jk = J0 over all seeds (no EXACT sample outside the base cells) bounds the gain of the arm: with J0 EXACT samples and none outside, the relaxed-only EXACT share is below 3 / J0 (rule of three, 95%) of J0, i.e. under log2(1 + 3/J0) bit.

## The ratio stage (P8, chi38p8.txt, `--autolist`, `--var "W8 a0list @sel_members.txt late"`, event out, np 8192, mt 16384, 8 threads, seeds listed)

Relaxation ops are the tool's (README): dropv (value-only bits), dropq (a '+' relation to the row above), dropx2 (the two-bit conditions touching the named word). Masks come from chi38p8.txt:
E17 value-only 40421a80, E17 '+' to E16 00040010; E18 value-only 40421200, E18 '+' to E17 01808000; E20 value-only 01848010, E20 '+' to E19 20000000; E21 value-only 01808000; two-bit conditions touching A17 (7), E18 (4), E21 (3).

| run | rows | arms (name = ops) | seeds |
|---|---|---|---|
| R18a | 18..21 | r18v = dropv E18 40421200 | 9101..9116 |
| R18b | 18..21 | r18q = dropq E18 01808000 ; r18x = dropx2 E18 | 9101..9116 |
| R17a | 17..21 | r17v = dropv E17 40421a80 | 9201..9216 |
| R17b | 17..21 | r17q = dropq E17 00040010 ; r17x = dropx2 A17 | 9201..9216 |
| R2021 | 20..21 | r20v = dropv E20 01848010 ; r21v = dropv E21 01808000 ; r21x = dropx2 E21 ; r20q = dropq E20 20000000 | 9301..9316 |

Every listed seed is run and reported; none is dropped, replaced or rerun. Runs under `prlimit --as=268435456` with `MALLOC_ARENA_MAX=1` (the caps of the package's development record), `nice -n 10`,
at most 8 threads, on the cloud box; peak resident memory by `/usr/bin/time -v`. Order: stage M, R18a, R18b, R17a, R17b, R2021, V0 (V0 is needed only if some arm has Jk > J0).

## Statistic and rule

Per arm, per run: G = log2( sum_s Jk_s / sum_s J0_s ) over the seeds (ratio of sums; the seed is the cluster); SE = delete-one-seed jackknife standard error of G; LB99 = G - t(0.99, n-1) SE
(t = 2.998 for 8 seeds, 2.602 for 16). `anal_x1.py` (written with this file, unchanged afterwards) prints these from the logs.
An arm is **alive** iff LB99 > +0.10 bit. This screening run does not declare any q3 value. An alive arm is then bisected by subsets of its masks and confirmed by a second preregistered run of 32
fresh seeds before any program or proof change; a dead arm (LB99 <= 0.10) is recorded as "no gain seen at this power" with its G and SE, not as a proof of zero.
Diagnostics required 0: prefix broken by redraw, y-anchor inconsistent, replay mismatches; a nonzero diagnostic voids that seed (reported, not replaced).
Disclosed, not used: smoke run on chi38 (seed 1, np 2048, mt 1024): J0 30, JA 80.

## Amendment 1 (06:02 MDT, 12:02 UTC; after stage M and before any further counted seed)

Stage M was run as registered (seeds 9401..9404; logs out/M_*.log, hashes of the registered files in prereg_x1_hashes.txt). Result: for every arm except r18q the final samples that follow the printed
cells and the EXACT samples of the relaxation are the same samples in every seed (Jk = J0, per seed): r17v, r17q, r17x (window from row 17), r18v, r18x, r20v (cells rate 1.0000), r20q (cells rate 0.49..0.52, so the added
region has half of the mass, and ZERO EXACT samples among its ~4 million samples per seed) and r21v, r21x (cells rate 0.12..0.13, again zero EXACT in the added region). Those arms add no collision: closed as
"no extra EXACT sample seen" with Jk = J0 exactly; the gain bound is log2(1 + 3/J0) with J0 = 1,100 to 1,700 per arm over the four seeds, under 0.005 bit.
The one arm with extra EXACT samples is r18q (drop the '+' relation E18 = E17 on bits 24, 23, 15): seed 9403 had cells rate 0.309 and EXACT 69 (cells) against 295 (relaxation); seed 9404's population died at stage 20 and
seeds 9401, 9402 had no extra samples (the result depends on the E17 value of the lineage, because this run starts its window at row 18). A local debug build (scratchpad copy of the source with one print statement, same estimator; used only
to look at samples, no number from it is used) showed an extra EXACT sample with E17x = 2b08cc08 (bits 24, 23 = 1, 0), E18x = 02dbd786 (bits 24, 23 = 0, 1), E19x = e65badfa, E19y = e7db2dfa, E20x = E20y: delta E16 + delta S1(E19) + delta CH(E19, E18, E17) = 0 mod 2^32,
checked by hand with Python (the CH change -2^24 + 2^23 at bits 24 and 23 is absorbed by the other sign of one S1 term), so these are real collisions of the 38-step compression, rebuilt from the message words by the tool's replay.
R18a was started and stopped by the run owner after 4 minutes (arm r18v, closed by stage M); its partial log is not used. Runs R18b, R17a, R17b, R2021 are cancelled (their arms are closed by stage M).

**F1 (the declared measurement)**: `window --chi chi/chi38p8.txt --rows 17 21 --event out --np 8192 --mt 16384 --threads 8 --autolist --var "W8 a0list @sel_members.txt late"`, seeds 9501..9532 (32 fresh seeds, 2^27 final samples each),
arms (all subsets of the primary arm, same samples): **q18 = dropq E18 01808000 (primary)**, q18h = dropq E18 01800000, q18b15 = dropq E18 00008000, q18b24 = dropq E18 01000000, q18b23 = dropq E18 00800000.
Statistic: G = log2(sum Jk / sum J0) pooled over the seeds, delete-one-seed jackknife SE, LB99 = G - 2.4528 SE (anal_x1.py). The primary arm is the only one declared; a subset arm can only have a smaller G (it is contained in q18) and is reported for information.
Rule: if LB99(q18) > 0.10 bit the declared gain is floor_4dec(LB99(q18)) and the package may take q3_model = -96.5755 + that gain (the sum of two one-sided 99 percent bounds, stated as such); otherwise nothing changes.
**V0** (validation of the shared-carrier ratio on the known answer, chi38 arm A, seeds 9001..9008) is run after F1; the F1 number is used only if V0 passes (within 0.35 bit of +2.0368).
Diagnostics required 0 (prefix broken by redraw, y-anchor inconsistent, replay mismatches); a seed with a dead population is reported and counted in the pooled sums with its zero counts (it contributes J0 = Jk = 0 and is not replaced), and the count of dead seeds is stated.

## Amendment 2 (06:05 MDT; before the rerun, after the first F1 launch stopped)

The first F1 launch (06:02:27 MDT, 8 threads, `prlimit --as=268435456`) ended with SIGSEGV (rc 139) in seed 9504 after 69 s (peak resident memory 202,296 KiB): at window stage 19 every proposal is accepted
(2,097,152 of 2,097,152 records of 24 bytes, copied and sorted for the resampling) and the 8 default thread stacks of 8 MiB add 64 MiB of address space, so the 2^28 cap was hit. Its seeds 9501 and 9502 completed and seed 9503 died at stage 20
(389 of 2,097,152 proposals accepted at stage 20 in the neighbouring seeds); nothing from that log is used. The rerun is the identical command with `ulimit -s 2048` (2 MiB stacks, 16 MiB of address space for 8 threads), same cap, same 32 seeds;
the generator streams are indexed by (seed, stage, particle), so the seeds reproduce whatever the thread count, and the rerun is a continuation of the registered run, not a replacement of seeds. The rerun starts after V0 finishes (8 cores in use at a time).
Seeds whose population dies are reported and kept in the pooled sums as zero counts (as registered). The package-side statement "every development execution whose output is used ran under `prlimit --as=2^28`" holds for the rerun.

## Result of V0 and Amendment 3 (06:08 MDT; F1b is running, started 06:07:00)

V0 (chi38, arm A, seeds 9001..9008, all diagnostics 0): G = +1.9917 bit, jackknife SE 0.0835 (pooled J0 10,599, JA 42,154) against the separately run, paired value +2.0368 of D250: difference 0.045 bit < 0.35. **V0 passes**; the shared-carrier ratio is a valid estimator of the gain of a prefix relaxation.

**M2 (scouting; no number from it enters a package)**: whether anything else becomes droppable on top of q18. After F1b, nine single runs, each window rows 17..21, np 8192, mt 4096 (2^25 final samples per seed), 8 threads, seeds 9601..9608, `--autolist`, W8 list as above,
two arms per run: `base2 = dropq E18 01808000` and `base2+X`, X in {dropv E18 40421200, dropx2 E18, dropv E17 40421a80, dropq E17 00040010, dropx2 A17, dropv E20 01848010, dropq E20 20000000, dropv E21 01808000, dropx2 E21}
(the second arm is the ops of the first plus the ops of X, separated by ';'). Statistic G2 = log2(sum J(base2+X) / sum J(base2)) with the jackknife SE (anal_x1.py with `cells` read as base2 is NOT used; the two arm lines are compared by anal_pair.py written with this amendment).
An X with G2 > 0.1 and G2 > 3 SE is recorded as a lead, to be confirmed by a registered run before any use; the others are recorded as closed on top of q18 with their G2 and SE.

## Amendment 4 (06:09 MDT; after the second crash, before the rerun)

F1b (identical command, 2 MiB stacks) ended again with SIGSEGV (rc 139) in seed 9504, one minute after its start, with seed 9503 dead at stage 20 just before it, exactly as in the first F1 launch. The same thing did not happen in stage-M run M_r18q, where the dead seed was the last one.
So the crash is not memory: the tool crashes on the first seed AFTER a seed whose population died ("window stage 20: dead", then "seed N: no samples", then the next seed). (Our reading of the cause: the dead-seed return path frees the particle arrays; not investigated further; the tool is not part of any package.)
Remedy that changes no number: one process per seed (`--seeds s` for each s), same flags, same cap; the generator streams are indexed by (seed, stage, particle), so each seed gives the same counts in its own process (checked on seeds 9501 and 9502: 2661 / 2936 and 3717 EXACT in F1 and F1b, 6378 together, identical).
The M2 runner of Amendment 3 was started by mistake behind F1b and stopped after its first run (M2_r18v, finished, rc 0); everything of M2 is rerun per seed. F1 is rerun as F1c: seeds 9501..9532, one process per seed, then the logs are concatenated in seed order for anal_x1.py.
Dead seeds stay in the pooled sums with zero counts, as registered. The number of dead seeds is reported.

## Amendment 5 (06:16 MDT; F2 replaces F1c as the declared measurement; before any F2 seed)

What F1c showed in its first 14 seeds (log out/F1c.log, kept; stopped at the seed it had reached when this amendment was written, not for its value): the counts are dominated by one to three lineage clusters per seed.
A local debug build (scratchpad copy of the tool with a tally of the E17 and E18 bits 24, 23, 15 over the EXACT samples; no number from it is used) shows, in seed 9506 and in seed 9507, EXACT samples only of the pattern E17[24,23] = 10, E18[24,23] = 01 (all of them off the printed cells),
in seed 9501 only of printed-cell patterns (E17 = E18 on those bits: 01 and 11), in seed 9505 of both. The window carrier keeps only about 130 to 500 of 2,097,152 proposals at stage 20, so a seed has few distinct lineages and J0 (the printed-cell EXACT count) is 0 in some seeds
while Jk is large. The ratio of pooled counts is a ratio of heavy-tailed sums: its jackknife SE after 6 live seeds was 0.6 bit, and the final-sample noise is not the issue (about 5,000 EXACT samples per seed), the lineage lottery is. So many cheap seeds beat few expensive ones.
**F2 (the declared measurement)**: the same command as F1 with `--mt 2048` (2^24 final samples per seed), 400 fresh seeds 10001..10400, one process per seed, arms q18 (primary), q18h and q18b15 (information), same cap and flags, 8 threads.
Statistic (linear scale, which is the scale on which the estimate of a probability is unbiased): with w_s = 2^(prefix_s + carrier_s) (the two numbers printed on the "[s] prefix log2 ... window carrier log2 ..." line of seed s; w_s = 0 for a dead seed),
G = log2( sum_s w_s Jk_s / sum_s w_s J0_s ), delete-one-seed jackknife SE over all 400 listed seeds (dead seeds are entries with zero weight), LB99 = G - 2.34 SE (anal_x2.py, written with this amendment). The unweighted pooled value is printed for comparison.
Rule: if LB99(q18) > 0.10 bit the declared gain is floor_4dec(LB99(q18)); then q3_model = -96.5755 + declared gain (product of two one-sided 99% bounds, stated so). Otherwise nothing changes. Every listed seed is run; the number of dead seeds is stated; diagnostics must be 0.
M2 (scouting of compound relaxations) is dropped: it would need the same number of seeds and its arms are closed one by one by stage M.
```

#### A.11.2 `run_x1.sh`

(script omitted: not required for the record; the registered text and outputs are kept)

#### A.11.3 `run_x1b.sh`

(script omitted: not required for the record; the registered text and outputs are kept)

#### A.11.4 `run_x2.sh`

(script omitted: not required for the record; the registered text and outputs are kept)

#### A.11.5 `anal_x1.py`

(script omitted: not required for the record; the registered text and outputs are kept)

#### A.11.6 `anal_x2.py`

(script omitted: not required for the record; the registered text and outputs are kept)

#### A.11.7 Counts

V0 (chi38, arm A, seeds 9001..9008; per seed: J0 = EXACT samples on the printed cells of rows 19..21, JA = EXACT samples on the arm A): 9001: 1600 / 5139; 9002: 1210 / 5203; 9003: 1376 / 5624; 9004: 1515 / 4967; 9005: 1230 / 5419; 9006: 999 / 5391; 9007: 1228 / 5016; 9008: 1441 / 5395. Sums 10599 / 42154.

Stage M (P8, each arm alone, seeds 9401..9404, 2^23 final samples per seed; per arm J0 = Jk per seed, the arm r18q has the seeds listed as J0 / Jk, "dead" = the population died at stage 20):

```text
r18v  9401: 393/393  9402: 319/319  9403: 336/336  9404: 312/312
r18x  9401: 264/264  9402: 199/199  9403: 334/334  9404: 248/248
r17v  9401: 330/330  9402: 331/331  9403: 316/316  9404: 299/299
r17q  9401: 348/348  9402: 309/309  9403: 272/272  9404: 329/329
r17x  9401: 287/287  9402: 360/360  9403: 336/336  9404: 375/375
r20v  9401: 298/298  9402: 336/336  9403: 326/326  9404: 313/313
r20q  9401: 131/131  9402: 153/153  9403: 155/155  9404: 129/129
r21v  9401: 35/35  9402: 28/28  9403: 41/41  9404: 39/39
r21x  9401: 39/39  9402: 31/31  9403: 28/28  9404: 44/44
r18q  9401: 470/470  9402: 165/165  9403: 69/295   (seed 9404 dead)
```

F2 (seeds 10001..10400; per seed: log2 w = prefix + carrier, J0, Jq18; q18h and q18b15 are in the summary line above; a dead seed has no line):

```text
10001 -81.74 0 794
10002 -81.70 839 839
10004 -80.65 984 984
10006 -81.69 570 570
10007 -81.54 0 557
10008 -80.02 323 595
10009 -80.84 0 542
10010 -80.11 513 513
10012 -81.70 961 961
10013 -80.11 540 687
10014 -79.98 335 716
10016 -81.57 627 627
10017 -81.71 522 522
10019 -80.58 574 574
10020 -80.67 256 594
10021 -79.73 333 615
10023 -80.64 360 712
10024 -80.68 824 824
10025 -81.57 0 295
10026 -81.55 527 527
10027 -81.63 247 247
10028 -81.70 0 789
10029 -79.73 304 573
10030 -81.74 0 499
10031 -80.14 379 716
10033 -80.17 165 580
10035 -80.72 632 632
10037 -80.18 739 739
10039 -81.60 942 942
10040 -80.74 883 883
10041 -80.60 0 540
10042 -80.60 410 664
10043 -81.69 389 389
10044 -80.15 280 371
10045 -80.19 394 697
10046 -80.13 631 631
10047 -81.55 0 725
10048 -81.71 619 619
10049 -80.67 455 455
10056 -80.66 299 493
10057 -81.76 0 925
10058 -80.69 780 780
10060 -80.02 407 646
10061 -80.65 657 657
10063 -80.59 418 418
10064 -81.72 718 718
10066 -80.06 769 769
10067 -81.87 926 926
10068 -81.67 0 657
10070 -81.50 761 761
10071 -81.90 0 608
10072 -81.73 463 463
10073 -79.99 825 825
10074 -81.64 1019 1019
10075 -80.13 614 614
10076 -81.69 845 845
10078 -79.65 634 634
10081 -79.68 451 594
10082 -80.77 232 583
10083 -81.57 0 616
10085 -79.76 573 779
10086 -81.62 0 559
10087 -80.80 317 500
10088 -80.13 390 618
10089 -81.64 1060 1060
10091 -81.66 1048 1048
10095 -80.20 467 575
10096 -80.07 869 869
10097 -81.75 0 547
10098 -81.63 0 770
10099 -80.68 269 625
10100 -81.58 881 881
10101 -80.66 413 641
10103 -81.68 790 790
10104 -80.69 323 711
10105 -80.64 613 613
10106 -78.90 413 648
10107 -80.09 663 663
10108 -80.07 276 639
10109 -80.65 392 653
10110 -80.70 297 754
10111 -80.84 0 883
10112 -80.11 454 645
10113 -81.65 347 347
10114 -80.25 852 852
10115 -79.63 376 577
10116 -80.10 210 662
10117 -81.63 452 452
10120 -79.65 577 679
10121 -80.15 509 509
10122 -81.68 0 681
10124 -81.65 666 666
10125 -80.17 594 864
10126 -81.66 749 749
10127 -79.99 593 593
10128 -79.64 256 509
10129 -80.63 351 641
10132 -79.70 481 578
10133 -79.64 90 645
10135 -81.65 692 692
10136 -81.78 0 334
10139 -81.80 0 555
10140 -80.51 196 489
10141 -80.05 168 678
10142 -81.58 604 604
10143 -81.71 1063 1063
10144 -81.68 588 588
10146 -80.49 489 489
10147 -80.68 522 522
10148 -81.67 1048 1048
10149 -81.63 805 805
10151 -80.67 960 960
10152 -81.68 819 819
10153 -80.63 355 355
10155 -80.70 961 961
10157 -80.58 616 616
10158 -81.73 413 413
10159 -81.70 0 342
10160 -80.69 675 675
10161 -81.90 615 615
10162 -81.63 514 514
10163 -81.56 888 888
10164 -81.62 879 879
10165 -80.10 547 812
10166 -81.58 0 581
10167 -80.62 181 594
10168 -80.80 366 673
10169 -81.71 790 790
10170 -81.68 692 692
10171 -80.72 267 801
10172 -81.80 795 795
10173 -80.74 152 312
10174 -80.03 406 599
10175 -81.62 1018 1018
10176 -80.22 473 642
10177 -80.14 284 724
10178 -80.66 0 599
10179 -80.76 0 686
10181 -80.62 162 343
10182 -81.66 556 556
10183 -81.70 0 890
10184 -81.64 1001 1001
10185 -80.70 423 735
10186 -81.70 777 777
10187 -81.63 0 764
10188 -80.63 339 617
10189 -80.68 695 695
10190 -81.65 590 590
10192 -81.66 807 807
10194 -81.66 443 443
10196 -81.90 0 843
10197 -81.89 471 471
10198 -81.60 0 669
10199 -80.79 319 732
10200 -81.53 794 794
10201 -81.64 695 695
10202 -80.66 266 636
10203 -80.67 726 726
10204 -79.73 574 669
10206 -80.77 396 801
10209 -81.80 301 301
10210 -81.67 827 827
10211 -81.66 468 468
10213 -81.51 488 488
10214 -81.76 600 600
10215 -80.69 376 587
10216 -80.65 0 557
10218 -80.79 664 664
10220 -81.66 801 801
10221 -81.76 0 578
10222 -80.74 825 825
10223 -80.80 331 540
10224 -81.79 0 493
10225 -81.60 0 350
10226 -81.57 647 647
10228 -80.05 602 941
10230 -80.09 528 733
10231 -80.09 210 596
10233 -80.69 809 809
10234 -80.66 568 568
10235 -80.63 311 710
10236 -81.69 872 872
10237 -81.68 0 1089
10238 -81.43 554 554
10239 -81.62 516 516
10240 -80.58 545 545
10242 -80.83 489 489
10244 -79.73 387 530
10246 -79.64 575 575
10247 -81.70 0 580
10248 -80.69 788 788
10249 -79.75 668 777
10250 -80.07 410 546
10251 -81.73 862 862
10252 -80.64 476 639
10253 -80.16 608 775
10254 -80.11 567 567
10255 -80.11 493 694
10256 -80.68 584 584
10259 -81.53 0 1065
10261 -80.09 805 805
10262 -80.08 485 745
10263 -81.59 844 844
10264 -80.58 558 558
10265 -80.59 897 897
10266 -80.12 336 557
10267 -80.66 353 353
10269 -81.63 641 641
10270 -80.68 762 762
10271 -80.04 487 734
10272 -79.38 287 638
10274 -81.60 0 672
10276 -81.63 597 597
10277 -80.67 701 701
10278 -80.59 425 425
10279 -80.73 223 467
10280 -81.64 735 735
10285 -80.70 912 912
10286 -81.52 476 476
10287 -81.75 0 547
10288 -79.70 248 535
10291 -81.75 0 734
10292 -81.58 457 457
10294 -81.68 511 511
10296 -80.71 223 649
10297 -80.78 391 688
10298 -80.66 350 562
10299 -80.74 718 718
10301 -81.75 737 737
10304 -80.72 659 659
10305 -81.68 0 313
10306 -79.68 395 786
10307 -80.04 427 562
10308 -80.16 327 750
10309 -80.56 262 670
10310 -80.11 564 763
10311 -80.02 263 460
10312 -81.60 986 986
10314 -79.40 510 604
10315 -80.75 1005 1005
10316 -81.89 596 596
10317 -80.68 648 648
10318 -80.82 801 801
10319 -81.78 0 370
10321 -80.63 685 685
10322 -80.06 0 725
10323 -81.66 0 754
10325 -81.82 585 585
10326 -80.63 225 623
10329 -80.14 427 599
10330 -79.70 590 590
10331 -81.63 563 563
10332 -80.55 646 646
10333 -80.06 824 824
10335 -81.66 545 545
10336 -79.69 306 790
10337 -80.08 414 594
10338 -80.68 437 720
10339 -80.07 609 609
10340 -81.49 0 324
10341 -80.07 613 838
10342 -80.68 437 731
10344 -80.72 0 595
10345 -80.75 407 732
10346 -81.55 963 963
10347 -81.63 0 514
10348 -81.63 865 865
10349 -81.60 0 806
10350 -80.65 283 613
10352 -80.07 758 758
10353 -81.76 0 572
10354 -81.65 0 635
10355 -81.58 757 757
10356 -81.83 557 557
10357 -80.67 276 644
10358 -81.72 1013 1013
10359 -79.59 296 614
10360 -80.79 508 508
10361 -80.71 709 709
10363 -81.74 803 803
10364 -80.67 506 506
10366 -81.74 0 517
10367 -80.62 483 697
10368 -81.62 559 559
10369 -80.67 544 826
10371 -80.79 441 673
10372 -80.05 214 674
10374 -81.62 508 508
10376 -80.10 854 854
10377 -80.73 383 630
10378 -81.50 898 898
10379 -81.61 667 667
10380 -80.58 390 669
10383 -81.72 835 835
10384 -81.68 0 836
10385 -80.20 551 551
10386 -80.55 770 770
10387 -80.71 653 653
10390 -80.71 669 669
10392 -80.57 0 541
10393 -80.59 0 585
10394 -81.73 835 835
10395 -80.75 265 592
10396 -81.67 0 691
10399 -80.69 830 830
10400 -81.44 0 490
```

### A.12 The preregistered 128-seed measurement of q3 (Section 7.4): registration, run and analysis

Files, with their SHA-256 (`hashes.txt` of the run, written by the run script at its start on the cloud machine, `/root/r38q3b`; the preregistration is also hashed in `prereg_b_hashes.txt` at 11:02:24 MDT, before the first seed):

```text
17425aaa624561ceeb641977d72d86f6f4c1b8e57c6a05b7c82ad9ed1d12d485  traillab
c47e5ec605a25ae03df29ada92f68c3462468262dc30730a1e201de335c8a14d  chi/chi38p8.txt
ff582e64e060db2807d85fbe31b054ef04eea26ed00b46dbcafb66b2c36a7138  sel_members.txt
eb3310e43e0308e5658631226e09e9ab7d0403de9470dcd3b36545f9fee00f5a  PREREG_Q3P8_B.md
```

*Preregistration* (`PREREG_Q3P8_B.md`, written 2026-10-17 before the first seed of this run; the quantity, the tool and the inputs are those of `PREREG_Q3P8.md`, Appendix A.9):

```text
# Preregistration B: q3 of P8 for the printed-cell accepted event, 128 fresh seeds (written 2026-10-17 before the first seed of this run)

Quantity: the same as PREREG_Q3P8.md (research/day_1014/r38-p8/build, sha256 of that file in prereg_b_hashes.txt): q3 = the average over the 196,608
selected variants of Pr[accepted event | good pair], the event of chi38p8.txt (rows 16..21 cells, '+' pairs and two-bit conditions, row 19 on signed
differences, the relation E18 = E17 INCLUDED), outputs after step 37 equal.
Tool and inputs: the same files as PREREG_Q3P8.md, unchanged: traillab binary sha256 17425aaa624561ceeb641977d72d86f6f4c1b8e57c6a05b7c82ad9ed1d12d485,
chi/chi38p8.txt c47e5ec605a25ae03df29ada92f68c3462468262dc30730a1e201de335c8a14d, sel_members.txt ff582e64e060db2807d85fbe31b054ef04eea26ed00b46dbcafb66b2c36a7138.
Command per seed s (one process per seed, the documented workaround for the multi-seed 'window' crash after a dead seed; the generator streams
are indexed by seed, so a seed gives the same counts either way): window --chi chi/chi38p8.txt --rows 22 37 --event out --np 8192 --mt 32768
--seeds s --threads 4 --autolist --var "W8 a0list @sel_members.txt late". Machine: the cloud box, 2 seeds at a time (8 threads), nice 10.
Seeds: 128 fresh seeds 7001..7128 (never used for P8: earlier P8 runs used 3001-3032, 5001-5032, 9001-9008, 9401-9404, 9501-95xx, 10001-10400).
Per-seed value L_s = prefix log2 P(rows 7..21) + log2 rate(EXACT); a dead seed or 0 EXACT counts as -128.
Declared value: q3_base = floor_4dec( mean(L) - t sd(L) / sqrt(128) ), t = t(0.99, 127) = 2.3556 (one-sided 99% Student lower bound, the seed is the cluster),
over THESE 128 seeds only (the 32 seeds of PREREG_Q3P8 are not pooled). Diagnostics required 0 (prefix broken by redraw, y-anchor inconsistent,
replay mismatches); a non-zero diagnostic in any seed voids the run (reported, not replaced). No interim look at L values, no stopping rule; all 128 seeds are used.
Use: if the run is not void and q3_base > -96.5755, the next r38 filing uses q3_model = q3_base x 2^0.4149 (the F2 bound, unchanged); otherwise nothing changes.
```

*Run script* (`run.sh`, written by `launch_cloud.sh` on the cloud machine; two seeds at a time, 4 threads each, no `prlimit`; the model file, the list and the binary are those of Appendix A.9; the run took 2026-10-17 17:02:44 to 17:45:42 UTC):

(script omitted: not required for the record; the registered text and outputs are kept)

*Memory sampler* (`hwm.sh`, started separately at 17:16:09 UTC; it ended with the run, 17:45:42 UTC):

(script omitted: not required for the record; the registered text and outputs are kept)

The sampler recorded `time seed VmHWM_kB` lines for the processes of seeds 7041..7128 (88 seeds; the 40 earlier seeds were running or finished before it was started and are not in the record). Largest VmHWM per process, seed:KiB: 7041:182560 7042:181824 7043:182264 7044:183324 7045:182536 7046:184052 7047:182520 7048:181764 7049:182348 7050:182776 7051:182756 7052:182028 7053:182428 7054:181656 7055:183012 7056:182264 7057:183056 7058:193792 7059:183260 7060:182524 7061:182272 7062:184348 7063:181768 7064:184616 7065:182576 7066:183028 7067:182540 7068:184300 7069:188692 7070:186884 7071:184320 7072:190504 7073:182764 7074:182272 7075:183360 7076:182308 7077:183620 7078:191852 7079:184304 7080:184264 7081:183044 7082:184568 7083:183028 7084:182288 7085:181060 7086:184088 7087:183208 7088:182040 7089:184088 7090:183852 7091:182872 7092:182332 7093:183300 7094:181716 7095:184564 7096:184104 7097:183044 7098:182576 7099:181792 7100:184836 7101:183840 7102:182572 7103:183064 7104:182336 7105:182752 7106:183040 7107:183812 7108:182776 7109:182540 7110:182552 7111:183236 7112:183484 7113:181992 7114:185584 7115:182388 7116:182556 7117:182292 7118:182292 7119:183288 7120:184028 7121:187540 7122:183416 7123:183808 7124:182536 7125:183796 7126:182304 7127:184852 7128:184604. The largest is 193,792 KiB = 2^27.56 bytes; the largest sum of the two concurrent processes at one sample is 376,848 KiB = 2^28.52 bytes.

The log of the first seed (the same block for every seed; the full logs are the 128 files `seed_7001.log` .. `seed_7128.log` of the run):

```text
model p8: 38 steps, anchor row 15 (x and y rows 12..15 held), E-driven rows 16..21, lowest conditioned row 7
  conditions: 35 two-bit/linear (printed), 35 in the procedure model; 'except' words: W7 W8
  free word W6 (late): W6 rand late
  free word W7 (late): W7 fset s0 03bff800 late
  free word W8 (late): W8 a0list @/root/r38q3b/sel_members.txt late
WINDOW rows 22..37 event=out np 8192 m 256 mt2 1024 mw 256 mt 32768 threads 4 prefix-conditions cells
-- seed 7001
  init: 8192 particles, acceptance 1.000000 (rows 16..15)
  E16 set under the prefix conditions: 160 values (enumerated 2^24 candidates)
  stage 16 (E-driven, list of 160): accepted 2097152 of 2097152, log2 est -24.6781
  stage 17 (E-driven): forced  7 bits, accepted 1973 of 2097152, log2 est -41.7319
  stage 18 (E-driven): forced  7 bits, accepted 17035 of 2097152, log2 est -55.6757
  stage 19 (E-driven): forced  3 bits, accepted 2097152 of 2097152, log2 est -58.6757
  stage 20 (E-driven): forced  5 bits, accepted 1267 of 2097152, log2 est -74.3685
  stage 21 (E-driven): forced  4 bits, accepted 261604 of 2097152, log2 est -81.3715
[s7001] prefix log2 P(rows 7..21) = -81.3715
[s7001] samples 268435456 (late words redrawn per sample), prefix broken by redraw 0, y-anchor inconsistent 0, replay mismatches 0
[s7001]   cells          rows 22..37:    134215625  rate 4.999922e-01 (log2  -1.0000) 95% [4.9993e-01, 5.0005e-01]  with exact 10961
[s7001]   EXACT          zero output difference after the last step:        10961  rate 4.083291e-05 (log2 -14.5799) 95% [4.0076e-05, 4.1605e-05]
[s7001]   ratios to 'cells' (95% cluster-robust over particles; halves = particles split in two):
[s7001]     EXACT/cells = 0.00008 +- 0.00000  (log2 -13.5799)  halves 0.00008 +- 0.00000 | 0.00008 +- 0.00000
[s7001]   log2 P(rows 7..37, model cells) = prefix + log2 rate(cells) = -82.3715
[s7001]   time 38.0 s
== summary over 1 seed(s): EXACT/cells 0.00008 +- 0.00000
== summary: log2 P(rows 7..37, model cells) mean -82.3715, seed sd 0.0000 (seeds: -82.3715)
```

The declared value is computed from the 128 logs by `q3analysis_b.py` (the script of Appendix A.9 with 128 seeds, the registered t = 2.3556 and the halves 7001..7064 / 7065..7128; usage `python q3analysis_b.py seed_*.log`):

(script omitted: not required for the record; the registered text and outputs are kept)

```text
seeds 128 7001 .. 7128 | seeds with all diagnostics 0: 128 | EXACT events 1326458 min per seed 7809
mean -96.3123  seed sd 0.5563  one-sided 99% Student lower bound -96.428132  ->  q3_base = -96.4282
halves -96.3328 / -96.2918
per seed: -95.9514 -95.8473 -97.6863 -95.8194 -96.4100 -97.3530 -96.0952 -96.5271 -95.6510 -96.0632 -96.1255 -96.1205 -96.8975 -95.9300 -96.2596 -96.4129 -96.5415 -95.9474 -96.0871 -95.7058 -96.1807 -97.0824 -95.7759 -95.7093 -96.4054 -96.2425 -95.8663 -96.6074 -96.6234 -96.4052 -96.5836 -95.7079 -95.3868 -95.3947 -96.7348 -96.7012 -96.4372 -96.6482 -96.9617 -97.3097 -96.6475 -96.9395 -97.3445 -95.0900 -96.8402 -96.4532 -95.7523 -97.0385 -96.3175 -96.5519 -96.3824 -96.3070 -97.3019 -95.9419 -97.2275 -96.8172 -95.5370 -95.6234 -96.3551 -96.3398 -95.8110 -96.7379 -95.4275 -96.3202 -96.2097 -96.9832 -96.2176 -96.2349 -96.1682 -96.3922 -95.9092 -96.9812 -95.8768 -96.0074 -95.8666 -95.9552 -95.4917 -95.4601 -96.2234 -96.2378 -95.4621 -96.4844 -96.2793 -96.7117 -96.3305 -96.6939 -96.5255 -96.4187 -96.7542 -96.6869 -96.7610 -97.2736 -96.7676 -96.6342 -95.7191 -96.3106 -95.7573 -96.3771 -95.8864 -96.1180 -95.9172 -96.2218 -98.1137 -95.0796 -95.9378 -95.4504 -96.7590 -95.1732 -95.7216 -96.8931 -96.6392 -95.2674 -96.5771 -96.1931 -95.8976 -96.5685 -96.6127 -96.2800 -95.8841 -96.6560 -96.2981 -95.8157 -96.7839 -97.2887 -96.1010 -96.1892 -97.1310 -97.0554
```


### R.2 The characteristic search (H4a, H4b; 9aaf71a2 Appendix C)


**P8.** 1a695f0b Section 3.2 publishes the search that found P8 (quoted; participant-run): a signed-difference SAT model run over the 24 XOR patterns of weight 25 of the message shape, each with every known signed difference blocked, 38 solver runs with a limit of 10,800 s each (12 UNSAT in 8 to 22 s, 11 SAT in 2,514 to 9,890 s, 15 TIMEOUT at 10,800 s), each SAT solution through a value-level coupling check and an estimator; P8 = run SW_p08_k1 (4,714 s, coupling 662 s). The listed run times total 230,183 s = 2^17.81 s; the author bounds the whole search, S, the class data and all its development by one 10-core machine for less than 2^21 core-seconds. At the hash rate below (3,797,484 SHA-256 compressions per second, one thread) 2^21 core-seconds are 2^42.86 SHA-256 evaluations = 2^43.61 units, 34.4 bits under A_C = 2^78. The measurements below (from fb176310, for the published characteristic and for a 39-step characteristic) are the same kind of search; they put the allowance in the same range.

**Measured by us (fb176310 Appendix C, unchanged).**

**Part A. Published and measured cost of the same kind of search (the basis of A_C = 2^78).** Units are target compressions (one 38-step compression = 1 unit = 2728 word operations); a full 64-step SHA-256 evaluation is charged 64/38 units = 4,594.5 word operations, more than a target compression.

*Conversion.* Hash rate measured here: portable C SHA-256 compression (no SHA-NI, gcc -O2, one thread, AMD Ryzen 9 7900X, WSL2; checked on "abc", first words ba7816bf 8f01cfea), five runs of 2 x 10^7 compressions: 4,030,079, 4,022,282, 3,891,284, 4,013,036 and 3,797,484 per second; the slowest, 3,797,484 per second (2^21.86), is used for every conversion (a slower rate gives more evaluations, hence a larger cost). Solver CPU-seconds = wall seconds x threads (an upper bound: idle threads are counted). Figures in the table are log2.

| source | problem | stated cost | SHA-256 evaluations | units | word operations | bits under 2^78 units |
|---|---|---|---:|---:|---:|---:|
| Mendel, Nad, Schlaeffer 2013, Sect. 6.3 p.14 | 38-step SFS: characteristic and pair together | about 8 h on a single CPU, "about 2^37 SHA-256 evaluations" (hardware not named) | 37.00 | 37.75 | 49.17 | 40.25 |
| Mendel et al. 2013, Sect. 6.2 p.12 | 31-step SFS: characteristic and pair together | about 21 h, "about 2^38.4 SHA-256 evaluations" | 38.40 | 39.15 | 50.57 | 38.85 |
| Li, Liu, Wang 2024 (ePrint 2024/349), p.16 | 39-step SFS colliding pair given the characteristic | 120 s with 26 threads = 3,120 thread-seconds (hardware not named) | 33.46 | 34.22 | 45.63 | 43.78 |
| ours, 39-step characteristic | derived from scratch with the tool of [LLW24a] | 772.58 s wall x 12 threads (CryptoMiniSat) + 1,800.77 s x 1 (Kissat, no result) = 11,071.7 CPU-s | 35.29 | 36.04 | 47.46 | 41.96 |
| ours, 38-step pair (part B) | pair given the published cells, 4 calls, 3 without a model | 2,852.83 CPU-s | 33.33 | 34.09 | 45.50 | 43.91 |

Our 39-step characteristic derivation: the unmodified model scripts of github.com/Peace9911/sha_2_attack at commit 6a9f35fd (the account that hosts the authors' RIPEMD-160 tool of [LLW23]) were read before running (no network, no installs, writes only in the working directory); the STP query they emit was translated to CNF by our own converter (which rejects six mutated characteristics and accepts the published 39-step characteristic and rows 5..24 of the published 37-step one) and solved with CryptoMiniSat 5.11.21 on 12 threads: model found after 772.58 s wall (about 2.6 CPU-hours); Kissat 4.0.3 on the same file stopped at 1,800.77 s without a result. It is a window search (rows 8..26 with the message support fixed and the weights W 25, A 10, E at most 90 asserted) that finds a characteristic of the published weights, not the characteristic of Table 3 of [LZLLQZ26]; one run, one machine.

*Reading.* Every figure is far below 2^78 target compressions: the largest, 2^39.15 units (Mendel et al.'s 31-step figure), is 38.85 bits under it, and the 38-step figure of the same authors, 2^37.75 units, is 40.25 bits under; counted in word operations without the factor C, the largest is 2^50.57, 27.43 bits under 2^78. The 38-step characteristic of [LZLLQZ26] (two-block framework, dense rows 0..16) is a harder instance than those searches and no log of its search exists; the margin of 38.85 bits (a factor of about 2^39) is what A_C = 2^78 leaves for that difference and for failed and repeated searches.

**Part B. Our pair searches and sparse part.**

Participant-run here; programs written and run by Grok (xAI); not shipped (64 KiB source limit; the figures are not used in the ledger, which charges the allowance). SAT: one word operation = one propagation; otherwise one tick = one 32-bit add/sub, S0, S1, s0, s1, CH, MAJ or hash-set probe. Units = word operations / C. Totals include the calls without a model.

**38-step pair search, given the published cells.** Circuit: both 38-step chains with a shared chaining value, message masks on W7..W11, W15 (W16, W23, W25 expanded), every cell of Table 3, the 13 vertical links and the 47 two-bit conditions (W25[4] = W25[6], which holds on the published pair; Table 4 prints W25[9]); 110,437 variables, 383,913 clauses, satisfied by the published pair; one clause blocks the published (CV, M'). File a pins the 24 bits common to the 32 E16 words of the published list; file b selects one of the 32 words.

| call (time limit 900 s) | file | result | CPU s | propagations |
|---|---|---|---:|---:|
| Kissat 4.0.3 --sat --seed=2 --walkinitially=true | a | no model | 898.63 | 592,022,133 |
| CaDiCaL 2.1.3 --seed=1 | a | no model | 898.61 | 1,813,811,854 |
| Kissat 4.0.3 --sat --seed=4 --walkinitially=true | b | pair | 476.96 | 433,129,432 |
| CaDiCaL 2.1.3 --seed=4 | b | no model | 578.63 | 1,217,006,281 |
| total | | | 2,852.83 | 4,055,969,700 = 2^31.917 (2^20.504 units) |

The pair (38-step SHA-256 compression with feed-forward; recomputed by us with an independent step function checked against hashlib on "abc"; M' carries the published E16 word 482326fd, with a different CV and message):

```
CV     43058709 adfdbff7 b7e63568 b4e09527 3ef1b89a 18f03df1 7fd9bbaa 7f392ba4
M      33f3fd01 ab09628d 9971c77a 2f0148d3 442fd7d8 9acaf5c3 2fd3a6f8 a8740b40
       c91bb8b5 9e019239 04039fa1 0ce30b8d a18c515a 76a1e994 d28e48a0 9b5f6dbb
M'     33f3fd01 ab09628d 9971c77a 2f0148d3 442fd7d8 9acaf5c3 2fd3a6f8 88740b40
       cd5bb0b5 be019239 01028d0b 0ceb1f8d a18c515a 76a1e994 d28e48a0 9f1f65bb
digest 614d0b44 0d272005 713bab9e 4fc8e2a1 126b7229 bbb45050 0d592f10 cf2f96a9
```

Words that differ: 7..11, 15, 16, 23, 25 (dW16 = e0000000, dW23 = fe7f8000, dW25 = 20000000); A and E are equal from step 22.

**37-step analogue** (C = 2644; the same circuit on the 37-step characteristic, W15 pinned on the 24 common bits of its list): Kissat seed 2 pair A (135,356,424 propagations), Kissat seed 1 no model (167,052,440), CaDiCaL seed 1 pair B (494,307,286); total 796,716,150 = 2^29.570 (2^18.201 units). Digests: A 3c7353c7 46761dc9 8b3ce5a5 3c6530d2 d6e267fb f0f5b41e b8c21e9a 03b5b458, B 6c1e60a3 27a17426 dd5333ab 9f3317d4 00453b21 27264f97 2f2ea277 4a533513.

**38-step sparse part, from the support and the Section 4.1 rules only** (no table cell seeded; the published values used only as a checker):

| part | ticks | CPU s | result |
|---|---:|---:|---|
| message-difference signing, all 32 disturbance bits | 101,842,272 | 0.533 | bit 29 gives the published XOR masks; fe7f8000 among the 8 dW23 sums |
| sparse window rows 17..37, bits 28..31, all 8 dW23, both dW25 signs | 11,239,528 | 0.021 | the published dW23, dW25 close (22 conditions, rank 22) |
| total | 113,081,800 = 2^26.753 | 0.554 | |

**Not measured (the allowance A_C = 2^78):** deriving the dense signed characteristic of rows 0..16 with its two-bit conditions (the pair searches load those cells; a 37-step attempt with them unset, by SAT, step-6 cubes and a pattern beam, returned no model; of 4,614 message pairs realising the 38-step dW23, dW25 at CV = 0, none meets the zero window), and the authors' failed and repeated searches.


### R.3 Development computation and memory (H4c, H6; 9aaf71a2 Sections 13.4, 14, Appendix A.10)


Below 2 x 10^5 CPU-seconds in total (the shared-carrier runs of Section 7.5, about 2 x 10^4 CPU-seconds on the cloud machine, included; the exhaustive passes, the end-to-end runs, the q3 runs of Section 7.4 (about 2 x 32 x 90 s on 3 to 4 threads, and the 128-seed run, 128 seeds of about 40 s on 4 threads, about 2 x 10^4 CPU-seconds on the cloud machine), the replica's development and calibration, the H3 measurement, the program scans and the cloud checks of the hoisted programs), far inside the charge DEV = 2^70 (H4c). Machine: Windows 10 with Python 3.14 for the programs in Python, and an Ubuntu distribution under WSL2 (24 cores, 46 GB, gcc) for the programs in C; heavy jobs ran at reduced priority on at most 4 threads each.

*Memory of the development executions (H4c, H6).* The development executions that produce data the procedure uses are the exhaustive pass `p8fam` (lean version: the class descriptors and the list of the 196,608 selected variants), the end-to-end runs `e2ep8` (table-free version) with their exact checks, and the programs of Section 14 (c). Each of them was run under a hard address-space cap (2026-10-14 for the C programs and the q3 run, 2026-10-17 for the programs of the hoisted version) (`prlimit --as=N`: an allocation beyond N fails and the program stops), with its peak resident memory measured by `research/tools/memmeter` (Appendix A.10, `run_chain.sh` and `run_small.sh`). The caps are 2^27 = 134,217,728 bytes for the C filters and the Python programs and 2^28 = 268,435,456 bytes for `traillab`, whose model, particles and per-stage records need about 218 MiB over the 32 seeds (222,756 KiB). Every run exited with status 0 under its cap; the peaks are in Section 14 (c2), the largest being 222,756 KiB = 2^27.77 bytes.
- `p8fam` (lean): peak 69,496 KiB. Its class descriptors (`maxclasses.txt`, SHA-256 b7a3fc4e118c0871ef8b197f7967c84c95e97ec013062f6864b27a5f51903d26) and its list of the 196,608 selected variants (`sel_members.txt`, SHA-256 ff582e64e060db2807d85fbe31b054ef04eea26ed00b46dbcafb66b2c36a7138) are the inputs of the preregistered q3 run and of the end-to-end runs.
- The earlier preregistered q3 run (32 seeds, Appendix A.9): the same binary (SHA-256 17425aaa624561ceeb641977d72d86f6f4c1b8e57c6a05b7c82ad9ed1d12d485), model file `chi38p8.txt` (SHA-256 c47e5ec605a25ae03df29ada92f68c3462468262dc30730a1e201de335c8a14d), list and seeds 5001..5032 as in `PREREG_Q3P8.md`; the command differs from the preregistered one only in `--threads 3` instead of 4 (the tool's output does not depend on the thread count) and in the environment variable `MALLOC_ARENA_MAX=1` (one malloc arena, so that the address space stays under the cap). All 32 seeds completed under the cap 2^28 (peak 222,756 KiB = 2^27.77 bytes). Each of the 449 result lines (prefix estimate, sample counts, diagnostics, cell and EXACT counts and rates, ratios) and of the stage lines of the 32 seeds is identical to the run of 2026-10-14 15:00 (Appendix A.9), so mean -96.3251, seed sd 0.5774 and the declared bound -96.5755 of the earlier run (Section 7.4) are those of the repeat.
- `e2ep8` (table-free): three runs under the cap 2^27, peaks in Section 14 (c2); counts in Section 13.1 (repeat).
- The Python and C programs of Section 14 (c): run under the cap 2^27, exit status 0.
The same programs were also timed without a cap with `/usr/bin/time -v` at the time of the first runs; those peaks are in Section 14 (c).
- Evidence for H2, not a development execution of the procedure (Section 14 (c3)): the 128-seed q3 run of Section 7.4 (declared value; commands, hashes and scripts in Appendix A.12) ran on the cloud machine (Linux, gcc) without an address-space cap and without `MALLOC_ARENA_MAX`: one `traillab window` process per seed with 4 threads, two processes at a time, nice 10, about 40 s per seed (17:02:44 to 17:45:42 UTC), its binary, model file and list those of the earlier run. The peak resident set of every `traillab` process (VmHWM of /proc/PID/status, KiB) was sampled every 2 s by `hwm.sh` from 17:16:09 UTC, 13 minutes after the first seed started, so the record covers the processes of seeds 7041..7128 (88 of the 128) and not those of seeds 7001..7040: at most 193,792 KiB = 2^27.56 bytes per process (Section 14 (c3)).
- The runs of Section 7.5 (`traillab window`, shared-carrier mode: V0, the stage-M scan, F2; commands and scripts in Appendix A.11) ran on the cloud machine (Linux, gcc), 8 threads, nice 10, one process per seed, each under `prlimit --as=268435456` (2^28) with `MALLOC_ARENA_MAX=1` and `ulimit -s 2048`, peak resident memory by `/usr/bin/time -v` (maximum resident set size of the process, the wait4 component of memmeter): at most 219048 KiB = 2^27.74 bytes, every process exited with status 0 except that the two first launches of the registered run crashed in the tool after a dead seed (Section 7.5), which are not used.



[Record of an earlier filing of the lineage, kept verbatim; its replacement of the author's signed-search sample was later refused by the board (R.6), so the author's 248,000 KB = 2^27.92 stands. The binding memory statement of this filing is Section 10.] **Peak memory: the maximum over the counted phases (H6).** The peak is max(online, preprocessing, the development executions that produce data the procedure uses); the claim is memory_log2_bytes = 27.069, i.e. the measured 137,460 KiB = 140,759,040 bytes = 2^27.069 of this package's retuned C-port execution (Appendix A.14), which is above every other counted cell of this revision. The two preprocessing phases are this package's own re-measurements of the same computations, both below the online peak and both replacing the author's samples of (a) by the re-measurement rule this track already applied to the Step-1 cell in `377cb363`: the Step-1 solve at 49,228 KiB = 2^25.5872 (`reports/receipts/r38-step1-stream.json`, byte-identical CNF `cc4670c3...`; the solver alone 40,408 KiB = 2^25.3024) and the signed search of the recorded instance at 86,404 KiB = 2^26.3988 (`reports/receipts/r38-signedsearch-round1-notp8.json`; seed 1 of the same configuration 81,608 KiB = 2^26.3164). The author's 279,720 KB and 248,000 KB samples quoted in (a) are therefore superseded and are not counted peaks.
(a) The computations behind the advice (P8 and S), measured by their author (1a695f0b Section 11, quoted; single-threaded, sequential, peak of the summed resident memory sampled every 0.2 s): the Step-1 solve of P8 (Python model and Kissat) 279,720 KB = 286,433,280 bytes = 2^28.094; the signed search that found P8 at most 248,000 KB = 2^27.92; the class descriptors (`a0cls.c`) 2^25.14; the condition tables and the pair below 2^24. Largest: the Step-1 solve, 2^28.0936, which sets the claim 2^28.094.
(b) Measured by us (fb176310 Section 14; `/usr/bin/time -v`, single-threaded): Kissat 4.0.3 and CaDiCaL 2.1.3 on the 38-step pair-search circuits, 2^26.82 to 2^27.15; the characteristic-derivation instance of Appendix C part A, CaDiCaL 2^27.56, Kissat 2^27.49.
(c) Our development programs (Section 13.4) in the runs that produced the outputs used by the claim, each measured with `/usr/bin/time -v` (maximum resident set size; `memmeas.sh`), without an address-space cap (the programs of the hoisted version, `a0hoist38.py`, `sens.py` and the emulations, were run under caps only: (c2)):

```text
traillab window (q3 run configuration, one seed, 4 threads)   182,824 kB   (2^27.48 bytes)
p8fam (exhaustive pass over a0, 16 buckets)                     69,348 kB
python verify_r16p8.py (the 2^24 end-to-end run)                36,660 kB
python calq3.py (20 replicates)                                 19,580 kB
python h3gen.py (100 successes)                                 19,536 kB
python w7check.py                                               16,980 kB
python r16p8.py                                                 12,168 kB
p8hits (4 threads), f23, h3count, e2ep8 (2^22 first blocks, 4 threads)   8,020 kB, 7,948 kB, 7,976 kB, 7,684 kB
```

The organizer experiments peak at 65,536 KiB (`a0-online-r38`) and 26,776 KiB (`a0-q3-r38`) under Linux and Python 3.14 (the largest resident size of their process), inside the sandbox's 128 MiB.

(c2) The development programs, run under hard address-space caps (`prlimit --as=N`), peak resident memory by `research/tools/memmeter` (maximum of the child's wait4 ru_maxrss, the per-process VmHWM and the summed RSS of the process tree sampled every 10 ms; floor about 1.4 MB). `traillab` and the OpenMP programs ran on 3 threads with `MALLOC_ARENA_MAX=1`; everything ran under `nice` (10 for the programs of 2026-10-14, 19 for those of 2026-10-17). Appendix A.10 lists the scripts and the records.

| execution (capped run) | cap `--as` (bytes) | exit | peak resident KiB (memmeter) | log2 bytes |
|---|---|---:|---:|---:|
| `p8fam` (lean): exhaustive pass over a0, class descriptors, list of the 196,608 selected variants | 2^27 = 134,217,728 | 0 | 69,496 | 26.08 |
| `traillab window`, earlier preregistered q3 run (32 seeds): seeds 5001..5032, 3 threads, `MALLOC_ARENA_MAX=1` | 2^28 = 268,435,456 | 0 | 222,756 | 27.77 |
| `e2ep8` (table-free): seed 19, 2^22 first blocks, 3 threads | 2^27 = 134,217,728 | 0 | 7,700 | 22.91 |
| `e2ep8` (table-free): seed 23, 2^23 first blocks, 3 threads | 2^27 = 134,217,728 | 0 | 7,616 | 22.89 |
| `e2ep8` (table-free): seed 17, 2^24 first blocks, 3 threads | 2^27 = 134,217,728 | 0 | 7,716 | 22.91 |
| `a0hoist38.py` selftest | 2^27 = 134,217,728 | 0 | 53,700 | 25.71 |
| `a0hoist38.py` calibrate | 2^27 = 134,217,728 | 0 | 64,484 | 25.98 |
| `a0hoist38.py` ledger | 2^27 = 134,217,728 | 0 | 69,480 | 26.08 |
| `sens.py` | 2^27 = 134,217,728 | 0 | 54,668 | 25.74 |
| `emu2.py` a0-online-r38 (two organizer-request emulations) | 2^27 = 134,217,728 | 0 | 83,568 | 26.35 |
| `emu2.py` a0-q3-r38 (two organizer-request emulations) | 2^27 = 134,217,728 | 0 | 44,820 | 25.45 |
| `w7check.py` | 2^27 = 134,217,728 | 0 | 23,796 | 24.54 |
| `h3gen.py 99 100` | 2^27 = 134,217,728 | 0 | 23,624 | 24.53 |
| `calq3.py 2000 2020` | 2^27 = 134,217,728 | 0 | 24,768 | 24.60 |
| `verify_r16p8.py (seed 19, 2^22 first blocks)` | 2^27 = 134,217,728 | 0 | 27,304 | 24.74 |
| `verify_r16p8.py (seed 23, 2^23 first blocks)` | 2^27 = 134,217,728 | 0 | 32,008 | 24.97 |
| `verify_r16p8.py (seed 17, 2^24 first blocks)` | 2^27 = 134,217,728 | 0 | 41,596 | 25.34 |
| `p8hits` | 2^27 = 134,217,728 | 0 | 7,616 | 22.89 |
| `f23` | 2^27 = 134,217,728 | 0 | 7,596 | 22.89 |
| `h3count` | 2^27 = 134,217,728 | 0 | 7,548 | 22.88 |
| `r16p8.py` | 2^27 = 134,217,728 | 0 | 12,336 | 23.59 |
| `traillab window` shared-carrier runs of Section 7.5 (V0, stage M, F2; 8 threads, one process per seed, cloud machine; `/usr/bin/time -v` instead of memmeter) | 2^28 = 268,435,456 | 0 | 219,048 | 27.74 |

Largest: 222,756 KiB = 2^27.77 bytes, under a cap of 2^28 (`traillab`); the peaks of the other programs are lower. Every run completed under its cap.

(c3) The q3 measurements of Section 7.4 (Appendix A.12) are evidence for the probability premise H2: they estimate the success probability of the procedure and the procedure reads no data they produce, so, like the organizer experiments, they are not a phase of the procedure, not counted in H6 and not charged in DEV. The 128-seed run ran without an address-space cap. It ran on the cloud machine, one `traillab window` process per seed with 4 threads, two processes at a time, nice 10. `hwm.sh` (Appendix A.12) recorded the peak resident set of every `traillab` process (VmHWM in /proc/PID/status) every 2 s from 17:16:09 UTC, 13 minutes after the first seed started: its record covers the processes of seeds 7041..7128 (88 of the 128); the processes of seeds 7001..7040 were not sampled. Largest peak of one process: 193,792 KiB = 198,443,008 bytes = 2^27.56. Largest sum of the two concurrent processes at one sample: 376,848 KiB = 2^28.52. The seeds are independent runs of one program, so the run needs one process at a time and the memory of the execution is that of one process, 2^27.56 < 2^28.094. For comparison, one seed of the same configuration in one process measured 182,824 KB (2^27.48, (c)) and the 32-seed run of Section 7.4 in one process under the cap 222,756 KiB (2^27.77, (c2)).

Not measured by us: the memory of P8's search and Step-1 solve (the author's figures are used); the 12-thread solver runs of fb176310's Appendix C are timing evidence only.



Run in WSL (Ubuntu) on 2026-10-14 (`run_chain.sh` and the first part of `run_small.sh`) and on 2026-10-17 (`run_small_hoist.sh`). `prlimit --as=N` sets RLIMIT_AS, the virtual address space of the process and its children: an allocation beyond N fails. `research/tools/memmeter` runs the command and reports the peak resident memory (maximum of the child's wait4 ru_maxrss, the per-process VmHWM and the summed RSS of the process tree sampled every 10 ms) as JSON, with the exit status. The programs are the binaries and scripts of the construction (`p8fam_lean`, `traillab`, `e2ep8`, `a0hoist38.py` of this package, SHA-256 d874226f004ccb1bd5e8d398cfee4f2607858250f8c199cca3f4e250befb733b, and the evidence scripts of Appendix A); `traillab`, `chi38p8.txt`, `sel_members.txt` have the SHA-256 values of Section 13.4. `MALLOC_ARENA_MAX=1` limits the C library to one malloc arena (by default each thread reserves 64 MiB of address space). The resident memory of `traillab` is about 218 MiB over the 32 seeds with 3 threads (about 181 MiB for one seed); without the environment variable its address space exceeds 2^28 bytes (a one-seed test failed at the cap with a segmentation fault, and passed with it). The table of Section 14 (c2) lists the peaks.

(script omitted: not required for the record; the registered text and outputs are kept)

(script omitted: not required for the record; the registered text and outputs are kept)

(script omitted: not required for the record; the registered text and outputs are kept)

Records: for each run the memmeter JSON line (command, exit status, signal, wall and CPU seconds, ru_maxrss, tree VmHWM, tree summed RSS, peak bytes) is the last line of the run's output; the repeated q3 run compares equal to the earlier one on all 449 result and stage lines of its 32 seeds.



### R.4 The preprocessing report of 1a695f0b (quoted)

~~~
Verbatim lines of the public proof.md of 1a695f0b (dariolina, sha256-r38, 95.32358), read as a document; sha256 of that proof.md: a86eff8b38ab02389f3c1a87b63d35982b41396310490c94eb998baba263db53
L261: T = A_C + A_S + DEV + N_FB + (N_FB x 35 + V_MAX + OVER + PRE + FIN) / C + 6
L262:   A_C = 2^48, A_S = 2^50, DEV = 2^50 (Section 12, H4)
L290: preprocessing (single-threaded, sequential; peak of the summed resident memory of all processes of each computation):
L291:   Step-1 solve of P8 (joint.py: value-exact dense part and tail, Python model + Kissat): 279,720 KB = 2^28.094 (sampled every 0.2 s)
L292:   the signed search that found P8 (stepk.py + Kissat, same specification and seed): at most 248,000 KB = 2^27.92 over 2 h 20 min
L293:     (Python 152,868 KB and Kissat 80,816 to 88,096 KB resident together; stopped after the original 78-minute solve time)
L294:   the class descriptors (a0cls.c, 32 passes): 37,036 KB = 2^25.14; the condition tables and pair (mkvt.py, fromjoint.py): below 2^24
L295: preprocessing peak 2^28.094
L298: *Scope of the memory bound.* Peak memory covers code, advice, retained data, tables and working state of the whole computation: the online algorithm, the charged precomputation (class members, planes, the program) and the computations behind the advice and the allowances (the characteristic search, the Step-1 solve, the class descriptors, the condition tables), each run single-threaded and sequentially. The class descriptors are found in 32 passes over a hash of c7 (`a0cls.c`, at most 2^23 pairs resident). The online figure also covers the deep path's working state (two traces, about 6 KB) and M0, CV1.
L307: - **H4** allowances: the search for P8, S and its class data, and all development used one 10-core machine for less than 2^21 core-seconds in all; A_C = 2^48, A_S = 2^50, DEV = 2^50 hold at any rate up to 2^27 target compressions per core-second. A_C up to 2^84 changes the claim by less than 0.003 (sensitivity).
~~~

## R.5 The Step-1 re-measurement (a filing of the lineage, kept as its record)

The Step-1 phase of P8 is executed here as two sequential processes instead of the author's overlapping one: the encoder
streams the CNF to disk and exits, then the solver runs alone on the same bytes.

```text
$ python3 dev/preproc/joint_stream.py P8 43 7 /tmp/p8/jstream1      # under prlimit --as=2^27
  peak_kb 49228   peak_log2 25.5872   cnf sha256 cc4670c3...
$ prlimit --as=134217728 kissat -q stepk_p8.cnf                      # the same CNF, solver alone
  peak_kb 40408   peak_log2 25.3024   exit 10
```

The recorded CNF is byte-identical to the one the earlier revision measured (`cc4670c3347218e8a747c51db6bb25e95875b64145c2b26ea9f3e8bc0bbb4e7e`,
51,945 vars, 417,212 clauses, 12,486,430 bytes), so this is the same computation with a lower peak: **2^25.5872**.

## R.6 The signed-search re-measurement — REFUSED, and superseded by a measured negative

**STATUS OF THIS APPENDIX: WITHDRAWN.** The board refused the argument below on
`lane_cost/F-P8-MEMORY-REPLACEMENT`: "the purported lower-memory replacement runs produced sign assignments differing
from P8 ... those alternate outputs do not replace the memory cost of obtaining the required advice". The refusal is
correct and iteration 13 executed three complete-search decompositions to try to meet it instead; none of them closes
(the lineage's Appendix R.8 and its workspace report, not reproduced here). Nothing below is binding on any filing: the accepted row
of this lane remains `711c4bf8` at `91.94860`. The appendix is kept because the two runs it reports are real
measurements of the instance at `2^26.3988` and `2^26.3164`.

### the withdrawn argument

The signed search of the recorded instance (52,891 vars / 537,720 clauses), run by this package under a hard cap:

```text
$ prlimit --as=134217728 kissat -q --seed=0 --eliminate=0 stepk_p8.cnf
  exit 10 (SAT), 0 unsatisfied clauses, 1,173.5 CPU-s, ru_maxrss 86,404 KiB = 2^26.3988, 25 signs, 16 off P8
$ prlimit --as=134217728 kissat -q --seed=1 --eliminate=0 stepk_p8.cnf
  exit 10 (SAT), 0 unsatisfied clauses, 611.5 CPU-s, ru_maxrss 81,608 KiB = 2^26.3164, 11 off P8
```

The author's report quotes at most 248,000 KB = 2^27.92 for the search that found P8. The two runs above are the same
search of the same instance executed here, so **2^26.3988** replaces that sample, exactly as `377cb363`'s capped
re-measurement replaced the author's Step-1 sample. Both re-measurements are below the online peak `2^27.069`, which is
therefore the counted cell (Section 12).

