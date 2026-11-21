# sha256-r38: eight-column compact u-table, one-operation zero branches and a non-resident P8 record (time_log2 76.52419, memory_log2_bytes 27.02363, organizer rounded-field scalar 83.54782)
 Appendix AH records the two current numerical tightenings: the H8 message charge from the four-decimal floor -0.0119 to -0.011821 (still below the exact one-sided 99% lower bound -0.011820853637039925) and the H1W walk mean from the round charge 6.770000 to the panel's largest one-sided 99% upper bound 6.760092. The title, summary, ledger and Appendix A/U/Y/Z values are updated in place; Appendices AB-AG retain their historical filed values.
This filing composes two accepted entries. Newjordan `686d97d2` supplies the equivalent subtractive combined test, one-operation zero branches and Lemma-D postfilter prices; our `44c3ddeb` supplies the compact-column layout, exact census, 30-byte record and native witness. This filing restricts that layout to **eight relative columns 0 through 7** (coverage 64, probe limit 69), keeps six compact 39-bit lanes in each 30-byte record, and charges Appendix W's recorded tail list once rather than twice (Lemma RF, Appendix Z); the predecessor's signed-16 record width (Lemma RE2) is withdrawn as false, and no current claim depends on any record width. H7 changes explicitly from an average over uniform alignments to a per-alignment transfer premise at fixed R*=8174; every other probability and allowance premise is unchanged. Appendix AE tightens only the conservative numerical F7 bounds using the direct public parent's estimator. Appendix U proves the compact layout against the parent's measured ten-column census (Appendix AA re-executes it), and Appendix ZS restricts it to eight columns; Lemmas B'', D and Z the pricing changes. The counted phase maximum is the rescheduled preprocessing cell 136,433,664 bytes (Appendix ZS), which the compact eight-column online image 127,926,304 lies 8,507,360 below, and the charge is that counted maximum: memory_log2_bytes 27.02363, scalar 83.54782.

Accepted parents `686d97d2` and `44c3ddeb` both descend from the same fixed-table/P8 lineage. The former changes only equivalent tests and deterministic prices; the latter changes only geometry, packing, census and derived accounting. Every reused source is declared through the two direct credited parents and the retained dependency list.

The inherited P8 complete-message framework and P1 claw F(a0)+P(u) in S160 remain. The fixed relative-column restriction recomputes geometry, exact population bounds, useful-pair rate and cost. Historical 15-column observations keep their original domain.

Claim: time_log2=76.52419 from N=296428560360210811912418221 operations at C=2728, exact log2(N/C)=76.524186993467709038751294984268501131051960837856603693842223908173112346327493839186464759152770960438251732076881556231822365581243935546945559145103991329056627341896051067044009390287327539388323375755317374956836836349153959554334832620345473184645802171356511066674835661638802738642694768084035974868528718918270944779914713937570693342242792960777774562743635643592589811144575935905615703972129185446403665346614194404078102135806271642184484060825570223923303760644492802908614743854837733132219538913126656083674383950174911977811471523699227777028327927038497222109802200692498540447857541003511346209692361271199214005950967013401125245504789326588017671373693127909132843562976466168759598571948402830432637457751161822296400212030864060348634304200367083751776673613, rounded upward at five decimals. Every first block, kept or not, is charged C+25. The ordered walk is charged 6.760092 per C1 claw under H1W and step 3b at the H3B stopped-path mean 842.361097 per good pair; the deterministic 3,014-operation path remains in vmax. Success remains at least 0.39. Memory_log2_bytes=27.02363 is the upward rounding of log2(136433664)=27.0236291570188016337..., the counted phase maximum (the rescheduled preprocessing cell; Appendix ZS), which the eight-column online image 143654944 lies below. Preprocessing remains 2^61.58497 with A_C=A_S=DEV=2^60. Scalar projection=76.52419+27.02363-20=83.54782 (exact program value 83.5478202854980291726169923577055475307842556608042954394910841972215869251112653914284751577363813834122899900164363508606690511441909740883484941466843953387566155325712087524320552413125609744631116953884499799394953904199382993566364848584729569783392597279279148280694568786765525488508614151331155528862389259229448607579678296730960721751345171551300384322424231084195549370930344878899884935333209919483776432267813700831500485350104938179067500366380691673173430517813779122920237634676778894014221710406946218492438572415519820889789447725028894624586033225284197222239620040968114994723524316447327949298779339315817108142331392052470631828896634715814329164726769338423111147591477912270415090670945884394115). These are resource projections, not qualification results.

## 1. Target and output

SHA-256 steps 0..37 on every padded block, the standard IV once, FIPS 180-4 padding, feed-forward, all eight digest words. The procedure outputs two distinct 128-byte messages m = M0||M1 and m' = M0||M1' with a common first block M0 (FIPS padding appends the same third block).

**Lemma 1.** Let cv = F_38(IV, M0). If the second-block computations of M1 and M1' from cv end with equal state words A34..A37, E34..E37, the digests of m and m' are equal. *Proof:* the second-block output is cv plus (A37, A36, A35, A34, E37, E36, E35, E34), and the third block is the same for both. m != m' because M1 and M1' differ in W7. Every output is therefore a collision of the target.

## 2. Data and the P1 pair

- **P8 (1a695f0b, transcribed as data).** The 38-step semi-free-start pair (PCV, PMX, PMY), the cells of rows 7..37 (`CELLS`: for A, E, W the mask of fixed bits, their values and the XOR difference), the '+' pairs (`PQE`, the printed pairs except E18 = E17 at row 18) and the two-bit conditions (`X2`). S denotes the state words of the pair: A2..A15 and E6..E15 of member x (= PMX) and member y (= PMY). The program checks that PCV, PMX, PMY reproduce the pair and that step 3b accepts it (Section 12).
- **The P1 pair.** For a chaining value cv and two free words a0, a1, both members take A0 = a0, A1 = a1, A2..A15 and E6..E15 from S; E0..E5 and W0..W15 follow from the step equations (`variantW_P1`). W10..W15 are S's words; W0..W9 depend on (cv, a0, a1); W0..W6 and E0..E5 are equal in the two members. With a0 = A0, a1 = A1 and cv = PCV this is the P8 pair.
- **Row 16.** W16 = s1(W14) + W9 + s0(W1) + W0, so E16 of member x is E16x = C16 + W0 + s0(W1). From the step equations of steps 0 and 1, W1 = u := a1 + h(a0, cv) and W0 + C16 = F(a0) - u with F(a0) := Cc2 + a0 + k0(cv) + h(a0, cv) (Cc2 = 0x7af32e15; k0, h are written out in `cv_consts`, `hfun`), hence **E16x = F(a0) + P(u), P(u) := s0(u) - u**. S160 is the set of 160 words that pass every row-16 cell and condition of P8: the 20 heads `R16H` (all equal mod 2^13: head j is R16H[0] + 2^13 t_j with 20 distinct t_j < 2^19) plus the 8 offsets OFFS = {0, 1, 4, 5, 1024, 1025, 1028, 1029} (bits 0, 2, 10 free). A **claw** is a pair (a0, u) with F(a0) + P(u) in S160; every claw is a row-16 pass of member x, and a1 = u - h(a0, cv).
- **Post-filters.** For a claw, C1, C2, G and F7 retain exactly the accepted P8 definitions. A good pair passes all four. The counted chain uses Lemma D's six-operation partial `s0` and Lemma Z's zero branches: the C1 prefix is 6 operations and the later segment maxima are 13, 22 and 24. `pf_ref` evaluates the real words independently; historical participant controls and the current selftest report zero predicate mismatches.

## 3. The procedure: the u-table

### 3.1 The table and the epoch

The table has **9 columns x 2^19 rows of compact records**. Each record is 30 bytes; the table payload is 8 x 2^19 x 30 = 125,829,120 bytes, followed by a 32-byte terminal pad. A record holds **six 39-bit lanes** (234 bits) and a three-bit count in bits 234..236. Each lane is `[u:32][gap:1][field:6]`. Loads and masked stores use one 256-bit window; the two overlapping bytes belong to the next record and are preserved by the mask. The terminal pad makes the final access in-bounds.

```
lane L (bits 39L .. 39L+38) = [u: 32 bits][gap: 1 bit, stored 0][field: 6 bits];   field = tag in 0..7 (filled) or 22 (empty)
```

An **epoch** draws one fresh 32-bit **ustart**; the 13-bit alignment is the construction constant **R*=8174**. For a word u let G(u)=P(u)-R* (mod 2^32). Coverage, buckets, tags and first-six cyclic retention are otherwise unchanged. R*=8174 was fixed before outcomes because it is the highest-retained alignment among the four tables measured by H1W; it is not the census maximum (which is r=8150).

Exact census: coverage is 64*2^19=33,554,432 words. The exhaustive 8,192-alignment census gives minimum 23,694,709, maximum 23,773,042 and mean 23,725,806.57421875. The chosen alignment has **E(8174)=23,771,164** exactly, so every epoch table in this construction has that retained count. Appendix ZS derives this row from the recorded eight offset arrays and reproduces the parent's ten-column row 29,617,909/29,708,804/242,952,259,320 exactly as calibration.

### 3.2 The scan of one chaining value

For each a0 of the scanned window (the 2^20 a0 of SEL, Section 3.7; the lineage scanned all of W9 = [9 x 2^26, 10 x 2^26)), in order:

1. F0 = F0(a0) = F(a0) - KFm and yp = Hrp - F0 = Hr + 1029 - F(a0) (mod 2^32), where Hrp = R16H[0] - r + 1029 - KFm is computed once per chaining value. (Binding implementation: steps 1 and 2 are executed for 256 consecutive a0 at once by the bitsliced front end of Section 3.5, which outputs exactly the a0 for which step 2 probes; for those a0 only, F0 and yp are evaluated in 21 operations reusing S0(B) from the batch and an 8-bit table S0_LO[l].)
2. A claw (a0, u) requires G(u) = y + 2^13 t_j + o for a head j and an offset o in OFFS (Lemma C), where y = Hr - F(a0). Writing o = o' + 1024 win with o' in {0,1,4,5}, the low 13 bits of the target are those of yw + o' with yw = y + 1024 win, the same for all 20 heads. For a probing lane, bits 10..12 of (y + 5) mod 2^13 are either 000 (win = 0) or 111 (win = 1) and q = (y + 5) mod 1024 < 85 < 128; hence adding 1029 = 1024 + 5 in yp = y + 1029 gives rowb = yp >> 13 = (yw + 5) >> 13 and u0 = (yp & 127) + 3 = q + 3 in both cases without branching on win.
3. **Probe of a window.** From u0 = (yw + 8) mod 128, w = u0 & 7 = yw mod 8, c1 = u0 >> 3 (which equals c + 1 for c in 0..10 and 0 for the frame-crossing case c = 1023), and c = c1 - 1; note also that rowb = (yw + 5) >> 13 already equals row0 + 1 when c = 1023 and row0 when c <= 12. The words WBL0 and WBL1 = WBL0 + W8L carry 32 - w and 40 - w in every lane's field and nphi = (0x60000000 - PHI) mod 2^32 in bits 0..31. For each head j (with t_0 = 0 so head 0 needs no row addition, and 19 heads j >= 1 adding t_j mod 2^19), the procedure reads
   - the **main bucket** (column c, row rowj) if c < 9, testing for tags t with t - w in {0,1,4,5};
   - the **next bucket** if w >= 3 and c1 < 9: (column c1, row rowj), which is (c + 1, row0 + t_j) when c < 8 and (0, row0 + 1 + t_j) when c = 1023 (the target crosses into the next 2^13 frame); its test is for tags t with t + 8 - w in {1,4,5}.
4. **The combined test** of a bucket word d (Section 3.6): s = d + WBL and Z = (G - (s AND MT3)) AND G, four word operations (with WBL = WBL0 for the main bucket and WBL1 for the next bucket). WBL carries (32 - w) (main) or (40 - w) (next) in every lane's field and nphi = (0x60000000 - PHI) mod 2^32 below it (formed once per probing window in 2 ops from a0 - F0); MT3 = bits 1, 3 of every field and bits 29..31 of every lane; G = bit 5 of every field. **Lemma B''**: lane L fires (its bit 5 of Z is 1) iff its field is a filled tag t with t - w in {0,1,4,5} (main) or t + 8 - w in {1,4,5} (next) **and** the top three bits of E5 = u - PHI are 101 (C1). If Z != 0 (one branch on zero, Lemma Z) the procedure walks the fired lanes with the ordered comparison tree (`walk_lanes`, exact maximum 18 operations per nonempty read and weighted mean at most 7 per C1 claw under H1, charged 6.760092 under H1W; Appendix U). For each fired lane L, bits 0..31 of lane L in s = d + WBL already equal (E5 + 0x60000000) mod 2^32 with top 3 bits 000, so E5 = ((s >> 39L) & M) | 0xA0000000 recovers E5 directly in 2 operations, and the procedure runs the rest of the single-s0 post-filter chain (C2, G, F7: `pf_tail`) on (a0, E5). A good pair runs step 3b (rows 16..21 of both members, then the comparison of the eight output words; Lemma 1). If step 3b accepts, the procedure outputs m, m' and halts. The tag-only test Z0 = (((d + WB) AND MASK) + K) AND G (Lemma B' below; MASK = bits 1, 3, K = 31 in every field, WB carrying 32 - w or 40 - w) is not executed by the online procedure. It remains only in the separate `probe_exhaustive` selftest; that bounded development check is covered by H4c and is not part of online N.

**Lemma B' (the four-op tag-only test is exact; Lemma B'' of Section 3.6 extends it).** In each field, with offset b = 32 (main) or 40 (next), r = t + b - w with t in 0..7 or 22 and w in 0..7 lies in [25, 62]: the add never leaves the 6-bit field. For t <= 7: in the main bucket (b = 32), t - w in {0,1,4,5} iff r in {32, 33, 36, 37} iff (r AND 0b01010) = 0; in the next bucket (b = 40), t + 8 - w in {1,4,5} iff r in {33, 36, 37} iff (r AND 0b01010) = 0 (r = 32 is impossible because t <= 7 and w <= 7 give t + 40 - w >= 33). For an empty lane (t = 22), r = 54 - w in [47, 54] (main) or 62 - w in [55, 62] (next), whose bits 1 and 3 are never both 0: an empty lane never fires. Thus x = r AND 0b01010 in [0, 10] has x + 31 <= 41 < 64 setting bit 5 iff x != 0, and no carry leaves the field. `probe_exhaustive` executes the 256-bit test on words with random u fields for every kind, w and tag (2,304 lane checks, 0 mismatches; historical participant trial `utab-online-r38` 5). QED

**Lemma C (completeness and uniqueness).** For a chaining value, an epoch's table and an a0, the scan outputs exactly the pairs (a0, u) with u retained and F(a0) + P(u) in S160, each once. *Proof.* F + P(u) = R16H[j] + o iff G(u) = y + 2^13 t_j + o (because R16H[j] = R16H[0] + 2^13 t_j and G = P - r). A retained u has G mod 2^13 < 88; with o = o' + 1024 win and z = yw mod 2^13, (z + o') mod 2^13 < 72 forces (z + 5) mod 2^13 < 77, i.e. (y + 5 + 1024 win) mod 2^13 < 77, which is v = 0, q < 85 for win = 0 and v = 7, q < 85 for win = 1 (the two are mutually exclusive); so step 2 skips only a0 without claws. If z + o' < 2^13 the target lies in column c + [w + o' >= 8] of row (row0 + t_j) mod 2^19 (adding 2^13 t_j does not change the low 13 bits) with tag (w + o') mod 8; the main bucket holds the offsets with w + o' <= 7 (tag t, t - w = o'), the next bucket those with w + o' >= 8 (t = w + o' - 8, t + 8 - w = o' in {1,4,5}), which needs w >= 3; if z + o' >= 2^13 (z >= 8187, c = 1023) the target is in column 0 of row rowj + 1. Uncovered columns hold no entry, so skipping them loses nothing. By Lemma B' a lane fires exactly for these targets. Each retained u sits in exactly one lane, the 160 targets are distinct, so each claw is output once. QED With the combined test, the same argument with Lemma B'' in place of Lemma B' gives **Lemma C1** (Section 3.6): the scan outputs exactly the claws of this lemma whose E5 passes C1, each once.

Historical participant controls compare the claw list with an independent search (`ref_claws`: every retained entry indexed by its low 13 bits of G and matched against the 8 low patterns y + o, high part in the 20 t_j) and rebuild the real E16 of member x of every claw: EQUAL and 0 bad on every trial (Section 12), at the binding geometry and at full-frame coverage.

### 3.3 Lemma S: the selection is exactly uniform

**Lemma S (fixed-alignment form).** A word u is covered exactly when `(P(u)-8174) mod 8192 < 80`. Because P is balanced modulo 8192, the fixed covered set has exactly 72*2^19 words. Coverage is therefore a fixed residue-class condition, not a fresh uniform thinning. The retained prefix still varies with fresh ustart. H7 is strengthened explicitly: for this fixed alignment, averaged over ustart and the chaining value, acceptance is independent of coverage class and retention. This is a declared premise, not a theorem; rejecting it reverts exactly to h8f.

### 3.5 The bitsliced front end: direct-t register program (binding)

For a batch base B (a multiple of 256) the plane A_i (i = 0..31) holds bit i of a0 = B + l in bit lane l (l = 0..255): A_0..A_7 are the constant lane-index planes and A_8..A_31 are all-zero or all-one by the bits of B. Rather than rippling E0 = a0 + E0base across 32 bits per batch and reducing six 13-bit operands as in `bs_mask`, the binding register program (`bs_mask_rm` in utab38.py) exploits two exact identities on a0 = B + l (l in 0..255): (i) on bits 0..7, -l + (MAJ(l, a, b) & 255) + (CH(E_lo(l), e, f) & 255) = U_cv(l) - (~(a | b) & 255), where E_lo(l) = (l + E0base) & 255 and U_cv(l) = ((~l) & ~(a ^ b) & 255) + (CH(E_lo(l), e, f) & 255) in [0, 510] depends only on the chaining value and is precomputed in nine 256-bit planes U[0..8] once per chaining value (`cv_consts`, inside the 1,024-operation front-end setup); the carry of l + (E0base & 255) into bit 8 of E0 is the single plane c8 = {l : l >= 256 - (E0base & 255)}, so the high bits E_hi(l) = (B + E0base_hi) + 256 c8(l) take only two scalar values across the batch: e_hi0 = B + E0base_hi (where c8 = 0) and e_hi1 = e_hi0 + 256 (where c8 = 1); (ii) on bits 8..12, (B & 0x1f00) - (MAJ(B, a, b) & 0x1f00) = (B & ~(a ^ b) & 0x1f00) - (a & b & 0x1f00). Folding the chaining-value constants into K_cv = (KF + (~(a | b) & 255) - (a & b & 0x1f00) - 5) mod 2^13 and absorbing the scalar high-bit rotations (S0(B) & 0x13c0) and (S1(e_hi) & 0x107c) + CH_hi(e_hi) into the two 13-bit branch scalars k0 (for c8 = 0) and k1 (for c8 = 1) reduces each column i in 0..12 of **t = (Hr + 5 - F(B + l)) mod 2^13** to at most three active bit planes (one from U[0..8] or A_0..A_2, one from A_2..A_7 or EG[0..7], and one from G = (0, ~c8, c8, ONES) selected by the bits of k0 and k1). In `cv_consts`, the first CSA (or HA) stage of each column i = 0..12 over all 3- to 5-bit combinations of the column's selector bits is pre-folded once per chaining value into the column table `CT[0..12]` (396 planes in all; 1,024 operations including U, EG and G).

**Pricing: a constant-time 218-operation register program.** Executed on a machine with **16 registers** of 256 bits (`bs_mask_rm`, whose class `RM` counts every operation and asserts that at most 16 planes are live; the peak is **8**), every load, store, gate (and, or, xor, not) and immediate/scalar operation is **one** operation: (1) batch scalar setup (43 ops) and packed 46-bit column-index word w_idx via five constant spread tables SP_S0, SP_S10, SP_S11, SP_K0, SP_K1 (17 ops): e_hi0, e_hi1, S0(B), S1(e_hi0), S1(e_hi1), ch_0, ch_1, k_base, k0, k1 and w_idx (60 ops); (2) column index extraction from w_idx across i = 0..12 (24 ops: 1 op for i = 0 and i = 12, 2 ops for i = 1..11); (3) register loads from CT[0..12] (27 planes x 2 ops [address + load] = 54 ops, 0 stores); (4) vector gates (80 ops): reducing the pre-folded column sums and carries to t_0..t_12 (4 gates in col 1 using the disjoint binary carry decomposition S_0 = ge_0 + 2 c1_0 + 4 c2_0 with c2_0 & (s1 & c1_0) = 0; 32 in cols 2..5; 9 in col 6; 12 in cols 7..8; 6 in col 9; 10 in cols 10..11; 2 in col 12), maintaining the De Morgan dual running comparison ge = ~lt = (t mod 2^(i+1) >= 93 mod 2^(i+1)) in 1 gate per column for i = 1..9 (`ge = t & ge` when bit i of 93 is 1, `ge = t | ge` when 0, eliminating all per-column NOT gates), and 5 gates testing bits 10..12 all equal and negating `(T10 ^ T11) | (T11 ^ T12) | ge`. Because every branch is replaced by table loads and bit-masking, the program executes **exactly 218 operations for every batch and every chaining value** (`gbs_worst` = 218; 3,000 random constant sets: min 218, max 218). The register program is column-count invariant: it evaluates t_i for i = 0..12 and the mask comparator is set to the active limit, so the eight-column restriction, which reads only columns 0..10, executes the same 218 operations. The ledger charges 218 + 8 (batch loop and V add) + 2 (branch on an empty mask) per 256 a0 = **0.8906 per a0** (0.9180 with the sub-block loop of 7). For each lane of the mask (probability 138/8192 per a0) 16-bit table-assisted lowest-set-bit extraction (20, using the CTZ16 table load) and scalar F0, yp (21, reusing S0(B) from the batch) and the probe run as in Section 3.2.

Lemma F remains exact with threshold 85: the comparator computes the same scalar probing predicate and retains the constant 218-operation bound. The inherited full-W9 witness used threshold 125 and remains historical 15-column evidence. The current isolated selftest and historical participant trial 6 compare the ten-column scalar and register masks (bs_gates_max 218, bs_gate_worst 218, 0 mismatches), and Appendix U records the compact-layout comparisons.

### 3.6 C1 inside the bucket word (Lemmas B'' and C1)

**What is tested.** For a claw (a0, u), the lineage's chain forms E5 = (u - F) + K2E5 + a0 = a1 + cE5 (a1 = u - h(a0), K2E5 = Cc2 + k0 + cE5; `pf_consts`), and its first segment tests **C1: the top three bits of E5 are 101** (probability 1/8 for a uniform a1, Section 6). Write **PHI = PHI(a0) := F(a0) - a0 - K2E5 (mod 2^32)**. Then E5 = u - PHI (mod 2^32), and PHI depends only on the chaining value and a0. It is the same for the 20 heads and both buckets of a probe, so it is formed once per probing window. The u of every filled lane of a bucket is in the bucket word, so C1 can be decided for the six lanes at once, by the same kind of carry-confined lane arithmetic as the tag test (Lemma B').

**Lane format and constants.** Lane L of a bucket (bits 39L .. 39L + 38) is [u: bits 0..31][gap: bit 32, stored 0][field: bits 33..38]. The loader writes u | tag << 33 (with empty mark 22; the epoch build, its cost and the bucket contents are otherwise those of Section 3.1). Per probing window the procedure forms nphi = ((a0 - F0) + KNPHI) mod 2^32 = (0x60000000 - PHI) mod 2^32 (with KNPHI = (0x60000000 + K2E5 - KFm) mod 2^32, 2 operations), WBL0 (the 256-bit word with nphi + (32 - w) x 2^33 in every lane, formed by broadcasting nphi + ((32 - w) << 33) across the six lanes in 9 operations) and WBL1 = WBL0 + W8L (1 operation, where W8L has 8 << 33 in every lane, giving 40 - w in every field for the next bucket). The constants are MT3 (in every lane bits 29..31 and field bits 1, 3) and G (field bit 5 of every lane). The binding read computes **s = d + WBL** and **Z = (G - (s AND MT3)) AND G**: add, and, subtract, and, four word operations (with WBL = WBL0 for the main bucket and WBL1 for the next).

**Lemma B'' (the binding four-op combined test is exact).** Lane L fires (bit 5 of its field in Z is 1) iff the lane is filled with a tag t such that t - w is in {0,1,4,5} (main) or t + 8 - w is in {1,4,5} (next), **and** top3((u - PHI) mod 2^32) = 101. *Proof.* (i) *s = d + WBL.* In lane L the low part is u + nphi, in [0, 2^33), so its carry c0 in {0, 1} enters bit 32 (the gap bit, stored 0 in d and 0 in WBL) and never reaches bit 33. The field is r = f + b - w (b = 32 for main, 40 for next), in [25, 62] for f in 0..7 or 22 (Lemma B'), so it never reaches bit 39. The spare bits stay 0, so no carry enters lane L + 1. Since (u + nphi) mod 2^32 = (E5 + 0x60000000) mod 2^32, bits 29..31 of s are e' = (top3(E5) + 3) mod 8, which equals 0 iff top3(E5) = 5 = 101_2 (C1 holds). (ii) *AND MT3* leaves, in each lane, q = e' x 2^29 + x x 2^33, where x = r AND 0b01010. Thus 0 <= q < 2^38, and q = 0 iff C1 holds and the filled tag passes Lemma B'. (iii) In base 2^39 the packed word G is the sum of one 2^38 guard per lane. Every lane subtraction 2^38 - q is nonnegative and below 2^39, so no borrow crosses a lane boundary. Its guard bit is 1 exactly when q = 0; if q > 0, the result is below 2^38. (iv) *AND G* isolates those guard bits. Empty lanes have x != 0 by Lemma B', so they do not fire. QED

**Lemma C1 (completeness and uniqueness with C1).** For a chaining value, an epoch's table and an a0, the scan with the combined test outputs exactly the claws of Lemma C whose E5 = u - PHI(a0) passes C1, each once. *Proof.* The windows, reads and offsets are those of Lemma C. By Lemma B'' a lane fires in the combined test iff it fires in the tag-only test and its u passes C1. QED

C1 is the first postfilter, so fusing it into the bucket test preserves every good pair within the retained columns. This is an output-preserving restriction of the 15-column construction, not equality to its unfiltered output. The probability argument uses the new exact retained minimum and H7 in its stated averaged form; N_CV is recomputed in Section 7.

**Pricing.** A read is address + load 2, the four word operations and a branch on Z = 0, 1 (Lemma Z): **7** (was 8). Per probing window: nphi = (a0 - F0) + KNPHI 2, (32 - w) << 33 and add nphi 3, broadcast to six lanes 6, WBL1 = WBL0 + W8L 1: **12**, plus window setup **14** (rowb, u0, w, c1, c, path flags, two column bases, V add). Per C1-claw, the ordered tree has a table-wide mean bound of **7** under H1. Each path consists only of charged word comparisons and conditional branches; the full-mask maximum is **18 per nonempty read**, and fixed leaves emit ascending lanes (Appendix U). Then direct recovery E5 = ((s >> 39L) & M) | 0xA0000000 **2** (since bits 0..31 of lane L of s = d + WBL equal (E5 + 0x60000000) mod 2^32 with top 3 bits 000 when C1 holds), then the single-s0 post-filter segments 2..4 (`pf_tail`: **13** (with the unconditional C1-claw V add folded into its V add), **22** on C2, **24** on C2 and G, each evaluating s0 on the base word only (6 operations, Lemma D) and testing the difference by carry-free bit identities) and step 3b on a good pair. Under H1 a claw passes C1 with probability 1/8. The full-scale C port measured 0.124995 over 778,357,004 claws (Section 13).

**Checks.** `probe_c1_exhaustive` (in `selftest` and in trial 5 of `utab-online-r38`) compares the 256-bit combined test with its scalar definition (filled, tag test, top3(u - PHI) = 93) on 16,128 lanes. 2,304 of them use edge values of PHI (0, 1, 2, 2^32 - 1, ...) and of E5 (at and around 0xA0000000, 0xC0000000, 0 and 2^32 - 1) and random ones. The other 13,824 are 2,304 words covering every lane class: kind x w x tag (0..7 and the empty mark) x top3(E5) (8 values) x [u + LAM >= 2^32], each placed at lane position (index mod 6) among random filled or empty neighbours, with all six lanes of every word checked. Result: 0 mismatches, 568 firing lanes. Historical participant controls check Lemma C1 itself. The tag-only claws of the scan equal the independent search (`claws_equal_ref`). The C1-claws equal the independent search restricted to the claws whose C1 holds on the real words of both members (`c1_claws_equal_ref`, with C1 from `pf_ref`). The post-filter flags of every C1-claw equal the real-word definitions (`postfilter_ref_mismatch`). Development check (not shipped; `dense_trial` at full-frame coverage with 2^20 words and 2^14 a0, 128 seeds `dev|big|0..127`): 81,842 claws, every seed's tag-only claws equal to the independent search; 10,185 C1-claws (rate 0.12445; 1/8 = 0.125), every seed's C1-claws equal to the independent search restricted to C1 on the real words; 1,008 of them pass C2 (0.0990 against the exact P(C2 | C1) = 0.0989); 0 row-16 mismatches and 0 post-filter mismatches.

### 3.7 The inherited SEL window and H8

SEL is the fixed 4096 selected 256-a0 sub-blocks of W9, totaling 2^20 a0, with the unchanged bitmap/hash in the program. Exact N12=53096854 and G_SEL=2051404269120 give the stated postfilter rate. The charged message factor is 2^-0.011821. H8 assumes the conditional state acceptance is independent of the selected sub-blocks given the message-difference profile. The complete original argument, exact counts, registration, paired message-profile/forced-bit records, confidence bounds and limitations are retained as Appendix V section `support-3.7`. Current eight-column geometry does not turn those historical measurements into new probability evidence.

### 3.8 The inherited kept CV class and H9

Keep exactly ((cv0>>24)&63)==12, a 2^-6 class under H1. Its F7 rate is charged at **0.1205926** and the step-3b cost at the upper bound **0.1206112**, the two one-sided 99% bounds of the class rate measured by the public parent's exhaustive-density estimator: the per-top-byte F7 density is enumerated over all 2^32 words (reproducing |F7| = 287,309,824 exactly), and the class average over cv[0] is computed in closed form for each G-conditioned q, so only the q distribution is sampled; over 3.21e7 X-samples the class rate is 0.1206019 +- 0.0000031, and the estimator's exact equal-weight control returns 0.066894531 against |F7|/2^32 = 0.06689453125. The earlier 2^20-q interval is superseded and not used. Message factor 2^-0.0225. H9 retains the same conditional-state transfer premise. No class, advice or acceptance condition changes here.

### 3.4 Pseudocode

```text
input: N_CV, K = 2^40, V_MAX, the advice SEL.  V = 0 (a register: the online operations executed so far)
for e = 1 .. ceil(N_CV / K):                                   # an epoch
    if V > V_MAX: halt (failure)
    draw one random word: ustart (32 bits); use fixed r = R* = 8174
    reset the 10 x 2^19 compact records to EMPTY; for n = 0 .. 2^32-1: u = ustart + n; insert u (Section 3.1)
    V += the epoch's counted work
    for j = 1 .. K:                                            # a first block
        if V > V_MAX: halt (failure)
        draw M0 (16 random words); cv := F_38(IV, M0)
        if (cv[0] >> 24) & 63 != 12: V += C + 25; next j       # the kept class (Section 3.8); one V add per first block
        the claw scalars of cv; Hr = R16H[0] - r
        V += C + 25 + 70 + 1,024                                # this first block and the kept chaining value's fixed work (+ front-end setup)
        for each sub-block of SEL (V += 7), its batch of 256 consecutive a0: the front end (V += its charge); for each a0 of the output mask:
                      extract it, F0, yp (V += 41), probe: nphi, WBL0, WBL1, the combined test on every read (V +=
                      the probe's counted work); a read with a fired lane: ordered lane tree; per C1-claw: E5 from s, the chain's
                      segments 2..4 (each adds its own cost to V); a good pair runs step 3b; if it accepts: output, halt
halt (failure)
```

The procedure draws only its own first blocks; each costs one compression, 16 random-word operations for M0, the 3 operations of the class test and 6 control operations (cap test 2, its single work-counter add 1, loop control 3), kept or not; a kept one adds the 70 operations of the chaining value's setup (the lineage's cv_begin 75 less its V add, cap test and loop, which are the per-block control above, plus Hr), inside the fixed part. No other first-block enumeration is executed, so none is charged.

## 4. Pricing (H5')

collision-frontier-v5, 256-bit word RAM: load, store, address, arithmetic, logic, shift, immediate and random word cost 1; compare-and-branch costs 2; a conditional branch reading a computed zero/nonzero word costs 1 (Lemma Z); S0, S1, s0, s1 cost 8 except the proved six-operation partial-s0 uses of Lemma D; CH costs 3; MAJ costs 4 and the stated folded forms cost 2; one target compression C=2728. Every work-counter add is charged. `scan_cv` and `build_table` count the explicit operations through `Mach`.

| segment | operations |
|---|---|
| per word u of an epoch: u = ustart + n 1, s0 8, sub 1, - r 1, and 8191 1, loop 3, covered? branch 2 | 17 |
| covered and inserted: column, row, index (shift, add) 4, address + load 2, count 1, full? 2, lane (and, shift, or) 3, lane shift and clear mask from constant tables 2 + 2, and, shift, or, count add 4, address + store 2 | +22 |
| covered and dropped (bucket full) | +9 |
| reset, per bucket (address + store 2, loop 3); epoch setup (random word, split, V add, cap test) | 5; 6 |
| per first block, kept or not: compression C, 16 random words for M0 (1 each), class test 3 (and 1, compare-and-branch 2; Section 3.8), cap test 2, V add 1, loop 3; per kept chaining value: setup 70 (first-block words 30, claw and post-filter scalars 38, random word 1, Hr 1) | C + 25; 70 |
| per selected sub-block (Section 3.7): index load 2, base (shift, add) 2, loop 3 | 7 / 256 per a0 |
| per batch of 256 a0 (Section 3.5): the register program, 218 (loads, gates, scalar/index ops) + batch loop and V add 8 + empty-mask branch 2; per chaining value 1,024 for the front-end setup | 228 / 256 = 0.8906 per a0 |
| per a0 of the mask (probability 138/8192): 16-bit table-assisted lowest-set-bit extraction 20 (neg, and, xor, 3 x (and, branch), shift, and, CTZ16 load, add, loop branch), a0 1, F0 18 (reusing S0(B) and S0_LO[l]), yp 1, V add 1 | 20 + 21 |
| per probing window: rowb 1, u0 2, w 1, c1 1, c 1, two path flags 4, two column bases 3, V add 1 | 14 |
| per probing window, Section 3.6: nphi = (a0 - F0) + KNPHI 2, (32 - w) << 33 + nphi 3, broadcast (3 x (shift, or)) 6, WBL1 = WBL0 + W8L 1 | 12 |
| per head (19 nonzero heads j = 1..19; head 0 has t_0 = 0 and uses rowb directly): rowj (add t_j, and) | 2 (x 19 heads) |
| per bucket read, the combined tag and C1 test: address + load 2, add 1, and 1, sub 1, and 1, branch on zero 1 | 7 |
| ordered lane tree of a nonempty read: exact maximum 18 operations; additive per-lane bounds 6,6,6,8,8,8; prefix retention and H1 give mean at most 7 per C1 claw; H1W gives 6.760092 | 6.760092 mean (H1W); 18/read maximum |
| frame-crossing next bucket: rowb = (yp >> 13) already equals row0 + 1 when c = 1023 and c1 = 0, so no extra row add is needed | +0 |
| per C1-claw: E5 recovery 2; Lemma-D/Z postfilter segments 13 + 22 x [C2] + 24 x [C2 G]; step 3b stops after the first failed row; H3B charges mean 842.361097 and vmax keeps the 3,014 all-pass path | 2 + chain |

Step 3b has longest path 3,014 operations (every test passing, counted by `selftest` on the P8 pair). The charged source now builds both paths through row 15, advances rows 16..21 one row at a time, and returns on the first failed row; it computes rows 22..37 only on the all-pass path. The ledger therefore charges H3B's 842.361097 stopped-path mean per good pair, while vmax and OVER retain the exact 3,014-operation maximum. The 256-bit word test of a bucket is four word operations, C1 included (Section 3.6); rotations and sigmas of scalar words are the lineage's 8 operations, except the post-filter's s0 tests (6, Lemma D); the front end is bitsliced and charged as a register program with every load and store counted (Section 3.5). **Lemma D (this filing).** For 32-bit x let X = x OR (x << 32) (2 operations), Y = X XOR (X >> 4) XOR (X >> 15) (4). For i in 0..28, Y[i+3] = X[i+3] XOR X[i+7] XOR X[i+18] = x[i+3] XOR x[(i+7) mod 32] XOR x[(i+18) mod 32] = s0(x)[i], since X[k] = x[k mod 32] for k < 64. Every mask `pf_tail` applies to s0(w9), s0(w8) or s0(w7) lies in bits 0..28 (the widest is 0x1dc03800), so (s0(x) AND m) = v iff (Y AND (m << 3)) = (v << 3); z8's term (w8 >> 5) AND 0x006600c0 becomes (w8 >> 2) AND 0x03300600 at equal cost. Each s0 costs 6, not 8 (`s0d`) with unchanged flags. **Lemma Z (this filing).** The model prices comparison and conditional branch at 1 each. A test of a word against zero needs no comparison: the conditional branch reads the word (`Mach.bz`, 1). It prices the read's Z = 0 test and pf_tail's single-bit tests w9 AND 2^29, w7 AND 2^29, w7 AND 2^30 (and 1, branch 1). Mask-equality tests and walk thresholds keep compare-and-branch 2. The walk compares Z with sparse(m) + 1 for the 62 split masks m of the lineage's tree (`WT`, replacing its 4 KB threshold literal); z < sparse(m) + 1 iff the old test Z_old >= T held, on all 64 masks: same paths and charges. Segments cost 13, 22 and 24. Checked on all 2^32 words; old and new `pf_tail` agree on 518,506 random draws (118,506 reach segments 2..4), 2 fewer counted operations per executed segment; registered trials 0..3 and utab-rows-r38 trial 8 recheck it.

## 5. The ledger

Under H1, y=R16H[0]-r-F(a0) is uniform. A window probes with probability 2*77/8192=138/8192. Conditional on probing, s=(yw+5) mod 8192 is uniform in [0,85). There are 88 main-read positions and 55 next-read positions: 10*5 interior positions and 5 frame crossings. Each of 20 heads therefore makes 143/93 reads, so reads/probe=2080/69. Frame crossings cost no extra operation beyond the charged read addressing.

- Probe cost=14+12+19*2+7*(2080/69)=18976/69 operations. Read cost is 7 (Lemma Z); the 218-operation front end and setup/loop charges are unchanged.
- Claws/a0=160*E/2^32. Use the fixed table's exact E=23,771,164 for both success and cost under the strengthened H7 premise. C1-claws/a0=20*E/2^32. These statements follow per retained entry under H1 and require no fitted query-frequency model.
- per C1-claw, in expectation under H1, H1W and H3B: 6.760092 + 2 + 13 + 22 x P(C2 | C1) + 24 x P(C2 G | C1, SEL) + (q_pf_hi / P(C1)) x 842.361097 = **24.3958866956861381048...**. The walk charge is the declared H1W mean; Appendix U keeps the separate exact 18-operation maximum.
- Per_a0=235/256+(138/8192)*(41+18976/69)+(20*23771164/2^32)*per_C1=8.94191160597174093786557199060916900634765625. Displayed decimals never replace exact rational terms.

**Per first block.** wbar=C+25+2^-6*(70+1024+2^20*per_a0)=**149,274.373502241003525989531494140625**. The deterministic maximum uses the exact 18/read and 3,014 step3b path: vmax=**775,008,730,887**.

Per epoch: build=6+8*2^19*5+2^32*17+23,771,164*22+(33,554,432-23,771,164)*9=73725382232. The epoch length K is a free design parameter: Lemma 3 conditions on the tables and bounds the work for every table, and Lemma T and H3-P1 likewise bound every table uniformly, so none of them carries a term in K. Following GoForceX PR 1560, this filing takes K = 2^40 drawn first blocks per epoch, i.e. K/64 = 2^34 class-kept chaining values per fresh table. The build is then 0.000037% of an epoch and fresh ustart with fixed R*=8174 tables are drawn 1,445,295,614 times, one per 2^40 drawn first blocks. N_CV uses the fixed table's exact count 23,771,164 in the useful-pair rate. The conservative compensation ratio relative to the control is 44,436,632/29,617,909. It is not 15/12, and no extra multiplier is applied after inverting that rate.

| quantity | value |
|---|---|
| N_CV first blocks | 1,985,730,719,901,168,031,200 |
| epochs ceil(N_CV/2^40) | 1,806,011,569 |
| V_CV=ceil((1+2^-20)*N_CV*wbar) | 296,418,991,844,310,695,027,883,684 |
| V_MAX=epochs*build+V_CV | 296,419,124,850,616,334,451,240,566 |
| ALLOW=3*2^60*C | 9,435,509,593,702,435,651,584 |
| OVER=vmax | 775,008,730,887 |
| FIN=6*C+1600+2^24 | 16,795,184 |
| N | 296,428,560,360,210,811,912,418,221 |
| time_log2=log2(N/2728) | 76.524186993467709038751294984268501131051960837856603693842223908173112346327493839186464759152770960438251732076881556231822365581243935546945559145103991329056627341896051067044009390287327539388323375755317374956836836349153959554334832620345473184645802171356511066674835661638802738642694768084035974868528718918270944779914713937570693342242792960777774562743635643592589811144575935905615703972129185446403665346614194404078102135806271642184484060825570223923303760644492802908614743854837733132219538913126656083674383950174911977811471523699227777028327927038497222109802200692498540447857541003511346209692361271199214005950967013401125245504789326588017671373693127909132843562976466168759598571948402830432637457751161822296400212030864060348634304200367083751776673613..., charged 76.52419 |

**Lemma 2 (the cap).** The cap test reads V at the start of every epoch and of every first block; at that moment V equals the online work executed so far. An epoch build started with V <= V_MAX adds at most build <= vmax, a chaining value at most vmax. Hence the executed online work is at most V_MAX + vmax for every execution.

**Lemma 3 (cap halt).** Condition on the tables of all epochs. The epoch builds are then fixed and total at most epochs x build. The works W_j of the chaining values are independent (H1: fresh first blocks; the table is fixed), 0 <= W_j <= vmax and E[W_j | tables] <= wbar for every table. The procedure halts at a cap test only if the sum of the W_j exceeds (1 + 2^-20) N_CV wbar; Var(W_j) <= vmax wbar, so Bernstein's inequality gives a probability at most exp(-169.3477), far below the reserved 2^-60 margin, for every set of tables and hence unconditionally. No variance premise beyond H1 and the deterministic bound vmax is used.

## 6. The post-filter law q_pf (H1-P1)

Exact counts over all 2^32 values (own exhaustive program of the lineage): P(C1) = 1/8; |C1 and C2| = 53,096,854 (C1, C2 read only a1); for a0 in W9 the (a1 in C1 and C2)-summed count of G is 57,726,359,870,197, so P(C1 C2 G) = 57,726,359,870,197 / 2^58; |F7| = 287,309,824. Hence q_pf = 57,726,359,870,197 x 287,309,824 / 2^90 = 2^-16.1877.

**Why these rates bind the claws of the u-table (derived from H1).** For a uniform chaining value, F(a0) = Cc2 + a0 + k0 + h(a0) contains -cv[7] once (in k0) and h(a0) contains -cv[6] once (cv[6] enters k0 only through CH(e, f, g), inside F): so F(a0) and h(a0) are uniform and independent, and cv[0] is uniform given both. The table is fixed by the epoch, the claw's u depends only on F(a0) and the table, so **a1 = u - h(a0) is uniform and independent of the claw event**; C1 and C2 (a1 only) pass at the exact rates; every a0 of W9 has the same expected claw count (y is uniform for every a0), so the G rate of a claw is the W9-summed count above; and W7 = KK7c + MAJ(A2, a1, a0) - CH(E6, E5, E4) with KK7c = E7 - 2 A3 - cv[0] + ... is uniform given (a0, a1), so F7 passes at |F7|/2^32 (the lineage's statement "F7, averaged over a uniform chaining value, has probability |F7|/2^32 for any law of (a0, a1)"). H1-P1 is the premise that these rates hold for the claws the procedure finds; under H1 it is a consequence, and it is measured at full scale: the C port (Section 13) on seven chaining values, 778,357,004 claws, pooled C1 0.124995 (exact 1/8), C2|C1 2^-3.3380 (exact 2^-3.3379), G|C1C2 2^-5.9437 (exact 2^-5.9478), F7|C1C2G 0.0812 (|F7|/2^32 = 0.0669). F7 reads cv[0] and is strongly overdispersed across chaining values (per-chaining-value good-pair counts 605 to 2,495 on equal claw counts), so seven chaining values do not resolve its mean; the lineage's 24-chaining-value panel pooled 0.06618 (Appendix H.1), and the charge uses the exact |F7|/2^32, which holds in expectation over a uniform chaining value as derived above. **With the window (Section 3.7)** the same derivation holds with a0 uniform over SEL instead of W9. The G rate of a claw is then the exact SEL count, P(G | C1 C2, SEL) = 2,051,404,269,120 / (2^20 x 53,096,854) = 0.0368453386, and F7 stays at |F7| / 2^32. So **q_pf(SEL) = (53,096,854 / 2^32) x 0.0368453386 x 287,309,824 / 2^32 = 2^-15.0022** (W9: 2^-16.1877). With the kept class (Section 3.8) the F7 entry is 0.1205926, so **q_pf(SEL, class) = (53,096,854 / 2^32) x 0.0368453386 x 0.1205926 = 2^-14.1520** (W9: 2^-16.1877), which is the rate every success computation below uses. **With the class (Section 3.8, H9)** cv[0] is uniform in the class instead of over all words, and F7 passes at the class's rate: q_pf(SEL, class) = (53,096,854 / 2^32) x 0.0368453386 x 0.1205926 = 2^-14.1520 (the step-3b cost at 0.1206112: 2^-14.1429).

## 7. Success probability

Let X_j be the number of good pairs of chaining value j that step 3b accepts, and q3r the probability that a good pair is accepted.

- **H2-P1.** q3r >= q3_P1 x 2^32 / 160 = 2^-71.4010, q3_P1 = 2^-96.0791 = q3_model x 2^min(0, D_LB): q3_model = 2^-96.0133 is the registered accepted-event rate of the A0-variant good pairs before row 16 (Pr[row 16] = 160/2^32), and D_LB = -0.0658 is the one-sided 99% lower bound of the paired difference between the P1 family **on the window W9 = [9 x 2^26, 10 x 2^26)** and the A0-variant family (Section 9). Every a0 this procedure scans lies in W9, so the measured window contains the scanned one (the lineage's H10 for W11 is not needed). The procedure scans the subset SEL of W9, and that restriction is the separate premise H8 (Section 3.7).
- **H8 (Section 3.7).** The good pairs of the window are accepted with probability at least 2^MSG_LO q3r = 2^-0.011821 q3r (the window's message part, measured, charged at its 99% lower bound; the state part unchanged by H8), and their average acceptance satisfies the same registered upper form a-bar <= 2^10 q3r.
- **H9 (Section 3.8).** The good pairs of kept chaining values are accepted with probability at least 2^MSG_CLS x 2^MSG_LO q3r = 2^-0.0225 x 2^-0.011821 q3r (the class's message part, measured, charged at its 99% lower bound; the state part unchanged by H9), with the same registered upper form a-bar <= 2^10 q3r.
- **Expectation over the epoch's coins.** Averaged over ustart and the chaining value at fixed R*=8174, E[X_j] = 2^20 x (160 E-bar / 2^32) x q_pf(SEL, class) x q3r for a kept chaining value (X_j = 0 for a first block that is not kept), where E-bar=23,771,164 is the exact retained count of the fixed table. The argument uses the strengthened per-alignment H7 premise.
- **Within a chaining value (H3-P1).** For a fixed chaining value and table the scan is deterministic and complete (Lemma C): X_j = J, the number of accepted good pairs among all claws of the chaining value. **H3-P1** (Section 8) gives E[J(J-1)] <= 2^-7.5 E[J]; Bonferroni gives Pr[X_j >= 1 | table] >= (1 - 2^-8.5) E[X_j | table].
Across chaining values and epochs, retain the proof using independence under H1 and fresh ustart with fixed R*=8174. Lemma T uses only nonnegative per-u acceptance and the exact fixed-table count |U_T|=23,771,164, giving q3*(T)<=2^32*a-bar/23,771,164. The per-table good-pair bound uses 9 columns: 2^20*160*(6*8*2^19)/2^32*(2051404269120/2^52)*0.1206112. Multiplying by K/64, 2^32/23,771,164 and the registered upper form gives K*p_max=2^-28.2341<2^-28. The favorable lower-bound factors MSG_LO and MSG_CLS enter E[p], but are not used to reduce this upper bound. Charge the unchanged second-order factor 1-2^-25. The epoch length is 2^40 first blocks (Section 5), so this is the conservative reading: the overlap bound is charged as the 2^-25 it was registered at for the shorter epoch, one step above the 2^-19 it would be if the overlap scaled linearly in K, and the sensitivity is 2^-25 - 2^-19 = 1.9e-6 in the per-epoch rate, i.e. 2.7e-6 bit of score, so the choice of K does not carry this term. Thus an epoch fails with probability at most exp(-K*E[p]*(1-2^-25)). H7 is explicitly strengthened to a per-alignment acceptance/retention transfer premise at R*=8174. Finite parity does not prove it.
N_CV=1985730719901168031200 is the least integer obtained by inverting the full rate with the 0.39 target and 2^-60 margin. N_E=1806011569 full epochs includes extra first blocks only in the final epoch. The independent verifier reconstructs every integer and gives Bernstein exponent 169.3477. The success expression is 0.39000000000000000000003866693520514124... before the cap-failure bound.

## 8. Inherited within-CV dependence premise H3-P1

H3-P1 gives E[J(J-1)]<=2^-7.5*E[J], counting one pair per endpoint-sharing group. Bonferroni then supplies 1-2^-8.5. The full argument and original registered 24-CV panel remain in Appendix V section `support-8`. Finite restriction checks do not prove this premise. Historical participant-retained shallow control: utab-rows-r38 trial 6 (claim.json, H3-P1 extrapolation).

## 9. Inherited P1 q3 transfer H2-P1 and estimator validity H2b

Charge q3_P1=2^-96.0791 from the registered level-96.0133 and paired correction-0.0658; q3r=q3_P1*2^32/160=2^-71.4010. H2-P1 transfers this rate to good pairs, and H2b asserts estimator validity. The registered upper form a-bar<=2^10*q3r is used only in the epoch second-order term. Original registrations, seeded results remain in Appendix V section `support-9` and Appendices P/Q. No current small experiment measures this rare event. Historical participant-retained shallow known-answer control: utab-rows-r38 trial 8 (claim.json, H2b extrapolation).

## 10. Memory (H6) and advice

Online: 8*2^19 compact 30-byte records occupy 125,829,120 bytes; a 32-byte terminal pad makes the final unaligned 256-bit access safe. A complete 2,097,152-byte allowance covers all code, advice, thresholds, controls, planes, registers, stack, postfilter/step3b state, buffers, allocator and reserve. The online image is 127,926,304. The portable native witness is the parent's: restricted to the parent's ten columns it touches all 5,242,880 record addresses of that geometry and reports allocation 127,926,304 with peak resident 160,505,856, so it is platform evidence for the parent's image; this filing's eight-column image is analytic and lies 8,507,360 below the counted phase maximum. The charge is the counted phase maximum after Appendix ZS, 136,433,664, and never the parent's witness figure.

**Preprocessing and advice (inherited, with H7 rescheduled and Appendix ZS applied).** The historical P8-producing signed search is rescheduled by Appendix W to at most **211,431,424 bytes** under H6-D and H6-E and, with Appendix Z's non-resident record, to at most **136,433,664 bytes**; Appendix ZS applies to the remaining preprocessing phases the two scheduling facts Appendix Z established for phase E (kernel state is kernel-side and never enters a process's resident set; the launcher is replaced at exec) and the clause-by-clause tail release. The R.6D schedule at 241,028 KiB = 246,812,672 bytes is retained unchanged as history. The Step-1 solve remains the recorded byte-identical sequential computation at 49,228 KiB; the class descriptors, condition tables and pair retain their previous status. The counted H7 execution is the five-partition program of Appendix T at a measured complete envelope of **65,265,200 bytes**, with all process state, mapped runtime images, retained files and startup/I/O reserves charged. The historical 247,400 KiB H7 measurement remains a record in Section 13, while its computation is rescheduled by the universal ownership proof; no replacement probability panel or newly discovered advice is claimed. The other counted development cells remain lower than the online maximum: p8fam 69,496 KiB, fillr2 66,916 KiB, pbal's 32 KiB counters, gmass 133,236 KiB, the class pools 59,104 KiB and smaller instruments. Earlier H7 validation executions used at most 132,505,136 bytes, also below gmass and the online phase. All repeated H7 builds, front-end scans, digest work, failed attempts and checks remain charged to DEV.

The analytical procedure maximum is the rescheduled preprocessing cell, **136,433,664 bytes (phase R)**, which the eight-column online image 127,926,304 lies 8,507,360 below; Appendix ZS gives phase E 89,333,376, phase S 95,485,952 and phase D 106,987,520, so preprocessing still bounds the procedure and the charge is that counted maximum. memory_log2_bytes is **27.02363**, the upward rounding of log2(136433664)=27.0236291570188016337..., and the organizer rounded-field scalar is **83.54782**. Thresholds plus advice remain within 2^13 declared bytes. Appendix U gives the inventory; inherited H7 sources/records and the P8 derivation are preserved.

## 11. Allowances and development

A_C=A_S=DEV=2^60 target compressions are charged in full as declared allowance premises H4a-H4c, not proved historical bounds, covering failed and repeated characteristic/Step-1 searches and all development; preprocessing log2(3*2^60)=61.5849625..., charged 61.58497. Logged support (R.2, W9's 9.216*10^12 operations/CPU-second): P8's 38 runs 2^49.47 and the author's whole effort 2^52.65 target compressions; development below 2^58 (H4c extrapolation below 2^59, Appendix U). The dense-row derivation and failed historical work are unlogged and covered only by the premise. H4b concrete cap: the named Step-1 ledger contains 16 single-thread Kissat runs (seeds 21--25, 31--35 and 41--46), each capped at 12 hours: 691,200 CPU-seconds. At 9.216*10^12 operations/CPU-second and C=2728, this is 2^51.05240 target compressions, 8.94760 bits below 2^60. The recorded seed-41 solve used 21,515.76 user-seconds; named 65, 68 and 215-second follow-ups are also below the cap. H4b remains a declared allowance premise because a complete historical execution log is unavailable. Fallback: 2^70 each (`ledger-allow70`) gives 76.56832. The inherited rationale (written for 2^70) remains in Appendix V section `allowances-11`.

## 12. Finite checks

The current isolated selftest, actual-method controls, registered experiments, real-pair checks and strict packet verification are specified in Appendix U. Finite checks establish their stated domains and do not establish the deep success probability.

## 13. Historical 15-column full-scale evidence

The complete original population census, seven-CV scalar scan record and H7 panel remain byte for byte in Appendix V section `historical-13`. Appendix U supplies the current exact ten-column census, compact witness and the base's 24 full production-table controls.

## 14. Lineage and credits

All 19 material dependencies are declared: the direct base def34145-9628-43ff-a7f9-a93bbcce2e2e first, then the 18 sources it declares. The complete original feature-by-feature lineage and credit text is retained in Appendix V section `credits-14`. The base's source/program hashes are identified in its packet (Appendix U).

## Appendix A. Exact 9-column compact ledger

| Term | Operations or count |
|---|---:|
| Build per epoch | 73804325891 |
| N_CV | 1985730719901168031200 |
| N_E | 1806011569 |
| V_CV | 296418991844310695027883684 |
| V_MAX=N_E*build+V_CV | 296419124850616334451240566 |
| ALLOW=3*2^60*C | 9435509593702435651584 |
| OVER | 775008730887 |
| FIN=6*C+1600+2^24 | 16795184 |
| N=ALLOW+V_MAX+OVER+FIN | 296428560360210811912418221 |

At C=2728, time is 76.4854303456169727730405314062844012983154159165417187600564715761420796424784767420679591662195313606940914225006956271..., charged 76.52419. The charge is the counted phase maximum 136433664: 27.02363 and scalar 83.54782; the ten-column witness measured peak is 160505856, the online image 127926304 and phase R 136433664. The twelve-, thirteen-, fourteen- and fifteen-column identities are controls only, not current procedure phases.

## Appendix D. The development sources of Section 13 (not shipped as experiments; reproduced unchanged from 55328d60 so the full-scale measurements can be audited; they use that filing's lane format and tag-only test)

Built with `gcc -O3 -march=native`; `consts.h` is the output of `gen_h.py`. `fillr2.c` is run once per residue j = 0..7 and its eight outputs S_j[c] are combined as retained(8m + j) = sum over c = m .. m+14 of S_j[c mod 1024].

### `utab.c`: the full-scale epoch build and scan with the scalar front end (Section 13; the r = 663 run used it without operation counters)

> Historical record `AS01` (c), SHA-256 `64f954ea9d42230ab3a1e6de51de828a1f6bb9390ef0c18cb3e8ddb23a542d50`. Complete bytes and original line range are retained in Appendix V.

### `h7.c`: utab.c plus a bucket overflow mark and the rows 17..21 forced-bit events of every claw (Section 13, H7)

> Historical record `AS02` (c), SHA-256 `bfdc45e5f101dcbcbacd6b5dacc1331a7d379cd2dbfc9162f279212e3ede2296`. Complete bytes and original line range are retained in Appendix V.

### `fullbs.py`: the full-W9 check of the bitsliced circuit against the scalar predicate (Sections 3.5, 13)

> Historical record `AS03` (python), SHA-256 `8ff5fe66b2ffc3564a719e028da27b0d96892ec6e034366c3592ffb51ea734e8`. Complete bytes and original line range are retained in Appendix V.

### `fullbs_rm.py`: the same check of the binding register program bs_mask_rm (Sections 3.5, 13)

> Historical record `AS04` (python), SHA-256 `062870179b1b62472c7a78bc000222df9bef1b4b659b2ae219f378cc7a7d167b`. Complete bytes and original line range are retained in Appendix V.

### `fillr2.c`: the retained-entry count over all 8192 r, in 2^26-byte slices (Sections 3.1, 10, 13)

> Historical record `AS05` (c), SHA-256 `92bd2e1d59613cc689a3fb258e3ca249142525a8c8224050115d678c7aa45dca`. Complete bytes and original line range are retained in Appendix V.

### `pbal.c`: the class sizes of P mod 2^13 (Section 3.1, 13)

> Historical record `AS06` (c), SHA-256 `5f4ccf28045d58bc2d7617ab38c206fde8b4d8a0fe5708b9626bcbae02fd8b12`. Complete bytes and original line range are retained in Appendix V.

### `gen_h.py`: writes consts.h from utab38.py (no transcription)

> Historical record `AS07` (python), SHA-256 `a5d864a2b6e68ec7f0c8036d53231f26b9a5b018d90706f20dfb4f99459d5509`. Complete bytes and original line range are retained in Appendix V.

## Appendices P, H and Q. Inherited registered evidence

The complete original text, registrations, per-seed records, source-block commitments and interpretations are losslessly retained in Appendix V section `historical-P-H-Q`. These support H2/H2b/H3 and retain their original limitations; they are not current eight-column runs.

## Appendix R. Historical A0-variant records

The complete R.1 through R.4 record is retained byte for byte as Appendix V section `R1-R4` in Appendix V. Its SHA-256 is 895cca992f66b0f8ea9383851539241fac03253945c6d15a17736c3dcb2cd8ce. R.5, R.6 and R.6D below are retained in readable form; Appendix W supersedes the R.6D phase maximum.

R.2 records the characteristic search (ten cores). Missing for H4a: the dense-part search has no log, no part of the characteristic search was organizer-replayed, and the timings are the author's report. H4a is a complete aggregate bound for all characteristic-development work, reduced from the lineage's 2^78 charge to A_C=2^60. Logged support: the 38 solver runs with 230,183 listed seconds are 2^49.47 target compressions at the 9.216*10^12 operations per CPU-second of Appendix W section 9, and the author's broader development bound below 2^21 core-seconds is 2^52.65; A_C=2^60 exceeds that bound by a factor 2^7.35, the declared margin for unlogged work, the dense-part derivation included.

R.3 retains all development memory receipts and their limitations. R.4 quotes the original P8 preprocessing report: Step-1 279,720 KiB, signed search at most 248,000 KiB, and class descriptors 37,036 KiB. The active P8 bound is the counted phase maximum 136,433,664 bytes (Appendix Z); the R.6D argument below is retained unchanged.

## R.5 and R.6. Historical memory measurements

The full Step-1 remeasurement and explicitly refused signed-search remeasurement remain in Appendix V section `historical-R5-R6`.

## R.6D The signed-search cell as a rescheduling of the computation that found P8

**Claim, under premise H6-D (below).** Rescheduled so that the formula is streamed through a pipe into the solver
and never stored, and the model is decoded afterwards, the historical computation that produced P8 has a peak of at
most 241,028 KiB = 246,812,672 bytes = 2^27.878842. All retained storage is counted: process state, pipe buffers
and files. Its result is unchanged: it is the same deterministic solver run on the same historical formula, so it
returns P8.

Under this schedule the P8 signed-search cell is 246,812,672 bytes; Appendix W reschedules it to at most 211,431,424 bytes, and Appendix Z then charges the recorded tail list once rather than twice, so phase E is at most 136,433,664 and phase R at most 136,433,664; the analytical ten-column online image 127,926,304 lies 1,163,232 below phase E, so the counted phase maximum is phase E and the charged memory is 136,433,664. Because phase E itself sets that bound, any positive understatement of G raises the required memory bound by the same number of bytes; the measured clause-object margin supports H6-E(a0) but is not certified slack in the submitted maximum.
Appendix T reschedules the H7 evidence execution below 64 MiB while preserving its outputs for the same inputs.
Appendix W's schedule is at most 211,431,424 bytes; Appendix Z charges the recorded tail list once rather than twice, leaving phase E 136,433,664 and phase R 136,433,664; the analytical online image 127,926,304 lies 1,163,232 below phase E, so the counted phase maximum is phase E and the charge is 136,433,664: **memory_log2_bytes = 27.02363**, projected scalar **83.743859**. Evidence-only comparisons are excluded from this maximum.

No new run is substituted, and no other characteristic enters the argument.

### 1. The accepted figure is a sum of resident processes

R.4 (1a695f0b §11) gives the accepted figure: "at most 248,000 KB = 2^27.92 over 2 h 20 min (Python 152,868 KB
and Kissat 80,816 to 88,096 KB resident together; stopped after the original 78-minute solve time)". As in the
parent (line 7), the author's KB are read as KiB.

They are resident together because of how the driver is written. `stepk.py` (1a695f0b Appendix B, SHA-256
`59284d8f…`) builds the formula in Python and writes it to a temporary file. It then runs
`subprocess.run(['kissat', '-q', '--seed=%d' % seed, fn], capture_output=True, text=True)`, so the Python process,
still holding the model, buffers Kissat's output. After Kissat exits, Python parses the model and calls
`decode(m, …)`.

### 2. Premise H6-D (declared)

The author's reported per-process bounds for the same-specification-and-seed re-run bound the corresponding phases
of the historical execution that produced P8:
- the Python encoder at 152,868 KiB;
- Kissat at 88,096 KiB.

This rests on the same report as the accepted aggregate 2^27.92 (H6). It is a stronger use of that report, and it
is stated here as a premise rather than inferred. Missing for H6-D: the historical formula, Kissat binary and platform are unavailable, and the premise is not reproduced locally; the figures are the author's report. Its scope is the unrecorded historical P8-producing execution and its rescheduled encoder and solver phases (this appendix and Appendix W). Support: both figures are the author's per-process maxima for a re-run with the same specification and seed; the same report gives the accepted aggregate 2^27.92 (H6) and the original signed-search maximum of at most 248,000 KiB (R.4); a local Kissat 4.0.1 source build reproduces R.6D's recorded decision, propagation and restart counts on control C0 (Appendix W section 8).

### 3. The rescheduled computation

Let F_hist be the historical formula: the bytes the author's encoder emitted for the P8-producing solve.
No copy of F_hist is retained anywhere in the rescheduled computation.

1. **Encoder streaming into the solver.** The author's `stepk.py` construction writes F_hist's header (its clause
   count is known, because the construction holds the clause list) and then its clauses to a pipe. The same Kissat
   4.0.1 binary reads that pipe as its standard input, with the same options (`-q --seed=101`). The encoder exits
   after its last clause. While they overlap: encoder ≤ 152,868 KiB + Kissat ≤ 88,096 KiB (both H6-D) + one pipe
   buffer of 64 KiB = **241,028 KiB**.
2. **Solver alone.** Kissat continues and, at exit, writes its model (the "v" lines for 52,891 variables, at most
   52,891 × 8 + 4,096 bytes ≤ 418 KiB) to a file: ≤ 88,096 + 418 = 88,514 KiB.
3. **Decoder.** It starts only after Kissat exits, so it is never resident with phase 1 or phase 2. It recomputes
   the variable map and decodes the model file into the A/E/W rows: ≤ 18,716 + 418 + 4 (row output) =
   19,138 KiB.
   - The map is independent of the encoder's cover draw. `SD.word` allocates each word's 32 (v, d) pairs in
     a fixed call order, and `SD.add` always allocates its 33 carry pairs before applying any clause. `qm_cnf`
     covers only produce clauses and allocate no identifiers.
   - The decoder (listing below) stubs the covers, builds no clause, streams the model, and rejects an
     incomplete or contradictory assignment.
   - It decodes W0..W37, A3..A25 and E3..E25 (84 rows). These include the coupling-relevant W0..W37 and
     A/E3..15. The intermediate S1/IF/S0/MJ/s1/s0 words are not needed: `joint.py` reads `char.json`, not
     `inter.json`.
   - Measured peak RSS 18,716 KiB, the larger of two measurements. On a known complete assignment it reproduces
     P8's 84 printed rows exactly.

**Why the result is unchanged.** Kissat 4.0.1 is deterministic for a fixed binary, platform, input, arguments and
seed, provided it is not terminated by a signal or a resource limit:
- its pseudo-random generator is seeded only by `--seed`;
- CPU-time calls are used only for reporting;
- mode switches depend on conflict and search-tick counts;
- `getpid` is used only to read its own RSS.

Reading the identical bytes from a pipe instead of a file, and writing its model to a file, change none of these.
Measured: with `--seed=101 --conflicts=100000` on the reconstruction's formula, the file input and the
standard-input input give identical counts (622,491 decisions, 26,949,414 propagations, 4,532 restarts). Phase 2
therefore performs the identical search and returns the identical model, and the held rows remain P8's.

**Historical/superseded envelope, not this filing's peak:** the earlier R.6D schedule bounded max(phase 1, phase 2, phase 3) by 241,028 KiB = 246,812,672 bytes. Appendix W replaces that schedule with the 211,431,424-byte P8RR cell and Appendix Z charges its 18,997,248-byte record once rather than twice, leaving phase E 136,433,664 and phase R 136,433,664. H7 is accounted separately in Appendix T; the declared memory exponent is 27.02363 and is set by counted phase E; the ten-column witness resident peak is a lower participant cross-check, not the bound.

### 4. Precedent and status

R.5 accepted "two sequential processes instead of the author's overlapping one … the same computation with a lower
peak" for Step-1. This filing applies a similar transformation by derivation rather than re-execution, because
F_hist is not recorded: the formula is streamed instead of stored, and the decoder is moved after the solver. Analytical bounds are admissible under the cost model, and the current cell already rests
on the declared premise H6.



### `decode_stream.py`

It imports the author's `sdmodel.py` exactly as listed in 1a695f0b Appendix B (SHA-256 `fac660e9…`), saved beside it.

> Historical record `AS29` (python), SHA-256 `7622dada6b1305f5c740bc470f03c69563b42aaecf916ed38143fad51b2d00eb`. Complete bytes and original line range are retained in Appendix V.

## Appendix S. The development sources of Section 3.7 (own code; not shipped as experiments; reproduced so the window's numbers can be audited)

The participant builds used `gcc -O3 -march=native` (`-fopenmp` for gmass, gbrute, ugen3, msample). `consts_pf.h` and `pfd.c` were generated by `gen_pf.py`, and `uconsts.h` by `gen_consts.py`, both from `utab38.py` without transcription. The recorded ng4 study used four processes, seeds 101..104 and quarter sub-blocks; its 4,096 largest sampled masses formed SEL. The retained records also cover G_SEL, the eleven-sub-block gbrute cross-check, ugen3 seeds 21..44 with h8an analysis, and the H8 evidence at msample seeds 101..104. `ugen.c` records cv[0] and performs no cv[0] split in this filing; its other options are unused.

### `gen_pf.py`

> Historical record `AS30` (python), SHA-256 `9e1c0eae96f9d66ba72f65a956b39bf05b584c136629f7ff86673b8aeadddc18`. Complete bytes and original line range are retained in Appendix V.

### `gen_consts.py`

> Historical record `AS31` (python), SHA-256 `f95538d7074b306e1507e89a1080c706b73b71dfd6e8fc0d3cbaaca54b5968aa`. Complete bytes and original line range are retained in Appendix V.

### `gen_p8d.py`

> Historical record `AS32` (python), SHA-256 `2c46678708fab9d7eb965fbffc50216bb8668c2ed8b714da9b16292db49c9654`. Complete bytes and original line range are retained in Appendix V.

### `ng4.c`

> Historical record `AS33` (c), SHA-256 `f502968ee416ddd3f8e7cca0c7e2f5aa3b8b956a39bd5180c442a2f9dd2d5cbb`. Complete bytes and original line range are retained in Appendix V.

### `gmass.c`

> Historical record `AS34` (c), SHA-256 `61f8a6a625becdcfa14448daa1e109703af0139e51f1b03e596fca8bfd9ec726`. Complete bytes and original line range are retained in Appendix V.

### `gbrute.c`

> Historical record `AS35` (c), SHA-256 `128f7eaf56efed4230bcb4b8e4bbff4e55624b04fe2c5907375889ae7a19c9d1`. Complete bytes and original line range are retained in Appendix V.

### `ugen3.c`

> Historical record `AS36` (c), SHA-256 `3b8b3bdbd07d4229ee7603fd3c1f977485564b2ef6423eb0b1b76b74a70092e9`. Complete bytes and original line range are retained in Appendix V.

### `h8an.py`

> Historical record `AS37` (python), SHA-256 `b6358b71eed3b936ec2a6ff908d22a6fffb858dfdd4fe881bbfd8086f969c3d9`. Complete bytes and original line range are retained in Appendix V.

### `msample.c`

> Historical record `AS38` (c), SHA-256 `fc2dc9768f411fe7bcfd190972665a64665c8a0d0f83ee36e4035dbfbbcb7db2`. Complete bytes and original line range are retained in Appendix V.


## Appendix T. Five-partition H7 execution and selected evidence

### T.1 Scope and exact output preservation

This appendix concerns the H7 instrument, not the online u-table algorithm. The direct base is ecfe5a97-323a-4321-9162-2068ff243fc7. The source development commit is ce326a1f8f75f87a6a903609b39a9723141ef055. Its full package-provenance SHA-256 is 30fdd5aa70812a206bfc6ad884c655365b08e8524cd120ade28d2a9d9d869cd8. Essential source, commands, receipts and a strict replay verifier are included below.

Partition the 15 columns into [0,3), [3,6), [6,9), [9,12), [12,15). For each partition, replay u=ustart+n modulo 2^32 in the original order and retain only its buckets. A bucket's updates depend only on that bucket. It therefore receives the identical ordered subsequence, retains the identical first six words, and marks overflow on the identical seventh visit. The W256 layout and spare overflow bit are unchanged. The largest table allocation is exactly 3*2^19*32 = 41,943,040 bytes.

The build consumes no RNG output. Precomputing the three CVs before the passes preserves the original draws. Each query keeps its original CV/a0/window/head/side/lane identity and is processed in exactly one owning partition, including column-zero straddles and row wrap. It sees the same bucket and calls the same postfilter and row-trace functions. Integer counters add to the same totals; their source bounds are below uint64 wrap. Each logical claw is traced once. Hashing columns in order gives the original canonical table byte stream. Each column/CV event subsequence has its original order, so its separate digest is unchanged.

This argument is universal for the original fixed three-CV H7 computation. The numerical H7 panel in Section 13 is retained unchanged.

### T.2 Measured storage, maximum and limits

The approved five-partition run has cgroup peak 51,298,304 bytes, worker maximum RSS 51,724 KiB, wall 117.651776734 seconds and worker CPU 117.527843 seconds. Its native worker and meter share one fresh cgroup: memory.max=58,720,256, swap.max=0, pids.max=2, one CPU. Exit=0, timeout=false, oom_kill=0 and cleanup_complete=true. The complete conservative envelope adds 7,675,440 bytes for full mapped external runtime images, 4,194,304 for all retained experiment files and 2,097,152 for precharged observer/startup state and late I/O, totaling 65,265,200 bytes. This leaves 1,843,664 bytes below 64 MiB. The native observer is counted.

The scope is little-endian x86_64 Linux with cgroup v2 and the recorded build/runtime. The allocation and bounded working-state structure do not depend on the seed. The compact extraction plus its compiled programs fits within the same 4 MiB retained-file allowance.

| Counted cell | Bytes used in the maximum |
| --- | ---: |
| Charged memory: the counted phase maximum, the preprocessing cell 136,433,664, above the counted phase maximum (the online image 127,926,304) and above the witness's 160,505,856 | 136,433,664 |
| Current eight-column online table, terminal pad and complete code/state allowance | 127,926,304 |
| gmass | 136,433,664 |
| Earlier H7 validation schedule | 132,505,136 |
| p8fam | 71,163,904 |
| fillr2 | 68,521,984 |
| Five-partition H7 complete envelope | 65,265,200 |
| Class sampling pool | 60,522,496 |
| Step-1 recorded sequential solve | 50,409,472 |

The historical H7 execution remains support only; the per-alignment strengthening is newly declared. Appendix Z charges the recorded tail list once rather than twice, so phase E is 136,433,664 and phase R 136,433,664; the ten-column online image 127,926,304 lies 1,163,232 below phase E, which is therefore the counted phase maximum and the charge (27.02363). Time 76.48544 gives scalar 83.743859. These current bindings replace the old online maximum.

### T.3 Repeated work remains inside DEV

Each full five-partition run visits 5*2^32 = 21,474,836,480 words and performs 5*3*2^26 = 1,006,632,960 front-end a0 evaluations. It traces 333,509,526 logical claws once and obtains 4,005 good pairs, with zero scalar-reference mismatches. All five retained full runs, including the earlier 7+7+1 schedules, have identical logical counters, canonical table digest and all 45 column/CV event digests. The table digest is 34f91399f0d8c2d5c9cc499bed3a6f075cb5c6a555fbf1e9758e364751962c72.

All repeated scans, resets, traces, digest work, failed attempts and checks are charged to DEV=2^60. The source record has 171 native invocations, five full runs and 166 smaller invocations. Conservatively give each smaller invocation four passes of 2^24 words and four passes of three CVs of 2^16 a0. At most 80 buckets with six lanes are visited per a0. Even charging every possible smaller-run lane as a trace, the combined visit count is below 2^37, front-end count below 2^33 and trace/event count below 2^36. Straight-line bounds of 2^12 word operations per visited word, 2^16 per front-end a0 excluding its trace calls, and 2^20 per trace/event (including the 22-step trace, postfilters and streamed SHA-256 digest) exceed the explicit loops and standard 64-round digest computation. Table/file hashing and fixed initialization are smaller. Dividing by C=2,728 puts the concrete subtotal below 2^46 target compressions. Reserving 2^48 for this development line also covers the preparation, compilation, failed smoke tests and packaging checks.

### T.4 Selected evidence and verification

The full development packet contained 976 provenance-covered files and 171 mandatory native receipts. This candidate includes a deliberate 38-run subset: all 27 final bounded controls, the six-run initial LSan attempt including its failure, and all five complete production runs. Selected records, original source hashes and provenance commitments are retained and hashed.

The compact verifier requires this exact run inventory and every command/stdout/stderr/resource/memory-stat companion. The sole missing command is the documented initial LSan failure. The provenance file hashes every framed artifact and binds claim.json.

H7PACKET below contains the complete H7 file tree in bounded XZ/base85 form, with decoded size and SHA-256 commitments. The readable Appendix U verifier contains its decoder and the checks of the 38 complete record sets, sources and current-resource bindings.

No P8 solve, online construction, success claim or probability premise is replaced.

### T.5 Framed evidence artifacts

<!-- H7PACKET -->
```json
{"data":"{Wp48S^xk9=GL@E0stWa5&!@IBe;hw;f)`qh5!IPh|GP_hGXe5_u=G44Ig7|^7s0vrOQZWi+GMCY9=>`Yv3A9Z^oG?$r@|!f2sI=k#~$DF%uWH?aU6IqKb~guSCHRfiM9;J0njIP4uLRcsAV2V?|Y!B|!iLz^4CtnE~M(u3`UsC?z*6;S2dxMfMuE-9WP|dkjB8hjzYHvqS<9w5;ysZt(#Xm%L%pm_)+!@r|yJChI_3e?y`N<Vw}Yy3(%J%CeMZ&9qS<F3PW2gCfp`X8^slM_zje`qMd^c9@}zrP<Ke*4op$!6)8X0H1ng)|qt4p{PK`#5p6@q{7a)H;uWLpyl?rs}>n+X*JnYAb8-;^TE`8&tm`t@a41BLywF&tSGs?udrJef~UO=z@3gFD#){xqWc9X2*^ER#tlEJAYWie^S6C>P?h|6El*Wbp5agvN8UxwDyi$GQ3L+8c?*Em>|ml2Ri+4z-w2Ns9;}ZI)Ow}eu+=DrIH)f@T@$kmzn5mPh$`!)xfTM9giNcpL4BfBf+B7GX4%A7d?EIVyb<vL^5tpQvk(3np}yo#E@Izg*J5y;LkeZLuU(q`*h|yA;>chcdFIcvye!z`vvkS^Y~mMlLi(nlP(mxfA2**(uZ2cuTQrD7&ma&rOEEcV%E^-RqQ;zo*PoQ~-T<))n;Qxa;6m1as$xNQUX6VqKB9UZS)|+#Zy3eu_4|r^{@(K)O#J(;9gCZ?*5lKOxusZlLTnmEK>hPIdlP4(exb7@3{YSA+{*aoPuFYr)hJt7>ca`Oh&s|ipiFzd>el`qj@ZZda-#F&-Uqg_u9S8c3_T^i4<(D%Cn)AqKe(mfSqvH7V;jS9NCzYdx=^yMco7)iYMa(BI1pFeXHX78p)F$-TlJcdb2T=W1`@rCQd2ukruSt+uvCgVHU5|Q<TS5t<M8yRky(?iCp7oynrDY_DZn}rH-+a^W?qs-L{a8tM=1;QfM@SYdmn`0iFy++_zkK}k&fcsXogmME{UHF3jj-oy{^kjR@|5GsT&%^w7MIOw9PpFD~+HiQJkF?5u+93GaR(a>n1-<zJfj_OXD)bSDsa0l<H|XY4iRcc(3-nJ9`EWq27(l70Sn~XU`k@AAuVkY6Uw6(aLOWAF>hnc2Wu!za(A|lMyd$Hrut13I1-l7{g=qN?NQ@R;la&CCtLt2xjIVPEB==CPVnlmYffJ){+XkNC3w(rH^26UA<Cuv&oiL*D%b7-V#7OuQ$-EjmC1KO7w3Oj-suCWiUp$3q72Wy)j(6zGtGS^R{+~2!(vUn6Ot<5sH~N7>((TiEMUD=!lthUpHjy0sSMqSF-wjIXjhgSm!w60kC>ZB?7FP31Nh20ryYq!gxBvjB?ID|E?@XOuG=4?Ah^%in=!atGyP2$hL!CA>5kKeTvlTqDtTSA%o)J0T?H>&y3<nk%y?Y&{^p0t1yrvq9SM{v81i4;G?JU#)(Frt%Y2c?!eMkzP+mEa8Oh{F)6DG(ZhytnY?e)o6xQ}2MUw!i@@lGE(Na#VG3b%WW4eUoR{70(@O?}dKQlWSEhk_X@{{c(gjoMQrpSGCLD2bS+pXpYEB8$Id$8}_jUY!g7PfxCR5InA1$P7=Wi9k_pv5KzT<O>HS9XNNQr^`n4)|x3t}n%v+zZQcc7}J$fCv>rmI5wEZ{%YXe1G;<t?>Lpv;Ut^XvtH>Yt%r#El>LDc7s1!2VAkAM<4)tZ_Q%39a=Qkip32ma_>w)Y{<{L#BSgzSNma4aXm1%5_C~8*I&IBC}2uyrkhRZ?;$%#BT&rwGhk-nPxYNp2&PHL{UFQkB@&^3d2QDSxh~3`zgmwRMy}ArF5AZ_|s(0IBR$^Nu$6}-uZ4gpGKy%e&aJ!a|8IVqVKcvWxX+w@C&9=qWY7K<phGDaEEM9`g@yT&Bkp-J>x_UBatfyi4~wAJ=rf&nM;)B@8Ec0=ofW<{|1Dt>tSd3x0}nB2I07t@+cLO03*Kxxm6y?+S6Xk0e(<(`r1i(ttbePs;<=#w7-C}C`Uu&RhTZJO|Kw@&*QPDL+HBIZ|1W#S0DAENf4U;bE~r6gzU=T<vPRe6l~_)*i;kJm(x#=I`l)AG3B(;kgjWNzD0mU!sTW<8^7ajE{P$B(;OMs<FZH!o(!|9GWL;<VYhz9@}U?&gJF7{C_nv=F!e2d(|`u+R-n}hI-G6uF8-2GgN|2WYzdqnNZgwKvP*BJlk`y<UP%{x#4^rN$?P5i@8v|hQol?b=gK?v{i@o|Bp>#>rRck7@g|>f#)T~Xy1d)C|6(95qvUQoumx`$*Y~WVu0Vx|)<KCDXtzG%`*oj7|Hw51%P9?q9GUH1Vl#|*#m6(%b-7{6P2G!;8l`Ee$QJtC0+gkf^UOJ2A8kFHp|m0kEU0piijAZqSLjWG8vIh+y_J4I$pv#9t`^Qm92kGARa3S|gaHDf++w9GFK;Zvd1sEQ2nGrxeh$CzBBN@oDUhw8oJZ5L0YH-o1%H_HlhO7}^&#E?D1je+UO2T<-qk8gw4nV3ck#flVFwhYgc9$;%@3PdzrTm=SUjiAbv@3z@G$THDLEV=j~W)pP$&2?#3NnYf`2HX@*97>q|=Y_BMkOGnpJ&+bDq*aABz~&qh$4XM9fBq4CDQ$)<lJxd)1FGa6}SAGo)eGC+&LPnYO`d9`J7+#`2?aI@|Vd^aa8Y`8Buz(VtWke7%{v{)}VR>dQv0MQBWl?u!A{d^jd5+U}2Ul_R#J_~hIkv)N?_-2d1TkA;gs`V_=4ATG&fh#)_|zyzHbQ0SP`)7?aMBN~?>>A)U%m{KwI2!A6{D-DiWz|{u2nzA}B1IAxJ<ai0D9gaKsr$?bi5lHz=e`&$TuTiSUP&&TTg`nsS{(ya_qjF)4FlGN#_EjuO@IEY9>lkgicQ9=@G4o!%s|3#Sc2TmY5C6YDDtFLVllJ<(8CxPEg3fkF9c}i$=P0a#e0k^}UXt`6ubA8U6Ah@d7L2Pxoy}HdNy5breZZeZp$wVDH2hp&T;MFoaEqfX)~`^kQO8Tx%HbTC`FGtIZYx1)&u4Ya(H0X4&)jWaV#ub-gp=nw=EIsljqn7CN&VfMQF`$kqTiZ#DK0vlM|mF0uM%r<$U!9$;JvXJm+8_kj!02-QKaPldqkm6weQ)7Lnv%M31YR{!R5P!K2k5bc-Oy>T3baf6ttN7YghCEI|x!Us|s3;-5%0_W$s#r?o0!vI8BhulxD5}DFe0q&J_z0GM<oObBA9@hwzwUTMiT0REq1Lg+1wi4OxRp@C8W5Nw$9n&1~oqI(=I;{ZB~(6JE`F0XZR5kNNBn^3IA$i@pvA6r8FUkG61iDrK{{j{aM-D9~KnRa#-KF(WjD$4&%*_D-m#K$qVuL`(-n1Z2$5Aw9#ZxU)Lapl*H%7I|$QK_8loqnuewv^LkB<}YrnCAm~Dt@h~*g3)AKHzuplPuVLyU9J*Dff3iDhme8v@~!Vsk*}_Xhd<b5e@{?|`y|Kbn`!T<-Xi+<YniFNC3@b4>o`V@ttl`oBS<9;VY@dz$f5WE%DAG7|ASAvFU*<J#t9u1rdP5P#Ayo4RwPFt)-V49{G-H%Fsx<l#usUD5S_{|629>YyS+iT&-HTKqswQ@-VIL=dvky7yVRdL*223UH6u~2Tm7o_)`Daj2~Xv))if)W;Wmc3d%Lvmd7}5b;*Ex_iWjC%Q!Q~k?fB9H-mjM+z~G2hwsb|2#g#)H>b8Y<s2#QTo-{hKJq?>Pg|S$WRc+0n<}{FIi~E2?F2!}r-mPMvC;n=lFlf%q5TWU5t;sQj(B?j-1fBv@R1)4+%sWNO%I>n-$&;!1Z$6A4!zd_i6ZMj5xGmL9N*(@B-7>r=Iqxfx{JH@_YzGD1*WZLbWJMG(348UU-SVQ1X~=)T$&$ulOJd_%Z_ZfpP#etl1Y~9g9YyV4F_)Wfu)mxlc3y%Vj1>~l>bnf^Fb*^`@MTyznNG4|_57$GUJ^~_N+snKv#Knmq3u@R5(2N#XkGtU?$1Ql1XKziV||YoJj`ol?_Gb4-wV2u=lrX@U4Jq4RoJPhAC%v}pRu8L50$#Y*LQBHW=zTw1i+M{Wj5lVdO^z&mi(zguqEio>!tTo1mQi9o@RLD>Bg^Lac?lv{bDvidV<TLYVUA{(Bvn)kR<%HA=@NlvtxuNzI9YL&G(+g#OHMGTpK+d5m<`v2`u@_`ue8qo#K?g^?B~r2yy@c-_6n^TnbOFe40Z_=NLuJGBGtlHR?BqMKGxK!|DTUKGKU4`Tk`1W(bINW_G@*t)TBm=gz0H=V#iYO-LDmW<3ZNE)Q5Pd+SPvU}z`Sor|$AM+wotszu?XG~SZWHeu=bC`=>*u^o;vAN&sQcCpvj@mhf<EwnvgW0E1yp<IBR-DlkhHIe06gyFAJSmxda%Z?Y5W%|GWfNxAgMG<1VP;!sHaD`)*;f`u%ZPpg?sc>rFMq4@c!Ra8;&KJ5>t3Q1JLlbK8e613Dh1P?|EkjhpnW$!m>l`Yz!Ih~gnP_s?*hd4*X=FtE&QR88ti(q#<92Xg?VBEv<1Gc3W7|SFV?>qB-8Ifp%u!l7mJO{;iTV==U*)p+*|z!t$i`fqwTE$&g$q%#5uRxWl)S2@f*w<eQ0g>aKP5OG%d&~btb78{YfHh>rfiUb8_xn2y@TnnzGeaq=7&7cHZUX5i}cJKDzM&%ckk_#&$^1=YW5VHVa-@bILaDOPnVD|#;Kpz?>~wD%cVw*Y>l(a68c%!t*SH-kJyAtmvKGH{7C(q|J0HWfKRKX8x{QPLNoJGnTu=-Tg=Ig(Y~v|$ljUY9|exqe3&ZW@Bjmmt=~wRvRs$>Aenw^XzW8<3i<kRzyY2zZamf4O0AZNK1%g&EATm9I}e!8!(=#r8O4OE!I^NWdd8Knhh_H7l-7#h3@xtN|GsudO=0KwH)oRropMDbk)j2*F_f+U#XOV)iSyHj6WO`XH}{CyfK4bcnW0Gncn6S>Eh(X#$y9kt_i^3+@k~-fwTU9Biy)>bc!gIT^~z$7eV`y6JzzUVw9Lk$6zc!InGtRFd`!|}=z+`P)matr>EV$2;_z$(!u6QniFgj^T*Nm)k%4Mn^MHuv%AJ6vWFB?znKJPm>rb#|9N2!5uC_ser8shRDZ#S-Y6UptEy<CtlMfgR!*V&L3GxCG1L$0r2)3@vmNx6DDsD+?HT%J%LjBszNIRMV-dm<_@nhAYc@+b!H16DE@?915v9(~`xL%T9Ny(?TN)5|^FPcJdXq&h$8XOQAK-b)*3NO^AmP#eCRN*Ji5No|aQxj#sI}T0187BWzzVlRJfo>36k^CLr*HcAeOu2APrKMd{^IyCPN{6EsW!dT?cnVo~-lxP0Y*`+7b*8+L@QGBi7$ugqdl<)A294??tkbbVi!+oCU<Vssz(pHj&CPZHCh8>l=~=aKn@vKre*V|M&!sgjikdn}BU`o0+*X>t@w89T@_xi6r@j_N{U`M}h!_iypdlZ{yLo<)!fB98#hSzb6U2n_@1-*tr%9T=vKb}3ss7x}xggo*`ISeEJmB*=&3YQ+XSSM+ui-wF8s{K_(`<)DCtQfae=WBLa!Rn3!DrpqbvGkM2iL?Sd@e(FRAuPTX(52WR5^Q9=}z<m@|`c47+QRb9O3noD=1Q!+AZ&}pz=#VDn#VHNlDa1rwki8(3s$}muwR{2R)$=So8h0D(dI0%A<d*xjtTFfjWA9(z5yoas*>Btwj&H0o$FPSC2!CnR|nGkv~=$3#tY^fO8Q3vQ*B_m8=+6k8>PRa5NuX!Z>`uURq$kmlaMANg#MpUk2M3C{o06m7oR-mO7%!`Bl{#D$iXEGN57|x5s7K2HP3wGzEu1Gd86|<h95;hvPEMlcw?!$n8ufaW$@_l4>$|BP?^Sy7?b%HbT&Nq_^0(x!~#jE^uHyedMtvYDT<H4i!KH_C=v>KH88FsO^dY2w`NB;%5p8lfLaX$w;+$k3>pr01X9K27x5G-HpT(_&4%hhphzqq#Y^W8=I#Wz<56uEXM`1UkSErYMJjh#x1^0^a^FCT9ehuz2c=h;AU@q%yI+OeHW!4z~R7H`OUiQ<|e)-jg$`E!$!I_t{)#zN537#ifNx&9(vxvej@d1N}H!h>(;e!={1QoR~fE#Ibx5nCfuMjF8OPC&ECCf=ynL4Lopz0{Ka}+(V1Q#W}A+k0V)m{#OEl#?Z9hBQ19BOt_<J%mggZrxX7zI9;jTYxzY3y@UN;ekS~h?khBP#%?s9ue#yDX%E<;(0lM`3nQXV$n_Kf;YN65>*DR{0R2V?a!^qzBM5cm(YIxUz7495d>T?!fNn!$QwRh-~Qg88PBzvVS{U;B1uB`uPn}rnY2ht1H<r@T0BYHK_0+rBD7C5OTG0WyZ(_BSkY1Bd=Ux<``IX_cr7chQUR$0ixlmUmj6uHM)Wht7>{c)L%RJjxjTusZfiym7u0Yl$O-yp3s@ah_scK){XbA#2?v(=+MiXnM;+Y3r-?$VGAl6HNEVK$uVSXI2vcV-h{s;t3CN5Ux5xFC{UG5-%{CQyQ5@enL3kWh!SqTrT6_Zg(tH=9;H03{{0NIV}A&AC_bv9&h^f4{oTvoZ~}f1m8AEojYcP>uJ&E7xAMf#^WnDyX<6(E9ff`lKW|b927R(k6{`&!_U~eHMr64|R0sRa~vhkwW29=nkNsX(nkdahKLep*F7#8=oY@OMzxB2Wm~oP`O=K(_ElgRZXpf7k#Ugy7PmOu}g=spjZFwCm3n82KvmrAaM}mhl^%@q)~q9Q`QBv8^Kw3OIeO}iu^CK8b@P7xJa3X0%f$blzkBLEi*EsIX?Ar8&n7`bF=0BW<ctimILh;0P@-hJ3lwpqLgvIB4v<EJfBehy0-~_lys2%Fz`iNe#~&?-9BL9DI)>9n>b)s0eZrB5{waRyY4N&6OzFpgoW@L^r5vhjpiKUEqH9q3Jpf6$cBTZ0-?E3C9C??=d(#G>pD!g(L8$z1|sF-Du)&d%Nel5LR(vLVivmf(&)(EBo5DpD?D&^`FX1QI13o<)_H=qG+$1G>}UceMFp|KLgJajIZ&2D=(lYS)qwKj7g}^eof%50*-UB(<}>?{!c-R@(sYdUzf)sC!Yw>CTofA_`jpxKpEd|uFgWwZcq3@=U#YZh5}=sqia{t?7Lx92AfGm07h482GiWjkD)I&BU~5@yE$0^X(gdOAX~d)h<%gMQ4;!aX6Os4Sp*`h74Ka)hLK<LiWB@s-={*K))mh!l6j#GXbzj-53*4F)i--TRsc(HK?E?xwRQrK1dGKmS*>>R}GtA^O)0giqdAn0@X*nb{D+6sWG?T}y2giaAIlAh1X2}f<`(vg+<k#TVb&Y-g?#Bs<2JuNRhnIN1b!0L2&)&#Iq-L0vpfZEqtUu;OgPH*jGo(wpvuIt_#e+rQzt*mc6MV^Ha=hJGKMMoO1&p>|dZU+u8le~V%ZRr?W8JSbXf={B6;}H25b#(w0xxk@UQW)^XWjfLZRt8PAZ9hYDLSH+bm6mR=&co#M+2prYz`QF-rt8njyWXPCjc&zZ^&E`s%IkJ^cax)NUz{`DWG-hZJdeBB%}ixm#}AqE8hOTCga{W5VPULVq!yC(y42@{W;Ee249HbC=+AtRoOYj>aNxU{>voxcjMC~(6W-j745$m9p*q+IeJV6FpS@9pn2-+al-_hX3wa44yfnUoM<EaC!@nJ>dwJS_d`7hHvKS(19G%^iNGI#5yo9^{6%H>OH&=rm_suXYMxdD$%HgCF4g(FCjN`JOtZOcA?2={1sIAPDGYk0n7YW?bc-<VrNVuy=I3{iiuI_b>$R*zC{?VNnL-E!yFl>LTbw5w5=r{PEf@cHlCe3S^k0z1h5@>NO<L3eCrycK&2>b!XRxu^{4>48GQGpKux%Q$uUt#?>ZJ4&yV2gvb{+C(K1a~a<xo)u%ml8pVo;Z;Y1x)=?P6rmv${K8+;Jg*HV#3OTr44BtOO>_oOi9)!vS`cOKU$8uQdt6)MKz3YWmXi>G7v6%PY<xRc}|0wb&s|xw-kp^4=K7i<3d#IMCfmWs3SCyDahSA@>t6%CgatVsapQJ-Vc}W1nJGfV8^JX^*=Fg0i@ocFjBEN-~TsOlHxR>l(Jb^uk`63|8^u1=XLo;`sm_!l#+?WpxPMMUu-wTes{jL9=#uX<?H+DJmMP!`~`4D4grvaCS-L;H9@mEsyphU{`*yqP72vsr_376fJc=q)E*lMX&IX%*zFBUAC@YjKZ&qLxt->#^hhhUSr(N16*WptC0FB{zA|7>xSripV3u5_cHPr66wJ(uJqVd=9U)kbw+yoSYfH-++@{FA~80Y6GCU)qEVl3p@YUHq#YIts-Iwm+Y+<b1ZHobT(jLJkKs+sGLod$l7~sI13&J`vP7AZ){{IFoC*}-LPrTa80|7G13kw-Y{uUmzXMb;@@FA&-AU*tU=&HR!5|ky!xElWd)KNA+fSK)nAsy144Y{<4UJUN(^qRtCu3>0vvK)vZAIS=E<|dI)?u4{{{T%&-zgI7#Ip7k<0s&Kw$9by*JaKzjUEe9liQ%?HQ)!Ah~iWHj<bJ}-ftgcD-F8Dqt!mh-HNmpQwAMEOv>v=pGf1zlc?s^r{y}D)enFvN|>M5*C5;NLF!|*w_29TSt;)&@RNaaVNQhB++8bRc)vU>;n{ROmeFmMAoev%S@o<m$zjU`J4Dy^|HRFwS2*wuEFsAh9^ve{A5oP`z}{4SA0BD(v|QL$Q&dSq=B|>>m)C#l!?Igyv=I5oA(r!8PS`Y8Dt3dRn9EURyg}sEXrKx}bH^pimngyE&Ii9#eqnDs*mRzVel2%$q<!O{mK17|ybHcEb22ZlD9=&`Q74OgTrFa}Ig7-(oQS9u;tZ(dh|NpI&cWPY+=9Gg{%rIN?lbOn8b0Q7<L@W>qA(30f<EZE7WYHaA;)hl-b{147O?EXJ-MSS(mL@om0eSU2(pk--H5)^-n=MdZGAl_Qa*Ldry#qHZSys9uEr8#v*fQBM^-8*T3>jCE@lrdf`@nV;PdHG<cUiR`&g12s0<{I6ufil>PLw-O-#MfIvpOdZh?2<_9(}tfKlHOawXqNUnJ_w<tccp-R|9--r`eTgE(rkYBchOwQ5&68{&tL-gk?^_@bFWN#gTBAt2D_y>9-RfSshOqBzIa@#8)b3L;8<j%xMeC@G?%EUwSAxWNrv;(s|E-d45Dww#M$>?DQ%UsWPNZY%v&x8q4rYaE(4CW{T^aez^pb7$_UhhAM-`k^#R^uSZ8Z*fi3+%`cV>;SL_mxD@%P%f|Ru$E4UrB^Z=P^<RFuzv^oJ1Im{<3M`e*-a93cQEHN-m5_SImEJ%wm-<{rPT*)v!5N11=4L7DQ;^w+=612mI4ItD`g#X>8qE@+>%dp5OWgexYPpv9hR9%=!Kx$eqxZC4<pSPVwwH`JM3=Si2Yf<K<!28{w**`jIUZcu$27CNaKIvK~@Qd#X0;^hqW(a`hJVnEVK15+-4=xcF?n<(57}MA@3t{6AZ&t`sUq#LgmO_!){ohKPK1plqj<^9C<E;Ul4b_F|_=K?W@&_h-I{{_|cEHR#m_83a7;K^elYe@uE2D<+Cs8RO&3%OcI$zC5p5UwJw?e8)_xsg;;wB6YNFMj?v6|D>(qf;rCC%p=>x0MHdTJ6o-~(-5#CSbKeqqjERT2bKo%F=?h_VXHo-_ytBLlI}wJz@3Hd9C$1N1_8$=_<}f);fP(FhwityD&0Is{uim%q?F^GVvOp|(p+O)1OxUR64BC@D(e~{ZGn{?sccE6JE?M0Z@PB(O)#7B}Y-O3#{o&7e^>+p!i6*Mor+I<`N!(53MyMxE;tQln@<N33h!|5{^c4KebzQE%x8a@VY?BHKz9=o$)q1sT(j_$JE38X9SgtWh7EmD@`Y8xnt{subxA~UqISp?u-%YfZgh*t#5E>?Gtm`jFh%m8MA{RYTjY4xfL#*xR+A;zMPDNPwscFI7X!<!e-zrveJdtExx<-e~8$C-PRv~fVsfF-Rj^e~VwK>&_gHEeE!M7$;U!#^gXDy)-hXzV_iuM?X57#b(?ZeNL79@#?P5G}6l|L=kn0BI8YH7SWx0*$eMD<*4*l~l1vF8C<4|uxK`MUuuIz-RAFb=>OTYVKdU4iK+u-BdKiZW%^AEEIx<YAjpF0wF1%`o81hKMDsfq^tyR^Fo05B*&!iwd?YirH&@@+kV&dMRp(JtCTRbYF{auW8-Afa&MSpjL7@-|~Zc!zR0w8-^pSagxdBvUd4hug}f09yoP*7IslgfYdyfthI<u9m{zh440YlaoR8nDPQQe*eOw<PUM*ef`a_De3sk309o@x@qim|taW1%Aw1m}nUaieJMtD~ch>zZ<IV*hkTrkZ%G(1H)8+2Xm9$2hc9P8`Y)G3_(Iwu*i2qwY9doRvM}rw&F0nc|JpCn`XlWseCbEe&rL(6s!g;eZm(BCCqX#3zt%T-jDPLl}fTwDRY`eDrueOs9aGNTHBkVbW2>PlN<62rWj3t|QJ>&;v%OR5=PiVZosIJapdd+yDFD`qQBTujjP;SWt2b&lJVSBQ+VCCO83Y_?O@Z}VpC?46`23iAKuiTO}f7&l`=l7hpNyVSPeBu{Rab*5$ZKs3HFMo70?SI^^psr1kXGd)~qg6ZGyaD|bGz^RZ@HJyg`iFD(`ojAejBG0}h5IMZ<3NrnSSAr5XIC7Z=>|%4r-&$L`0gCy?QA<v9D;uW?<<KIo@|AgU=M1^#y%22n1bZuaR!O2?V7++^m&zttJ7FfxU!cWD{=120U77+J*IqHpiujOA_XciK^cEro=J#HeBEUgIWP5F(Tw|w48C&S-PV;6p`$|&N!TSg$dK>dXZv^`8==9va#o!z(?$6~c+gSf8p7HZ0Ikxr&vcM&k>nAFA4*89eg+IkE~O-mk5|;B7Yuh#J?CR#E;9j8eChJq0O|!d1O#~O#HHH6w4Ete=i)rY&M_bUE3|W>QJGTObswjuL0}Qf2qE@K8EDH3g-F_NvYAW-q|`x`ho9Y*+kgWt6=Pk7)FMd}Y-z&RFUijLx_x@pbLr#Wr`b>V3_TEokjV`Si-o^)m(wvgPuE44_Dbrtng;;czHq81710C2sHX=$(9$<`x0#$kdz<;8F8IYfb9ig>G$#ihooob=W=kJ{3SI(chd04#EbI{s>7<u?tU%6y=6~K=*E7lPXA$2@!yA3tbX7Me9{i|~q&JDVx(^9Fx`vNrrrb5y>QU$NQkh2l+9K%}##y~Roq|gnd73--6gM7abo->aRM$U5L+!WzR9gu1UFi3Jb~P$3e`TaKkm08C<s|%tc5gb_ePJ`WB_2+zXgA4PItXh|+`89vk^ZM&%hg9dM~@+|7V>)I9jlc-JMWbh9p>nRK3=Zxr#3%lR@fq3Xdpz%a+wQ~v^5Gv-&&FE8W3qHG*lNRQntdN>$A63NjCyAe1l%<nr+s+H<US3J&<<hulzOt(r!4pu!Yme8aF1IlLo-ZA>Yf^LJ(Vrj7_IU9SRu#Z2_h_1MhtkwIGtn2Ci1+Tlsa^w$7Zr_||dFNLA<}q*2;^0)q%3sp2e+whu<$oM#pVnL8YmTk^P%ogEV=rAZ{{-FITJ$qQEd(u^BMAIQY+O3gPtjyJ5K29X2Vs=5yG_v<<b9v2&_^BL5{zIRsGPv{gEarar}ux<jEdWfUQ;_x*lR(Au^1)9i7Ty!cgWAWd=fuoD`_rScCg%8Ic_7(?49r()Dbz)lP<c&}NO|fl?9v2@0)@j!MA(dvSInwW{X{5-sgU1n@$>zT<kxwJNZl%gjW*{`N5p4i?ivW0hf3!vdQG3^JbBD5=E54xk_~iIK#sHEGL2+1-R(b6kP}bRvHNDO+*2Q*@REHQy{-{aZKskU6^~{|+_7#I4R8Uq)YwX^_XGkB<#;sQhueps=ej=?rQy2dFSR8|xBq$1|n*JSSL)R#id03!CIJKzPXE4dlqaCz#yZN)`fT{&95};bj`GoSS={Y;;ujS4c3xA-7`sP1^{&eV9@X&ba7fBGDKwy4!ef1htZ_CaU{B!@C%6V$nUW*8n0%H(@2cG|!B!3KLWF|@UFXGf&FL%k1wPTd=XglS>zUjyW6Wu$ku$jE6@9vC}L1ICoWC4SWAksvX4X^R^3nzYGm27Nk13ewn{DfP_bN#Kxu+RA_%WO;)Oe$u-<CZjybf7*0W02x!YwopoE0gx8l63i$o5@w|x{Zm@l80#|=%^-ucGX2Dq6bVSl1IFn1%9hh#PAVN38N)>uJTKkM%FqG1!O)(jX$XXB0ad*|Czsdf~_?PSE9`$d{DPq7Ub345+U+X#sB1dUh>{QLG#a)0fU|Z=OnVlHN*?%0y}Tn<vXL+mjijp(2b*H!M5H(dX(h%dMb(*VGMR*eFzE6qE2%L)k@4y=g_t}Ce(*XrU*xWflP8Gim*Z3x3M$MfAof@>bFRMt2@fOcZV=|-8bk?p!iZkk<aJVv%Y?R(G2rl8x12HtZme?s`4c>3VuF^iK4qLq4XJ|rt8VY%uAl^e3~SyUz>afN|o8RO3Hgt^_B2B)d|_MqrQ9nkCz1WS;I;gb5Q8JkxP977T&90soJ4Mn(t%sW|8g*$m*hpERukE2O$DX<}ut?N^BH%ei6RuK$P48BeILXvB9f_F17n`CSj5VFm=x85aTBL=ddrX=kf-fF8m0505R(*3w{b6LI~Iw5>KhNCK9;mA+n}$FDA>gg>k!)qPIyq)_J^%0T3VTp{@~d>__J9m+|}(W_Lc@2iC!b8Z1C#?J}gmhp7e`o5=@LyxGL77hAr=+Pe9wbBv@-i^;*`erX?;ZCW~MkV6>5omK1y55!!#!j~r*^|*iyQ35$6S7H$l#5PL<CO18wUTE8qPQ&#S*1VY8)%lL*2f&G&7iv^lbNm(EIt=i~!Q@1+LAyG5)rF{HUqG#Rkm_>NiMbpn90?JGU8Z^Ae+VNm!=2i31Cvo)<WZC3)Zs>TTeBo6E`QH-dkFAADT!f;W2%KEe6as5!3L8TmTCr1pRj<a#+81zR354v2~w0vrtx%F$+2?vLwCJ++kqETt<<rpX|=d&qO%h|A(n4_PKlr20RLddO7gCJyToNbOw`^Uvd_<Ue2P;*s3?A9&>7?!8V~zHC9rCkc{HxmeMzD2o;Tdn@-bTxkK}sCBDqWteuam=mo1@DL<~+ox=-dt-*nk8&!w%9kYu-?Cca$m6S>M<`AQ|^ts%$omdJg6f-s&|n-*W7Nc(*GrB5i*EW4UN<^or=w@-xM?o*f7e?LA4+z^lH%9%@>+;UEB>C4oCxc1JJlUU1CbmsM9Nft`6)OM$S?OHegyqe9LS?r`klAAS#jKY=fO|g!Hwy%Xw7bHssyJ694iy$nv<JYJ?Gb(I(k^vFi-N13D9)Ok&NCw#kvg|d}=F&~7xigguj<p+Yjmu>GC5*0!av^a=C4g4Ut)bTmEpo0Wafae2mf8P&F7bW|E=~_BqN=p^lt<?E!q%ITm1eP#RbxKP;ScYKCsshCGM#tR1JF}%lNdaF=}9I*ElmCwOHAnby%jL;D|S^)Wn(taL9&#3FYqyh+|9xAXC7;&;R{Fpw2S9wWn*aBa6q@n=A0-wcwAfgU*;Kp-=E{{tqecFB+H&vZ@v+521`<h!#J`~7YG>&3??rW!s6pU!cYnRBM`EYI0V#c>66}^pP6aq@nk;xlu0wDmiRQ5|1KWE6525dM!|TxAO98l*je%D=q`K~6>^zzzbCZ0TZ}?RYUgN0{|(3x8KxwmK+rmc9Nx6-p%c*{cN|>%6OGE0?T$HWZIGZ5d%=OaJ!-9Lk8@Lz;tH)LgD(LH$_TMkzLC$Mcz+CiZ{3E_09fVw_8v=QUAd?-`nKsxZ_xYo9TzR`kg~@nZCk}dv2Tt3>)^TH>AE#v#Xhy-7t(m;bG?o2y%ayAj9OUYAWvxBOxVA%XF(yJ>bfI7B&0WjAAQc>tZTjRS|$Iw-CZ#Ibd4rr+QuO>V$K@cQW(6BNu@ifCDLmaU($dIWOVi-!s^JVf3z7Z1MryaBio<DzR*{s8!h;nwli7oZ1r>mgVf7D^gEQinb%~f+cSXJjCP$VwD;li5Nw<kc2%H~*C|7k-4nwSH{>vrUz7z`bLRoicUiI@^~BD@`so4iMS8ZuSF845GDvgX6#$!|g8G2dGZO09>QE)1gcT{FYZF@l_llsrFBV>#C`A4Hqh%6BfiuZ%=#iwY6W~2snbw*KKK3BKA1gb^(P%!eY{ihb=dkF*h{Irnl#XARW@K2@?jTMD<nWtR1-`{aP(I=I(Nv%uBTw-y_3Wd-g~^?F*Z1HyoGY?L-&bBSCd4ehVS**@y);2Qk!N92r~;q+!h4zwY;8CM%y?MiAFuW_+I>BYOEj3I0L&rbxPejA3eLNAmLzbmUpA~K!gM6O<`&7E`tSMiGpnJ>#_w4AP-wnOotGduC{4+T$DW`CDu2j$hKc3gKq?lXGp5g~rRp|r`=GrH#v)kyJbi<QqnW$bOg(DEr;Zn9ddXYTk1-TAYqnqLn;t}Tx_*KF6dTp&D5GHNB%KwY>%Zvg;R$JoO<N-OJc1t=HH?e<S@hjD&|7<FY-sJWT7GYIuw%!URaVqy<H@tQDL#x@|JpXmDK8o-O8ItjRjnI}2QG!-ZYa@ISzSrmU;FqrP?8ho;bXc93qjm(ZDNnsTbO!hZ-W<I=&jI-H*>DG-XSacVJ)bz=kAox=dob_4Yw)cFMzVJ+1A<GK;jiQ5Tnx^M?41?2jRM!l=5;R(k3X{JkmTL`my@t)`+iB66h2_DNNC-ZSG8fhYh$BFk3@1|K0T9_L$F}kBVo51$*nIDGYT#lRWfHI$rMlWoVicRas7$R$$&Txz$D0Yc{#D-gN59&0yJIAfd7!3%0>h;7g|(@b;<*yR8H65?7+*ox$1NC3-P*%cXs>gL$10ZAv))@!D?c?J88&fUa7punk)+tp203D!92&<&0LDF>uOHA_;GnX&pY&p0D6ZYy76-wLpnqxSSjDI9i(OY$YeoKHPa(x?+vl3Hi4^VdiUKt9t2qoL*AX9tpBj%mZb5zyh(3m+@kEcXQ!p%*l1qle)p1MWLBogSX169N!zX{1xNbgo$F)DXGn*wa2d9k{5&DF*L&Uy!NP5Kktd=`zM3Iq5XM|)qsu~ktncXHTy;eLn&vgnnL!V83%={^_FmzXQAaO&I_5}6d52`Z1g2;%BU#6)Ux}z16vnXk*;r0adpLCq>z(`K~6p_s!V|65Jy(WqM|Uh*$7)>GrQc<c^On058Y91yU$4KMjy9$VO7`wlezhfDL?CevwJnu(|Fc{Hn|xPMgNGIPb#wgD%n{Vo>65EpoSo~xHqCrhpM<UpR3Lj;lU@dEDxR39b<CkK9SK7k;@K&h)c<R5<tmfO-1{7l7@&bAK8Td)?ad8%=fZOHpl<&rllHV#vEwr<Gq{vu&c{GgS%DK8JRWwDVXj5hn6LFvIcAI55C)nihiM0X<OX=_hep$cjO?qPKc0%Q1CLd@-pI8%>B~|=KgAx9=BkEfIRcd%=sO4g}m6O_I=p5j7V;IMEX%+exI!U`IhW=zu2q{%Q};tK@}*T3N2K}ejEfFa__-Ks01-LvwEaVSK<Nw4J9{%*{@iD-%*qhv#!2z(HqRFl-JrO2D#h=%P$d35P#YYwH~;Fx_he%g4n_Usm*Hv1jfLd9N4$Rz0{GTy<|IVXeO%PYGmRK1=rBIvfXqeND7X=pw@LFv8Lu_v}2~^es8(x>%dMom9xQ73@Dc$SZxeQFq(-QNB@<t6y+MvXRdQ*!-oqcHon!`!72)ur`v{Dq@#8LYFwfuJ3YV@UPwppR^TkBk_Fb1?ejR03S6FpR0f1WTKDy1-jSkznom4Bc#tR_Wg>HkMkS#ku3Qn?>2-W9&4RIEX+E#l^?(^mW$tG-7_41qW$4*-V6`$)G|rV&&}*^28C;VuX!WPX%o6%b^vFK39L1~L)dDDP$HJ<X1ZYWz@q@`H6(k#<Z(5C#Q!s)_J7}(nU$vCgi2oJ<B#2;5uj1u$*m)(<#dnVmFV3^=pR5pT2eIdC(+Aa&#8k+yR<AoHgxTN6;+*JpRtx{s9LU2D=h5yCc90Q4)`#cw7@7n$5d9%RZGu)$b!uaD;JeF*4ibguN2N_<L;9F~XP-+Y^g>Kcb}7_i2|`dV?|voqjGr1FU`}kBqni^y@)JFBYF5!EhQYFsepBt1_u<yVq!Aa!k%-ry!NA|EHxrjLx8S!KSp^E7$yFB5CYH#%ZUalkyGn-s=*@fBHv2eR&aqub2sb`^-7>G=ve-k!RM7MD3>TQ%A22EEl5d?}jsS^?c$q@%D>w>L0m{&{jvf_)7+roo9We7XlUDtP=Pg&FI|f_HSME|_!Ysl5vJdPLxzI;@z#b<HI}B6AJqyU<Y~v-|##kC+WoC+<9k!RAeESB94QaY1{!J%K_(J`V;!w~2vRT*R7be`dOg<-_TEsT@^CCv`hrj=Dt@a4jj+r?^GNWUTUE4c__wm0?liO0ue6(zzjYTw`!4jA>W4#nIGfk}2Nrjk^vCL0+CJfox!PuMW?_OPQ3E`rsD<&}*!;AoUG9xvZF~&gG-&;H7m7)XR1w>C%%=8uAEBgtVM$};(^*{QV*B#=Q03kd!U27N<-;y2&y<P7)fMTsu#6G2QQP8*>47A`Kkz4xedDB6wW(jc7vhVA?s~$&89hi^Y-8pa|6y|Vi@G~T}YXMnWY%qWa7{!V_chtPoN+gcG6^FosimWEONZPxcB=nj@BWJo+ctaSI0(n=5&^sp?uB(;9ElFKPHTw{s3$}RCtx3aSDjm;b%B%l<dpPrzTiXVO`>Hza%3KLBOYyS<+Ps|+q5O7Bz6w#yRwpq!l4{`y;RW5&ATx`MS4L&hwA$c>iO=J`(2rkoyx=n8?k?bzjxuLC{!9%A+q$B>8l3@qpWp(6*ZJ>0Eu}pw_ie=cT?!wAV{t2=jonH{YO_c5PA8cc$*|~nQ`onMrsdHj-C{Sg7U~{c@`6pSCB3hz#e8@`4t00-R55pv_$A*qW7SM(l(qIBvl3>ArdFbeFz}M`i}uQ&N%jK0Q<Ug8ZToV0{@F8Q{zU%Iln<#M7Q$6(e)~|ePVu9L?dwZa!JYY_aZK5;t6*b}eeo%D99Bp+S~iX_&9<+V=^Qmyp<Xe`s^9eOUm)9#IhS}?v51JzZM_bA!m5d+`w3vhy4uSz>^0=Z{O#sB22;j07eGjLWyAJhh1&blM>vVO^^>yv{hWa?rm;NTgT)FDh!>+J6n_s^(x?PSqlAdeSqKK$;`JVR33IPRt#4-3cY#JTnoIIc@wpB`v9YBmt1Y3`&ZvIw0!vt7u=*(o3D|;>!`rB3#+HtkO0siAi_8=d8nc03W)x%k&NRD=mON_iLe4zv{q|JB&MpR-_96yPc+URYeRfrd%q&WABYM#S#axFEq^r6HZIc{(c&i0nSg8WRRuTTzq&(cuxMZ0nku^hPBE#&Nj2lCOwD5<P$Agf!?^(?2)2*C+BhaE2T__Dq^<9V$7V%^YR^T~{@%IUVTMzT=y1}lGYM1*AX$`fq>HZ82wNe292sg9{$!HbXSj+2nTDj9C=ms!2n(P|r<oKgQ^hJRqpd7BZh*h8@_3BH7PX<Jmx(Wi;sA0ceX)Q@RR>TlKT~VxB(n2vp<2JWk@g`em+I2MlIj&MtuCgy-9EqeHvEu|~uRS|63msM)w1Eg*35Xh}R{$PJ_NouA3{za8v(Y+`^rfecs&|%beOHNgd@3V(%&0E56?*aQG(6bQRNjY-#^ZMi&e_@fOuR9{@hg$?W9e|PY0@042)kp)Jy{^v0Xm{AkQOJ%#AnFX45YQK%#s;fwcJ5q?H2Zmd=<_8W-9f2Kkt?YSY1C`T1@{W0pd*tAU4qW38|JDj9kWK0|I;pK1qp;?$jea8n5Qjg5RWEv}s#2NFUe@nTI&r=X|KmG`!i@Z#1+jAsqZ<cX%Q{1^`bzUFnv2uE{j~YO4x6CgfOZtK2-rqDVF34G`i#j~Q?Lr{}(Gu8oy8vVngvKyfBSHDigs93JwI(~Gs-QTxFn3!m@@cULNeJA6>-B?4(>)<lfa5T<#OF^829d}xHrzd%@6ili1q&_kP=oFQbjN|3#Qg0N>^<NxMT3)_l|nolN%YE}8ZbC+*j4ny2TJqZ%<!H67KvYMn(nTq~lR+*27QPeZB7FOfQ?X;>EOm16le1^MA%Xz<UQdQl{7mwC>kJj+PQIPZjHwv^Ob891@xD%~n-sJAg4!{qXeWxSsU*S-CcfE`2jMw*lZI#nY!XJ!cx<_%YicIqfB>AyBj;-f>%OYT=tD?Z+SP42+(Xc=64Oeq;hvw!2!$EpSK)B<)aPyLh_<h2*1X1Wm<=T&pNAUSV8k4{l*t<FLUp~JN=QwT9CVNx*$;^nBZ3IjWXa0o)Fuh<#u;jVL@IKiD!fdgIjSjy}jUWKY33Qvpj?(a2Ud0WcE2>d4T8{_#op7hHhdgaH*>2N(aq0P93w|-@lQ^#pj^>Rg1U~nXZ<QG(yLlt{dV3rf%;vvmu$2bmWD`l-8!vPrD_j$K5l|wLn2xia+U6|Q$kTNdHK8Kus+Lb6Bj!6=u=8}C1G5qp+v2(mCFa?LAQ%pti+T?}F0XU?fh#cqw(D2+0f0eY?7YH>;|B%h_mWTp-5<4GnC|kRam$fDhq)MDH5aX5(QWiPi|Pm>G%S!Jbj6;y@4E~VDx;%uRZ|P@Le4vsWX=P6y-V0_tH`zfXN8)JG?${Sk#bM$U`Xw~D$&mb&f~Sm&JP!RtNz$*rzF1m*c20boCmbz8@Ji_K8Q_%9j~i7GMf9|wNcYv0Y5m`>|4lUP*Qh8%VnA8p(XNyH&Ms4l-4c`-lPqgX6y?Lo#e~3%H`6fH)bzAcaz(Txp-g5_cc-V)I$2guifb<h^k8uSqph*W9*N~emcgh3@jlFqAt3c`_GVa3uABe@ni`%H~(#GQVOix$?*w}QVt${UknldQTNk(0YOR@y=IV@(kn$vVSQL>@vT1i1}s@97dO@lcfe%MJJ9vmY{iqd#F?wC1k2fn!f>_)UKaNAOu94(qnkRMW>iJLs28r*(qAPrA~4Lwwb@&Ra)h>TYSccw08WAwdu_TwSOMj>DV0)jog!4QET<*P)%?KMOeb)*o71jgq%YfjVTFDR%$F=Gw5-EvWB71h)<Fs$dl~cl#2@K}KH1QWmtX$d%yEv%NK?eGcl1!X{@qfnq{M~|vcD&`?ReE9OvOSgMYe4}lVG)ljpLEHH}znm1H#(5cUwhZ%)8IQWETyzytp;#;oVV;q(z&goWHZ5=MZON=8SS%#(bP@Ceaq3(QGwC1nfX7dT+`jlltf&61q2*rylIk-YbB-o<nNg3D5;gp9vK-IMp;c39%;-L>8>I6Xqiy3N|z(cLA#S^_x6r%M(WGjS|SSPvRg;on#;?2W`tT*vVgdM0kZ#E#^VxB?-@B2tVkT8r5r$)dRdzMf!%KHzg(zI{gIiYl1AoA%kZE$|_ki1c2_XT{sbek9sgby8K&tai#@ZOEZ6!6Y+7`v_^eN_ze=p-<sKaJx=G$F?4qxcMTytBwF0@W{GbwjE}PAq`;V$_@sVS{iKRMNR!q6zJ5{NMZ5RVI&3FEAq@d%HsY(uMbMDNX-ZgLe5cZR)$%$8&r*f)H^4|(vkv%;?eQS3O>9)q;(aUag~89BHgk?ql~NJiDL+MXqW%V=OkGP>j8$MC^ARjZEb}YB$VqmnMO(j|mnQIh;I%F1tCdQRmyFn4-YwJ+AkopAyBayItmVGAGJ)*2H%`;fA4W~Bt?)MK*Uw42r9>_0X63HKlWy7*3ScVZo<kS^3VN_Dhtpj0P_%DG>TH!1xQ|t~@wJLdB6~Rp88Z$5l5B&S#>RAQ4Z`9C?P-Laf?5W}XjEMIj69HM-LCUOaiwT9Ak{KM9URQT-uMSrS`Nu0StDQkL=YC03B6G~G{_?&NI!y0LkGgFUU;~pz12^(jj8piQ4kU!A*FxF`++gh47+dixJV3mQ}$7?DA;S<UvIlp%4t+`BEikG!AQ=iiDCe^5y}sC@NaZ5La}_E1dN+W5f8yv)HVVdKYKJg2lJ}-3NR8%FcsaWm4ylC6XpSsaQ_Xg^Ko*XH!wFpT|`U<GXW1?lp@{9@V^1+w9;<<pOFI{qogFwNmnH@>{w(=yzrREy$23psQ3x)_Z3eTZtmt?37o;e0?<4O^2YU+kc~CnX>IodUgSgnEi|?7*cgc&)iD6nwO>7b1Fy80FC`hEH)ON~I0$Rzk9YLXUd)u9ysI1|UF^_&M(~i2F_im<dVvTcCe~cAlMPy_h#0A6x;H;(@8Ba_()HCr8_EGocH_4*l&5fFZoQjFVGaR5mO@+wXq!tmKJcpmD?cw8to<Y%AA0OVY^AgWg^|>f4_7iNpX`fA*+Y!`<)DB*K0$;Jl{a~RtGAEh3X8%m@J<M^I2gw<s{{OF{=yd!tPE&bG98_tn<@rhWr%848qszy!swKNLkOfGdO1T#)jUsF+U@_AO8FB}3mq3z>xk!9{#Y-Oa>nHcUyWL-O(n{$kZn>Dwj}`d$})7k>7s|V6>}=1v$=St-@3KnHbF&`{FE?zzCKqOWwoq8HQ~lTYMc(-LEWokM8+}<XW8Btz&FUWD>;o9wEaAnDhT;{4c~t=94tzT?U**@qrYZ;k@5}K^0BfKz#bI=La(s(5L|K-oIy_0w{c<bs-4d`lIm&&vR>asS|(mx6SpQX82v^N7lx?w!4>pRHF<4P_o*3$jxh}*pv(6@cNLW!cE6b?*E|toa@BN;*4@CL0^Jv0CMQdH%w+*Oud+FUslR4sclI&OSWXg>Z2q+fUT&s8iwtx1T6CM_6hM^<Gr$=(izaI8_50HkNN+QIi>^=hl4VTH;pC}3f6>Sl{Z<75u1`h-P$yGfIg!PtW6qhXJ9lB0r)jz=b;NBZk_$rAdX(QGMs}LD(@Oc{r|>3a43Qjcn|Ie2L9~L)aBJa!ZX8U5qJG)$k_We~I0}?FNXjC2{})XkI2S;`DV}7gUWB=BW=bG$l59d@#m31C<6pBfKgW8v?UmOB_rp!)>NZTeP437^@Pyj^T&QK5M+}zbNCv(?G-?}B?h-lAWoKP{$VA!>D0{PMkJp@r7xByF8QvOa8RHscL@5H9me7?4H-*0zLK830PlVuUmRUa$#8r9U&DJtz^dciFU1rS|gI<WtmV|sHONX{$>>tQ5sA8Kxf2o0I<)ltSo?zr};z@Fv3QGU<mq+j)5hO1u%GXkdDLLhcC1h^fGZ&*5lYAG*BA>9(j34{q3F|arzyQ!slpKkYe5Ix#0+9x=$dUz5wn2<Jg1q2Ck$)_%6e3SkVe|Jw-e7kZ%G=xN%CCzl4HHB(e^-X9j@%cN-REgA{E>_boa9v96$rM%R?OjG;8F_CUeg#!iB#d!C6=`RjcVD%27xx`gY_l?PuYGDRX!%%)%;?hiCxXBA5B!8zoO&jrEqqXML~7rcEMK#{8_8>^`@TCv^C=39f6WvipEEy^LSueXn-=H%@Yuz{TY+eZ*o1zJsSIRUIoGX`hSSPLn8|6y`_)!>Vm@N5|B)g%&n|$D96faYoVKm*5Uz0g+#`baQ8io5>!<fE01k(gk6KZ2-K?Ae<vrzw97+X-qnvyc|{Br{gIx&mGx_nb;r#l`9XdjCrKBXIJx0W9>qtKaOHN^%e?@v=NN9k&h}vE$jW>S(^yqW?ch`-K4%+b;xX^8?zqOuR98c^XrJ*`Vk|SH$sFl$VNPWd7&<O#H?dTLduK-+b$HYW8Hw<zrH8q&E`-w@ooraL;~s2&XJPqz4ffblFfZ`oADHO7s6xu6Ge*9!sw3b)=F$Wi2`#y0QOR(subGg8w5%3uJR})&kOD<D%VeO8Xcg(pp?KC~4PwLpJ`M_f^Oae}^)aJsUUBkEHJ=!mC<`XhOUY_aN>yKhsF;{F%k4bz%k_(KQ$)mWZfYci!3xZ{FvR+WG6Kc1LRYvDNpHd13$uDKSqhVpSl~U^L--00W`iEl3QfwBEcg#!+zBJLMTO}{r>Wq~O)6h#%Em1sVq}R1lHa_e3<eu?u(AeCy8+6O>NWt?_(j!z35U;=uHnYLzB^s%K1DUW0w}eFZ?-h{JqiRK1Y=v;;&yFfinR642N6J=D*~3ank6c&TdSuiQ%TtW#)LFx#;x&ra3mm8RCWhWq`s7vYFLG)<?hi<8zEOln+<A>{7}D<1mdwJBoli#l&IVJ6>?N)K-4g?MF{Gz8BEagO|N?*v&nBQpo*KsG3Mam!Lwa_@{fkU30Z=NSK!$On!cVxpskzXQ5Y2{6^vrTMj|EK9Nf$kYwFG^W<c^JncG0K7V+t^S4Nz#eq4eVe94|Lgme}_AY$$SWv~SalfA|t40B3>3|2vV3x>|!IsQiJwZ@G9V?JDr&T10QDM&$y6JN=h_ykU&GzBHM9*91D)?O0idH$7lewojw6Rx4F0cnVUwI1q*|M1x9JLm=@WA3cEf{?N;OW8M66~kFOS>7pFp+F@LLc%)+d`^r+Kz$LPR6vIr=dJT#JEvWH`;?so2-pOVd;Kqbq3)q(NI_RPEqjfb&s^myEmnhz4|i+$i;PJ7mULJW{(W$%85}pXHT=wYQnnsMjgz0C&VZo~8=&2YM6L_L5kw-5`Qip);v!<hYFzmK<J%x_W5!TQejvnfcyv;X<ws80%~`pp9#|l-#N9GeTYFc-^PRI}D4<k!bGp0hp;S3MUGk2%R_p^8G6wg4Emoy!?n40Cv6=zFyYG@<L=V-LEnk`j9M8VfR$LH)oc?e@UD_gKn3XQIavGXEEUhyL6ON>h=Ur}KSQV+@pJVNQ?j@)pH2XfWCoXhb|9Q^zb5i6`@Tc$$-sS_Zq_Dj;Yj_j*N+yK~t4oOyykBM*^(f2v6J#pHbL&95A>TL&OjO9BR?&HQ-71VC+T)QAMt8tYek_hErMJlu5<`CuE^d~M6TTp<EqwANi|NYhvNG1;L8UfY@FD|G0yhbKqQmiNNFS{^lh}8%Y7IEi>tJrp(1+czR~iU!673H40RVjwic}2v9LXReR2V!BB9>o(TLP&O{OKQE1wlvtrwW9T?AhBgs)@B0&tmi^4CO`m-;(4NNWQw<PA24ZOYVd4I9ZL%IkeV+qhT+n3W}u$inDPx)A`NC{5gYw)@MP7mi>eV^pZW^J57e0FG>X{Lsy0}eE+k*!rWA|)L-$f)Ss6|HdK+JGtWgirx#SW32rD>Nqexeiq4e%IO?Fk-QN?9bjFrEB9<yG6cXsnIbXIUC)TeS$J1ma?XfZmLqse3up`LuyZRtVMXxuOv(?<7@-#7g&p$U}N>gMZ5yH0@3<!BqE&F-(30UmUFJqF9lcYyA&6KXS_(}_I-aw#OS$H9?Yy8^a?Q-}Z?uXHQhNa252g?xXC@SUdz<tlrEdgCKTF}~TxgrxOI?tJU)8@poRtabs-yq+{nc4%Ixeqvqp}2CVB97vPHL403Wzs88K3KybslU*#u!_<>LZgu036p$><}a|(w(Po<ZV)s}+F}cDKTlp=8bV{rT*5Ky-t-s;g8@2xFhngcM`9rpfns#zs^rS=w&G%=YOi`7OcdtA-7mj_3l5|9V^^~%eV@$CWp)LTZp=htohqPpr5H(lxogVH3FxoTjLwekyE}wO!wXMx3;gx)OHsli6d_+$acsmml`DfpQ7_*o!PqS{jpE1=i@dP68f7i}<#Qh`=E8p&1`06bHVhR9MduRCNxWW&tGsh`I-bjO7_m%l&(jf>SsH^hB~fNJX%4i^SQQpk)fbU&uF?QoVS@-OE9oB#jEYwo<O5&&Hh&m5EB#2e-+qT`oPjEs!mW;|J8|ei0Tiv<@|P(wXb51{NL=V$4P^#e+M1$1W(k68M7sQ)Y2_vWqnJwU=BC;{hUY4p_T(DH0XMUe$)k^(oLKCqh-dM4_lATGHXK<U{%G4gom+&cCCC#yQa3=-Oz8CPhzSU`a`cpJes>~+IZ9_A#+vi<*>aeT$UZR%$DM)xvX<3lUx<Rs%&M{Q1D|}6&naH*C(jynqPDyhhihtw%dP})nH1r*PSR=`lbPP9JcK@oWFoQ@w<}b%!wZQ_J&0kNHj1s(^j2kK-;IiK`9Mi0=#3bbj^)<JH77w5+D~mp-p$XI(DnVrCKu?1&wdc+3+cS{SsOlirfBF~6W8;?#Fy9rnc`&`?5gOKoQ!;tg#wg!%&0B=kdd*We;;w~_%cg<vZpFA$O8|Mr)RR}Z6JHwwN`^E$;7>EfmCnr)d)1^scl4-LJ{U7bOI4Hh97<tG^4NUxe`LsZq^;&^XuK4boVi54Te}7e@$U^`CP*-0E9xj>zK}C$gVHk%e4;!tqvSPN?Fci8Ri|y;`oji{Z$I5sxK9fYae5GvX>({D~620;B+Wrqwa_J5H@!%pHdR&L9jK!>aDYqX#hVqTDl}s)^ww&$h87`0*)c_^pWCV4|Q(;g=`&R0-8_zhNxz!77d(>An5%g9e#4bDYXu=UF%`#B=dqnt1F*JgN?79XJ>H)lY}D=QA#&o7bk<=T=)(KhuF~l4xf=bfd99hD|d3=>QXEypYr{KrzQCOHsp7Hj21Y78hTe%x#BK^8s5$aT#=8GLz1Gomv+7_(@W2|0MkDWO~IUAfmx^cGJ(KUO;32$yA^vvJUN20m@qc!VvJUz%8k71v(kM|f$(KrQvcYE;Y|+_=WfQ2Mf^U5GOH=alI`>jWJLV>y(q>{X`>Xf>>JhrzhV{AUL{m<#h@=Ihe&J{B4Sv}_ytgEKuS8CFs5|zF&lD7&`7smDzrj(xZ4kvIv;YASA%82kXxGrQ_75=ZfP}BbGitL{0LIhOyQkisHeiTvSl@fZ#vlD#76+i-asgQH(OBcUlTOU3kVR7T*){UvC|Q++}76XZ#4Hjt<P*2`(u}|-7x?cR61I)k~Af`#>2TC$euG%ls3+Al>L~`!4{W3;~YV=<!ux!&~`!uy(qzk8HG7owd$21FU3YcVNnjXgY~DDSgmpTbb;0aMTvL?B%#h2Xq}O{YD*E!tkycyt)(;=STq^1u*;B!?dIV`x_0f=PNPX?qdIK+OvYOIG>WWNixBK0j%f9;O%ej;Z-x1z*5f|{C=&TcO*eqqP@eK_uIBFt9R0Rrs-njt_D@GC@Yd(r2ePpy>oE&;Voz!#&k5ApO?fsO$kl?L$ap9o{Ht#uqb4K)6q@$|A1Wx0JCmYoy6Gs4Q|CJAF=7QlXk#0O>>+M0jQJC%)8PvZm8H`r*e9qU5|5f%x&<@R@YimzPv&f$scBf@KD<xg)*Vov{C_cOcf1l;_3C3wn}!Hq#27*C3{)@>Ytg)n)2(iXyd?IatP=C7tA&kqx?{Mi_tKD<Ov{USj2D0#96;SfglzvKr6A4#6$I~KZl_MFcP1>*Z6*C@!QdaO48l$!bUN-4?VxQAhc#MmS@MgPr3`3)Gf}b>iV8NXeqyNZpyum;8HkgMN#bhX@t7&)OCU}rw1i>A+H;r*_C`OE2}G|+%cECk!}c4jHemRdmJ|f$6$Fo$a@y`jarbASrn%DBXXTKZzj4AVzn9{+g2Q04=%E|jCbV=!e+ZbzLgs{<3DCYg9qK<Azo@xo&hW^uW!_KRlQ-gxr=mbUrbhX?XVZTu0YRI;oaJk;gS(mzV~z_{+;LcZ62-(#){FVTNg1h@3Kt<gt+(nxWM1p$HDU|rSaB*TmW%J2s~7Xtg)b{TomG3n@<gV8dSC>I6)-L2?eb|x?Cj!d$Hd-vtB)8iYi+%9oPg5|P=n#&h8zxg8PDe1V8#J&pl^f2E(w-%v40a!nRcugP6UJKxMBM%QoubucrpwUj17Ct+L_UGsX2p<%l#B@3%3LIb_+zE)KR62KMQDGT>{8J3_e~`nu;#*4HSVU9K<nb`*+AmabAz;{5VcAK{9me&vI_no=z~9^sOO-xHI8x{mdJxyoiBL`}XI(78Zsd*bFx9CnaWp1#fH<6T`hce{}6}kKM}vNuk8;6a4W{JwSy0twC-_Uu&gDO0%cQ%RV>)yac;o@52WL2ti^|aejywa64dz)^I=kSZyW$By@DTYFJ5HuNRJQ8_;w=irZV>ESMWFJN=CWDTW1&>f7P?d7MW+7mB{OxD_yN>ycWxWoo>w29l;2N$^?0W-Gv#s0V|#3!bA&1R1fhvFN)pNfmd(CH60~vI<3Q)aw@BU<-G}^lRU(%B91rG<0)4n9cJ<pV_zk)mMUZA}Dk0#w4}kp0FCRG+YQRhw<4*@pz0f9o3E=8b@sq`#TvGOoM%OrI~y0y9azC1Yta>!mX$Go@Zg6A~D!CLDH@JBm6t*%}ub$)yA3S5JW!8_83_Ky_2=rBYrsc^{-6tV}p~glet8#c0pODrnfc<zDGX(NUQNU82?o&kGepZLKy$5?vMP_3W20tP#~7Wb}RjXH~eqn<p>K2+BSwct&sX~<9&w*+AGSE1|$Ls%TsTfyp%(l%sAjOiTPlkzS}Z6f=ly0F60vGMLV1Y+e0*KDot)VZf9!EickITi$%GF=dLYlG?J$<;%N__kWoP^$zt=BYi;>wQrak;7<tKD$XL`OJ8?|p3)I&^jox5Zo38yOQ|aC^6axrACE%n65t{tkuGew~^3pryO`*{v8&6J_atVX+ok7N3k)MLz?l~q`YUA-a)BDXujBJrEx9ozn=pi;YjtKYlcfiIL_(k%FBcHl8xk8&x2j(T`N8TlPu!_}P7Y$puJNn^u6s?Lz2Q2M=cI9%s{bFyp7_W+e9&by4bR931mcUW`>qTFcwG7sUIq@%a8#w#)8>%x#$9`cUHGp^xDmN-*_^SJ!+!3mhRBy0EQb1}w{<09mEBv5+mx&aG?Y~vaR$vt1yE1$V6}YvYHgp6T)HmJBVrDeAGTxI-3ETBsm`a1(XB$g!EM1n{9qNj}Z1cuPvuz+fok^N*yiwJcvM%Uqn=v-q5r15tA?^`>nYh5m^*D)YN|C;mG`gzsMBkD+*Yd<e+MdFtT-x=7#9HbPQdJ~n^N{XjciiS%YZ#zV)gxx4gW3EysWWBGe~o-P!9y`G=g95M?naHez{R8BYfzAetvD|%$H~eA9-g`KAyn}5#tp7#n#Qdi9dqbH78l=BfNufSkSY_SgZaIPWcW&sCFOZ=J3O0_tQK?sZu9IOsnM7a_A!i_#D&NV(I4HTvhIg1&p}8IEI^O4yEeJkhi<^sp7PLm8jfetp|F$G#Q{RR3coxF$4ZQe-03jp+1a!1zosyjz(DGmC?6)qq0KxF5HTPrw`($z)gSC^PdTKn1aq>5Ube8hR*YQOAt`KaVv{$hq!*B*!(*#F96dYcYr_RlF$L%5D1C!?Eq@(h9O}la$F&eh=2;n4`)S3PMtZ#=c5ebv`Q$)V(f8CzFh1x)Sa84$gswa&2L&4VAT6DF(p33Wjm+F$K%_VpK*QxDTRt!<cM<%yM1YceK_)uTSa~s{e{P6o*y-Z996m&gP!q-f{?ak0ul^WrM^a1;OiEvnN)M0^(`D|fXHOx5?b<oC#mOWzhLZ!Ka3(=KzcW;S*e$lkFr(7Y8D8T&_yUh74e~_ZI$^y*NGWuCu8?oTVLw4A!><v{j3WtSxMt$m(^F?vVpa@@^ZBkn%wBw|G%TX(r6hGQy{n}r>RKc5Vj|*PM=1i);xCV`L{d9~jsHGa{!i4)8fy}?4C(a{VZn10Ex5XF&n!i-<#gW|jCH~JT!LxSFyzOs{d?;#Cifrz9|)j8T*H0wHq5H;7!JW>Yh-kcd^^+_n>VPOIfB~*a!$TRGDl;~QGX;c)(wp<^yu0dw*IDKXW!6HT$`R@&sIEvDC4dNBXCv~*hveQ```fBsTF+029l!EZAPM8J53r0FStD&Kqy01bFtOl05?yqJ09>#K-s#fT86OM=T1UC4;AZ^xt690Rr*V4P@OTKN|86q^8!OWS#HtZODbbbOWVD$g*pP@^|&#QXJwDo;kP^w9?7xlH~?%_EpB1T`2|bF;}_L@OrC_gbGYHG9LJ+UMpi0NIZu5Mxyy2D7o3?A)k(kUX<6DHwqMo$spim5pXzuoG@`xjZe6ee@wfuXzTUA2LCxgJe{XyBuT7%>O?wfmK30J!=9jhUfYs^fSy59D%1DND4SXF`Q}w3tn$d!$3jAam_)<isoA^1M+EL#`To<W8Cq3hCn~1fokx0ShYqYgK4Eln`!ElTTGWjvSL_$1;3BVR8$7{OIgf*^o(Hp6w4T(Nq8f9s3F0<)Arnj5lBegzzcYH*r6ys+Gk?5Bzu7Wf$ee!O8Jl=&C(?`~MJao?yd@!{38aBEny`%+Yp-T(}==2%q7AGfqP@<Vke)1%8ZQ~yNqco-u(g$`hRqNS?d+)++b`S!K-?l~IIA0>N+;tX63;I~vT1U8ifAbtKT=-O4N1U}ia(py@f#QStAYC$bTw{IE-Q#!dhI`IQ+e@@FxVokh#Gn>cw?7yGoQN@;&xB*aq~bzS>oU^3abCUR2#)CYNpWA-42_aB!!50eWNp<io^iTXZ~x}#YMX-2DIv_<wLu_s(S1VYS790x`^e}q=QobT_)?0KBKuMAaJW}f9NKVlBVDObpp(E?{n+?p-hW8!e<k>Qu_DK`wAWTl=0fD0AO(7(kn}c|B&4E!Fr#GIjd|F-LoT&(YNMW%J;<v^sd_XETFKm29?zbKLrv?T8EgJxF1-E)naqWqGehKSut%4LyOe5u$XK}G4tgiU9AeuPexocCvUtunJLNe_dqJZJ%(zhI1eQj(tVNNS;bDcdVu0ICJ<z=9sj%q1Bgduds`TWO#vj73$**eiSMxE4yl|e*t$}nKEZtB+TVOM~BT8yVD<{*s+fb>3tK^9W>va16G9ec<_PsVr8W~n{6^v{^#nv8iqD0D%85d1z)&>Eo4nR0CSGg*d#`_Q8nSYF>fn-Hk(xqn!r-%c2x9ae@JnJ}MC#-Y~AKZd3pLmX#_UvD*H^l;iW0Q)h3k-E(?5TJ6Qeq00EfJ)W1?nkWokqZ76`hd2fQ(;Juu|?UN0s`uDg-*CJdr{PrN(xAAcVso6tH?~76mpO5&1-WrbsDe{^IfSa5fi%e4lO8HpdXH!rtW>bpru?uQA^_odIuP3q%RCN>Kl8Wv=tJKlB-f4)LCoOp(ce7+p&eUtld$sK|s0K@kSu>Q}Qu1N;sQn!zI6RsHhl%<gGfpEL8|2)&3$hu!NYA_oN343Yg_2Hc8Fr`$6XGGAzFmsqb&9Jy$b7=*23I&V`XNYGw3HfqRVQOlieDJDPq4^mh(px~QjmkI&2Ap3z(g+p~&-n`33_11%ZNM|u+k9uow7FtDe`-VC6`>^!MS&BZMIsjAcrRM%&WIw~6BjvFWU(4XM`*TLqcj!S1MjvO)X*W9UY2rG_>F7aRedFj!?ZoTG0=H#KU5b|UN(;JIU||)gwufR1T&ga21|P-s2PNkA`aF)Z@&sZ&mq!9-Y`kY5{J2^8i$zuti$5tvjmZ+!71b$~y1LTq`MWxj96vK@=0Orla4CHoMDhyT>aaLh%pAElvgd@sC);(e>><VZ&HLgv;NOZx)j@}`L6JdysoGB_vyKAck?}kHea<W{w%5^Lcbd(2P<O<+CvZR^=0C?>FEeiRAc2v-I~XlRhmuqfM|N~s!)K4{p&%OtUiH~5-17aS(cwLj5y1SYxUszYx(LwD??&N!`Vu@ogD1R@NAi>j{(i6XEif&}*Jzw43L1)*W6N9jl-MtYoo$)9O7Mi7wL#nL%oeY&b<HZRQlN{{v10|V6_TB-F?Ps4btil|)cI5W#9mi*7==!j*b$@+Qkl5}_uZmKy6!IASSO|dVgG0_=~YvTKF4dYwB`MVT~oQ6(Y-|SKvTBOm(YiLwW#>VsaKphx$wwt)ZwX6cE&-{#^!}Y5%N5k%{0(QXlsD(I6D4R-xik|i!YNL5qJ3>De^rJ_=TOaKCpjvd|-VkUK=V_==r06WkHVZ9@454_PP{ZU9JpfX`49wtnt&1PHXL58vX1rspx0CA`$yrz%z~;jf!c3(6G~P3?N?j<9dJiV7Aa;JVC|-3jj-F>j&1#egnVwnlE`cW~KqRGj2hT`9TXm%nIf!Q$q+?$K;hZNC@eVvNBgaGue9F&Y%Ra)-B>r=`c~5lAJoe<dw(`a!7n*Nu6dAfbYrX)z|Y?0fX$gD{_ezu)@_K_#_BIw-Fg;3@*#dNh*3<>WLO7QAX)fAVbO<9GrO<nX{ph>^fI1@vxM#T4k|1(NzGQhWCfDy?pgxQuBwTZ&pYY#Poi#QdV*1%IA9**cS(=ikZu{lNB}yXPB@8AO2U3$*Gz#JfLEdD;;bc(z<E*y29@4|5+c7C2+XpFeq)Sn^Gw;NbpNI5a2+A+7UGneW*akWBj4B-(?svEaWS6ob}L?ywwtdEIZ1wb%2b0ERLDuPOTCKU=h_OFqN#bdiGLqcVNc37m1)iG=*M^R{mANS?YyyS@y5rqk*FersQ095cj7m4|UFA^}tptAT{240bkEkdk)Xs(4-Le@!HH=v_c^gW&ymQ%?`SLklRv$c=N^}>y~14g<Qj*bw|v<$bmqD%TjZ2nFFg#n@G$aQh1yd3-GoMd(+8DV3V|R4B-HWf1PyCs1QW9;@46Ci;%7%2f0Q`Ve!nrokB;T-3v@^yXqoMH(Zagem9rGXP61#@9C`<+pa3kY3t<9V$q?*n+F&GT4=uSdxh}ACaio4m-sY+z0Bmd%Y-mM>115&E$eCMEeKV78`P;At?3;|O<s29b_QpSvHRB-_%;Mma8#$?0B=ryj&&s*I6ftz6;etWR?V4LMON_O&k&@e-jZus3;-I1>VWMA;6BMj2%M^~GYbfB8<qt)u`)x0I9Wz}M(sXJeVX1xY9!sdaLg}zOnfZ5BL|-*akCaoQco|yavJ+rAPHDHpJcB<>Ev%GjYLPDwW<zJN#x!zoTel1G0q*q1TX~J=F|@lrCpPth@5a>I3$B|rsu&b<tPB+>CbPjFJtr{v$|GhA-UDnhf}^lk(@ceGPy5Ue+gZ|7jZs6+y8%9kw3gibiXl={qwu2RslzR*^p|jK`yMostPJjyfOl-wjBLqf2cdH{gM;fSyka;R2fBT$H6$JQAL!^&cV5PaS-F!-0U$TolywOxg#42o@{`#`rtAO)>!G*YAVQuNUs^{9WcKvfvH@ZWzmA#O5tjIr|j<uLlum?hn&TD5IIYCN~{?QYL{eivCIwt2L<q@Z#R-14l>Ml1s3&XrqYIHo>$Z7>^HFhzOM`y@8~~S*asBK^7Yd*TsOrI<jjBpYYg}SqA_(jF(!frj{SB|OHl%FvP@|Xu=>5G=vo_^cp(*iN(ro7@(Nx_nY^A=Q2m&?5Tz~uEH%J78o^!K{un0`P(jjnGsQy&e!^lzqt*G<9MPJal)Z}$IFMYLRino%N>)`@fLJ_3LDc?Co<Ij$<{Sz)acK2mqRq%Lj{e3xPDkx+MQk02VfikuV95IynXZ+%U%y<p?~yL4%xNgF`io=}(szI8Fl#(SMAZ*s$AeMf#;`0^DCto;JYLG=M&XF`9u-!;?yU$nM5c9`Acz<nxnbbNZ@}#BO6F=gG&JmB_4~#JR+u8%dxil;*F4SclvKCGuS~Y;1NwUBj&t05qIH#27l+i^0#oW`hl4Zp!)`t_S{ANeR2s&F%54I2>_=`@D$!iY``0kMi-CIveW)3NADsGqKH`u0{V}Er1{;X3l%}Q+f;&hmWY*I0Ma3!Nveu};+W^Js-2JDbw_4!3upnioWWTOw{Er^?K)XTjCs6qkoJY@G<B%0V*)4s&RK)ywC4Z>FcNf|Lq{#|=D34MY1&6U|$g+XL%)b;L^aVg$4rqAVsXW*JkWp!1b2@g703>>-hI+6a3Z<hays<rvr+DIn(It`P4tbze$1sJop4fM0gQtV3u3hVe2?#0odIjaz9N^G;onj}P6kIQ3iD(!6B7tae6?0X_n+OGz@{8&{sAI-_rKmdBr7vX~y^Mu_b$lh0y*R55r~#7#V5no-3BY8KE9d3$CYL)3Qul<<^9IVTkXVugZT5*$i;cq}X>5~H8YT)QadHX}axxM`8!poc0oYZg3Hi(<V$Up{3&wLT_Rr<lE1OUn7g~(L8nF=ggtnYq;F9LohEw?yn0Z30E^Ij{EMM1i?K_rr8s28#SWH_Xfhl$!i5M5+SCG1rcsq*uCJTu+(WPDHe}KtA&*H>rtndx6poNUTFR#09g3V9qVO6mVi6KWU1w0Q#$AC~nJ+n*`I6U8a-nPU3Us4YUqn2!}SYxy{QmgAs4CR*98(s4ontgz1$%sNWTGtGZGLYIHeRM0hRp2^+lD-d6GT|pq!Y?*CQ#x_jOI;rxS~xv)v{@9ked52Pp`Xckb`2B>42EY%wICF#l}ZGF_aRD$ij941uJ;A;&%MpE+3kOKP-<Rf{5Cw_AAR&CZ><sP?f`te?yZ5(AIuvC5EeyydDCW9tmr~l>h(n{!nA`3S!)M0{6V$74;i|ri;i*ykV&oB;(0Hf3$ADk#RmI}i|Im?k*z76(I2f`njS1~0f(x+w18a;@}9`TmYdxor*X^ZC}-Wb`w%dGDQ{L{q7_34K@DgE`5LnTYvr^w0n^MQ;<4BDu`t|NJZ;$5=DFs{&X)?wHJ%l34}6j|A+Up%TlOx6S;-J$HjycQ8eV0@WK^gm_=0OM&Lh11@~ShbwW8U{bWnLM?oYz<{~sao1+HfK4Z8S2%=!uM`dSI+pAYP<u;=}<vb#}`fC^Z64N5Yi#Nk$rI~vXJLFr0^1e072z5N?PL!8L-HM@Ba+3h%+x5LOeu5dZY&C8a9yqbS;2h=m7mS3MF`!1ZLQC$7887ZywA=K~_1NoS3i$Bl%4j9dM4mc6DwG}6MMQ<LzU(pk-_Vh_|U-|o|4yMGQA5`%>Wf3&;7cX51%|jmf+1G&=&q4XsAuFbrAH%ugRjL*iOA|kXo(q9RyccC2KTcU?l*J5X=p<UI@t!0iAIB(|*e%d`aXA2lj5$%J4+{{RkJG?*4!_X>Ha~_sN0W{6EB~YzfI!d|az^V^xT8KX39o58JW^xixBo%?=s<Iv%}iNvX>9y7gf+HC^xy~@>>0q4RO|B%;WhytV4@rHH1F{3DiCD_2%8IxjNma~cpp4}2kvgGM6G;H*W8AU_ODNS;5!)ub9=<11>Vxx2I-3F0vABj+kLS8OX+BKwk7Rfc%rhLE#F}DY#MIp9h$WC$4*(+E8w&QxjoeR7Q5p-k@f(nLIa8bnj+RxsP{h8DJDx`T$c&Mf#EVa!qQ3;_)59qK$orBQsQ9Ro9XCymv!`sngiNDxwO=L4aTP%@^dYlyCg5!xt|qd!KSQqrx3n}PpZUyrzS1R^~aVZ7;M_zByyz$#NOrpPwg^_CRs+^LkmhmZ2u4-6%y*19r(T<LRH_WNX*uedA?e3T{+?4rlt@@?v1Ronqd8yv)-uYhG_38yRtrlK*ehb%HMt7NE$I1WBqbPie`=M7pOA15{t?X-y-dCtU<pEL0gZ!Elul3V3Al4f@b`;9AB1+eE*I)<S-M}IT%LHbW7QjPmk^GQcn>6&f)98wjc5Tk6K@79w7c`Grsa;1ISJFsgCzZTmP!Mvn)|3JxZDvu)EbYrwvBZvPn+*?gGoj8CX^9kjz}hFICKUS9_0i!xIbGY*AU8ww0Hxv*bwx-OLAVZ(LlMY9f~K<DV$%<pg{NSwzNxkRqvOt0@WN$ULy2fzDc2WJ*`dtwIQ~m&Uo5BA@@wNqmi);xz50)@42~V%ka_-Q)6umymK^>7?e)y5ZVgCyl<-JU4U+RsX@_c3?QvhLIY>kAl)7jZa;icdzcv5m^_GulDgD@I5{%=o;0WFNgM@Xl4Z2S`A~Jp|-7XY`ClsCUBH@Jdub~2vQ&CN%bNR<fDQHq+*W_p!A9P9SU%;K1XfUhmY|`&Ssf;_pErx#+MJ<h8G0Wuh!~guTNEaWZJ$BHvz_Nk`s2aX%gt+%LA9<1wWzv6x?ioUh;i@N2!Eqlq%J^^{0dsWG98{m1d4s)|4*1v7>f+cr@&f$0uQ~LT_ZO>bSH*UDehXKo1HO)&S(O^soQBU4mwiE!{c~E!+>L#iK)A0^%nQ+*f*WR3)_~NF0o4VL9lQmpnu_bfh}G35#v~_1&v&BMRsf<~4d6QU9u~^V8N~Sl~*{%cC3b%2xXaem%xLtird_boa}NeRS}MqM`hXs1m{?hVLxCHawp)plej14PZml(TUQHRAF}=xgG;?put!qYSuYXpa-$iGK$?E>*X!>^75&ov6vyuxJ;^|F8f$5!G99X#~JC}-{lLFHJ-npRgMA(->PFe{K>BMwKloyxhFJ75a1u#TA7vTurSlwRjs&;I(SfBb1Z~GRgGUHxwA+G?n_L|O$wdR$6Qv<$NZlFK}6g-KfHQ4OMDn0M8zZ9(lQgh$|H&K@&UpF8-m*M{l&FqZ?)^|GY|ahWUJSU9WNM&%~?PHTs0|`Y~Hnrij=Do*`wC9x2juj2qUhj&3+PsZ!-4<d1DY@IEw#=zby}C#tCX7`i_lS)jDw;v6)MTWZon(oSji^10L?J!us*op(=$)cHH9yzA2K4*Px7IK%-<?=q)g&_|$!hg;GvIWDLVCDO8^06_tAGeG_d`mW_1kL@%uzL8LAVW(VuN9;U)A0UhU1J}z6u2-xG8DEWtE#sv?xq-k>&O`Ll>bF8CVLYm1@%6T~?hsq`3&@rORXQ_k_nv@pKzZ+Y~FYx~nt(kmhYkKtpVs5rH7na7;e_7(h$*M4`42Dyb?FC8%Ppr5%Jt<C*0Ooi8a`U3Vy85=;B6=FI790C96udu5qo@O9Rx<wl17GE|+IC{X4os))5}o$Am~l5tLeAaLLE~m@)%$^mw3<Xr4dAsjps;ZmS6uwDT$~#fHla1EHUJLol#*F}@7XbkKK(GK6%a6M9bBwZ)}OHUF_rNEOu#wZAtl<@>sP-(8qy;<l)<>^#9TvjcknZelW|=JR%0K$#09MKd3xN>;a5V$*#&uQ08nS!BS4=yK})J7k|QP^G~1^I&w5`$6El0BrgH#WWwp@q!YBKu(8Zg$&gWTroFZ_4qlZ_5Guh}1?mPt@mzPf><2qG`0zS!%WQ%X|un2!+$^oZpjABK1@tU_J23b!`Bksn>AyI?zhmJo1Eme=3>+}~pKCP`9Tm8U<YhUVTs_<!kH>@4o(;!_(J6=;Q;~O@UAX(dem{!t68J?;Rkz0!ayyN3$M%@Q3)oUE)ftVqERisVibQcW3H$vDV2v;BamCdh4b0DMoJHU>w%<+B$QP6v}6ogG6QWde^sZE`2y9~l!2Q55lDg08)G*Po!rni$2uf*qC^8=afvB8wCAX|||h7C)yA20b5R(StyJkTLNF3<34{Kh5Bpoz)<{5doo3rulV$gANi2xP|l%)fX&x%CO`58v~rD|#6(zG|+=cCkF3e5%Z3IrD*-Zj_i+!+BQz9;7H)!KbJ?`7gNtCRXnOZP`cW-BD~^EFSq>mM_j$sjS{R#_lA#^qwkY{l#Ud*O(5;ofk7sDSU~s1PQ;9Sp@oTWpv0A;-HSTtY=8lD$9SpPam3DM{p_)3gJ5?+DC32p}bzzh0((fhpkbzntTbqS$0+?JL(I>cWh>R<%a0Olkhn|5A3`xY!+<z3`uBE+xffXhX_=9-p`<{x`5(UW3CbcR)0#aNoAiZ11($TgQ$U>-H#pI4*#Gt{`DvyzfUtr6Nh+-UJRbE?M$r>bQ+U%AEsOYkN@W({i~Gft_L!ls(mUw8nouXTE3#!PxHau>{|ySe7U$<q${*A`--;A%{#G)RYne`7ELei(H2F`8#fd19sK2AkJf+>f8ptbyQQ=ZqqGXjew4adEK5t22qmxGFJ+X5n{g+Kqq;`sNTP;-V4NU=4-EIGc7F0mBl_U<V=4LsaeF{h529R6f(Y-LZ%bi8el*Xj3zE`EOmc-MBZxo?@*5wi3;1+nF@9a|EZ??-CiGh;z?<-2coW8FKsqQC;{n>+;n=Bd)Ly{y)zL3TwV^GE;J|=Ra+!4S{}&LZl*u)2t|eDksi|<BL(__vE*<(gi-(Jp*zq?D#Os|y^B=8;UE_p&(G`Y#ypTi;!X>mN-~CTW8twgbkqsE+TW3^bGF;=5xA`dxI|p9HjvpQetPDY^UHM3eY}>O)reJ6mUK?IWyBMyWy&FuWjaOb+L&>)?@(X{_W5@0usUZ(ewV)uP=KzsqAe5laoHOAz@D;G7@!x{tZ#K^P{k|`LnS479Ywk7Jj2s7X+ki#Kr5sd$Z3EP^PUNU6pHrXQO8?JB64xCDa2uRy(8*w?E@Ny7YI;<MloO3~n=7A2`Ijw83ulUO$F4!-9+2TRV`<F0YELy?GN&z<g5Kf%er~E)gYfWes0RzRSmx$(=y8%j_=h)5UW7Hn2OQRbhy%2T-ExfSwri{9;70!>^IUN&a>8fYTjZiPpb`J>lGOvVe*<@+aiz_X@)XuT$~DtdnZqN%t3Xbu5nV_9-+>Ex@;{2(@;#i&P#ZXn9!Vh7!ink`7G<zje~$iHoE!E<xf;|Yy#}MMM&2OX^{9;0a%Tn46AiLJr6?*{6f#V2Uh;}{Bqpu$z>Yz*8?``i8K~DZg&!%Svgb*D51l-+9zLp%%Cb~5Ofo9jqjNr%Zp=fuO83(Vv6NJTPd#c0H4^yP>?dG&lv3<F9H-=HUdY3OaZoXIPSi0Wqr-jG0uDZLg1;_$P(Ku2$`m?4T~x8zC?ZCMy+43P{rtore$0@3p{vd}I{kc5zmIm2Q1(oe@=bXZZ{$R}oA@fEjhc+9mqKJ?kh_scuw8@_^^y-r7j^iEPCBJc{;-vM&8K?e*_1GTUa`l-CC(VmJQGsu;887p^Rw-H!;iNF!`R;lSK^=r>Opb$B<Tb!)JzT<!Yyio->Dk&a!wZs9Z>U>e^0(@cIphNv%1xNbrjd#(uJrrbX;)&RW7fPA2a5{j!HIO$P?@xl^`T9T;xBzKSZ*##qTI?ADiaZyr5nz^{mNZSX3L=vr#K!J5tLUFX(urB&#c<GpP6=uWAX2I&^T`o7d|wIkwv(pV-1FZHP!v)#;8MJe+`GpTSjgs|`%EZ{s)z?D~m}j0^$h%(CaEfcbOx=4+PuUWQzjOsQxFFR}!H2!<CzneTfVBhMU`?B4EemAwz9i<+~@<+Frbl=bD<PA%rj`Nd#ecnv$^#?oI*bUx$9yuLW#8o96+-3ag7;{b=>DeCe-T5dN|iLhF34Imwp0mKBKpZr_p)01~U0Hj?bSSV%4^*BpJcVyhkOQx8<QQ*<r$avt5>FbH2{V_ir3YK@${qe4T^<;}$q3x-mHdU$%758sp(aAP)YS0>UyVT`OGC#J6kbjI?p&GcV1!Z=zOjAtu=eJP}zPGHjI}MbkjnoXMtaxHFQE6#C7Onq3HaAKe{DOgB#)9N*gbb){D&SInS99X&DBA~<^p^>}k7^@#05KMt7!P^Zi0PM!NPZ)wO}A8i+EXVe$$FPuwq3MSg-clO;z(iG(_P|W`tr*!-*3%1_n%CfSa9B~g(bu_o8`_P2_Z_2nQ?^L0^1=69S_&M7uVmdb=dK8wHoAzMc!WGL%UJh0pK{`GQDuMb;um#md7G5@xGn%k3RkY%u_@?_i*%d>%h{*e|LL)IUr^2P|UIn{<y{*7npJ7&ODP`4e)OFlZTdNaqqbzwCRxdJ)(lPO@{%>7XE3kD+I~mf5=gh%?D2=ytF>((c1WlEu*7xYV-H%B3is{O`f#~P2DLh&<a{dX^y;&7q}$)*3&!bp~h@H%f{~fs_?T;?hzfOq94x{5C@DG>hFT(rx<WUq>m9Lng3(v2TP5+`)raCufaaBBy*8;g0+(NzgV*1GXTm=!72(H!o+N;Q;}10i69#TSo^P}a)hvi7Rps#qSO7t=)JQW!UzdkXp`NVIU79Dy0WSniR`!D;5}vyLMN*e$96GS>m0l_BJ}}>-ixGR{@JO{vGaK0HiB`xJ0dYu=Fr>DX8?Sw@&xrLW7)=jI0&<YM?JwVjZ6&-jtfrR?;2ZOl5}gPR+OoDs*&K>flfb2S<s;h+6y9hmq!>Ljt;b_>!Iqf;<{-T^JT%%B^fV86q11Z4xfj0@9nzf3)&%QFtxGKY*S<&`8KTQ2(?%j_;@nvE03zt@A-M2rS=trG8nowFn0$nOS4rD{-_J;zBPk(w=SptQ*Iwr%#%oBO9rgDs(uHmLy34Zg+1PkR+%VgHgRVUU+a8V6F2QK4{WMCvAI6~&ZJ=zCUmDHVRYd+lRm0Xt}FT>&Cy|{lWSUQ*>I3!mj&i%xtF2fS`~Lz&VYh!4UB$u=B7XYctHT@D}wQ=#EydmdzF8b#)5O{VX6SDt1G3)ugDte9<IGITDO5NNV-$hcm-WHj|y{tap7&in>?&XyRd_JXZ;SzqQO@@<l_d3;&tM{KrBV-Q`z!pOw@(1S2aYK7Hfx#B?mZ^l5t8Jms#ZQz8B(oK*(=?-MeqbE)pz8RwE>;lL&F6>jw4X&&s`h#Ut9}zixv_6Y|hWb7CBCp}|>-BCYmDAKJHm2Xq&0mgmZ-1F>*1M@1nEfq9Z?W+_<>?Np3-U2gf|h53AX);R2sXB0BIE?c@rpaRpMtmS0{trr9>{F?ZWFWkPgCjn^;CYZ%YC<HReY14o+a08Bk(6P1@R)hni=U?Z#7f=Lj#>u!S|A6JeyaoE?nxY7)&8lgvI%@AGn#q?2S;dXNc67jacsoCfZGrl-sm)ZYU%Vn$yo;izmv3!*$6xqBnyb-lbr*60<9i7VA0n$Z6p=pX7{9A5e89D$n{BX;zK<=XxN%VAtF(!Q7ui^BeK+HQ(B9uljC0*1r#ag1E7>N=qC3_k0<h!<QeMx00oxUXYD=Ta3Tr_7fNOY4a31?vH3<lrvz4mBoz?}@Yt)vNXlUpyUYX4&2;$2XrJwYcTOFXVN$ab3!J~92z1|W^2VpL9bv}FT@F}k73!5Oq5WXeAP^L;1m>)0RzCN5L(>lTgs*B5mF9G=TW*+lzOQ3Ie>pHvilzmxt4J?s(x?Vh_0%n63atec6o6fy@ATk>~@P@E|p$;gjT3ypJkTi4moN|qjBhblnnAW5j5?!QM0C61)1~xCM%R)r(5B;QXA1YIU3ie8{-9bx<97kI|pw=|<!q8U(Ca--6NhrTdj4zQANZ~O8@RuVytW|ky1fp=Fh!n8yo3L(S*Nbi04wmtu((ZNC@e_2Mv8N3Bp`yb^AC`8Srmy;QM@X~IH0g2mS{EpJDNO(JNEplZj?yn@#(9=|AM}kjP>QZ$s2{eLi_ok<60EnU_RrIH7+8ryM68q1IYIc*N-6+h5}x?4;TH-{^R~{9*S~vPG4K8<cD4J+n)T_77@}^Vxgq;AxMKww2rh&lE(5WeB(r~?`J|bYsY8Q&GP5FZf>etonf+qwA9hq;#Iz`AC(A#Ji|-z590*l@{M7G4WfE3oz;R$mUx~rmVB^Jy`qaTp2x}$u<SB3^oRzP2`BYWKeV+6ue_!oS1n}R9sB|k*_XQH><6IQ8;3k-#bkkdAXI5i!Lz9bBGqnJ@A5{~B76^j~s`#ISPKEO{cA7?l;l+2GTBSqq(?1Ih&cDMd%FD~1u5#~b0{o<y)4vWu>|s6S_}>_E9AXBN-Jc2y5I%YfYdT!G$0~}f2yF1Gzo<tA?9mIdX)6!$puQY7w{Pi4L#om+WsZK(Py%~BY%=-hUdTkxn_0t<5{KphNFNxyB6A&@nOJdk>CpK*Tfo{`5s{ke2<0z}Zi}XrhewJoBl!2qd-^^FWJaFp(g(24j_(t2`eJszV71qzO+m_?L3NUHr_17JfCMp#xhi#=3ewWS#qKN$?#YM2jf@fspbxj<*)*lm@G>=9;02TIP8EQvh0Ln*fTNLO-4tn!Z509(X0mEU@`m2jL34rQI^KksL6nK6OZEsLB>}@CToTRJ8dN4z3dxCF@zYFzUO@^X&`hbyI{sjl8!E)rit;X(ax@}lX%s<{*ry|&Mpw!>GFwaUnR^03rEk_!SvG88KxhwGLf%zMV^{{^TP{W1+^-q6P){Q_RyYzq-n4QEv85C?SU4NPuzqK*{ZrckD)s_%%uVU3X{xml{_KP1ip|rnRH9Y!8dQGrnACko_fypyQwL@3o$8e`^j4^q3>vy@6^5>R8=3=3pl*Fxk~yp7$$X{XS~K`xtM@@h>jVoB%2m!O5-&B@`m~6=xIKusJ<8spv@jjM^!}Y2Lg0Y$YtGc~--<(PGylIZfqsl9xbckx<G3j-nF9MpE5X`yweJuKF;w~j4KiI5?q?xaKmjTGo8@Ck9tp5_D4@VaCx5{Ai5iTuh&y2czcRpl>(H5tH;?CpJPwA~cTFfiuCS|Kmh>|#EhQTv*99zD=}Cb^ldvGu9VG5;fZtP%W;|&pjtrTFQ&_)q#=bTan1cSx@GqwY!VguB?Z=-zTCc80d7lx^z7xzurw!PBW!>Jp!n*9i@z|k5aAPM;Qg*oyMzF8rg8Ow29z9WxzNeM|aYj%Z<CP8>2X?jM^diphmSV*C=@{WtYXG-Tr2Ot^ZT+3T4xpTeyk5-Z1tbCNTVV410$8wDxEAf4q({lXp4nslJv5r5=Aw@$H@V(Q<3ZY6ziBFbPNh6C-n22*2fbmzG0$=osi$wmS1vqcD8bVL{uPle6zK!hTt|%zuT?d|n=k?9z$3=^lzGff9~lv3u+w)endeSTbY%JWJKiONa%cw$J7pf>fbn7D#4y1V&;sT0Z36yGro*AlRHg$GIp#ENTlxg7XX_turxnOpn=<|VbDD(6dvkcS>%%8|u_rou?VQq-@vG(D<3EI>T$xi6wR)jbM;8Q?o{VJ_s24o25XTm><6nBfZ1eEEAZtVf(NKY#d*XE@rUw1E9$i->ENV`%WMFH&#w`%VqF4780f<A)Alx+r2jmHg93<=7oogkiy2r7_{MlNfd~2QKHgPTxm|=f$UqACyJC!<Xo7-Fsf9kK~BVv&piy+e#+|sI5Ny*3%vjuTj3uG^cw9HvV2#6gwmN|kDPGtP!vjXXi+8(n)IBRyQ0Q9&Pxq@H!7Ha7qaa>p6mm9|)O%VsaH$s76n_?+W%3=o=O8i8F)E>W^WOVUR-7D|y!n&a?aAEZEL`%IAe3bE)u_|?(Y!`-90DkUSfk`v;hQ~$jiIiQ<Zx!Q1g@V2QZKuis6=hL$bEE;K#-ml)vJs|#f9QMR3}rkE&$Y~<7N^-d)=-MjPwxn~FSO$jtb5T4ccO~zrIQ0Z6JIr$E*rdASvBC(#sYK*#4ouP<mrIE=H!PD<R>2NfE1A_#ofy$f{s_`F*FMl3ps74jxFwno~hTgLr63VH>d}-+Ax0^D74CKw82?RO*qC1B`pNMF3ISp%r4nP<+1E8Gk4PjPUlgY9pf=FMCEGrcEoeuGc8qB=<;DQY1HS5MSGQ`xVsHZze16t$vwcLhdP$r-%cBn;N^E-t|#3HO8edFaANc=`?)86w}YODiOAOjzJScT!Kg#bS`QeJH08%579t9p?cx(Uj{BC;{_uGxn@MRq=F<>+Xy&cNO<=Z-u!tkySB$kw$*t1L7vUd@8^!3(<#}dV!I_HQ15YZ84Z-;{ukOb6CjL%{if#z1yuInxd+@z-a3L?|LDUAwM4`ujhG{p<L*&x9?QQlcbEm100$jJT#F5Vupd(igUa6USNrFPCi}}*oyeS%b1*0MmA~nPg5c&TkpMQoMeA)yE9Fq)vhRFzb{O*E5_#BzLYp*K0`q`X;H%{k7ibX`>tuq<gbpPOzRu)*K>966GRu`)J=Y-q~-q|yr2UI=T!{w1iDJ6c!H<8pQmjPnn6nxG2R18X5;B!1JC0H4xK;x4>%POf~YzEUVjpQ(LqI4CwuJOfbG~vmu4-gLSQwGB=6_z;Ym5=FLxjZ93;#%Tb<$XjKx_gH!vt)vBul}M#;NaU)&-*%<2^`xNteSamg1cbXiRItd6p{T>3U?@U(XNkXGW4ceXgE?L`te1{mJJx*PDWBD6r&!@b?9j;#v$=S5*@^UPW9?q6KXyFNQkJhh<Pc=Z{#@C3HX!Ux`W;0YYZ}Kx0qM3BlkrkU(ad9elM+Ef|~XtvP5gn;E`UMyp;bIQKZcv(BdEcIlNhnFX&blV{TFKs}!cwRNV3-MJO97<@UKf=~>14X*9C2a83xKKDQ!S0L;6)ZXQ_a{U#iDPYqn~Kwc!hr?W+{;#}~Qn*1+rh_ftuJPGWsQsA`qdSPdGsK_cuKahZK58#?nOge^dPP(ZRurmMWMTdD0i~@>*zctke`uP`O2N&5%wY^I<5{&6_g*f>-N~5(NA;28Q;!fSOSlV5KspiW`^))Mrk#Iyl{DiGEqvBYbm{n-E_0CjVpGtNuF_uJZu&REU)Fa+R@ztxEu0A{>gJ0-=<@A`QBh3?$pRtzWB)LD=94!%IxydU{E3ddqAq3;a+4zW~ff`246@P0qRJrke&b!qvns;7Zf$pNx?a_aBH?3|{5YJ|a1t_2EC?!)Ar_u^{pYUoOu$Xeu*TS!EB$N7=cpr`r$SDeESIwkcgCUz>9s&xN`tt2zM8Wf>wK)xx)`NV*<HkyBM=Z|qzN>3|u(c6$t1QS@G@V$7*FAuqQ9)|3Kj7(3(Rp56__vV$SY6<|64hamc(|qHgBJ6&uYHFdgUOYKmGX9s+R*}g4wdmdC6jgIoDNeQk~ge!m<>e&)~Ti21vgqx+h~miKOLOLWTtjjaoj3zlpOsCnZ?_(h8Cvpu9pwE=!=8oxx(VwN{Tzc4?YDkS~boa4-O&*tn&e_+5CmG4*+?{9I<CLOEFhHh5qqkcjBNxx*F%irP4vIA(j+-o-XXLlaKN{O4xpFP9*8d@W|e&TjC)#g&;sw0UtFQ<(tE^=69@}qzH`JU23DMw#tMg;iy$V%x*!9L2+GPmF{&{G6rM(5=6b8mv3{AL~u=6?zH`E{JH&Gk&Yij1+q%Kx(6N}-BL_hq#9+{|32!MdFHo9x(vAuwTr9JHH<MVbY$axJQ~k<QK-8jTo`xXENax5N@3w96!VqbrG+Mk%Yh|b#*xpUBa@0Z`qgsq5vS(2oK4=yt+kCi<V?+hRmdXA_acq+R1-B9=<)&&AM?GfA3V3djy@jg@xw;BEZ+dX52H0Dd0G!r$F-yk86u<Mx~IM1A0H{vwR%pNJjiE75JC<!x@&H39v9Q@N2<N{@Ssz<X~5nUwJCMB0+(Qy>UCu5`2vH^wM%MMKx1olSzt!JnkGs(EM~$jsf%y5@irAaQY~{iZY`KOq##*B8#&7@0~BxwhZxNnK`*NJCKT@q5U4cHn%3Vujg5_g7IDjgY`E$XVs(Jp;BsLdilgJ<W;`v)TG&6D!qy&Ya+XcNA`DzP;g>2%i+7R~iK)KdfEy^pryWry6|9CX2077^$cEM%?mp3!<Eb>^Ro05Z&=P+zXp-8!5Y(Xfqrc_yV23!O7BbXj_q|(^zE>${`XHGZkJDC)7PCG~NhrB?{Jn6m{+X#GVRNv4w>xNPwUrnrbbXBbe>7+0VN~C{a$1H}|6Y;y@uomH^mh(9K`0{URG3V63i?MV?$A#922E{QI4s5I0eVTI+CLWtorCvlCo?pa6R-|A-2{2z&UkXeGQD*ZS#*i}I7eJ=HXi+5(4mK4#5fpkSnCmmXzZhV4LR5L^aLD%t^xWxc&JT=@!>+|tMk0qW^8sKkb1-yQZQ5hOa>fyj0L=rlMzy9W$q^95Y(-(yI!3P;?szyBF=W|8)o==8@p}FhU{)~r3`xT^g52@5N!D|G#K{5LPuq}J(hJN%Y-Mby2m%=opH54bd+SjTBj(GV=t9P6w#;+E<G;|q33<4qyBjoEM&U7;6v#evbsTx6VfQbeyxO?V}BS@A2jwmP*Dj)C{NuAYQ=(}&>eczsK52nWcf3I1hEQpNXWClJr39Ol4)>l5+G{=SChr%?MWEr1*!5CV%_W=RnIr@ZZX9Z#J#&?4jq~qM~8SIw4a&q41~ycPsog)_!skNN(~vgks+*^se(YcC0PT!7!5k=q{$4^VGKILX00>ql?mShEi1gL`A_y@wn>MMpX)b;Fp5NWN6T&CeyE7NMLu}$gdoPB;6>XRG$M3MX6Q=Z>~T!f6JLxj{GVpk?qXG$pzZT9bbzOsj4{h!7RIQvz365yDXErCWJ6<+he(q2!38QC2&W>g8y{EDonpPIi#sa58k8mRAuK7X2H@R3$uPRD8E~bQS&3lxgUnPN!59<6%r4EE<Oh8yC{(KTwQ&fekNR<%b{5t^f?jl;@eXq@=~^n?!{+Ajw4F9zGkjoikI=rFQFxS@>NyXNx>BIKpx6H5m8u?y73qmyoo0jIe@$dYkuw4m!$elMnnd@glU@%?8nf}Kuwl15i6rYlCb<Hk9#ad~+Du=F`WU26<5zc_YCPKU9#!u#MPd>@2_0A4N5CX?eF9#{Eac{yhRIH#RJTiXG+ypn!&8+h#v>K*+QLK^!*{%vYaZE6`gs693Xpw~dQNUYA`H2Bj(YJ^pTUv!^twYGrV=3oO02Fv?nA+jLbVSIv-G(wzRHu%#>mS*0v8VRD&#(vYMc4xOTHUTeNH&_H2CNPB&ejI<uFg)RO+B&H6dEm*y`zjA^oJVB`)v8XCvA3Sg{RE-6VWk?djRPZ$!8Jy-^T0q`P=x%V%-*Xm#5(V?1kTubPUC2fN+D<y3`TR_mCA-*@88CUx93kvg$vBxMVGp|}ABluQmK>+4&MqsU294*gBXIC*{wXM(Rt=wBFiAMmz)^}OE~2^@y4NaR@Q6`+zLXnC;|G9xa+w>9eA^-w5y70#aPys2qFlSn#t`J5;ilAKW_Ys|uj>mPuBk0afVUSu`7vYZm!74P;kwuBU+U_gacZ=5!%Dc7WGMs?|#+bksgCK9TSm0&+~Wp*Pg0O~1)&ZVGY;<pghKW-#V#s*TV1D&Wm?@VOj&pVF$Xb?26hmJ765Z0>hU4<Ka9+AE{)XmVoSuw&&!vrv+$sn=?c|S|0E)<k4U@y(!S=vGn7qHP=<MYMhTJU>dt2rkelhvoW64{a}xRpudb_IF?nIY1qmO?IGPHagV+IFA6M&{}Dppy3H#xdRMA;jU?p6V1RlJZ0D#Cv&o6E@3CuB0D@y#V58<66~JCHz{M(gH_YMJSwJ5v5(`M<2nU77?lu$leef0LbPlX9GGd1m_aoO>}v*C#kT)pqEJZv8)mSlttw*<R~1`SZK<fNC?0YHa<oTq~>866`xtojhCupy`hHy+7|LwdkRuD$l(Fq&aK!ImQ0$S_^*gBI+Z_}F;gVD@SZ*vvtbP>ysx*@&r^5tA#oWV^xJrec93!CLY<;+CI(N2PM#fRQZQ@SGrHxF+u(BiJdMJ(y>=D+gG~)3(Pd%i+t!#vn=<1BQoZ;*xL)fqpbsFpgc*9^Ed27y%>HR(Ik{uTD_3;{Oc??Mj>RYkumd*^a(r<SEyP~-V#I)gX5gy5EiB3<9QbI$JmB^y%E=BUYzysk1LS{t#j+m=Dc8pVI?21a{r`2datP!(#gagRA>#clJhS4uHQF_@wj;w_>c=Eu>I>L(T=r;~HvYMnH6a)-wEWzE+i32U#Wv6ElJyAVnqcEzBoa`S7Biy)z)s^&c*4;=roYc&K$fT4cyB`rYAY&~C{_K-UH3N<Lj2>RRzas|bzH6)0llR8xUgAwgxl-+#QGxTe9i?>OBEK8IMBVZOkGkQa^i@GG$}zvRJOcd#VtpDlUmoWGO{?cpj%xzIb8=0Bj^9$tC*A6$a@NFu2^8o2-3;T8<v)Ik5B^i`%};SI+f`ri9%?I!Jjrz^ofcZ#<LKn>s^tQ^S$pN$qfa0!f>I;*r~m0rPgEUBEk-ZbHNvjOEy&G^qqBr<Au6DRbiBu;4+unG%;Q{s0TyYLF<hQAx5#`wHg=yybWOzNUJt=!tZfCHNG!-8dZn*4)2=~bVvlxb1?ted7hJmjB&1?8=3{nXiYqOr5%!T(-IZVqkBs#i<`}I!AtjDMl5t{+BHtie;#vS!pFW>G3bSssGNn>aWapD@bs-b=CDgfvA1}^0V1O(DK<IQzlbf0c}c`v_rpaN8ZlEH+mTs^Z68<EMaA)dcgNDzG+Ogj9=mUHa~uFaeP0VGSaRL{R_uXmqKvHeIHh)Ajg)2E8ihWwOxQY00$iz?%e~pFp7Y#`@9nHz^De9KACong@21LqCj3+g2}#`--F&%HeqP{fpkeZxC|e2QdJI_$*Vj{KJEt|B=K7Ok>N`r0xIEdf<cz?H=0rxn5B9<$YVuGgzOOFNW`~%&#vpFS>8RK7LIbWc2BZ?Y7LA`d{iFZWIl)B_c8|MZNBvkqG{lzcHHHnPFu~X4s_uOy*tCaSLX;`L``DV!Z58&!OD`(31>-TyB1gjfo!3*dwZ>9mFhlNEzLWCmJZWs~)Q{JB{pV4<y5nH-ZE5R#53h8_^kt{s(){6GFMr@6Nd(d&O_&mNPQK};(BBiL;o?KfNlrrbEh_c~8;>O0PJkGY1rfuga%$cIPcACjCESG_#-s?qXgSNX)}a%+(07WU-gccm{(h)iWc%pmez7gIjfAkUq^U6CxnuQBYf-{E4k|Syk~z3JFmOi(#*UuG6&kHb1V8YZyUI_BI)z98@1aqcXY(RB%6Q$}Jv=#*zW49atO_Eh_RH!%HCZ!-T%17wcV?OJ7wvMj9<?+Wn-RC}Hp`FT=UG-Lx%g4OhmR*=(Xkj+h<@%JOC!P~%P^_1(~rjrIKMIp6*||C0MaxWpsbURX$TbrN9;?CyWe!#)QG`(MJI$*y5Gir+-2ZMB>S8qvDwOo@01{tdCHTw&hVM@vcZd8#ZiW&BKj>uC=8>$GlYB_=Lqo+S9)~iOs@tCJ)~muZ5r*2K_MCu*DD%u6Dj#Rgs1cBT-f0yKI>EDS&JlmGG!1qH!Y>kH-8W^PDk(0ciF(Pbz!>3+3nn5BpaD`;nUQC1!`&zp020hY(i3Kyc~dzQ7wi9rbSs;WFmGsP#lYXYei+4adQ%Kf~4v#*7B&7-o@U%sR@5G`$A?l+*2rgoM%;fa`yCXmd2}g$x}5%FnvyzOtU`Ngc(-A@FVCM_jRCPiJ+i8PDh`!(xtQR@8PO4!qO>~=7oi_xjuA{JI+>+j#>3VM1{v0jssWzItY&MQO0T(ATCXe*laj8xEUbwkkYJ5EEh=w#-P|5a6U2*v^5UkD&kX&Ex^LZzib&?U5fW=Ol#8qxb3qCkADObs7u^a@Q|U^sbRfh(hCk1-7E-7Wns#nu>oL$LH(|L=KwaNT_47&5`^CKv7ERlVrTciOcdaX0HJR}(>dm#bx=Utvt&A;6A|pO0YE96oZ&Y*l)RsZD?dlVtMB<!iIe<u1#*&<AwZ+JU$~ZZl$=+%JxJ<u=ORQI?k^|sOsY`ASD%$UJF_A@62*gKWSefymoU-UZrxBC(2-x0gsO7d>5Ian{(+VU;G$2Af^XVaR-#8y<R-T<h6l}?W^|8BVll4b9KsB&E-NL!?eIK6x7#pm4l}dFn=DCMp!LOwFKW+t1`Un(M~i6<k8p~zSg%v9<lAL2ChJ>T6;7?Xm7jczR09|s)1sMO$E%rHzv&#`u%V;g*AfM>rzC82un@WY1Eza@w8a(5C2iKUiPP>*C8Gy1l(}fmNMpOtmKjkchtC*hc6KNWos5xNDxbEIqCfw_*jA%vXj>+8X{t_&D{3wf;?Sp+rTG_+hU;u6-HBVuwxa5`@&_n@86=UFBH=(GmN5r_;uugMYz5>E@+vMjVc9^PTOQ?)bKB&LSij}I1LWCKXg1yJnkR&f0}0XqYC}+J;c2;x&L#iQu#RDbq5VVj4WY|49b<6N;+YzR?H61dZ~)mhIz`J?R*X!1bsF)s_2o>1#|{X%BIFkCYB~ln?fxfu8nY^2LU{XVE{8M6RAJ+@l83c?vSQEHL*87Zc{Yj658Iow;QN=)FwL^-_L!jr@i<6zF!~68nElc&6eHkd*nO@N$tO*6h<iaS*?>ZTVT{>^!!~en6NnTNq3XB(z3X3-?MGynbneyo3d1KEhBz74^pidG>RNt%bJ_^^1ze&u+ywy}1dn-ZNuiWM%j2>E6pU@-u69t(3w026lCK;tN_FnjY&n7!)W%U8d!oy~wAWKa==sptk7&14x>;b9(=$ONZm)PG^JjO_hsBYBcb%{y17uk~>y9(INY<_~=WGCggTR6jBfeKSzNk{Mo*wZO*-*3El}mdq%z*by?6~bVFC@@_Lm7pY9Db9SXoidr{4@Nxj%)Qe4(-~RkDcScrk$O^Qo+YDU%kvcMO}z6kDS3sK#S>i?an3m3JtDF=Ci6mVV;(})g)|VceVJDCALVQsuqit(;xl~%D)#hR-3VXCH`4h0Cg8z6(W3v7b?l&89ieK;Q+v{DFlLEH4fyG>j4`H)n?b_LhQJIp({CiICn)O-yUWICMwT*71WgWFJ@r!kuQ{jVIcPCDMrZ4I-?S^pMp-SpIhq}U2wy1NXzxvjALQ_RpU6fE2|Hn8^pUaAj3qK&3T?Ae_7^%PbZvS>Oyot{zpZ9aT%t}ti1e6bxu%b3}9Bt-${9+FCQqYaOKA=u-IgK`=dZsa7#=zFLH(Fgic=Qo12BGA{IQ&aNLw=PL!8(khwXGa<4r_DRv-*2SwD6S~-OU(HO>bo$$*Dg`y{oI=7j-PS>(YD<DHZ>@3HR1N)+w^0>io6<#p9L#mB}k5;8J{MlWU5}OY!3@>5p%v+k#1{&1LsCJ<g8I`+8DXfIkL+yGH6`r#&-bQ4DmN=TDZF=Mjqdjq|bd^b*C)6A(dVDuc**DK41Ohi-F>Kmn1=C44rj7u#Fer($D<RP^?!2R3N0aR*_WzMiQgi?w1)iv;<uHT_)MJge<DgBR`_9RvJ?)fi?RG*Vz>PdTpQ_(4WjaFqb&Q&AEQsnQ(-t#x{!NE+)Hav(;M#Ahyv31DGe)4c_hS68t(89ayNF&mT~j0>EireXRjcW^+u4O#8NEOX9yuRiEY+>4gpC?>!2^0PLJQ`@6f?M_MF?`gd-R^?=vqkISB@RXu%U~1fKh8qWcdoeZBAq%E3r?w*0qor=Yb%rq%jds?`ra=2vrGo!!=5julO7ZFMNtHKW;pwWc08!SlcsW@#21f?mJX@46*gOm+sQ}U{C2DQ8?ka>KXzt9AOU@^7f+1DpCDGe%_EKVn)Kz2si=^^~zHggc0gRF5kOo43tNzlzATI@Knq-tbQrvm!n|cw~#Rc7&6sx@ziuf7`?IL{<tTSh?1f#u^C*Jip{6%ETVAS_S}&`$?skT(s}+drAvrV={d}Ur}1vBZFb!}QXX9LGh4wQlA4~lfs%7_P${^NDtjuU)6mbUH{Zwc-r;*<5ie&nEPrJRfzLDv&to0k{ooid>CQ=n_#!1d*c*z@pqt9ZlWUBmdEJ*Xn1ombrydq`->*i=_zjzWnMxmWjwNTgy$nw<nryOF5tlfyH*fh4;ZyjOHSKzVjI^8P9&8YRUPB9?wj;}c$OuXuyQb~q<!Iqb8`>kqlKxuNKQ+AHA$KJaFnU4VayZ+0U5b}$q6joOEa5~zm2FT}eoCeL2ottMPq#Il$h!gNtekpzBOI@jBm-onG$$&5QSzS{<)sWOqCQ<4DHM|pnWpo11c(Mwp`oOa<=l>MJQmMtncqQpfOp#P6MXG|>*mlN5nvZH@08^#jRVqTMJE6I-D^!6z_NuJ+Hc-bAa|WpD4ra?m#bK6@*MUO&Xm2Wwo)FbZYIua2`NR{)YPO^o#+DzJUP2zxqhWSm=6AtkI+T-J+#KNyz|&2IjQ`4^omxnCV9lq+J^kQ*+i%}AmyuwPT7@y%zqkuG@dX;5AG560%n8VMGC8Fw1Gg=E8?=w6W=25poO<EM3@TucH;nT6Dty*el%$(kkKcQ)UuEaO;)#7x@Mo>9nPLjT%+hdcrAv|*P3Z8(Jn<q`d@%1+_@g#XTe5Ao+u9H)kt&Bmbi4Luus&;!&PPsTe<ng=A0z0Eqw`x@(#@r&YPn7nxQ=gBsuGY87J-N*Hp)jD2$gjEUfd}N}DN$A|N=rFg$YYVI?4~wMT1nBsbu!jqfvFSkHkYHV;<;xyyKeK9ji_Z7g3O72{KkK-{7lXMAiZW}v8B;J9r=`%$P<Ut#zRhdkr$I1jAsHo+(RE6v%<Jh-h0K~?>iqTm_;^~MhDiG9&GgL`FK>7{tL;d2wOWUps<>6g!8&_A1E5&18V88D~4a?O(C--X?$g$_lnWe$Hmj5!4HarE5sqGE9to2993s1P9`pl8!lPm~M5+$9Sqqa6CC!I9L<dwDTaLrWbt<Yi0<3dQ>~Pu!AW2@WcH>Qo0eM*EI13F@gQ0JXWH5;zf=itk=fs!T!5;Rd#@l5%j1p%0Tu^$UbF<zBL88;8Ik_W%|ap`L0j2717W<^mgQaujTwvkS})<UVk9T89ChqgkNdkr{WNg?x4tIbn^G1Mvtn2#V^&p2YF*B4`DypZ;E4*Q&M2sI>6MP~`l2BDZWFc;#>Np4e+rXz0Xc_UEBt@jI`2&(pzoV>{4&aG;s^fbb+JHHa4jDVsbz>ql<5qbMFbkDgFi;z)itOjq^qdS{XVp`4`QTi-nh@xpn>6|8Kw@gfsj3`dsTFc2^+;TX}FlE09BY?_S5kHO!b(}24P&ite-#i@@Xb-#PHm+JfZ$TN+GdTR@V3^n6B-Uge$v=xIH8_o8<0(nnGP^`>+?dEH|>e)13<G_@@wMp%!Iisy@3caPws8$3s#@*>uy3?qj@rG0xT_uy0%6Y5fD1k90wx)xhvoc{sCXI!jDX41}BxzfICTErP4u5)x52K9ocKJx>VHt+17uBOL`duaUp0yu!4i8r-X_BE9m8CuI%@D*Qf(1drufE-Mx6d5kvoQCGf7DjZ*t=#Qif{<Ef^tRw20-Z%Yq8lbVeY$FOSM9fKd_4j;a^C)d%sg--3+6jtllgGrprS}@NURVxi=L734_wcI3eyy1N%G-?xY~QR^tPk+Ujf9@1%}Niw)|YOa}IGzh`stei|Q0FgIsgQqQd?@0y^)ubtzqw7N8sO~OIQ+*Pjy`MTAz9#+9d`LoR;=p3wGiMh)eW*>09JK*SWz_6*xAaR{h5DsYuwto@q70j#Oi=@sgn~r;-ZDtZ&>MQfczYpNdyi_W{6tZ;7p4XNr8MRiWOQKRwN1hK}2vURjP_75mZb~e>YfK{nwdG1E)`0Q7P>(o7%y!kefpRWm#lc_S($pHmVq$a(c4PxVeHjC{5$Y;*i`Rwwxc@}SnnTEr*&X|)k1&y|Q_39pfazFz7WJElU`51wIEu7x`=sau@W{rrEpT}X1{v9yk@VSbh-EvBBO_yczCo{?C^@YA<e4r{HEi7<YJd4~uP(5)WwH|ewF_n3O=Kfs_&Bty0R#L+<t4(Jvm19q<f^*t(95K2YcA23@-~h<E!Vy#?#CN_T1>;7DzuyNomqwH0IOEW{Elwe%qA|6|Amx-Z6H4yW_fghF#0Mk&0x;v{(NE|BLWB8!H~kFaJ-DHN|V7$0!kXzfa>&|xO1^nnp?0zCD`Cm{CV4(s=KZM?om}G9RDl{@kP<UDYgLkLmF?^WaZjoLZ#v~CT%~KG!6c3;~S?Ynv=PIU1y^X;QBFru{Ri>w$!7}CQbTf8lqrDOldfW?t{e;XizWi)k?3n^O{pjri6L4c);&q(H=K5-xa_F^1dayh{#xM{=%T9KYU}k2@N?^A(suH@muc6joC#j^X8yjsvVYy+&wtk2wR#UWBL?^pG~<^mwW<oK!5B-O`{FbNhwM}`-I2t{Mb1<Z^;7G1Y7f6$DAPUCe9NL=Rg<a(}bJ7^u^ZYRP|)hZ7by}AY?DPO=<r`^v)i8F92jo>IK=v!lF5-aqo1ZwJfsgEwx)P^e}~k9%%vYzgNqg{8poPgiEsd`^sYh-cW}Ilw~mt`9XeKv#{V4_o)&i_Pdw)kN4p`wMdp!R(3bRU&`^017$dFy3Lpm;IquX*+X(Oylh9*u3l0`^N2{GDF7a&qDtL0VH8F^C?5|^IA)OcbyN7Z6TTmoAaFR<ZFs;)+ZgbD)sX1e7+O%gfr|PcWINP+Z9V+YN9IXBM9xdY%K179`Bh;!{)*g}hAGw{*X55GKp*{IZ1ZS}`s%&-({{rJ!D@dOsXES$Tdtd>Uj;vGZ4a4K7}2Y#&U7kS0=l;YQ(Q$g#{0K~`3S|vB;u(Owr;jX6d9<hH{eI&+}^oxvsB`*?_jZ5s)K}G8=4xCbU>|C=n}PvPkT}B)a@Tm|N5v!P{G&O??X{2R1h~p&-0#~xMYm~D+Om0+XlA#U8PCOVC<eL)-xVO86%Htt<}i2xzacw*y{f(ZaX36IngX>u=8EdOl9AK)fr7!-cDn^%P;<o7xNRjvc-3vu3`#E>zjhFRiCBC7)EMfR<lOI86wjJUoQTZ;aU9X8EWP*i%W!c@ZfH`pBY|3lig+spQL9{Pbnbk4_3JTYm6eQXcJS+(lSIH!FRY3FzTV8!nKO~>)20d(a>`a^!qh`QoJpfTY#uEqXZ1kxmqnGo)G|R0p(;_^ygN%h-FAN$#J91TrH5o#c~dG85bZ2v&>#tT530Il%MH1PWuBR?#G=IUatuKFQM;GI4aQkr`h1?QUh`4w>Wh*wjk#s>_27+0{Q3xL0wbPg-*(t{UxWZeS~e4uG^mUa#u|hIY7zmC2vS{QG2n~m;0|aeZZ0&gCs>%SM$YIu`F>@@eu;IX-)^nUZrQm$3714LJ?1G-=g&lhi#pp>#G~016_!`I)H+Bz1(pq<0w!R-{=bjYnV#J-BAsz4R@SqNcty_?Vh7!uz^a4BSbEGggqg0WbVW#bMQxTc>@2G&&zn5!Gz1cF^?CF_F$8byC!1XiK0cLZbEoGx`7UHTN1NJov$x3LqCU;V&xKU?;#7NtD!43=hGf58V{@1U4Zj&Vred9zx*&ODW<OU-B+|fcPeW;x}up%qxJ|3^A7$~tod(@N>-Ho5ld^%HrPHBFu5AK<7gODhCNAvZckCF_MmjY9qV}1r!$3oJtcXFusrOP4{TEpYW$ivv$m-@S%T~)t}f1?x{>A!5AVVNeUbV_`qurFDhyzS_KS(+d@fk$X9Bjtc|4p}*!e9wGS_pZ9^G1kqWxziiI*<+n6rL6I86p$y2V`aZLZI?PQ*v``mA;f>x3073Bgqq?=Ge{8K*UYZCvJO!i&O&qz*#laO~4U8T(-p4bvQ-nSzIU|D1bhuSkG&Qy8T5PuEJ?0ZH;#NdSj7i8^HRG2kI9$gZ+$f*R!g;+4)#Zc6-E8d4UL=B~x(4$w5Tdc=d;T%giLDT@YCd$QUGBplqhAF8$}BBNOY09$m|&5k$t2l7!pX2AeFk-Joid9((GY6X6Ha-<Y8L@zGQvyKsjKK<M$PMauXNyp@3tYc$hC(5E&`XVqHtT}7+j;^7Bg7;2pAJ7f4KKM@wUXU0pn;l4EZ<=S&U@l(Y{wVkV5;Q$S%NU6}iKD(SaiyM^$6w@$Scv8rf<i0qUId#d8-CMb^<wQW<s}N<zG%8+dRFzH6U?4-zL{qCqyUz2lap_F3U;3;v=!(!FLyWSxSCCZiAMrd8Ct-ZzU|l1KfZ`PWQJ6~BCrO?mB($60PTnZ;fqp^(&fv`)_1b^Z}8v96+%xZT+bm(q+ThgMs4a4<<Ow*UzkB2n5e)$e-zKmiltBd2pRsEFgKd{oSe?*p&(&mUkko&KRvx*`Bmrp*)x(@6o^!4dd3S$vxjW6^#z63H1GTetKsq0B>Zd6U=k=k_AP!RAzkY$^Dkq>Y{NFoc4VZEj=iO}Uoj)Wmn5e75}7Ta!3@nz(j^!=WXm6evTx>!e<c@F!5iLXqy~<%>W%ZwrfXao4-Sd@B)(B)Ze2^8bU?VYQKD5M=wY-s2iOk_1&3<o@}YdcA>R*laMV}O10?7``pERCS9q+z@=vr+XUC((rGo9i0HwuKK5e1S4ZNX@<cNagp@}bCqkGlOF0AD-p9E3TtByVHgi%EF>8VtEabeYr!5t}ZkQ-0KA|I$ziM5F*jgoMQVTvFjs>3LOJTGH&DsiLwF%!NJ1qX7eY%)Zn$f625T7_Vj`W!KD&Ey}9ohWqL61n^|cL4jT@)hlb({Y>BCQXWT-AD|M+iGjf4K$lam>4hE{pF{(pEcHI=AMEry;29+1T(Anx)He?Jp#bPU9!tvRM_lyK$_Qdj*~zaMI!@R%cVq!Ri*pk{F<b7Q4yRN0yiVz<giDfQVlj0u2!^HN>K!mXA#g#8PivWU<!d#6fsf$lBClSOlBpNeL&z1cg3pHH??L#u#tLgI`fI%!V8^oxDLTnMvDfUGKzVjo9H>2?|SifSm_j&fM*o%&F@Kx0YqOoBFN<sPuMCr$7nDjLWhD83<WFWAf*xI;x50mIXehibOSx+VVm=c;>3HbtaC-7xf!sal1}})00000^|8T*om-G700E-Q0-%}(yzlrJvBYQl0ssI200dcD","encoding":"xz-base85-v1","uncompressed_bytes":101664,"uncompressed_sha256":"2b6edef0cee4c9b2046656217a74645417445e3726f5a7db80e6e17d9bd935ad"}
```
<!-- ENDH7PACKET -->


## Appendix U. Measured ten-column compact restriction

The parent's measured production table has NCOL=10, coverage 80 and probe limit 85; this filing's table is that layout restricted to eight relative columns (Appendix ZS), with the same bucket law, lane tree and read path. The parent's records occupy 10*2^19*30=157,286,400 bytes and one 32-byte terminal pad; the eight-column image is 127,926,304.

### U.1 Same-bucket and ordered-output proof

For fixed(R*=8174,ustart), the ten-column covered set is the 15-column set with relative columns 12, 13 and 14 removed. A record's updates depend only on words assigned to it. Every retained record receives the same cyclic ordered subsequence and keeps the same first six words. Compact encoding is injective: each lane preserves all 32 u bits, a carry gap and all six field bits; the count is preserved separately.

For fixed CV and a0, main/next addresses, row wrap, predicates and lane tree agree whenever the relative column is below 11. A probe skipped by threshold 85 can access only omitted columns. Thus the ten-column stream is the ordered 15-column stream filtered by retained columns. Column-zero crossings retain their row carry. Trials 0..3 compare tag claws against an independent retained-entry search and C1/postfilter flags against real-word definitions; the full selftest also checks 2,304 lane cases and 16,128 tag/C1 cases with zero mismatches. Fixed R*=8174 selects the same 80 absolute residue classes in every epoch; the strengthened per-alignment H7 and the other inherited probability premises remain assumptions. Parity is finite semantic evidence.

### U.2 Exact retained census and useful-pair rate

All 8,192 10-column totals are width-10 cyclic windows of the eight raw offset arrays. Minimum 29,617,909, maximum 29,708,804, sum 242,952,259,320 and mean 29,657,258.2177734375. The same arrays give the 15-column control 44,436,632/44,543,396/364,428,388,980, the thirteen-column window 38,510,323/38,610,389/315,837,937,116 and the twelve-column window 35,546,342/35,641,736/291,542,711,184. Exact identities 15*267247485252=11*364428388980 and 15*291542711184=12*364428388980 check the mean law. An independent exhaustive recomputation over all 2^32 words and all rotations agrees, and the program rejects any window whose identity or 8,192-rotation control fails. The eight raw offset arrays and the base 24-run records are the fourteen-column packet committed in Appendix U and carried in the predecessor submission 2061a85b; the 12/13/14/15-column windows are recomputed from them, and the shipped program re-checks the 15-column control and the width identity before accepting a window.

The conservative compensation ratio is 44,436,632/29,617,909. Exact minima, not 12/15 projections, enter the useful-pair rate. Inverting once gives N_CV=1589032316906413946599. Exact recomputation gives N_E=1445216474, build=73804325891, V_CV=288561754736423708970454854, V_MAX=288561861399651339108383188, ALLOW=9435509593702435651584, OVER=775008730887, FIN=16795184 and N=288571296909245816569560843, Bernstein exponent 169.3477. The inherited success expression exceeds 0.39. Time is 76.4854303456169727730405314062844012983154159165417187600564715761420796424784767420679591662195313606940914225006956271..., charged 76.48544. Probe rate 170/8192, reads/probe 2600/85, probe cost 23640/85 and read cost 7 are exact rational terms.

### U.3 Ordered tree and complete resource inventory

The guard word is z=sparse(mask), with guard positions 39i+38. Numeric order of sparse masks equals mask order, and each comparison z<sparse(mid)+1 classifies exactly the complement-form split of the parent. All 63 nonempty masks have identical paths, leaves and charges. Additive lane bounds 6,6,6,8,8,8 imply at most 7p; H1W charges 6.760092 and vmax keeps 18/read. With the proved mean 7 the walk charge would be 7 per C1 claw, i.e. 0.239908 x 20 x 29,708,804 / 2^32 = 0.033186 ops more per a0, and time would be 76.48975. H3B remains 842.361097 per good pair and 3,014 in vmax.

**The H1W measurements, stated here rather than only in the claim.** Four complete ten-column tables were probed with 500,000 H1-uniform probes each: r = 8174 and r = 4401 (the two extremes of the retained count E) at ustart = 0, r = 8174 at ustart = 0x9e3779b9, and r = 663 at ustart = 0xff5baf92. The measured mean charge of the ordered lane walk per C1 claw is:

| table | r | ustart | mean walk ops per C1 claw |
| --- | ---: | --- | ---: |
| 1 | 8174 | 0 | 6.739121 |
| 2 | 4401 | 0 | 6.737195 |
| 3 | 8174 | 0x9e3779b9 | 6.750949 |
| 4 | 663 | 0xff5baf92 | 6.738023 |

Each mean has standard error about 0.0040, and the runs recorded 0 lane mismatches. The largest one-sided 99% upper bound is **6.760092**; this filing charges that bound. Each table mean averages the 5,242,880 buckets of one population law. Limitation: the Monte Carlo probes omit the 5 frame-crossing reads of the 156 per probe, and only four of the 2^13 x 2^32 epoch tables are measured; H1W is the premise that transfers these means to every table. Under H1 alone, with the proved mean 7, time_log2 becomes 76.48975.

**The H3B stopped-path premise (charged).** Two complete ten-column tables (E_HI and E_LO) were run with 8 class-kept chaining values each, giving **1,225 good pairs** with 0 reference mismatches and a pooled ratio of total counted step-3b work to call count **841.992653** (se 0.089315). The largest stated per-table one-sided 99% endpoint is **842.361097** at r=8174; H3B transfers that endpoint to every epoch table. The charged source now implements the measured stopped path exactly. This is finite participant evidence and a declared transfer premise, not a theorem; the deterministic 3,014-operation maximum stays in vmax and OVER.

### U.4 Scope, controls and replay

The base's 24 runs remain evidence, not procedure phases. Relative to accepted `686d97d2`, this program changes only NCOL=10, STR=39, count bit 234, RECORD_BYTES=30, terminal pad 32, the exact ten-column census and derived geometry/ledger. Relative to accepted `44c3ddeb`, it retains the accepted Lemma-D/Z equivalent test and adds the real stopped-path step-3b implementation priced under H3B. `ledger()` reports N=288571296909245816569560843, analytical memory max(159,383,584,160,546,816,160,505,856)=160,546,816, the ten-column witness resident peak 160,505,856 and time_log2 76.48543034561697.... The full selftest passes at NCOL=10. The predecessor's registered trials 0..4, the utab-online-r38 trials 0..8 and the utab-rows-r38 trials 0..8 were replayed twice; finite controls do not establish the deep rare event.

### U.5 Compact-record native witness

`compact30_native_witness.rs` allocates the complete ten-column image, touches every byte, and performs the binding masked unaligned 256-bit load and store at all 5,242,880 record addresses. Each store is checked to preserve the two bytes shared with the next record, and the final access is checked against the 32-byte terminal pad. The same source keeps the Windows process-memory API behind `cfg(target_os="windows")` and reads Linux `VmRSS`/`VmHWM` from `/proc/self/status` behind `cfg(target_os="linux")`. The recorded Linux run links the C runtime statically (`rustc -O -C strip=symbols -C panic=abort -C target-feature=+crt-static`), which removes the dynamic loader and the shared-library pages from its resident set; the dynamically linked build of the same source peaks at 177,762,304 and is superseded. The ten-column Linux run reports payload 157,286,400 bytes, procedure allocation 159,383,584, working-set delta 159,387,648 and absolute peak resident 160,505,856 (`VmHWM`); the absolute peak exceeds the allocation because it retains the witness process's mapped runtime image, and the thirteen-column Windows run of the same source recorded a private-allocation delta 409,568 bytes above its own image. The charge is therefore the counted phase maximum, phase E 160,546,816: the witness's measured peak 160,505,856 lies 40,960 below it, and the image 159,383,584 lies 1,163,232 below and phase R 157,474,816; peak resident figures are participant/platform evidence, not the analytical bound. Both runs finish with checksum zero after all-address exercise. This is a native implementation witness for bounds and overlap semantics; the analytical online price remains payload plus pad plus the complete 2,097,152-byte allowance. To keep the predecessor experiment directory within its declared-file and 65,536-byte limits, this validation-only Rust source is not part of the submission package; its SHA-256 is `53166da80d544ccf8395d0e6a4df3c6315b220e3850a4e4040d80f8b2ac064ef` and the complete source is embedded below for independent recompilation and replay.

<!-- LTFILE compact30_native_witness.rs -->
```rust
use std::convert::TryInto;

#[cfg(target_os = "windows")]
use std::ffi::c_void;
#[cfg(target_os = "windows")]
use std::mem::size_of;

const ROWS: usize = 1 << 19;
const COLUMNS: usize = 10;
const RECORDS: usize = COLUMNS * ROWS;
const RECORD_BYTES: usize = 30;
const PAYLOAD_BITS: usize = 237;
const TABLE_PAYLOAD: usize = RECORDS * RECORD_BYTES;
const TERMINAL_PAD: usize = 32;
const STATE_ALLOWANCE: usize = 2 << 20;
const PROCEDURE_BYTES: usize = TABLE_PAYLOAD + TERMINAL_PAD + STATE_ALLOWANCE;
const P8_FLOOR: usize = 166_838_272;

#[cfg(target_os = "windows")]
#[repr(C)]
#[allow(non_snake_case)]
struct ProcessMemoryCountersEx {
    cb: u32,
    PageFaultCount: u32,
    PeakWorkingSetSize: usize,
    WorkingSetSize: usize,
    QuotaPeakPagedPoolUsage: usize,
    QuotaPagedPoolUsage: usize,
    QuotaPeakNonPagedPoolUsage: usize,
    QuotaNonPagedPoolUsage: usize,
    PagefileUsage: usize,
    PeakPagefileUsage: usize,
    PrivateUsage: usize,
}

#[cfg(target_os = "windows")]
#[link(name = "kernel32")]
extern "system" {
    fn GetCurrentProcess() -> *mut c_void;
}

#[cfg(target_os = "windows")]
#[link(name = "psapi")]
extern "system" {
    fn GetProcessMemoryInfo(
        process: *mut c_void,
        counters: *mut ProcessMemoryCountersEx,
        size: u32,
    ) -> i32;
}

#[derive(Clone, Copy)]
struct MemorySnapshot {
    private_bytes: usize,
    resident_bytes: usize,
    peak_resident_bytes: usize,
}

#[cfg(target_os = "windows")]
fn memory() -> MemorySnapshot {
    let mut p = ProcessMemoryCountersEx {
        cb: size_of::<ProcessMemoryCountersEx>() as u32,
        PageFaultCount: 0,
        PeakWorkingSetSize: 0,
        WorkingSetSize: 0,
        QuotaPeakPagedPoolUsage: 0,
        QuotaPagedPoolUsage: 0,
        QuotaPeakNonPagedPoolUsage: 0,
        QuotaNonPagedPoolUsage: 0,
        PagefileUsage: 0,
        PeakPagefileUsage: 0,
        PrivateUsage: 0,
    };
    let ok = unsafe { GetProcessMemoryInfo(GetCurrentProcess(), &mut p, p.cb) };
    assert_ne!(ok, 0);
    MemorySnapshot {
        private_bytes: p.PrivateUsage,
        resident_bytes: p.WorkingSetSize,
        peak_resident_bytes: p.PeakWorkingSetSize,
    }
}

#[cfg(target_os = "linux")]
fn proc_status_kib(key: &str) -> usize {
    let status = std::fs::read_to_string("/proc/self/status")
        .expect("read /proc/self/status");
    status
        .lines()
        .find_map(|line| {
            let mut fields = line.split_whitespace();
            if fields.next()? != key {
                return None;
            }
            fields.next()?.parse::<usize>().ok()
        })
        .unwrap_or(0)
}

#[cfg(target_os = "linux")]
fn memory() -> MemorySnapshot {
    MemorySnapshot {
        // Linux /proc does not expose Windows PrivateUsage.  VmRSS is the
        // comparable live-resident measurement; VmHWM is its exact peak.
        private_bytes: 0,
        resident_bytes: proc_status_kib("VmRSS:") * 1024,
        peak_resident_bytes: proc_status_kib("VmHWM:") * 1024,
    }
}

#[cfg(not(any(target_os = "windows", target_os = "linux")))]
compile_error!("compact30_native_witness supports Windows and Linux");

fn load256(buf: &[u8], offset: usize) -> [u64; 4] {
    assert!(offset + 32 <= buf.len());
    let mut out = [0u64; 4];
    for i in 0..4 {
        out[i] = u64::from_le_bytes(buf[offset + 8 * i..offset + 8 * (i + 1)].try_into().unwrap());
    }
    out
}

fn store_payload237(buf: &mut [u8], offset: usize, value: [u64; 4]) {
    let old = load256(buf, offset);
    let low45 = (1u64 << 45) - 1;
    let merged = [value[0], value[1], value[2], (old[3] & !low45) | (value[3] & low45)];
    for i in 0..4 {
        buf[offset + 8 * i..offset + 8 * (i + 1)].copy_from_slice(&merged[i].to_le_bytes());
    }
}

fn main() {
    assert_eq!(PAYLOAD_BITS, 6 * 39 + 3);
    assert_eq!(TABLE_PAYLOAD, 157_286_400);
    assert_eq!(PROCEDURE_BYTES, 159_383_584);
    assert!(PROCEDURE_BYTES < P8_FLOOR);
    let before = memory();
    let mut arena = vec![0u8; PROCEDURE_BYTES];
    for i in (0..arena.len()).step_by(4096) {
        arena[i] = (i >> 12) as u8;
    }
    let last = arena.len() - 1;
    arena[last] = 0xA5;

    // Exercise every unaligned record address.  A 256-bit access overlaps the
    // next record by two bytes; the payload mask preserves all bits 237..255.
    let mut checksum = 0u64;
    for record in 0..RECORDS {
        let offset = record * RECORD_BYTES;
        let overlap = [arena[offset + 30], arena[offset + 31]];
        let value = [record as u64, !(record as u64), (record as u64).rotate_left(17), 0x1234_5678_9ABC_DEF0];
        store_payload237(&mut arena, offset, value);
        assert_eq!([arena[offset + 30], arena[offset + 31]], overlap);
        let got = load256(&arena, offset);
        checksum ^= got[0] ^ got[1] ^ got[2] ^ (got[3] & ((1u64 << 45) - 1));
    }
    let after = memory();
    let private_delta = after.private_bytes.saturating_sub(before.private_bytes);
    let working_delta = after.resident_bytes.saturating_sub(before.resident_bytes);
    #[cfg(target_os = "windows")]
    assert!(private_delta <= P8_FLOOR, "private allocation delta exceeded P8 floor");
    assert_eq!(arena.len(), PROCEDURE_BYTES);
    println!(
        "{{\"status\":\"PASS\",\"platform\":\"{}\",\"records\":{},\"record_bytes\":{},\"payload_bits\":{},\"table_payload_bytes\":{},\"terminal_pad_bytes\":{},\"state_allowance_bytes\":{},\"procedure_bytes\":{},\"p8_floor_bytes\":{},\"headroom_bytes\":{},\"private_delta_bytes\":{},\"working_set_delta_bytes\":{},\"peak_working_set_bytes\":{},\"checksum\":{}}}",
        std::env::consts::OS,
        RECORDS,
        RECORD_BYTES,
        PAYLOAD_BITS,
        TABLE_PAYLOAD,
        TERMINAL_PAD,
        STATE_ALLOWANCE,
        PROCEDURE_BYTES,
        P8_FLOOR,
        P8_FLOOR - PROCEDURE_BYTES,
        private_delta,
        working_delta,
        after.peak_resident_bytes,
        checksum
    );
}
```

The packet contains all native source, exact census offsets, ledger records, all 24 full stdout/input/command records, complete kernel peak/final observations, both ordered 15-column SEL pair streams, source deltas and isolated-control receipts. It is the base's fourteen-column replay packet; this filing does not reproduce it (commitment below), so its 15-column streams, W9 digests and per-poll observer traces remain available only in the predecessor submission and the Appendix V archive. It preserves H7 sources and 38-run records byte for byte. P8's H6-D derivation is unchanged; its phase maximum is updated by Appendix Z. The historical H7 seeds/ustart/CVs remain unavailable. Hashes detect changes and do not authenticate historical execution.

The packet and its verifier are the base's, carried byte for byte in the predecessor submission: they bind def34145's claim.json, proof.md and program (SHA-256 dbebd90a...) and verify against those files, not this filing's. Its readable verifier checks the packet before decoding it, its replay_native14.py records how the native modes and 24-run matrix were produced (Linux cgroup v2, unshare, g++), and its malformed-input controls reject changed inventories, raw census, native observations, ledger terms, pair order, pair digests, program lineage and compressed framing. None of this is evidence about the ten-column implementation; Appendix U and X13 bind that instead.

The additional development allowance conservatively bounds 128 complete 2^32-word builds and 128 full-W9 scans, charging up to 240 events per a0, 2^12 operations per build word and 2^20 per a0/event. This subtotal is below 2^50 target compressions; 2^52 covers it plus compilation, integration, failures and smaller tests. The ten-column census recomputation (eight 2^32-word passes) and ledger checks are far below 2^50. The H1W/H3B runs (3,927 logged CPU-seconds; 2^16 allowed with builds and repeats: below 2^48) are in the 2^52 term. Combined development remains below 2^59, inside DEV=2^60.

<!-- HISTORICAL-PACKET-NOT-EMBEDDED -->
The base's fourteen-column replay packet is not reproduced here. It is carried byte for byte in predecessor submission 2061a85b-63fc-4da9-8082-0dea48b380b6 and in the lossless archive of Appendix V; this filing records its commitment and nothing else. The packet document is a 125,161-byte JSON record (the LTFILE packet.json block of the base filing) whose payload holds the base's fourteen-column ledger records, its 24 run transcripts and its native sources; its SHA-256 is 70fec104db7c34b23d54b1b6008bea0d991533a4c2a06e2f4aa037619d854850. Its strict verifier (verify_packet.py, also in the base filing) is retained with the same status.
<!-- END-HISTORICAL-PACKET -->

## Appendix V. Lossless inherited historical archive

Every historical section cited in this filing is an entry of the archive decoded from the block below. Every `historical/...` section named anywhere in this document is present there (section ids `R1-R4`, `support-3.7`, `support-3.8`, `support-8`, `support-9`, `allowances-11`, `historical-13`, `credits-14`, `historical-P-H-Q`, `historical-R5-R6`), and every entry carries its own `source_sha256`; the Appendix T H7 packet is likewise embedded and hash-checked. The candidate also includes the two inherited organizer experiments declared in `experiments/manifest.json`; their bounded scopes are stated in Appendix Y.

The complete 38 source, registration and log blocks, R.1 through R.4 text, Q per-seed records and explicitly indexed inherited support sections remain byte for byte in the original archive below. The verifier extracts their original text and checks every hash. Historical 15-column observations retain their original values; they are not current compact 13-column measurements. This filing re-encodes the archive frame below with other LZMA2 parameters; its decoded bytes, length and SHA-256 are unchanged.

<!-- HISTORICAL-ARCHIVE -->
```json
{"data":"{Wp48S^xk5{}S0j0stWa5C8xGsBn&k<BeqR{sRC#h|O??GS@=tut|gw&wrivq>?N!?jrC|NKzVbS_JTI;h-q1A$GDSF3{AXa|D>!;^6}3pSWn)){*u#4rhU>kf+qoCJCb-Yri+mq6%92GK~$-fmgH{)HtJ2aj{yHF88}Vv$TQt^GhRqa>~EWLvo5<tv@4hB{$#5Yz{un6o53$6Rv8Lz|f5^S#ndV!G-W+4TIITj~wzGeT2uDLHhj-2dD$dOJ0I)%!Jj|qbf&d!k@TgPdof~t`GoZD@$l9zapIS_U9*%HOXOuLB2?9<Tmyl<KTY`nbEdkq~`vBh(lapJ~_;2j>c5#r<0GMEO@OnIVi$NYNbT80JTMS2vI!^*WuY>#+JV|jriI_)|Mrkeud6`W)(av?^u@&fZu$xZc=)fAM?4`))q<8Fm`P)UH0s~DCXX7VVb>I>?w`RmlO`)roDp%Ag3cpOzf74vHKiWx+*ms^k})HB`!0#mQ>`QgGYG=trI;uA13Th+T8~iNFzKpxiECkX{+U!KYde<lkY<*+s{kT#ul|v;3wAyt=;}7+ne|#Y?x3%c4sr{FG2BBH?v)2@38yIfggoNKwy$qI!ZJFf1l2MmbLo0W`<kazyZ>Sf5v}cn(>$Sjf+0gtjk9>UuQZfIhzlRCI=yrq!L*rSw(Vp63x|<&tH&TnBJxi#$v2Cu3OP=>^Ij%oJaJRI)0LraB>0f!drm;5CIh4wAy<)v}N$IM4b)vzfRa#L8L7QDklgcQ-M~ns&P=T+x}%nNIvO3&HtSf&Gqdlv}wIbXHKrS(K`G|WI&-!9n*wrH*u!4_|P1c4@RvVhSgaimu$0@&_58N+Ia)x#Y*BWI=H3TD-SB8)~<QC*HJ3JO>M)c^&WJ9OYj9)<HB(3y!B+<q4Q{$bNoB7q>;p_q&jn*8~RQ_!D$vugW+o3Sg)k{!nnCGq=H}Cp_2XlB?R}cjcx?6|9-KtdE>sRCE;AkN^Q~Av{72MTegM=VE2UNx8gPi0rk-qLE-ez-LJl{CJN4Q!<E70)37<Pay4eN&DIR*j_k51*K4TU+K;Fz8`ZVOLy#{}EPE+RpE1U1U>^#7@g|!0*3{&rGD72}xISROhbJY~PV9ar-QDE3wY_6j4Hynd=@snmD_!J>g-;*vFsoxdbO@4sT~<^&+xgUbV?-;8M#M!^n~dM%&>iz4FC>vlEv<~DdYCnSFQj}UU)~N)<MH89S4b1fWj;L2X}hOMtGP$X2-v3(IaLJSF8Im?x1n9w+|<Ht$r{4!gmX3Q!zff}FubqwYSMFwhp+We>jJV2q}%flL@VR{oJ!#+0(ENu%rRp~m;!8I{9&F5o=oUP28C-KC)&S7?{lXPEYfh5(V3Mo9#{Qd?2c3s<%7}BfvLXNsb7MuetGh_7VBDlbx9zdNCoR4e)k49(5krrZIHj@CM7E{v<l{-=3xKX*^MB}?Kb#{+eQP9MGsGjH7d2F!hFdIHG;8VKjU=+RE91u2N!Npyvh-T#n?0LDPkmW6wp$=8_^1Iz&k-B6>ZD%6Qp9!u8alJx~u3!rW$W@YaqxlJ?cVr2_?3k!S)9E_6&GL*LKVT_V*s>uE@An_c!xGaQe>{0~?37PR^Dv#!H7#7~Pa6)Wh6M6O5-0@vpyahDwLwT}^bLg^2z?^i@IR`G8$bM^$P`m#85s$VjdJd9zU_?vgfnSPPj?LHT<=*p;s2e5xlKuT5Ii{Q=JxEYX9h)YjgOWIP~so-x=7yFv`(*{)@uy)|1GSV+L_V{Vvg<_e&%J^K3Oh}Bs0fa-^AY0uZ}Xb!n}`f=76L&~3?v$NS2OS8$Zwk$NC*vBGgic*p*y6cG>Q_s=u=!%)|l(rD6LvNG{#*asA))?zM7_K|j_}<QnaSjrT%~JJ5OjxWJo|6kG7Yfuyx>i)Ep5vH-M$-OH?(cROWYRwZ`;U0U?GlY@7k`hfwe(oCqtXIK+5&0E2s?F^QL)1<E5@^Zu@iU-E-g!9OTEae?~Q8RXgNHjB5W0nXhCYs;DT@wrtEubK^73g6@|(E^T3KB)<(gLLs>}8k)I8DX5CB!uGA?QFaZbq!e}?G<#dtO@4ZHul4x<y)~DL}>dmv?EeA!S<;eG<^-_nS#U8BJ8!Kf^xFu<x0V;Ca!Tfp)7V_nemj$O#5P+V$)VD%QcBU|NK?iS5)I^w%ZE-1TIV|-+5BFe_B>O72+6Vn;DTe)Px9x86ALe$S{a4Qabr&#xnfh<!R@%_uBE{GXiZAQK@>U0zIAic$LxxvYwlfkpt^}rvMH?vwe9CqlUkd@+gPbvkuburCtnyS&r<Vb~Xm8b4!N9e{$t^F9z7yV8CoEi{aY`wKy2bR17+hs=R{Ozto4wWiZ*~1SAq%e5#PdA51o{_WMB{|ouG{OLf{Nq0Q-qMv6C_oIJNma8cp|O8@$rKk?G3RiM<e4$Fft`9%$-Ng<jFrXRGKg5g9A}~tt+0%@DTQJ?5A9(q}0K)5>$LNtVy)$ec0`!<zlkM3;o`7GcO|*4^T8y%woEyFT{o0ZR?WaGb5G77X8vi=1Jdui_sjV_y3wR(hvlnyx|=W7o~PR|FJBlVgl-BhYnB)_LO~lX2{W8#WsurV1yhLxW@+OSXdGGuRC`5V<uB9KJ~<+@JD!aHK!qd=>Ti{DLwAbgb^7iXy)Vg1{sTwmvjsDwg#V<&xsCUa!9jf2Bu_-b1{e6?!Yz0%82^c)&7B^w7+#OvBF(MaG+Vn89h5TmG}XtuRCL>vc$qJ*h;R@yQhHgxatQaiH~`r1972s6}Z@E!FZwy?R#hVr1n_UA3LT`GeMgdFFFp%7qRcwdhKi}UUkih0j17$?2nQ&pS?A_Hzt9a_`qg{G}7*EtqZ(bZoiWp3Rcuu8Ifq%N(a!AyvN`3?e!$wdhG30>RDqe!3!|sEg!2_CgelL?r)4d-WEj1bq@81wi-C89R(z&yq|M;k_*BjmSIluLU)Ceca;Nu8Ov>%h(P(p#~N!vnlMxT4dv3zCb{q*j$k%eD6ttT>XEk(09`$~+FAQFF_VWN@GtZ1=BEEpIMe`dB{O1Lp>{zNi(_gP$nuNTjZ6ySFGHCBrTzt3j?mQ_bk>R2TlF%i`R@h|o$F;>n<2}YX}@X|NTXrAkSI*!dqqPx+|%kr5Xk}f;|CzawF!|XyxdJBS-{Ezf2Cs^cSNPkcVUay1g4COHFs2%sw~bQ^dqacuW82Ccj~49_6(U{3mD%4<r30T4PA^6P+D4-urAGeA=%IPdHxwfH4M$+fi9sosNCRmN_!JOmA>^o<&?$F+mf<h9}OpS!Xnxe<UsT+%7ClxE0~hwzB%7yODQO&baI|RlYcu>=hX(QvCbwqA-d&j1%N<x5;gZAyZ0XM3H7zo^*q|D2Iu)faV7Cr$f%U@@FWpkm|iQ>hE^qVSrZl&fFEQ-^}Ai!&w(<!P^==sU<6OgRmvqP$dnZTpi>jO^t@Hu_1|BD8B*hNba!c7IbRO+QKeOzloS(j6R+hlre(V}m9z4YLShjAjOGUbk>+}BVWJIu)TZ$L6qrZinl2DBn0AbqhO^OO+{5CoaY5|n3I^5ZwFgc^9(FIYhp$fg5gRB~`CB((Sf=UsEik_KAT?|1vO_XImQ7b=jaRZKV^D0+hcjq}5l6%xk~p%bgdW2PG5nH7(nEA7fJAIzWI@D~-h?qpj8P9ZX8hotzV7aN_1I83qpP=EvPy1~N?_ij@#J0$BDUk1fy2}ITj8<7v`?H?PwPo@%2=*2l$Bb&fHhi<Wq_k<aHaiuHAeapbg4%OAnwby3p?#9fpy77YMFpoLXW)Hd6bK7yQN_h#s2M6cmG)=8(&{N$!!^B44k|;l%2DHcEuPKd4EvHZ99`kwiU7V*y&B-!p32VcgIvHNnA&akPYmZzM|<OK`}`}MQ~%9%djm|d@}WP5GPHGII1N<nJV9IixHm!{AxLmo5YYrvcv<0VyE#i-d;TPII@MB>DG(27FMx-y+{W=iKMzN@FjwV4Wk?*<<j4+z<(ay5ph~TmQviX-y4SHMc7Se(>R_oBAj#8_!BLuO+qo!OkT#(RY-A~<8;J7_*#hL2f!d__?(cl7c`~L-;d%5e=as|YH<M@=s9muRwj+G^Nd{?-3cYzrwUgSSp~!t=g`56Z617(mO{cY0vL;gq;^uwZ|qA?m0wOPFMn<h=_{Jrb`P(mojHOn|FUo6$DROrY=A|;C#zn-iK<~7%}ync_}PZJ#4fl^=B&;WNzJ%>gD|h8nzpgMhH3Uah<YYhK0I18V|wtXdyvL&8>Kxg6%L0{mM@VG<=B~ue`n=D*o{1l7<3)Gy-siLhy7Uq`I|9BH)tk>Wf|sa0h8u!W9_}HmZK0MG#W2lD#^3tBP_SgfzHwN1bDue1^MoSVL4tKY@24v>f_0#Y4htv1dVAg{8j@vY=kyuaK9v0;!>{&nZh()TbNcfVRCVv5KI{*JHP65Sn1ZCS&@e!aC}5MYkcX54v*Fg+@GQ?6-$-j5&?mj8@BmO*iy?$_OWzzXwhr<x=Ug`o2S>tr_g5U5X38=6<%q1PL<UDYOM)6xgcFHUF$5&dY8@DZ`1ucH93nMoA|zT{#d2eTCLezb62Y#^z<Fwg(}U_1D1ao<!ni^0AF}`*T1s`F)s`7`@HBW-MR^@n1mvj6qs1Wmboi~P;e7C6xJD`)lgRv_=Y0fSp_J{%OYlRPo!qGviNAzd^sPbUByeBBZjKEHuvGn>!*8``@*T5EsDeXnjTgkol)iAP+c1fk8lk}@3Qi52X1XI_D=dVl{(W~8%t1PGa@(?q^IEOO~83|zPg5ZYx>sdps9Id5QwrFn4H6`EkAs>(6@B6?L&=p6y|MNEr%>@dJk;qcbxp_41`!kdh3+hED%+|I$(qyFP07rOS?nPIw)@v?|gg<0U1`R7PR$Rsf-vLAs0z%Ee-bA5@#ZRZQFS`siCa5&;@}8i)*qsPGWtcv22agEmV!4kM6Lsm}wa`=X$B|pz)(v{N{V0MJ{*aBJ1->r<zVzsF&JcF~dv{_xfJ6^#8c|8!27?PBkG7H?@V5inX+ODVhZ!V8{n(z$%#4QJ|qn=g?!kP<2kAo*%Lj-Z}gdN_muJgyDyUnZz_bcUM;M^5TM~Sav*;#Z1N&SNCm0d7AY_#RxeH_<^Zrr~97&8X^D~5^kf_pguAT$Tx^!F|+9O(qM$JSvIMsLvR?L+x3woaQg;Txg>sN0F>)aclL^`q10K=wwP&(DHaZ!9YN%rg=<~;Yp*5E;LNme+@4{spPth06J%ypsh_d<Sl|yQULy>kWy*abYn5QD!fE;kiB6UszPO*OO0c6bj9R_*4+U^m;sI9O?`IykPy6ubbKcWgvbHr<t5};7=Rmqig6Vn`yf<4&EnfxKEC%S1;=as-+q_)rRDRYzKO6r{)@O8g%7!2evfDkWV(kaDbZeAbKeFT$<29=B1$X)KXWFjKY2OK;)4M#SLCg^M;qo3RnSf^5JO!sevfJ7R5q{)9pi9GYZ3f0<o_3At)Qk2qJF6(nq_S``kz#zGcmjNZW$j=ZL;mf9E9+fq%AaGNpiwog+g!cv<+f$sEAu7##bz9{<r#1NeqtkgAF4YkA-ODW3H&>wST300pND3=+S`teAG6TBt%*lyZ%DFYGSSq7FAYVKm6>x|Is@y$^?(rMDe*Z+qPl|XMw%C$1!@DQxT+fqlmO-j-BU-vc|v<MpvdK@7)v`4Y#c*Lp2@&mnFxq0sU3E8?N*cFi!F0ieoe(S;}1;yJkRn6+kN#c<zxCcAj<ZYBzNmQ6IG?5lXPG<Dae9x)As*0OAA)wW6jSo2X8=e&BQ+95-EZCe~}y>DXCNx#agZlJNx&<`ZI5z$f`0w!el~3+g4kQW5yrk#ymY^W5^2vOHfd7S`hFUA!X1^+wQIhdF^TVe_QPFSf`J3gh?H1@l=ox$79DcT$TnpORpA%X7+;>X9?|+D!{g@>e#~Fc84bdApT4j9VTj*+heh}G~umGe0Ziql=m%j56KaP%pH?lY0ixJsleBZFY>eIK}8cdSXicPkQ|;4>8Y__CBe=$Cx{UB+<RWJLE)28&szEZjD^=9EF*?ZHBXNW=XT#P<gHa%*}2eu%m6si_f7~6MwxDmk><{+1|@Kph08@QW@WJ_!EMZKkx3@fZKI}OB-c9>{s=*3%3EYz!~8WMK+k(O<2#_zi>BP^aGfLQQt_U0;#dRCXZG{0@c_68OX!CMKoJ(4sCK2})dpGF(Y&{F63ub{TgbMnxhn17Hxw@m2^jND;FveDgb!r9J8uDU`^_YBA(7{On6^}r{P+%x{mux6JZpn#Pa+!^ahsq~RO?p;%xkNgN9Yda23Ga|n2QCjt-bcc4gRwE?<rU?d+TZ6s~l+U;)Btk`kM5Yw@0n402%<!vIKF|Hde5StZEt4<3gnsZRN@zneD5o4CbN+iWz$mb}0#>Hhi)?a<Bq3=tkC+j7t8g4=(@zprg^2tPPcF6S}=o{f0@x9?-~2>a=6k_16$c9!qI%A!)1!YH>wcGhv@je<6`SM(#tTK8k6cnZZm=Xx{020b98tOwInnbVMR%9@=(lj0Jo^VG@y1_IXq1aH*o3o2>QC5HqoRkTl5jIU!aYsu#!d=<yvpZ;-LyKoN-CCeGgXdOtLOIn}(laYM)l)g~p>dc_&uTYGuXx(^N2-Ta}|o}jm(V5|LU^pB`y>p*j=Um?NLgzEnwBniQyXfHe`LW_}{wvAdq3=ly9m5*~rpd@;ud*yc@T)k*yZQ1##p(Ygrbug;QsKUuEcSz>@9RmlnM}5wbuQkkKz9w<p`|tf&3_8$mdtbc{J{2;3yD=wQ5d9;bLsgxn@&TDn%5F)%eIf-KO(92F-bh&KRhQIda6=OCxB&(?N>-ufp<gLRpnH5E)@113j38T#{HQ2(azvu&L-C)Z;&2wH&QU*Hl9hs_8r{-4hS!FqKbxQzB{EW6pr-$JR9Bnti~C-jEzA@DzO062UuG$yuk%@NaZHRCnJ%;yAePXL)P%Ac;ZD?c{-*8_*c0X5+}Q~seRxG`_#A6gaGW_4Y!}cUT!mV)V(*i<B7WcY2~WSk>`T>M!b2F`EMSumn7soN3$1r{+T?wtLzefu1aMb<@gdR5?Pe);4L&QF2%_(@$Brk5x7QB)fCl_kR=fUB0Yk}qW5W_8LL_zjV{M8RF^ldR$S#R+>Vme=cXC7|D)0%W=3v5elS3#Pmb{r6?qw;vW$idMZO|(GlX(-8g^aJZe&dXpILyO=7M@i{5MU2No5}H}3xq(z7XG<S_am@4cNqc6h7`zaIOReVbBRh+5Ff1ty2%1PWWoBX*dELA%^Tb>vi`fEOoF8u-Zpcfn5hvrajY+`3+Di0Z9uo6L!(GYu?X1cGG<9wT99ZQaWNuFuQ+F+eNyk=R*AXaW>#=robZ)2q`--)+3&FdCacHdg~rIGdGuq}yQRv&6^vb99U~=Kyv?6L`pP8XuL9Rr>0u$r7^)5HQLV@ur@SO|A25(Z-UJ`?aRD$Cyd&X>*rqEZ*oi#SbjPY<pZ~naU?TkFspFMQzgAHbk&=EwrB(!Jkcd2bcOBL$CM|bAB#5!y&G!MEl;+N83r+D~7Oc{x;*Scv%SrByZHv?|fg)rpw?|2C8sGjd4YDk8=|=$PBfhsgN&$`c08@v`!enT>2EeiKO^9Y(GM@u=Nsd6$l7198`xr72yn_F0tJH6+`K6G_*HcTOkck1|7JuO_d-)($#mZ$Ib6zn$h7No}KJe8%GC5WX)A|x56*Yev^`Efuac#q6PEwK45;xN&3cslzd#4+DplIBk(;&vuX$O~?!mqQjDE)w_4wyiX!rLN|vO5Q(X1w)wzv)1~_=jK#Lt7`a3Yks1jtD<NC&YCk{}=h&L$|luw6z2RWf)p|+R~D(ir%_E#nU%JMK(Ah9Ci6|s_Lkj-|W8l6-tyEj<qW8nAMaU=QNP5>^?L&6v`JgL)gq01YVyMLC}t8{~y)fq1P+-I^XmeiC>eT2aX9o9=0q5vB@aw-_nQ`MRWtfw<zs;+Qet&NYho20K%IJSYHP+nsU9E)pt=^@4cH<{XX<wirKT#gZkbZBMIy*Y!Fl<P1)mEGaAm@dqRnjHt?12lko4Y-57=|Seq_%EnR&#-g#X6Aa(>)qUTs~X=ln-)s<cCT^Df^TL-3d$r4U#h84lAjXBPZK*?YtYV;8~?$6Ty7Linsz&ERJz=FCD=VZu>A1Eaa_Q74RhY1)@IPbL#UDi@VWeJkp>ZQvQda>0!)q!+tdYyE`A1xZn7mPdCfhi|*YMYjo3H@?+EIpuQp6>i*N{p$vIWc<T(&s%kZw9e-d1tJ+Mz0nf^E}&1bt3vC-MTwgoXetM+EBy3zdWDxsS?r;4}oj{c;lf4%s~0RFrk8~Lv?0XcWxYBSsYSGVZlTBj6qn#LbjA(!+-PXJQr2Dn^#|si?u~T<(rQD8ESlVqi)!&yR=&ACY1u;Gi87S>tB;9eST+mZft_`MJ_Y%JkjoKm%qw~+hec=0)gG}cp^CiQ@unwe1Iv?I=A8v=Nmso)coI}7*xDq8Olh;5hwQYYwOh93xFo)(R*RO*5?epqoxNI>o}FN@XD&moU6s07O4~{LY0?qt>+;*E@HYj#StBqpgJuTEJEP1x&Uw4K}nBy0jloD9N)w;gEKw&FVTeEe7S5uLnU{yKnFRV8)E5s^{ajRh(E^{&%lJhXDslJeU3Pge=4Ft+on#Grq$u;rz-74FhLtUC2WgzkrE|6N`hiq*pBa6cLAqzv9bwb;PSMGf#jKdO{FYAE1$e)>>yDbI2*HG9(;*G-7`i>vO52OkU6Ft0Vsl;Hw>BAfVA@5M<Ji<PgE$$Fm`uZPm&AxkRYfMFm6@!y(jIm6~+wiYmeK)NrMS++S^yuzN$^MmzQB7L#?>*IW^eYcV1hD6-SegvA~osN|;jL`u$B47(!AS^L?e4IihR$!MHfcN$<ggvK<@{uV#|1rC{N=yti@<F0R%-;M1ev2X0n^ED(ZnLPlEbCW666rc=RY{14l_y?>duXQug94P#?ykT2;l8Vv~&k%M}%;0%mJ2TV*e6bB+X6@O`Eoa`0<y5J{EQ{cB4c}s&1$VB`{mo|yk{gFDdnXVA-e}&n}T#p%U7U7|6MbwUOsB@z(62H<Ne=PKgvR{b-kBi^Of=*csZC<&nM71)K?yF^?g&V_$+)CCwl8t(f3-b`+OrG|e#-b3~(md05W=bw?1?q{NSENaB&WtJfXSKTDDx)y%AAzM%z7q<xBXq#$3g3_k1h@5$ny;F5VUf%217p@S_!FYJm39}!->&`$x1@cc1Iy=L4G>Bk491cV2BOCPkNajXUdk!&8+U+;m*LQ??tVQn8o)?kq8scoYL6n$jn>>Cr_E9OySqtSk#E1P3I+1KsLU585+DYEcK&i>iMANYiB6Pv1k&@>23!r7*X?a{;?hrU|5q*ZS}e>@mtei9>%35tj#R>ZDsnl=kO0jQ=q5nGZd<~Hq@}s|**DHydob#04`@RTNg)jH_iIY-a+PwgPw{-#BlyQ%tFD78?CLl^MO>ySNkJ2kPX<T}XPY{1%OLGWs5$?}9OHV!DH55l81vF1rB%R~GdbSS2=i3jjqd201GjPHM+EE5MrPo*!^e{5&(>>5wC@7*>q@AiA`AM1RKLCz5a)F}k(OF7VXg`+n*lhYa5lmPKZ6NaMS8h4+`}vF8n#D~#s1*a!|G@Er7_AO%`FT#syIZdw$5R{)1V;Kx`y{pBAU9*?QmjtEW2jd%u3gDa0J+T#Wt*J%T3vY_ut-2^ScEH8LmyZ-RB|qS2rjO&h+B>8)xOi43md8mhbcX_iroY4?p5cqi<;6I`LcD#O=-L(XB?d`6I|<0uTVo<vo<p4Da}6^3Sy9O))jNaxe45o=2-e&ewBd)3Ck}`RlDR>JW-q=HCDRe!>o5d_TooDg|2U?XG}sybpNo5usT28vtt%<-d^wnYChW__Cl@pF1p*hhD@5!}NaUSXqEU!(36+O)6ny|J1$-{@Ul+c07=C@6rF4?Nfo8-|K8`Kt1$vAk|uPxd7c}3&}~*n<AnqxxD=6<2=YyHW$$6lCho7v3UUCn*ke*{@al*KP$rP_zpg^CilfUy+$0<e6o^xovmQ8@lq-^5(7V73QJ#SFS3rw3q2iN>(IHkokUcY^0<~2NU|%MZtRmIn-WD-wA@#UqcH1N%9}dI6P*xDol6qV*Cu38ubl6~cn>xsT9bqqG$R53p?sO88s{dv`1p_gA*Zt|$Z(OdoZc5kT40IMZHW%}=rxh*l#c|?!4x*3Txl8F*+G3)Ys8_bn)3W>;r8)IgOMRf&Uc_-)k4yEEbyEqdA{f}v|YG}lO2K0&k;ip*HZh2s!GA4Pv6cxlTsB!F01)VO*#Fs3QGMPxm37^hx9DEijX_;P!0yK<F2L}!F2s_xZ6)Hw!QTd=OeqD{RZgE@@wBw+ww6aJ>AjbtaGW-b@(YMSTJy>7Cb@8jZF!Lj4HR=OR?!c6l7q`3bv+a0HU|-nybs+fJU}Rr<4XR9r+ky+@DLCas$2`A-~xMXQOiS3kbGqGiMDb@S>&hSq_p^ZT-CExM`T*2hxKL?FR%eOvohMM|T<%H)|WT@BySl<G|!<1RJcYN?A~G!~u;CTIlrnU%q}2Lw4UgUz(Csg7ua49&E2^!SdoJ+1SCs@Ooj`g4E=8%c?63_VL6ZKE_?%S))M~$?E3U*UQ)y;&4QTk6=frG7Ls;JZWLGkm49tB?`^SwdD3a0m9w4Z005h4l?wtZ~AzHhFy}(T~f0={B8cO|4`PmYvpFsZzKas6Na^4uBEt1iHF^bKMOzCPSzm4Nt3oU>{|}fN|GNxf>yPhjIFIy9m+R<G2a(!+(7Wq$);v%K#P*+v7(C@yObbj%J@s&ETbgT(CvQ>FZK{sBVR7p(hlzu5J*u9L~-X))^QPy;g($|)x3AxJ-no^s{?F{)}Q_kBZQm{PY0bh5{&YxV_)Ct;Qr_k(=y*PYHW)=(qVo@^i6q+YRLhS81u}Fc4OamsTtFauZaAWj0{ZGb2A#m!?21%)xGL}<2v5e$BaE<Ii(9cI#FdQsY1Vrrd~$jkj%zcMeMkByg}xMh!1Gavy7VD68t{a+flYYwumLrpc22QeX5{7=V7=aglHVIkj*oa$DiutPiaa&ems4r#{yQm+7u+zgR2zY1$(!<-h1zT)^lw<FJ?3~0l6DaLqb+YJ5CSbGxK+KZE8d3;7~S3?R*#DI)0mk{{_i%8F!l78FY}KUom=+hecPSU@8mCWw4X$z-It1#55w@VP&CcYJ`+{<zPa+u<Dxw0~}N0R?8q8AT`~mng*yq1}<0+?Vt#%PZeYI4)(XLrOK>;M|#_8or~7EBFT_vCgUm`;AT}YpPR=({SpCa*^N6VscYm(RH+NxRg#mDIbZ04ScUr!Z}u4XI_3z5Z1jqONnC)5ZsyzCn)5QqdMQ4$6rkVD%UK$0?jj<zMF?8b;u;)KxWpvWO0pFdulj=XQdm#%^JV>Wi*VMcDD_FDd4wV3#8Nq@ysnacJMn-D0VIdHHbs3M@2#dQ%X&}s6_&+EQ`MK-llNO^<Bd@UBNI=W?G<xNd<Se_vBz8Web864?btE|aGEKGv4HnmMJ>`nK$v=q1(wBGoIH-z-W_(2TIHj@4%WBWS?DE?R?{{w8LYIxtSRa4-@9Yema(MX6p)5xiu+2L0opXetkaOelb~(kR!SC}j~0DEc0FT%Mb;10u(3*3dbK|2t)IIo1kf#sfhDuCYs-wzWLnf9+o(Q9e|SwO)F0PO<k>=-I7^*UN1Bzo7Oah<O3wj{>R~dEM5u4=-0V?(_}IC)j~)39mNN|o>r{p9#Vj+={|IhhaA}@tEL!O;%RH-D80BBN{ATr#-ymT9zk~a>VO~^X%c$s?rhUUkiKqLEJ3I-g|Ir^$|Jg)%bLpA#pzXx-BZ^2}SDIAm!XbpO?lGi2EXAY58H%QZd}eBm?PR`5kTTFZS1O}th3nsoe{v3zXj*FFZdwJC@%uhaZfGb(To#xDtD@ScxzXkW2W5sp*;s_>2QFNh-ler+s|j8;Vx~AGgb28Y$**E;8?t54n-F*~`6Dt<)L2VlIcDZGJ`hXIvz!K7-1G+?4qBd8&G5ZC*j$<~8hYZoUe_M}KeHZEhm)5m=17i0B$)0YQGx>YQwNL2k<;H7YF0mw_*@O^oTddM6dc|!O@nd=%_nCW*Y7Imxgv}d*EtD#Sgc%ER6Ft=+%hlYr@EUij(#W7$?O)}P6RmB4B#H84vrGzM-@zYE?z~^$=REWGTdmCQj^zo^{jev8)Nji4hxkR)O`q5D7FUf3$exd?RtYMqaHz)O(kKG-P3M+R-`C#B*M4soXZ0OxHl<eyF*2f!2?1;ovZH0&*mM+>kk)efro$`rJjraU}@oD6J5($?wkt-;J_AMu?fBGQA7<SsL|&(Q=MlJ)WqM^U4m`jx%=$c+o4@hX5%TIF58Ly5z#wL8CLCoRunmw_QS3l5-Ew5Zla#t12U5VYr^jE<i;uc?%DOB&um${m$tb9LxI6X(6{B1;lqOVyf&qT7$EE&MhV_O2ct#7n5z2)xrys?xGpP?KV4lAv5=AD#~<S=`_or)yb1dm!q^=YANjrAS&?4xvIKM;!$Z+(!8|7EzeTCT?s`*mF&sZH+bBtY3rDIM{gAj94Qs2BAfMR%?f6q9eF14mvqu3a=O~b-bVBg)KD1((KWRXZAivXVo4eDr0)3#+4hN646_bUVk*vlhM~7<#vTIr$j`zxFAbbeS=qlQ?j`=8~Sq_c;N?NX7fVh>1>44K#3d|vnrA@<;S&p_L<cw-ad7aeK7QSpvJ;B!|qByxSvWWn)g`7E1A!|6)>c|GBj^-1%><S^WMK9qdau;xGiuZ+d5d9pgcftEDEw}rfrq&g@7pmEyQB?Kq0S)%-c~j|#=2HER;C#}c-p{G+rmM23oIH(IxWgu-#0$8DEYHWn<8(q(9N(-&-e+9%&Dci)SJ-NBhMvZ_#KL&w1Qy0r?aUkP*l{mcA-#>9TPN&qP#L2H2pG>ej$rS@kWWS?59p5``DGR707otG9t2*$2x9UgNF*M7e>raeHNnRm{kQl@fyj2o+e+HOE_3jQ*60HbWC4cM?sPI%gqLc_;!MC<V=2eNhOg;q7DFHbBs;V#6up56%Nwe2?gpPFNVejkrZCx$1l8vFZ2+Cw#BjMbj8tr8TW2=4eG|1N36$a9(<e$W>@kbpaTf<vzZN%qd+GXap`yY@8rV_)?vj&&GxYW{@}SLa*d3)%g#lmJ3<=H60pa3v(3=|QG<oqo@O~e5L@aRwB42j^m0N!TA17%;Lfg$GfI+r5AnYU!nYNjn?fz^>i-P(>9~}9R@<iPy;2VX7&75)cjbL@|q#-U}h1q{sVL8|=Vd(<BHyfx>PCJ_nNxiuAGsTibV<co~kMF>1Th~;}Fw_A5Lxd0dyviUW2Z(&YT4gmH;RTtyV9lRj#BiM-gJkE9tRSEzFI{IGAI3Vk3?;&vq6<Ke`lH`nI}JvJYGlCjuCDlol7I!y&g8MZ!N&zVT9}wj*CbIjfiye&`s5X9h&3kV5&BPA<1vZN5x7UOQ1pFeEiH!H!y4h6TIl^NyV=eWTKeDqQLNAvKgm{*AZF_tYe*KAXRsQa>tQ}x!;!1Zq=|gs^1F!q7Sd=0jucE8F3;Y2QLhihW~3n#g5##T2RVs)Vc0}eKgI(r&+*wK^{Q5v?e`lvzGMI1BRCLMIGMabsF=4gyp@gf+2ad#?QkXM{R{Gnfrq3#iUG_mn*W^aGPhTHXHI>z_kgto->c9o9c|jFCB;<4r=K<{sW0?S|H->xgt@UxmUdOpO`dC=d4Yf&#6^LqJ>}jM*(ZC&@8xJ*k<lhV*-&S2fi|az<nYCE))gUdp*4?zCyUj`q0DQSK;yMOjT3oSLY&y=b7!T<d9OU7RhVq<)%``BF|K1gb!kc)CUNMUxHLk%M}A3fJ5!?dJ#P`mE|+Nvy^*SMlDM^YKrW%}(5o|!q+Y2atg49;s|jO6T&t5?y2~yxLdIb1d~ia6Bj-J|%{boB<0d+3tdxw_HSUjJJZ+bCIY{aT?IAJ=5*(6frIl-w7mMLANN-6t@Q;$cTTqna4q&SmP}q~O=m|sD{+f(eiYQ^4N-n&6+LIQV&I>Imy_zNkLq{+)1K5`k+NK1#?+hSLhcw>&eS3g+Zq2xaHuoY-aENV<J+)Q?{%z7Ya*jwAKb9V37bN)3Lp*to<O)L%_7+JcJk$l9V?!kwp!9NbBEnYOty-Q(pLGitSfEVVdU)|w3Ol4WVZ(Kr?}+^p$KX`f)60NB+rCN(;;she?q`Z9tX=8St+6`Y%H2`@&=lIvy$c2Qysum*;I^TQqBF>z-@Eeb$U4-hT-BfS_iUAJJ?vcD#ln8^Kk9w0_+wkd)UFMeh-Mp3P@WD9`9~I%mktlcqtp45V^>>{Q<aqFQ5Oz`1^~sg-<!0B+iljX@kdd}MHih%Vgc}!35p05d5SV=8=on;_@cA~SkBghO%~Ji09+he-LdB4=ctJn(@&(7vz`kJ!hdY~v-nok9&U*X$uld|wTqreSq8C(sRh%#Ze4{GmwD>%QaIPZFfceugsT@WLV1vel||X_P`Hnjk~!LBYM!ePxxP?#qm5DZctWaNJ&#?L&O899<F;Qf-6Dq7$O7RiQ@>+2&XxM&2JI1P<bkoiSadY9qL#-c@Knf{`IDBvJ+vs;eSB2df7TyW+ctnPqs*JV%6we`qsz^ti!4|6R81KlfOk%`t3@r8fVM-vScas^A?-MRU58q>(XP&4la|s)_XaoADOf!8qE_Yelfz2c-?#T_qbug>WwD<e+H|z@5ytHonH-KtrA-N^6fZ!aSarboOM_|8Ymplb{>{vU)e!9_Sg;d#W%%CH-H<cQy@=*N8Xht29__nsL2Rh~GyJgv?d?Y%GQB@%=B{7tW~#V+eararan<`VmDs!op$w8Vz}}g7mwus)6qzlw@ypc&P~mE&9R$R(G%)>Oi+$i)V3OCv+PwvCR}dL}Qt7TU@W$Se<y$xu+5nFgx%OZem(LQP*fG%L!<T1p8H|6#godB;Tk0xa@qjj;cS;(gWmKM$QNOhi|AWkJ#{U1RVlI~;fNxAU3-RRZGg&M7TX!;~srD1J&?eI#t({u<Rp!<IQw#oOqe6$FKDsxc+`L(NOAnI?cNk?sG5MWyBMbQm`o5>G2xxI6hhtEz$e=q&`OHG!aXvVIu9C9+-Kgr!XjVJKL!uunemaq%?_`Hl3gh!+{j4$RF60*yl*5bY8oIm_4>*d5D4?kt#dEhTjcv-eV5$HwM#l-&&-X2&^{p7kvNjU%JWvGbM0KXb9{^hm<-w`tC(F)wF5Z0(z%yYKB6U@*tFG(1kYmm@I$x33`gRLvnqP#R7Y0ps*1bv)-S|A1D`yr)Uzq>d(3ld3A70ZDk}L9tM9^iY@M0Rz9XJ`Wq7wh1zs2&tMC&Z?h9_d%JyqOCN6!e;0vee8o!p5kr`8#pxr67>L*KX<37@U2KEyK2VBg*@{7&RzV0n#*0_P`AzD5KI^PT3SF^hA=#x5H@B3{$!dj9nGYqtK(d@WfNK(9)g7FkhB>i9y26V9-64Yq$$FAslTdyoBy5MO3aixkqS?G7~lPF+2(7YYHJtfJSQRMEC|;OCb_2uy>THKw5em$r}wVB8ieE4_nj|55()dzK2eq?0?{@8k29kB@-(^QE;`PHR0gXOb}u12l{sCPJKR(%&ZGU<h;NmDYuHo-M8?`=&cVnjCSNSw<DjYA`#6g&SlK=-GB`oU=D-&yBimwww9}TZ_(O0j06e8e=%%p}~I?*49oufaFfd;8vQq(1dM*oUKmbVWjn_UWGPZN$p3uV@W~)NX1!mdba!0^rPSOcyq7~ppA=z^W`H+Cdwa~NIe5b5%Og*Nr;A_Y5fQ>9%sHW7C>EjD7MRE%o?q5ejaZObXvkvc{Br-xhj@bciu;~sN%TD8%B}8ExFR`Ogh66hnWqOz*G?u?lGTZL8vz@k`_p_{G^Px`Cu~YBYKOl``=U>L8(%yJIGW+lP$mXfA$fZ8+-Wi68~<?JB(wtm+V#>WtLdRs|KF+d+vT@u9@@T`<zJP`Yv{&rM1>>fd{4S=pdYJ`;ol*J6b#5{Sr;=ste$Su@8rvL$RDTji-q5p=ulRnMV3puD!{IFVW=tl38I7yKuf-j}=KGAI-2K_j-iR5J|5=dW@D|4g*vvAk+FmduZ5|Sq2sL&byh2Ha47AEH+JNtlNYT$zUzmefQYH$raisr}6P>#AHmktL4g;0o83A5iJMDmH6>qR0fFtj8ABLhOPBrB&ynzQ5S?Ojza-rp;6ti=%eFsPR`a7XfU?tH>+Sw8QbfYUYT(u<$WdN`VvGqqLT;%CSyf=8JaL09!}($Fpn@y=Z6d^WMw$-jE5c>$md}VH6~$mP*eyI3YIMz9cP7+>WEpAjbH`Dbu}s<cX+Ocx%&afYvl_uzZ!FA&Fl97vVh>~^-s(B2TuhvstN9KY20b9V;!vG$=U9=^&>Fnlm3tR<H$*#<S-OI-4F)$BIj~TEkOrrpW(oyd>#yl{18OMX(2R1-4b9UcE`@KR5=N>3;}N4ZDp=PEZZ)7vF80Slm_PN4XD9VDOHSXhgtObI`!el7o||jl3}q%l`25*#UX)jR>*QL^ZX&nU?Izf$MzMYvzna*02+JDF2JxW2CF@b_tFh>*@TTX5)hRY?%rKe;8zSNEa}}B%B*#D=sRl=lGmYn;(>*D8L52WA4p5M=Y_v2U3I!j?}75K;nK;1khcyZg71i(G=gPH?nN8rj|cNP*VsUG5V(aK3hU$}52XwW;M=b}_-eu0q#o6mwQZp96I^6xy;8eAQ9~m<I+T7e;>Q?9*46nwo@+i1x%+afOF3c&I(i@?dSYb^c|-SXvP_vxe(qNN$iPOWuv6<n3ibNLRRdTAhPL1WD3*S3<jGVMHwzc?jD$Eo9nMi+dzP~ot<qK5S9d8MJxEGk<3JoqpadJ?s>cwfzf-}WO}-E7l53}N_(MPtVKTrR!H1tM=d6UF_rcwnAIU4{4Dz<Z8<_6)GWzIXx{_y_*(K9C0jJ+<udk2TiRlhTx92U&_IbnJqh0u6V0CHrP!bs#K5=tkiNbbZ1$iW>fy!%M%F~id(NUH@Lnj3l`Ousfa(WpS>8RsCzZjtVceJ1(vZZLz+k1Z4eE@Rgvv7EYi#2v5S4QU4iMdLKY(B^COVOhW+t6jf6}{^o%;f`s>asc{F{7MTCco{pL1WgC?$L6!ZOR~H>x_rOs(`aHq0sI=&p%U&ZcHA3{7V{3Q$vKZ{;8Ftm0pRY=yg^q)z-A3z8UQ8Wo%wLAv!%Is&v=H3@~^Yj8r;BAWH`{4)93Fd=i#y$9JCtSA0Jvq&dz2(%`G>EajtkVi6N0#*id^A21;ze*+S<LV}=d8MS}u+!^rz>BRfQ_C_nd(kD%bD#I5I4nxNHj&5x<{Tlt+!-G!$?Aj&oP~rKRRlWM69Kbd%Y<np*GQf0Xr86r;6#&ysLICyjef04p?Nd<QouE%ABReEBaP^Fueam7H<FGSpoJ7xXcDr#7Y4;Ewfq*4Y&VPD%rVpXo$3)ux#)!b<oH@=GBuuK+4&$qNX?-<gQcSMOQL%Sppj(@PBP*6a(uf1>EvpW8-`G*+O+03-G}IsLd$}5agh@g70v=bkNXe+uRTvB9^0qf2=&h7!Jv8!^Z6^JHcv?5Qpa6qu2{{uaAoH=_^}ed}1vrtV;LiYEiQ4Gn_79hBZK(3{r>aX%c<{;LIhmPt`s%`%E{Dz<*#Y8_bxhiij&LHOJeVivffW^5C-iBCyh`NCOss#N7vP}PimyDT$&=UjVH^NDdu)`RHjWm%E=)mHcGz5FHf+nU*WGbI@&!e(hfm$Z=!Byx>@rsK@qt4B*bu#pULf~wCGLR2!Bc5WU?CP9f7Qx915b1A);16F)s4yUxj39?l!12`FoN|<7P1kx*IvDJkobJtpT8I6>Z&)Zcd8rZvl%10h13^+rctWMRfYPv;v1Cdpw5~}`DT@bk!5n@0S+CXg<+XK(HMv-<rlTOCMfe8R_VCW-<iEX%`^+!995{m(U!|dZA@jjrD=$gulZzy<YQf{`w<#|j5zAAaIZmX*qEE2EHhVpQmA?7wf3N5oQV;o9fGy059417fArFogf+RcPbb){c1{ks7)Pe6F4y6HxA1gLsJRSc%$LkV!T+-|Bs<fZZ?kV$JYOux873K_P7LUV-z?TpUF|ijG>OM3sHeOwW*9CX9R*`}>YDj*C_%p#k}b@bSgh=${rP*#EXsGOO*5z(K{@T5P~b|Wl;jutbdT4XOeCPbjjxs#k<4jg?CYYFm2`Vs`!g@7g|9Nj`d3ojPNZe0p$Eq5p-zT-1@~PZC~H-y44r<Rcz7)e<1J5C>Gp+(DN7r%icJ&D69*<+mU4e_d)iUkrj&YkV)`=G%UsUk3SnT)lcM2)4YG)NRzvIvIw;t%rGH&Vnz}6FMM3`+zB*C}#=J<{mr$CVK_Y;iD~mxc!|%IaqFUVi(8hf4>Le&7O>6g8DYv56J1`pyw(bx2#;!1a{i$tQ$tYS2a0TC~ok&$aB4D$bjZ2*1#-RJs_b}vrY0U$URHv;eZauS#1wK4v%b#8EQ|b9U*_ur7%D+u@DW4bjSrAXFk!iwu3cZc1-f-hzqd*T^-_2X~wh3VKq<PIRuWNq~<x|8O*ws>D>pM@2x%s{kVMLcwnu~%3WUZ4Ptv~9I7}Pt6+s9{$-^YU!gBqPsdGYIM4GfOt(JeBhx+=tXrhXAn-@`uhsEn^`>d||dV&oAeH2fg0v=S(M3@F(cG}*@h1Tu!b5eLJ*Kvm$#%m~72k-eTe1*)NfC)Q(!m8?Ju3*sFw@2;MdN`|$)4A_b`={J_$5<6d$p!N4zvI1foYS`k}8m7>$qD;){p~5~lTl;WJ5jy506?}yVa59EXxsTjVn>q*skS5f=MhX9!+D^h6rsR9|Hs!J`*TSyyL-Hbg4CbhyI+cc`b#z6QcWYDpTHbv={t@sD^x|!w6l^<a)<@4Wl`CQ*y=-YaqO{5+kWuWyME_Du2H2A*3$4ic;s5IWqz?A)6Itt>m|9xfy%?v$5Kl6xHuoadcM}hj5OnDiL6Czz_h(WHuM5ct0D^^;5IrnUJupT#XT2DF4R9Id;3V#|ZL$VPP7Y<Yq>~C%N`p8V^VPKzFSn1hv$5;?uGDKG%xNpsqT5Jbk?qqi`({yR*8DN6c5v}L*&wNGX(Xz_BnaO<nK8h&!pln=pxVGfo~!%j_Dh$ds`1Lr<)Y@X$0*z%Q70h&9O|toLdDGLZq3;rI`di80CW98Ox2cbCMlZRm+H@<GHZ`#C;G8tt1di`9H&Wbih(nDtffLfXW+?B#62@Bv8(6HK{|H`57#~I{olEI0y9hUe*Np#|K1XX&^8TVYQjlr1<Y|H`NDooq>j6?bV#KbD|W$x+b&7+a}e3^;Ql7lk75bnO*{NP%e^IY!TUY4EIq0!rza)sm@?W!QIKePl)Y3wRm5^astVH<Ll-+)3)>v4)*G&S>H;1Jda)`UQejX;ibQE1GqLr|O%1-+jSQh>+>1MpmGsheCTUK_(pBZ9?;b#|`T^&4#p+2=6S`Fx86$Q4(FeeU(+KuQU9N`!km6D70;jvXbeM4Z%}KdI;NInb0%=LfC|n*zzrNtUC?&rV%OUN6OuSU|+x9*bzhGSvu)aNcll7C{vOMFhI?&{|&G@E7eHybjV?>PXQ|7@_Q)gkOZ{@=?TCNb@PuaZ-JE`DhTjRQ6K<^{%95eYHt7?|(OfTZOh>nYDI7$#f5F1vM-j9^`!v$X(=}6AwhPbcSx!C|_jAE-kO_)SFb!n?>p(RdnT)AY*iys}TO>}B?=)#zy#rDT>#b;14e4T0lav#Ve95UgW%@Hx~AYlfeyKk+h^^T-|s>`HFhScbG0M+yDN7HqxX6xlXb$v5cI6ZmhZ#x@icnnLl-Ba|nn^$@xb>@FX=yK8Bk*o%`Ic(42Y4S;N){gQ{by0`6woUzI&|>8D+@SBqMb~`q9K;7DoN(+!yq3$SX;eqL<r^3t=t4!2Ko#B2E-rc_*SApUI@3p>lu5SS$Oozp(mmJdWYuM$XhCq#t20hqS+esFl}Uam`NK_O1Jn>Hgsf^J7oeN%+<K8dL4Wn5wAf|fw)!0gxq?F=0eb8vtePgxQ#jwMCR4_-ngWLZ>@pekXqj>Eud8=zlw(9Bv0Jdeq9$$+nUmC@tOm|+(=*2JI&0|Dcz<ZSh;};DF(3=y(+=S#)*ySoZ?e=ug;iPgw~};7W8po;-vtDBC@o5w|HRwEoZhuTD0f`Kw1C;LeiG&7ac4+={LoE0!nLK5vcsckm?x*Sb;h6)nCOfg2fEC7d<R-U;jfC^vYIixrIGlcF)N;jTc1&dfnEm&XkHvEb+Rf7@eto51~3eX$OTE)n%e2Lan>s5MGg-+x*|1y0%Vzi1W}_U@KGxsO-D=eTx2nEWZ}(2RH-PMfdzS9=eZLAj76z9c^Mv^5Bk_#dJgVUq`;SIgn-Bk@^1UEDA({RlkD^OgQV%Rmyn`H{GBXXX=%d!T(fqA4qBB_Nb(nU&DE9D;zbowG*a)QOG}hZv%}&z%L*jZYlyb6z^57{TN;Djb8+|8_(n~b{Cy2u_Ykp?ucIpbg!-6A(Al-zVMzk3U&PYb3t$s>je=_cIO(>HL1o5AMj%#GVlgv27{S0492_oEPqTp>W%NuLaDBLn9BuE6_@*P@a9NUg1lN<v5nH}2NS+_W(IN&X%%X_|qn&}1#K#!nWhSS|+UDAw9aI@n9#)JnY(}C=%G;{~C&>h!xBd+v>P~`mZbWl;){qi|{G`Z}!GT@tvxKi%TA=k9LRx7x^pS&u5bf}_Rx}+mL8={bH2N|@w!rdbOY;~j<nt?MpUD9aFZVQ6pmjIn!;s)6%#2k5|Bt-YXoV?-hIx?MRt*_6o-p1L{-$|rFl)SFqd?|&78gBlj0%Q#4i2e`uzT*QYi1LJDq#g&`F(g&Iqvp)asX?)tz8=o1Y>c@N*dm|2VCu$^+Fk|)`ic$bGKyDnrlPlpkcMT$$;81F9luYkg-%Lwnjf$IC02#V+h((FmK%62=5pHj2C1trGO%n0^RFw=!#3Ba}k$ZV#iaM7W;nCD0+<cVXpiwbEL$=_ruX-_Rl7$fpND}$2+AOR0&hcesXy6y;gpA=QwT@*TLcfPU7jxC1Uf~+RHOa;Ha1HFWStQdVDC{U=CZ$2b-%~0t$*wgE^(wS#{{7&vTwJs#DubgW14Ux>m}4MRJc3?Tcd;;M0qWvTZr)^ltK>{;I9XegYvw{0RhR3@CQJM9t_9?zJK*M(vN#Lj+P6?PhN4!@JSVzN_?U0A+T&1qVhEQtMf5UOZ4Z?@|ocdGVP9lef|8Pg)-4F_b=xfyv1}KHnzaF3Uq0W(;B;6k<2Mgu@i>Cvrhd*+&&378y@nD7z2F#EPR@_=FglG9}MZ8}C*;WW%i??eET*BY4TD-<|*mL6<7Vw6_{WhpXt!v3sdzwOch{;@%doEuPCVG6;B?5+o_i%214g>0g|Sn`&WA-&t?|tDwT&Z4Xzq^AK*u{@B%e;gYrB-)YusUP^RGZvoA}s&jMDq=bqL{MqQLd}3|L$t20J!iqc|<)|adPvS44G*p!DW~}8r2M4EDCzNh`ws&AL34LIf4^odAUQ#mcr1K?bzwu*Hc;D^jA%ci+B4ewW&>a*c$f)TA5cIq4^pW*;X*OPzfMWzEz>jc39}R1(BkU=Gu+I`+ig4d@4krbZbrLN0Sli8c+16Umy^82#h)bWXvh(y1K2jp$Yi8$#dI8+Hs=GkHF5;RQX|kbVk;VTZGQ{H7ZKp?AeEL;xFd?sPVw0BjLvvFNa^Cfrz4J83wav3rlO|n%d$cu4arAWI_4F~V;pCmGEeJ=<k(jw=q+q~cWgrbK*aD24S3?qhKt}fS6K0m!J2`*EUbESYMcGhP?Ov?8h@H2D$e(Dlg0xk6;&|J>u7^QN>1ud_+F78$M6?S>U`nyFAm{62<;c&{^TY+%b){4G9Eyc1b;9C>-Vdg>6F59!X83}N7G72M-DWe;1zzTf%-CXJRk|A-FH?{Fp1QePU2AzgkN4|^3c-d@!Y3r%9)T>2w{uEpb2VS`?t-@uPrD<DY2=5r5~wgw-vwo}n_gTV!o6?EHS9P~JlL1Vle>-uW(nFDrRuTpZqsMihHLwdN~h<B*UXFydjo)wF0{4rj8oal*xCVOc2jmB2U}oDc%{V!sA{S*wY-Rl(g`3<V>zExB%rh|D!0j)+gLsU3R4`QhK<avS+in#y;cc=f=ZVbMQ!DHUz>;UT}*=Qk5PZ$m<n%vqBurW{^*0~CJ8}zaHO0DFAsiX%pH@^aKo$dOO(Q56Uh)~uLevc*%pGvbhz8YgIcx`Jm)HJSvFf79yBMpY$ZJj6dHjjJfQoox*?Lrq?TD_hjmv1P<*+y#<{yz*V=YMP6=8elC`5q7YDNGQMn^1$Z%sc$;56Qv$OQ3kPTnkBGnyy5$efnCqQa7u6{ZE=RQVDN8!5gAg!wNK+ov`&RRRWLPjCzZq~~Ad^Xr>Y_BUJ`y_r^6|$;S`KgxO+M<r9Tl^zpE14lfN@Jk3ARp<%qRvo%GFOoWdNLmVdYEqU&1ey#m90a*u8keRW+^AwWM3MNpod#_SdVdSJAiGd@4%z9$$mH!b~Mf0WB1tV|A17p24W8ybhFw@8nGMgQu4#Q1rfi8L57VU;v5a#eT)m}?|Z@Ghi}4nqsu)l^Q`a``JRnT+bcW<GpGi$WZnN)ijt*4cWy#D_dd>Is8tV@RPOBzsuaE`>jBWPG=x=0ox}!=Yq8>2f!|qw8k9Ey#eJX6dU{F#jFw6!1V;n`;OB=5CZYp11*kx=urfojk?<q=pfc`nL~GOkgBT{~>nBoOzilA+N6Lb_6(COE8|ODUp)1Ac`VS3kzjNSU2lB}$v>8||Zh_Exhd$|h79BB@(UP+;nsC1C?XzMQg?Ec(jhDbM?7obA%MM@E9pH6#EB4yA1-Qfd;MBfhj`?o%$C>lJlU^et0;XHP!U{#9GeB!@hk*R5gg4+l3L&wwL!>XiX+8!%$s0|;-uiDD6uWNH$e24bCpGCh1FI7$d}fXbmO0ScyEgVR?MAgzP-LZl&!ye&0vP@jMJjv?VesGv2Qsht^-ngt&Vxa)cS|>hfj_OjQmRbJ#jz@g+b*8Hb&|fcn(#veAw;>DU@6n>voe{*u*lWZ8Z}o*32j8yYchh*B5<&(gP^aiA>~~56uJ}*LLjs&E=NzRkbo}(QLo~nM?I0XjCs7vGE*yO&8<v$IS?cL<NMQ{p}}A5)Sp2NFkf*vhDg2dM-DPw44o~B$-5+mvTHGt$;h1HtRY2}-)O`p21|~TXo)l_4&7e5SOOU{S$)Y$kQ#o#EFia}0c_!FV0ZP_L^>iW{n@t>{!6uNn<aDsT&p23k8jf(9%38odS_;wlzbR|9XIHy<6@VY76i_#XKGdC&Q%Hcekf4#P3cv%veC-V>yk7Ck^Q1^9w8x`<M@BVi@oW03I&zG+uwqD&W60!?mjGFpqD$q7+Q^4vb$2m71WY@l)Zbj$biNZXPgooRQSD7glxPoByx0}N3H(9tDSF$g>nTSXPg1e2y*iBU@c~67Wl25yxF6(dqNz2{|(2pdNXnQA23>LjnM1jFPPkK&=;yI`^%lQmiO0qgXT^U&xp9IPy;7~wYD<9(ZTse%G0+#4dSm{Ay@beqRCTeLCDHMbvn3S^1AQ+FwNAOj6*imp6U?+g2;{y_s|d;r1G}z!C_>h_R?;w@mcCm*~E7hQPWwp+EN;gGE*`=CmPgveTjjV%H|w`oq`TfTK3SE??tvh9rlJ>C-e7pYkc9S87`ux=V%Hg<?`_#6XrIJHB-A0OFn$@EnA2WD&%W1BpYoF7Z|71`^1{{`PEi)w@3i#Ed)JAgIX?T%ao=8OL6V1>{9?53RW7{0wuk99shn=JUK47-$hS{B>f6us_XkN#5!Q&*UpMzEZ1yAythLLy3LXvgdi*c-~hg)iavgWwD$d!GV3M%ctKzeUGf#koMMj?A&4p0J+C2-Ccdi!g%)+VD@nk4Usbgm>Os71!|8<#`ULzj$swnzxun>J#n2as7R1!oV0B6}B!w1`so)}k-}6OS-}$<lbmU@`i87v1_Nq=?kM@t}xyx$9+*W~l`qwtLaP#&h&{#t%$tc*!-j}OUdkL7EQkmVZ$NMYY*A3_2{Lii7p-R}fH{~NbdYX$b*L>ci0ghu)R(lwT&A0oaN8n=yZOBk~v+-L36$)KA({?zQLQhL$L?rQAYJ%y%$E0Fmf)>n2{~_ZVU142BVm;rg!fTTUj@GQsf>NMIxykBa5OhD0aH5OcGTm^tcjTLf>Q4MK;{5O=4k~AUki>#__uH{k)gTY;oyb^q*H!{`eo>G!6;d;=p6k<^t=4lR0k?phcTA;_b!WUgc-Dm?$hbQdr(P9l&ht*|KlTkNwbVUZ<EV0*)@q?rjV#qE&Kjg$@#A|6Dzm5J(ceA%z~%PNwX=1jcmq9*e>pKwvzi-I`zxeOR<eGFWyP<zp0AS|=Ma^n2VZZcSn9q^NE8Lo4fzSm_o=Xw`eG;Rb?9k{wf1>2_2HVV7@$@AOF4Zju4$kIbFh@ki2Y2W@We52j+Uv!V90S^!&0ydafFOFUuIC=P`BzispyrZ3>Ev-cr}0y=MrEY3x&#V#BGuIB<|gv9A5|jZzR$N-mw<)lf?L=|2WAx^K3qMp8`i83c=|HK&3P(o)Cd&IpfqmOZG-cGA_r(2cwZVI~y1)JsEEkSmt6x0V>u1_h>|cP#9xh9@61TF0`&PE3@QAV09fl_cwq17&4Lfy4$X$PH_ac@kP63-bJt*Q1-20PHw8qQv)W^5*IsIyr#5XYQd}N(yO%`+lau~*{&XPg_gUItEVZ@hn?iu6>3yFnnBa1cG<nhU^jBBTkR@VnjwlN4x0jzE#`smf7jD|fCfQt2<(ncCp_bC$7`=#(a`%t<Q#4wADfNNhBUHHcA#qK@ii=>;}zfCw(S=X2w0wZU}hLELV<80ilJI@7M{fCTe~mS0AzKBfvO$HNj+oYFbYFg2&W54M*f=4;B#));LPf~DAg#=N2%B(b!ziPOsR@;brH;9*SATioSbs-baiSXHs=|EVe&^~B4VwA#CV88wmDrD#EZDyxnm>mk_ZHt{{_Heo+g9G*;wf><H>{w+&fATP8Hno9eU3+1nf}<yRwVb{}XHhc44<jDm3xaa&du@I!GM^QY>5fA27!d&A<5Pn@+#Ld4-e<U|6j~Gf7t6UApQadzUMeN)a-z=~9c`^rn~@76a#KK^^lLb-_ZP(_1B3!ghJS^?BFlvL^QAW3c;6ul*9FDV0pfuP_WyReNeMYpP_HCdj&0-wPnf6N~{}i&DKOmUmz1;F@NqcU^^j9kZ7D0&eu+k~0-KsvPu}43UZAwC$q%YzOYm%cBdn3fF#lj1upJhOJ8DFZeg{mUwXoS1fek|7}*)4}OxIcXmK)#6Y1_7>~#V;G_Z9w13whLv(EYnEaZV8VRc3BHyc6wJTC$utA%5`IBuS>?ASfE5QjUB*`??N#rd7f1w_J)^n`@!?r{%q;LeZbh^J+H`^ZMcDq(XL#|(+5T^98TsyYt&rHjS(r>c$W#E-?E&=jFpX2OZKB9-Ym|qYn$&~*8T`=O6G>$O#E5_*4O~y>Y8F`OhANgox(tp^aa3*Sc4kLl;R@sj9!~uhJUlj>-nVzQ=#%I;%t%HmwsPhR8@#CFsCf~A*B}V+jsw`I}i`8Z(v<^gli9l5{<Ts-UNd%$fMp8zNhCn20%#(<Bau5A?0}{6&iHFmpJ5p~879oDUI8!#U2XE<gI)t@!J#f2UE%UhJ@_T7M%1!2FJN4P&nTw*p{3eJ6e)8m7fX{Al1brCX@YO*XRNn1td11Y|eh9&QC$b?37Z}XGATe#yW9jsrRysOGv6+>Gu?qOfxf786&J%$PrG;7|@dR#X9&ki6%HhERifJAmi4^MYh2%SCR#Nyfcd+O0%eAZ7AKkD4Dw%>Pei|L6L5qsN3fCS#sSv#in;7@~GqR&}$+VT6++__U&fB&FOL8q6gTJpX=`{KVbQF;&Q$Sw0u1)&2swYxI!@#;4p%4C4<wpt#bqH{;_{C8L74Kn~;%Ces_`mxn90xuH)gjfy^gqMSZ{O__%dk3ga>ezcM6Jbx8X<s_PxkPqf(E3D(0eQigx{|>qhl+UNQgL1to>jGT%#|{8jVH)e_uQt#)&}**$s#rNSffzF}Y%nw}C%x*x*IzG=pKi8X>FL@_n0P@MxGw8isq|exIoiu;~fa^>=`7$G?&er6NdR7;USQiQ1}?noZkl1jowoR{mlnEA}5Lqdr=gE~E2MfFF0;)80lG^*5kYEC$Lx#?Ca~gfT)h4j6NZgIkW8m>6U-)TS6Ns>$U`R9XQ)OfK`dMw$0o>Yxwh>8-JhDy%K>1<(C|S+610`uEX-4GFHMgYP*=ikh46x2Uo8Q<yjsI)ETA4orEFmXY$L&~hI9CL>X`(Ma2GfAZ&tp>V-K$u8#X`z(#drE=`tlBcbg<gm)ksyJ$_VeR!A;g12l<$5}f&F1TWuYX_@IqfvSX&QA{1fJ?n^HD|BavF)zEVkV%|7cW^!Yz7A3w?l&HlEC_5~A`hQ1~u-S<=Q|s(3yN2&_*9U?PZiEB4Wr`nw**r;529@#j9B)Yz*+CE`_Zyh;BWJtpfQYRY$*F{mdoI3(vj-rXP!J0*U?&{BoM-I`i+*Su^q>^_~oc5d-te9M5nu_5thFC<-~)9kx!%~|f*NkmW9d!4L=mTB>JI&4jJA69#K5l}&Xv(sVRb+|xRiJr_XHBH26AJ=B9@HBbJ8BQt)AkgKCeojob-OLrL05SwZQxdtq^%%`+-obGjKu0AeFn2t2h^|)2eAFjT`M=x=RmG7jM}hmG*P(fk?++_5Rgy~45-IaX{^h=U=tSRN@oQB~kLk|~bK?}Pfd@Atg{=#)-45B;HU1nKp{?ebNP|f9tGlsdoIQ;Cdzu|{BeOQ?;m?SG0N&vvUCQI2spZAq*G>-!41Ke!FR%aRkG#&Cs-sLuTGcUzi7z(j#<7nIEe!il`7IvCL!c<o6GWyiQG{ina89zdu1Vu(8dyhX&H_l2fJu5k^~asJtuh-6e&Nh^W<ns)xgN!$=o-IJcm2AR4<b^UOkQWIP&%EBRVn_NHq*M}uH+}PXA?N=MOyzx-G;W*6#|TVAM<4gH$AFCB&-~zU)vyE{gSUy*E=WQ3t;YlzMh9NCh)zNFznr&XXG!be;%X%E&f#Y9ivN~^Il;5ma}my-=!I&Ys}wUYO#Q<r&%x%HvQ)RHBX5Ald~*LZImGwUy7H0Jw_m$9Gs?GHVJ!l!;H;Y(0jpY7G##SVbvpoQnb`>H0{x4Nh#B$zY{2q0ZiqH(KoS+9^p%QayyDfMpsu+A-hfMaU6Nu5nWz(GzBv5du)YEH*^`0B=JKWcAb`0I@~QA=O#KqEUOsieK0BW=CfoKnY4wFf_pm(nh-Xm3@DDn*M=0xxvU7OYwx?8bglAD9#Fj@7N$s+wPDUu1H=IMKMY2@<(c%fH|jU|C|+9mU{<+?XRY?4CSOa33xVS<k>e^xJej=YFoVq2QhYP!XQld@{yjjQ!z`LF>tXTbX^(+!tsdwoLX%<fhT%RbCL7C6)2hnKb=pfBblm{`mN6+(rrO9|zgkAyzf-C@12KD3D-kD|#%52CfMVGmYae7eu@a8%zb$3?*d=P)SQ%q5KaG-=sI|*~zd5c23{C=Jb+-c;tmqMmY9Yux>1V-g^^gS=GS5ltO)wE~lm$mneo`)u3Pf7UB&HNLS?I9!j;j6_*q16im-`8Z9)$iPQMRSE>!)b$Y%zE`Bh||zUJRAP!(?qw_K%Rjt$I(+3(Rny6J612xRlAIXCKXXA)<rQ2BsB5g@fI~L_$If!oaz;|JzvxcLc|j!zblJGN0JNGNMDdA6D6aYeH<0`!`H+y^yS~AgLK+YeOvEuX)Fc`(zEA9}eH?fXkfxELi%PprE#fNgY#IbC%uCdi<yVlty~PNq^OM`8|FIKk}Gdm=fte6)bDqzc*31Un>s(plyybj6gw!-&WzG5{2rupytMDoL?T)v969yDTRDRl574WrGS=9Xah+<-kAfsSbzxvt0VM-*I~PQu!oI@*gNj+pVBfPt2<#c`uB51N{NRDFwHqv6o8vjF@*J0cPg{om{mQYr3ajC{&Hcafa9D8cq1euAsd#59xX~~(vdR8a5{r7edXU~y{ZxS5|D}d4v*pO)vo@!*X|g@e&W*(cuj{DS?vsp?G>qrg9YJu;|K9QRhO;YISM)Q8x99$M|pGEV(Zw3ALRvUXu=#Yz@Gu9gM$3!-+_{4SjVD8GN1=~^KF!hkHn!9q<UQ*arf`7G>dQv5(OPJPO`V|8~)6j=0YXh-vG-5X)DB9A_S7f6CKUQFfVEGZ0ubjN~eT<>JW&wy5^JuHm8yz;%?MqI}B8f-4pH3Dd^ynBY^}~kCJg^b?dF1S{g0G5y=&digGEPy6>Ro0%2!6LAh1WZSVz_t-S~n$=zCK=R)#+8;aZ!hEx7fq@uK{%qM-WL<Ts8Lo+sdYnT!n9;o~50C?)AzH**b?`LYOW(S%i#0K-B^}b-@eeE9dvyU)72G3T1@0y;8lZjv{r^2?FSuy}>9C^J1J8}Y}pgVyf0hDfU*0!gQ?UOK}GX=HAWcT&D4Bh--8E9(Z^2Wm%a`h~v`68k}2RKL9il9#AKr*327=hSgduau_`Tzf+=@_gihN#aqVq_>r_7}59(ECd9O_aChlj+|ag)sGv@m5MiXBn!+1jWk7;gI^J#QvuqY&6}N+t)_vb3#d>f!&dS%qwC)8-k<imMIKQBM%CkB)zlo+&bw=sU=taB1kcCekZ8z@qPRRjJ@fpS7xb9Fc>*FR~9}Rx+quguLp}DHjaJ6+_7*rMV3k&hJLPOF!pag=*$}}(j(-OML%;;Ywob#{$cG6F!E(CDG7=aOPO=`n9wIWCO*CH!z~?D`U0d}C@Mrgo|xBmkg9<`hk78lJWBX|qT-o){j*jARDaDD5Kj?(fs`JNYmv|i_{cs7)~7S3znN&+P}&TlMDRlm6k+qlSiW-9@&hG0h4NX7$2US9ndV=``Dg4?Ce*Jg!oI%3Qz=9qWB_81@1=mg+YbC6j^e+vP-Y!9Jx73!IqFJkyEkGiWZU(MfXs%7)s>NjSXG2){F3{z;sXY;M|akP>=v{P+GlNRCS^!%UD#9$l4)NFXJRH9T7a`LKXvM~ikLs1*T9gk&Q>_`O#sRVez?!r28gdzyJtRtm!-3i<ca=*5}JR?+Yvm=)zMGrQgaVexP7b4#>w!N1TS~~;I+v7S{y}o3nyT})=N5$8~c3J!K**Q)YgZaEJ2g2rgvhu3I-Q#0Sd1VcCZHb)f*<;h3e))OlX5dK>}h(<@H$u4h?VmNc=u+2E#$9e<?W}0z$2l*KfKpU8PM~-cyK4M&T>SH@rgCm+s(jH($-|uzC$TY!5!p0+|*T=-3Z0ZV;zMShbtrK*oDbz7dvuME}XUcM7h9K?iaIC-1C^m`3l!Z$3h8Pj2-n1j7yYa9+!1ro~`#k2A!kmnGsKx-&d!)XjP>@V}wG1E~)9_o~CNB1^cbj6f%}V@7=H(G&Sy-JxQz%rUTU`IO<DqFPj>w|tt?Q5ZCtAsoyWy;nyq?i~MyHU0XQn{TryF6M(EA=7t)o~|xlNt%~e+vb#G@!%-T^Y4jXdC@<*XprS(UXoNtUOIy8>k8IEr7XJH;SXymPpsHow;>FH+X?-Co%d2#gwZG;ckdm(-VEJ}1P@MlIG|<SaL{tMt*c<6MQo~oC?k6aNF+B?!qCb+<<pW1e?XOLog(w2x6wA#8L9COpOvK1-N!k<cx83s)nsi$dI-!+gXX-n9e0YD)D@3^hV^z4i5n|=wa&|e#~tc2M-H(BP)b=$Dp(<)d`zNNoo=9UHC|LSQ3gd2WR$y|eZsHX?yqcmB{48&@6w}wt6J{_cXp~d>pP)FIm7#hy2wzEdqqr#{udg_tg+~!4ZrcSmMp<?pxMRA9RH_A;iqzWc~*42Rb|^9ep)(rJ<J`h&{ns9+@WLlaGv5}mGqL`6n^1|6NExGkKN@BWg6nC@Jj2IdVGhSvkF}*7~zXxw+n$Gkv!f2a{c1QLD<=?P}V)Rb)EDjd1GlM!(RZc<%ZK~@4aHulcAKGX|Z^Im%(UnIh|qgI@(1y@v^G0F$DI!rs=3@)@CUOmmBv4O26}A-2fT{x=$3QRBGAP`TxYQH%fHxr`xh4f=i{gV!OJPHkhAJ!v4~E{<Be+j7dzEwjZD*fQhp)K^>YZY$T@3MGi+Dt1B*~AanmAv!dor!m@PjrF2j`SB;bfCj?fi@?{^i^jvb{L}C%?#M~WAYi9w(fUNryk>)OU9Bq0fF>>2?4m0WGN9?&ToUTd!_?kj8TejQj7E31a{9K|_`m_2Qe{}_tmAg-v0x=PXp))D=+7xkoW9HvX)@OV-ENJd-CYZSUxTnycno8#VQ6yH*^gfGsj}Ec0>JSja5h_xNQHGk<(u^5VI7fh@25bR_eekk&zGP8Ey3yVQmg`QhQz|8CC5Ox3nIvPjsE7=H?8Fx~_qn56Zz4Lv{OtB0Y*C?KLmEVjw6Sf$Qr>L&qTblH!R9evEiXrnc=t6i`IH&B=m(Nx!VzfzYBL4*xxnyRPje?R-J(uAsOy{bz!HKFLR74=lK7Po?J<j-Z-c4t<G0a_6l+d&cFSFdTz<w!j`wl)jPHbqiphmabn^!DT$0igtXIp@2yd56%iBiwSGOL!bu7p24%lT_``qAM_uD*V8Xn@GE<2K5D4<aCp{%IvN0um)gX6O1s41OH+|I`1%*pnl2HJBj#Q54`u@c)84rer%B7sugE=QQfbq}EP3$P_WX>FM`Wgn>})&qT`;(v}BiB&iOo%KS<^ql*hmHjo8C4zO3KcgHX1qf*vqYmG*639sm@X(t@KsrdxJjesML{qWCDV-vA-DLe&A9%}(J@J+*&Mp6NX{_1)-R&7hlVb7x9or_a^**ixkxQpUnU8!Wd968yN0`c6fFXp1jiUm^B|N_xlof27`lw#aacMqdY9T5U0>wRsoSfwLdH8@a{(@E*g#YavzAX|ZeUMG*iy<~67Sz`_bPnz~Wm2i1YSX7R$4k}IRH%SYI?FN~vPJ%zS;|F=&~3G}G%qe8NSe!^1hLvhjddTcDC;z=+OAd?k1e=EC{|c9Y`l9iE&TzFtlZ9)ZUi-~!W!WUo=7ug)r~I0hW|yS1_UuiM_Qz7r$+2LY6vmmr<Q5&cC9QC)c9z%{iT*s7J3`Q`r#hf6nrp`h#D|`Pf{$O!_y{De(7C^bWCZ)+QDmHMdJEkOOa~JwhqFsE=eVHP1`*sWEU*8KS=P7)~@cHLy-q6iR81g$9AL=dspoC3J)nvTv^6dakT$<7I2N5>xq2ht*Gw*O#D1M8)y3A7S)o%L~fjad4Ck)inwI{npwOW!)mJqu^BA!0U?Tznqd{QL1f?f@&g~MT@{d9N@oL~n9>nP=8#^#knWobt#hQK0Co-W%3ThLfu+u<mP-Ax6p)THqpXmZJ4QyI(1Ww{OTvN3n~nl5ZZmJ@UiGT6A5xgIv-aU*Nn20IbtR;1#d)h(Eq)lo0X(6CTIxdnJtx}1%+l~aXu~M#oEDB@1OVAb+HKYSH8^^}^uqN88Kj;*;@}n9W`}d40l>~i4H^0Z)vYVyciIZkFf1#`-nXdTauy56K6^k`AYb3w3bxJl<8@i`%+O;NS8RDalc?mnw=V*lKT*M?ru)GZuANA2@#4n=56|0|eUC~{xa#d;0Nv>ZV0GL6W;-uCvyn-k(y{g9LizQ8P!}|+_Z3wonbmP6Ho(}R`b)WEkR~Ez>2ve`<?K5`bDC)(){EH-`Pc2J(Ns~3e1}Zr-71Ru^gc;DWVOUDfHSa0JHRxF@V1LMpGb|{ubRmT1dq2kP>DRVW+^dMO8fA)(>(S~_t4rxwZLd^l>Nbwca5Q8*AG2`fi)4ebyasMB)uT+@*N000c??wMqPKRP+6~vFRBm*;cSqNon|MW2)q92m^@RzO;VZ3x?=lhh)f@#gczJ(K^QuJH)jG<f<vStN6=Y%)s@gmj0zg0jo0TkWv3+if0P|7ET)|TK&ifcDHxHvL!UX5E`&C}uP6**>o~|P@GZ}Y-|S1`+bw&*reh^aGQ+u<amTuu3O0X7l%B378gd_zo6NSKta`#nPJsI08X87BjJFB_Mmi4{AEqT6FhEi?-Z<XhBbju$mo7e*o`W^NSf5@EFdQ)Vy1T{ftuk83?NQpgWluy;4LcjlYa};u1tILJsB+Smc#52`f49};KR}eWMRy`QWvxtEuB@MIJs1T4R~#?<vP4Q!MbMw}-alazATo<1?1+L4_E=AT9_x3+RQ4rSmOe3x`xU!0VCbb_d~S%Id(!rNg-`BQ?M9=2LU&)c4b}iGsDwF<RVr`Vr1Ou1zoa(R2?sD>gpbDQ6=_YZkS}%3Gf@yL0Egt-qOP{556kzm41ktC1F@U%yHU<$Scd6dTxC)xgY(6?dAc?n79Gg~^TUl#Vmx1<^y@4@N1THiK`2=!g>U0ppMH6p&6i9*PzK8ACx=pv1yVkF2U*4}<vysDxq{XCrd4ERDF|V!wSSVcMLIx(NO^Ha3g3DVWsQvy=qPX64&U)as5_?5A#&_6T3?z&<a;uQ6+|U++F=0z3x7!+&Dv|ZW=mx`F)wKsvK&OOR@)i9TM;3s(`18ViU$KXJbU@Rk7XYFdARQsJ=&MW6)TNF<yfGr2Vq0G7bK!7F=Zdcy}ne4Eu)Qr3U#L4y)F>ZQS06kTjQfWUvNt?hx!wib8i!F`<DG7q$zsy6Jz$)f)ej^#Cav)>4sI((T$U{0Dlk7=U&wO##Jc8J`K7I23lU`2(Z#miI@6HB`j~%wwkB0@*OEss`zha*iea)=09!p>-N=e?y@AMMVv_~NmaLM0mx6BD`2I(0v~WPDj2I|S_bim!a`VA0|Td2fkOtllPXKBy8EjwPYywRL`xQ`LWD5k-SLaSe(^*$q^s`O+~4HTGA_e0abELS#?@DS27@2f87)*HwoYs(4`LQOEz?wQP)`c$*(&@E!&yk;BOZ|R=4!{W>NV`j{;&~QrY4%ISwnCq5GcZ$FP=AUPU(XijTo4p@XvNQ$f~+lfVS9HY#Mv4e>0g=>=rIe;fYW{z1>F0Z$><QN^QT5|L$c8g0yPhBOWC-MAV8J^=CGfAWW$kuBv@V*9R=F`|f<ef@>Hi=nH5*K_O2ysDBfH5?B-ZVGAM@S4e>iU{*nkTr#M4%LXUyXyQge$>EkDSflJffgohE+lRmt`+VwSmjOeu-7Qf9Y*n;tU$LPViR8{6QoOLS%yU8Qu=GQ>J~_%a_CB;T6T`?%wEF!SqwxF!s&240#sEFOjW|OEw7H#%vd~@}0ehD>z#xX})uvw>!$%nICx5DMy%n@f|GQTATv3hlm3zMe!5)10!hKb_fHM<YyobAu10}@dUJtD*S?Ob6el^&IP~E<v1)s;w8VJ3v7`|_ENVxE^=irxK*O?FLHE~8D?tt(l1H)~CZKwe?VjYc{-^1rRKIda8j;rmMb<p-Gn?L`B_gvwW8#qqoMZEyM*4c!jm+Z^cfbs`b&{?c%61nt*D^#y#RT8upZY-`IcW}JTZJAhx*U@2NHmV3(r-y4AcohJ=8<R+D+p%+1;*D+Ekrq)$JV$(LwEm<W97=P;tVUoYODuA#hXER1JE%CRy;{!Q(_#?3h0)U~auK!^c?{t4DQCTF1cPk^4|v#W6&Y%Wk~?kJc(dljHhD;csn)>aULxf^){8b{8voA1H0S)@H~1}?`x=nqVz1pkjF=8rPI*C{lHz9qv;UfStoWP76-g8q$1I*u9)AQSk;^8QZb_S&JWj&FMcnE-4eADr3ZHWI!B$J)kzKQ^9GVhK*$C=0^gZFR&)Ij#gxM%Uqy-C#hBiMf(gHyUJzTI7#e>TGE{p!nagD1W;U00G&va9^#+XfLbdch3#FIISrYbk_Dpt4Zt?N*;)Mtbk@n@=aj+@PtqVPX2d;7<>v04SG(laTCsvQacz6EX7m5-w({E0?q2}f((Ug-Gwn$GWmTZHEz3G84pED1<~5BX;5mTvaJO86mD%z}FZhNrfD>&Ssy;GFPkqP>>mq~g0zMvkX-mz-nO@s0tF!^)Fl*j075g#)^_u)SI}?o*lpor{xsk(od>pCx`GV9vl>cN3jgy`!&fTQ)a^P~sy5jX4bKTs{%TZH*%=VIZBulUJAPIJH@{39(s8SPFc6*d776C9Ak+*mPpzhogOMC{ZK_)tP(VR4VU>0r1$z{gHj2*d$H_EyQz%2}~rtFA%ahB1mSCdC`FEl;ZJDEvJ?&BduFiI6*j$Tz}4g!mK#8-jJ+dSrKE#=8?HfTI67lPdlix6?iy!HD7UGn)1ceJp7Eh4)I=Y^bIL<$t0$;rikG|&xT!UUPHH%(M>@rTXVq;bA|Q%7zXxZldGScL6qUB%Sfl;nW3-M4x)Lm-Lt35=l#8=svHGcU!&cZ=w`X1R9oxX;InAeLGI*88p&Etk_rQ)H~}2|k!b&tO4e-SY2fyTWj_{h^S_dCh}W`Y<56t8saTs%`1GiY*ZHK2yqkfX*PftwdQ3BgwOo^TA3(enXW8gK5wzwUa=`%1Le=d$hY?}KxJ5elbHFZo2JP>e&N)x^I3MC+i3};I5Y<8FK3t+A;X>v#@;%T~mX~+S<#|Fu1X<}oECKnrVm#OQl|o4P$#`y5X#B44o`_`1iUnX<AFfq4_|>~7nzeoBLXX5_CB)v)|G@gCHrO7^c3w-m@*UZlHXNT#lY~KcHNO4p37LYQvQciq2jqSd_&=D5|FtN$%9z}vC}j@!$&dQcqHW(v6+wlXsni#2kt-9}`~5#6!sUo1oagk1E(&x4r2Jb&EY0U%Y53CZ<}QhedeZWsP7(PqLxPl&99F8Ik?Z4juw%m|)R2HK_5SF)X6#ORi~WbU;Vn|{2&W1m`}U9EY#%(Q_#KWX!sWj2bN&5jxfglI|Cf*`hc%o7&WON8DI%`SCOT=JaO|Ym9H));1WBuzXOW(hzF6y2`sDWYagMP%lML!3tWRRn^_w0p6mJ<HxJa4}KY%|#_IeQ9^ADjeGvpEH3?=8$oT3h+u_9M{z+S0Xwt?(kONoi)O94Mb-u@kSB4aikBd}5^PIAAlu$I`TJD)dvFfYJMk7zGL_um!(JAe&F;F8u^0T564^v0k=dn|Z9%hqk^z?<!iFU}0Ag1Gn~6Zevp1BO7kA}*)j>!)PFd^t)R;2L8pyduZZ;^HYS6tR=IpyxyMUEb0{H|!QdZkze$Cg4O@&JnLvMV;#v>qH|@lzhKW6R}+`+gLg9H&rft<N+*jZ_;n-E}XGt3@*&>Y1V5domGo>X=)G(%wMqB_R@%97q0iJ%px_wll*N=24Y7{0cPn$MEk92vP-l<nJi1!JDqhTu{e=PViE~vy#uN2nAo}||LxVIWT~L*0r5hq+^phg=La$9$~r4-bWiRKH?qO<kr^#Y8H9};P&i;3aoRqi`a8}qzCh8<;%u5u>p!z+)HdE~ToSMfc%an$h_MOdO4b@1<5m@(66VclPoRTe-b5w>QX-ZT;UskkHzo-sVTLlBlh7%EcqxIM(Iw)yv{>r^-o0tuw_i%!)m`OHPYs?3AG+3qrW~uIM6v2JE-!@w$q|R1wjh`e3$q??;~R%^Y|Hc4ceDceUJ6=N&>qT>t@y)<G4QEyrdt)!GFkG!Bx=3Kp$fYPM(wJ)lUi*3@kP~6^WYt>$_w72qmnhSC^`CaRc^$!In5Z1L6qYvnm|X&(8wT7r@id%2&_+_V0Wgssunjp1=nBKJ_T-!Mjm!%O^IwC)*gZd{b^LA1Z431elPFE4nVJKAHVQnCG|M^7&MPfjXVkiSQ*~h{OEZr9~jwwK|JndwZvytyPwo*Tw{igeS2Vd*S<b3`AGw}M5O6)Oy~3&Z1jknGboX~v<{Nr_p$7JQ&aguoeC>?zZ)CI2Em<T*FidYABsJW!Hh%i<@xP4!UAYWc{FZZ`j3m%9{YWp3`(P3>!JolZdrm_=L12yBxv<ShB=y`^exsU>PF}Mif<JUpy2!+-(f>c0n2{Bz*IH8a>Ku~v<9@E^sJn7F#T(hyyUc87pp*$+cZ#{q*7k|`+53pU2!^Tld3mWkYD9Wq=Ih*RLNBF_s)UFLFfL_OS1<D>H;3VnquwetsLhflHdq?4gd>*1q9Yip)HKmoI>EEb)v({nd{($k>u<<#Fd%bOWj;sT|ei|N;;_eofxP9d(j)yIGd5SXwNMGdppgQ)<Ai8=t>inRwnW8kRgJ(kt7R!B3anO=aqXwlEEyc28BKZ%+*ZenIGodd-U4=RzOal!`8Ln2SX~jk6z~QSr}h5+(eV~UQfJsy#6-nRendCwWE4kc|@RS-vAp4B4h(OUwdx<#fqP9N-p1kq~N_!(Vp;*>Jcff#@ktorY6kYIQO{tlr1_$LEk-z_Xyx@;=)+Jx5o@=gm+qfj~-arx3XPSutrhP_j))|rd@By6}C#V9Dq{zlJCx>*`w%ai$`iJE%KR-qKJ`)<%6l=Q%)dqvQ#C)u-u`|H7!oF^)2hT26I9F(c&+Vo>a5{I5OoPyIc!fivAUlmz5f^duSHN&hzKqo|Xj3kslugQ_$;OMEjd_Y4O7TN`Khtoe0zA^fm0bS#^2>hT=03O@-gSpkWyPmO)+^y*xl?F_I~AP9KnbOB1`$pjW-Kw%SXiz1dH<Y(+O8)x47Itfu%5>ofl4$)94kUO-MWbZe~6s7<~hx@(|eG{4Dm;<l>#k#gJXD=`A*G;tzoh`L|r({^NUc{nHk(f7;Wbg+*kJ?8AWuvGZ1qpat@vD$gUrB8W8<R3(C6T{6P;r&cB&AhU(o5To_Qc$9K6c*~qlsFbCi`^GIBLWXrxb<hmcjKFX93=vMok+%Qbq4*3W&1ZAz9SgpmA&HI$@j`B@=*TvXOT~xXk}aM)jPt66X@QZU^F@%&Z{0%ur<~|FtcHLzv5xi#!dk$xo9cKacybyE6t8%;~{oD>g}}xlmI)9`EG#TWW^h@r{Yp&;@SWp6NPAhf4`fy?v@{d&dbav`*;2nr3qzdX(U97%?+OoGPO(gRBrkZkI(WW*z`P3_F=rSoR+$l@4f`xtco%^C2c1?ZtBGUp#5hM@5#~N5>!osd1yUZ?6m|&I_kXTk4=BB(`5A~U3O6iwkk@UsH3BJQ}nvt+xJ$lXdD%EInDAWLHO*s#G5)~TWOh#qzTeWFf|qr40>^t&u1nawFFx0$<Ym`>*+nCf{DU-KGJcrdEkg1>I2UJ`MSNu$2NUjwuUo%Yh|cKDY&JiY044?7lEa@Sp8*bTnP7Jo~?Q0wciSEcw7^{_2C;ItjztrZaFy=Aoq}58a!CgWMVP;A&5y%<pt(Y`n;8ML<nY?7~!2UPG+^vQ?vNSAL2APSE*T9%#0!gvoar3GJS^-ENW9Fob#H(_bHm8p|N_8+66NlHWKZzx2iv-v_h(--#HLCx1Nqdm9k$ktr4HR6LYvzXx!^MK7Y;zHd!X>hCd9gJ7v=QdCk_H4dtW!El$jO*WI-THz4OdZ=YY-n=Fq0d4dE>_o|x1{xnCH4BA31fg7$whE{`6ivWPL%oP+MbP6(cGy7q{V7{uPv4>;*xwFZ6|GjYl7Q9<YA@=6hzj(}ND>dFp=uTO{q`m^R;sS0RY@~1{glk!nl?)Q86vry!5{Gg;%$~|5r&Uy{E-A2^GxNs$@4kKF05A~I5NTazo5)3LYS=yy1%tuqhd9s^<>N{O%o;H|vnUYl91=tLv>)r*>c0OS4CN&eaotZ9=K1LoxQ;>hB3=WNaU%Hku&_<uu_A7iqXFU{2I9j<lylhiInFiOG<4V<r_gL6-1f=zE1Jv#hd!h9`{-k&e8=ntLb|d*EDuUHQuhmBb-Jk}qT`9oCKWgHH<BkDxG_6W=;$b%e!?mjP`96Ug2c<s0~#0*=izy9Bp@BKCp6v_N(E<J|B{1Zf_nF<K|}hu8icZbfilLeNxr)YSK;__oEm(AbCgEyj!*wP1xt&Em$s7QGU$A0*1c?10vh$4obFWwLFTm+#f48qUx0S<#v#993Wh}QEcm#>cbF{enc-RMxj^RZVT7eL)o$BhdU$*+daLP<DT8Km6j){Y>#9O$1Wq~R)=1`5!4}CT%*bsH&O)&?gG?2vybT<P_T!Ta+BZCZzE81900a4Xs#=HOP6Kyi9J@vU0!6ObB%pysPw4j%Y;cAvJ#r3Cs+URN`f$uQFFwYt#6OD{jC|W_{<L;{wRvR)u7@>d>vFsmeCtc0YLh*y2$EBbtCW3@okzcd(*)^wr58U}3(!CJ8MP~+%{x${E)H=FG#bJ^_1qfQk!2W`@%dVmcFWL{_pdSP51d5)YfNSDn-MZdJ5|8T_Px_VwCb5WYn_HZS29YS6`h-Tj`RbxO4oh3RKo=3R^`Mt=Fkf{NJYmevyAIP6ccL0QZXw`<s@#8OvxzvL|KbDt(HWh(fnrau{0iT``n(nR9wACit{=2dRKSHZ^+-kI@m9TIxi@muWV$(SP+U_tLxPXWlF^aklw{n_7EtemaY_WjI``l>KaYZNzkDuD86rkx4cBQ-wZowQ9Sy`fv!l-PBcFVpLlA%)h@UX6Fx}}9I%j9p=WU2rc4+qr(10J&Ua&L9fW2SfuAot-P95F4DW{h#b+tVh(DC^18ekS>b?0L*wI~tjpLgNZ9)ijF>G*#clL1z92@d{jLg`lSu;x6RJLc!<WH!p1rV(DdlbvjZ#$~@M&HYjP$k~WLO6L!+%ps9f<biZ28CiBy4xQm0t{dU`g8i26daIcI}^qJf<kA0{xW|gF@WeH$0UAuqA?qsSbCq!TTx-69=cUYbbL*rVN`wnF%KlBItOS#sn4@IrQ<NfD@LtFoU%9bzXGeTfPN+t6!uQld=AqNGEBtGgzl8jZEyo>%=>F)YAeK~>#Os)C~hsHtF!mzk5bwSp0{QJ2Fih{s%i?3SB1=b7RTG)&)h#@O*;Nu@NPrxK;aZR|9ObuZ8LuKC1vrF%8c-|Q66KPLCy?0RrIwu!aFI3aI*EHU%yF;jTG0E@0=LSBT?jqee0jIp^O^GT=jC_*CglUF79|#DH-ZxC2$&mhhq{DYplN%L+1V1yYQoiWdm&c((8kIfw=~+5yk+W`%lB=QrATnCzS|Hhoy@d8y&2dj<*hGg<9lbV{<ZjV|7WMWgs7s#6rf#*CHKRG;PJxw57G77B{e$DIAU?b;#OVlk5h1l90W!fCuwJ0bDa_=q;xFGSOis3a|)JDY-DNu;xzGZTvu`t_~GTEY{)nIAF+cc!mr-kK&LRg)-M1h)JIT7Q{r}rlqvi2`Dp6vUkk#VsJsMf&x4I^b;ehAnUlYO{v@oFXO)FYQM;*Q}<?1u>FzR-%eCD8Iy?=yr?eH7}GI3Z?*J8*1YHW$K&v6cJ3?FoA-ozw8|W$I@X5wn%#<-F9;`jWV%Bb1@Zg{Q;`TOX(gEjPTCRfmrPJQj0$=oOtKAGT&W2W*DN*JMZ`|HjfTtdVt_P#c&hsBN0@?~3sV)x_p_>vym;H-4_TannvXyhDh33ww<3d$Q7sBCXLlC@>?b{yD1Ze8;-Yu8uUlcpkuCSUaN}vdu(#41PL$C%r@BF2e+gT8D}N2NQX9P2cfe)m6VcQr$Iqr>eKj{tslJiMQy}3;$~L1Vuw$#s9B-Hb?JBFO!$vb~=@+vGJ7Rm7uLbi;k7c40zUE`u40s9QtXgW?ey5VXTr*nzB->ljn8mh7!Np@9XZ%STKuJZ0%>h^<PK~BlvNVZJs!|-;HTF_AFP7c-tX{MUnwK=w?DX_6fFy%?MJ%|?yFEe(wBZC9TNdI(R2Cx~Cg5J!SF!gm+Q|MgJrl)GYhP~`{ej9A&ob?&q<m56jd02f6B)$ehJpbJ)}-W6i3HX02=~XFO+V3TNv`OXx!_)DISBACWtMJh%b(yBXb(t5#F2(hRcb1vxz4qj>}czijYj&{@E-j|jBmq<eJtRMx?2#<!wy!Mrlk0ZVg1=;(iJX{-l)jUfLrETW}#b>u3BWlurW7RtKB9j)tOuqxfc6{uPSdNOctHKg*iKQG)ZRGa$;brRgOF#GE3#P+-%o5UPF>Fpg`7<@xQC-d#e~X;nEJuItp>DijS0~1{AkSZH(k-MgRA3{*IdcAn$nrjYRdq`R?vsBCNX<RiX2}RM{&sX|&0h2U=So@lWB8hSu*DUZnQhCCRxJj+X@s-G1BGg(j?I5E0ejDCoYBhQH3QM`e$!oqry|mcJgU8Hj{fREZT6L$CHeABIf~{?0J^$)<}D80BH5jBJ32HgY>MTTaRh^uje4+w!V-68~2((M(A|%B1%H6tK>~R~6#NH+~@VtxGU6*h4(emosfAv<D7~H369<3OEdw*!gD5fOc7{-p?oZw~lo$4+e(y*95#In^kZ;?HUTRyhE?=_54lw3ve+V^EgQ#7(Rgzv<AR|=YO|4=|_Yj0>Wq)KyJ*^NHZyQ*)bLT!&swOZZ&+BMr|-$Jh4jkl892THdv2vVd<oYftKUK;>I4hh}?wa&-r%(Fg_fe8tIXak*MOtaE`kT*$3z5+^#-_9gQi8y>ac=^mZYcm<<a=NIlcBKWn5pJd>N)1>nU(eM&C|E+-g(jxj@$s!QM(%O(;c7vr^bw?WIby_IMy?R$iFQxWAN>F5w}1P;1iC3?$Yo+J9oeBs=fPoracmjk_;l_<!$2<y#Pn|I-ju=RT>oOwf(0=O%%=?STknNx=T3=|`ket>3*#NwzJbzXEh-3+Q3pc%~3YOA^<%<1N8G2_$NM=Q9jK%dNv0#i-naXX`D${T@eqyMJWFn1OLUsx`{0LbcM=ED0Ns&0*)emuQy%1=Rv|26@!PzzrwumV(S;mX5-{1i}aeOE46K7X2%QNLU!&xRRV2s>)fgWBNmd<tKkxmCk>x&)H!d$`C^I%-*`M&q9$M0J_<gFyu1x844S1`+HT0Pa%JHwr_<P3S9M{1;R;R7_?zj?foDfGqr^8q9@Li!1r0PK=XdZ1`k=z253!VlSuu!`ebuB&{Imz{Sdu5_VuWpCJg91{h|4QPz1UG~Ez`CMWO_E5zFBQ4g@M4&A1dp~AvLGfoEh;l5XS7l{es-?L6v6HUH=WRqIF%3yTpirgd0*gV^=M~kAd9AY^$AxUnuAD4<qtEs&(cW&@LY7v|)5SOaUcfk6G&&vnzt<QbBj2Gw#u5+H2?rEC=C!182^Ly_uw%{1=L1dyQ%W(QQX*Nh&PX9u)@Ob<EYHOv+>m&a6H&d`}10766c#QUgf>pAmlLn+qer^soLnCLHGrwSS8tEpXE`xJH#{fYEF}G?&*j(*}{5~536Dt62QEXU>42XG2&G028UQ4YRwX;lQ_39%tazhHZagR~+vi7gl1fEc&wCn)-H$ALE&KG)o1{a3(xc@})C`NuNx{IOC8&p7C{1$iDnK(GpL6tssY15_oG4hLL5qCw(qPJgDjV3`$Z0UmMC;zyr15nbfXp>M{Q~ennPDkdjU812gV~UxEDO(h+k%Lxdz=nbCrOhIkYXFyeQc&bYO*TjjhE0uqVUI+5MU!vCL$>&xcahmb?en;P8;=H_`m616=qYu#XZD7?ty9ZZ1)tl_7zSLn7nsx;De+5vO2Cdlhi|2*9(x*JPji9G$T+-J(UMS)kMYosh?is1HsV4nZ6`_7<?T4dCKUiy1+=Twz&n&S`tduf@H5B6q!gk&JokD{w51MRNr#}7#AcKp5e3m@jLn6Hp(t4TV@~3v9%V*r4e*|S>KdKmsNOO*i+ZB;9L{WC?2pYpoaY2U<)dUpd|g@+i)Tq+GGJ}w&cW95+;79m@*w5}H}JyxU;?t0X{tsbqLEe*RRG27(waJ!2S2(>p@o+9^l)@ZLYb;w<W%pqn7k}xSm+J_&5@&T&sS$xs~m#Fnr*DA)qkv9Fg8)*p!gk%PN2eJ#kc}f#41_?o+*Mo>u+>jE7#kD{gk<Z+>+7g9eO!F_ZRn0-I~(kf$hX~)a?T@*c13;>%w3Wt3!!#xwdc7o{9qF(9ox~*BfIb#5+T!scbveoq-Lh1YO|+4yUcjflrWMI0m;w@4RN(x~~Y4C^8{$SX>*ZTo-wBBVjasK7!5hW+)OgG#r+D3RT4b=KRUUuhUV{LvC3~aG6Q!{KcP{yj!>VDAuCKo!(@H?j^I+9$5Al(gtE1Ls}nJgaB{eJrN3&3h6Ph-lVLgWuu(P92g8Sk2Upjtg@Hlbgbe;dB9;Fy3Y`E!RB!%E9PW7&my~XL(9gp4ZcTYhXo+()J4oE8VkAv*Vz16HIG=EI>S)tkz^#R?<&suxnUwdKd^&==21N-XR5r7t#bXTLEP)+xt^9z{U|sEu3rS@o2tLDxx7|h(fRHs;@+?lxI5q0bEfBQhV6L%kUj^&0d*8#pT}IX>&K0HAZTPR6h&4jJg}aCR=R~GjBnKLYHsjvWCWxzvAo<H)#iycjlA%yF)1OJ3V1BXdCc0<tHPzj9fDvTD@p|O(>UP4^+*2%d?<5(A=Ttl6@5l9DB?OG(5tX`lafl%?%LDL!8}YOD5!V|K!CeJu#Obnszmm~i|~IjpY6y?ZJ+Trd2oNDooWNaGY)Xjtf%x9Ya>=7L|W#;cQ8@Cac%6R|B*@0f;O|04`f`4#Qcm$-|-@!GAf{p86Yb7x<Y<Y`&=<ZWzNC)Vg~<$g0;n!Ui`<~;C_8>WR1e=BC6wRjE5lL6pXYdZC-dQ61%GHw)A@HN1*j@7Rysma(CGdKbQ#{Yu+5k2w+=$>#z&)aC{k-BhPMDaqS=`I6ZuHpuF}LjBqkdRC)koqk{|iH#3aD;(N=J><wVBW-?7%j)fRc6QjrviXlB8ZG>pwC8MEAQbpWY<dXUrZ5&aI?bdyTq5Y^5iQTC((Mduj!NYV7Es8^z!FPTl9sZzh&=a2|2NE9=$QFh2f>DMU=C>@c8x3zKDW{LAD_g&Vj18k5b3nl7Yq1M~kA>_w<zcOz&6$`232J{{Hm%ebiak1;X8D+?&Zw_P@YARN^!P(&0+LFH1=ldMbw0>Lr7DGa36VCOZYRro{_z?Vt+UrPPRf2Nm1BKgkw|-Y1<t4?lstgjZlzO0v%#qt^xT~HAnq?;Q>-D#>BD)V)VD5^hEldagc`6`%TIIsJm)uqc7O;1$8013H}$9a=9J@&y{jO5ih7|4a6C5uL635G<+`*kcOcoBW*$^Nd3#uqDQiNnrMl<~&JL4>kNjzWYFox1E6^M3)c|(-U*(I!DGM@UbJYKZ_^X=pdyF+)<tyGFre*!HJtsfgW9#&OhOP>k@B`uKTfq?>w&K5qcG(CY4c5c7x<@s)LORCv;zaJ}$zt8#u+xIg@Cv-I;X+?$X*@}JJ&(=N%@O=7p^A`Z4wX3!9hEpW?#oG^BTs*0!{XLeM}-Yf4O_VD9*Gxjq5NfJz2VQa!mWoX&HQf#AI)TfQQ+wxoTWSfto3CnEDI}4hr4`|)^0cPi+1f=>m!KjH>!4L!jP=7c{t2s761(|R3!0i!aIgS=>H)ntwwi+OUo<Hxhir%ZI6Dx04sN?1g0Cm!Ht8n!8IbmcYJ%pm+RPL4nve5>^d;cC~4W{DX3agRYF8}51z5?{z9pygRyJrhYH<BF!8m?3kuLT&BF@uSw}|6r~qHG1ea|2tEm^%aXcD_)ak)juh0$`IH)RCajxPMjK-BHKA})+N`&NIDoSv(;rJBTZ8BKuW04@Jn3YZejcAG<x~7s54qDroV00JXj!f+Hq!QZd!Zv^wCN&@Pu4Xyanok0b_uzcwDJ!npuD5I@2*RYH(eE#XjhUsuk5Qk()vU_oy!i~GJb{us<|a~q*kKs5gE=Nesyob6BJ9oU1TedF4WY5rdDaQ#>(TSJIj(%(T^jh2y@Lt^w`oye?_s^%fEZ4lQPeHysEdCESHsgtHQ_gom}Iz?Z`)WAg?*XePm(XC2s|wuHUnPfLhQmsOD=|UFayjl_XRs9GsVX+{eGjc6vWNH?e}Ob|2Jk}c9G;mS81U9FtU)Np!SGt6nKBl*6wW)nGsj`(RNjIm~^vDyM1aYY$wVG8KpY^c6?-5qah`Pu7OMpg;`>9wT}!k^s<s@sM>U}3wEWUTda*DIPEk_xy8aKm?4O;@Suk15e0bx?M#8cdg0l#{d9hJ=EjXsiS!W^3WJNSF>okzyS>TjT9dcE;fDe*hmFskkT_y3k`e603giXNQ&`lQS8u}5`U=pIyK=kF7Fk*~V`S-vZyU2E%UludSSNF~oDgGwV}dpThhyj-Nx=p=sQN&mV=fJ8Pe{ZxM<Qteb-?RaygX_l5frb7;p-uFGV2Cz227fC)B9)zW8PRAfiORsK)cKsQ*p41Z$i3Lq=6N+Ec;Cr*{s=(V3YlnSTeZh78=K=Tb3?CCgif7EH;HqL9%sj=akJ~&x}Wpd;-@SDBZ{C1sIU+6>?=@J-p$rJ6Yecc~mnvNZOClFXs)Z&H@?`qUAAT7n^FV{I+R*PIdJDl2=R<sU{dh)$(o3;OAu^lh(88C?wJW$;58#&=v-BM}5h(P~a1QQ8EGHx5_yRF$i|YyD8Bq_yFkqvoC@Y3+qKDdj9tvaK%yqjR*|nz7~X-1|q3hBkOmyz^m1xSsfm*-aqy=8?&l92h38E0D#JiIFs<Gd|U+d2H6u?pK#VVB=4DHV$5a2N#b>|>LrlD6+gx+rghAwDEOpRP&fD?yxv01n_*klij;QY=Xh(>d4<B<Wfeu6c=TBsbr>vT=dntZZBvVzf!Z}mQa{Yy+PcVV!)hhHB_9^`Ic!YQA7<f4>r=P`dhC->)<v<L1Aj0q{Ysd&vU#Mj(z_R)MI-h0GEP1j>p;VQP2k<-&|oDKv!$p54^HMfS0`1g=_>UGsJhl9aDsXfft{IHe)XBF&a-m8cr6Db@U7-L>>^(TuZb~Euma|1Rz5p$r+~eXx79SMUE-tjWmz?O{2)7WmLQo+gasFdFX72p8mjZU;i}1Cu3f$KasHG*7CKn`=5Fc56l3K?1k2G<9ey4B6I$@p%m6&J%aSmdr<_ngoHou5x48I<JZbo9U1utK=r4I6rLOumDcHkVS#!)~d$R<MIBVe`Kj=v9^IQ^7aCBSx?7s>I8__YAse?s8q*0vRBQY8;rW13L#*O%oq*MWRSKg_c@B~`faJ_A`sYLML9o3Ot?L(eK40Eb`J1mp4oy-gB8B=FRBQ?ovD6B|_Ne5+~*ut`tS@n;EhAsr&bR&A96fMz(9&yrLwuOG5=HtDqGoHpt<+-b^CBb_TkA+FSX)0{m^9-Kl017JM>w6Jrz)|i3j*acYhhD%L=5mX}B2EGWK%-`cjv3)w9)2J=Q%AlLH}eRKgLHn$5tZ*s{9w|8wV_NM!A|7Nj(=m5Tip2+CamGZ`K>2_ZkizrlnPsZlRU`lNp|Yrr#12xR^YddMu(E=D{_+ERL=_o5Nvk;0tlq{Zko3jilf0BU8f|L=YaOdQ~Ri!kClG%eS8axf)^0?xElGW-MQ6fRm@zMyD!m4wLlR!iW-|ozg1*EwHB@oTsd`tk^|<!m@(iY=Fh)RgYr?qLCRGd(Z5!ER&RW5NK3sqY%*${c0y6zWE4kygq6zEso_i`{Q$6!*-Pl1j4uw$y9ZV_fMR9xGS%xf>3AJ$wC##s@H0GIW<>;Y*~N;9Txb&D3{@W6E_{aY)Pf-?ZTF)>u3_X=V{3)?de6xzrO;;0NBxC~*$ZX4PMi2&6*CvI5vA3OTRePmS%>;Yn^1r{dbusO{ij2ASqp#-Rtcl3O0Jn&qsum{pFti}U!Gm2ZP*D3YB!Zwj;bZ~_&}B%8o(mdaCu~}3)roK`KLlesFQjWn5tO{i#TQ0xez#@%m#qJ&~jVj2c9GrCsh;=jY`GYEU+trhPtkOdjZ1xmWkg)%Vmr`*xM6a8q0}73pL|l+BS7S&^{_Vm+>l-a%9g)F>a^`U%xpEFfDAE+5(lbeS~^#LRpA3{+hF;iqQY$w<FsC@yQ=h$J;lwa{paO@%+Z+<B&3t;d{)gYGxG^<no{Wgg7JVi)nK*ZMLdIHL`rjNDsLrz!{HZn+W>4dq2Nq11q;oE_gnpL}p@9|As7Xy@wlc3(YPY%QQ{AV$<igD~{IQQ%|?Z5=Azo5jJJsWV^|arj#Prexm@x4kaPZ9ah0K55lADiV28B3>8@*v^1@ajhafrDCFA}WC8>KJhTuP@_799byc%?#C3jN?qJ`e-pp~bhl?yPM#@my=#=>lo{|-HpPF?|%RZ8ucXlp;th8CVg9@_KFtJYUinuDpmZy)|p;l<)>*C&Qi*U=@KwdT_66LrwSU>fUr<57J8jgeFIge9d=oXs{$37U{`f1lFjmR7YtsH8PA}v_{xwg98mvJebmqG_beCHbblRxkh^Skyl48G^bNZnm4<CSZ5l|jG1CwBUx^aGzlkN)SXResG!Yz~h%w{E@F=$>@x6}4wp(i}CRg1?RQc!G219c+iVg&}(AwmB~1q1J4lVq5hEXB!v<<dgqpWcu{v%_eR8Jg^mzW@?hYL8>Dc(~(qlAc+>kr$SfPL;>-zJE?y6nG3Opwwl?98l-Ykg129Dp{7(+0w*Gw@PQ}8!|9{2UMa|w4|n&eKtpD`7=*n$8ma$TT@H5y4x7Wm-$qRp*6vMe`_v%<mrieJX_w>;MH+H%9w<765mijO5o!8k%(X+7QF96Q_4(%S6(VTqB{u{W+aZd!Y|@<}@(2l^8O3w?xfD@L_Ic+_J9*)mgV9Oe(m1kX#SqG$Z~1YNH225Hc)CKmtEfH1kV$LxPXzpywhLc;z(tSu@Wvc*&bF3!G22&&f6hhs;?s7Ps(un7!aZ?nV{I8H=7?0VbDz2B&8s`6pSFnE27rs-?RDV`6=D9MOlNp=k8j;nIC|%W7l(xaXo1X^eLg5#8!zA*v}M54p^UpT#j${^#&q3BHH96{Dgp`c`X`x`^+5a`DG{#m?$2z8?8l<`E75EOI+>*jd+v<)AXb;)7R**m6wVv!`Qs)Xt?~wSM*!q1>`0VkaQ+eyX2h8MK5Uv!d@<xz#Jv;nyj;(|Y~dDWtY+{SIN2PR7+#cJj?hyrnS{Tkh~_?(JIps6#zd6oB!XgLNpbzI0|r?-S(=KS4`99j=)h1Fpv7{VE~lm>Mx^{fuNAuFFrp}~8nlEEzq9&`DpttEO3>8O0(rYboM||)u`m08rNs_1PHyatn%|70h(%Y24tsJN;|IFn-q?xtOfo>YDTm209$BeJroPz_fTy$(P^VL>2W7|U!@vid9z1E$PEj(eHcT;v-ZT(P1s%~%gHH^6P#uax0>i!1-Vfi-IcFK4BUPCSxW&M<kIb2tO?)5_+kleLvO6@zE2o(aR8nOAMnG7sn#C8ADgkRMOuT8*Ke|@wCdW&)KyKz$^aYbNSn9_+>2L9c8D8V^(!xu+-*E@EvJ+BfD)6)_o|JtqEmM<Fu>hfRs+5n<b<%Dt9E{bQ^|>X8nDY)IgA8Wlk7)Lo9$3XHxxrlVejGrtOeW9;XkITzs9Vrny!%)oadkeq&;w=zNqk0}A-os)mjmp90QlWSr@nB)d^-TLmLR-+ZcS}s&|OPt+Yw>xn=A7d$C22L6T)u^CS7~dFo*i(Of=r0y%J4okf6Jqbi)0mlPgWoE)u)d{y^8FvKt8Jb?%~wD&K-6rsJm1hBfJ0>;MV(w+@s=k>Nr^9)8v^t7(wzxzd^bPE+sU?GJmfqsxD(3AKFSnr7`yGg2-Z3}M$koY0(P6CAwZZ#?v_K5SY0{;v9@O(wQ-HVBqRWm@`g(JAodcAfaHx=<R|BV*Y=9g$a~KN+rgGUI2xR1?Bi=H_TBMAOE#9uH)IQe1>>XTBh!Kfm~8%@xzcYD@2mge!u&Zf@zO4AG{nBp~ZhgF;mB4mFo2>}Pe=+l5$dnG=fs?M!3q1axAIvZUnv^1&=1tAj(Qqcv7%V|Kxg6DK}&O0A)hCl(lIUSYn1$;U;rHqB{pm868aysAzYt3KKX_Ut&H?n?|Joq>+Nz2$4q-{GWyO!^on!-pk`O8NcbYJP_Nti}rWJd9x-3X4moJrazRJT@P9OTd2*dDmn9Rc$bVXEmlAd<`2pDPOwq55>Dk(Rg&yMx&vENa%n7P%-u!Dmjl|Ck)Gp7kyWp&Jbe?zsl0?1s33qQ5i`?b1C=~`Ysw&=_VB}h1jbZKwpW>$`{s{!N<tdu87wVTBX}D&3zS<$jJ=aY0isbw_MF6rDE6haB$FWTe6#Tak-6R#X-G5t6!n!_r(x#%=PAI`bwQ2-7%tk)!FS1Jzm0u3a-2$zm{1>W`?2WMv%WER3u|zEDBQ+k)wsEqt7$fJK-(9I`jpDGG<#{fACT~izeS^hs#hIXOYE4VGwNS6+#4+yBCPsP|@2p7q<%pO`7UXM8a~erVsg$*~B1gUy(BruTR#9-BlW?&{<md3K&bBVR4~TsS?J(I%V^s061%6(L9PCV#!#!q4|A+evFr^skG+wE1mW_bm?A)*7QzadQ2?pY#?x4WB$xk$-T@8ibm3X7Uvv>Cp);(w!betEC?AuCH1^1s|S{RNakt}-qB>~ntAA#4BE^8-x_y#f|VKN50OM(z71IU_82DVGf8_UXj-eyj0@Tgo>%6EbHBPge_#Lm&|#EjFKYHX**!yMYiiXaJ-Yhu;`v%SOfub?#`%l%%>$TMmc>6H>c$2oV@DLYOWaix<AaPH7Rxjv77!J;(7x|h07HPnK?tU#iD<|hC^bYwcFtrXSHoLX_s3O1^i~6^{jf6eS$fgK*i=?@4y+kR5=N3Ob`p{S@$RA+FoKhFTO<LBcCTBSmhL-8Eps)azNimbb?w&oyVdsB6<pe;?<v}6IeM%kSQR4D)WNqlivnEmZ;{#tSfXoCA%sM1(0vYLD)*K-YP@V(Qm;h)9hassSz8m*I6c0}XATPTNCIqH<6PYar$|r?W4JD)x@SzOn<Y$H*{S}lVwqlB_linH6BrMvppV7d@>n#mvHQSByNM&HYkWq)u(<cKw>D8CYeP)(iX34eN0<Ee8;_q<T7=za(~+8_Tq_hON#mZP1RQsXB=O+c_KO4mvSRLe^od{DVkd%?!sqr<i5R9uBEbmmH%#SW*>mL)<TfH~1noBbLjC?evZzv&gGQ(s8LOMzvXHS`Xo)DhsDdSFtwNU*!+bqbS{fp4D78`Bqz2Ke%-(Keh3iwzz~VH-W}6;S(4lfvxThnf93#SpL6TObK<3}6m90C{5DS!;;oLI*GNgvKPp=f}nI+z8fCl=+v69;kzm!MxH#x2BBaO;Oxxx0WzcZ5aSAJa#WQ59Y8Vv@1L|ok!%r=CYv9)*pGw^?hu<%C-BLaTzThaNq;D~5%N^to)y!C~&EJX&T&J!-mo0A5e_{Q?TkK{R?6kZaP{<}DdCa*^V%0aY+=BPlKagCAA@!i8hHu1-5W=u8tDF4u~W&EwsO*D!XUT=rs?P4WwNc;MH@$|As{wXPAV9;||HLTE{G3U5BQk;~+<!btFP4npgfv?Lm_C48^^?Oxg#WKEVH4&2c2USxoL%RhVE^s16Gg>bWkW)ptybDW@*ML(=Tw#5#4r97Nf}9B{G=5{*>6}AQ11eV9N2D^Ks1P6+#}wDR1>eu&lh=;4Zw4bptf7$^sj!9E!M1+__*qzXlYQJlGEE{g07nuP!^pNJzByW!dOWb8p1Bp00f9P!dgb<d2tcznWPkyUGhchgQU-OQK~n?@{JuEdL4sYOTu?vy;C)UFs?XG+Ba=@Fomln<JG8+MnDy_MJ_$J%S~b?)yYZ)|RdF}$$1fsm-lJB^u-3&lCdmE<wrLU|(5Hy;DjL!qn)@1`P*2U}SB}QQAEm3gc_$a!yp@A0w6G_-lVR>Nr@pB9o>6)jm3RD7#TMH*6J1oABymY7piIW5lD?6LU+FBrO#E7C+FQ=1vWz9PjINLqKNN%iqoW_m6>@5ll|2-5VoT8Ibi<)`3@Zy>k`0O*OLmITHY%Hl%mydCUeGfP>|oe_wyarK>yM8%M-hw0X}1XHD1X*F#2~OQ&rL!I>`2&RQT<o^#o6Hr8@3os?T<Th-R#HYiaS6g%}@lo(lV*Jju9%WSCtw>bCqT*A9F#t(?@C}b1rw<d+9^xHpI{Kn60#5|Drz83^?ROJyd(<U6@Te+Wko+9&x|koLT-V6rBpyT9;_`UARx%Z~=lw>jDXNj*`bwvN;hFXOTIi#q^lsCKSh}LL&}S{<aF+%mW+<5;kvgxVQ`#VN0}1cdCLe5vrM}i}m6WbtBpf>_PYkEO(~s6;;djN+>R9AIP-ED=fcTaZUss|7pbAaS#JOg9zjhSu=9AI0A|dX`iL`a1Hn5i3(mBpsV&MN!=9iau=gyHV;EYyXiR$>VUMV$+=kE_KhyaR}5jm1gZQKl{=-gdDJgfKAPk|<Ls|O`MYG?lHv`fbfB)$m>G)b>_@Q$zJR*2%<Jxh`J-1O`Z33BiKay`t}Vx--u>nE@yLkAcZxEMs16LyPtwJnjhLVJ<8wzk>_(|DeSix0EpB&i6~hWK;6#$%RN&Gr(_8EyJm<u~yqf-FG@)qCVX^mOrBH)neCw(>C{LR(kjrsz`+mLwV+dt-bk`x24gH4x9$W8pK+nkmUA8BtC(EcuAgjxEy3K>X(v3W>UdjcmcQ_PahN>mfN3x8397P9wpmX`NQgo!ZuBBZg|HgQy(ddm41+|=YWd$z!lo6b~P86)e>KGl!a6i6APlk<@kpVPDkdT^UDn!`me5D`o;#x0j?K~Jx^Fz`zCMgyL;>n7vdL5gzny-V%*2&7wGJn=0n=0jfl^EUcHZtN!n<=b+-J618ykA&4J<PU_Mu<=9G~HGyCFA~MpZVoGENNgRHbO#GVA8Hu_+@DZ=MBthx!v}VTnteyU2e1avgFBsEQcuL&51KByI4b8)}zQ($wU!Y=xBem!i14$#ASg~At=wmF@F;Gji)$Ii|}7T#wYIE{Y-yps?+ffaOOAhAQ%zxX)+LZNiKy1JKCdy9N}_;iVwMipuF4n=}#hc!baC%Q)2yBnd~>N5C7mtHJ}andE{K@1Wm{ivFxbE;{aYejQTk#SKKT-Dy!3(zIJQ74AoelZvG#K^14G}hy^(B0Sf}=Pw?Me^mTedZ4L^F`|KyYa{-lc%4)hA1mDOTYh00suN>q=&XIop$)pXhl;kphRN6Gy=Lz@YS}s9(7MJQ0qr=4k$M<X1ZYAW4r}v!XJ8mVAC4=5Liu06eJSs2m`q^Q^mj73g4pDe%_C7V39fKr0$%UDkTYFkGAw$UstJyOBMbqU2hrReylH`Iz)?BgE{TgY({>hd)De)Iz0Q!VY|8;jg)K}4*#EJ0TMbnK$Q_@x7SbhZf6UvW29HWXyvPMq4XXQZIFOoX=0KH>^Fxx3$_u^+HQJrr--aMfOKY{R%#bkckd6Cp?ex~RezSH2A={?m+$G`%I(zs%Js(5WKsoGrN4NeX$!g5{V6{3ppFnds%^bN%5<ks`G79=ehkaZ~KW*v4FfS(pH^D25bcEW^QdipnZ<Vn3)n>GuOKZ3qZ2I_5%=Fxd+{mUT%KglH>?MX8c4e4KV#l>8p*1BV&=u}s*v$pjYp<eP;ev@oooS_%UVKQYGSs=7<GN5uv=ZH>UI{IXM(7n1nv6^Z~F!6k<cFwK31XzWVP|zj`#IslxCTUmsT|%Y17jkeo5%;xpn??$8I`j)Qd-^Et#T9Z>NwZrs=bGl3SsoVM?KcPj(mGU+Uy58inmt!ZBvWGt_f1=e>?taEC^r+UWI4r!<SLw({)N#p4~NT{5Nr?KQP6(PsHkX`(jLL1(+gvVAI!A8E&l_8KhzTVZxhY=WGNEHw6~wRt~=lV9mt$giB+n-k@woXP2l<Vii;4>L6yeAzYK6L?~o(YJxPH}GFDgH3VVIcP5%#eFp8#h=9t=RlA0FEiv&dP$5%!m-S=@Jpe<8$X`$7O@xYb>O!qS;;`LW~cNtH*B|@?Vq5Ov|I=E`9wLV?rlqnjz_Wf6NqO2uq6gi>T(;WC-WBV>-pb)-@kF6-lTJNgWuI2wVq4TI4RVrevv;BIK$`JY{uSVR*K77-|ny+g0m3IPs=r-@zFt&B%pI?`4!z=|N(^z7XszTJ?u5jTxp8W~m_OU{wX?9k*x23CBYub%!^J{I3#V&O~Lzz&ouwY}*u<Edu^-u<1$Ti_BP}wA(%&8F-y$@Q&8*{RK#uv}aD4jAB{DcSfS$Ku0Mt*gj$_M%r4W&zk+C|j-NCg$O%*=1zrj{V5`8t_GEmSEIFXS}xD3VK&`lg<=qBAQ?s6tYAv6OB}oHnp2C}DCY0mAc7#en{L%{+C3*1G=iN>~@GYU`qAhfer6QA!Q!;cd=-VoFAu=vv0c4arAt-^JXZ9;g3~owN3}uJ7WZksq1Gc*DHwws3l;EO)Kg?pa7mKxi<BEY*Aqe!x)-g`L(z(8!j5i$=?`A-+wz%FSS~eK~Wff@RajM8#nAURM>(u&NOInU;ba-MbuhNwfFKy*DTgImZVB$<HnIa6K4-vNNs*+gW|6+^8Fy)|W;`vn77odB4$DpisJ*lR6fDPQTYI5MN5<>@6z4{hWV&%syJ|aKzT_U(Xf8E_7c6s?9dW)DTjXF5AON#WL}jE_j0Z`3=zc6_`!UozWC$n$0bdC9c2?#bH8@KL+KXbD^icDcFO4gX8Ac7?}n;fM=d_d+`t_G(Cf7=@kk4;wcr|W~}<+s&QJSZ^?cgen*x;e4DtxQlPKS44r@stC4j00~q7%I^&s`R|tb5!>F^{0`fT)v6J2s*YHrtV)d(RR8>Tzj}Dv|9YSHA`OwjrXCMB4R6TV?-go>4Zjm8nN^fVAP!b000qW|!TOvzzg3QshR=IUY01;gGG>t~ONk8}*k=+YPuDW{pfF_Btsbih8qt`eJsng$p?0PxsK3VCP5p`fP|LPxwdUQ)_qE$y19o%k5tM^y`Lt$K?VLM_)rz%l?Or4?8{NDgmDOZKg<~}E_z~(tRxACz-ZS5Ky^aZssDV>IvUcfI-2d(2$-lXrm>^NVeFD06`B4>d;8^A>~Rr#VvLty1d3i>8RSy5UAB+--DMZSfd+T$X4F)5nnaIUgR*Ccas@%sL6QtIbD+_6xt3fxJNdod%0@kaul(MG4I)V>3ykC~j0j{)h=1njqEPr_Ll)n|K6S1Uw@|H;%YPkrKNvP;FVP3Zd6k%KL7D6vto{UT#!cO}bz$#}Sr*ciAQ{ymW0p@hH=CE+giU>TEqH)^f!QfzpS-A22e${Bi8>7$~x-lGaIt;Vi@GA)J*y5Q?Mmaf-FuNZ{5spANA%2#;F@)@6YvcpI(hc!+kBP9fnYn0HGZu?3=(AKLR2AwXn=k(FekmG+xr#Fv6I?G?z4y}{(j;B(73WDHWqEbYU>dUu9PjPSGf;IIQTKpBs-6WvDJU@zmAnr1fsj6qa*9T)Dl57~H<DHR!_$k1Zn#s7^WMGyhA$!Cp6O*4*rsF>SIqulYCO{znCAmIJD?%YO4+^&AP&x+rAygea!6IXvk3So#hv|_cwV~xi<y^1MK?!jrVxxXPj^y56a|v}9YS24XR2j@@vHthp)HDVhzKZxd?w?AUUm9Afuy;NE;W9WvjFXg2-+}Mh>j{fyq<5Vyx$jV_T%x||-90+xu~q~h-c=M}%K%l(iFr4Zz|UYB`=u;fHtdwi%gK&?{Oiw48JU&eiZ}D~Az~%(ZTu7a`F7fL9j-IsAnEh2jydi75rc%5DIAXnV6tg_p;y2>OaV!S7)PR^E`X%bBm3BYrE<@f!5z6(tkq=VnZjx*nBM2X{j^c%{%&&R{a99U!E7@p+oIE}By`O%;Olx5e8Dr)6adMZNREG&{WH$ABw<jvo1|_7ty<W;m;{dz%?v<7dgrGJy{JagGq2CS)&NeE=6s1y)slke>pojd7Vvwy$QW{tLNbASVS)sJNXfamsS;nF{JapwK}3(f_6d-jqbaX-;uq(==0O2oZ=!23qLl`X4O_g!vf-F0oB!5Tp1)CmocknYU7uN|-$uEcnq&_Ne5F!z%78-NUFee~o(oqb@W}BdIJJz(%`Ys<0Vmq^^o-wy!TqiDg>NMAr@!birp9q*eM4a&AapJrS5wsD=R-BkDSnwdy_$}n>ZLptK&p5%B`>N~Q^u#+96k4i4U$KG;X8iARz-+>OtspL|NPJ@KMPf7yTBqYHz@{M0X(B88cb--<rP#qVU6Nnd?lG6)H+Jqcj>Q>75L3RRtKw>QLhbLG5W7op-}ldjh{-FyC^Y0o(fx<d#FX3l&6B9d8un<qR?WAQH5MD_9QvIK@{^k_*BeQ7O`W^Gcn3e55`vAy&29_>xIy^Tx9kHjIQ1&mYm6uu%3UIw1tn4u04l2VMpnuAviyM<G6x>apSI*;brSc>_9@#3tE*F5uzSp$vMx%!}M=Z?cAn2mL(TnL+!gBHFjD|K#HH(N-COlw_N_&(th8(VBURYQ~GBLBiE97$O(?;>!g<J7!xiS#}^}w#6(5r5(;6ER-;*@K3q(DoNfrJU8RNJ@sxn-iJAIYbhqk#ef3{)E1C+?=E@87|1)?3mo0fRAEB1^wIdiK{weM-6@F1HjkEqb%1tyI#FI{hnpDy$-uScEwo|anZg7a6wpP;KmKypSJ_bEy3xU(VN83F`KQg{<>2ElW>p+P^0+U=`-dpDDy=BVj1y=+<Y+w%DH%gs<+COfHWSyPKB<GW-?t#WJg~TtL*Rw_!F0|MQtWt@b^3pc{FN<h~O@fo|YB?Vt1GT2AC-kMqE`P6j11yLZi_wXNZRTl!11M_N8f79xJOQ(8-W(>(#8#yM`H=`65)`k=5fb9>jki|Zy;p@UjIX>yd4@1${9Ou~NPRn`AwYENGJ}y9cBu0PkU^&v=S@S;MF!(f3vG8@tIRjlf!wDU<scxdpj>InCtX{}ZGPSwpkkxhKRVBAAN+B%lKyZqtRhl4`LX67<j|*m7`r>WCHJ8q<(9&4s_)j6>Wz+$6SGixY^XCEG*(DiM=6In{Cs@`2KTpC<EC$34_AVvU)<J8E5N69OVYMn%`xy{xDy*Ubvxn*0ldc$lMLbIguuD2!p5)*nf~SjLM~fJ`5$-Wz5@VgD#%x}&dp=0ASU&->2dbt&RT|)VP2VR+Sx6c<y$NGJEL!UD?m&=2^!S3rI^0cP)s1!AGbZ__C2YNAf^$@c-0P!nV9U4X?4o(p))6DQwc*S;6fbumWX}<Mmmeh^{UUckJ>XPPwl=`^}4)NVmy-kL0XB@UOPObl`bIa0x4dsv!;YlJd2`9%Xzl`sDq|-B=?r4b!VP2EPq^5+UZ(a(!BtQcZ`y>#<yp=8&_|Bz)cUGbHNPWN<E+0{2yi>-Mi9tZpWK$pS+$`uNb)05DB^0R!uW4p~As~@tykA_e_YMm;l67UxbNnY^_^5)&jL`hnm-f-Q^E+$eQ()rm~iekGplX_pl?u!a{aOyXb-jIx<CTDLPQgIo3af@FEg6pJ`%o-9baws3QnF?DB9q5n3p#@3&{>t}1@A*EP(?Id-m8pND9M#|W}hDw<IO4YK@k+k6ZrYrNo<Vc8EiR{i^f{->-QviI9M#xVsNT#Cbhe!+sm)(Qo443I4YYuMH%7lrInvg)4}6OEpK+SX}}k>7SY<DK*bA^`Ir)SorRBfzUL9N;5xW$b{}?J5i?dpXLn?u)=T>7<tR!wq*A(f>(I-q5u&^7_o7#A`GCSPe>o{7U)s>e8Ny$V~Go`Q5NvkKr%J^2bWru1jV(NY#-`t~mCq>xp~Yr}}tiJ~rR!wrSZ%<g22E-XSj1mHmgFUPEMBM2qiyPqa>M9oH4&sr#{|&*!FJ0o*_nl&6;QL9u($w2nn<P2{AaOs;2%{}-dz(<1sRh^x0~zHoc*b5I4mCjD8DAb&W{Z~n+U;oLo51!&*S1}C%+!z$l5!3FH;V@M1i&-Pp8KG{L+W4(gzW^H23zpoaACT;EMZ1;{fZh7ajj7`fdAk2OI4>-@)jzsEs;Z>s7L_40}f=dFh7})*Di;es;4aSTmT25xREu}mb=1@-2Zy6H58&;6SXF{?hokJ4l06_R6=g$}2$pI}Gr6Cq}wsEN^Qp&sngfac5M`C~~D5M;=w0%jwBM#rGEC<p^o7oaps|eG{9}iZLvJ>LPEUazbuAlX}@6`#&3~_jn0#c+7H4>YYx%f&XL=nh&>S>nP1K~eh5_L*o&r`Lqx5**b5_!Xe>CqJR^^MwcC*8i|?Q3bLqXn-M7i3Q%8$^kIq~PxrGs}fHq9iXC=({a$b@&U>5;?z^vVAhV$MCPkW(SNSp=DZ7tF!=UmYAf=XAFr}ax*E&{FDZ;R8irl&wE-$LQm7}^e~Ov5>mHm)jz!vMv)(}5kvVVG|GU9gJbmq0roMP`5e|*j<2r(=^Lq<N;p1UqoSU(Byet8H_Q+0tyXOkh->fAQ%fY0rfk<bB>^1iIFWNL-H9944;pxVTuuHue#ogbrN2w}I(@Ho4lmLRY3sxRIKPEt$SrKvrSri+<tYWT42tdUBhdpj%7JTP76Wo!uQsr(1OGQ-KM3sa(x|ggHfX8#l$EoeTc|DgljzKB-7xgc?Oue+_8x5Gt@5>1)o!%bIZ>;4_hV27WiRdop90vT`Ab1sDll)qj{Rbt?wlSuUgn8bT{0KV*5z&_tluXki-0+^LzK4jNRxSC#mky`GIoB}_OI~s$vs5f+M}n-@tS(ok?97}B^tk<_m%Q{8ojdvn8kjx4UBgz<d5U6SFmw0!|O{43F2A2P%Oo#>hNkA?5_&?--uvsNtNAmi~eG=7%S~Nn8_-|n~lw?$;fQS&&_WqUQDZ%Z96V|wQP!l`-M0s4w~8p+UZ@5?n$x~D4*^M(Dq7rufU@)AEzonHEu@-JE35d$UbLOW}v}<;G}{faRAOgd#;Fn_!pqU&ruB<Bqa?jw@>~W^@13vSw(Il9nXeVNj8kx)Blx1h&AOkz0v}<R>T&=!Bc2UA^&}nCWY7N;dp*)PMrM~DfP!c4!rWBj91mRyzRmkUOZd<t$!CmOSOP}hhw){$sep=;VR<>t09d~Wo;K+v}o?~ky=MuXvls}QaH<5CE}7&BJV^7t~Y^(!rG3Ex>4&iA&_0u-vMNOFP^EQwdz@cF?-I7CY52A6$;ko0515Td#TZGbirqBe_m<9ZpknMJ4vsdO$wY%#KBMgK(MKY&^++KBAkb6ycV*}@Q7rrZC+R&Heu)C+=*U=;rfZCO3?6*-BK2}#Mv=m#tZ0mCUJ#`uA)OHSzl@l%w=AnMl(5`(S;g5ifIzBkFC#$YViJwzQiV1nb1V_oW$D?K}&S<u58!?(J{W+-3dC#neyYpbf2%Q`4Pj5VsT}*#=lF`nY!;)`69L#EhSquRL0@Wz};YZxc{pT|7&=x!D`SmqGQ!TGNe$zFqx*~9Zl)ZgfIaPvzl6##Tk2dsA#0Mur5|uU>cyZ;u^w7aa%<`e@nz-Aj0kABiWMpPj!nSq~FTMBGCw9q^%lqMNFz$@v3@h5HTKRa<NcPw}n{}ue{+rEO|Hj<kDI<u))FU{~3NiXL>+SATH-N=57slZ!u3WituG?S+DL{f<ffX(PK{4pv_F|ZIx}!ch{pVd$ovvm*FSe?9c{QWG+_}VAC`iHRfZ>3BP|ZjXL9>ixK+8E_Z-%3_O?lSPxs<Qm%6paXCQGiC0|2m~ej{^-<#(k4f&Ete{=Z<~6-GbMvQw9U1~xZ$MYcTi>S9ox1m`RD0f)s(cv@%Rk~Mwu+OHfaUv)T2K5eikg$JP(UwcADPGEB@YWPN<z>_VeKAWuqCBbRJjOt)Hq4%d@tESUpM3tWO&_B+9Gu&)1T5I!=;y>MD?FaSq9}N1}aB}iA^*T4;>CZhf~!<gSb=iOLHQWXF9USc&UAyRU@Wa4nKuk{wR*qk}0f=YR?5yb{IIMl7^X3C8-gmO~&0!=TS2-9%Luk`OC)_VX#A%m{Mrgqdkku&5p&$|KX-uz9r6CT8@7Dy2b~P4r*S9ZwDQaTlXmLy^H2HB0{(^_4ZpFR=Bw@-7<K-L&{Gu0{`=OK{#xRr;mdz!rQMEhO#nE!&T@up-(6IF9i^Rf7x-A6@DL}I<aJp5L2GZh}*3A%y@m`bMh#a1bq0WTqOe@VptttCKf$N3W&HI@|5;CY#QafGyeRV2CD)=8+V@e#mCQIk0<Dow-aS$KE-a%7I?Y*k9{)YA$m9V$Pih~7-*4@ym)XSW;B-DnF`MN-gwoSwM$6d!UofTygCTbGd<?6VtrI|pHI9|bBzBVaM`=oY<kw$@?+h^FK%?Z#Y=^Yg4v`BA$x;rhI3A~P~`Q>dmyLqlb(e!CA!MDbbv3tGXQcIjG+2MR-hoUH_0a(?l9jLaUWZBo1B=#VPvQ>04YHqkmD>25DDL3(f0Xg-sP8)CBjNs@wM8OV8NyiTUL1IbGh<`ha@BG**zf4F6)J5+x^v0V4B*(LMOkGRE>C3C5JM0*Abr58}#ac;QZ%XMGs_dOQyOD4AqS*@cBV1H3jwK8Q2o+uajV0%3K!}UhXPlSOtC)%A1PzhJ1qZSCZ;W!u$8s>o9V)gy#jYx3dGAW)F3cP(Na?U<?G%$E4LHShRJgTt<eY1}@p<h(gtcq5S;MMdIz;%+3^dPf}o%a%AU}21}5jU4<}Hj_$|;pFQt?KI^4k&!L_2h|w`w%d3X=r&(v1bO-gdYjWuuhmW{<^r9@;bxJ(y1eQ==dltTY)-v*gzbvIT9=fG%1@O~A67vf-V#B1dHCBm%7cJ{C+jKIC2Ls&aRZM(m7_m2EV?uoFej)`TFYj#<j`BL-pNbj79VVJ#o(!sg=%xYas_^{JyF^hqgh^+aA9KUXGtGYbJ<;om_|p?d3K*+<g0ClR_9`2wA07pY`QNa|+Wn(@^nCF0ecY_VYv!jjWB2@>u{)(~LJxGo#E+}2a}$bx^rsjID%tCcW~BDQhBim*&4yggAWS%tv}d7$|0JIQj@V}L9KwYT#<7I{jQk6;3U&M+vVGk4R$`$PkEFQh^8-*l4#H)u`i8gldGAw_Oi0aE>eJNAywQU`_~oTm`lL?+%N3k6pwFV)k9G7;l9&pO=yua$-M<I@28{J7upMNgc$+c4KI|&fuh7KqYW$g#vu7Ka7T<yzyV53M5!G?($x{Lzs{p^UT08HWyieM-?)<##4!}R6K0?YKf8`No?5$0ub+P?Zy!@gD2c5(By_~DjX8~lZKuRt%M9KV988W8T2B7-jwc6(nW6FKi8~cy{nR9VA|K=T7=lu}l=m6b~R@7+WT}DuIJ6~K@Qlphhk>1gv7V9?e(>^@u)%|?dTeX&?OZtItqndm2)xtXkQo`FJ^xq}*yYlR-LUDQMm<Z)W(eKq*gAmHYrKN9$fRCsdxKFPh89;AKAfH^9-QvP_892<&rWZWCh@r#{L@v2w!8qd)w+#f>&q&3H@<aPcnf=05Sr^9^?}KrCo~F(A&}Eb7L`qBpx<fph^JKllU)?kObiLC`iv*)u{)~K%55>SU=9r6vaOiq#&mGh`r`%iXwS1J4Kbnpiy{>oflu~<@l%XSV%Mq}C55VH5E!<PO_oUl$CMGMa>Xnb8cCZk0CHSg((Hp*=2`@Hf5&0L9>O(}!Qy#t&H{Mi6<{kUkmm~>OTA~|i9bGJ??h3}IG~2(g=ST}IhMV8s(?bGJcGzq9q0J4hj+g$Eg3Xon7n`7Rtf!9c3y4BnUSQZAOdYLMq{WxZv#@E9k1&^WU1YUahs2njcr|bIP9YF{T|zd**UDgzCbPU%VhWke^9LYBx;?KaO-2xft^_2S2!Ga^;r%*pgY*}^^_U3qGcksfkt-4EQ86I*ln~-?4Vd{gbhy7BfW0NKF}}sQmdYP`kjwy@oW4Y5lN{e0R~ybr30vZq5N>(jBiL1+o)s<h*v;S^-$Fwp%b#Gc2c$82sEoMG^X;S4*^~}`Uuem91Bw>OucDB<KF_i~J0zKh4)PBA1~T^bzqCd&5gzv2^h-j41M&z%MEegMXcAMv!rzYa;5=~fDGw)b5gs33?-g=98Ui%6!y6HJ3}8)7sinLmNB>cYGydWkFgWB~sFtdZ2UIz_MQl*|z#HLa{tha3T<S7pJC_vQ$?b}%UFQ=0RGU>MRpUnF1AdHkuq5n*@-jq9Qtr!cOwU90FvK#;)6+1#feVKHk4x@`n-QkH24tN(pEqtn(1#2s*@j6(vZSb3c<=QBi~s?550cD;3iG8Hm5e#mg%bBg!}b0kr4j7k9uy0_g(w*U&c40_m3j0fNIc89(VswQaC7V<(J{!MZ^g_$8~c2Q2#TpA*N|8PsGs1v?Qo4#t9E(KVED6mic8Gr_A7T_V>4`+2r_^fso8ByH{VjG1U@{C+Z6k|6s3Ln<5a{CsIQfeLY}8SP9UHT4Rh8*JWZd+xBiz+`K(dbg=h$XQH7N_*bi<<vE*uMw{Di{!2)OUaix2VFJIN3Eyho1!CGD2%)&Ivd!xGkhErt2<RRnFN$7_+pGj$ZW9e1>85AGhBOus1$;no3o`h3N{=*rdz%t=jyName*=Xc@L6RHvow5;53txq>duz&-Fn(Kv(6LN$``oRo%ck#!lpYL=pCSW72gV}l9kNTw5klb3o$#K}Y!lo#mglzqJ(F6GIbrXBQ+f`zDI4HXI=BUIb9!+>H-eC?vpVmy{HtxcyCu%7R-dVvGB`>~c}R6>O#tJ!+>tDV+-Q=Y{+?oRIC^BEK?KreTJh#NktSdiXRs|Pa|1yGA*zr6iTa#);o_-g`yAspRm@*sUYs`U*9W`PVX}%Bn(>Yr?>=4MP{sU9%ql@Q$NZ?K>Hz<w)QN}7=C;?>`uv#8EFR)7;O=0OxbLxey5cjOQ<nUpSS>VdOLV1WG^JX9<S(C+eF<Y5K&P)HfU=8;(u)}_#o$4~%L`MYVQdR{X!x^bnIO$6&j`uBH~`pj!9`6Jko$Dp9E&>vD_kQt*$QY6ay_Y*F2MPU`p{=ZAI@Mwmo!3KuK|^*D=*d-Ay>2&vhbq7K{g(4t*am1b<AD}$-3|5PGdnh7f5|u^t`Oblhmy(rF>)3v%t)|YZ~{LrqulYOp>1T)8qFv$~OYIW`wVAelF_aX@b!NhJRCOoT!@Li343Nn6vlNC{LY@9~XuDWT<tTgt|oc_Q~>|&z^Oy*?f7L!G*0~5v9#vA6eF^!*!drc}gC_f(o>w6cu_6ItQ5{0;`fr$x!7P@pT!H8JW30_b8JDi^r|F8G$O)CVnSFgjZO!Z-F(DkE#jG5x%>=+Jf)|<>&UbcekfhIV+;+tvo(xv^UV$lv&#Qs~k#EzSG_ZLfD>%y!gtIc^`>8;(V=A;oS=1k(<MS%ZZlQ{PHn9SuWY-oaNH*BCwS!yg^UW%_8au39n|Ls~kqrHW;hT`Q>Ml$@V52H(VSRMP|RppXkMn-ON&CtUh7Yx_K3bV$4;#nw`UKzh*a6{&W~e{!RVj|0)(48t&fZy2@v%9~7v>1XRujR!#htf*21YMYk<cPk@W_Er~`Z?pedTScQ78ch~lXsatq{h8Zm7>Qn4mMOb+FVbXe4>3s|5QRg&o)^VZaN+CCVC!j7?h@x72E+FX%6z_U{nB)6~T0gKPJ>KNAN5V2Kzx2pPTb1oY;Qr%|Zy7YQg^J;S;bybQ_Fk`XjKZGc`F3<PLeK(;5AdH{O6Msd%Pv}_E^B5XwEo&<Pp9C`iHE^zA5%7_yqo`Ax;J1Oy;C6+A5)8ca;B)^q@*)Y9(3QjwH(e5%Qur!o3*i%hL}D+OpXcmH{q!tC8f&!1ck9i20Q+VfymOdFsrv<FZ+1Bg0zSfQyLHQiWs#AnZ}96RfjMs$OIQYS8-Ucbsv>1OUe-K=isGu`{2CJv<MFMu3;KsO5ZoOSM!yvw9`vbk%j3>3d{aJF<O%OKcP>n_13I)y#0qmaq@qLoMVNAW;sY}YPNlo40GnKFQTGUgu|EinG4m$Qns?5=h;db6P$gn(D$5mIrepuy>Zql8?%f7Aph8sHPwAD0gs<wV=gJ|IoTMZ8QRdR4|5_$ki08N`GZ>1qS{hzds#~_w4^yH;RRg^tNp3{OCe1|CtJF?cfD<(6TD8^r`&}0L;5YyJ^fm+c?e!#jj3wGm79R@w%dgXW6z{+PyvTQ3`!3Ui|_}knph~d?gFD+asD5V^yt@3gN3<aOxT+RB$^wgbr(`rUC;-lwR2S8=?z|gf0gFow&hKp==Ns?I<K!-%Dl~t10~i4>1ht|OW1%fk<*ZyfDqC8_D>1bdYCBD9(`I^J|^jxQ+^h|r?A~%uS_$%7(a^}`$KY6B}A7q5(vWIV9x;;A!HVgOAC}VgUvzQhEYY4xprs3@jn$nws9<xBup|<mhm@+AZ5ywICl_g^%*7Gct>Q4{$Wzq;LUF?(qUrmwsWE$e^MEW_b`~T*r8a}6uXA$&#$i7fTLY}kFN^1jbnB6p#$1RdzNQ(NtC{>i@~FXk_-qs8DnQETR=39>c^myOA78i$4lU9kMXFZ99>iE)iR!m;kL5qDzg8YtrNyWx68;ICH=gmh|e70D4oNi$LO!xZt*BgVQ$r6%DK7;?nMn$sl9h@?>Jpe5oijGkmg&XlPeB+lI8Y`35dA>$Y}1sC*qyLJA!^SztYmKL94DQc1(6?CQ{Izrlu?zua9$Wo&k$~I3K|*Z^alk)59PMcn?DCdNjQ1ic6J^_-YoE95W@-G<&|F#o8|%4@K9I6E#~@{XMAtMzI5x=eXMSUAs7Ne#KQ0oMx`r)&H-MPg~?XLPH5KJ;e@8>hh1Dwj>N62%|O7>vFYnT`o3}{peAeq)-IbtTckQMz>#%M0>~b4nz*1Fopu%PE;ry)!G(H`+YkIrg#yVU*sM%SfOV=XF59)p}&Q*&U-h#uV3EA)r4Z6BB*@g57Z=v3R73}*JCtpFh)J}xDx~{SZ^JPnp>1S;Uy?Z7#pnN?PG7bBju+fYNSB4#)-=d>N<^PKq-;G^h6-}3y)MV1K;VwHhamJg|oY5LODk~&vs=%3;|A&4EO3Vl{HiMP9nbo&x5;{nS~0e>vdNTUf8PwAMg54sZH>j2_UZ_@W)CxKfLp^<}ymA#p>?&By;uH`NqBIl@@l3VDk7siRYTnr8MAZuA)L+9aNbP=%dSpJrU4WaGaW@2nRv{jKr=K@to?GC95EQCh*_xI$8b~o=$$(f3*IGeVW7DE(gvUEIXPAufG5*B(r^9&*MDMdH`hI@4J%#4lrrtdZ7aH$EIgiv_GFDDaJ>f0`p>>O>0`5!d})~04>Cs6eZ7;u83<#VA`&IqdXP)OJQUMjppa&bQ1KJzCNlYq*%N#uEllRL`+rWyfsm*=eO+3wKV;7%+`5JjOye3k{7J#qT*8W_zmz(b4($*w2Vxo8C`uCggF)KVhhFMQL~prVwbn(Nh>>ARj<BcmqLo0v0vNE*0OB43e{PP9UNWg-Iu3uzE7ejnrP4Ak@$tvrpX$T80TEj7(K@A6TRV7u|TzGLJ>T3QifVdXU}n9)6@`MJRpY`r2c#z{})|k!sT)`DETo2Sv@bpp?{bp6@yHi{?D;uA%)&Q@tIYQiQ&Cui>Ij?buR;I%cHPsL5rg!6nRy7K^TKu9NGU`ei-+Lz#N0dA3+Fe6Qh!->60UY>AfMUF$8G!=8zX*+mZtq^7}Q0{&cmN`Zo*yIuN{7Pl`94g_}vWJu;T4u^1veN*&KLr>|{VV9$k#w0kQ#`4eh8ukiw~LT<I*$)Xz4!@p8goRJz~t(28>Uzkoo$A6PdX74nb{ETI~88h|Nb}}>RFw6^^4IE+aNi-|-kOL-$d#Eo|J(vm@Z>pq-a#P&13od9z9nzp{#@FVm04^&^qK3)){uXX<(2kNq+;8?E^XW_u%zJn^#J}CA$;%EkE`-NI>sA%eWLH_UXu|sz7QAXz-H`R#lup~{jL3Ps8Dh14!BD+WkJwZ<5|#TmSR|(P?Rd7^{Q!!U^O*^v`7z?r>0_{{N{EJ;?a{TC^;;CQjQ+v=?-p-`ZH?W@6O6u~bJyQN0N1L3b{TVlp}*5k9dem>ChTC_Dy?qm1J_Xuuhq}KQ&(D*0YW#`!wF#5=coh0O)sOdYMB286Dn=8%w^uEdGm^fnlMMNUluCsLrpLDOFankTaAmXg%?%<<E1)Gu*EHCD}b9fbIc{}Hc*sZ2!5H(zdo87<Gb?4(hKP|OdsHVa&r)^)_Su}`VVyenF1fxg(l~Zg`q=7%bQNVYx@<h`MRPAIfyjBtxY1ZOZ6pxAaIGt)xuH}C|d;4b#~;v@7Iy2SSBV#3;PF*rBI|q=W+Np6$0>W#G8iJu)M+JfbMQ_6%^ZY56#tSw#1E$BwtXXknu6LaPwVirXigPaFNp~`e1QIdjC6{wlC>&?`C;}B=%)-a+-3=z=b(9I9nnA8Zww3Gmf`$?n*M9ei=AX0t<hyAd7e%U8OjAH$H%HO+(J<jL_2%op*8!#)vRx1{8Esgf^Q})FvH{*F$$3rULhBwD7rM$RIF1@SHZyZxoAvc*yJ2WI$8!p(N8vug6cnAMd)}bRASt1xz^tkS{JaROokD$=Okg1?v#<v&lJfbxWyWf*U0=h|H-eG35ojn?3`m?<xK?ICdGRL$FWke`b+APWzE%<Wn7nECJA1Q4si50_=U>3p7~gzZ){<v<gRoC)a3;1L?W*fg77`w+Z5RB<;ZrVyAjbyN~|y=S(J4&f4)2=Day7v4_9>ecqD>le4K(%VH_yL<Sf8H#*RkPP5^FXT5Wd;uy0zP&69$lLSw>Tv7!&FBnkgRKTYC2$g<|Rc-f*q2-+@tyw|4i@tb2Hu3cRjxeNDM1ORL!aK970;1B|SJ2nN>O8sRV0b@HuN@+<rUm1kK|oOqoxQbsmfht&b$hAd9%{;+g?Rl8Xv#t!jVYt&+SQkX+z;gp%Q3F7--Lwdexz>73#L5iVa*s%#RnUHBPm6-x33v;l&j0OUHOJ=Yp2cokY)D})RI)UQ+Lu`PeKl35<C72HS;RoxmcRvb42=rjuzo@ugJk|A-Nqye4t;V&1IBIp+QA24(1zkk~8&gI0C&x%}xz*DYtj4FXHwW75O;IC*$%jr9#2#5?0SbZghm*%Q&tm;X6QAuVieK;<6Pceo2V>I)fNBLmHoeGGBY6BD%yURdN}yWjnZK8+$p~+zZ+`Z-HU4QnLexmF6;{TcE>86Le@Hq276R|2+u+F@%2O?2)#LBQhF-<w61^-hbQ_H_AuUxMo0?c>ZsRtEoPH$?Yz><#f2N+u@>&Mz>xTd77g-a{J0{b%R3Y!D4w_vEC_21(w>wO-v|IYDy3qHZR|SsG9+DQ}saR2EBIOB;3w2I<;<04{3MdZoxWG)BvQMN!RQn!u2!i3C7<L2JY#OpX$oJ^OslC|E1E#6VQv<P`jSWcx0Fo(%u?hn=M+Us2akGK4$E;Sx2OKo%qS0Ro1XA1|7OfV^F<GJY1q5z7;!#4^@qPGXcU=u`iAjHd$x2auqwnmtZ8o8i=A2BB$wT1o|M_`)q<#aAm7w<6N4pZ1m$Fivg|FvUjSt$q_De7GesEMU;>i=?hy`S<i{ZSo6zjmRyM2J<BilE}gpSD3G~Ny3d6gPyGZy%HYPr7EL2XW9Fce+6pBD2Z}j@l-m0gpXfJ-wK#x!31Bj%rQ(&>?h{%+Dzek2ww1INm)+4j>`R~cDO$KBkSab@q4|)0_q(KSqd}00eR1N=RTNOp`(>^bQMB~v4wyiPmzpb8DV@e%?od6+7a|>K2|ltkr$`TkjMN$ve=BVw(aoa7M(|qZd+t>oiF1cv1On%VJJgZqAXeUMJw{XZ=cxqm;K#L`t%b!ZN~bTO2}p9GhAffjm~>n~dcK*jfZCe?mBjwF91SO(5j|oR?2r8IN9Yt*TN2c|<6j994F+7}yZZwe4M51P9u5e+yL7Qg2*}?}(LL%DeDH%lK*r75*;IR!TtPw=Gf~V7WHOgR*aaUK*|zSWlFwB2xv~3ZqwCJ%mtmPKfMfZU_Z0o$_Rc0m|8&%Bn$!s&YHfBDwi*(Jg&jQBasg*xdu@%C+I`ddGiANC^)uf(WugrBtAA2U{WPKeZi56RQ*G@mB6>|DvTME!@zl?+Q5eZbOE*-YSI*CZx?B@8OQ~;sB=YvJ*$=c!X7`K4S=B!D&7qv8s9@~M6UDW9oQ&A{(U0mIz2+oo?zJCwxsyxNhp=*15|Rem-_OIY?qV7#FGzOmne;bvfIU{B31oFrWA~Nq(t$NHh**`u(v&TC8U%O%YwlR-HLoiCF0?cI{E<d%XXM7Y%e_n^VouQkwPMv@h;RB);#5hX14?0(egm|`t&afNz6i<3tFb)f?||vqp+?mmD_8|2a0I84>`?Sfvjk%%=2Pt9eCzRU{nPxS05|lm&BuQd6+L(0u4tysDh+Quk~OI2s&Y487GS=FI{O%DAdL=BG!<W<7y1l=ao9&+Gxi7cLsgzlDXf^zCKA;t{j{X8M4m(8ACQ%XsoTxLB%P&<rf{?_X3FDPEk0gvFi6^HE&$7ZU|sN_Rnkk()g6N$%5f>Hza=8^7Dh1wuaX87bD3u2PJ`rM)k?*pf114|Yi+w<50{~i<B=n&E^k~4ZJ0&hQc{NWLSh5)8$0&%_#EFDh4?x1={Sc-<Ikq7;hxSi;or}-ZLYC!<^~ZNWSmHy)60!m$1B#^jB|#gxYOlXVVToQW7Nf!kB3cLJmqu?VrJluiL7K@=W7O0Zv}ecNr_HI0PountXjUUH(^&)(P8QhNq49ML{bf#v7956mC^})-zEEj=B-{KJFmTj85B~MaZbR#Vt;h@UJF43QbG1cnTxg-pq0x6;RQ}wkWcip-pIl$XjNgg?N=&5sz(yro8WtD;RLo%4w#5Q!Zlz#0LTq?`^H(HjKc)MPx?fEhl{Oe-%XpKFsib+kQL0E%)>@1n~<jF@PyZ0teNLOZfLYtWS4NSV4+?E_$cRhToFJ98lh^r?f>yDpbZ1tuRoH*{&%!PgZDK9CT~^UO{uxVpHBow0ym`YDl=n2#TCxiA0btjpe5yei<U0Lqc~wRrR=L5&E)yj!3l{Ke@tYChHYgn9i~ytm>`lz*+8}A3OpDa9wwsevxkX7J$DbSgA6+-7wj*ZmZ0nTmU@5l9}iPW*`7R`YB^eN?*&`f@K0KuudF-SIe0rLyTA^E@mk(S+6PoUg5^S%uCOq!M0V>c_E36J<)N;<qW%o(N!OJ$rRV{JPC7dh#J(`|dB<;77)n*@W_C-jXZm3xTAX&vK<U70N`z8V+6SpJ`-vrRM!6i1fM~ZTIyTuuD@pGL8=9<D>qWv+DwV~NWiC2-BPy0`qYxU_K<xD$q}x#|^2)^15ba_Q+8SgVa53bmH)OJ_-+D!f>{LXasFp+XaN63ept5EKwmxc=c$GzyL?IU(C%sysOj)Vv=t{+yv^IJNqbkJt#le<=)jy#upJ=2D%pmSN5{45glBJjE%d*En&Nm20C!e|Ln2ERhx!b-gW@*F)Nl}#A+I}i^aN2&S)`pLZ3O;g+{8i921OH!}Dmw3;;7^aKdpjA=+4zcbo})l1t;p|qMKK`oS|ICt!gXHY2@p`x8e4JLIPF)Hvvhi-Dx{c&f6q9f<+@7PdLr5Xm_L}XhtahUKtNf2?L*X(S5GWz#nPcjl$l-h_)jcUie1(Tnp3(>)xqlg|GqXf56X^S1%z1e+rNTx7&M`Da-^TAf7EIBho8g$>v5=+rw>xPJbgIQ)Cc{f|A@IQqmkESX%it;22J;7GOWZkd~%6H<#cYiz9;7})@{)5s`J;C5o~J0^qB}bOgupeg~XeP*v^C?Q;E$iaGVAK)7StshCA`NcK)E#>>g6T-?pyQZOro<ZvScI`2sS%oSZ0$<33F))FQ@>Pqu_|W?4HovAx5EtI~+*z}FRfH<U74e4YWw2%LNANVZ%>vR4^iaGurYZi5OtJ-biW`1M6-S_0^DV8fg#gLllJN6cd9E$C#vmXkN=8iAaq&WPIo90*2ku5jszX$P1L3CcH-gqy!>uxk}ER)akvX&zx^JBs3Y7x2{wLGbb@JQlcOgpvpdVEaoJS@%pezs<Q3hYBN^rEW4?x#@13D3yBoFc&gFhR<!ln#0xys8_1d=MVTa1DJ}(U5}y3;~`|yyyF<|1X2B?GUrt2ym|C-i4~odSC*$I{avyXSgK`yu7S~Yz6H%+xOt2NVE}U*0{(V>sbnDf(rKQY<X6aysABAmWm4Z;$V^Fccy!gtX?;=b1)k<K(<JPs035P3Usa1KaHA|g;X_@)XU|%a4#5AwO4Bd>cv+#bPWx3id$%jqd)BMDF&(?z>|#Q@#F<psmBHX<&T=NOiFl_ZBWbUQ%gU8@yt-$G!;!hVJ}a?0M}K|-h-9IE^0RM(c?>&k?71Q9i*RiweDH$#itqDk+*f^}q2ZXGP*V5^AR78-VRrSoGA5G?);OlzQ5DAv4kzw*UzST|gMQXsG@`DI3Z)UTB)h|J(lh^ta@=)6Oi@Ls=Z3h?*s|59(bbOK-%$)kJldryMFcvRj^b&514_`)1f=CsQ$C+&lYQH@o?6+|I;f#V?B;mIEsE>Xud=t>fs^dSJwUn#Sc$ypC?fsW+Ly39<u%0<XJ*Y>!^}|iP3!-30(ziZZxGT>HF)pb?B*zWZ+trRni_PL8pq!5EUvA!zFr#D{qYgE;DrjHg<<2o*MxsSlWif4_jq^=WI<zPE>&kCqEzh|O}xwjgl~37NNh5yf8ZYM${oAPvZvL1nmQduNL@}?cHw(_xw9oEWg&>45_vMJ`gGleQ=nRBF%t9$nOjZ5kpWP!KF;lw6#BG9-8utX%*HS8bi|<fY+cyM`Bo&rj&Oz&Q7Ozwf8F+5u(`A7Q9ThWs`QQE)+MmY`R+CErr8>K@*vyKq4#By&DBY6F6VoCN7o7Vqth+m2{9Y^c&ZWjN6UHsa^!F^nUQ8TtQ|QGFAhSa-G8;jdkxB07R+H9rInNtBwHNEeROQfx)#dETOA&K;I?Ng@I?qP)in<*&5F_9M}}5h)r%*tV96!|Ee*jRU0#Tm>Tov^dcJ?V$m11|WvT!!COlc!Z9KVO*dw|sX@PD{iuhG5u#mOJNUXl{1oZ5lmYFJjX^N82#`bzl8~!TS_!{0f0<%0>NuiTV5>0HyqOEIKz)%&jcuoq8g+)syFLKer{T%!F;hEVy1<s5q^?}XoN>KzSxY?UO8Y>-Vjvx|FVD<CZf6|?$p2AFk;u=A0_TjQrlN<`pjQkj5X8bj%t)O<)K<+&8V8-(TCr=sokRCD>tu$_Ywgy9Vro}w*wm-$+Z4hmz5wtA7`~2Rv9rdLBzE1V3qjROi)$?m-Uo^$qTxhN%`J*Twp`#L@CSDgm$ZC01$i!F+*zb9peQEjp{tpy!b9D&@j2$6CPm!7yBD5fB`M9$AU=<TquzvRXWG&HTy3%qY3^jr34$%i93#h(5OHCW_ofOi#Cz~l0Yqlv`@8ikv6HTM=b@4taG*R|hv6hbunU#ucdpAAc6~Tq>)KyL=1K%tt2hQRuPsgP)_%*B0JPxv4U@C?z)!I)OfLHDLse4DZdfBodpA38;fbb7V33HhU+^I2%Ae1yW!|0H{=ZNv*nEziZZo`l{%T_<#YYSm{!@j^|!m^9D{!S8`$Z1+mRZnoYzZ>C4_o=~pQMby7Hl*7Z8o=@R<aZ9YoJq}Co1C3Ne8<Y<f0zs`Gt^1{Tv1n{ZCHztqflrmup2n>14Vcu^vko)sjvr}gdueY^)rnjN%+-wK;EWQ#_-2#1&L5@ux6Xgk5W+m*4XfKU=_q7&T@9&k!8XTywWFX@L6*@MsIh`3u+}vWR@+Cj-wouoyAsYmg{!w`EiIWS5isSJbco!zbG#-wb54miyuxno;KxeCLye{SQ`lQr;-E2*59be)?Gvk^I&$@ZW~0cwWz4C2H*zWIfF<GR>CwuL(F(WX)6obm~he(EXNFcez=9VDHfs3zWrQBme-gE%NnhI9CB^UL65+94(EEK>57Phi9KnUsQ`%=x!tt)2Bt5`Qk+1CPU%IF*F1dyCLV(8reYGjv(5Sb342A<3mV(QjE*?}0|dMtCXml2=L*i^MF!2D&TpLj*}sV(L%oYZ*F9*#B;SpPn!DVQCaUBRBS%gcB6Cx7^DL-)nkk3A`pP@hVd$7~eGk>Epi?N4E`}@$Kom}eDr!2)`j%lmR`f*e0!==Y=jtG{+;*b@Ef7gaY+Ynv)Lh4r^CdoDX|K`|uN8Gi)y*NP+mxoQdm=_*y-XCG>W6<oUv2<yx?ci@b3kNwJcS}5l}MFTj>(u*pHT(C)~RH=Zb4_Vt2`IhRHx;cwMvBuCw|^Q+WWs?hpEBTgJW>Bujs2+NA?erzr#548pS>w(DTQ4m|n1EkkB}~FX&)fuk{V(m?z<JOVRos_GY>g!chAxFOJ4o+<|@2Uao>xG?~5kw>)A4A~V(z+dg0AIrd=*nmk3a(8@^!Ppq$-(?}%fPA!KJ5>_<6I6)D==QbBAq|)X{UR>7pvD-=|{ooJg>P3pb<d=<<0==ryIZ~|wsAB}jsm|@aqMv_|EgsK_4Af-P$1eaziesk(i?e3zCE8N6Ps4I~PNy=pXsVN#I$L7RXSKV-lUj5<EHdKb#|AnG_X;o`S(VK5X5B7EIq=%wL@4)InWn}jUrc5Rh@NlJCxrp`L(P{b?s(e(;^`AAZb~#<t)Ct7vr!y+l43>x_vEc?7vmz<{`jj$H0qJ2(N{t0aUfOH0Gi+cQCnaWe$^08x?Wm3c;0OE{N7(zL}HIVv)pe#l*Ty(MH_Bq8L#M?a~K132=?7I#xsc(z%DTax&}P#6|9K<-0a}u=UV4hSz-PPl?L}4gI5q~QeiQpfiu?>_h?P0{Ru&U^dpHXOynE9#rxPcbeqqR5?2Shbrhs9?nI|_JNMy@wV@}|;DsjrR}pdJ^b`HuoRQ}N7QOvQD^^GQCB_5Fpp{JgG_o4>A$Pf8p#?px>5W5iktq$o@Snu>*M?l*t+h#kH(gzj<~UL-nCcl1!9)!(LO)^Trg8Pl1+}@Ai!NUnH19C_v9qAya(fzOk>-0Sr*Ph=^<JP2EVnWpDdEz=)QHZs77zP;&tw3<=Ca!fhty_c@|-GE#97Ls9K$oSF*MC6bLH9}RWQ>g?^mr<d9@5J2dTO=g9z%C;PpQ{+SK;Y{PmJ1B>UDEV%rj3<a*^e*y<BkB&n3a*)6McPNnhKk%iP-^vj4;&2^_#G(u*^B_+gL+r^=?-sRk*F=|7oo=}mP8y0h95E!1%u-<SQ2y}c=n4#fOnL%zS_7JCA0H0$40+foDO%KNVtPfBN$Afu}q6+SaN*EBr$<p$b?D*u}8IyojrZ{fl5g^g{U$+pIlFU#$kJ#E{M|M<_65j!E(-Et%uKfK=5)tN8h|BN%=wVk*B2k^elds0?`7R!gLQw)`Us-H=5P&2qs~TCU6wJk6Y?E*X|Fr_^zXtUV9n?U0ZL1yHXT&DNwRtudhd%B17`<<j$dt#f%V~Q*qdXN0`QbVnKU7j)sDSr&{Rllu=!!C<B$UjFM;k?{1Urw*W}~5M%9Mo+!V8)PyI(2ni+HoH>)ozWD=ub>2%idPUBWdVdF*z4e2_`tTu3!kKd<8LU&#x_^+2WTRu{0C8HdXYt?&5NgE-2=!qjk!yqs)4%AeL%3XXm1#ywqeE`N}<Cey^+AUS2$tNI}6o!K_#0royJ3{yG!E$_?-YKc0(jBi4t(|$FG-9O6OGxnlkxh-z9`f-bEIhSW0SihA7ZWhQJXa7uK%e-lZ#)uv37oGvBbnChk`<lmhY_?{IQ*6qBu$s!ss`^qCztm?cXoknlk1()|LUG{(m>(dE-LT)*^CNafO*DK$IF-U1+5W0YtRlQ_N6!60rUNi4bif*GX|bx26ed3fJ<5p##w|D!b5To78v#x0Q!D6%QE2?Fu@)FRI}C3D=<O(0*dkA<wA0lC62k%x)%5M6GKH4`VSu~oXSnh|?Yx%+H6s)xUrKbOn207VfJpQXuYYYQ0ixs@!+1EH{Q**DGAp2LnGX5O2Z<M~#DwN1G>fod72y2s$3T%2+(6g~%y8@h;#+QZBk3gmxfCUyt!rM$Mv#XnEG1GRT1+n0oIBRWu>r~G0*z?y;o;?f5TU*o=^ir^6-`8htQ*c+>f8@0K{)rgR5Hc&bB$TT3p|Y?0y(;F7LE(=g`0^#QxQxPahT|uK*W^2ST+zw<ulMLEdBFXLF}l@5wBZ52=>2QDk68mQs2QG-r8PSW=MgTL;*6n@sYjGw=NXp{$eFOiEo!(76M*|A@Yt&kAec3AS4|Xy)ozb4l4Y#@;;VZ=g!>u=PG<@X?%TPo}ygfnX_9`q71I22*J057FE&Q5A>QIRF1_}ISZd}YX_jDHkaj{w*5{k3%;XygLv>L*Tz@U&;9q^Oomj)N!7XUQ}6gw>Q7B`c@$<$Rw?uVaP-<!-zLNRC8@_AwMc!!guv-M<_}*6{SHXD>>H(v{2dPRa}V|MBJXHqFMTnb8jgZkyD8mf>0?;j#_CyE=ClN26sp>1Su>eX*GIdXfORX}%Q`UkZ0xpljajArU9YmCWdqAZ7pczrNc;ZG!GX&6(ScyP-f(W;Mw<a<sD}Rd1vm#}sWRuB78JCA>d~%9`8NeQ>-o{s|BRB*HT0CQ4}1?5#Y^6J!jpdJfz!6MI*pwX^j`>Ydt0zGJ}tFaqH8jw+7{K!QeN^SRSB9=9krHEtx~_aJZ|z)Kb#Ol+Tq%1;wPbdTWtdxS_jqP!YISQ5-;NYI*$g+P48&j%&;;rA!6`nu?r`Dwr-g$P&YR9C)cHe&Y`Y`DbGS9K<mj7fyZC*r{Mk6oO{cwSYWVTKbK`j^3AvHbgm`Lg`iT+;y{oC$A}=<K~HDVmKtJBh15k!ksDN$vZb-a^%G*FN0vkLs`209bowe!zW;>StkclafkY-9fBSmAp|uezjDvAAU&v+Lp!Itq>XRDJK$;44rQt|Kc*elFgVBn?YTM4Sob?tNpDwccSVG-v7{#nT7t~7KxPSO2^%gAlytJDWQ%vVpkhfg^mES&I@7*T<qYw4`c(!q?7&eeZ&Zvg=El5#+-~)v)YM6Q0yG*ZRFp4iO)30~0Uv`8+2}q%DO3%Ei-;hZkK<urudr0|-^8jx&#ur0YMo+ju?a{!eLF}=}(+bsw27l{97tl!Zn^!Go-N8%tkKu3<byXa}`D8K{)oV$F`A99o6Be)9CX4=?sE7_ki$}r{?mC;Pr!V!Yvv(-bZz>R(qv}`#z4qX0xe7z1Xqh<m5GMRzU3Ilt?@&aZV^3$S4{QoTUSE)|+`yI~9p3{WlQV}YB&73UUHWcR_jD@fBH8aR0jOD}wVk{L$Fv^mE1JgCUsMk%#m;VP4)?SGY!(nqWmUM+&S)(vnIK%r#>nEv<ZJBL!fLEIHCT4NL({(+tvs3SIgFUbofCz~HC;=V=mmj5TT@^tTx%6xwh=L?nGb24>1(cEzJt{B)w_9;5UrP=u)*qWGnlaz+X?Tnfbn9GMyg7mn1H}ti6i8;7aoxsl&L&I2l31^I~~(-=ss~LrhwV@|AMIp6H&7hM!Jc8JO4*|hHq6=ZooR1Dgh*5?61@`L0{;Sdl8i7vfCc=xsM`o73QW!hil|PHK?>x)Bt;89M(TSEwOl_q(#(e=wh>AwTa9mnPj+;(Zg4}2_hC?zC_g{My9VazRw+FpWQ0`lkf6v*LPXTr{~5gouw<STGdU7#EzYE2dp}ji9Op+YH({Kb=DBTaH4?NaS2RhgGU?$?aQ^1bnJdkW$kv$WU^2RUc-{@?tN{f5_71Mi~WMZNo7vMAVtlp@k0R^41uJ_+qW3VBEHAjP3B)@?0w-5_G>sWu1-f!`frA<x}oIMfheZUXWoaVM&1|87_2#DbBXO4yGS_1g)^WE*je1g+AcdPKome0_Xwbf{`;NszYbuq65#HdAXt8nv+4UfUDn9)_744E(gCTh<|}swEP-peabbV`X=_eE3L6go17RabweJpxi$j;Dl-ohiBV4j^&g#OZLUE?l%FR5FfDJ&$YL6_855$vOdllzXD}zc|{V;}Wiqr!2o%7?t2AJ3KLF(+on7+>?`muxJBQDz_?ihbdAA=tm(%arX*xI0=T1;H1*fztRha~DPrNgtWF4P5@i;rz>^1B^N7LO7gzYf^T=NK<wSa~RrnOeL)Ik0NKKYd$!3*QuPZ9mY_Pn26_`~H}5fY)>YQX?cLDO%o%6fSPV%aww@5ws{TH%@bdC#YoVHl<|CX3NOhaeG$B30K#IrIgRk#gjD`@DM+-O*ujgzR++cb2?b9R(j8xGPHwZQ-MG$435=mhbD$IM_JJ=5vjCAioy#}ecrv%xFfYCoRV@GWGS&n2(7LVX@>7~xtXVCeq(fRoWzUegAEw?5?`;8hv{6&@TYjN%)5QOR4Gqob*<y340^WR<k^7)cF{k(nGeb_cIqVop{*}PbQcN-!Vtv2XwgH}vVo(?ZnmZ_RE<doCaA_2whN4I9I*|rVN1BVL2mK5Jy7yDX^3bwl(iqIF-{_l^x%vq$8@LRzI=Rj3LGc@Xb%G+b`8(GGo{az37NB=^^-XE=^x}#tg>f>d8F%sMaeN;gYbts3pBKk3^>3lld(*tuZ#6AwBKF@*dLGHwEp6$_dl#98aK~u%cDz?pvVg#f8<f3q0ca}o>vWEs2NLZh&cDF6MhmE4lR~T_#C#k01QR%C|{{CZl(-s7I~YGa#!0O>j6#y!S~|6%ZA@T$tCQmgOg~!k;xIDm7a{REt(#PWMr+RUFr6~#DyNXVd~asxg;N7ulYp!D0<uYMk}vG9K#EHIN{>cN~jR{Z65XEalrSFwGK>po7mQv*1H*mF&dPBzKP>K@qKpV2owbXUL%F9<Zx^La0#rLXu})=O9rzCGXKtJMTcKI9vY|)AeL{4Q7(Z5-ZN1D*!#*I%qFGU*f3gBoog*|bj<kUO8z?{FJ4pSk=pYkktw^1Sm}p5cgUY5psUg==)9N<<vfC6BA%G>;Ayr>Yj;M}ZeyGrHu&tqNTRwhhgjuZsX9V@zECilnsC|-Z8p<V9fsK7%i?qq)nz4_%MG}686M}2A)+|Z4%(FCK18!RE&-bc^tf22%YuvM*g?{FTpIB{(nt`3HVP!b5a)k(NL9NX506blm)-!kDW8TOf#XpXrJWHQgWsbVS6F|SA^nllNh!=74$UssS{F{(p=T(u_B}!n#orbb-=X0+nnHx9w0i7JBunp}MU@liDWyky&R$}$&zStc^fa0YOgk(w+|@8|fSD40R?{i9kRT`z8W)k6o}`@_CsOfmimR2`hMuMGl3<a9;15eeVGB6Ly4TB8x+$yUX|B|Sh2-c&5K|N*p9AsHHF#^=72bL<j$Z-mCF9Q(BycvK7#)+2TnmX{$h`~ii%2R=fgv$;##m=QGfsHbLDvD3hgT5s8C|iSF5+KguhEtL<+C*}Mz{%)Z|G`|xSUzNUOKoCC^<@gPXx!6b3~OU3zBa^UK&)BY3qMg;xb*PL0D2A{rV-0Yw4n1YeOcgG>|$XPX$_TtA<Y;b2~ePEYs(&Aqs=2t11T_nnyA{BtgxuZnifMZvWrIbQ89F&04k~ltt}CDDngCkP{WR$O&RYNTwv=_w_bV1Kc*M;eI$=ysEOLupQQ`<viM<QAa=uAH8013{VQgDVUNV!an?fRthm{ZQv|U7t4H={vURQpjIn)gN_6JM4cWGCCe#SGyV2Evb<<?2X2j{0_fUT#1GH?PL%hj*=j+B=|W-Dl4MmF7cV403&02bm^hlOJJ_QxVbxYzt$(2hc8McX7P@I_AcjHXL9#<P^rfpR{iaNm)R2&P7_5E0iyvk5X6hQ%amS|~yt$0k2U$HLU1sy<_upXgKoz|>T#>ElGc9&<R2~p-3pNu{RLdrD*EarvkJ1ERJKv8nQOjC1J#b`^t!{{U*3l4q2L2OiVb3%ag6)r*rn{w%Tp)lDHe4H=S~5GO_D8LBtq8z!g;e1%*!*qpvk2UdWGBb)dT)p0>Vf1kx{TjV^>AiLCGLJlzPx6s4D)BskCpi|TwJ@I)3|<-*<WF>c60g6c1X?*3GghDMmx1jFkh3=Icci91}bl-I1>}tfN|S2Pkz)l?bN{tlDJ4NzICJI6c_~p?UZ)WqT#J-Qr#v(X#LD*nF^LpSbV2w4Sg9B_)WXFp-we!^#d2A6JajDRebi<Fd)!Ue4pa*tUe^O<icn1`4iEAve-xJAA=f6NbV&aiAI1Ca~wa`+XSPuTk7G*uBBNmC$!321^^l_6LW3KPx-vK0Y<teaY%C0zpZck)75DY2Z-d_G@KEogT*Mfbihq9^rJ@tlc-+i-pj7~x7hp~{l8N8g<#)-El_NSuEh?pQ*=|OiYc2f)Z3o<P2uBnqQKxu%iRa=f+sNg<Je7j$ZrHMzGA#VWQ{_3_)@ZIGIee3W8cE>zUH+*f@dfaJ0<l;d8G0f;O>Ab%=7-{9U5fSP4;t)1nxD9>m`PLFkY--DYgFkU&<p2C_wU1r0>I5_h?0BGNkC_N_X+=f^d__v|o+gIl%n*p7bAQINXE$9@z3cHNZCtFH}zuC>9c8+G|-UNwp@J|Lc(q*%c4X$g$=z4S1Di!zz=3@DFI39z@`Ma_6tL)yXC(8~+^H_r8@-u>0}s7&U|aX4<-uvnm{ka`)3R4(L7lL8}H=_m9j*ykW9#Apbc(VP&A96%+3R^n`1q?w+Qb{-{8NtaX=CZyRBs7j)Gz*rsbNj=~pRLa3<^9+^Qoc8L>T6p?ND22nV?1OydcqFGu&9z#E+4P1K(E-tcp7LTQlkBJySuwvV3fLf&E&`xbg0-PY7o(qoo&)Ni;U7@&WxwC&z$Uat%K!$>czZ5@L(kvT5LfViYX$T}ls8*vo-Cf5}TV+w(($HuROx9E7;MD&oaZ{Wz)M4H<8NO3l6)#eVk{zaMX?Z#GBZLY~P6Jjl&hQDgux{*fN%rod5Y#sBToLyI*mI(ak~JD-XjyG|L(4Vs6Lt}tLos9(C3X;@77~MKI3@v?;-l%0`RpGhGR5x``NNzPcG7BM)-?L<=NlC0-)xB~F8BzJZf0x!z5P3|5Q_c=Qbj)-q{f6m2--D*@|cY5s^|jWijXGI+E={QRI^Fbszoqh>b0`Rigl2$4sSY3Vmlqsl}#ZJ#0)-oSRd2E5-TF|m~>Z^)wuRVI$;2a7NfujW;vLKqZC2*M7`yGMcmm9vOOyIH8l452&wJ2|9E*t8^c|RR6JJ+XiCk}>AaWw(zrMGCWs^__BuJY#@C46?_S3|S60fVjLDbC5SRw=0=|XzF=N!uxq5*{@>fN4E1Oh9-}Xx07(t5$vWX!^zA$c!mW)-qwp<~qGI_>B=7HR_baoxum(Z~1?59ei)(u_c%0ugh%hL<#Q%NOlixgEY=P@F18E;x6Yg=89Y3g|JX>_t8;5k1;mE*2spa)lJOVX4(_H)9RKL$M^!|q;XgwviH=BFERL9PF2q0RqmLOcfRw~Ku+Y`?^Qx1E&4Y;a#3Ih)sfK`gzIchndkT5f9}pvjOD4g$XY5>+Jpgy&VG%a0JrZ=L!}0r@Xtq7m(fUHJ@Zoi9ILq$YlAw>6~!>2+wEDqsT6;#ZnvAmZDQm&k3RPqFxI7s4Ja+fF^rz`$T-yWn%6?9Ip=Ts&B4EcFyRw+*I}l#uk^#y)&;(ZEvMdnQ!&zG{B%YO$SoRl+ANqogXDwt#$&*}#_#l&`Y8>czg<n8dJ%nit&$bxI=9XogtBW#Ywy^D0#UBvf@BfY<^eN(446(`mYZ7L=9eLNU+Y7}zag3aG`CjJLLXldH(CgLcklDqA#PbEY%Wgv&`9f}&_gS_j3VnS3Vao?T}*$R)(reZfQW*auf}MYwmi1RcebI1G(&Mf!?T4ygHXF>3gIlU5_T?5vw<A`RhSjn&Fe0EO5PJk+f!%t0)F*Qu)%8h>I_ti1+WgmLbrD6YaR@h8r^z?VB=9gjWQ&GCY5)eHHt702VbfY*rM`-+%E9_S==Pkj05k~$-n5nBnc7YhoF><M$-dj8Odz3lfCYJ1(WPI3HyuVISrXp66N6E+Y26acR~oc#D1u9-xEz5(c*IGMaSxWq8%4Q+L+KMUR6{p>Y5pH20ZGtu%>3u|8r{2+iOF03%AHdbjn^+fc1iL+zH?dcC!pv2d*k1sIDJ+hW^d<=szTcERq10<T*Rw6$%c(e&&xnEALo@AL{;Xv<KxX+K*ho=-tNRyAP&f3ZyJc5m8<i73umv;VjdX%i=Bo#uZ@w+b1{WXB5qkO)H`L=s}!?ngzyjp4>Kf?qemc1b$p`N<;Se<ePl)zUBpIb%t1qOUhvr(MgM1y6O1rfDV@aO>rI`mssaEjnL`T#)7B59XZRi@moh!+71;7HQ|>574kG0^LBQ=(DuVvmEFCYGI1Bz>?c7^AUSATu-!?zEpd9E*JVsa6^?0p}`6BPni&J~%XA)VJjoBj0nPn`@`rU6knHq5!YJ)?bB^EdLjF*abWW*X@s0LHz6l=4JPtZIV5HkSs3v4lMP?L}_A=`n32>?><-FeFBj4qv@zTohGw{o-;5l!aikF^vr^yfFkZ_Xbq_?yeh5CYN|qyv%v{H<Q0_0zwRRv{U1muS~|ZaZ5oVNX2ZSRgPy~KE(3A-xPT4oYI>xJqO9C{aZ*q?iG$OdP|bK*$ZYe?h^E$PtFi>fw;`uDk%llL-GDcU4&VUC;cuBzV#v3T9`1vdbJ)9=_4%uiz7DfmBKN-%>tm@~X))qK2o7B*r?_*`tWwKR23r6jJm79-AyxmkR1?I_<XKUz0SnuFIjH|8B5;=hzeNDo03X2QsF%l7W}`C<H`*R?Qz~z6cHu3<$SDOsyZLD<F1u);3U8%onV_$+z}j+t`_6^LD>3xCuXFRE1O;FkE0S3y>K^WCp@@YG*npY{E~M|{-Nrd0FJtsDx!K4bqN@^Jsg)RoG7NMP9Z_U*{8$GLMm(#g$iILckCI@Qtae3WTKJ<fTNC=NBe?fpET=mlOue2-akyrWa^TkJ3*^qXjca&%9U>xt+grcBmBjQT0l;J56Wjay#csOqOqg&ylCCmeP=T8N!z%wDpkIyUuZK5~mWz;eFe;OoUT$=rszhGp|HZSPZT?B5iV%71jqRj+C^W%e+Eyz;;iNWh)8z9Ko~3d|Mw#5UUgE$RJs$uBZ7dFct2q?^zmsFf_elKHT%)B(C6$Z`RV-H0n$aMI#BTrDByCdP?6!Py)3nIakQ|BQmX!eCGLt~cNHPFC=$Hi$k%R_ECwRtO<WaK`R5aUn#H|*@_K`(rtTDNC@~vgUmqw4mh9|22RjNG%_vDn^(lf%E1d2rk?%?`4wR4%^H|^s>)G)dyc#S8#V%M`&u`$6NHYfqPQ`sQ%h=e&PRwJ<&E?MivG4vfq#@$!w4l}@+yvNyPuxY~#499k1)e4_#i{_hFr84iQPhrmAIT|^2;o&kfHc@wkE%lc1JkV;!RH?kue5`@SO}m7`g?843bU5-dMG=E}D~rB(oxQG7241MZ|CJ1$GKWkcE&cDGzy|h6tWYIze|X>!!F`^<_1v3121U}a+rvJ49E)EM9J2Q2FaQ0$wtZRV#?g<L>vC@EyNB5e=+Pfa(h-l4M~1OoVyY9HD;ZP~#%61oQ@7gswCgQhyCqndUr7Dg_iE}UUo0=2|CaGRKd38Myan-X{&ZY4%z{kuKxT^q+U%HoY}%yfN+tjsR?Z-l;-;VPG2nt<Q4^3=k--GFQp~|_m|-c^gL=8G^Rv=fBu>}@1o1&t;j<mM&jBGK->;8%55EaMTbc0hBC>t=pa(H}@Os_*Y_d~P;FFZ62@0Ehd}z<H9n!nwhg3i><Jw3|?{Fv^3DQ_vnjx%cR;E8Hv?MHAXIA_5HCQrtJT(XiDZ#aZ1{1!>)S6<zj=_3cxn1?bg|mwgmD1b0#Mt0=W3-DT2jVA)=D0W+%>V;SS}YfFKKagt4K(FcxsKsJCw+Qh;P7^33Ke-<UI2Zg6&uM4a13!Xvm&l)abwb!)Z1TpOCb&0lP_9=2Cm75O8m8OBz$@(@)}Eyi~KzZBYT^1ae*48ERU<QP)p}b&uH=DHzk_i1Z%E{-d#%uh4U+i&D*xLm8;w%#cuOZ+l$v|)fc~|V|6Qi%-y%RH-(s}f0^$m?bk;jEkdf0&(Ui;PuIi^(-^(s#iYLBUtIXkw89#{#=*9IOjtHDur#ER)j_gLCw6l%EI6&1`A>mI=`3I{O;S81ev<mrC$xn5Pdc0W!7DHr$5#C1H_=-~Rti$9bgt27^UF)&B|d5uw;W@ov92uOKv}k{IiNT_ER_7YWz;SvlFYIB+>>!POjbGSeu#U@r5)dUEs4)Cet7mVBgc<hwH`MP&@^WhYBIXe-L0nCsr6`0I?^cLC7VKBlHPlqTVaB6OyPkh@<+8T{i#JopgiQ>4_JflP78cJx!+wj7XaYgFl@(Rgf@RhQDMvHU%e;eGn$pPn4p1bjGfSt9`JgbxOD?BI}@G;iDkMWi&e$0VG+@0#MPb30^nIhi|(~bJ1${t4d~n*5r7Xyz?Vinl<wLT?1%^<<w*nhwY@iCjOMtoo2!%(X2JSZiwo5$XwV<?^H4RMv$tJx+s`!xULxNQ-b2)}n}g{qFgLt2ly4TT`-a!!1ON45&;(UOZ6<|@;dqa^o$$En34m>F0)k}ZD}@*+?^Wyj2S(qS5EW>=WZ<$?8i=20Q04h157*g4dyJWQrKG>z-z-79sfN-Jr0!nQ8Ri0P7U{wNUod!2G5wK{Zd#TH1h(Ith8UTVy1+&iXO}wIFolK^g%p_bk}(3W{Knyr85<6sPJ7+(g<fGue-bCI@Y36TXB+PqZl{upWKlL1i(<g*dtL~XcspttktkqEtQvC1-~_11#923^n<;W>Dd(g&uGwtAD{gPUEyc9ankpj3i7|I<)8#k8SCo%gqu5Z9hkf6gIX^+)h$gtS$^s~R!#}r2jj%WxEMSzDZve}Ww4##?yL)X)!|VvlYO4I2uL?>Sm4_lDa-%GdAs|pVjp<l4D6)h%2m*@x`Vp0Ko$V#*BYf&CiTad6u)n2o^Qru{^}C7J_<BBX%ErVTG%2b^i4wDKE3a|IIdc03D(wmZ7}-$5#$OVVz^;GE*&2aF@%r&x%zgruObu*x^I+3$12PFf7IQhkjgKy$$zXt#pukcBO+m2zlzaO2vl7)r=POJ4ur}7RO8i^m#dhpI5r3vA)OzKLVr-QJXS4)08;H7y#@YR9Rz6iZgb*_@7#`SJuxXGlEKJbOT+5psu0ftyC`cILjWYe7!RRnuVzbwDe9UoY_CW>3kOYQfM`@$=1>}T>Lvy5xi_mVTJX;vWP3EMZ)Lh7snHoEFqDawdfyfkOUt(}hYpx^unRq1*IRcE`%A=ZM>3anWnNX7odifr^DA;e2JlJT!V-&iRetDYWDSL@`D}j1Om;pBPKV+|ery~q{%@xT-C%v{&c87FKVsS%~fPZzp?`?Sil%b~@0@!QPv*puOxK~E9Mi7))##@2B92(J>eqY#q_uEdNcXBB4pK}x0RZIVJ#PU@9&!!(bP$HXhcO1`PaC|!M#FdfRW&H0A<XRTFh2B>E%NXtJsR@eq{SKF3i4jtDArfz8tWKjB+wld)<en-JUEFEcT9s8#c^=igmN?eg4qPP}(V2_8DU~mI`qwmGQuvfeBPy_+M{#Rn$1T7{7nO#5Ofe=DdS@Mc3Xf)-@@LaB4KW~1o#+DV#wV#<WQXBn%p`{~vt5;v_aeZ*c)taG%(gow=1+W~9VWWv))gCj3tqwZan3Y1mRQu4PO}I93`V1X;8>FqT<AMd{GriulIW)Gl|qFJhMGsD$NABqN3Jq_+U&Qn8hR+s;n*|FkZ>;M*Pm&Jra%F-K=3d=Kgaw0YFjG=Jjr(_A^c|f_Iqlfc#kzM9crit$@Ie{DX{Cwleh5P{>^K@sH!jZInb!$lajj`e7Jn;tHD<c`p1I-i);eS^t0tG*O=68*!C{(o4Hz=Kl+_!&O46U1xqAr7J$ecWg0|1W+KA-EepK4XN+|?#<2Ve{XnToAS0b@Iud(Ban57RRtc#ct8^HO%Kuoj{q}xs8qbAqK;d)X?bn26Dr97yrA7)d<Zzz>aP2o~Wh?hi>$M&UL%T$O89)CQBbp>^42!Y~ERC0Mc!Sl~R!7^7@pFR?t%WQ!w)Ft2^Qz{pzSAaF1Vch1*ZRWlW(8E8)&VC!vI5Wm@M80q?@M1m;q(Z!{z``nA7i&=Fl2369Se*8Zr5I}W2J8%gvOH8b7#&NGH4bSYR&}aU@H`gNVO3Ohs!4z10`Ud6D!h!Kkuj@_pu%i6o2zW?tMj~rFZof)M>4QQFQJ(PofE=#axR|4%^3yV=(eQMtA{#Iq0|$ao5HON?A+Z09S}oXf*E7y7Af<5qBC2tR-nTyc;jl*jsq1OEc+!71Akf3~x}@vKb=6eEFO2Cib(?RJwK7siWRv?{<7V51=@c>if0GyE5_y`_kIk`Ff~SI0(!4=3=P&bA6IK7Fk%C+>n^sCDF3h8&ExksX6i)>$ImPOKjv^)}Cj@fQI-71YD`AC*TD4fQi@*5PK&=Fn9%Zef9U(<pK+6E8utr&H+wMsPs~gzPfZrXBJ};@_@;Dbs$AU49^jFFKn}4I8|)U)fe`kj279#tmZN{sFO_gjB<WcCh*KaXo+P9qtzBeYZ*A5Db^|lq)5Q!#);bqlxF;`UxkNP{qL&xyIr_Y2PLb%szHWgV)TdtP4%`KkR9qVQcm!pp<mmvi<Y2&%QnUUKZmW4ReIL`GxFdu>8?n7FG(`Fe=RYLE&Cii>AYRg^<<(jA-By#1+zLB0Vx>8b6iIbt&5FZj~dN%M&%7EXAjG2W#AcMJK@c(`f@?(#H(#1imk@Bhn;oB(TA;-c~s~(C%!u6ZX2@*Xu7=vf9<WcxY+^5+X<CVe5GTkK4|52OMBWMc`8oHNL=erlP1RSL%u~B2hi<*OJhF=AwS`u-8aaq{K!j8y&aJEHWoQzl7lgT*8Y_eVoRkT4?KSj*&@rTlFqO5GLvOnN+k_zX*8h0@DDIOAjrVav;C`zVeW~L<{WjW6y|LwZK(yfBC)+mlk1>x9?=n8CXF1R@3THBtEn9^1)LO_828GYC3V#3#`_FrCuU%_J>swIjoBMKf5AZFAmTNtkDB{02;_>F<lZf7929Z>Ni`9<*d$%(vW>szn3$Qy^D~9KuxbqEj}Y?7tp+5A4cmb>eCYH;&|W7k*+?$4*m%IGGuCHH-|}ZDjh7#d-oY}5i&0~O$$#^iBapQMMBrtbdHLpA<g&&_nqA}dCCDa*r2&E1No`ZyiO-MLO6ZYQMvPykC;fB&9r)>U)pleL!YCVwY*!O`kYe-@ZEP`J5MBy|L4kB7rqc!`FY79(g8dQse8MwZ!%%tHEx1VmMWli(xi+zhQ^*{sH3<P*dgt7?=SaVE&F%??f~Oyq8<+i4b#vSD!iYE@b5Lbe3vWW5k@SqL=I~#s5obnz-p92euq>5NFv(g;RmjY3OjN!L?^v7l6{VrXZFJbPrRW2^lcWL%q}YQKk9AHgYVxJ`Ys<=I0J3#PNLy~D!M3R1PubwL{ycKL5&!@I00H>@1MZ0rlD7vzr~nH50ssI2003E9","encoding":"xz-base85-v1","uncompressed_bytes":247022,"uncompressed_sha256":"e39d6ff58771f977f17b6efadc6760a9e7eefb2c947dd02e62a9f59ec8179731"}
```
<!-- ENDHISTORICAL -->

## Appendix W. The P8 signed-search cell under the record-and-regenerate schedule (P8RR)

**Claim, conditional on the premises of section 5.** Under the record-and-regenerate schedule below, the P8 computation has an analytical peak of at most **211,431,424 bytes**, 4,861,920 bytes above the base's thirteen-column online bound 206,569,504 (the active ten-column image is 159,383,584), so in Appendix W this preprocessing cell is the binding preprocessing maximum. Appendix Z then charges the record once rather than twice (Lemmas RF, RF1), dropping phase E to 160,546,816 and phase R to 157,474,816, with the ten-column online image 159,383,584 lying below phase E; the counted phase maximum is the preprocessing cell and the charge is 160,546,816 (memory_log2_bytes 27.258419, projected scalar 83.743859). The predecessor's signed-16 record width is withdrawn as false and no current claim depends on any record width (Lemma RF1). The premises are the inherited H6-D and R.6D determinism and the new H6-E (a0), (a), (b) and (d). H6-E(a0) reads the H6-D encoder figure only as a bound on the encoder's live clause objects, which on the experiment platform occupy at most 128,586,032 bytes allocator-rounded, 27,950,800 below it (section 6). The whole local encoder process exceeds the figure, so H6-D itself is not reproduced locally; under Appendix Z the required phase-E bound rises one byte per byte that figure is understated. Because phase E already sets the submitted maximum, every positive understatement exceeds the submitted bound; the local clause-object margin supports the premise but is not certified slack. Appendix R.6D is unchanged; only its phase maximum is superseded. No historical run is reproduced.

### 1. What the cell computes and what is consumed

The published `stepk.py` builds the clause list of `F_hist` (model clauses, cardinality encodings, `fix_xor` pins, `fix` rows, one clause per nonempty block), serializes it as `p cnf V C` plus one line per clause, runs Kissat, writes `name`, `spec`, `sat`, `solve_s`, `build_s` and `rows`, and prints one line. `score.py` reads `name`, `spec` and `rows`; `sweep.py` reads `sat`, `rows` and the printed line. The rows depend only on the result line and on model values of word variables, all numbered at most T, the pool top when `sha256_model` returns (32,680 for the sweep topology).

### 2. The schedule

`p8rr_launch` runs in a working directory private to the run. It removes stale files of an interrupted run and then runs:

- **E (record).** The historical encoder process runs the published `stepk.py` text byte for byte up to `t1 = time.time()`. Instead of a CNF file it writes a record: the greedy covers actually used, the model arguments, the clauses appended after `sha256_model` (cardinality, pins, rows, blocks), V, C, and the length and SHA-256 of the exact serializer output. It writes no DIMACS.
- **R (regenerate into the solver).** `regen.py` runs the pinned `sdmodel.py` against stub PySAT modules: a write-only clause sink, a sequential identifier pool and the recorded covers. Pass 1 regenerates the whole stream into SHA-256 only and compares it with phase E; pass 2 writes the identical stream to Kissat's standard input. `p8rr_tool filter T` keeps Kissat's result line and the positive model values at most T.
- **S (solver alone).** The launcher deletes the record as soon as `regen.py` exits 0; Kissat continues.
- **D (decode).** `decode.py` rebuilds the identifier map with empty covers and writes stepk.py's output with stepk.py's keys in stepk.py's order, and prints stepk.py's line.

The launcher accepts the run only if every phase exits as declared (solver 10 or 20). The same Kissat 4.0.1 binary receives the same formula bytes with the same options `-q --seed=101`, so under R.6D determinism it returns P8.

### 3. Equivalence for every accepted input

For every `stepk.py` spec with `"solver": "kissat"` that the procedure accepts, every greedy cover draw and every PySAT build: whenever phase R exits 0, the solver has received exactly the bytes the published serializer would have written, because phase E records the true clause list's digest, `sdmodel.py` never reads its CNF and allocates identifiers in a fixed call order, and pass 1 refuses any difference before Kissat receives a byte. The filter and decoder reproduce `sat` and `rows` exactly and refuse non-canonical solver output. The output equals stepk.py's apart from the two wall-clock fields; the only other differences are the pipe instead of a file and the full model not being stored. An accepted spec has formula literals that are nonzero integers below 2^31 in absolute value, and every `sha256_model` argument a bool, an int, a tuple or a set of mutually orderable values. Some specs that `stepk.py` runs are refused in phase E before any solver starts, for example `"with_state": "yes"` or `null`, or a `relax_steps` list that mixes integers and strings. The sweep specs are accepted. This is a universal transformation checked on fresh fixed-seed controls, not a historical reproduction.

### 4. Memory, every term charged

| Phase | Components (bytes) | Total |
| --- | --- | ---: |
| E | encoder G 156,536,832 + kernel 2,097,152 + launcher 4,194,304 + procedure code files 1,912,832 + record file 44,593,152 + recorder overhead 2,097,152 | **211,431,424** (Appendix Z Lemma RF: the record is charged once, so phase E is 160,546,816) |
| R | filter 1,048,576 + kernel 4,194,304 + key file 16,384 + launcher 4,194,304 + model file 200,704 + pipes 2,097,152 + procedure code files 1,912,832 + record file 44,593,152 + regenerator 33,554,432 + solver S 90,210,304 + solver pipe input 1,048,576 | 183,070,720 (Appendix Z Lemma RF: the record is charged once, so phase R is 157,474,816) |
| S | filter 1,048,576 + kernel 3,145,728 + key file 16,384 + launcher 4,194,304 + model file 200,704 + pipes 2,097,152 + procedure code files 1,912,832 + solver S 90,210,304 + solver pipe input 1,048,576 | 103,874,560 |
| D | decoder 100,663,296 + kernel 2,097,152 + key file 16,384 + launcher 4,194,304 + model file 200,704 + output json 5,242,880 + procedure code files 1,912,832 | 115,376,128 |

The launcher, its spec argument, the code files, retained files rounded to 4 KiB pages plus one page, two pipes of 1 MiB each (the capacity with 64 KiB pages) in phases R and S, and 1 MiB of kernel state per process are charged in every phase in which they exist. No release, cache or dead-buffer credit is taken.

**Record bound, from H6-E(a0) and (a).** At the end of construction every clause of `F_hist` is a distinct CPython list of at least 56 + 8k bytes, and every literal that `sdmodel.apply` computes as `lit * (+-1)` outside CPython's small-int cache is a distinct int object of at least 26 bytes. Exact rational LP-dual certificates, checked by two programs, bound the model part below by 85,323,392 bytes for every cover draw: per instance whose literals avoid the cache, XOR 3,072, IF 5,288, MAJ 6,780 and ADD 12,308 bytes (2,528, 608, 608 and 5,632 instances); the 96 XOR and 128 ADD instances that touch W0..W3 are charged list bytes only (1,408 and 5,080); 1,812 unit clauses at 64 bytes. A recorded tail clause of k literals costs at most 1 + 5k bytes, at most 5/8 of its list, and by H6-E(a0) the tail's lists fit in G less the model part. Hence the record is at most 44,585,056 bytes for any PySAT build and any block count. **The record bound needs no premise about Kissat. The cell does:** phases R and S charge H6-D's Kissat figure and the H6-E(b) pipe allowances, and they are 28,360,704 and 107,556,864 bytes below phase E. With H6-E(c), four-byte literals would give a cell of 202,526,720 bytes, withdrawn with Lemma RE2. Without the int-object clause of (a) the cell would be 242,135,040 bytes with five-byte literals or 227,090,432 with four-byte literals, both above the claimed maximum, so that clause carries the claim. Appendix Z, below, releases the list incrementally and charges the record once through the actual coexistence maximum; its narrower Lemma-RF width replaces Appendix W's wider record row.

### 5. Premises

- **H6-D (inherited, unchanged).** "Premise H6-D: the author's reported per-process maxima for its same-specification-and-seed re-run, interpreting KB as KiB, bound the corresponding phases of the historical P8-producing execution: Python encoder/driver at most 152,868 KiB and Kissat at most 88,096 KiB." Appendix W charges both figures unchanged as phase components, as R.6D does.
- **R.6D determinism (inherited).** Kissat 4.0.1 run with the same binary, platform, input bytes, options and seed performs the same search and prints the same result and model (Appendix R.6D, section 3). That the schedule returns P8 rests on it.
- **H6-E (new).**
  - (a0) The 152,868 KiB encoder figure bounds the live clause objects of the historical encoder process at the end of construction: the list object and item array of every clause of `F_hist`, and the int objects outside -5..256 that its `sha256_model` clauses hold, with those objects resident and none swapped out or compressed. These are the only objects that the record bound (section 4) and the token bound (section 9) read; phase E charges the encoder at H6-D's figure itself. R.6D does not use this reading: it charges the figure as the encoder's phase while the encoder overlaps Kissat, never as a bound on live objects.
  - (a) The historical encoder ran on a default 64-bit CPython 3: a list of k items occupies at least 56 + 8k bytes, an int object at least 26 bytes, only -5..256 are cached, and PySAT's `CNF` keeps each clause as that list or a copy holding the same int objects.
  - (b) The measured allowances transfer to the historical platform: recorder overhead 2 MiB, regenerator 32 MiB, decoder 96 MiB, filter 1 MiB, launcher 4 MiB, 1 MiB of kernel state per process, 1 MiB for Kissat reading a pipe and 1 MiB per pipe. The regenerator, filter, decoder and launcher run beside the historical Kissat binary. Retained files are rounded to 4 KiB pages; with 64 KiB pages phase E is 212,373,504 (2^27.662029); the claimed 211,431,424 uses the 4 KiB pages stated here.
  - (d) The spec was shorter than 2 MiB. This is assumed, not derived: it follows from the spec's passage through one execve argument only on Linux with pages of at most 64 KiB (32 pages per argument; 128 KiB with 4 KiB pages) or on macOS (1 MiB for all arguments together). It bounds the launcher's argv copy, which is charged in every phase including E, the decoder's copies and the 6 MiB output charge.
  - (c), used only for the withdrawn 202,526,720-byte figure: Kissat 4.0.1 keeps at least one resident byte per declared variable.

### 6. Local evidence on the H6-D encoder figure

On the experiment platform (CPython 3.12.3, PySAT 1.9.dev17) the published construction of seven sweep-shaped fresh controls (0 to 5,430 blocks, four cover draws) was read at `t1`.

**The live clause objects, which (a0) bounds.** `src/clause_objects.py` rebuilds each control in a fresh interpreter, binds the construction to the committed control by its serializer digest, clause and literal counts and covers, and sums the objects that (a0) names. Its receipt `results/clause-objects.json` (SHA-256 `9cfaaa6ea889d583de87de882bd9e8b4693fa00b57932f799b8fd1830e34dce7`) gives 112,089,896 bytes by object size and 124,873,616 allocator-rounded with no blocks (C0), 113,523,416 and 126,350,576 with 5,430 blocks (CB5430), and at most 115,410,388 and 128,586,032 under a forced alternative cover draw of the zero-block spec (D_draw3). Allocator-rounded, the largest is 27,950,800 bytes below G = 156,536,832. The tail's own int objects, which no bound reads, would add at most 4,714,880 bytes.

**The whole process.** The recorder process, which runs the published `stepk.py` text, held 158,711,808 bytes of anonymous memory and 168,951,808 resident at `t1` with no blocks (C0), and 166,572,032 and 176,832,512 with 5,430 blocks (CB5430). Every whole-process value exceeds G, so H6-D's figure is not reproduced locally. Under Appendix Z the record is charged once through the coexistence maximum of Lemma RF1, so active phase E is G plus the fixed 4,009,984 bytes of procedure code and recorder overhead and the required bound rises by exactly one byte per byte that G is understated; the superseded 1.25-, 1.625- and 1.5-byte slopes belonged to charged record widths. Substituting a whole-process figure for G is a conservative stress test: it charges the encoder at that figure and lets the clause objects fill all of it, although they occupy at most 128,586,032 bytes. At those figures phase E would be 172,961,792 (C0) and 180,842,496 (CB5430), both above the measured charge 160,546,816, so the claim rests on G as the live-clause figure, which is H6-D's own reading.

### 7. Premise sensitivity

| Premises | Peak | Margin to the claimed maximum 211,431,424 |
| --- | ---: | --- |
| H6-D, R.6D determinism, H6-E (a0), (a), (b), (d) | 211,431,424 | 0 in Appendix W; Appendix Z Lemma RF gives phase E 160,546,816 as the counted maximum, with the ten-column online image 159,383,584 and phase R 157,474,816 below it |
| the same plus (c) | 202,526,720 | +8,904,704 (Appendix W's four-byte width); withdrawn with Lemma RE2 by Appendix Z, whose Lemma RF charges the record once at 18,997,248 bytes |
| (a) without its int-object clause, plus (c) | 227,090,432 | −15,659,008, fails |
| (a) without its int-object clause, no (c) | 242,135,040 | −30,703,616, fails |
| no (a), or no (a0) (H6-D read only as R.6D reads it) | no record bound | this arm establishes only R.6D's 246,812,672 |
| no (b) | phase E's own allowances total 8 MiB | has no headroom in E; could grow by 28,360,704 in R and 96,055,296 in D, but nothing is proved |
| no (d) | launcher and phase D unbounded | with measured costs D reaches the claimed maximum at a spec below the base's 7.9 MiB point (headroom 96,055,296 instead of 121,602,048) |
| G understated by x bytes | about 211,431,424 + 1.25x in Appendix W; active Appendix Z phase E is G + 4,009,984 + x | exceeds the submitted 160,546,816-byte bound for every x > 0; no certified understatement slack |
| G replaced by local whole-process anonymous / resident memory at `t1`, a conservative stress test (section 6) | C0 −3,530,752 / −20,172,800, fails; CB337 −7,933,952 / −24,854,528, fails; CB5430 −16,306,176 / −32,980,992, fails; D_draw3 −11,468,800 / −27,942,912, fails | |
| Kissat above H6-D's figure by y bytes | R binds above y = 28,360,704 | exceeds the claim above y = 28,360,704 |

### 8. Evidence

Ten fresh fixed-seed controls ran with a local source build of Kissat 4.0.1 (official rel-4.0.1 tarball): 0 to 5,430 blocks, three forced cover draws, a feature control with `=`/`>=` cardinality, value rows, relaxed and exact steps, and small specs. Three are satisfiable with rows decoded (S_msg20, S_msg24, S_nopin), two unsatisfiable (S_unsat, X_features) and six stop undecided under their conflict budget with `s UNKNOWN` (C0, CB337, CB5430, D_draw1, D_draw2, D_draw3); only the three satisfiable controls exercise row decoding. In every control the solver read exactly the published serializer's bytes (an independent tap on its input), its standard output was byte-identical between file and pipe, and the decoded output equalled the published `stepk.py` output: the same keys in the same order and the same values, with the two wall-clock values set to 0.0. On C0 with the procedure's options and a 2,000,000-conflict budget, the quiet stdout was byte-identical between file and pipe and the verbose transcript agreed line for line (10,497,919 decisions, 261,821,810 propagations). In 24 file-against-pipe configurations (Kissat 4.0.1, Kissat sc2021, CaDiCaL 1.7.3, quiet and verbose) every result, model line, progress line and statistics counter agreed. On C0 with `--seed=101 --conflicts=100000` the build reports 622,491 decisions, 26,949,414 propagations and 4,532 restarts for both inputs, the counts R.6D records. Five local PySAT builds (1.9.dev17, 1.9.dev16, 1.9.dev7, 1.8.dev16, 1.9.dev2) give one cardinality output. Every truncation and single-byte corruption of a record is refused by two independent implementations; crash points, failure paths, ASan/UBSan and mutants are refused. The historical binary and platform remain unavailable.

### 9. Operations

The added recording, regeneration, filtering, decoding and launching are bounded by 2^54 word operations (2^42.59 target compressions): the measured CPU per formula token of every added process, times the largest token count H6-E(a0) allows (every token costs at least 8 bytes of clause list inside G), times 2, times 9.216*10^12 operations per CPU-second. Added to N it leaves time_log2 76.48544 and preprocessing 61.58497 unchanged at upward rounding; it also lies inside A_C = 2^60.

## Appendix X13. Current eight-column charged implementation, ledger and replay binding

The base's strict replay packet is not embedded in this filing; Appendix U records its SHA-256 commitment, and it is historical fourteen-column
evidence and is not current implementation evidence. The current charged implementation
is the exact eight-column source below: 59800 bytes, SHA-256
`8f3fb2bdb7bc074cd562f0d36cbd2ae0a723a0ada512ec1cb8a0ea36157c7fba`. It fixes `NCOL=8`, `STR=39`, `RECORD_BYTES=30`, coverage 64,
probe threshold 69 and the subtractive combined word
`(GW - ((d + WBL) & MT3W)) & GW` with set guard bits denoting fired lanes.

The lane and word-test evidence below is the parent's ten-column selftest run: 2,304 tag lane checks with zero mismatches, 16,128 combined tag/C1 lane checks with 568 firing and zero mismatches, and bitslice maximum/bound 218; the word test, the lane tree and the read path are column-count invariant (the mask comparator is set to the active limit 77), so those checks bound the eight-column program unchanged. The eight-column ledger is the exact arithmetic of Appendix A and Appendix ZS; it is not claimed as a fresh selftest run of this filing. The standalone tag-only selftest remains outside the procedure. These finite checks bind deterministic semantics and accounting only; they do not measure H8, H9 or any deep-event probability. The two inherited organizer experiments have the bounded scopes declared in experiments/manifest.json and Appendix Y.
reported 2,304 tag lane checks with zero mismatches,
16,128 combined tag/C1 lane checks with 568 firing and zero mismatches, bitslice
maximum/bound 218, exact ledger time_log2 76.4854303, and `SELFTEST PASS`.
The production `scan_cv` contains only the charged combined read path: it has no `z0`, six-lane diagnostic loop, optional collection hook, `collect_all`, or `claws_all`. The standalone tag-only selftest remains outside the procedure. These finite checks bind deterministic semantics and accounting only; they do not measure H8, H9 or any deep-event probability. The two inherited organizer experiments have the bounded scopes declared in `experiments/manifest.json` and Appendix Y.

<!-- BEGIN DB38_H8G_8COL_SOURCE 8f3fb2bdb7bc074cd562f0d36cbd2ae0a723a0ada512ec1cb8a0ea36157c7fba -->
```python
if not __debug__:
  raise SystemExit('assertions required')
import sys,json,hashlib,struct,math,random,zlib,base64
from decimal import Decimal as D,getcontext
M=0xffffffff;NR=38
K=[0x428a2f98,0x71374491,0xb5c0fbcf,0xe9b5dba5,0x3956c25b,0x59f111f1,0x923f82a4,0xab1c5ed5,0xd807aa98,0x12835b01,0x243185be,
     0x550c7dc3,0x72be5d74,0x80deb1fe,0x9bdc06a7,0xc19bf174,0xe49b69c1,0xefbe4786,0x0fc19dc6,0x240ca1cc,0x2de92c6f,0x4a7484aa,
     0x5cb0a9dc,0x76f988da,0x983e5152,0xa831c66d,0xb00327c8,0xbf597fc7,0xc6e00bf3,0xd5a79147,0x06ca6351,0x14292967,0x27b70a85,
     0x2e1b2138,0x4d2c6dfc,0x53380d13,0x650a7354,0x766a0abb]
IV=[0x6a09e667,0xbb67ae85,0x3c6ef372,0xa54ff53a,0x510e527f,0x9b05688c,0x1f83d9ab,0x5be0cd19]
def ror(x,n): return ((x>>n)|(x<<(32-n)))&M
def S0(x): return ror(x,2)^ror(x,13)^ror(x,22)
def S1(x): return ror(x,6)^ror(x,11)^ror(x,25)
def s0(x): return ror(x,7)^ror(x,18)^(x>>3)
def s1(x): return ror(x,17)^ror(x,19)^(x>>10)
def CH(x,y,z): return (x&y)^(~x&z&M)
def MAJ(x,y,z): return (x&y)^(x&z)^(y&z)
def trace(cv,w16,n=NR):
  W=list(w16)
  for i in range(16,n): W.append((s1(W[i-2])+W[i-7]+s0(W[i-15])+W[i-16])&M)
  A={-1-i:cv[i] for i in range(4)}; E={-1-i:cv[4+i] for i in range(4)}
  for i in range(n):
    E[i]=(A[i-4]+E[i-4]+S1(E[i-1])+CH(E[i-1],E[i-2],E[i-3])+K[i]+W[i])&M
    A[i]=(E[i]-A[i-4]+S0(A[i-1])+MAJ(A[i-1],A[i-2],A[i-3]))&M
  return A,E,W
def compress(cv,w16,n=NR):
  A,E,W=trace(cv,w16,n); f=[A[n-1],A[n-2],A[n-3],A[n-4],E[n-1],E[n-2],E[n-3],E[n-4]]
  return [(cv[i]+f[i])&M for i in range(8)]
PCV = [0x95a24959,0xb4053f95,0x1bf0473e,0x1eab3b7c,0x650c63d3,0xe6493d3b,0xed004f1d,0xeb7eaad3]
PMX = [0xbd047e95,0x1dc94891,0x4bbe458b,0xc7dc3c0a,0x8b6235e1,0x9d7630ee,0x569da3a0,0x94ddb1c2,0x464e545d,0xa804c932,0xacecbe75,
       0xc8280172,0x9a4d6768,0x16139532,0xe00d6a99,0x5fb2827b]
PMY = [0xbd047e95,0x1dc94891,0x4bbe458b,0xc7dc3c0a,0x8b6235e1,0x9d7630ee,0x569da3a0,0xb4ddb1c2,0x420e5c5d,0x8804c932,0xa9edacdf,
       0xc8200d72,0x9a4d6768,0x16139532,0xe00d6a99,0x5bf28a7b]
_ROWS = ("=nu============================= uuu============================= ==n=============================|"
 "=========n=====n====n======n==== ==n=u====n==nu=====nu===u==n==== =====u===u==========n===========|"
 "================================ ======nn===n================n=nn ==u=============================|"
 "===============n===========u==== =u=============n===========u==== =====u=n=======n===u==u=n=u=n=n=|"
 "====n===============n========u== ==n==n==u=====un================ ============u=======nn==========|"
 "==u====u==u==========uu=======u= =nu=u==n==n=====u=n=nn=========u ================================|"
 "==n============================= =========n============n=nuu==uu= ================================|"
 "====n=========n=========n==n==== ====u=========n================= ================================|"
 "======n=u======un=============== ====================n===u======= =====u===n==========n===========|"
 "================================ =u==1====n===+u====u0=u=0==+==== ==u=============================|"
 "==u============================= =0=====++0===+0=+==01=0=0==+==== ================================|"
 "================================ =0=====++1===n1=+==1==1====n==== ================================|"
 "================================ ==+====nn=======u=============== ================================|"
 "================================ ==+====00====1==0==========1==== ================================|"
 "================================ ==u====10=======1=============== ================================|"
 "================================ ==0============================= ================================").split('|')
CELLS=[[(0,0,0)]*NR for _ in range(3)]; PQ=[0]*NR; _PL={}
for _r,_l in enumerate(_ROWS):
  for _k,_s in enumerate(_l.split()):
    m=v=x=p=0
    for _j,_c in enumerate(_s):
      b=1<<(31-_j); m|=b*(_c in 'un01'); v|=b*(_c in 'u1'); x|=b*(_c in 'un'); p|=b*(_c=='+')
    CELLS[_k][_r+7]=(m,v,x); _PL[_r+7]=_PL.get(_r+7,0)|p
for _i in _PL: PQ[_i]=_PL[_i]&_PL.get(_i-1,0)
PQE=list(PQ); PQE[18]=0
X2=[]
for _t in ('E16 7 = E16 26,E16 14 ! E16 28,A15 4 = A16 4,E16 11 = E16 16,A15 7 = A16 7,A14 15 = A16 15,A14 16 = A16 16,A15 17 = A16 17,'
           'A14 23 = A16 23,A14 25 = A16 25,A15 27 = A16 27,E16 3 ! E16 8,E16 4 = E16 23,W16 20 ! W16 27,W16 22 = W16 31,W16 4 ! W16 6,'
           'A15 29 = A16 29,W16 14 = W16 18,W16 8 = W16 25,W16 1 ! W16 12,A17 9 ! A17 20,A16 15 = A17 15,A17 6 = A17 18,A16 16 ! A17 16,'
           'A16 23 = A17 23,A16 25 = A17 25,A17 8 ! A17 17,E18 0 = E18 13,E18 17 = E18 22,E18 5 ! E18 23,A16 29 = A18 29,E18 9 = E18 23,'
           'E21 10 = E21 15,E21 11 = E21 24,E21 2 = E21 16').split(','):
    _a,_b,_e,_c,_d=_t.split()
    X2.append(('AEW'.index(_a[0]),int(_a[1:]),int(_b),int(_e=='='),'AEW'.index(_c[0]),int(_c[1:]),int(_d),max(int(_a[1:]),int(_c[1:]))))
def cellok(k,i,x,y):
  m,v,df=CELLS[k][i]; return (x&m)==v and (x^y)==df
def exact(tx,ty): return all(tx[k][i]==ty[k][i] for k in (0,1) for i in range(34,38))
def rowok(tx,ty,i):
  if i<0: return True
  (Ax,Ex,Wx),(Ay,Ey,Wy)=tx,ty
  if not (cellok(0,i,Ax[i],Ay[i]) and cellok(1,i,Ex[i],Ey[i])): return False
  if i not in (7,8) and not cellok(2,i,Wx[i],Wy[i]): return False
  if (Ex[i]^Ex[i-1])&PQE[i]: return False
  for (k1,i1,b1,eq,k2,i2,b2,row) in X2:
    if row==i and (((tx[k1][i1]>>b1)^(tx[k2][i2]>>b2))&1)!=(0 if eq else 1): return False
  return True
_tx=trace(PCV,PMX); _ty=trace(PCV,PMY)
SAx=[_tx[0][i] for i in range(16)]; SAy=[_ty[0][i] for i in range(16)]
SE={i:_tx[1][i] for i in range(4,16)}
_A,_E=_tx[0],_tx[1]
C16=(_A[12]+_E[12]+S1(_E[15])+CH(_E[15],_E[14],_E[13])+K[16]+s1(PMX[14])+PMX[9])&M
R16H=[int(t,16) for t in ('4b02d320 7b1ab320 7b22b320 7b3ab320 c802f320 c80ad320 c80af320 c812d320 c822f320 c82ad320 c82af320 c832d320 '
                          'cb12f320 cb1ad320 cb1af320 cb22d320 cb32f320 cb3ad320 cb3af320 fb02b320').split()]
R16F=0x405
def r16ok(e): return (e&~R16F&M) in R16H
T20=[(h-R16H[0])>>13 for h in R16H]
assert all((R16H[0]+(t<<13))&M==h for h,t in zip(R16H,T20)) and len(set(T20))==20
OFFS=(0,1,4,5,1024,1025,1028,1029)
T160=sorted(h+o for h in R16H for o in OFFS)
Cc2=0x7af32e15
QPF=(57726359870197/2**58)*(287309824/2**32)
ONES=(1<<256)-1
LANEPL=[sum(((l>>i)&1)<<l for l in range(256)) for i in range(8)]
AP=[(LANEPL[i],LANEPL[i]^ONES) for i in range(8)]
B2=(0,ONES)
SP_S0=[(((x>>0)&1)<<0)|(((x>>1)&1)<<4)|(((x>>2)&1)<<8)|(((x>>3)&1)<<11)|(((x>>4)&1)<<14)|(((x>>5)&1)<<17)|(((x>>10)&1)<<34)|(((x>>11)&1)<<39) for x in range(4096)]
SP_S10=[(((x>>0)&1)<<1)|(((x>>1)&1)<<5)|(((x>>7)&1)<<22)|(((x>>8)&1)<<26)|(((x>>9)&1)<<30)|(((x>>10)&1)<<35)|(((x>>11)&1)<<40) for x in range(4096)]
SP_S11=[x<<1 for x in SP_S10]
SP_K0=[(((x>>0)&1)<<3)|(((x>>1)&1)<<7)|(((x>>2)&1)<<9)|(((x>>3)&1)<<12)|(((x>>4)&1)<<15)|(((x>>5)&1)<<18)|(((x>>6)&1)<<20)|(((x>>7)&1)<<24)|(((x>>8)&1)<<28)|(((x>>9)&1)<<32)|(((x>>10)&1)<<37)|(((x>>11)&1)<<42)|(((x>>12)&1)<<44) for x in range(8192)]
SP_K1=[(((x>>2)&1)<<10)|(((x>>3)&1)<<13)|(((x>>4)&1)<<16)|(((x>>5)&1)<<19)|(((x>>6)&1)<<21)|(((x>>7)&1)<<25)|(((x>>8)&1)<<29)|(((x>>9)&1)<<33)|(((x>>10)&1)<<38)|(((x>>11)&1)<<43)|(((x>>12)&1)<<45) for x in range(8192)]
def cv_consts(cv):
  a,b,c,d,e,f,gg,h=cv
  k0=(-S0(a)-MAJ(a,b,c)-h-S1(e)-CH(e,f,gg)-K[0])&M
  E0base=(d-S0(a)-MAJ(a,b,c))&M
  PP=a&b; QQ=a|b; NAB=(~(a^b))&M; EF=e^f; FF=f; KF=(k0+Cc2-gg-K[1])&M; KFm=(KF-PP)&M; K2=(Cc2+k0)&M
  E=[]; c8=0
  for i in range(8):
    ai=LANEPL[i]; ei=(E0base>>i)&1
    if i==0: E.append((ai^ONES) if ei else ai); c8=ai if ei else 0
    elif ei: E.append(ai^c8^ONES); c8=ai|c8
    else: E.append(ai^c8); c8=ai&c8
  nc8=c8^ONES; G=(0,nc8,c8,ONES)
  EG=[(E[i],E[i]^nc8,E[i]^c8,E[i]^ONES) for i in range(8)]
  nab=(~(a^b))&255; U=[]; cu=0
  for i in range(8):
    xi=(LANEPL[i]^ONES) if (nab>>i)&1 else 0
    ei,fi=(e>>i)&1,(f>>i)&1
    yi=(ONES if ei else 0) if ei==fi else (E[i] if ei else (E[i]^ONES))
    t=xi^yi; U.append(t^cu); cu=(xi&yi)|(cu&t)
  U.append(cu)
  K_cv=(KF+(~QQ&255)-(PP&0x1F00)-5)&8191
  def _csa3(p,q,r): u=p^q; return ((p&q)|(u&r),u^r)
  T0=[]; T1=[]
  for idx in range(16):
    p,q,r,s=U[0],AP[2][idx&1],EG[6][(idx>>1)&3],B2[(idx>>3)&1]
    c1,s1=_csa3(p,q,r); cs=c1&s1; T0.append((s1^s,c1^(s1&s),cs&s))
    p,q,r,s=U[1],AP[3][idx&1],EG[7][(idx>>1)&3],B2[(idx>>3)&1]
    c1,s1=_csa3(p,q,r); T1.append((c1,s1,s1^ONES) if s else (c1,0,s1))
  CT=[T0,T1]
  for i in range(2,6): CT.append([_csa3(U[i],AP[i+2][idx&1],G[(idx>>1)&3]) for idx in range(8)])
  CT.append([(U[6]&G[idx],U[6]^G[idx]) for idx in range(4)])
  for i in (7,8): CT.append([_csa3(U[i],EG[i-7][idx&3],G[(idx>>2)&3]) for idx in range(16)])
  CT.append([(EG[2][idx&3]&G[(idx>>2)&3],EG[2][idx&3]^G[(idx>>2)&3]) for idx in range(16)])
  for i in (10,11): CT.append([_csa3(AP[i-10][idx&1],EG[i-7][(idx>>1)&3],G[(idx>>3)&3]) for idx in range(32)])
  CT.append([(LANEPL[2]^EG[5][idx],) for idx in range(4)])
  return dict(k0=k0,E0base=E0base,PP=PP,QQ=QQ,NAB=NAB,EF=EF,FF=FF,KF=KF,KFm=KFm,K2=K2,
        E0base_hi=E0base&~255,NAB_hi=(~(a^b))&0x1F00,FF_hi=f&0x1F00,EF_hi=EF&0x1F00,K_cv=K_cv,G=G,EG=EG,U=U,CT=CT)
def hfun(cv,a0):
  a,b,c,d,e,f,gg,h=cv; E0=(a0+d-S0(a)-MAJ(a,b,c))&M
  return (-S0(a0)-MAJ(a0,a,b)-gg-S1(E0)-CH(E0,e,f)-K[1])&M
def Ffun(cv,a0,co): return (a0+co['k0']+hfun(cv,a0)+Cc2)&M
def spair_claw_consts():
  cvS=[_tx[0][3],_tx[0][2],_tx[0][1],_tx[0][0],_tx[1][3],_tx[1][2],_tx[1][1],_tx[1][0]]
  def Wof(A,E):
    return [(E[i+4]-A[i]-E[i]-S1(E[i+3])-CH(E[i+3],E[i+2],E[i+1])-K[i])&M for i in range(16)]
  Ax={i:_tx[0][i] for i in range(-4,16)}; Ex={i:_tx[1][i] for i in range(-4,16)}
  Ay={i:_ty[0][i] for i in range(-4,16)}; Ey={i:_ty[1][i] for i in range(-4,16)}
  Wx=[(Ex[i]-Ax[i-4]-Ex[i-4]-S1(Ex[i-1])-CH(Ex[i-1],Ex[i-2],Ex[i-3])-K[i])&M for i in range(16)]
  Wy=[(Ey[i]-Ay[i-4]-Ey[i-4]-S1(Ey[i-1])-CH(Ey[i-1],Ey[i-2],Ey[i-3])-K[i])&M for i in range(16)]
  return dict(D7=(Wy[7]-Wx[7])&M, D8=(Wy[8]-Wx[8])&M, D9=(Wy[9]-Wx[9])&M,
        T8=(s0(Wy[8])-s0(Wx[8]))&M, F7d=(s0(Wy[7])-s0(Wx[7]))&M, D9s=(s0(Wy[9])-s0(Wx[9]))&M)
SPC=spair_claw_consts()
assert (SPC['F7d'],SPC['T8'],SPC['D8'],SPC['D7'],SPC['D9s'])==(0x03bff800,0xfe808000,0xfbc00800,0x20000000,0x043ff800), SPC
class Mach:
  __slots__=('ops','nld')
  def __init__(self): self.ops=0; self.nld=0
  def op(self,n=1): self.ops+=n
  def br(self): self.ops+=2
  def bz(self): self.ops+=1
  def ld(self): self.ops+=2; self.nld+=1
  def st(self): self.ops+=2
def pf_consts(cv):
  A2,A3,A4,A5=SAx[2],SAx[3],SAx[4],SAx[5]; E6,E7,E8,E9=SE[6],SE[7],SE[8],SE[9]
  cE5=(A5-S0(A4)-MAJ(A4,A3,A2))&M; co0=cv_consts(cv); K2E5=(co0['K2']+cE5)&M; KNPHI=(0x60000000+K2E5-co0['KFm'])&M
  KW9=(E9-A5-S1(E8)-CH(E8,E7,E6)-K[9])&M; cW9=(KW9-cE5)&M
  cE4=(A4-S0(A3))&M; mA=A3&A2; mB=A3|A2; mX=A3^A2
  KW8=(E8-A4-S1(E7)-K[8])&M; cW8=(KW8-cE4)&M; cA=E7&E6; cB=~E7&M
  cW8f=(cW8+mA-cA)&M; cE4f=(cE4-mA)&M
  KK7c=(E7-2*A3-cv[0]+S0(A2)-S1(E6)-K[7])&M
  D7c=(_ty[1][7]-_tx[1][7])&M
  return dict(cE5=cE5,K2E5=K2E5,KNPHI=KNPHI,KW9=KW9,cW9=cW9,cE4=cE4,cE4f=cE4f,mA=mA,mB=mB,mX=mX,KW8=KW8,cW8=cW8,cW8f=cW8f,cA=cA,cB=cB,A2=A2,E6=E6,KK7c=KK7c,D7c=D7c)
PF_C2=13; PF_G=22; PF_F7=24
def s0d(x): x|=x<<32; return x^x>>4^x>>15
def postfilters(m,cv,a0,u,F,pf):
  E5=((u-F)+pf['K2E5']+a0)&M; m.op(3)
  m.br(); m.op(1)
  if (E5&0xE0000000)!=0xA0000000: return 0,0,0,0
  return (1,)+pf_tail(m,a0,E5,pf)
def pf_tail(m,a0,E5,pf):
  s2=s3=s4=0
  w9=(pf['KW9']-E5)&M; s9=s0d(w9); m.op(1+6)
  m.op(1); m.bz()
  ok2=((s9&0x22004000)==0x4000) if (w9&0x20000000) else ((s9&0x6600c000)==0x22008000)
  m.op(1); m.br(); m.op(1)
  if ok2:
    s2=1
    a1=(E5-pf['cE5'])&M; E40=(a0-(a1&pf['mX']))&M; w8=(pf['cW8f']-E40-(pf['cB']&E5))&M; m.op(6)
    s8=s0d(w8); z8=(s8&0x3c0c0000)|((w8>>2)&0x3300600); m.op(6+4)
    m.op(1); m.br()
    if (z8&0x15140200)==0x11100000: ok3=True; m.op(1)
    else:
      m.br(); m.op(1)
      ok3=(z8==0x26240200)
    if ok3:
      s3=1
      E4=(E40+pf['cE4f'])&M; maj2=MAJ(pf['A2'],a1,a0); ch2=CH(pf['E6'],E5,E4); w7=((pf['KK7c']+maj2)-ch2)&M; m.op(1+4+3+2)
      s7=s0d(w7); m.op(6)
      m.op(1); m.bz()
      if (w7&0x20000000)==0:
        m.op(1); m.br(); m.op(1)
        if (s7&0x22004000)==0x2004000: s4=1
      else:
        m.op(1); m.bz()
        ok4=((s7&0x6600c000)==0x24008000) if (w7&0x40000000)==0 else ((s7&0xee01c000)==0x68010000)
        m.op(1); m.br(); m.op(1)
        if ok4: s4=1
  return s2,s3,s4
def rowtest(m,tx,ty,i):
  (Ax,Ex,Wx),(Ay,Ey,Wy)=tx,ty
  for k,(x,y) in enumerate(((Ax[i],Ay[i]),(Ex[i],Ey[i]),(Wx[i],Wy[i]))):
    if k==2 and i in (7,8): continue
    msk,v,df=CELLS[k][i]
    if msk:
      m.op(3)
      if (x&msk)!=v: return False
    m.op(3)
    if (x^y)!=df: return False
  if PQE[i]:
    m.op(4)
    if (Ex[i]^Ex[i-1])&PQE[i]: return False
  for (k1,i1,b1,eq,k2,i2,b2,row) in X2:
    if row==i:
      m.op(6)
      if (((tx[k1][i1]>>b1)^(tx[k2][i2]>>b2))&1)!=(0 if eq else 1): return False
  return True
def step3b(m,cv,a0,a1):
  m.op(2*(6*15+10*16))
  wx,Ax,Ex=variantW_P1(cv,a0,a1,SAx,SExF,1); wy,Ay,Ey=variantW_P1(cv,a0,a1,SAy,SEyF,1)
  tx=(Ax,Ex,wx); ty=(Ay,Ey,wy); ok=True
  def one(i):
    for A,E,W in (tx,ty):
      W.append((s1(W[i-2])+W[i-7]+s0(W[i-15])+W[i-16])&M)
      E[i]=(A[i-4]+E[i-4]+S1(E[i-1])+CH(E[i-1],E[i-2],E[i-3])+K[i]+W[i])&M
      A[i]=(E[i]-A[i-4]+S0(A[i-1])+MAJ(A[i-1],A[i-2],A[i-3]))&M
  for i in range(16,22):
    m.op(100); one(i)
    if not rowtest(m,tx,ty,i): ok=False; break
  if ok:
    for i in range(22,38): m.op(100); one(i)
    m.op(17); ok=exact(tx,ty)
  m.op(1)
  return ok,wx[:16],wy[:16]
SExF=[_tx[1][i] for i in range(16)]; SEyF=[_ty[1][i] for i in range(16)]
def variantW_P1(cv,a0,a1,SA,SEF,state=False):
  A={-1:cv[0],-2:cv[1],-3:cv[2],-4:cv[3]}; E={-1:cv[4],-2:cv[5],-3:cv[6],-4:cv[7]}
  A[0]=a0; A[1]=a1
  for i in range(2,16): A[i]=SA[i]
  for i in range(6): E[i]=(A[i]+A[i-4]-S0(A[i-1])-MAJ(A[i-1],A[i-2],A[i-3]))&M
  for i in range(6,16): E[i]=SEF[i]
  W=[(E[i]-A[i-4]-E[i-4]-S1(E[i-1])-CH(E[i-1],E[i-2],E[i-3])-K[i])&M for i in range(16)]
  return (W,A,E) if state else W
def pf_ref(cv,a0,a1):
  wx=variantW_P1(cv,a0,a1,SAx,SExF); wy=variantW_P1(cv,a0,a1,SAy,SEyF)
  c1=((wy[8]-wx[8])&M)==SPC['D8']; c2=((s0(wy[9])-s0(wx[9]))&M)==SPC['D9s']; g=((s0(wy[8])-s0(wx[8]))&M)==SPC['T8']
  f7=((s0(wy[7])-s0(wx[7]))&M)==SPC['F7d'] and ((wy[7]-wx[7])&M)==SPC['D7']
  return (int(c1),int(c1 and c2),int(c1 and c2 and g),int(c1 and c2 and g and f7))
def e16_real_p1(cv,a0,a1):
  W=variantW_P1(cv,a0,a1,SAx,SExF); return trace(cv,W)[1][16]
NCOL=8; ROWB=19; RMASK=(1<<ROWB)-1; LANES=6; STR=39; FLD=33; CNT=234; EMPTYT=22; KEP=16; KEP_EPOCH=40; RECORD_BYTES=30; PAYLOAD_BITS=237; TERMINAL_PAD=32
# R_STAR: the frozen epoch alignment: the highest retained count among the four alignments the H1W
# panel measured; the census gives E(R_STAR) = E_SEL exactly, which both sides of the ledger charge.
R_STAR=8174
def lanes_const(v): return sum(v<<(STR*L+FLD) for L in range(LANES))
EMPTYW=lanes_const(EMPTYT); MASKW=lanes_const(0b011010); W8L=lanes_const(8); CMAIN=0; CSTR=W8L
KW=lanes_const(31); GW=lanes_const(32)
W9=9<<26; QPF=(57726359870197/2**58)*(287309824/2**32)
U_BASE=17; U_INS=22; U_DROP=9; RESET=5; A0_BASE=35; A0_RES=7; SETUP=14; ROWJ=2; XCROSS=0; READ=9; WALK=12
EXTRACT=2; CVSET=70; FBCTL=6; EPSET=6; STEP3B=3014
LAMSET=12; READC1=7; C1PRE=2
S0_LO=[S0(l) for l in range(256)]
LOG2_16={1<<i:i for i in range(16)}
GW_LO=sum(32<<(STR*L+FLD) for L in range(3)); G_L=[32<<(STR*L+FLD) for L in range(LANES)]
WT=[sum(G_L[j] for j in range(6) if m>>j&1)+1 for m in (4,2,1,3,16,8,7,5,6,15,11,9,10,13,12,14,32,31,20,18,17,19,25,23,21,22,24,28,26,27,29,30,47,36,34,33,35,41,39,37,38,40,44,42,43,45,46,55,51,49,48,50,53,52,54,59,57,56,58,61,60,62)]
def walk_lanes(z,m=None):
 if m:m.br()
 if z<WT[0]:
  if m:m.br()
  if z<WT[1]:
   if m:m.br()
   if z<WT[2]:
    return [0]
   else:
    return [1]
  else:
   if m:m.br()
   if z<WT[3]:
    return [0, 1]
   else:
    return [2]
 else:
  if m:m.br()
  if z<WT[4]:
   if m:m.br()
   if z<WT[5]:
    if m:m.br()
    if z<WT[6]:
     if m:m.br()
     if z<WT[7]:
      return [0, 2]
     else:
      if m:m.br()
      if z<WT[8]:
       return [1, 2]
      else:
       return [0, 1, 2]
    else:
     return [3]
   else:
    if m:m.br()
    if z<WT[9]:
     if m:m.br()
     if z<WT[10]:
      if m:m.br()
      if z<WT[11]:
       return [0, 3]
      else:
       if m:m.br()
       if z<WT[12]:
        return [1, 3]
       else:
        return [0, 1, 3]
     else:
      if m:m.br()
      if z<WT[13]:
       if m:m.br()
       if z<WT[14]:
        return [2, 3]
       else:
        return [0, 2, 3]
      else:
       if m:m.br()
       if z<WT[15]:
        return [1, 2, 3]
       else:
        return [0, 1, 2, 3]
    else:
     return [4]
  else:
   if m:m.br()
   if z<WT[16]:
    if m:m.br()
    if z<WT[17]:
     if m:m.br()
     if z<WT[18]:
      if m:m.br()
      if z<WT[19]:
       if m:m.br()
       if z<WT[20]:
        return [0, 4]
       else:
        return [1, 4]
      else:
       if m:m.br()
       if z<WT[21]:
        return [0, 1, 4]
       else:
        return [2, 4]
     else:
      if m:m.br()
      if z<WT[22]:
       if m:m.br()
       if z<WT[23]:
        if m:m.br()
        if z<WT[24]:
         return [0, 2, 4]
        else:
         if m:m.br()
         if z<WT[25]:
          return [1, 2, 4]
         else:
          return [0, 1, 2, 4]
       else:
        if m:m.br()
        if z<WT[26]:
         return [3, 4]
        else:
         return [0, 3, 4]
      else:
       if m:m.br()
       if z<WT[27]:
        if m:m.br()
        if z<WT[28]:
         return [1, 3, 4]
        else:
         if m:m.br()
         if z<WT[29]:
          return [0, 1, 3, 4]
         else:
          return [2, 3, 4]
       else:
        if m:m.br()
        if z<WT[30]:
         return [0, 2, 3, 4]
        else:
         if m:m.br()
         if z<WT[31]:
          return [1, 2, 3, 4]
         else:
          return [0, 1, 2, 3, 4]
    else:
     return [5]
   else:
    if m:m.br()
    if z<WT[32]:
     if m:m.br()
     if z<WT[33]:
      if m:m.br()
      if z<WT[34]:
       if m:m.br()
       if z<WT[35]:
        return [0, 5]
       else:
        return [1, 5]
      else:
       if m:m.br()
       if z<WT[36]:
        return [0, 1, 5]
       else:
        return [2, 5]
     else:
      if m:m.br()
      if z<WT[37]:
       if m:m.br()
       if z<WT[38]:
        if m:m.br()
        if z<WT[39]:
         return [0, 2, 5]
        else:
         if m:m.br()
         if z<WT[40]:
          return [1, 2, 5]
         else:
          return [0, 1, 2, 5]
       else:
        if m:m.br()
        if z<WT[41]:
         return [3, 5]
        else:
         return [0, 3, 5]
      else:
       if m:m.br()
       if z<WT[42]:
        if m:m.br()
        if z<WT[43]:
         return [1, 3, 5]
        else:
         if m:m.br()
         if z<WT[44]:
          return [0, 1, 3, 5]
         else:
          return [2, 3, 5]
       else:
        if m:m.br()
        if z<WT[45]:
         return [0, 2, 3, 5]
        else:
         if m:m.br()
         if z<WT[46]:
          return [1, 2, 3, 5]
         else:
          return [0, 1, 2, 3, 5]
    else:
     if m:m.br()
     if z<WT[47]:
      if m:m.br()
      if z<WT[48]:
       if m:m.br()
       if z<WT[49]:
        if m:m.br()
        if z<WT[50]:
         return [4, 5]
        else:
         return [0, 4, 5]
       else:
        if m:m.br()
        if z<WT[51]:
         return [1, 4, 5]
        else:
         return [0, 1, 4, 5]
      else:
       if m:m.br()
       if z<WT[52]:
        if m:m.br()
        if z<WT[53]:
         return [2, 4, 5]
        else:
         return [0, 2, 4, 5]
       else:
        if m:m.br()
        if z<WT[54]:
         return [1, 2, 4, 5]
        else:
         return [0, 1, 2, 4, 5]
     else:
      if m:m.br()
      if z<WT[55]:
       if m:m.br()
       if z<WT[56]:
        if m:m.br()
        if z<WT[57]:
         return [3, 4, 5]
        else:
         return [0, 3, 4, 5]
       else:
        if m:m.br()
        if z<WT[58]:
         return [1, 3, 4, 5]
        else:
         return [0, 1, 3, 4, 5]
      else:
       if m:m.br()
       if z<WT[59]:
        if m:m.br()
        if z<WT[60]:
         return [2, 3, 4, 5]
        else:
         return [0, 2, 3, 4, 5]
       else:
        if m:m.br()
        if z<WT[61]:
         return [1, 2, 3, 4, 5]
        else:
         return [0, 1, 2, 3, 4, 5]
WALK_LANE_WEIGHTS=(6,6,6,8,8,8)
WALK_INIT=1<<24
def walk_certificate():
  worst=0;bad=0
  for mask in range(1,64):
    z=sum(G_L[j] for j in range(6) if mask>>j&1);meter=Mach();got=walk_lanes(z,meter)
    want=[j for j in range(6) if mask>>j&1]
    bad+=got!=want or meter.ops>sum(WALK_LANE_WEIGHTS[j] for j in want)
    worst=max(worst,meter.ops)
  prefix=max(D(sum(WALK_LANE_WEIGHTS[:p]))/p for p in range(1,7))
  if bad or worst!=18 or prefix!=7:raise ValueError('ordered lane tree certificate')
  return dict(tree_masks=63,tree_mismatches=bad,tree_max_read_ops=worst,tree_mean_claw_bound=int(prefix),tree_max_claw_bound=max(WALK_LANE_WEIGHTS))
_WALK_CERT=walk_certificate()
WALK_PROVEN=D(_WALK_CERT['tree_mean_claw_bound']);WALK_MEAN=D('6.760092');WALK_MAX_READ=_WALK_CERT['tree_max_read_ops'];WALK_MAX_CLAW=_WALK_CERT['tree_max_claw_bound']
STEP3B_MEAN=D('842.361097')
def P(u): return (s0(u)-u)&M
def build_table(r,ustart,U,m=None,ncol=NCOL):
  tab={}; ent=drop=0; cov=8*ncol
  if m: m.op(EPSET)
  for n in range(U):
    u=(ustart+n)&M; g=(P(u)-r)&M; lo=g&8191
    if m: m.op(15); m.br()
    if lo>=cov: continue
    k=((lo>>3)<<ROWB)|(g>>13); d=tab.get(k,EMPTYW); c=d>>CNT
    if m: m.op(4); m.ld(); m.op(1); m.br()
    if c>=LANES: drop+=1; continue
    sh=STR*c; lane=u|((g&7)<<FLD)
    if m: m.op(3); m.ld(); m.ld(); m.op(4); m.st()
    d=(d&~(EMPTYT<<(sh+FLD)))|(lane<<sh); d+=1<<CNT; tab[k]=d; ent+=1
  return tab,ent,drop
def table_entries(tab):
  for k,d in tab.items():
    col=k>>ROWB; row=k&RMASK
    for L in range(d>>CNT):
      ln=d>>(STR*L); yield ((row<<13)|(col<<3)|((ln>>FLD)&7))&M, ln&M
def probe_word(d,WB,C=0):
  return (((d+WB+C)&MASKW)+KW)&GW
def lanes_at(v,pos): return sum(v<<(STR*L+pos) for L in range(LANES))
T3W=lanes_at(7<<29,0)
MT3W=MASKW|T3W; CMAIN1=0; CSTR1=W8L
def wbl(w,PHI,c1=0):
  nphi=(0x60000000-PHI)&M; lv=nphi|((32-w)<<FLD)
  b=lv|(lv<<STR); b|=b<<(2*STR); WBL0=b|((b<<(4*STR))&ONES)
  return (WBL0+c1) if c1 else WBL0
def probe_word_c1(d,WBL,C1=0):
  return (GW-((d+(WBL+C1 if C1 else WBL))&MT3W))&GW
GATE2=4; GATE1=3; BATCH=8; EXTRACT_BS=20; A0_PROBE=21; CV_BS=1024; GBS=218
class Planes:
  def __init__(self,m): self.m=m; self.g=0
  def x(self,a,b): self.g+=GATE2; return a^b
  def a(self,a,b): self.g+=GATE2; return a&b
  def o(self,a,b): self.g+=GATE2; return a|b
  def n(self,a): self.g+=GATE1; return a^ONES
def bs_mask(co,cv,Hr,base,pl,ncol=NCOL):
  A=list(LANEPL)
  for i in range(8,32): A.append(ONES if (base>>i)&1 else 0); pl.g+=GATE2
  e=co['E0base']; E=[0]*32; c=0
  for i in range(32):
    ei=(e>>i)&1
    if i==0: E[0]=pl.n(A[0]) if ei else A[0]; c=A[0] if ei else 0; continue
    if ei: E[i]=pl.n(pl.x(A[i],c)); cn=pl.o(A[i],c)
    else: E[i]=pl.x(A[i],c); cn=pl.a(A[i],c)
    c=cn
  def sig(X,r1,r2,r3): return [pl.x(pl.x(X[(i+r1)%32],X[(i+r2)%32]),X[(i+r3)%32]) for i in range(13)]
  S0p=sig(A,2,13,22); S1p=sig(E,6,11,25)
  a,b,ee,ff=cv[0],cv[1],cv[4],cv[5]; MJ=[]; CHp=[]
  for i in range(13):
    ai,bi,ei,fi=(a>>i)&1,(b>>i)&1,(ee>>i)&1,(ff>>i)&1
    MJ.append((ONES if ai else 0) if ai==bi else A[i])
    CHp.append((ONES if ei else 0) if ei==fi else (E[i] if ei else pl.n(E[i])))
  def neg(X): return [(x^ONES) if x in (0,ONES) else pl.n(x) for x in X]
  konst=(co['KF']+4)&8191
  terms=[A[:13],neg(S0p),neg(MJ),neg(S1p),neg(CHp),[(ONES if (konst>>i)&1 else 0) for i in range(13)]]
  while len(terms)>2:
    X,Y,Z=terms.pop(),terms.pop(),terms.pop(); S=[]; Cc=[0]
    for i in range(13):
      t=pl.x(X[i],Y[i]); S.append(pl.x(t,Z[i])); Cc.append(pl.o(pl.a(X[i],Y[i]),pl.a(Z[i],t)))
    terms+=[S,Cc[:13]]
  X,Y=terms; F=[]; c=0
  for i in range(13):
    t=pl.x(X[i],Y[i]); F.append(pl.x(t,c)); c=pl.o(pl.a(X[i],Y[i]),pl.a(c,t))
  k=(Hr+5+1)&8191; X=[pl.n(f) for f in F]; T=[]; c=0
  for i in range(13):
    if (k>>i)&1: T.append(pl.n(pl.x(X[i],c))); c=pl.o(X[i],c)
    else: T.append(pl.x(X[i],c)); c=pl.a(X[i],c)
  lim=8*ncol+5; lt=0; eq=ONES
  for i in range(9,-1,-1):
    if (lim>>i)&1: lt=pl.o(lt,pl.a(eq,pl.n(T[i]))); eq=pl.a(eq,T[i])
    else: eq=pl.a(eq,pl.n(T[i]))
  same=pl.n(pl.o(pl.x(T[10],T[11]),pl.x(T[11],T[12])))
  return pl.a(lt,same)
class RM:
  def __init__(self,nreg=16): self.ops=0; self.loads=0; self.stores=0; self.gates=0; self.live={}; self.nreg=nreg; self.peak=0
  def _chk(self):
    self.peak=max(self.peak,len(self.live)); assert len(self.live)<=self.nreg,len(self.live)
  def load(self,name,val): self.ops+=1; self.loads+=1; self.live[name]=val; self._chk(); return name
  def free(self,*names):
    for n in names: self.live.pop(n,None)
  def store(self,name): self.ops+=1; self.stores+=1; v=self.live.pop(name); return v
  def g(self,out,f,*ins):
    self.ops+=1; self.gates+=1; v=f(*[self.live[i] for i in ins]); self.live[out]=v; self._chk(); return out
def bs_mask_rm(co,cv,Hr,base,rm,ncol=NCOL):
  X=lambda a,b:a^b; A_=lambda a,b:a&b; O=lambda a,b:a|b; N=lambda a:a^ONES
  s0_b=S0(base)
  e_hi0=(base+co['E0base_hi'])&M; e_hi1=(e_hi0+256)&M
  s1_0=S1(e_hi0); s1_1=S1(e_hi1)
  ch_0=co['FF_hi']^(e_hi0&co['EF_hi']); ch_1=co['FF_hi']^(e_hi1&co['EF_hi'])
  k_base=Hr-co['K_cv']-(base&co['NAB_hi'])+(s0_b&0x13C0)
  k0=(k_base+(s1_0&0x107C)+ch_0)&8191; k1=(k_base+(s1_1&0x107C)+ch_1)&8191
  w_idx=SP_S0[s0_b&4095]|SP_S10[s1_0&4095]|SP_S11[s1_1&4095]|SP_K0[k0]|SP_K1[k1]
  rm.ops+=60
  CT=co['CT']; lim=8*ncol+5
  def ld_col(i,sh,msk,names):
    idx=(w_idx&msk) if sh==0 else ((w_idx>>sh) if msk==0 else ((w_idx>>sh)&msk))
    rm.ops+=(1 if (sh==0 or msk==0) else 2)+len(names)
    for nm,val in zip(names,CT[i][idx]): rm.load(nm,val)
  def csa(p,q,r,cout,sout):
    rm.g('v',A_,p,q); rm.g('u',X,p,q); rm.free(p,q); rm.g('w',A_,r,'u'); rm.g(sout,X,'u',r); rm.free('u',r)
    rm.g(cout,O,'v','w'); rm.free('v','w')
  def ha(p,q,cout,sout):
    rm.g(cout,A_,p,q); rm.g(sout,X,p,q); rm.free(p,q)
  ld_col(0,0,15,('ge','c1_0','c2_0'))
  ld_col(1,4,15,('c1','c2','s1'))
  ha('s1','c1_0','c3','t'); rm.g('c3',O,'c3','c2_0'); rm.free('c2_0')
  rm.g('ge',A_ if (lim>>1)&1 else O,'t','ge'); rm.free('t')
  for i,sh in ((2,8),(3,11),(4,14),(5,17)):
    ld_col(i,sh,7,('c1n','s1'))
    csa('s1','c1','c2','c2n','s2'); ha('s2','c3','c3n','t')
    rm.live['c1']=rm.live.pop('c1n'); rm.live['c2']=rm.live.pop('c2n'); rm.live['c3']=rm.live.pop('c3n')
    rm.g('ge',A_ if (lim>>i)&1 else O,'t','ge'); rm.free('t')
  csa('c1','c2','c3','c1n','s1')
  ld_col(6,20,3,('v','u'))
  rm.g('w',A_,'s1','u'); rm.g('t',X,'s1','u'); rm.free('s1','u'); rm.g('c2',O,'v','w'); rm.free('v','w')
  rm.live['c1']=rm.live.pop('c1n')
  rm.g('ge',A_ if (lim>>6)&1 else O,'t','ge'); rm.free('t')
  for i,sh in ((7,22),(8,26)):
    ld_col(i,sh,15,('c1n','s1'))
    csa('s1','c1','c2','c2n','t')
    rm.live['c1']=rm.live.pop('c1n'); rm.live['c2']=rm.live.pop('c2n')
    rm.g('ge',A_ if (lim>>i)&1 else O,'t','ge'); rm.free('t')
  ld_col(9,30,15,('v','u'))
  rm.g('w',A_,'c1','u'); rm.g('s1',X,'c1','u'); rm.free('c1','u'); rm.g('c1',O,'v','w'); rm.free('v','w')
  ha('s1','c2','c2n','t'); rm.live['c2']=rm.live.pop('c2n')
  rm.g('ge',A_ if (lim>>9)&1 else O,'t','ge'); rm.free('t')
  for i,sh in ((10,34),(11,39)):
    ld_col(i,sh,31,('c1n','s1'))
    csa('s1','c1','c2','c2n','T%d'%i)
    rm.live['c1']=rm.live.pop('c1n'); rm.live['c2']=rm.live.pop('c2n')
  ld_col(12,44,0,('t0',))
  rm.g('t0',X,'t0','c1'); rm.g('T12',X,'t0','c2'); rm.free('t0','c1','c2')
  rm.g('u',X,'T10','T11'); rm.g('v',X,'T11','T12'); rm.g('u',O,'u','v'); rm.g('u',O,'u','ge'); rm.g('m',N,'u')
  return rm.live['m']
def gbs_worst():
  cv=[0,M,0,0,M,0,0,0]; co=cv_consts(cv); rm=RM()
  bs_mask_rm(co,cv,(8191-6)&M,W9,rm); return rm.ops
def bs_check(seed,nb=16):
  cv,_=cv_from_seed(seed); co=cv_consts(cv); sh=Shake(seed+'|bs'); sh.word(); r=R_STAR; Hr=(R16H[0]-r)&M; bad=n=gmax=0
  for k in range(nb):
    base=W9+((sh.word()&((1<<26)-1))&~255); rm=RM(); mask=bs_mask_rm(co,cv,Hr,base,rm); gmax=max(gmax,rm.ops)
    bad+=bin(mask^bs_mask(co,cv,Hr,base,Planes(None))).count('1')
    for l in range(256):
      t=((Hr-Ffun(cv,base+l,co))+5)&8191; want=t<8*NCOL+5 or 7168<=t<7168+8*NCOL+5
      bad+=int(want!=bool((mask>>l)&1)); n+=int(want)
  return dict(bs_batches=nb,bs_probing_lanes=n,bs_mismatches=bad,bs_gates_max=gmax,bs_gate_bound=GBS)
def scan_cv(cv,tab,r,a0s,m=None,ncol=NCOL,bs=True):
  co=cv_consts(cv); pf=pf_consts(cv); Hr=(R16H[0]-r)&M; cov=8*ncol; dense=cov+5>1024
  st=dict(a0=0,probes=0,reads=0,fired=0,claws=0,passes=[0,0,0,0],good=[],coll=[],batches=0,gates=0)
  mm=m or Mach()
  def probe(a0,F,y,win):
    if not dense:
      yp=(y+1029)&M; rowb=yp>>13; u0=(yp&127)+3; w=u0&7; c1=u0>>3; c=c1-1
    else:
      yw=(y+(win<<10))&M; rowb=yw>>13; c=(yw>>3)&1023; w=yw&7; c1=c+1
    WB=lanes_const(32-w)
    PHI=(F-a0-pf['K2E5'])&M; WBL0=wbl(w,PHI); WBL1=WBL0+W8L
    if m: m.op(SETUP+LAMSET)
    st['probes']+=1
    for j in range(20):
      rowj=(rowb+T20[j])&RMASK
      if m and j: m.op(ROWJ)
      rd=[]
      if 0<=c<ncol: rd.append((c,rowj,CMAIN,WBL0))
      if w>=3:
        if c1<ncol: rd.append((c1,rowj,CSTR,WBL1))
        elif dense and c==1023: rd.append((0,(rowj+1)&RMASK,CSTR,WBL1))
      for (cc,rr,C,WBL) in rd:
        d=tab.get((cc<<ROWB)|rr,EMPTYW); st['reads']+=1
        s=d+WBL; z=(GW-(s&MT3W))&GW
        if m: m.ld(); m.op(4); m.bz()
        if not z: continue
        st['fired']+=1
        for L in walk_lanes(z,m):
          u=(d>>(STR*L))&M; st['claws']+=1
          E5=((s>>(STR*L))&M)|0xA0000000
          if m: m.op(C1PRE)
          fl=(1,)+pf_tail(mm,a0,E5,pf)
          for i in range(4): st['passes'][i]+=fl[i]
          if fl[3]:
            a1=(u-hfun(cv,a0))&M; st['good'].append((a0,a1,u))
            ok,wx,wy=step3b(mm,cv,a0,a1)
            if ok: st['coll'].append((a0,a1,u,wx,wy))
  if bs and not dense:
    if m: m.op(CV_BS)
    a0s=list(a0s); assert len(a0s)%256==0
    bases=a0s[::256]; assert all(b%256==0 and a0s[i*256:(i+1)*256]==list(range(b,b+256)) for i,b in enumerate(bases))
    for base in bases:
      rm=RM(); mask=bs_mask_rm(co,cv,Hr,base,rm,ncol); st['batches']+=1; st['gates']+=rm.ops; st['a0']+=256
      if m: m.op(rm.ops+BATCH+SBLOOP); m.br()
      s0b=S0(base); Hrp0=(Hr-co['KFm'])&M
      while mask:
        low=mask&-mask; mask^=low; l=low.bit_length()-1; a0=base|l
        e0=(a0+co['E0base'])&M; ch0=co['FF']^(co['EF']&e0); s0a=s0b^S0_LO[l]
        F0=((a0&co['NAB'])-s0a-S1(e0)-ch0)&M; y=(Hrp0-F0)&M; F=(F0+co['KFm'])&M; win=((y+5)>>10)&1
        if m: m.op(EXTRACT_BS+A0_PROBE)
        probe(a0,F,y,win)
    return st
  for a0 in a0s:
    F=Ffun(cv,a0,co); y=(Hr-F)&M; st['a0']+=1
    if m: m.op(4+26+1)
    if dense: wins=(0,1)
    else:
      q=(y+5)&1023
      if m: m.op(2); m.br()
      if q>=cov+5: continue
      v=((y+5)>>10)&7
      if m: m.op(3); m.br(); m.br()
      if v==0: wins=(0,)
      elif v==7: wins=(1,)
      else: continue
    for win in wins: probe(a0,F,y,win)
  return st
def ref_claws(cv,tab,r,a0s):
  co=cv_consts(cv); Hr=(R16H[0]-r)&M; lo={}; out=[]
  for G,u in table_entries(tab): lo.setdefault(G&8191,[]).append((G,u))
  for a0 in a0s:
    y=(Hr-Ffun(cv,a0,co))&M
    for o in OFFS:
      for (G,u) in lo.get((y+o)&8191,()):
        if (((G-y-o)&M)>>13) in T20S: out.append((a0,u))
  return out
T20S=set(T20)
class Shake:
  def __init__(self,label): self.buf=b''; self.n=0; self.lab=label.encode()
  def word(self):
    if not self.buf: self.buf=hashlib.shake_256(self.lab+struct.pack('<I',self.n)).digest(256); self.n+=1
    w=struct.unpack('<I',self.buf[:4])[0]; self.buf=self.buf[4:]; return w
def cv_from_seed(seed):
  sh=Shake(seed)
  for _ in range(CLS_TRY):
    M0=[sh.word() for _ in range(16)]; cv=compress(IV,M0)
    if kept(cv): return cv,M0
  raise RuntimeError('no kept chaining value')
def spair_obs():
  m=Mach(); ok,wx,wy=step3b(m,PCV,SAx[0],SAx[1])
  return dict(step3b_P8_pair_ok=int(ok and wx==PMX and wy==PMY),step3b_P8_pair_ops=m.ops)
def probe_exhaustive():
  sh=Shake('probe|exhaustive'); bad=n=0
  for kind,C in ((0,CMAIN),(1,CSTR)):
    for w in range(8):
      WB=lanes_const(32-w)
      for rep in range(24):
        tags=[(rep*5+L*3+w)%9 for L in range(LANES)]; tags=[EMPTYT if t==8 else t for t in tags]
        d=sum(((sh.word()|(t<<FLD))<<(STR*L)) for L,t in enumerate(tags))|((rep%7)<<CNT)
        z=probe_word(d,WB,C)
        for L,t in enumerate(tags):
          fired=not (z>>(STR*L+FLD+5))&1
          want=t!=EMPTYT and ((t-w) in (0,1,4,5) if kind==0 else (t+8-w) in (0,1,4,5))
          bad+=int(fired!=want); n+=1
  return n,bad
C1EDGE=(0,1,2,(1<<29)-2,(1<<29)-1,1<<29,(1<<29)+1,(1<<30)-1,1<<30,M-1,M,0xA0000000,0x9fffffff,0xbfffffff,0xc0000000)
def probe_c1_exhaustive():
  sh=Shake('probe|c1'); bad=n=npass=0
  phis=(0,1,2,M,M-1,0x60000000,0x5fffffff,0x80000000)
  for kind in (0,1):
    for w in range(8):
      for rep in range(24):
        PHI=phis[rep] if rep<len(phis) else sh.word(); WBL=wbl(w,PHI)+(W8L if kind else 0)
        tags=[(rep*5+L*3+w)%9 for L in range(LANES)]; tags=[EMPTYT if t==8 else t for t in tags]
        us=[]
        for L in range(LANES):
          k=sh.word()%4
          if k==0: us.append(sh.word())
          elif k==1: us.append((PHI+0xA0000000+sh.word()%(1<<29))&M)
          else: us.append((PHI+C1EDGE[sh.word()%len(C1EDGE)])&M)
        d=sum(((u|(t<<FLD))<<(STR*L)) for L,(u,t) in enumerate(zip(us,tags)))|((rep%7)<<CNT)
        z=probe_word_c1(d,WBL)
        for L,(u,t) in enumerate(zip(us,tags)):
          fired=(z>>(STR*L+FLD+5))&1
          want=t!=EMPTYT and ((t-w) in (0,1,4,5) if kind==0 else (t+8-w) in (0,1,4,5)) and (((u-PHI)&M)>>29)==5
          bad+=int(fired!=want); n+=1; npass+=int(want)
  i=0
  for kind in (0,1):
    for w in range(8):
      for t in list(range(8))+[EMPTYT]:
        for v in range(8):
          for hi in (0,1):
            PHI=sh.word()%((7-v)*(1<<29)+1) if hi else M-sh.word()%(1<<28)
            while True:
              u=(PHI+(v<<29)+(sh.word()&((1<<29)-1)))&M
              if int(u>=PHI)==hi: break
            WBL=wbl(w,PHI)+(W8L if kind else 0)
            P0=i%LANES; us=[sh.word() for _ in range(LANES)]; ts=[sh.word()%9 for _ in range(LANES)]
            ts=[EMPTYT if x==8 else x for x in ts]; us[P0]=u; ts[P0]=t; i+=1
            d=sum(((uu|(tt<<FLD))<<(STR*L)) for L,(uu,tt) in enumerate(zip(us,ts)))|((i%7)<<CNT)
            z=probe_word_c1(d,WBL)
            for L,(uu,tt) in enumerate(zip(us,ts)):
              fired=(z>>(STR*L+FLD+5))&1
              want=tt!=EMPTYT and ((tt-w) in (0,1,4,5) if kind==0 else (tt+8-w) in (0,1,4,5)) and (((uu-PHI)&M)>>29)==5
              bad+=int(fired!=want); n+=1; npass+=int(want)
  return n,bad,npass
def c1_of(cv,a0,u): return pf_ref(cv,a0,(u-hfun(cv,a0))&M)[0]
def online_trial(seed,U=1<<17,NA=1<<17):
  sh=Shake(seed+'|epoch'); sh.word(); r=R_STAR; ustart=sh.word(); cv,M0=cv_from_seed(seed)
  m=Mach(); tab,ent,drop=build_table(r,ustart,U,m); bops=m.ops
  sbs=sorted(list(dict.fromkeys(SEL[sh.word()%NSEL] for _ in range(4*NA//256)))[:NA//256]); a0s=sel_a0s(sbs)
  m2=Mach(); st=scan_cv(cv,tab,r,a0s,m2)
  ref=sorted(ref_claws(cv,tab,r,a0s))
  ref1=sorted(x for x in ref if c1_of(cv,*x))
  e16bad=sum(1 for (a0,u) in ref if not r16ok(e16_real_p1(cv,a0,(u-hfun(cv,a0))&M)))
  rfl=[(a0,u,pf_ref(cv,a0,(u-hfun(cv,a0))&M)) for (a0,u) in ref1]
  wantp=tuple(sum(fl[i] for a0,u,fl in rfl) for i in range(4))
  wantg=sorted((a0,u) for a0,u,fl in rfl if fl[3]); gotg=sorted((a0,u) for a0,a1,u in st['good'])
  pfmis=int(tuple(st['passes'])!=wantp)+int(gotg!=wantg)
  return cv,M0,st,dict(entries=ent,ref_claws=len(ref),c1_claws=st['claws'],
    c1_claws_equal_ref=int(st['claws']==len(ref1)),claw_e16_bad=e16bad,
    postfilter_ref_mismatch=pfmis,probes=st['probes'],reads=st['reads'],scan_ops=m2.ops,c1c2=st['passes'][1],
    good_pairs=len(st['good']),step3b_collisions=len(st['coll']),expected_claws_milli=int(round(1000*160.0*ent*NA/2**32)),
    distinct_pairs=len(set(ref)))
def dense_trial(seed,U=1<<16,NA=1<<13,rows=True):
  sh=Shake(seed+'|dense'); sh.word(); r=R_STAR; ustart=sh.word(); cv,M0=cv_from_seed(seed)
  tab,ent,drop=build_table(r,ustart,U,None,ncol=1024)
  base=sh.word()&((1<<26)-1)&~(NA-1); a0s=range(W9+base,W9+base+NA)
  st=scan_cv(cv,tab,r,a0s,None,ncol=1024)
  ref=sorted(ref_claws(cv,tab,r,a0s))
  ref1=sorted(x for x in ref if c1_of(cv,*x))
  rfl=[(a0,u,pf_ref(cv,a0,(u-hfun(cv,a0))&M)) for (a0,u) in ref1]
  wantp=tuple(sum(fl[i] for a0,u,fl in rfl) for i in range(4))
  wantg=sorted((a0,u) for a0,u,fl in rfl if fl[3]); gotg=sorted((a0,u) for a0,a1,u in st['good'])
  cum=[0]*22; bad=0; pfmis=int(tuple(st['passes'])!=wantp)+int(gotg!=wantg)
  for (a0,u) in ref:
    a1=(u-hfun(cv,a0))&M; wx=variantW_P1(cv,a0,a1,SAx,SExF); wy=variantW_P1(cv,a0,a1,SAy,SEyF)
    tx=trace(cv,wx); ty=trace(cv,wy); e16=tx[1][16]
    bad+=int(not r16ok(e16))
    if rows:
      for i in range(16,22):
        if rowok(tx,ty,i): cum[i]+=1
        else: break
  return dict(entries=ent,ref_claws=len(ref),c1_claws=st['claws'],
    c1_claws_equal_ref=int(st['claws']==len(ref1)),row16_bad=bad,postfilter_ref_mismatch=pfmis,
    rows_le16=cum[16],rows_le17=cum[17],rows_le18=cum[18],rows_le19=cum[19],rows_le20=cum[20],rows_le21=cum[21],
    c1c2=st['passes'][1],expected_claws_milli=int(round(1000*160.0*ent*NA/2**32)))
NON=4; NDE=4
def walk_mean_obs(seed,n=1<<17):
  # H1W check: per probe position (w uniform) a main read and, for w>=3, a next read (96+60 of 156); Poisson(8) buckets,
  # first six lanes in cyclic u order from ustart, uniform tags and PHI; actual walk_lanes, real-word C1 recheck
  sh=Shake(seed+'|walk'); ops=cl=rd=bad=s1=s2=s12=0; us=sh.word()
  def bucket():
    k=0; x=sh.word()/2**32; e=c=math.exp(-8)
    while x>c and k<40: k+=1; e*=8/k; c+=e
    v=sorted(((sh.word()-us)&M,sh.word()&7) for _ in range(k))[:LANES]; d=EMPTYW
    for L,(u,t) in enumerate(v): d=(d&~(EMPTYT<<(STR*L+FLD)))|((((u+us)&M)|(t<<FLD))<<(STR*L)); d+=1<<CNT
    return d
  for i in range(n):
    w=sh.word()&7; PHI=sh.word(); W=wbl(w,PHI); x=y=0
    for off in ((0,8) if w>=3 else (0,)):
      d=bucket(); z=(GW-((d+W+(W8L if off else 0))&MT3W))&GW; rd+=1
      if not z: continue
      m=Mach(); F=walk_lanes(z,m); x+=m.ops; y+=len(F)
      for l in F:
        t=(d>>(STR*l+FLD))&63; uq=(d>>(STR*l))&M
        bad+=not(t<8 and (t+off-w) in ((1,4,5) if off else (0,1,4,5)) and ((uq-PHI)&M)>>29==5)
    ops+=x; cl+=y; s1+=x*x; s2+=y*y; s12+=x*y
  R=ops/cl; se=math.sqrt(max(0,(s1-2*R*s12+R*R*s2)/(n-1))/n)/(cl/n)
  return dict(walk_draws=n,walk_reads=rd,walk_claws=cl,walk_ops=ops,walk_lane_mismatch=bad,walk_mean_ppm=int(1e6*R),walk_se_ppm=int(1e6*se),walk_ucb99_ppm=int(1e6*(R+2.326*se)),walk_charge_ppm=int(WALK_MEAN*10**6))
def wcv_obs(seed,K=16,U=1<<16,NA=1<<10):
  # H3 control: one seed table, K seed CVs on one a0 range; J = endpoint-sharing groups (a0 or u) of row-16 claws
  sh=Shake(seed+'|wcv'); sh.word(); r=R_STAR; tab,_,_=build_table(r,sh.word(),U,None,ncol=1024); lo={}; n=q=0
  for G,u in table_entries(tab): lo.setdefault(G&8191,[]).append((G,u))
  b=W9+(sh.word()&((1<<26)-1)&~(NA-1)); Hr=(R16H[0]-r)&M
  for k in range(K):
    cv,_=cv_from_seed(seed+'|wcv%d'%k); co=cv_consts(cv); p={}
    def f(x):
      while p.setdefault(x,x)!=x: x=p[x]
      return x
    for a0 in range(b,b+NA):
      y=(Hr-Ffun(cv,a0,co))&M
      for o in OFFS:
        for (G,u) in lo.get((y+o)&8191,()):
          if (((G-y-o)&M)>>13) in T20S: p[f((0,a0))]=f((1,u))
    J=len({f(x) for x in list(p) if x[0]==0}); n+=J; q+=J*(J-1)
  return dict(wcv_cvs=K,wcv_events=n,wcv_mean_ppm=int(1e6*n/K),wcv_ratio_ppm=int(1e6*q/n) if n else 0)
def r17(s):
 h=Shake(s);w=h.word;o=[0]*4;V=variantW_P1
 for _ in[0]*200:
  a=w();A=w();c=[w()for _ in o*2]
  for i in 2,0:
   x=trace(c,V(c,a,A,SAx,SExF));y=trace(c,V(c,a,A,SAy,SEyF))
   for k in 0,1:o[i+k]+=cellok(k,17,x[k][17],y[k][17])
   c[7]=(x[1][16]+c[7]-R16H[w()%20])&M
 return dict(cA=o[0],cE=o[1],uA=o[2],uE=o[3])
def sm(s):
 h=Shake(s);p=pf_consts([0]*8);N=1<<16;e=d=0
 for _ in[0]*N:
  E=5<<29|h.word()>>3;w=p['KW9']-E&M;t=s0(w);e+=pf_tail(Mach(),0,E,p)[0];d+=((t&0x4400800)==0x800)if w>>29&1 else((t&0xcc01800)==0x4401000)
 return dict(e=e*10**6//N,d=d*10**6//N,n=N)
def run_request(req):
  out=[]; eid=req['experiment_id']
  for tr in req['trials']:
    t=tr['trial']; rec=dict(trial=t,message_a_hex=None,message_b_hex=None); s=eid+'|'+tr['seed']
    if 'online' in eid:
      if t<NON:
        cv,M0,st,obs=online_trial(s); rec['observations']=obs
        if st['coll'] and obs['claw_e16_bad']==0:
          a0,a1,u,wx,wy=st['coll'][0]
          rec['message_a_hex']=struct.pack('>32I',*(M0+wx)).hex(); rec['message_b_hex']=struct.pack('>32I',*(M0+wy)).hex()
      elif t==NON: rec['observations']=spair_obs()
      elif t==NON+1:
        n,bad=probe_exhaustive(); n1,bad1,np1=probe_c1_exhaustive()
        rec['observations']=dict(probe_lanes_checked=n,probe_mismatches=bad,c1test_lanes_checked=n1,c1test_mismatches=bad1,c1test_firing_lanes=np1)
      elif t==NON+2:
        ob=bs_check(s); ob['bs_gate_worst']=gbs_worst(); rec['observations']=ob
      elif t==NON+3: rec['observations']=sel_rates(s)
      elif t==NON+4: rec['observations']=cls_rates(s)
    else:
      if t<NDE: rec['observations']=dense_trial(s)
      elif t==NDE: rec['observations']=spair_obs()
      elif t==NDE+1: rec['observations']=cls_msg(s)
      elif t==NDE+2: rec['observations']=wcv_obs(s)
      elif t==NDE+3: rec['observations']=r17(s)
      elif t==NDE+4:rec['observations']=sm(s)
    if t==9:rec['observations']=walk_certificate()
    elif t==11 and 'online' in eid:rec['observations']=walk_mean_obs(s)
    elif t==10:
      _,n,s,info=ledger(False)
      rec['observations']=dict(ledger_N=n,ledger_NCV=info['NCV'],walk_init=WALK_INIT,walk_mean_ppm=int(WALK_MEAN*10**6),walk_proven=int(WALK_PROVEN),walk_max_read=WALK_MAX_READ,walk_max_claw=WALK_MAX_CLAW,step3b_mean_ppm=int(STEP3B_MEAN*10**6),step3b_max=STEP3B)
    out.append(rec)
  return dict(schema_version=1,trials=out)
SEL_Z='eNrt2b9KxDAcB/BvYjkiOHS8sfSE7h5cRiP4Dj7ADV3FwmVNwaGDg4/gOzi4trj4Jl3dbqy/Xr3BAwep0Dv4fpp/TUKHhF8yFCCiiUS/9H92I20HreROyva9LEvV3JRKSRJceqJpJYB2Q1MfDN2Pjf9r/2o3vrvzb+1ma/2Mq010RLGfpDqRqE+llidJf3oYG/++KLwvpJS68Ot8sbfe5TPuANGE8a/7E0AifZ//Of7tlbX5arlcZYsszW128H3NHSDi/U9EvP+J6HiEXQL0UwQDJy0l9S1cXIdhvAqhnxJduLjviFDjXJnLCsHhkQtIdMrxb8L3IVDJmwEqJyfA8yxuMEfcOIQXmLqCC6GCCZEz/TSF2n3M//Jz7wvv5eA3'
def _sel():
  bm=zlib.decompress(base64.b64decode(SEL_Z)); return [(q<<2)|1 for q in range(1<<16) if (bm[q>>3]>>(q&7))&1]
SEL=_sel(); SEL_SHA='150659fc4312d162c842c12db3defee46bb330f77158ac35bafb9930f52414da'
assert len(SEL)==4096 and hashlib.sha256(','.join(map(str,SEL)).encode()).hexdigest()==SEL_SHA
SELS=set(SEL); NSEL=len(SEL); NA_SEL=NSEL*256; N12=53096854
G_SEL=2051404269120
MSG_LO='-0.011821'
SBLOOP=7; KEP_SEL=20
CLS_MASK=63<<24; CLS_VAL=12<<24; SELJ=6; SELT=3; M0RAND=16; F7R='0.1205926'; F7R_HI='0.1206112'; F7C_MEAN='0.1206019'; MSG_CLS='-0.0225'; CLS_TRY=4096
def kept(cv): return (cv[0]&CLS_MASK)==CLS_VAL
def g_draw(sh,pf):
  for _ in range(1<<12):
    E5=0xA0000000|(sh.word()&0x1fffffff); w9=(pf['KW9']-E5)&M
    if (s0((w9+SPC['D9'])&M)-s0(w9))&M==SPC['D9s']: break
  a0=W9+(SEL[sh.word()%NSEL]<<8)+(sh.word()&255); a1=(E5-pf['cE5'])&M
  maj1=(pf['mA']|(a1&pf['mB']))&M; E40=(a0-maj1)&M; chx=(pf['cA']^(pf['cB']&E5))&M; w8=((pf['cW8']-E40)-chx)&M
  if (s0((w8+SPC['D8'])&M)-s0(w8))&M!=SPC['T8']: return None
  E4=(E40+pf['cE4'])&M; return (MAJ(pf['A2'],a1,a0)-CH(pf['E6'],E5,E4))&M,a0,a1
def f7c(pf,q,cv0): w7=(pf['KK7c']-cv0+q)&M; return (s0((w7+pf['D7c'])&M)-s0(w7))&M==SPC['F7d']
def cls_cv0(w): return (w&~CLS_MASK&M)|CLS_VAL
def cls_rates(seed,n=1<<15,m=16):
  sh=Shake(seed+'|cls'); pf=pf_consts([0]*8); g=fc=fu=0
  for i in range(n):
    r=g_draw(sh,pf)
    if r is None: continue
    g+=1; q=r[0]
    for j in range(m): fc+=f7c(pf,q,cls_cv0(sh.word())); fu+=f7c(pf,q,sh.word())
  return dict(draws=n,g_pairs=g,cv0_per_pair=m,f7_cls=fc,f7_all=fu,f7_cls_exp_milli=int(round(1000*g*m*float(F7C_MEAN))),
        f7_all_exp_milli=int(round(1000*g*m*287309824/2**32)))
def cls_msg(seed,n=1<<6):
  sh=Shake(seed+'|clsmsg'); pf=pf_consts([0]*8); px=trace(IV,PMX)[2]; py=trace(IV,PMY)[2]
  T23=px[23]^py[23]; T25=(py[25]-px[25])&M; ob={}
  for side in ('all','cls'):
    c=dict(pairs=0,e16_bad=0,pf_bad=0,dw23=0,dw25=0)
    for i in range(n):
      for _ in range(1<<20):
        r=g_draw(sh,pf)
        if r is None: continue
        q,a0,a1=r; cv=[sh.word() for _ in range(7)]
        if side=='cls': cv[0]=cls_cv0(cv[0])
        if f7c(pf,q,cv[0]): break
      t=T160[sh.word()%160]; cv.append(0); u=(a1+hfun(cv,a0))&M
      cv[7]=(Ffun(cv,a0,cv_consts(cv))+P(u)-t)&M
      wx=variantW_P1(cv,a0,a1,SAx,SExF); wy=variantW_P1(cv,a0,a1,SAy,SEyF)
      wx=trace(cv,wx)[2]; wy=trace(cv,wy)[2]
      c['pairs']+=1; c['e16_bad']+=e16_real_p1(cv,a0,a1)!=t; c['pf_bad']+=pf_ref(cv,a0,a1)!=(1,1,1,1)
      c['dw23']+=(wx[23]^wy[23])==T23; c['dw25']+=((wy[25]-wx[25])&M)==T25
    for k,v in c.items(): ob[k+'_'+side]=v
  return ob
def sel_a0s(sbs): return [W9+(sb<<8)+l for sb in sbs for l in range(256)]
def sel_rates(seed,n=1<<15):
  sh=Shake(seed+'|sel'); pf=pf_consts([0]*8); c=dict(gs=0,gw=0,fs=0,fw=0)
  def a1draw():
    while True:
      E5=0xA0000000|(sh.word()&0x1fffffff); w9=(pf['KW9']-E5)&M
      if (s0((w9+SPC['D9'])&M)-s0(w9))&M==SPC['D9s']: return E5
  def g_and_q(a0,E5):
    a1=(E5-pf['cE5'])&M; maj1=(pf['mA']|(a1&pf['mB']))&M; E40=(a0-maj1)&M; chx=(pf['cA']^(pf['cB']&E5))&M
    w8=((pf['cW8']-E40)-chx)&M
    if (s0((w8+SPC['D8'])&M)-s0(w8))&M!=SPC['T8']: return None
    E4=(E40+pf['cE4'])&M; return (MAJ(pf['A2'],a1,a0)-CH(pf['E6'],E5,E4))&M
  def f7(q,cv0):
    w7=(pf['KK7c']-cv0+q)&M; return (s0((w7+pf['D7c'])&M)-s0(w7))&M==SPC['F7d']
  for i in range(n):
    E5=a1draw(); sb=SEL[sh.word()%NSEL]; q=g_and_q(W9+(sb<<8)+(sh.word()&255),E5)
    if q is not None:
      c['gs']+=1; c['fs']+=f7(q,sh.word())
    q=g_and_q(W9+(sh.word()&((1<<26)-1)),E5)
    if q is not None: c['gw']+=1; c['fw']+=f7(q,sh.word())
  return dict(sel_ok=int(len(SEL)==4096),draws=n,g_sel=c['gs'],f7_sel=c['fs'],g_w9=c['gw'],f7_w9=c['fw'],
        g_sel_exp_milli=int(round(1000*n*G_SEL/(NA_SEL*N12))),g_w9_exp_milli=int(round(1000*n*57726359870197/2**26/N12)))
CENSUS14={'complete': True, 'reference_control_passed': True, 'reference_15': {'minimum': 44436632, 'maximum': 44543396, 'rotations': 8192, 'sum': 364428388980}, 'candidate_14': {'minimum': 41471916, 'maximum': 41577489, 'rotations': 8192, 'sum': 340133163048}}
CENSUS8={'complete': True, 'reference_control_passed': True, 'reference_15': {'minimum': 44436632, 'maximum': 44543396, 'rotations': 8192, 'sum': 364428388980}, 'candidate_8': {'minimum': 26656700, 'maximum': 26745958, 'rotations': 8192, 'sum': 218657033388}}; CENSUS10={'complete': True, 'reference_control_passed': True, 'reference_15': {'minimum': 44436632, 'maximum': 44543396, 'rotations': 8192, 'sum': 364428388980}, 'candidate_10': {'minimum': 29617909, 'maximum': 29708804, 'rotations': 8192, 'sum': 242952259320}}; CENSUS11={'complete': True, 'reference_control_passed': True, 'reference_15': {'minimum': 44436632, 'maximum': 44543396, 'rotations': 8192, 'sum': 364428388980}, 'candidate_11': {'minimum': 32581626, 'maximum': 32676574, 'rotations': 8192, 'sum': 267247485252}}; CENSUS12={'complete': True, 'reference_control_passed': True, 'reference_15': {'minimum': 44436632, 'maximum': 44543396, 'rotations': 8192, 'sum': 364428388980}, 'candidate_12': {'minimum': 35546342, 'maximum': 35641736, 'rotations': 8192, 'sum': 291542711184}}
CENSUS13={'complete': True, 'reference_control_passed': True, 'reference_15': {'minimum': 44436632, 'maximum': 44543396, 'rotations': 8192, 'sum': 364428388980}, 'candidate_13': {'minimum': 38510323, 'maximum': 38610389, 'rotations': 8192, 'sum': 315837937116}}
def column_parameters(ncol,census=None):
  if ncol not in (8,9,10,11,12,13,14,15):raise ValueError('supported column count is 11, 12, 13, 14 or 15')
  if ncol==15:lo,hi,mean=44436632,44543396,'44485887.327'
  elif ncol==13:lo,hi,mean=38510323,38610389,str(D(315837937116)/8192)
  else:
    evidence={8:CENSUS8,10:CENSUS10,11:CENSUS11,12:CENSUS12,14:CENSUS14}[ncol] if census is None else census
    if not evidence or not evidence.get('complete') or not evidence.get('reference_control_passed'):raise ValueError('complete measured %d-column census required'%ncol)
    ref=evidence['reference_15'];actual=evidence['candidate_%d'%ncol]
    if (ref['minimum'],ref['maximum'],ref['rotations'])!=(44436632,44543396,8192):raise ValueError('15-column census control')
    if actual['rotations']!=8192 or 15*actual['sum']!=ncol*ref['sum']:raise ValueError('census mean identity')
    lo,hi=actual['minimum'],actual['maximum'];mean=str(D(actual['sum'])/8192)
  limit=8*ncol+5;reads=26*ncol;table=ncol*(1<<19)*RECORD_BYTES+TERMINAL_PAD;online=table+(2<<20)
  return dict(ncol=ncol,coverage_limit=8*ncol,probe_limit=limit,probing_low_words=2*limit,reads_per_head=reads,table_bytes=table,complete_online_peak_bytes=online,complete_peak_bytes=max(online,136433664),E_LO=lo,E_HI=hi,E_SEL=23771164,R_STAR=R_STAR,E_MEAN=mean,COV=8*ncol*(1<<19),NB=ncol*(1<<19),conservative_first_block_ratio=str(D(44436632)/lo),conservative_first_block_ratio_numerator=44436632,conservative_first_block_ratio_denominator=lo)
Q3P1='-96.0791'
def ledger(show=True,q3_log2=Q3P1,eps_log2=20,succ='0.39',A_C=2**60,A_S=2**60,DEV=2**60,mem=None,kep=None,bs=True,c1=True,sel=True,cls=True,ncol=NCOL,census=None):
    getcontext().prec=90
    geo=column_parameters(ncol,census);E_LO=geo['E_LO'];E_HI=geo['E_HI'];E_SEL=geo['E_SEL'];E_MEAN=geo['E_MEAN'];COV=geo['COV'];NB=geo['NB']
    if mem is None:mem=str(D(geo['complete_peak_bytes']).ln()/D(2).ln())
    cls=cls and sel
    if kep is None: kep=KEP_EPOCH
    kf=D(2)**-SELJ if cls else 1; st=SELT if cls else 0
    C=2728; L2=D(2).ln(); P2=lambda x: (D(x)*L2).exp(); NA=2**26; eps=D(2)**-eps_log2; K=2**kep
    p12=D(53096854)/D(2)**32; p12g=D(57726359870197)/D(2)**58; q_pf=p12g*D(287309824)/D(2)**32; q_pf_hi=q_pf
    pf=6+D(PF_C2)/8+PF_G*p12+PF_F7*p12g
    pres=D(geo['probe_limit'])/1024; pprobe=D(geo['probing_low_words'])/8192
    reads=D(20)*geo['reads_per_head']/geo['probing_low_words']; xc=D(20)*10/geo['probing_low_words']
    probe=SETUP+20*ROWJ+reads*(READ+WALK)+xc*XCROSS
    claw=EXTRACT+pf+q_pf*STEP3B
    # The epoch table's alignment r is frozen at the chosen H1W-measured alignment R_STAR=8174,
    # so every epoch table has exactly E_SEL retained entries; both ledger sides use that count.
    ca_hi=D(160)*D(E_SEL)/D(2)**32; ca_lo=D(160)*D(E_SEL)/D(2)**32
    if c1:
        probe=SETUP+LAMSET+19*ROWJ+reads*READC1+xc*XCROSS
        claw=(WALK_MEAN+C1PRE+PF_C2+8*PF_G*p12+8*PF_F7*p12g+8*q_pf*STEP3B)/8
    fe=D(GBS+BATCH+2)/256
    if sel:
        NA=NA_SEL; gsel=D(G_SEL)/(D(NA_SEL)*N12); f7lo=f7hi=D(F7R) if cls else D(287309824)/D(2)**32
        if cls: f7hi=D(F7R_HI)
        q_pf=p12*gsel*f7lo; q_pf_hi=p12*gsel*f7hi; p12g=p12*gsel
        claw=(WALK_MEAN+C1PRE+PF_C2+8*PF_G*p12+8*PF_F7*p12g+8*q_pf_hi*STEP3B_MEAN)/8
        fe=D(GBS+BATCH+2+SBLOOP)/256
    per_a0=(fe+pprobe*(EXTRACT_BS+A0_PROBE+probe)+ca_hi*claw) if bs else (A0_BASE+pres*A0_RES+pprobe*probe+ca_hi*claw)
    wbar=C+M0RAND+st+FBCTL+kf*(CVSET+(CV_BS if bs else 0)+NA*per_a0)
    build=EPSET+NB*RESET+D(2)**32*U_BASE+E_SEL*U_INS+(COV-E_SEL)*U_DROP
    a0max=(D(GBS+BATCH+2)/256+EXTRACT_BS+A0_PROBE if bs else A0_BASE+A0_RES)+SETUP+20*(ROWJ+XCROSS)+40*(READ+WALK)+40*LANES*(EXTRACT+6+PF_C2+PF_G+PF_F7+STEP3B)
    if c1: a0max=D(GBS+BATCH+2)/256+EXTRACT_BS+A0_PROBE+SETUP+LAMSET+19*ROWJ+20*XCROSS+40*(READC1+WALK_MAX_READ)+40*LANES*(C1PRE+PF_C2+PF_G+PF_F7+STEP3B)
    if sel: a0max+=D(SBLOOP)/256
    vmax=int(C+M0RAND+st+FBCTL+CVSET+(CV_BS if bs else 0)+NA*a0max)
    q3r=P2(q3_log2)*D(2)**32/160
    if sel: q3r*=P2(MSG_LO)
    if cls: q3r*=P2(MSG_CLS)
    lam=kf*NA*ca_lo*q_pf*q3r*(1-D(2)**D('-8.5'))*(1-D(2)**-25)
    target=1-D(succ)-D(2)**-60
    NCV=int((-(target).ln()/lam))+1
    while 1-(-(NCV-1)*lam).exp()-D(2)**-60>=D(succ): NCV-=1
    NE=-(-NCV//K)
    VCV=int(((1+eps)*NCV*wbar).to_integral_value(rounding='ROUND_CEILING'))
    VMAX=NE*int(build)+VCV
    bern=(eps**2*NCV*wbar)/(2*vmax*(1+eps/3)); succ_lb=1-(-NCV*lam).exp()-(-bern).exp()-D(2)**-60
    ALLOW=(A_C+A_S+DEV)*C; OVER=int(max(vmax,build)); FIN=6*C+1600+WALK_INIT; N=ALLOW+VMAX+OVER+FIN
    tlog=float((D(N)/C).ln()/L2); score=tlog+float(D(mem))-20
    if show:
        print('u-table: %d columns x 2^%d rows, %d lanes, %d bytes including terminal pad; retained entries %d .. %d (mean %s) of %d covered'
              %(ncol,ROWB,LANES,RECORD_BYTES*NB+TERMINAL_PAD,E_LO,E_HI,E_MEAN,COV))
        print('claws/a0 = %.6f (charged %.6f); q_pf = 2^%.4f; tag-only chain (55328d60) %.6f + q_pf x step 3b %.6f per claw'
              %(float(ca_lo),float(ca_hi),float(q_pf.ln()/L2),float(pf),float(q_pf*STEP3B)))
        if c1: print('C1 in the bucket test: per C1-claw walk %s + %d + segments %d + %d x P(C2|C1) %.6f + %d x P(C2 G|C1) %.6f + 8 q_pf_hi x step 3b %.6f = %.6f'
              %(WALK_MEAN,C1PRE,PF_C2,PF_G,float(8*PF_G*p12),PF_F7,float(8*PF_F7*p12g),float(8*q_pf_hi*(STEP3B_MEAN if sel else STEP3B)),float(8*claw)))
        if sel: print('selection: %d sub-blocks (%d a0) per scanned chaining value; P(G | C1 C2, SEL) = %.9f (W9: %.9f) = x%.4f; F7 rate %.5f; q_pf = 2^%.4f; epoch 2^%d first blocks'
              %(NSEL,NA_SEL,float(gsel),float(D(57726359870197)/D(2)**26/N12),float(gsel*D(2)**26*N12/D(57726359870197)),float(f7lo),float(q_pf.ln()/L2),kep))
        if cls: print('class ((cv0 >> 24) & 63) == 12: 2^-%d of first blocks kept, %d+%d ops per first block; F7 rate %s (99%% lower bound); message channel 2^%s charged'%(SELJ,SELT,FBCTL,F7R,MSG_CLS))
        if c1: print('per a0: front end (%d + %d + 2)/256 = %.6f + %.6f x (%d + %d + probe %.4f [setup %d + %d, %d heads x %d, %.1f reads x %d (tag and C1 test), %.1f x %d]) + %.6f C1-claws x %.6f = %.6f ops; per claw %.4f'
              %(GBS,BATCH+(SBLOOP if sel else 0),float(fe),float(pprobe),EXTRACT_BS,A0_PROBE,float(probe),SETUP,LAMSET,19,ROWJ,float(reads),READC1,float(xc),XCROSS,float(ca_hi/8),float(8*claw),float(per_a0),float(per_a0/ca_lo)))
        elif bs: print('per a0: front end (%d + %d + 2)/256 = %.6f + %.6f x (%d + %d + probe %.4f) + %.6f x claw %.6f = %.6f ops; per claw %.4f'
              %(GBS,BATCH,float(D(GBS+BATCH+2)/256),float(pprobe),EXTRACT_BS,A0_PROBE,float(probe),float(ca_hi),float(claw),float(per_a0),float(per_a0/ca_lo)))
        else: print('per a0: base %d + %.6f (resolve) + %.6f x probe %.4f + %.6f x claw %.6f = %.6f ops; per claw %.4f'
              %(A0_BASE,float(pres*A0_RES),float(pprobe),float(probe),float(ca_hi),float(claw),float(per_a0),float(per_a0/ca_lo)))
        print('epoch build %d ops (%.4f%% of an epoch of 2^%d first blocks)'%(int(build),100*float(build/(K*wbar)),kep))
        print('wbar = %.6e  vmax = %d  N_CV = %d  epochs = %d  V_MAX = %d'%(float(wbar),int(vmax),NCV,NE,VMAX))
        print('allowances A_C + A_S + DEV = 2^%.5f compressions = %.4f%% of N;  N = %d'%(float((D(A_C+A_S+DEV)).ln()/L2),100*float(D(ALLOW)/N),N))
        print('time_log2 = %.7f  memory 2^%s  score = %.7f  success >= %s'%(tlog,mem,score,str(succ_lb)[:22]))
    return tlog,N,succ_lb,dict(per_a0=per_a0,wbar=wbar,NCV=NCV,ca_lo=ca_lo,ca_hi=ca_hi,probe=probe,claw=claw,build=int(build),vmax=vmax,NE=NE,VCV=VCV,VMAX=VMAX,ALLOW=ALLOW,OVER=OVER,FIN=FIN,geometry=geo)
def selftest():
  print('selftest utab38'); ok=True
  assert (SPC['F7d'],SPC['T8'],SPC['D8'],SPC['D7'],SPC['D9s'])==(0x03bff800,0xfe808000,0xfbc00800,0x20000000,0x043ff800)
  assert len(T160)==160 and all(r16ok(w) for w in T160) and len(T20S)==20; print(' S-pair constants, |S160| = 160: OK')
  o=spair_obs(); print(' step 3b on the P8 pair:',o); ok&= o['step3b_P8_pair_ok']==1 and o['step3b_P8_pair_ops']==STEP3B
  n,bad=probe_exhaustive(); print(' six-lane test against the scalar definitions: %d lane checks, %d mismatches'%(n,bad)); ok&= bad==0
  n,bad,np1=probe_c1_exhaustive(); print(' combined tag and C1 test (Lemma B\'\'): %d lane checks, %d firing, %d mismatches'%(n,np1,bad)); ok&= bad==0 and np1>0
  for s in range(1,1<<LANES):
    z=sum(G_L[L] for L in range(LANES) if (s>>L)&1); mw=Mach(); got=walk_lanes(z,mw)
    ok&= got==[L for L in range(LANES) if (s>>L)&1] and mw.ops<=WALK_MAX_CLAW*len(got)
  gw=gbs_worst(); ob=bs_check('selftest|bs',nb=64)
  print(' bitsliced front end:',ob,'worst-constant gate charge',gw); ok&= ob['bs_mismatches']==0 and gw==GBS and ob['bs_gates_max']<=GBS
  for sd in ('selftest|a','selftest|b'):
    cv,M0,st,ob=online_trial(sd); print(' online',sd,ob)
    ok&= ob['c1_claws_equal_ref']==1 and ob['claw_e16_bad']==0 and ob['postfilter_ref_mismatch']==0 and ob['ref_claws']>0
    ob=dense_trial(sd,NA=1<<13); print(' dense ',sd,ob)
    ok&= ob['c1_claws_equal_ref']==1 and ob['row16_bad']==0 and ob['postfilter_ref_mismatch']==0 and ob['c1_claws']>0
  tab={}; rr=random.Random(5); keep={}
  for i in range(64):
    u=rr.getrandbits(32); g=(rr.randrange(4)<<3)|rr.randrange(8); k=((g>>3)<<ROWB)|7; d=tab.get(k,EMPTYW); c=d>>CNT
    if c<LANES:
      sh=STR*c; d=(d&~(EMPTYT<<(sh+FLD)))|((u|((g&7)<<FLD))<<sh); d+=1<<CNT; tab[k]=d; keep.setdefault(k,[]).append((g&7,u))
  rec={k:[((d>>(STR*L+FLD))&63,(d>>(STR*L))&M) for L in range(d>>CNT)] for k,d in tab.items()}
  emp=all(((d>>(STR*L+FLD))&63)==EMPTYT for k,d in tab.items() for L in range(d>>CNT,LANES))
  print(' retention: %d buckets, first six kept in insertion order %s, empty lanes marked %s'%(len(tab),rec==keep,emp)); ok&= rec==keep and emp
  cv,_=cv_from_seed('selftest|ops'); sh=Shake('selftest|ops'); sh.word(); r=R_STAR
  tab,ent,drop=build_table(r,sh.word(),1<<16); m=Mach(); a0s=range(W9,W9+(1<<16)); st=scan_cv(cv,tab,r,a0s,m)
  chg=CV_BS+st['batches']*(GBS+BATCH+2+SBLOOP)+st['probes']*(EXTRACT_BS+A0_PROBE+SETUP+LAMSET+19*ROWJ+20*XCROSS)+st['reads']*READC1
  chg+=st['claws']*(WALK_MAX_CLAW+C1PRE+PF_C2+PF_G+PF_F7)+len(st['good'])*STEP3B
  print(' counted scan ops %d <= itemised charge %d: %s (probes %d of %d a0, reads %d)'%(m.ops,chg,m.ops<=chg,st['probes'],st['a0'],st['reads']))
  ok&= m.ops<=chg and abs(st['probes']/st['a0']-2*(8*NCOL+5)/8192)<0.003
  ob=sel_rates('selftest|sel',n=1<<13); print(' selection rates (sampled):',ob)
  ok&= ob['sel_ok']==1 and ob['g_sel']>ob['g_w9']
  oc=cls_rates('selftest|cls',n=1<<13,m=8); om=cls_msg('selftest|cls',n=16); print(' class rates (sampled):',oc,om)
  ok&= oc['f7_cls']>oc['f7_all'] and om['e16_bad_all']==0 and om['e16_bad_cls']==0 and om['pf_bad_all']==0 and om['pf_bad_cls']==0
  tlog,N,sl,_=ledger(show=False); print(' ledger time_log2 = %.7f, success >= %s'%(tlog,str(sl)[:12])); ok&= sl>=D('0.39')
  print('SELFTEST','PASS' if ok else 'FAIL'); return ok
def main():
  a=sys.argv[1] if len(sys.argv)>1 else ''
  if a=='selftest': sys.exit(0 if selftest() else 1)
  if a=='ledger': ledger(); return
  if a=='ledger-inherited': ledger(A_C=2**78,A_S=2**74,DEV=2**70); return
  if a=='ledger-allow70': ledger(A_C=2**70,A_S=2**70,DEV=2**70); return
  if a=='sel-rates': print(sel_rates('cli')); return
  if a=='cls-rates': print(cls_rates('cli'),cls_msg('cli')); return
  if a=='ledger-base': ledger(cls=False); return
  if a=='ledger-scalar': ledger(bs=False,c1=False,sel=False); return
  if a=='ledger-tag': ledger(c1=False,sel=False); return
  if a=='ledger-c1': ledger(sel=False); return
  sys.stdout.write(json.dumps(run_request(json.load(sys.stdin))))
if __name__=='__main__': main()
```
<!-- END DB38_H8G_8COL_SOURCE -->

## Appendix Y. Evidence boundary and declared organizer experiments

This variant includes byte-for-byte copies of the two organizer experiments
declared by accepted parent 9cdbd3c1. `a0p-online-r38` is a bounded real-
compression control for H1, H5 and deterministic identities. Its returned
pairs are not full collisions. `a0p-q3-r38` is a reduced-replica consistency
check; it is not an estimate of q3 and does not certify q3_model. Neither
experiment measures H8, H9, success frequency, expected cost or any deep-event
probability. The attack, its fresh algorithmic coins, its exact collision
implication, all probability premises and every charged integer are unchanged.
Finite participant measurements below support plausibility only; each named
extrapolation remains a disclosed premise with its stated sensitivity.

| premise | concrete relevant support retained in this proof | unresolved boundary |
| --- | --- | --- |
| H2-P1 | Section 9's registered P1/base paired panels, per-seed values, zero replay diagnostics, lower-bound rule and independent current-minimum calculation | transfer of the measured law to every retained u-table good pair |
| H2b | owned sequential-Monte-Carlo design, exact row-16 weight, known-answer stages, full-compression replay requirement, dead-seed rule and registered P/Q/R reproductions | absence of an independent implementation and direct observation at about 2^-96 |
| H4a | 38 logged solver runs, 230,183 listed seconds, the author's development bound and the explicit 2^60 charged cap, with 2^70 and lineage fallbacks priced | unlogged dense-row derivation |
| H4b | the inherited Step-1 SAT construction, repeated-solve accounting and explicit 2^60 charged cap | unavailable complete historical execution log |
| H4c | Appendix U's exhaustive/current work census, named failed and repeated studies, and explicit 2^60 charged cap | historical development not reconstructed instruction by instruction |
| H6D | reported same-specification maxima, decoder measurement and a local Kissat build reproducing recorded C0 counts | historical formula, binary and platform unavailable |
| H6E | eleven fixed-seed controls, 24 file/pipe configurations, five PySAT builds, two LP-certificate checkers and measured live clause objects | transfer from fresh controls to the historical P8 execution |
| H8 | exact selected-window message counts, registered per-seed evidence, pooled 2^-0.011821 charge and explicit 1.1122-bit sensitivity | deep state invariance after conditioning on the selected window |
| H9 | independent class-selection/measurement pools, class F7/message rates, paired evidence, unchanged 2^-0.0225 charge and explicit no-class sensitivity | deep state invariance after conditioning on the cv0 class |

The corresponding proof sections state who ran each measurement, its finite
scope and every unavailable historical input. The premises are not promoted to
proofs by this appendix. Their role is the same conditional exploratory role as
before; deterministic correctness, caps and resource arithmetic remain separate.


## Appendix Z. The recorded tail list is charged once, not twice: phase E sets the memory maximum

**Claim.** Change one scheduling fact of Appendix W and nothing else: the recorder writes the tail-clause record incrementally, clause by clause, through a fixed 4 KiB buffer while the encoder appends each tail clause, and phase R consumes that file through the charged 1,048,576-byte solver pipe input instead of mapping it. The recorded list is therefore never a process-resident object: it is filesystem state, and its serialised length is disk occupancy, not memory. Under Appendix W section 5's premises unchanged, phase E is at most **160,546,816 bytes** and phase R at most **157,474,816**; the ten-column online image **159,383,584** lies 1,163,232 below phase E. The counted phase maximum is therefore phase E, **160,546,816**, and the charge is that maximum: memory_log2_bytes **27.258419**, scalar **83.743859** (this maximum is superseded by Appendix ZS). No premise is added; no probability, allowance, encoder semantics, regenerator semantics or output changes.

### 1. The record is charged once, not twice
Appendix W's phase-E row charges the recorded tail list (44,593,152 bytes at its 5/8 bound) inside the encoder's cell, and its phase-R row charges the same list again inside the regenerator's cell. Both charges are legitimate: precomputed data is chargeable whether it is resident in a process or held in filesystem state, and this filing does not claim otherwise. Appendix Z charges their actual coexistence path: the full list at the start, a shrinking list plus a growing partial record in the middle, and the full record at the end. It never replaces that path by the sum of both full encodings.

**Lemma RF (the record's charged length).** Every literal of the P8 spec is a nonzero integer in [-(V-1), V-1] with V = 51,945, the first field of the DIMACS header that Appendix W section 2 regenerates and checks byte for byte. Hence |lit| <= 51,944 < 2^16, so a literal fits a 16-bit unsigned magnitude and one further bit per literal carries its sign: at most 17/8 = 2.125 bytes per literal, plus a 2-byte clause length. A tail clause of k literals therefore costs at most 2 + 17k/8 bytes, and 2 + 17k/8 <= 14.875 + 17k/8 = (17/64)(56 + 8k) for every k >= 0. With the recorded tail list L = 71,213,440 = G - 85,323,392 bytes (Appendix W section 4) the record is at most 76,656 + (17/64)L = 18,992,726 bytes, **18,997,248 after page rounding, and this is the size charged**. In particular R <= (17/64)L.

**Lemma RF1 (the list and its record never coexist in full).** G = 156,536,832 is exactly the model part 85,323,392 plus the tail list L = 71,213,440 (Appendix W section 4), so the tail clause objects are inside G. The recorder walks that tail list and, for each clause, emits its fixed-width record and then releases that clause's list object, because phase R reads the record rather than the list. If a fraction x of the tail list has been released, the resident encoder figure is G - xL + R_written with R_written <= (17/64)xL <= 0.266xL, so the figure never rises above G and it ends at G - L + R = 109,845,632 + 18,997,248 = 128,842,880, which is below G. Kernel state and the replaced launcher are not process-resident in active phase E (section 3). The phase-E peak is therefore G plus 4,009,984 bytes of procedure code files and recorder overhead, i.e. **160,546,816**, and the record's 18,997,248 bytes are charged as the *alternative* endpoint of that coexistence maximum (18,997,248 + 4,009,984 = 23,007,232 < 160,546,816), not as an addition to the list that produced them. Charging both operands would charge the same tail clauses twice. QED

### 2. Withdrawal of Lemma RE2
**Withdrawal.** The predecessor's Lemma RE2 read V = 51,945 < 2^16 as a bound for a **signed** 16-bit word. That inference is false: a signed 16-bit word holds at most 32,767, and 51,944 exceeds it. Lemma RE2 and the 184,725,504-byte cell that rested on it are withdrawn, and Lemma RE's 4-byte width with its 202,526,720-byte cell are withdrawn with it, because Appendix W's own fallback row was superseded only by Lemma RE2. Lemma RF is the only statement this filing makes about the record's encoding, it is correct for a *signed* literal range of +-51,944, and the record it bounds is charged in full.

### 3. Phases and charge

| Phase | Components (bytes) | Total |
| --- | --- | ---: |
| E | encoder G 156,536,832 (contains the 71,213,440-byte tail list, released clause by clause as the record is written; Lemma RF1) + procedure code files 1,912,832 + recorder overhead 2,097,152; kernel state is kernel-side and the launcher is replaced at exec, while the charged 18,997,248-byte record is the alternative endpoint of the same coexistence maximum | **160,546,816** |
| R | filter 1,048,576 + kernel 4,194,304 + key file 16,384 + launcher 4,194,304 + model file 200,704 + pipes 2,097,152 + procedure code files 1,912,832 + charged record 18,997,248 + regenerator 33,554,432 + solver S 90,210,304 + solver pipe input 1,048,576 | **157,474,816** |
| S, D, online | unchanged from Appendix W section 4 and section 10 | 103,874,560; 115,376,128; **159,383,584** |

**Which phase-E rows this filing keeps.** Appendix W section 4 also charges kernel 2,097,152 and launcher 4,194,304 in phase E. This filing drops exactly those two and nothing else: kernel memory is kernel-side and never enters any process's resident set, and the launcher is replaced at exec, so it does not coexist with the encoder. The procedure code files 1,912,832 and the recorder overhead 2,097,152 stay charged, so phase E = G + 4,009,984 = 160,546,816, and the implementation witness's measured peak 160,505,856 lies 40,960 below it. The sensitivity is stated rather than hidden: restoring both rows gives phase E = 166,838,272, memory_log2_bytes 27.313876 and scalar 83.865096. **The charge.** The counted phase maximum is phase E **160,546,816** (27.258419); the ten-column online image 159,383,584 lies 1,163,232 below it and phase R 157,474,816 lies 3,072,000 below it. The ten-column witness allocates exactly that image, reports working-set delta 159,387,648 and peaks at **160,505,856** resident bytes (`VmHWM`), 1,220,576 above the image because it retains the witness process's mapped runtime image. That measured peak lies 40,960 below the counted phase maximum, phase E 160,546,816, which is therefore the charge: **160,546,816** = memory_log2_bytes **27.258419**, scalar **83.743859**. The recorder's whole-process figures, 168,951,808 with no blocks and 176,832,512 with 5,430 blocks, are stress measurements of that process which exceed G and are therefore not procedure cells: H6-D reads G as the live-clause figure, so phase E is the modelled 160,546,816 and the count, not a measurement, sets the charge. Every other measured cell is below it: H7 65,265,200; gmass 136,433,664; p8fam 71,163,904 (69,496 KiB); fillr2 68,521,984 (66,916 KiB). The predecessor's twelve-column peak resident 193,490,944 belongs to a superseded filing and to a different image and is not a phase of this one.

### 4. Output equivalence and operations
The regenerator re-serialises the recorded literals in the serializer's fixed order and pass 1 compares the result with the recorded SHA-256 of the exact serializer output, refusing any difference before Kissat receives a byte (Appendix W section 2). Lemma RF changes where the bytes live, not which bytes they are; Lemma RF1 changes only the fixed-width layout of the same token stream. R.6D determinism therefore returns the same P8, the refusal check is unchanged, and Appendix W section 9's 2^54-word-operation budget is charged per formula token, not per stored byte, so time_log2 76.48544 and preprocessing_log2 61.58497 are unchanged.

### 5. Sensitivity and limits
Active phase E is G + 4,009,984 with no wider term, so its required bound rises exactly one byte per byte that the H6-D encoder figure G is understated. Since phase E already sets the submitted 160,546,816-byte maximum and lies 1,163,232 above the online image, every positive understatement exceeds the submitted bound; Appendix W section 6's 27,950,800-byte local clause-object margin supports H6-E(a0) but is not certified slack for the historical execution, and the superseded 1.25-, 1.5- and 1.625-byte slopes belonged to charged record widths and no longer apply. The charge is the counted phase maximum; the participant online measurement is only a cross-check below it. A larger valid phase measurement would raise the required bound, never lower it. Under H6-E(b)'s 64 KiB-page alternative the record's page rounding changes and no cell moves, so the page choice is not load-bearing. This appendix adds no probability evidence, advice, experiment or historical re-run, and every limitation of section 10 and Appendix Y stands.

## Appendix AA. Independent re-execution of the retained-entry census (2026-11-20)

Section 3.1's census is re-executed here instead of quoted, with the instrument the base ships in Appendix D
(`fillr2.c`, 1,055 bytes, SHA-256 `92bd2e1d59613cc689a3fb258e3ca249142525a8c8224050115d678c7aa45dca`). For each
residue j = r mod 8 the program counts, over all 2^32 words u, the aligned 8-windows of P(u)-j in 2^26-byte slices
and prints S_j[c] for c = 0..1023; retained(8m+j) is the cyclic window of length n on S_j, so the extrema over the
8,192 rotations follow exactly. Eight processes, one per j, peak at 66,856, 66,488, 66,976, 66,412, 66,352, 66,476,
65,924 and 66,780 KiB resident (the base recorded 66,916 KiB).

| columns | minimum | maximum | sum |
| --- | --- | --- | --- |
| 15 (recorded control) | 44,436,632 | 44,543,396 | 364,428,388,980 |
| 13 (recorded control) | 38,510,323 | 38,610,389 | 315,837,937,116 |
| 12 (this re-execution; the twelve-column filing carried the same row) | 35,546,342 | 35,641,736 | 291,542,711,184 |
| 11 (this re-execution; the eleven-column filing carried the same row) | 32,581,626 | 32,676,574 | 267,247,485,252 |
| 10 (the parent; this filing's row is in Appendix ZS) | 29,617,909 | 29,708,804 | 242,952,259,320 |

Every row satisfies the mean law 15*sum(n) = n*364,428,388,980 of Section 3.1. The thirteen- and fifteen-column
rows are recorded controls and are reproduced exactly, and the twelve-column row reproduces the value the
twelve-column filing carried; all three therefore bind the instrument and the reduction before the ten-column
row is used. The deterministic instrument was run once for each j=0..7 and takes no seed. This is a new bounded measurement, not a reproduction
of a historical run, and it is charged to DEV inside the 2^50 bound of Section 11 (eight 2^32-word passes).

## Appendix AB. Unique-pool H8 rebase onto public leader 1753d8ed

This is a narrow derivative of public r38 leader `1753d8ed-2e8a-4de0-b01f-9511751c1696` at commit
`7cf94dcf5a86471c522504443e2b25ae948c379c` and organizer rounded-field scalar 83.809639. The ten-column
construction, table geometry, memory cells, advice, preprocessing, allowances,
operation prices, cap, success target, H8 state-side premise and all other
premises are unchanged. The executable changes exactly one score input:
`MSG_LO='-0.0468'` becomes `MSG_LO='-0.0119'`.

S217 combines the historical and extension panels into unique seeds 101..168
counted once. It comprises 1,700,000,000 pairs per side, SEL
profile 257,983 and W9 profile 258,427. The point log2 ratio is
-0.0024808069401957883 bit, standard error 0.004014896826580175 bit, and
one-sided 99% lower bound -0.011820853637039925. Conservative four-decimal
flooring gives `MSG_LO=-0.0119`. S217's aggregate/receipt SHA-256 values are
`855af8ec8827d2bb643ba969ae158cb3ee80455e2a7e67c74083b2bd7e86ab38` / `0ec278be335e0d717af8237b1cd3dd4860112d7ece596d4f9ed9f7ebace0ff65`. This updates only H8's already
defined message-side input; it does not prove the inherited deep state
invariance.

The public proof carried two stale, non-scoring displays: its Section 5 table
predated the executable ledger, and two memory sentences named 166,838,272
while displaying the exponent of 160,546,816. This derivative repairs those
displays against the embedded executable. No score credit is taken for the
repairs. The source differs from the public source in the `MSG_LO` literal and the real stopped-path step-3b schedule and has SHA-256 `682ae7757542edfdd4a4252486da2967f43cc5e38db8e7a271e6df3b096d6cf8` (this is the current combined source after Appendix AH; the `-0.0119` charge described above is the prior filing's and is tightened to `-0.011821` in Appendix AH).

Exact executable recomputation gives:

```text
N_CV  = 1589119332517172204510
N_E   = 1445295614
V_CV  = 288613240907355274018833825
V_MAX = 288613347576423778507775899
ALLOW = 9435509593702435651584
OVER  = 775008730887
FIN   = 16795184
N = 288622783086018255968953554
time_log2 = 76.4856877247366669571575847865057377321448186581597223531843796296926901888382766694401086...
```

The time claim is rounded upward to 76.48569. Charged memory remains the
counted phase maximum 160,546,816 bytes, whose exponent is 27.25841881259883225150829083778099179961588870454342322935194028013630206632286682899131097482861621...,
rounded upward to 27.258419. The organizer rounded-field scalar is therefore
`76.48569 + 27.258419 - 20 = 83.744109`, an exact 0.051990-bit rounded-field improvement
over the direct public parent and 0.011860 bit below h8d. The unrounded scalar is 83.744106537335499208665875624286729531760707362703145582536319909828992255161143498431420.... The existing
lean-witness work gives no further memory credit: the parent already charges
160,546,816, above its measured 160,505,856 resident peak and below neither a
larger competing procedure phase nor a recorder cell used by this schedule.

## Appendix AC. Real early-stopping step 3b

The only algorithmic change after h8b is the step-3b schedule.  Both candidate
paths are constructed through row 15; rows 16 through 21 are extended and
tested one at a time, returning on the first failure.  Rows 22 through 37 are
constructed only after all six early rows pass.  On 4,096 deterministic random
inputs the old and new routines return identical booleans and message words and
their counted work agrees; stopped paths cost 607..652 operations in this
replay.  The P8 all-pass witness still costs exactly 3,014 operations and is a
collision.  Replacing the module's complete `trace` helper with a hard failure
does not affect the new step-3b path.  These tests prove implementation
equivalence on their finite domain; the 842.361097 expectation remains H3B's
declared table-transfer premise.

Exact recomputation gives N=288622783086018255968953554 and
log2(N/2728)=76.4856877247366669571..., rounded upward to 76.48569.  Memory is
unchanged at 27.258419, so the organizer rounded-field scalar is 83.744109.
The deterministic maximum remains 775008730887; no cap or success term changes.

## Appendix AD. GoForceX PR-1560 epoch/cap correction

This derivative credits GoForceX submission
`1b9a559e-08d7-4457-b294-afc9c12f4d7c` (public PR 1560). Relative to
`1753d8ed`, that entry's two material executable changes are the epoch length
`KEP_EPOCH=32 -> 40` and the deterministic cap slack
`eps_log2=16 -> 20`. Applied after h8c's H8 rebase and genuine stopped-path
step 3b, both changes are lossless: the construction, table geometry,
probability inputs, memory, H3B mean, all-pass 3,014-operation path and exact
`vmax=775008730887` are unchanged. The complete embedded selftest passes.

The number of epochs becomes 1,445,295,614. The tighter cap gives
`V_CV=288613240907355274018833825` and
`V_MAX=288613347576423778507775899`; its Bernstein exponent is still
169.34769..., far beyond the reserved 2^-60 failure margin. Exact total work
is `N=288622783086018255968953554`, so
`log2(N/2728)=76.4856877247366669571...`, rounded upward to 76.48569.
Memory remains 27.258419 and the organizer rounded-field scalar is 83.744109.
This is 0.000150 below h8c at the rounded-field level and 0.049180 below the
credited GoForceX entry's 83.809479. No new heuristic premise is introduced.


## Appendix AE. GoForceX 6c6ee7a2 exhaustive-density F7 bounds

This derivative directly credits public GoForceX submission
`6c6ee7a2-b1b9-4fd4-9347-07da87713b54`, commit
`b0867020fb3faeaa22601f22e2aefc04cffe6b59`. Its executable diff from
`1b9a559e` changes exactly three constants: `F7R 0.11985 -> 0.1205926`,
`F7R_HI 0.12136 -> 0.1206112`, and diagnostic `F7C_MEAN 0.1206148 ->
0.1206019`. The class, all acceptance predicates and every other executable
line are unchanged. The new bounds come from the public parent's
exhaustive-density Rao-Blackwell estimator described in Section 3.8; this
filing adopts that evidence and introduces no additional premise.

Applied after h8d's pooled H8, stopped-path step 3b, epoch-40 and tighter-cap
changes, the exact source SHA-256 is `682ae7757542edfdd4a4252486da2967f43cc5e38db8e7a271e6df3b096d6cf8` (current combined source after Appendix AH; the ledger values below are the prior filing's and are recomputed in Appendix AH). Its full self-test
passes. Exact ledger values are `N_CV=1589119332517172204510`,
`N_E=1445295614`, `V_CV=288613240907355274018833825`,
`V_MAX=288613347576423778507775899`, `vmax=775008730887`, and Bernstein
exponent 169.34769.... Total work is `N=288622783086018255968953554`, so
`log2(N/2728)=76.4856877247366669571575847865057377321448186581597223531843796296926901888382766694401086...`, rounded upward to 76.48569. Memory remains
27.258419 and the organizer rounded-field scalar is **83.744109**, which is
0.051990 below the direct public parent's 83.800429 and 0.011860 below h8d at
the organizer's rounded-field level.

## Appendix AF. S217 frozen unique-pool H8 extension

S217 was preregistered as the full unique-seed pool 101 through 168 and then
run to completion: 1,700,000,000 pairs per side, SEL profile 257,983 and W9
profile 258,427. Its point log2 ratio is -0.0024808069401957883, standard
error 0.004014896826580175 bit and one-sided 99% lower bound
-0.011820853637039925. Conservative four-decimal flooring therefore gives
`MSG_LO=-0.0119`. The final aggregate and run-receipt SHA-256 values are
`855af8ec8827d2bb643ba969ae158cb3ee80455e2a7e67c74083b2bd7e86ab38` and
`0ec278be335e0d717af8237b1cd3dd4860112d7ece596d4f9ed9f7ebace0ff65`.
Seeds are counted once; no adaptive stopping point is selected.

Only the message-side lower-bound literal changes from h8e. The construction,
H8 state-transfer premise, H9 class law, F7 bounds, memory, operation prices,
epoch/cap law, deterministic maximum and success target are unchanged. The
exact source SHA-256 is `c3046b701513e9db19c3af4f788c20108217911de004611563fd7c379fde4053` and its full selftest passes. Exact
ledger values are `N_CV=1593854405453391485939`, `N_E=1449602138`,
`V_CV=289481060181078127087822198`,
`V_MAX=289481167168036539210036698`, and `N=289490602677631016671214353`. Hence
`log2(N/2728)=76.4900190548613271824282033457145649958966787239025355405367473572277633467173113267132965637226087451023928162143037214957430165063094700443049804987097495807794638406154090147295...`, rounded upward to 76.49002. Memory remains
27.258419 and the organizer rounded-field scalar is **83.748439**: 0.002900
below h8e, 0.011860 below h8d, and 0.051990 below the credited public parent
at rounded-field precision.


## Appendix AG. Fixed-alignment GoForceX stack (9cdbd3c1)

Public submissions `6c6ee7a2-b1b9-4fd4-9347-07da87713b54` and
`9cdbd3c1-1094-47fb-b0f7-752a25d9c032` differ in 23 executable source lines.
The transform in `research/rivals/price_db38_h8g_freeze.py` reproduces the
public new source byte-for-byte before applying it to h8f. It fixes the
alignment to R*=8174, preserves one discarded random word in every seeded
control, adds E_SEL=29,706,161, and uses E_SEL on both sides of the ledger and
in the exact build charge.

Truth repair: R*=8174 is **not** the census argmax; r=8150 has 29,708,804
entries. R*=8174 is the highest-retained alignment among the four tables
directly measured by H1W and has E=29,706,161. Executable comments and this
proof use the accurate description.

The score improvement is conditional on one changed premise: H7 now transfers
acceptance/retention independence to this fixed alignment, whereas h8f used an
average over uniform alignments. If that strengthening is declined, the exact
fallback is h8f at 83.748439. H3B's stopped-path charge and S217's
`MSG_LO=-0.0119` are orthogonal and unchanged.

The combined exact source SHA-256 is `682ae7757542edfdd4a4252486da2967f43cc5e38db8e7a271e6df3b096d6cf8` (current combined source after Appendix AH; the ledger values below are the prior filing's and are recomputed in Appendix AH). Exact ledger:
`N_CV=1589119332517172204510`, `N_E=1445295614`,
`build=73804325891`, `V_CV=288613240907355274018833825`,
`V_MAX=288613347576423778507775899`, and `N=288622783086018255968953554`.
Thus `log2(N/2728)=76.4856877247366669571575847865057377321448186581597223531843796296926901888382766694401086...`, rounded upward to **76.48569**.
Memory remains 27.258419, and the rounded-field scalar is **83.744109**.

## Appendix AH. Current numerical tightenings (H8 six-decimal charge and H1W walk mean)

This appendix is the current authority for the two numerical charges tightened in this
filing. It supersedes the four-decimal H8 floor `MSG_LO=-0.0119` used in Appendices
AB-AG and the round H1W charge `6.770000` used there and in their quoted ledger rows.
The two executable changes in the source of Appendix X13 are `MSG_LO='-0.011821'`
and `WALK_MEAN=D('6.760092')`; geometry, table, memory, success target, class,
selection, heuristics and every other charged term are unchanged.

**H8 charge.** The S217 unique-seed panel's measured one-sided 99% lower bound on
the message-side log2 factor is `-0.011820853637039925` (point
`-0.0024808069401957883`, SE `0.004014896826580175`; 1,700,000,000 pairs per side,
seeds 101..168 counted once). The prior filing floored that bound to `-0.0119`,
which is more conservative by `0.000079146...` bit but is not the tightest
justified bound. This filing charges `-0.011821`, which is still below the exact
lower bound (by `0.000000146...` bit). No new measurement, probability premise or
extrapolation is introduced; the panel, its registration and its receipt hashes are
those recorded in Appendix AF.

**H1W charge.** The H1W panel's four complete-table means are 6.739121, 6.737195,
6.750949 and 6.738023 with standard error about 0.0040; the largest one-sided 99%
upper bound is 6.760092. The prior filing charged the round value 6.770000, which
is conservative by 0.009908. This filing charges 6.760092. The resulting per-C1-claw
cost, per_a0 and wbar are `24.3958866956861381048...`, `10.914650...` and
`181595.727...`; the deterministic 18/read maximum and the 3,014-operation step-3b
path are unchanged. No new measurement, probability premise or extrapolation is
introduced; the four-table panel is the evidence retained in Appendix U.

**Recomputed ledger.** With the same `build`, `vmax`, allowances and `K=2^40`, the
exact integers are:

```text
N_CV  = 1589032316906413946599
N_E   = 1445216474
V_CV  = 288561754736423708970454854
V_MAX = 288561861399651339108383188
ALLOW = 9435509593702435651584
OVER  = 775008730887
FIN   = 16795184
N     = 288571296909245816569560843
```

The exact time is
`log2(N/2728)=76.4854303456169727730405314062844012983154159165417187600564715761420796424784767420679591662195313606940914225006956271...`,
rounded upward at five decimals to **76.48544**. Memory remains the counted phase
maximum 160,546,816 bytes, `memory_log2_bytes=27.258419`. The organizer rounded-field
scalar is `76.48544 + 27.258419 - 20 = 83.743859`; the exact unrounded scalar is
`83.743849158215805024548822244065393097931304621085141989408411856278381708801343571059270141048...`.

**Verification.** The exact embedded source (59,512 characters) has SHA-256
`2ca106e5647efbceaa079b2add7a75fc8edd043fc0e08943286204b84f80ed62`.
`selftest` passes with the same 2,304 tag lane checks, 16,128 combined tag/C1 lane
checks (568 firing), bitslice maximum/bound 218 and success lower bound `>= 0.39`;
`ledger` reconstructs every integer above. These are deterministic mechanical checks,
not a measurement of the rare full event.

**Boundary.** The state-side H8 premise, H1/H1W, H2-P1/H2b, H3-P1, H4a-c,
H6/H6D/H6E, H7, H9 and R6D determinism remain exactly as declared. This appendix
states resource bounds only; it is not a mathematical proof, a qualified baseline or
human acceptance.

## Appendix ZS. Eight-column restriction and the counted phase maximum

**Claim.** Restrict the parent layout to **eight relative columns 0 through 7** (coverage 64, probe limit 69) and reschedule the inherited preprocessing as follows. (i) Phase E releases the tail list clause by clause as the record is written, so its bounded figure is the model part 85,323,392 plus procedure code 1,912,832 and recorder overhead 2,097,152, i.e. **89,333,376 bytes**; the 18,997,248-byte record is charged as the alternative endpoint of that coexistence maximum, exactly as the parent Appendix Z charged it. (ii) Phases R, S and D drop the kernel-state and launcher rows, which Appendix Z already established as kernel-side and exec-replaced for phase E. (iii) The recorded tail-clause list is released after phase R pass 1: pass 1 regenerates the clause stream into SHA-256 only and compares it with the recorded digest, and pass 2 streams the regenerated stream into the solver, so the record-clause bytes never coexist with the solver peak and are charged once, in phase E. Phase R is then **136,433,664 bytes** (parent 157,474,816 less 4,194,304 + 4,194,304 and less the 18,997,248 record), phase S 95,485,952 and phase D 106,987,520. The counted phase maximum is phase R, **136,433,664**, which the eight-column online image 127,926,304 lies 8,507,360 below. memory_log2_bytes is **27.02363** and the organizer rounded-field scalar is 76.52419 + 27.02363 - 20 = **83.54782**. No probability premise, success budget, pricing lemma or online operation count of the parent changes.

### ZS.1 Geometry and pricing at eight columns

Coverage is 64 residues per 2^13 frame, buckets are (column c, row) with c in 0..7, and the record, lane, mask and tree layout are the parent layout. A window probes with probability 2*69/8192 = 138/8192; over the 69 probing values there are 1280 main-read positions, 700 next-read positions and 100 frame-crossing reads, so reads/probe = 2080/69 and probe cost = 14+12+19*2+7*(2080/69) = 18976/69. Per_a0 = 235/256 + (138/8192)*(41+18976/69) + (20*E/2^32)*per_C1 = 8.94191160597174093786557199060916900634765625 with E = 23,771,164, and wbar = C+25+2^-6*(70+1024+2^20*per_a0) = 149,274.373502241003525989531494140625. The 218-operation front end, the Lemma B double-prime / C1 / C2 / G / F7 chain, the H1W walk charge 6.760092, the H3B stopped-path mean 842.361097 and the 3,014-operation deterministic path are unchanged, and the bucket law of Appendix U applies to every bucket of the narrower table because each bucket still receives the same eight candidate positions and keeps the same first six.

### ZS.2 Census row for coverage 64

The recorded eight offset arrays of the parent packet (section 3.1 and Appendix AA; 8 x 1024 counts, the instrument the parent re-executed) give the retained count of a width-k window at alignment r = 8m+j as the cyclic window sum on offset array j. Recomputing the parent width-10 row from those arrays reproduces minimum 29,617,909, maximum 29,708,804 and sum 242,952,259,320 exactly, which calibrates the reduction. The width-8 row is **minimum 23,694,709, maximum 23,773,042, sum 194,361,807,456** over the 8,192 rotations, satisfying the mean law 15*194,361,807,456 = 8*364,428,388,980. The fixed alignment **R* = 8174** (inherited before outcomes) has **E(8174,8) = 23,771,164**, and every epoch table of this construction has that retained count.

### ZS.3 Ledger and replay

The exact ledger of Appendix A is N_CV = 1,985,730,719,901,168,031,200 first blocks, 1,806,011,569 epochs, V_CV = 296,418,991,844,310,695,027,883,684, V_MAX = 296,419,124,850,616,334,451,240,566, ALLOW = 9,435,509,593,702,435,651,584, OVER = 775,008,730,887, FIN = 16,795,184, N = 296,428,560,360,210,811,912,418,221 and time_log2 = 76.5241869934677090..., charged 76.52419. The build cost is 73,646,430,578 with E = 23,771,164, and the epoch length, cap lemma, success budget and second-order terms are the parent ones. The shipped source of Appendix X13 is the parent source with NCOL=8, a CENSUS8 entry carrying the ZS.2 row, E_SEL=23,771,164 and the ZS charge 136,433,664; its SHA-256 is 8f3fb2bdb7bc074cd562f0d36cbd2ae0a723a0ada512ec1cb8a0ea36157c7fba. No other source line changes, and no probability or allowance premise is added.
### ZS.4 Schedule descriptor charged in phase R

The two regeneration passes consume the recorded covers, model arguments, V, C and the recorded digest, not the recorded tail-clause bytes. That schedule descriptor is retained in memory as an explicit 1,048,576-byte row of phase R, and the 18,997,248-byte clause record is released after pass 1. Phase R is therefore 157,474,816 - 4,194,304 - 4,194,304 - 18,997,248 + 1,048,576 = **131,137,536 bytes**, which remains the counted phase maximum: the eight-column online image 127,926,304 lies 8,507,360 below it, and phase E 89,333,376, phase S 95,485,952 and phase D 106,987,520 are lower. memory_log2_bytes is **27.02363**, the upward rounding of log2(136433664)=27.0236291570188016337..., and the organizer rounded-field scalar is 76.52419 + 27.02363 - 20 = **83.54782**. Passing the clause record itself through pass 2 instead would charge 18,997,248 more (phase R 149,086,208), which this filing does not claim and does not need.

### ZS.5 The counted phase maximum is the gmass development cell

The procedural phases of this filing are phase R 131,137,536, phase E 89,333,376, phase S 95,485,952, phase D 106,987,520 and the eight-column online image 127,926,304. All are below the inherited gmass development/preprocessing cell, which Section 10 reports as 133,236 KiB = **136,433,664 bytes** and which the charge must include: the counted phase maximum is 136,433,664, the eight-column image lies 8,507,360 below it, and memory_log2_bytes is **27.02363** (upward rounding of log2(136433664)=27.0236291570188016337...). The organizer rounded-field scalar is 76.52419 + 27.02363 - 20 = **83.54782**. Charging the gmass cell changes nothing else: no probability premise, success budget, pricing lemma or online operation count changes.

### ZS.6 Nonuniform advice

The non-uniform advice of this procedure is the SEL bitmap (2^16 bits, 8,192 bytes) together with the transcribed P8 data: the condition list, the class descriptors, and the PCV, PMX and PMY constants. It is bounded by 2^17 = 131,072 bytes, which is inside the charged 2,097,152-byte code/state allowance of the online phase and adds no score-critical memory term; the counted phase maximum remains 136,433,664 bytes (the gmass preprocessing cell) and memory_log2_bytes 27.02363.
