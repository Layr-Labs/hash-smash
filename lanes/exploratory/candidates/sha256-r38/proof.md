# sha256-r38: the P8 two-block bound with the P1 sum-claw on a 2^27-candidate a0 set in a seven-lane bucket table (time_log2 83.01264, memory 2^28.00811, score 91.02075)

This is a cost bound for the target sha256-r38-prefix-v1. It is a credited derivative of:
- Jbenisek's e4243e7a: the P1 sum-claw, its post-filter chain, step 3b, the counted pricing, the registered rate q3_model and the form of H3-P1;
- newjordan's 711c4bf8: all 2^32 scan words per chaining value;
- 0xplemonade's a32131ff: the online memory cell is a measured full-table execution;
- 377cb363: the capped Step-1 memory measurement;
- 0xplemonade's b561f523 and its predecessor e6a33086: a table of seven-entry buckets with exact tags, the observation that all 20 row-16 heads are equal modulo 2^13 (so one w per scan word and constant bucket deltas between heads), and the pairing of a head's two windows with buckets b and b + 2.

Our own work:
- The characteristic P8, its semi-free-start pair and its accepted event are our own (1a695f0b).
- Our previous filing of this line, with the 2^27-candidate residue table, is b79d2f6c-f3cd-4e8d-bc7b-8e2f582ee376.
- The program `experiments/p1b38.py` is our own code, standard library only. It transcribes P8's printed cells as data and executes no code of another participant.

**What is new against b561f523.**
- **Candidates and occupancy.** We use the 2^27 candidates of the set P, the best class of our exact C1 C2 G count (Section 6: 2^-12.2765, against 2^-12.2857 for b561f523's R = 9). With 2^23 buckets of 7 lanes, a bucket receives 16 candidates on average, so the buckets are 99.916% full: 2.18566 claws per scan word, against 1.98008.
- **Bucket layout.** One 256-bit word per bucket holds 7 lanes of (9-bit tag, 27-bit offset) and a 3-bit count. That is 2^28 bytes of table, with no separate payload words.
- **Scan.** One SWAR pass tests the 14 tags of a head's two windows; its fields have headroom, so no guard bits are stored.
- **Our own measurements.** Exact window counts, a registered paired q3 measurement of the P1 family on P, a full-scan link count with its group bound (Section 8), a full-size C-port panel with step 3b on every good pair, and a measured memory peak.

Claim: time_log2 = 83.01264.
- **Time.** N = 26,615,677,263,635,467,762,332,733,907 counted word operations, which is 2^83.01264 target compressions of C = 2,728 operations each. The online work is charged at its hard cap V_MAX.
- **Success probability** at least 0.39.
- **Memory** 2^28.00811 bytes: the measured peak of our full-table execution of the online program (Section 10).
- **Preprocessing** 2^78.09276 (the allowances, inside the time).
- **Score** under hashsmash-scalar-tm-v1: 83.01264 + 8.00811 = 91.02075.

`python3 experiments/p1b38.py ledger` prints Sections 5 to 7, and `python3 experiments/p1b38.py selftest` runs the checks of Section 12.

## 1. Target and output

SHA-256 steps 0..37 are applied to every padded block, with the standard IV once, FIPS 180-4 padding, feed-forward and all eight digest words. The procedure outputs two 128-byte messages m = M0||M1 and m' = M0||M1' with a common first block M0. FIPS padding appends the same third block to both.

**Lemma 2 (output).**
- *Statement.* Let cv = F_38(IV, M0). If the second-block computations of M1 and M1' from cv end with equal A34..A37 and E34..E37, then m and m' have equal digests.
- *Proof.* The second-block output is cv + (A37, A36, A35, A34, E37, E36, E35, E34), and the third block is common. The messages are distinct because W7 differs (W7y - W7x = D7 = 0x20000000 for every pair the procedure builds, Section 2).

Step 3b accepts only pairs whose A34..A37, E34..E37 are equal, so every output is a collision of the target.

## 2. Data, the P1 pair and row 16

- **P8 (1a695f0b, our characteristic; transcribed as data).**
  - The 38-step semi-free-start pair (PCV, PMX, PMY).
  - The printed cells of rows 7..22 (`_ROWS`): for A, E and W, the mask of fixed bits, their values and the XOR difference.
  - The printed '+' pairs (`PQE`) without the row-18 relation E18 = E17, as in e4243e7a.
  - The 35 two-bit conditions of rows 16..21 (`X2`).
  - S denotes A2..A15 and E6..E15 of both members.
  - `selftest` item 1 checks that the pair reproduces (outputs equal, the accepted event holds) and that step 3b accepts it.
- **The P1 pair.**
  - For a chaining value cv and two free words a0, a1, both members take A0 = a0, A1 = a1, and A2..A15, E6..E15 from S.
  - E0..E5 and W0..W15 then follow from the step equations (`pair_words`).
  - W10..W15 are S's words. W0..W6 and E0..E5 are equal in the two members.
  - W7y - W7x = D7 and W9y - W9x = D9 hold for every (cv, a0, a1); `selftest` item 3 checks this on 300 random triples.
- **Lemma 1 (row 16).**
  - *Statement.* With u := W1 and F(a0) := CC2 + a0 + k0(cv) + h(a0, cv), E16 of member x is **E16x = F(a0) + s0(u) - u**.
  - *Ingredients.* W16 = s1(W14) + W9 + s0(W1) + W0, with W9 = cW9 - a1 and W0 = a0 + k0(cv).
  - Steps 0 and 1 give W1 = a1 + h(a0, cv).
  - CC2 = 0x7af32e15 depends on S only; k0 and h are written out in `cvc` and `Ffun`.
  - Checked by `selftest` item 3 against the real 17-step trace.
  - Inversely, a1 = u - F(a0) + CC2 + k0 + a0.
- **S160.** These are the 160 words that pass every row-16 cell and condition of P8: 20 heads (`HEADS`) times the 8 values of bits 0, 2 and 10.
  - `selftest` item 2 checks the row-16 tests on S160, on 20,000 random words and on the 1,280 one-bit neighbours of 40 elements: a word passes iff it is in S160.
  - A **claw** is a pair (a0, u) with F(a0) + s0(u) - u in S160. Every claw is a row-16 pass.
- **Post-filters**, on the words of the two members, in order:
  - C1: W8y - W8x = D8, tested as E5 = a1 + C5 having bits 29..31 equal to 101;
  - C2: s0(W9y) - s0(W9x) = T9;
  - G: s0(W8y) - s0(W8x) = T8;
  - F7: s0(W7y) - s0(W7x) = T7.

  C1 and C2 read a1 only, G reads (a0, a1), and F7 reads (a0, a1, cv). A **good pair** is a claw that passes all four. The counted chain (`postfilters`) equals the definitions evaluated on the real words (`pf_ref`): 0 mismatches on 60,000 pairs in `selftest` item 4, and on every claw of the organizer experiment `p1b-online-r38`.
- **The a0 set P.**
  - P = {a0 : bits 25..27 of a0 are 010 and bits 30..31 are 00}, which is 2^27 words.
  - The offset map is p(o) = (o mod 2^25) | (2 << 25) | ((o >> 25) << 28), for o < 2^27.
  - P is the union of the four 2^25-windows k = 2, 10, 18 and 26 (k = a0 >> 25), all in the best class of Section 6.

## 3. The procedure (fixed caps)

```text
input: N_CV, V_MAX; data: Section 2.   V := 0 (a register: the online operations executed so far)
for j = 1 .. N_CV:
    if V > V_MAX: halt (failure)
    draw M0 (two random 256-bit words, 16 fields); cv := F_38(IV, M0); the claw scalars of cv; u0 := a random word; R := a random 27-bit word
    V += C + 76 + (2^23 + 3) x 5 + 2^27 x 57 + 42 + 2^32 x 369      (this chaining value's fixed work; Section 5)
    table: RAM words 0 .. 2^23 + 2 (256 bits each) set to 0; bucket b is word b (words 2^23 .. 2^23 + 2 mirror buckets 0, 1, 2)
    for n = 0 .. 2^27 - 1:  o := rotr2((n + R) mod 2^27); a0 := p(o); F := F(a0); b := F >> 9; c := count(T[b])
        if c < 7: lane c of T[b] := (F mod 512, o); count(T[b]) := c + 1; if b < 3: T[2^23 + b] := T[b]
    for n = 0 .. 2^32 - 1:  u := u0 + n mod 2^32;  P := s0(u) - u
        W0 := H0 - P;  w := W0 mod 512;  b0 := W0 >> 9;  C := K512 - (w in the 14 fields)        (the 20 heads are equal mod 2^13)
        if w >= 507: V += 301                                               (straddle: targets may lie in buckets b + 1, b + 3)
        for each head h:  b := b0 + DH[h] mod 2^23
            v := (T[b] AND TM0) OR ((T[b + 2] << 11) AND TM1);  r := v + C;  y := (r XOR X200) AND M3FA
            if a field of y is 0 (((y OR G10) - L0) AND G10 != G10):  V += 1;  MATCHES(T[b], T[b + 2], b, 0)
            if w >= 507: the same with T[b + 1], T[b + 3] and y := r AND M3FA;  MATCHES(T[b + 1], T[b + 3], b, 1)
    MATCHES(wa, wb, b, s): for every zero field (lowest first), lane i, field f:  V += 44;  e := lane i of (f ? wb : wa)
        if that word's count < 7:  V += 2;  skip the field if i >= count
        a0 := p(e.offset);  F := ((b + 2f + s mod 2^23) << 9) | e.tag;  CLAW(a0, u, F)
    CLAW(a0, u, F): a1 := u - F + CC2 + k0 + a0; test C1, C2, G, F7 in turn (V += 7, 22, 29, 30 for each stage reached)
        good pair: STEP 3B (V += its executed operations, at most 3,014); if it accepts: output M0||M1, M0||M1' (W0..W15 of the members); halt
halt (failure)
```

**The table.**
- *Layout.* Bucket b (0 <= b < 2^23) is the 256-bit word T[b]. Lane i < 7 holds bits [36i, 36i + 36): the tag F mod 512 (9 bits) and the 27-bit offset o of a0 = p(o). Bits 252..254 hold the count of lanes in use; lanes are filled in order.
- *Loading.* Candidates are inserted in the order n = 0, 1, ..., with o = rotr2((n + R) mod 2^27), where rotr2(x) = (x >> 2) | ((x mod 4) << 25) and R is a fresh random 27-bit word per chaining value. Every bucket keeps its first 7.
  - The four 2^25-windows of P alternate, so a bucket's first 7 candidates are spread over them.
  - The kept candidates favour small n, that is, offsets just after R. With R uniform, the law of a kept a0 averaged over R is exactly uniform on P, which is the law of the exact counts of Section 6.
  - Without the rotation (R = 0) the kept a0 favour the low half of every window, whose G rate is lower. Our first panel, run that way, measured G|C1C2 = 2^-5.9937 against the uniform 2^-5.9387 (Appendix H.5), and that is why R is drawn.
- *Padding.* Words 2^23 .. 2^23 + 2 mirror buckets 0, 1, 2, so b + 1, b + 2 and b + 3 never wrap.
- *Lookup coordinates.*
  - A target word E16x = H + o, o in {0, 1, 4, 5, 1024, 1025, 1028, 1029}, means F = W + o with W = H - P.
  - All 20 heads have the same low 13 bits (0x1320), so w = W mod 512 is the same for every head, and head h's bucket is b0 + DH[h] with DH[h] = (H_h - H_0) >> 9, a multiple of 16.
  - The window W + 1024 is bucket b + 2 with the same w.

**Lemma B (the table test is exact).**
- *Statement.* For a scan word u, MATCHES is called exactly on the stored entries (a0, F) with F(a0) + s0(u) - u in S160, each once.
- *Proof, in-bucket targets.* A target F = W + o (o in {0, 1, 4, 5}) lies in bucket b with tag w + o when w + o <= 511, and in bucket b + 1 with tag w + o - 512 otherwise, which needs w >= 507.
  - For a lane with tag t, the field value r = t + 512 - w lies in [1, 1023], so the addition and subtraction never cross a field.
  - In the normal pass, ((r XOR 0x200) AND 0x3fa) = 0 iff r - 512 is in {0, 1, 4, 5}, i.e. t - w is in {0, 1, 4, 5}: exactly the targets in bucket b.
  - In the straddle pass, (r AND 0x3fa) = 0 iff r is in {0, 1, 4, 5}, i.e. t = w + r - 512: exactly the targets in bucket b + 1.
  - The same holds for the second window with b + 2 and b + 3.
- *Proof, zero test.* In ((y OR G10) - L0) AND G10, bit 10 of a field (above y's 10 bits, so no borrow leaves the field) is cleared iff the field of y is 0.
- *Proof, lanes and duplicates.* Lanes at or beyond the count are empty (zero) and are rejected by the count test. Tags are exact (bucket and tag give all 32 bits of F), so no other lane matches. Two stored entries with equal F give two claws, with different a0.
- *Checks.*
  - `selftest` item 5 compares the SWAR test with the direct predicate on 4,000 random word pairs in both passes.
  - The claws equal an independent sorted search over the stored entries (with multiplicity) at 2^17 candidates (`selftest`, `p1b-online-r38`).
  - At full size, our C port gives 572,423 claws on chaining value 24 over 2^18 scan words, equal to the reference (Appendix H).

**Step 3b** (`step3b`) runs on a good pair.
- It runs Step 2 of both members (E0..E5, W0..W9), then rows 16..37 of both members.
- After each of rows 16..21 the tests of that row run: the cells of A, E and W (values on the fixed bits, XOR difference on all bits), the '+' pair of `PQE`, and every two-bit condition closing at that row. The first failing test stops step 3b.
- If rows 16..21 pass, the eight output words are compared. Step 3b accepts iff they are equal, so by Lemma 2 every accepted pair is a collision.
- Its counted operations are at most 3,014. That is its longest path, where every test runs; it is counted on the P8 pair, which takes that path.

**Distinct scan words.**
- u runs over u0, u0 + 1, ..., u0 + 2^32 - 1, which is all 2^32 words, each once.
- At one u, a stored a0 matches at most one target, and a1 = u - F + CC2 + k0 + a0. So the claws of one chaining value are distinct pairs (a0, a1).
- The organizer experiment reports `distinct_pairs` = `claws` on every trial.

The procedure draws only its own N_CV first blocks. Each costs one compression plus the 76 operations of cv_begin, inside the fixed part of every chaining value and hence inside V_MAX.

## 4. Pricing (H5')

The cost model is collision-frontier-v5 on the 256-bit word RAM, with the unit costs of fb176310:

| operation | cost |
|---|---|
| load, store, add, sub, and, or, xor, not, shift, immediate, random word | 1 |
| compare-and-branch | 2 |
| S0, S1, s0, s1 | 8 |
| CH | 3 |
| MAJ | 4 |
| one target compression C | 2,728 |

- **Table access.** A bucket is one 256-bit word, and the table occupies RAM words 0 .. 2^23 + 2, so bucket b is word b. Reading bucket b is one load; reading b + 2 is an add and a load. There is no lane extraction on the scan path.
- **Registers.** The masks TM0, TM1, M3FA, G10, L0, K512 = X200, the field value C, the 20 deltas DH[h] and the table bases are kept in registers.
- **Counter.** Every work-counter add V += k is one operation and is counted.
- **Counted pieces of a chaining value** (`COST` in the program):
  - cv_begin 76: first-block words 30, claw scalars 38, u0 1, R 1, V add 1, cap test 2, loop 3.
  - Reset 5 per table word (2^23 + 3 words): store, address add, loop 3.
  - Build 57 per candidate (on the inserting path; a full bucket skips 12): (n + R) mod 2^27 2, offset rotr2 4, a0 map 5, F 26, bucket b = F >> 9 1, load 1, count 1, count test 2, lane shift 36c 3, entry 3, shift 1, or 1, count + 1 1, store 1, padding test 2, loop 3.
  - Padding copies: at most 21 per chaining value, 2 each.
  - Scan word 13: u0 + n 1, s0 8, sub 1, loop 3.
  - Per scan word 16: W0 1, w 1, b0 1 (and 1 spare), the 14-field broadcast of w and C = K512 - broadcast 10, straddle test 2.
  - Head 17: bucket b = (b0 + DH[h]) & (2^23 - 1) 2, load b 1, address b + 2 and load 2, combine the two tag sets 4, r 1, y 2, zero test 3, compare-and-branch 2.
  - Straddling scan word 301: per head two loads 4, combine 4, r 1, y 1, zero test 3, branch 2; V add 1.
  - Match event 1.
  - Matching field 44: locate the lowest zero field by halving (three levels of and, branch, shift, add, then the field) 18; word select, entry, tag, offset 5; full-bucket test 3; a0 map 5; F from bucket and tag 5; a1 3; clear the bit and loop 4; V add 1.
  - Lane-count test in a bucket that is not full 2.
  - Post-filter stages 7, 22, 29, 30.
  - Step 3b at its executed count.
- **Implementation.** `run_cv` charges these through the counter `Mach`. `selftest` item 5 compares the counted run with the model mean at that size (ratio 1.0016).

## 5. The exact ledger

The ledger is an exact count read from the code (`model`, `ledger`). It does not rest on any measured operation count.

**Fixed, per chaining value:** C + 76 + (2^23 + 3) x 5 + 2^27 x 57 + 21 x 2 = 7,692,356,397 operations, plus 369 per scan word.

**Bucket fill.** A bucket's load is X ~ Binomial(2^27, 2^-23), with mean 16. Its stored lanes are min(X, 7), with E[min(X, 7)] = 6.994098 computed exactly (`binom_min7`); the empty lanes average 0.005902 per bucket.

**Per scan word** (expectations under H1):
- **Fixed part.** 13 + 16 + 20 x 17 = 369.
- **Straddle.** (5/512) x 301 = 2.9395, since w is uniform.
- **Claws.** 160 x 6.994098 / 512 = 2.185656. Each target word is held by a stored lane with probability (stored lanes)/512.
- **Spurious matches** of empty lanes: 160 x 0.005902 / 512 = 0.001844. An empty lane (tag 0) matches only when w = 0 in the normal pass, or when w is in {507, 508, 511} in the straddle pass.
- **Matches** (claws and spurious): (2.185656 + 0.001844) x (1 + 44 + 2) = 102.8125, charging the event and the count test to every match.
- **Post-filters and step 3b.** Per claw 7 + 22/8 + 29 P(C1 C2) + 30 P(C1 C2 G) = 10.1146, plus q_pf x 3,014 per claw: 2.185656 x (10.1146 + q_pf x 3,014) = 22.1958.

| quantity | value |
|---|---|
| per u: 369 + 2.9395 + 102.8125 + 22.1958 | 496.9477 |
| scan, straddles and matches per claw, (369 + 2.9395 + 102.8125) / 2.185656 | 217.212 |
| post-filters and step 3b per claw | 10.155 |
| table reset and build per claw | 0.819 |
| operations per claw | 228.187 |
| claws per good pair, 1 / q_pf | 74,167 |
| wbar = fixed + 2^32 x 496.9477, mean online work of one chaining value | 2.142067e12 |
| vmax = fixed + 2^32 x 1,763,590, maximum online work of one chaining value | 7,574,569,065,909,037 |
| N_CV (Section 7) | 12,014,587,405,061,634 |

**The per-scan-word maximum, 1,763,590**, assumes the word straddles, there is a match event in each of the 40 passes, and all 28 fields of every head match in a bucket that is not full, each match reaching step 3b:

  369 + 301 + 40 + 560 x (44 + 2 + 88 + 3,014) = 1,763,590.

The means use H1 (bucket loads, uniform tags) and H1-P1 (stage rates). Step 3b is charged at its maximum, so wbar bounds the mean from above.

  V_MAX = ceil((1 + 2^-16) x N_CV x wbar) = 25,736,438,737,648,325,429,509,603,446
  N = (2^78 + 2^74 + 2^70) x C + V_MAX + OVER + FIN = 26,615,677,263,635,467,762,332,733,907,  time_log2 = log2(N / C) = 83.01264.

- OVER = vmax (Lemma 3).
- FIN = 6 C + 1,600: the two 3-block digests of m and m', their assembly and comparison.
- Appendix A lists the terms.

**Lemma 3 (the cap).**
- The cap test reads V at the start of every chaining value. At that moment V equals the online work executed so far: the fixed part is added when the chaining value starts, and each variable segment adds its own cost.
- A chaining value started with V <= V_MAX adds at most vmax.
- Hence the executed online work is at most V_MAX + OVER in every execution.

**Lemma 4 (cap halt).**
- *Setup.* Let W_j be the online work of chaining value j.
  - The W_j are independent: under H1 the chaining values are independent, and u0 is a fresh random word.
  - Each satisfies 0 <= W_j <= vmax and E[W_j] <= wbar.
- *Condition.* The procedure halts at a cap test only if sum_j W_j > V_MAX, that is, only if the sum exceeds its mean bound by t >= 2^-16 N_CV wbar.
- *Bound.* With Var(W_j) <= vmax wbar, Bernstein's inequality gives Pr[cap halt] <= exp(-2^-32 N_CV wbar / (2 vmax (1 + 2^-16/3))) = exp(-395) < 2^-570.
- *Scope.* No variance premise beyond H1 and the deterministic bound vmax is used. A halted procedure outputs nothing.

## 6. The post-filter law q_pf (H1-P1)

Our own exhaustive programs (`gwin38.c` and the C1/C2 enumeration; Appendix R) give these exact counts over all words:

| quantity | count | rate |
|---|---:|---:|
| P(C1) | | 1/8 |
| \|C1 and C2\| over a1 | 53,096,854 | 2^-6.3379 |
| \|F8\| (the W8 values with the G difference) | 68,157,440 | |
| \|F7\| | 287,309,824 | 2^-3.90197 |

The C1 C2 G count over (a0 in a 2^25-window, a1 in C1 and C2) depends on the window k = a0 >> 25 only through k mod 8, with period 8 (Appendix R):

| k mod 8 | count per window | rate over 2^57 |
|---|---:|---:|
| 0 | about 27,917,059,050,000 | 2^-12.3338 |
| 1 | about 28,511,240,000,000 | 2^-12.3034 |
| **2** | **about 29,047,307,908,000** | **2^-12.2765** |
| 3 | | 2^-12.2949 |
| 4 | | 2^-12.3326 |
| 5 | | 2^-12.3358 |
| 6 | | 2^-12.3198 |
| 7 | | 2^-12.3283 |

For reference, the window R = 9 of e4243e7a (2^26 words, k = 18, 19) has rate 2^-12.2857, and all words together have 2^-12.3155.

P takes the four windows k = 2, 10, 18 and 26 of the best class:

| window k | count |
|---|---:|
| 2 | 29,047,307,906,207 |
| 10 | 29,047,307,906,362 |
| 18 | 29,047,307,910,144 |
| 26 | 29,047,307,910,144 |

- **Charged count.** The ledger charges 4 x min = 116,189,231,624,828 over 2^59. This is a lower bound for any mixture of the four windows, since the visible entries need not be exactly uniform over P. P(C1 C2 G) = 2^-12.27653.
- **F7.** F7 has probability |F7|/2^32 for a uniform chaining value, for any law of (a0, a1).
- **Result.** q_pf = 116,189,231,624,828 x 287,309,824 / 2^91 = **2^-16.17850** (e4243e7a's window: 2^-16.1877).
- **H1-P1** is the premise that, over the random chaining value, these rates hold on average for the claws the procedure finds. The claws' a0 are the visible entries, and their a1 = u - F + CC2 + k0 + a0.
- **Support.** Our 64-chaining-value full-size panel (Appendix H) gives:
  - pooled stage rates C1 0.12498, C2|C1 2^-3.3388, G|C1C2 2^-5.9358 (exact over P: 2^-5.9387) and F7|C1C2G 0.06503 (|F7|/2^32 = 0.06689);
  - pooled good pairs per claw 2^-16.2176 against 2^-16.17850;
  - claws against the expected 2^22 x 160 x (stored lanes) / 2^32, with ratio 0.99999.

## 7. Success probability

**Probability space.** All probabilities are over the procedure's own coins: the first blocks M0 (hence, by H1, uniform independent chaining values), the scan starts u0 and the rotations R. The target is fixed. Given its chaining value and R, a chaining value's good pairs and their acceptance by step 3b are determined, because the scan reads all 2^32 words. Every probability below is therefore an average over the random chaining value, never a probability conditional on it.

**Definitions.** For chaining value j:
- X_j is the number of good pairs that step 3b accepts;
- K_j is the number of good pairs;
- L_j is the number of *linked* unordered pairs among them (two good pairs are linked if they share a0 or u);
- for a claw position c = (a0, u), G_c is the event that c is a good pair and A_c the event that it is accepted (A_c implies G_c).

- **H2-P1.** The mean acceptance rate of good pairs, p := E[X_j] / E[K_j] (over the random chaining value), satisfies p >= q3r, where q3r = q3_P1 x 2^32 / 160 = 2^-71.3657 and q3_P1 = q3_model + min(0, D_LB(A0), D_LB(A0sel)) = -96.0438 (log2, Section 9).
  - q3_model = 2^-96.0133 is the registered accepted-event rate of the A0-variant good pairs before row 16; row 16 itself has probability 160/2^32.
  - The two D_LB are our registered one-sided 99% lower bounds of the paired difference between the P1 family on P and, respectively, the A0 family and the selected-variant family on which q3_model was measured.
- **Expectation.** q3r E[K_j] = 2^32 x c x q_pf x q3r, where c = 160 E[min(X, 7)] / 512 = 2.185656 claws per scan word (X ~ Binomial(2^27, 2^-23), the load of a bucket).
- **Within a chaining value (Lemma 5, derived from H2-P1 and H3-P1, Section 8).**
  - *Second moment, H3-P1.* E[X_j(X_j - 1)] is the sum over ordered pairs c != c' of Pr[A_c and A_c'].
    - For unlinked c, c' (no shared a0 or u), H3-P1 states Pr[A_c and A_c'] <= p^2 Pr[G_c and G_c']: over the random chaining value, the acceptance of two unlinked good pairs is not positively correlated.
    - For linked c, c', it uses only Pr[A_c and A_c'] <= Pr[A_c and G_c'], and states that a good pair's acceptance is not positively correlated with its number of linked partners, so the linked part sums to at most p E[2 L_j].
    - Hence E[X_j(X_j - 1)] <= 2 p E[L_j] + p^2 E[K_j(K_j - 1)].
  - *Second-moment bound.* Pr[X_j >= 1] >= E[X_j]^2 / E[X_j^2] (Cauchy-Schwarz), and E[X_j^2] = E[X_j] + E[X_j(X_j - 1)] <= p E[K_j] (1 + 2a + p b), with a = E[L_j]/E[K_j] and b = E[K_j(K_j - 1)]/E[K_j]. Hence Pr[X_j >= 1] >= p E[K_j] / (1 + 2a + p b).
  - *Monotonicity.* x / (1 + 2a + x b) is increasing in x, so replacing p by q3r <= p lowers the bound: Pr[X_j >= 1] >= q3r E[K_j] / (1 + 2a + q3r b) >= q3r E[K_j] (1 - 2a - q3r b). No upper bound on p is needed.
  - *Result.* Section 8 gives 2a + q3r b <= 2 x 0.0049 + 2^-50 < 2^-6.5, so Pr[X_j >= 1] >= (1 - 2^-6.5) q3r E[K_j] = (1 - 2^-6.5) E[X_j], where E[X_j] now denotes the bound of the Expectation line, q3r E[K_j].
- **Across chaining values (H1).** Pr[some X_j >= 1] >= 1 - exp(-N_CV (1 - 2^-6.5) E[X_j]).
- **Bound.** N_CV is the least integer with 1 - exp(-N_CV (1 - 2^-6.5) E[X_j]) - 2^-60 >= 0.39, computed with exponentials at 90 digits: N_CV = 12,014,587,405,061,634.
  - With Lemma 4, Pr[output a collision] >= 0.39 - 2^-570 >= 0.39; the 2^-60 term absorbs the cap halt.
  - `ledger` prints the bound as 0.3900000000000000047332.


## 8. H3-P1: pairwise behaviour of acceptance over the random chaining value

**Statement.** All probabilities are over the procedure's coins, as in Section 7: the random first block, hence by H1 a uniform chaining value, and the rotation R. Write p = E[X_j]/E[K_j] for the mean acceptance rate of good pairs (H2-P1: p >= q3r). Two good pairs of one chaining value are *linked* if they share a0 or u.
- *Unlinked pairs.* For two distinct claw positions c, c' that share neither a0 nor u, the events "c is accepted" and "c' is accepted" are not positively correlated beyond their being good: Pr[A_c and A_c'] <= p^2 Pr[G_c and G_c'].
- *Linked pairs.* Nothing is assumed about a linked pair beyond Pr[A_c and A_c'] <= Pr[A_c and G_c']. A good pair's acceptance is not positively correlated with its number of linked partners: E[sum_c 1[A_c] deg(c)] <= p E[sum_c 1[G_c] deg(c)] = 2 p E[L_j].
- *Why this is a premise and not a theorem.* Acceptance (rows 17..37 of both members and the output comparison) is a function of a good pair's 16 message words, and through them of the chaining value. Two unlinked good pairs have different W0 (a0) and W1 (u), hence different W0..W9 (W10..W15 are S's words for all pairs). The premise models their acceptance, over the random chaining value, as at most independent.
- *What is not assumed.* No probability is conditional on the chaining value or on the set of good pairs. Given those, the outcome is determined (the scan reads all 2^32 words), and the premise does not speak of that conditional law.

**Consequence used** (Lemma 5): E[X_j(X_j - 1)] <= 2 p E[L_j] + p^2 E[K_j(K_j - 1)], hence Pr[X_j >= 1] >= q3r E[K_j] (1 - 2 E[L_j]/E[K_j] - q3r E[K_j^2]/E[K_j]) >= (1 - 2^-6.5) q3r E[K_j].

**The link rate at the full scan is not small, and is charged.**
- Over all 2^32 scan words, every stored a0 has about 160 claws, one per target word, and the table finds every claw of a stored a0 (Lemma B). A good pair (a0, u) therefore has about 159 other claws with the same a0.
- If their post-filter outcomes were independent of its own, about 159 x 2^-16.18 = 2^-8.85 of them would be good.
- They are not independent. A partner's a1' = a1 + (u' - u), and C1 (the top three bits of a1 + C5) and C2 read only a1, so partners at small |u' - u| pass more often.

**The exact full-scan partner count, measured** (Appendix H.3, `partners38.c`, own code).
- *Method.* For every good pair of this package's bucket panel (7,699 good pairs, 64 chaining values), all claws of its a0 over the 2^32 scan words were enumerated: one pass over every u, matching s0(u) - u against the 160 values t - F(a0). Each partner was then tested with the four post-filters.
- *Claws per a0.* Mean 161.10 (min 118, max 217).
- *Good partners sharing a0.* 47 over 7,699 good pairs, 0.006105 per good pair, 2.8 times the independent rate. Every such partner lies at |u' - u| <= 2^28.6.
- *Good pairs sharing a u.* 0 in the panel. All claws at one u lie inside the panel's window, so the window count is the full-scan count; the expectation is 2.19 q_pf = 2^-15.1.
- *Bound.* E[L_j]/E[K_j] is half the mean number of linked partners per good pair. The good pairs of a panel are a size-biased sample (each good pair of a chaining value equally likely), which is the weighting E[L_j]/E[K_j] needs.
  - The one-sided 99% bound with chaining values as clusters (ratio estimator, t(0.99, 63)) gives E[L_j]/E[K_j] <= 0.00405.
  - A Poisson bound with variance inflated by 2 (a linked pair inside the window is counted from both ends) gives 0.00452.
  - The u links add at most 0.00030 (Poisson bound).
  - Our earlier measurement on the residue table's panel (7,789 good pairs of the same set P) gave 51 partners, 0.006548 per good pair.
  - The charged bound: E[L_j]/E[K_j] <= 0.0049, so 2 E[L_j]/E[K_j] + 2^-50 < 2^-6.5, hence the factor (1 - 2^-6.5) in the ledger (`BONF = 6.5`).
- **Second-moment term.** q3r E[K_j^2]/E[K_j] <= q3r E[K_j] x 1.03 < 2^-50, using the panel's E[K^2]/E[K]^2 = 1.0248.

**Support.**
- *Panel* (Appendix H, our C port of the bucket claw at full table size, 64 seed-drawn chaining values, 2^22 scan words each).
  - Dispersion chi-square of the per-chaining-value counts against the pooled binomial rate, 63 degrees of freedom: C1 77.2 and C2|C1 49.4, both consistent with binomial.
  - G|C1C2 gives 437.5. It is overdispersed by design: a chaining value's kept a0 sit just after its own rotation R in each window (Section 3), and the G rate varies within a window. Averaged over R the law is uniform on P, and the pooled rate 2^-5.9358 matches the uniform 2^-5.9387.
  - F7|C1C2G gives 158.4. It is overdispersed because F7 reads the chaining value.
  - Both spreads are in E[K^2]/E[K]^2 above, which enters only the negligible cross-group term.
- *Step 3b on the panel's good pairs.* All 7,699 pass row 16; 0 pass row 17, and 0 are accepted. Row 17 holds with probability about 2^-17 for a good pair, the second stage of q3tv in Appendix P.
- *Rows 17..21 forced-bit events.* For the components of the accepted event, e4243e7a's registered Part B (Appendix H.2 of its proof) measured these events on good pairs of one chaining value and found no within-chaining-value dependence.
  - That test was run on its own a0 window. Our pairs differ only in the a0 law, and the rows 17..21 forced bits read E17..E21, functions of (W0..W15, cv) of the pair; we cite it as support of the same kind, not as a measurement on P.
- *Not testable at any sample size, and the premise.* The pairwise behaviour of the rows 17..37 event between unlinked good pairs over the random chaining value.

## 9. The q3 of the P1 good pairs (H2-P1)

**The base q3_model = 2^-96.0133** is e4243e7a's registered rate for the A0-variant family on P8, from 9aaf71a2's studies. Their records are reproduced in Appendix Q.
- It is the sum of two one-sided 99% lower bounds, each computed by a rule registered before its run, on real step-0..37 compressions with disjoint seeds:
  - the level of the printed-cell accepted event: 128 seeds of 2^28 samples, bound -96.42816;
  - the ratio of the relaxed event (E18 = E17 not imposed) to that event: 400 seeds, bound +0.41488.
- The sum is -96.01328, rounded down. Its tail draws W8 from the list of the 196,608 selected variants (8 classes x 96 class constants x 256 lanes, a1 = S's A1).

**The P1 family on P, measured by us (registered, paired; Appendix P).**
- *Tool.* `q3tv` (our own C, `m38/q3tv.c`), a multilevel splitting estimator on P8's tail characteristic and S:
  - row 16 exactly over S160;
  - rows 17..22 by splitting with N = 1,000 particles;
  - a final stage of N x 8,192 proposals, each with W7 uniform in F7, the late words W8, W9, W10 of one pair drawn from a variant list, rows 23..37 and the output comparison.
- *Event.* `RELAX_TAIL=1`: rows 23..37 free, outputs equal. `DIFFROW=19`: row 19 on signed differences only.
- *Pairing.* The stages before the final one do not read the list, and the list index is drawn as nxt() mod nV. So within one seed the families see the same particles, the same W7 draws and the same generator stream, and differ only in W8, W9 (and in W10, which is equal in all lists).
- *Statistic.* Per seed s, Delta_s = log2 q_P1(s) - log2 q_ref(s), with the registered statistic D_LB = mean - t(0.99, n - 1) sd / sqrt(n).
- *Families.*
  - P1: 65,536 pairs drawn uniformly from {a0 in P, a1 : C1, C2, G} by joint rejection.
  - A0 (registered first): a1 = S's A1, a0 uniform with G.
  - A0sel (amendment 1, registered before any A0sel run): the 196,608 selected variants on which q3_model was measured, generated from their published class data.
- *Charge.* q3_P1 = q3_model + min(0, D_LB(A0), D_LB(A0sel)), fixed in the amendment before either bound was known.

| reference family (registration) | seeds | D (bit) | sd(Delta) | D_LB (99%) | successes P1 / ref |
|---|---|---:|---:|---:|---:|
| A0: a1 = S's A1, a0 uniform with G (PREREG_P1SET_Q3, 2026-10-22 19:24 UTC) | 23 (9001..9040, 17 excluded) | +0.1461 | 0.3313 | -0.02721 | 14,325 / 13,213 |
| **A0sel: the 196,608 selected variants (amendment 1, 2026-10-22 19:36 UTC)** | 23 (9001..9040, 17 excluded) | +0.1439 | 0.3333 | -0.03042 | 14,325 / 13,241 |

The package charges q3_P1 = -96.0133 + min(0, -0.02721, -0.03042) = -96.0133 + (-0.0305, the minimum rounded down to 4 decimals) = **-96.0438**, so q3r = 2^-96.0438 x 2^32 / 160 = 2^-71.3657.
- *Confidence.* The three registered bounds (level, ratio, paired difference) together hold with confidence at least 97%, by the union bound.
- *What the statistic bounds.*
  - The registered statistic is a lower confidence bound on the mean per-seed log-ratio. The charge uses min(0, D_LB(A0), D_LB(A0sel)), so it never raises q3 above q3_model.
  - On the same proposals the pooled counts favour P1: log2 of the ratio of total successes, P1 over reference, is +0.117 against A0 and +0.114 against A0sel. The charged shift -0.0305 lies below both.
  - The 17 stalled seeds stall in the rows 16..22 prefix, which is identical in the three families and does not read the variant list, so their exclusion cannot favour a family.
- *Limitation, stated.* Our estimator conditions on row 22 of the characteristic before the final stage, while the base runs' final stage starts at row 22. W8 first enters the message expansion at W23 = s1(W21) + W16 + s0(W8) + W7, so the family law affects only rows 23..37 in both tools.
- *Limitation, stated.* The P1 pairs are drawn from the exact C1 C2 G law on P, not from claws of the procedure; W7 is drawn uniformly in F7 as in the base runs.

## 10. Memory (H6) and advice

**Online.**
- The online state is the table, (2^23 + 3) x 32 = 268,435,552 bytes (2^28 plus the three padding words, at RAM words 0 .. 2^23 + 2), plus the advice below, the registers, the scan state (under 1 KiB), step 3b's two traces (under 1 KiB) and the program code.
- Our C port of the online program ran on 64 chaining values in 8 processes of 8 chaining values each, with the full table: 2^23 buckets, 2^27 candidates, the bucket test of both passes, the four post-filters and step 3b on every good pair (`p1b38c.c`, Appendix H).
  - The largest peak resident set of the 16 full-table processes (this panel's 8 and the 8 of the first panel with R = 0, which ran the same program) was 263,620 KiB = 269,946,880 bytes = **2^28.00811**, measured by `/usr/bin/time -v` and the program's own VmHWM (Appendix H.4).
  - The counted online cell is this measured peak, host overhead included, as in a32131ff, and not the abstract 2^28 plus a few KiB.

**Preprocessing cells.** All are lower:
- the Step-1 solve of P8, re-measured under a 2^28 address-space cap at 221,076 KB = 2^27.7542 (377cb363; the same reclassification as a32131ff and 711c4bf8);
- our own solver-alone measurement of that solve, 70,892 KB = 2^26.08 (Appendix R.2);
- the signed search that found P8, at most 248,000 KB = 2^27.92 (our 1a695f0b report, quoted in Appendix R.2);
- the exact window counts of Section 6 (the choice of P), recomputed in small memory by `gwin38lm` at 34512 KiB = 2^25.07 bytes (Appendix R.1; the first computation, `gwin38`, held the sorted F8 in about 2^28.0 bytes and is superseded by this one);
- the condition tables and the pair data, below 2^24.

**Scope of the peak.** The peak is taken over the procedure of Section 3 and over every computation whose output the procedure reads.
- *Counted:*
  - the online phase;
  - the characteristic search that produced P8;
  - the Step-1 solve that produced S;
  - the window counts that chose P;
  - the condition tables.
- *Not counted:* the statistical studies that support the declared premises. These are the q3 studies (the base runs behind q3_model, recorded by 9aaf71a2 and reproduced in Appendix Q, and our paired runs of Appendix P), the full-size panels, the partner counts and the C-port cross-checks.
  - The procedure reads no output of theirs. Its inputs are P8, S, P and the constants of Section 2.
  - N_CV and V_MAX are inputs of the procedure (Section 3), fixed by the ledger from the declared premise values. A different study supporting the same premise values would leave the procedure and its memory unchanged.
  - These studies are evidence, like the organizer experiments; their time is inside DEV.
- *Their memory, for completeness.*
  - Our q3 tools peak at 6,604 KB (`q3tv`), 6,540 KB (`q3tv3`) and 6,748 KB (`q3tv4`) per process (`/usr/bin/time -v`, seed 9002). At most 32 ran at once (Appendix P timeline), at most 215,936 KB together, below the online peak.
  - The memory lines inside the reproduced base record (Appendix Q, that study's own sampler: 2^27.56 per process, 2^28.52 for two concurrent processes) describe 9aaf71a2's study, which this procedure does not execute.

**Claimed peak.** memory_log2_bytes = 28.00811, so the score is 83.01264 + 8.00811 = 91.02075.

**Advice inventory (bytes).**

| item | bytes |
|---|---:|
| A2..A15 and E6..E15 of both members (48 words) | 192 |
| the cells of rows 16..21 (54 words) | 216 |
| the '+' pairs (6 words) | 24 |
| the 35 two-bit conditions | 140 |
| the 20 heads of S160 and their 20 bucket deltas | 160 |
| 21 claw and post-filter constants | 84 |
| 7 SWAR masks of 32 bytes | 224 |
| K and IV (46 words) | 184 |
| **total** | **1,224** |

The total is under 2^11, inside the declared 2^13.

## 11. Allowances and development (H4a, H4b, H4c)

A_C = 2^78 (the characteristic search behind P8), A_S = 2^74 (its Step-1 solve) and DEV = 2^70 (all development) are charged allowances: upper bounds charged in full. preprocessing = log2(2^78 + 2^74 + 2^70) = 78.09276.

- **A_C and A_S.**
  - The search for P8 and its Step-1 solve are our own computations (1a695f0b). With all of our work on the P8 line, they ran on one 10-core machine for less than 2^22 core-seconds (our accounting, Appendix R.2).
  - At 2^30 target compressions per core-second, above any CPU core (SHA-256 runs at about 2^24 compressions per second per core), that is under 2^52 units, 26 bits under A_C.
  - Our solver-alone Step-1 rerun took 18 min 17 s.
- **DEV (H4c).** The bound is a hardware envelope. Every code execution behind this package ran on one 10-core machine (our own): the exhaustive counts of Section 6, the C ports, the panel, the partner count, the q3 runs, checks and failed runs. That is at most 10 cores for at most 30 days (2.6 x 10^6 s).
  - At most 2^40 word operations per core-second, that is under 2^64.6 operations = 2^53.2 compressions.
  - The development of the predecessors we build on, which was charged in their own DEV and is reproduced in Appendix Q (68 threads and one GPU for 17 days, under 2^56.7 compressions), is also inside DEV = 2^70 by a factor above 2^13.

## 12. Checks

- **`selftest`** (`python3 experiments/p1b38.py selftest`, PASSED):
  1. The P8 pair reproduces, is accepted, W7 is in F7, and `pair_words` rebuilds both members. Step 3b accepts it at its longest path, 3,014 operations.
  2. S160: 160 words of 20 heads; the row-16 tests on S160, 20,000 random words and 1,280 neighbours.
  3. Lemma 1 and the P1 pair identities on 300 random (cv, a0 in P, a1).
  4. The counted post-filters equal the real-word definitions on 60,000 pairs. The offset map of P is a bijection.
  5. Lemma B:
     - the SWAR field test equals the direct predicate on 4,000 random word pairs, in both passes;
     - a run with 2^17 candidates in the 2^23-bucket table over 2^12 scan words gives claws equal to the reference search;
     - the claws are distinct and every claw's real E16 is in S160;
     - the counted operations against the model mean at that size: ratio 1.0016.
  6. The organizer experiment on 3 trials: claws equal the reference, 0 bad E16, 0 bad post-filters, and the P8 pair is accepted.
  7. The ledger and the success bound.
- **Organizer experiments.**
  - `p1b-online-r38`: 5 seed-drawn chaining values with 2^17 candidates in the full bucket table and 2^11 scan words, the counted procedure with step 3b, every claw checked three ways; trial 5 runs step 3b on the P8 pair.
  - `p1b-rows-r38`: rows 16..21 of every claw at the same size over 2^13 words.
  - At this size the buckets are sparse, so empty lanes produce spurious matches (reported, and rejected by the count test). The counts are reproducible observations consistent with the premises; no rate is inferred from them.
- **Full size** (Appendix H; our C port `p1b38c.c`).
  - It reproduces `run_cv`: the claw lists (sorted) and the per-chaining-value counts (stored lanes, claws, stage counts, spurious matches, straddles) are identical to the Python program's on 3 chaining values with 2^17 candidates and 2 with 2^19 candidates (2^12 scan words), and both equal the reference search.
  - Its step 3b is the one of our residue-table port, identical to the Python step3b on 4,001 test pairs.
  - With the full table (2^27 candidates) over 2^18 words, the claws equal the reference search: chaining value 24: 573,516 claws, reference 573,516; chaining value 25: 572,352 claws, reference 572,352.
  - The 64-chaining-value panel: claws/expected 0.99999, stored lanes per bucket 6.994111 (expected 6.994098), spurious matches 494,945 (expected 495075), 0 bad E16.

## Appendix A. The ledger, term by term

| term (operations) | value |
|---|---|
| allowance A_C = 2^78 x C | 824,487,408,977,177,097,149,612,032 |
| allowance A_S = 2^74 x C | 51,530,463,061,073,568,571,850,752 |
| allowance DEV = 2^70 x C | 3,220,653,941,317,098,035,740,672 |
| online work cap V_MAX (charged in full; includes the N_CV first blocks) | 25,736,438,737,648,325,429,509,603,446 |
| overshoot OVER (one chaining value at its maximum) | 7,574,569,065,909,037 |
| final verification FIN = 6 C + 1,600 | 17,968 |
| **N** | **26,615,677,263,635,467,762,332,733,907** |

N / C = 2^83.01264; score 91.02075.


## Appendix H. The full-size panel, the partner count and the memory measurement (Sections 6, 8, 10, 12)

Tools (own code; sources in Appendix S): `p1b38c.c` (the C port of the bucket claw of `run_cv` with `step3b`), `p1tconst.py` (writes the constant header and the chaining values), `xcheck_b.py` (the cross-check against `p1b38.py`), `partners38.c` (the full-scan partner count). Chaining values: for j = 0..63 the first block of `Shake('p1t-panel|j')` (two random 256-bit words), its real 38-step chaining value, and u0 = the next 32-bit word of the same stream. Panel: 8 processes, `GOODF=good_27_22_k.txt /usr/bin/time -v ./p1b38c cvs_panel_r.txt 27 22 0 8k 8` for k = 0..7 (`cvs_panel_r.txt` adds R = the next 32-bit word of the stream mod 2^27, `mkcvs_r.py`) (2^23 buckets, 2^27 candidates of P, 2^22 scan words u0 + n per chaining value, step 3b on every good pair), in Docker (image sha2sat:2), one process per container.

### H.1 Cross-checks of the C port

- Against `p1b38.run_cv` (Python, which executes the SWAR test literally): the sorted claw lists and the per-chaining-value counts (stored lanes, claws, stage counts, spurious matches, straddling words) are identical on 3 chaining values with 2^17 candidates and on 2 with 2^19 candidates, 2^12 scan words each; both equal the reference search (62 and 162 claws).
- Step 3b: the routine of our residue-table port, identical to the Python step3b on 4,001 test pairs; the P8 pair is accepted (`# step 3b on the S pair: 7`).
- Reference search with the full table: 2^27 candidates, 2^18 scan words, `./p1b38c cvs_panel_r.txt 27 18 1 24 2`: chaining value 24: 573,516 claws, reference 573,516; chaining value 25: 572,352 claws, reference 572,352.

### H.2 The panel (64 chaining values, 2^22 scan words each)

Pooled: claws 586,702,214 against the expected 586,708,588 (2^22 x 160 x stored lanes / 2^32; ratio 0.99999); stored lanes per bucket 6.994111 (expected 6.994098); spurious matches 494,945 (expected 495075); straddling scan words 2,621,865 (expected 5/512 of 2^22 x 64 = 2,621,440); C1 0.12498 (exact 1/8); C2|C1 2^-3.3388 (exact 2^-3.3379); G|C1C2 2^-5.9358 (exact over P 2^-5.9387); F7|C1C2G 0.06503 (|F7|/2^32 = 0.06689); good pairs 7,699, good per claw 2^-16.2176 (charged q_pf 2^-16.1785); 0 claws with E16 outside S160; good pairs passing row 16 in step 3b 7,699, row 17 0, accepted 0. Per-chaining-value dispersion chi-square (63 dof): C1 77.2, C2|C1 49.4, G|C1C2 437.5, F7|C1C2G 158.4. E[K^2]/E[K]^2 = 1.0248.

| j | stored lanes | claws | expected | C1 | C1 C2 | C1 C2 G | good | spurious | straddling words | good sharing a0 (window) | good sharing u | step 3b row 16 | row 17 | accepted |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 0 | 58,670,558 | 9,164,461 | 9167274.7 | 1,146,054 | 113,491 | 1882 | 127 | 7817 | 40973 | 0 | 0 | 127 | 0 | 0 |
| 1 | 58,670,729 | 9,166,980 | 9167301.4 | 1,146,035 | 113,221 | 1878 | 115 | 7540 | 40987 | 0 | 0 | 115 | 0 | 0 |
| 2 | 58,670,854 | 9,167,854 | 9167320.9 | 1,145,660 | 113,274 | 2034 | 145 | 7597 | 40938 | 0 | 0 | 145 | 0 | 0 |
| 3 | 58,671,008 | 9,171,511 | 9167345.0 | 1,145,427 | 113,203 | 1657 | 113 | 7657 | 40987 | 0 | 0 | 113 | 0 | 0 |
| 4 | 58,670,960 | 9,165,533 | 9167337.5 | 1,146,889 | 113,496 | 1746 | 149 | 7723 | 40973 | 0 | 0 | 149 | 0 | 0 |
| 5 | 58,670,553 | 9,167,452 | 9167273.9 | 1,145,756 | 112,778 | 1712 | 107 | 7819 | 40947 | 0 | 0 | 107 | 0 | 0 |
| 6 | 58,671,475 | 9,164,564 | 9167418.0 | 1,144,970 | 112,929 | 1704 | 91 | 7585 | 40980 | 0 | 0 | 91 | 0 | 0 |
| 7 | 58,669,156 | 9,165,895 | 9167055.6 | 1,144,866 | 113,414 | 1875 | 139 | 7898 | 40987 | 0 | 0 | 139 | 0 | 0 |
| 8 | 58,671,196 | 9,167,773 | 9167374.4 | 1,145,822 | 113,389 | 1889 | 135 | 7607 | 40952 | 0 | 0 | 135 | 0 | 0 |
| 9 | 58,671,339 | 9,162,088 | 9167396.7 | 1,146,506 | 113,204 | 1733 | 107 | 7544 | 40945 | 0 | 0 | 107 | 0 | 0 |
| 10 | 58,670,473 | 9,165,148 | 9167261.4 | 1,145,350 | 113,219 | 1989 | 138 | 7701 | 40947 | 0 | 0 | 138 | 0 | 0 |
| 11 | 58,672,098 | 9,162,714 | 9167515.3 | 1,146,272 | 112,748 | 1894 | 154 | 7402 | 41002 | 0 | 0 | 154 | 0 | 0 |
| 12 | 58,670,835 | 9,165,478 | 9167318.0 | 1,144,835 | 112,727 | 1938 | 155 | 7752 | 40969 | 0 | 0 | 155 | 0 | 0 |
| 13 | 58,671,288 | 9,162,105 | 9167388.8 | 1,146,034 | 113,288 | 2027 | 115 | 7680 | 40971 | 0 | 0 | 115 | 0 | 0 |
| 14 | 58,671,256 | 9,168,082 | 9167383.8 | 1,144,807 | 113,110 | 1665 | 89 | 7811 | 40981 | 0 | 0 | 89 | 0 | 0 |
| 15 | 58,671,340 | 9,164,601 | 9167396.9 | 1,144,372 | 113,130 | 1992 | 120 | 7579 | 40964 | 0 | 0 | 120 | 0 | 0 |
| 16 | 58,670,544 | 9,165,378 | 9167272.5 | 1,145,044 | 112,734 | 1754 | 128 | 7967 | 40978 | 0 | 0 | 128 | 0 | 0 |
| 17 | 58,670,944 | 9,169,048 | 9167335.0 | 1,145,719 | 113,579 | 2045 | 128 | 7653 | 41015 | 0 | 0 | 128 | 0 | 0 |
| 18 | 58,671,310 | 9,169,408 | 9167392.2 | 1,145,629 | 113,398 | 1971 | 133 | 7684 | 40971 | 0 | 0 | 133 | 0 | 0 |
| 19 | 58,670,691 | 9,172,572 | 9167295.5 | 1,146,442 | 113,528 | 1993 | 104 | 7911 | 41000 | 0 | 0 | 104 | 0 | 0 |
| 20 | 58,670,661 | 9,165,891 | 9167290.8 | 1,145,731 | 113,025 | 1962 | 135 | 7928 | 40988 | 0 | 0 | 135 | 0 | 0 |
| 21 | 58,670,999 | 9,165,855 | 9167343.6 | 1,145,876 | 113,667 | 1957 | 130 | 7579 | 40943 | 0 | 0 | 130 | 0 | 0 |
| 22 | 58,670,915 | 9,162,442 | 9167330.5 | 1,146,019 | 113,607 | 1732 | 94 | 7855 | 40978 | 0 | 0 | 94 | 0 | 0 |
| 23 | 58,670,547 | 9,167,726 | 9167273.0 | 1,146,616 | 112,791 | 1799 | 112 | 7573 | 40955 | 0 | 0 | 112 | 0 | 0 |
| 24 | 58,670,965 | 9,172,774 | 9167338.3 | 1,147,226 | 113,697 | 1746 | 92 | 7901 | 40947 | 0 | 0 | 92 | 0 | 0 |
| 25 | 58,671,269 | 9,170,008 | 9167385.8 | 1,147,348 | 113,394 | 1914 | 117 | 7915 | 40951 | 0 | 0 | 117 | 0 | 0 |
| 26 | 58,670,704 | 9,166,129 | 9167297.5 | 1,146,020 | 113,454 | 1832 | 144 | 7831 | 40947 | 0 | 0 | 144 | 0 | 0 |
| 27 | 58,670,276 | 9,162,927 | 9167230.6 | 1,145,782 | 113,025 | 1926 | 109 | 7780 | 40964 | 0 | 0 | 109 | 0 | 0 |
| 28 | 58,670,783 | 9,169,082 | 9167309.8 | 1,147,490 | 113,150 | 1734 | 120 | 7629 | 40947 | 0 | 0 | 120 | 0 | 0 |
| 29 | 58,671,319 | 9,164,344 | 9167393.6 | 1,145,757 | 113,601 | 1832 | 142 | 7528 | 40988 | 0 | 0 | 142 | 0 | 0 |
| 30 | 58,670,435 | 9,161,572 | 9167255.5 | 1,143,905 | 112,973 | 1799 | 98 | 7733 | 40937 | 0 | 0 | 98 | 0 | 0 |
| 31 | 58,670,620 | 9,170,304 | 9167284.4 | 1,144,862 | 113,199 | 1790 | 123 | 7726 | 40942 | 0 | 0 | 123 | 0 | 0 |
| 32 | 58,670,165 | 9,169,515 | 9167213.3 | 1,146,757 | 112,956 | 1948 | 137 | 7689 | 40974 | 0 | 0 | 137 | 0 | 0 |
| 33 | 58,670,858 | 9,172,288 | 9167321.6 | 1,145,226 | 113,094 | 1828 | 112 | 7665 | 40980 | 0 | 0 | 112 | 0 | 0 |
| 34 | 58,671,172 | 9,169,400 | 9167370.6 | 1,149,151 | 113,507 | 1878 | 126 | 7545 | 40988 | 0 | 0 | 126 | 0 | 0 |
| 35 | 58,670,148 | 9,166,942 | 9167210.6 | 1,147,646 | 113,672 | 1926 | 110 | 7985 | 40951 | 0 | 0 | 110 | 0 | 0 |
| 36 | 58,671,597 | 9,166,919 | 9167437.0 | 1,147,507 | 113,493 | 1991 | 154 | 7751 | 40991 | 0 | 0 | 154 | 0 | 0 |
| 37 | 58,670,329 | 9,164,389 | 9167238.9 | 1,143,558 | 113,147 | 1762 | 123 | 7555 | 40946 | 0 | 0 | 123 | 0 | 0 |
| 38 | 58,671,496 | 9,170,204 | 9167421.2 | 1,145,324 | 113,009 | 1931 | 139 | 7716 | 40958 | 0 | 0 | 139 | 0 | 0 |
| 39 | 58,670,927 | 9,170,406 | 9167332.3 | 1,144,745 | 113,289 | 1700 | 107 | 7702 | 40971 | 0 | 0 | 107 | 0 | 0 |
| 40 | 58,670,540 | 9,161,499 | 9167271.9 | 1,144,386 | 113,450 | 1937 | 141 | 7834 | 40967 | 0 | 0 | 141 | 0 | 0 |
| 41 | 58,671,225 | 9,167,876 | 9167378.9 | 1,144,750 | 112,814 | 1834 | 95 | 7694 | 40958 | 0 | 0 | 95 | 0 | 0 |
| 42 | 58,670,826 | 9,166,390 | 9167316.6 | 1,147,552 | 113,305 | 2042 | 139 | 7855 | 40963 | 0 | 0 | 139 | 0 | 0 |
| 43 | 58,671,275 | 9,165,975 | 9167386.7 | 1,143,605 | 113,082 | 1995 | 128 | 7652 | 40986 | 0 | 0 | 128 | 0 | 0 |
| 44 | 58,670,807 | 9,168,683 | 9167313.6 | 1,146,269 | 113,440 | 1692 | 98 | 7781 | 40948 | 0 | 0 | 98 | 0 | 0 |
| 45 | 58,671,312 | 9,169,586 | 9167392.5 | 1,146,275 | 113,599 | 1949 | 150 | 7718 | 40960 | 0 | 0 | 150 | 0 | 0 |
| 46 | 58,670,693 | 9,166,351 | 9167295.8 | 1,144,664 | 113,433 | 1902 | 100 | 7778 | 40951 | 0 | 0 | 100 | 0 | 0 |
| 47 | 58,670,272 | 9,171,684 | 9167230.0 | 1,146,699 | 113,438 | 1711 | 102 | 7836 | 40948 | 0 | 0 | 102 | 0 | 0 |
| 48 | 58,671,601 | 9,166,610 | 9167437.7 | 1,145,211 | 112,954 | 1741 | 109 | 7559 | 40953 | 0 | 0 | 109 | 0 | 0 |
| 49 | 58,670,575 | 9,165,134 | 9167277.3 | 1,145,225 | 113,114 | 1831 | 126 | 7797 | 41001 | 0 | 0 | 126 | 0 | 0 |
| 50 | 58,671,314 | 9,168,441 | 9167392.8 | 1,146,690 | 112,763 | 1717 | 122 | 7596 | 40989 | 0 | 0 | 122 | 0 | 0 |
| 51 | 58,670,331 | 9,163,890 | 9167239.2 | 1,143,336 | 113,096 | 1924 | 97 | 7900 | 40941 | 0 | 0 | 97 | 0 | 0 |
| 52 | 58,669,851 | 9,171,652 | 9167164.2 | 1,145,629 | 113,753 | 1856 | 154 | 7889 | 40947 | 0 | 0 | 154 | 0 | 0 |
| 53 | 58,671,056 | 9,164,667 | 9167352.5 | 1,147,816 | 113,786 | 1747 | 112 | 7674 | 40965 | 0 | 0 | 112 | 0 | 0 |
| 54 | 58,670,968 | 9,164,556 | 9167338.8 | 1,145,647 | 113,158 | 1877 | 117 | 7826 | 40975 | 0 | 0 | 117 | 0 | 0 |
| 55 | 58,671,106 | 9,164,671 | 9167360.3 | 1,143,348 | 113,261 | 1724 | 89 | 7845 | 40949 | 0 | 0 | 89 | 0 | 0 |
| 56 | 58,670,867 | 9,170,423 | 9167323.0 | 1,145,534 | 112,857 | 1629 | 87 | 7680 | 40971 | 0 | 0 | 87 | 0 | 0 |
| 57 | 58,671,338 | 9,172,502 | 9167396.6 | 1,144,777 | 112,560 | 1798 | 143 | 7837 | 40975 | 0 | 0 | 143 | 0 | 0 |
| 58 | 58,670,547 | 9,167,721 | 9167273.0 | 1,146,282 | 113,474 | 1690 | 91 | 7663 | 40971 | 0 | 0 | 91 | 0 | 0 |
| 59 | 58,670,548 | 9,174,583 | 9167273.1 | 1,145,611 | 113,936 | 1854 | 109 | 7922 | 40963 | 0 | 0 | 109 | 0 | 0 |
| 60 | 58,669,623 | 9,163,177 | 9167128.6 | 1,145,061 | 113,037 | 1720 | 137 | 7876 | 40975 | 1 | 0 | 137 | 0 | 0 |
| 61 | 58,671,223 | 9,168,782 | 9167378.6 | 1,146,970 | 113,584 | 1947 | 116 | 7674 | 40968 | 0 | 0 | 116 | 0 | 0 |
| 62 | 58,670,420 | 9,169,887 | 9167253.1 | 1,145,152 | 113,105 | 1914 | 102 | 7842 | 40968 | 0 | 0 | 102 | 0 | 0 |
| 63 | 58,671,854 | 9,169,712 | 9167477.2 | 1,146,425 | 113,111 | 2000 | 119 | 7704 | 40960 | 0 | 0 | 119 | 0 | 0 |

### H.3 The full-scan partner count (Section 8)

`./partners38 cvs_panel.txt good_27_22.txt` (the chaining values of `cvs_panel_r.txt` without R) (the 8 good-pair files concatenated; one pass over all 2^32 words u; for each good pair of the panel the claws of its a0 are the u with s0(u) - u + F(a0) in S160, and each is tested with the four post-filters). Result: good pairs 7699; claws of their a0 over 2^32 words: mean 161.100; good partners sharing a0: 47 (0.006105 per good pair). Every good partner (u' != u) is listed: chaining value, a0, u, u', u' - u.

~~~
P 30 157fb85d 06daad9f 057babbf du fea0fe20
P 15 25f5b112 1e13670b 07d90bfa du e9c5a4ef
P 30 1576afd8 06bd7e07 13aafc0b du 0ced7e04
P 3 350e6cec 20d55106 1a22a3ff du f94d52f9
P 52 357a0a9b 31962a84 238bcb40 du f1f5a0bc
P 1 146dc190 20d60adb 29840441 du 08adf966
P 52 358ec813 31a05549 31315369 du ff90fe20
P 12 34d24407 3aa0f3de 373f9fb0 du fc9eabd2
P 52 357961a3 318ef16a 3f6f824f du 0de090e5
P 58 057cd9ef 35874cf3 44ef4ccc du 0f67ffd9
P 4 257977bd 3562ee71 4999d486 du 1436e615
P 9 34fc74e5 596278c2 4a3482eb du f0d20a29
P 45 15677fbf 3b248c41 4b9fca24 du 107b3de3
P 21 24e31a3c 3a290944 4cada3a7 du 12849a63
P 38 14913235 5cd50da2 537af042 du f6a5e2a0
P 37 254ef8df 5d9c35a4 53a7eedb du f60bb937
P 9 04848669 5961932a 58a8149a du ff468170
P 14 256dca76 5b0dbb63 5f537f47 du 0445c3e4
P 25 34f609bf 6a055f0e 63fe03be du f9f8a4b0
P 32 0493535c 7ce6044e 64f033bd du e80a2f6f
P 6 0477a243 68e5cf02 6974cd22 du 008efe20
P 42 14989cc8 5b2dbeeb 6cf965c8 du 11cba6dd
P 6 05553c17 6902d484 7983d29d du 1080fe19
P 59 15cbb910 a115786c 8a73114f du e95d98e3
P 22 2406f289 8e899694 8f1894b4 du 008efe20
P 60 34703a57 9c4d6ce6 92ed6c82 du f69fff9c
P 60 2453ac15 9c4fae9b 9c3fae83 du ffefffe8
P 60 2453ac15 9c3fae83 9c4fae9b du 00100018
P 50 346f116d af286807 ac09f9b5 du fce191ae
P 50 3463e0ac af0a41c2 aeaa5f40 du ffa01d7e
P 34 04ecf6ea c0577573 be1b54d7 du fdc3df64
P 11 340739a9 c6fc8809 c1942c19 du fa97a410
P 43 147aa300 dc09ee1d c5e04d4c du e9d65f2f
P 63 35510d52 dddc7673 ccee72aa du ef11fc37
P 47 1578f441 d142391f d0c33b3f du ff810220
P 29 25f4312d d055ee45 d0e72c25 du 00913de0
P 47 15d9dc28 d140efdf d93c5054 du 07fb6075
P 57 1517d6de e312862d da8f21fc du f77c9bcf
P 28 05ff4a8b e5ef5657 def3aaf1 du f904549a
P 2 05e79f57 eaab6e02 e29e2d96 du f7f2bf94
P 28 35ea7580 e5d3adad e5c1adad du ffee0000
P 46 25e6bec1 ed67ab0e e8866408 du fb1eb8fa
P 2 050a3f23 ea8678a4 ea077a84 du ff8101e0
P 20 25642a09 fd5a5000 ec615c31 du ef070c31
P 35 04760b8d 02ab919a f2d227eb du f0269651
P 57 0586d343 e2e01178 f2f9218f du 10191017
P 20 354172a1 fd6cd927 fdeddb07 du 008101e0
~~~

### H.4 The memory measurement (Section 10)

Per panel process k (8 chaining values each, the full table), for this panel and for the first panel (R = 0, H.5): `/usr/bin/time -v` maximum resident set size and the program's own VmHWM, in KiB:

| process k | chaining values | maximum resident set (time -v) | VmHWM | exit status |
|---:|---|---:|---:|---|
| 0 | 0..7 | 263,476 | 263,520 | 0 |
| 1 | 8..15 | 263,432 | 263,540 | 0 |
| 2 | 16..23 | 263,104 | 263,536 | 0 |
| 3 | 24..31 | 263,304 | 263,540 | 0 |
| 4 | 32..39 | 263,480 | 263,484 | 0 |
| 5 | 40..47 | 263,436 | 263,504 | 0 |
| 6 | 48..55 | 263,424 | 263,516 | 0 |
| 7 | 56..63 | 263,308 | 263,504 | 0 |
| 0 (R = 0) | 0..7 | 263,432 | 263,476 | 0 |
| 1 (R = 0) | 8..15 | 263,484 | 263,488 | 0 |
| 2 (R = 0) | 16..23 | 263,620 | 263,492 | 0 |
| 3 (R = 0) | 24..31 | 263,488 | 263,488 | 0 |
| 4 (R = 0) | 32..39 | 263,156 | 263,468 | 0 |
| 5 (R = 0) | 40..47 | 263,288 | 263,468 | 0 |
| 6 (R = 0) | 48..55 | 263,368 | 263,472 | 0 |
| 7 (R = 0) | 56..63 | 263,488 | 263,488 | 0 |

The counted cell is the largest figure, 263,620 KiB = 269,946,880 bytes = 2^28.00811 (rounded up).

### H.5 The first panel, without the rotation R (Section 3)

The same 64 chaining values, u0 and table, with the insertion order o = rotr2(n) (R = 0): claws 586,680,070 against the expected 586,708,588 (ratio 0.99995), stored lanes per bucket 6.994111; C1 0.12498, C2|C1 2^-3.3384, **G|C1C2 2^-5.9937** (uniform on P: 2^-5.9387), F7|C1C2G 0.06568; good pairs 7,472, good per claw 2^-16.2607 (charged 2^-16.1785). The kept candidates are the first 7 per bucket, which favours small n, i.e. the low half of each 2^25-window of P, where the G rate is lower; the claw count and table behaviour are unchanged. This run is why the procedure draws R: with R uniform the kept a0 are uniform on P on average (H.2 above). Its peak resident sets were 263,620 KiB at most.

## Appendix P. The paired q3 runs of the P1 family on P (Section 9): registrations, runs, per-seed values

Tool: `q3tv` (our own C; source `m38/q3tv.c` sha256 e01dbb414ef2a7e0cecf79638bb287130e1309dfa439727b57bc8b32b3957ead, binary sha256 883beea75bfe25e8b8128e9dbe278efa970b57441579293cd6481a8e7089216d), data file `q_S.dat` (P8's tail characteristic and S's base pair, written by our `prep.py`; sha256 ee7c9033f5afc0d00ba3b9501486fd45eae6dbd2ba9679f1057ba179e85c283a). Variant lists: `vars_P1set.txt` (`p1vars38 base_S.txt p1 65536 vars_P1set.txt 11`), `vars_A0fam.txt` (`p1vars38 base_S.txt a0 65536 vars_A0fam.txt 12 e083b276`), `vars_A0sel.txt` (`gensel38 base_S.txt vars_A0sel.txt e083b276`); sources in Appendix S. Every run: `DIFFROW=19 RELAX_TAIL=1 VARS=<list> q3tv q_S.dat <seed> 1000 8192`, one process, in Docker (image sha2sat:2).

**Timeline (UTC, 2026-10-22).** 19:24:26 PREREG_P1SET_Q3.md hashed; the A0 and P1 runs started with 6 workers. 19:36:54 amendment 1 hashed, before any A0sel run; at that moment 7 seeds had completed in both the A0 and P1 families (9002 to 9006, 9008, 9009; also the A0 run of 9012) and their per-seed values had been looked at (the amendment's "21 of 80 complete" counted output files, including runs in progress). The amendment charges the smaller of the two bounds, so it cannot raise the charge above the original registration's. 19:37 the A0sel runs started with 3 workers. At 19:56 both pools were stopped and restarted as one pool of 12 workers on the 93 runs without a result (`run_one.sh`, the same command). The machine was shared with other jobs and the slow seeds (whose rows 16..22 stages need up to 2^34 tries) ran three times over, once per family, so at 20:19 that pool was stopped too and the remaining seeds were computed by `q3tv3` (Appendix S; from 20:30 in 12 single-process containers taking seeds from a shared queue, `run3q.sh`): the same source with the shared prefix (rows 16..22, which does not read the list) run once per seed, the generator state saved after it, and the final stage run once per list from that saved state. Because q3tv is deterministic given the seed and the final stage starts from the same generator state and particles in every family, its three outputs are those of the three separate runs; this was checked byte for byte on seeds 9002, 9003, 9004, 9012, 9014, 9015, where the separate runs had completed (15 identical files, 0 different). At 21:38 the 20 seeds still running were also started with `q3tv4` (Appendix S): `q3tv3` with each stage try evaluated on the particle in place (the new row in locals, the particle copied only when accepted, the conditions of each row in a per-row list in the same order), which makes every decision and the generator stream the same; it was checked byte for byte against the separate runs of seeds 9002, 9005 and 9008 before use, and where both builds completed a seed their outputs are identical (0 files). The 12 `q3tv3` runs still going were stopped at 22:14 UTC, before any of them completed, so these 20 seeds were all computed by `q3tv4`. No output of an interrupted run is used. Stalled seeds: 9001, 9007, 9010, 9011, 9013, 9016, 9018, 9022, 9024, 9025, 9027, 9032, 9033, 9034, 9036, 9037, 9040.

The two registration texts follow verbatim, with one redaction: a local absolute path prefix is shown as `<local>/` (the sha256 values are of the original files).

**PREREG_P1SET_Q3.md** (sha256 46ec2355c2b1c744966a14880dd3e6d467a7bbe1c6d8308caa5c7fc9558cd24e):

~~~
# PREREG_P1SET_Q3: paired q3 of the P1 family on the table's a0 set P against the A0-variant family (written 2026-10-22, before any seed)

## Quantity
D = mean over seeds s of Delta_s = log2(succ_P1(s)) - log2(succ_A0(s)), where succ_X(s) is the number of accepted proposals of one
q3tv run (sha2-search/m38/q3tv.c, own code) with seed s, N = 1000 particles, T = 8192 proposals per particle, the relaxed accepted
event (env DIFFROW=19, RELAX_TAIL=1: rows 16..22 of P8's characteristic with row 19 on signed differences only, outputs compared),
data file q_S.dat (P8's tail characteristic j43 and S's base pair) and env VARS = the variant list of family X:
- P1: vars_P1set.txt, 65,536 pairs (a0, a1) drawn uniformly from {a0 in P, a1 any word : C1 and C2 and G} by joint rejection
  (p1vars38 seed 11), P = {a0 : bits 25..27 = 010, bits 30..31 = 00} (the table's a0 set, 2^27 words);
- A0: vars_A0fam.txt, 65,536 pairs (a0, A1 of S = e083b276) with a0 uniform over all words with G (p1vars38 seed 12).
Within a seed the two runs consume the generator identically (same particles, same W7 draws, same list indices), so Delta_s
compares the two families on the same proposals; only W8, W9 (and W10, equal in both lists) differ.

## Seeds and rule
Seeds 9001..9040 (40 seeds), every one run in both families. A seed whose run stalls before the final stage (q3tv prints "stalled")
stalls in both families (the stages before the final one do not read VARS) and is excluded; the number excluded is reported.
Statistic: D = mean Delta_s, sd its sample standard deviation, D_LB = D - t(0.99, n - 1) sd / sqrt(n) (one-sided 99 %).
The package charges q3_P1 = q3_model + min(0, D_LB).

## Hashes (sha256) of the inputs, recorded before the first seed
97fe61672e5145a539ba305cf68bec515bd7cbf362da7be513cb73958d6444d2 vars_P1set.txt
d77ecec2c8b07844f8ef0cea20a510246d98d1d519c1acf416e0d8a202db80f4 vars_A0fam.txt
ee7c9033f5afc0d00ba3b9501486fd45eae6dbd2ba9679f1057ba179e85c283a q_S.dat
e01dbb414ef2a7e0cecf79638bb287130e1309dfa439727b57bc8b32b3957ead ../../../m38/q3tv.c
883beea75bfe25e8b8128e9dbe278efa970b57441579293cd6481a8e7089216d <local>/sha2-search/m38/lowmem/q3tv
~~~

**PREREG_P1SET_Q3_AMEND1.md** (sha256 a775232640d0f8b47dac9367f5a017fd9abe51aedfda26e59cfd7f888f739081):

~~~
# PREREG_P1SET_Q3 amendment 1: a third family, the selected A0 variants (written 2026-10-22, before any run of this family)

Reason. q3_model = -96.0133 (the registered bound of 9aaf71a2's studies, as charged by e4243e7a) was measured with W8 drawn from the
196,608 selected variants of the A0-variant family, not from the family A0 of PREREG_P1SET_Q3.md (a1 = S's A1, a0 uniform over
all words with G).  A paired difference transfers q3_model only when its reference family is the family q3_model was measured on.

Third family A0sel: vars_A0sel.txt, the 196,608 selected variants (8 classes x 96 class constants x 256 lanes), a1 = S's A1
(e083b276), generated by m38/lowmem/gensel38.c (own code; the class data CLASSES, MASK, LB, G1, G3 and the formulas bconst and
lane_a0 transcribed as data from the public p1claw38.py of e4243e7a; every one of the 196,608 satisfies C1, C2, G).  q3tv draws
the list index as nxt() mod nV, so the generator is consumed exactly as in the other two families; the seeds' particles and W7
draws are the same in all three.

Seeds 9001..9040, the same command as run.sh with VARS = vars_A0sel.txt, output q3pair/S_<seed>.txt.  Exclusion rule unchanged.
Statistics: D' = mean over seeds of Delta'_s = log2q_P1(s) - log2q_A0sel(s), sd', D'_LB = D' - t(0.99, n - 1) sd' / sqrt(n).
D, D_LB (P1 against A0) are computed exactly as registered.

Charged value (changed before any A0sel run; the P1 and A0 runs of PREREG_P1SET_Q3.md were in progress, 21 of 80 complete, when
this was written): q3_P1 = q3_model + min(0, D_LB, D'_LB), the smaller of the two registered bounds, so no choice between them is
made after seeing either.

## Hashes (sha256), recorded before the first A0sel run
5aa8d5eb044ab997d4d9e124940059ed9c51d39d4071c8e41015522334da97c1  vars_A0sel.txt
6f127183000a31d2b43338709da21b7aebf7d7748a71a07d3c432773554e5b57  ../../../m38/lowmem/gensel38.c
~~~

**Results.** P1 - A0: n = 23, D = +0.1461, sd = 0.3313, t(0.99, 22) = 2.5083, D_LB = -0.0272. P1 - A0sel: n = 23, D = +0.1439, sd = 0.3333, D_LB = -0.0304. Charged: min(0, D_LB, D'_LB) = -0.0305 (rounded down).

| seed | log2 q A0 | log2 q P1 | log2 q A0sel | Delta (P1 - A0) | Delta' (P1 - A0sel) | successes A0 / P1 / A0sel | final stage A0 / P1 / A0sel |
|---:|---:|---:|---:|---:|---:|---:|---:|
| 9001 | stalled | | | | | | |
| 9002 | -96.3864 | -96.3739 | -96.4248 | +0.0125 | +0.0509 | 572 / 577 / 557 | -13.806 / -13.793 / -13.844 |
| 9003 | -96.1507 | -95.4922 | -95.9994 | +0.6585 | +0.5072 | 389 / 614 / 432 | -14.362 / -13.704 / -14.211 |
| 9004 | -94.3962 | -94.2916 | -94.4261 | +0.1046 | +0.1345 | 585 / 629 / 573 | -13.773 / -13.669 / -13.803 |
| 9005 | -95.5768 | -95.5317 | -95.5541 | +0.0451 | +0.0224 | 504 / 520 / 512 | -13.989 / -13.943 / -13.966 |
| 9006 | -95.0167 | -94.5167 | -95.0167 | +0.5000 | +0.5000 | 466 / 659 / 466 | -14.102 / -13.602 / -14.102 |
| 9007 | stalled | | | | | | |
| 9008 | -96.0333 | -96.3548 | -96.0655 | -0.3215 | -0.2893 | 726 / 581 / 710 | -13.462 / -13.783 / -13.494 |
| 9009 | -95.9975 | -95.9645 | -96.0064 | +0.0330 | +0.0419 | 649 / 664 / 645 | -13.624 / -13.591 / -13.633 |
| 9010 | stalled | | | | | | |
| 9011 | stalled | | | | | | |
| 9012 | -95.7356 | -96.0372 | -95.7792 | -0.3016 | -0.2580 | 774 / 628 / 751 | -13.370 / -13.671 / -13.413 |
| 9013 | stalled | | | | | | |
| 9014 | -96.1802 | -96.0799 | -96.1314 | +0.1003 | +0.0515 | 639 / 685 / 661 | -13.646 / -13.546 / -13.597 |
| 9015 | -96.7525 | -96.6709 | -96.7166 | +0.0816 | +0.0457 | 515 / 545 / 528 | -13.957 / -13.876 / -13.921 |
| 9016 | stalled | | | | | | |
| 9017 | -96.6885 | -96.4106 | -96.7482 | +0.2779 | +0.3376 | 518 / 628 / 497 | -13.949 / -13.671 / -14.009 |
| 9018 | stalled | | | | | | |
| 9019 | -95.2204 | -94.7458 | -95.1646 | +0.4746 | +0.4188 | 457 / 635 / 475 | -14.130 / -13.655 / -14.074 |
| 9020 | -96.7554 | -96.2027 | -96.7287 | +0.5527 | +0.5260 | 482 / 707 / 491 | -14.053 / -13.500 / -14.026 |
| 9021 | -96.0583 | -96.4198 | -95.9410 | -0.3615 | -0.4788 | 767 / 597 / 832 | -13.383 / -13.744 / -13.265 |
| 9022 | stalled | | | | | | |
| 9023 | -96.1398 | -96.3357 | -96.4181 | -0.1959 | +0.0824 | 701 / 612 / 578 | -13.513 / -13.708 / -13.791 |
| 9024 | stalled | | | | | | |
| 9025 | stalled | | | | | | |
| 9026 | -96.2255 | -95.9874 | -96.1778 | +0.2381 | +0.1904 | 624 / 736 / 645 | -13.680 / -13.442 / -13.633 |
| 9027 | stalled | | | | | | |
| 9028 | -94.8501 | -94.5324 | -94.7980 | +0.3177 | +0.2656 | 544 / 678 / 564 | -13.878 / -13.561 / -13.826 |
| 9029 | -94.4411 | -94.7449 | -94.4449 | -0.3038 | -0.3000 | 753 / 610 / 751 | -13.409 / -13.713 / -13.413 |
| 9030 | -97.2030 | -96.4511 | -97.2972 | +0.7519 | +0.8461 | 364 / 613 / 341 | -14.458 / -13.706 / -14.552 |
| 9031 | -95.4008 | -95.3124 | -95.3024 | +0.0884 | -0.0100 | 538 / 572 / 576 | -13.894 / -13.806 / -13.796 |
| 9032 | stalled | | | | | | |
| 9033 | stalled | | | | | | |
| 9034 | stalled | | | | | | |
| 9035 | -97.3113 | -96.6835 | -97.4010 | +0.6278 | +0.7175 | 365 / 564 / 343 | -14.454 / -13.826 / -14.544 |
| 9036 | stalled | | | | | | |
| 9037 | stalled | | | | | | |
| 9038 | -95.2514 | -95.2234 | -95.1892 | +0.0280 | -0.0342 | 613 / 625 / 640 | -13.706 / -13.678 / -13.644 |
| 9039 | -95.3278 | -95.3761 | -95.3171 | -0.0483 | -0.0590 | 668 / 646 / 673 | -13.582 / -13.630 / -13.571 |
| 9040 | stalled | | | | | | |

The stages before the final one are identical in the three families of a seed (they do not read the list); every run's full result line:

~~~
A0 seed 9002 |G| 160 p2 -3.9046 stages -24.678 -16.985 -13.981 -2.943 -16.017 -6.996 -0.981 -13.806 | succ 572 coll 572 | log2q -96.3864
P1 seed 9002 |G| 160 p2 -3.9046 stages -24.678 -16.985 -13.981 -2.943 -16.017 -6.996 -0.981 -13.793 | succ 577 coll 577 | log2q -96.3739
A0sel seed 9002 |G| 160 p2 -3.9046 stages -24.678 -16.985 -13.981 -2.943 -16.017 -6.996 -0.981 -13.844 | succ 557 coll 557 | log2q -96.4248
A0 seed 9003 |G| 160 p2 -3.9013 stages -24.678 -17.058 -14.005 -3.050 -14.993 -6.982 -1.022 -14.362 | succ 389 coll 389 | log2q -96.1507
P1 seed 9003 |G| 160 p2 -3.9013 stages -24.678 -17.058 -14.005 -3.050 -14.993 -6.982 -1.022 -13.704 | succ 614 coll 614 | log2q -95.4922
A0sel seed 9003 |G| 160 p2 -3.9013 stages -24.678 -17.058 -14.005 -3.050 -14.993 -6.982 -1.022 -14.211 | succ 432 coll 432 | log2q -95.9994
A0 seed 9004 |G| 160 p2 -3.9030 stages -24.678 -16.963 -14.016 -2.992 -13.979 -6.995 -1.000 -13.773 | succ 585 coll 585 | log2q -94.3962
P1 seed 9004 |G| 160 p2 -3.9030 stages -24.678 -16.963 -14.016 -2.992 -13.979 -6.995 -1.000 -13.669 | succ 629 coll 629 | log2q -94.2916
A0sel seed 9004 |G| 160 p2 -3.9030 stages -24.678 -16.963 -14.016 -2.992 -13.979 -6.995 -1.000 -13.803 | succ 573 coll 573 | log2q -94.4261
A0 seed 9005 |G| 160 p2 -3.9077 stages -24.678 -17.032 -13.944 -3.022 -14.933 -6.993 -0.987 -13.989 | succ 504 coll 504 | log2q -95.5768
P1 seed 9005 |G| 160 p2 -3.9077 stages -24.678 -17.032 -13.944 -3.022 -14.933 -6.993 -0.987 -13.943 | succ 520 coll 520 | log2q -95.5317
A0sel seed 9005 |G| 160 p2 -3.9077 stages -24.678 -17.032 -13.944 -3.022 -14.933 -6.993 -0.987 -13.966 | succ 512 coll 512 | log2q -95.5541
A0 seed 9006 |G| 160 p2 -3.8953 stages -24.678 -16.946 -13.961 -2.994 -14.367 -6.980 -0.988 -14.102 | succ 466 coll 466 | log2q -95.0167
P1 seed 9006 |G| 160 p2 -3.8953 stages -24.678 -16.946 -13.961 -2.994 -14.367 -6.980 -0.988 -13.602 | succ 659 coll 659 | log2q -94.5167
A0sel seed 9006 |G| 160 p2 -3.8953 stages -24.678 -16.946 -13.961 -2.994 -14.367 -6.980 -0.988 -14.102 | succ 466 coll 466 | log2q -95.0167
A0 seed 9008 |G| 160 p2 -3.8952 stages -24.678 -17.006 -13.877 -2.978 -15.999 -7.024 -1.009 -13.462 | succ 726 coll 726 | log2q -96.0333
P1 seed 9008 |G| 160 p2 -3.8952 stages -24.678 -17.006 -13.877 -2.978 -15.999 -7.024 -1.009 -13.783 | succ 581 coll 581 | log2q -96.3548
A0sel seed 9008 |G| 160 p2 -3.8952 stages -24.678 -17.006 -13.877 -2.978 -15.999 -7.024 -1.009 -13.494 | succ 710 coll 710 | log2q -96.0655
A0 seed 9009 |G| 160 p2 -3.9039 stages -24.678 -16.912 -13.871 -3.054 -15.923 -6.981 -0.955 -13.624 | succ 649 coll 649 | log2q -95.9975
P1 seed 9009 |G| 160 p2 -3.9039 stages -24.678 -16.912 -13.871 -3.054 -15.923 -6.981 -0.955 -13.591 | succ 664 coll 664 | log2q -95.9645
A0sel seed 9009 |G| 160 p2 -3.9039 stages -24.678 -16.912 -13.871 -3.054 -15.923 -6.981 -0.955 -13.633 | succ 645 coll 645 | log2q -96.0064
A0 seed 9012 |G| 160 p2 -3.8994 stages -24.678 -16.877 -13.945 -2.922 -15.952 -6.977 -1.015 -13.370 | succ 774 coll 774 | log2q -95.7356
P1 seed 9012 |G| 160 p2 -3.8994 stages -24.678 -16.877 -13.945 -2.922 -15.952 -6.977 -1.015 -13.671 | succ 628 coll 628 | log2q -96.0372
A0sel seed 9012 |G| 160 p2 -3.8994 stages -24.678 -16.877 -13.945 -2.922 -15.952 -6.977 -1.015 -13.413 | succ 751 coll 751 | log2q -95.7792
A0 seed 9014 |G| 160 p2 -3.8908 stages -24.678 -17.030 -13.896 -2.972 -15.980 -6.938 -1.041 -13.646 | succ 639 coll 639 | log2q -96.1802
P1 seed 9014 |G| 160 p2 -3.8908 stages -24.678 -17.030 -13.896 -2.972 -15.980 -6.938 -1.041 -13.546 | succ 685 coll 685 | log2q -96.0799
A0sel seed 9014 |G| 160 p2 -3.8908 stages -24.678 -17.030 -13.896 -2.972 -15.980 -6.938 -1.041 -13.597 | succ 661 coll 661 | log2q -96.1314
A0 seed 9015 |G| 160 p2 -3.9127 stages -24.678 -17.015 -14.011 -3.052 -15.966 -7.072 -1.002 -13.957 | succ 515 coll 515 | log2q -96.7525
P1 seed 9015 |G| 160 p2 -3.9127 stages -24.678 -17.015 -14.011 -3.052 -15.966 -7.072 -1.002 -13.876 | succ 545 coll 545 | log2q -96.6709
A0sel seed 9015 |G| 160 p2 -3.9127 stages -24.678 -17.015 -14.011 -3.052 -15.966 -7.072 -1.002 -13.921 | succ 528 coll 528 | log2q -96.7166
A0 seed 9017 |G| 160 p2 -3.8948 stages -24.678 -17.011 -14.006 -2.999 -16.004 -7.040 -1.001 -13.949 | succ 518 coll 518 | log2q -96.6885
P1 seed 9017 |G| 160 p2 -3.8948 stages -24.678 -17.011 -14.006 -2.999 -16.004 -7.040 -1.001 -13.671 | succ 628 coll 628 | log2q -96.4106
A0sel seed 9017 |G| 160 p2 -3.8948 stages -24.678 -17.011 -14.006 -2.999 -16.004 -7.040 -1.001 -14.009 | succ 497 coll 497 | log2q -96.7482
A0 seed 9019 |G| 160 p2 -3.9036 stages -24.678 -17.042 -13.926 -2.976 -14.397 -7.056 -1.016 -14.130 | succ 457 coll 457 | log2q -95.2204
P1 seed 9019 |G| 160 p2 -3.9036 stages -24.678 -17.042 -13.926 -2.976 -14.397 -7.056 -1.016 -13.655 | succ 635 coll 635 | log2q -94.7458
A0sel seed 9019 |G| 160 p2 -3.9036 stages -24.678 -17.042 -13.926 -2.976 -14.397 -7.056 -1.016 -14.074 | succ 475 coll 475 | log2q -95.1646
A0 seed 9020 |G| 160 p2 -3.9033 stages -24.678 -17.026 -14.005 -2.998 -15.989 -6.983 -1.024 -14.053 | succ 482 coll 482 | log2q -96.7554
P1 seed 9020 |G| 160 p2 -3.9033 stages -24.678 -17.026 -14.005 -2.998 -15.989 -6.983 -1.024 -13.500 | succ 707 coll 707 | log2q -96.2027
A0sel seed 9020 |G| 160 p2 -3.9033 stages -24.678 -17.026 -14.005 -2.998 -15.989 -6.983 -1.024 -14.026 | succ 491 coll 491 | log2q -96.7287
A0 seed 9021 |G| 160 p2 -3.8967 stages -24.678 -17.036 -13.984 -2.963 -16.006 -7.019 -0.989 -13.383 | succ 767 coll 767 | log2q -96.0583
P1 seed 9021 |G| 160 p2 -3.8967 stages -24.678 -17.036 -13.984 -2.963 -16.006 -7.019 -0.989 -13.744 | succ 597 coll 597 | log2q -96.4198
A0sel seed 9021 |G| 160 p2 -3.8967 stages -24.678 -17.036 -13.984 -2.963 -16.006 -7.019 -0.989 -13.265 | succ 832 coll 832 | log2q -95.9410
A0 seed 9023 |G| 160 p2 -3.9068 stages -24.678 -16.925 -13.940 -3.063 -15.993 -7.016 -1.013 -13.513 | succ 701 coll 701 | log2q -96.1398
P1 seed 9023 |G| 160 p2 -3.9068 stages -24.678 -16.925 -13.940 -3.063 -15.993 -7.016 -1.013 -13.708 | succ 612 coll 612 | log2q -96.3357
A0sel seed 9023 |G| 160 p2 -3.9068 stages -24.678 -16.925 -13.940 -3.063 -15.993 -7.016 -1.013 -13.791 | succ 578 coll 578 | log2q -96.4181
A0 seed 9026 |G| 160 p2 -3.9019 stages -24.678 -17.043 -13.861 -2.994 -16.036 -6.938 -0.995 -13.680 | succ 624 coll 624 | log2q -96.2255
P1 seed 9026 |G| 160 p2 -3.9019 stages -24.678 -17.043 -13.861 -2.994 -16.036 -6.938 -0.995 -13.442 | succ 736 coll 736 | log2q -95.9874
A0sel seed 9026 |G| 160 p2 -3.9019 stages -24.678 -17.043 -13.861 -2.994 -16.036 -6.938 -0.995 -13.633 | succ 645 coll 645 | log2q -96.1778
A0 seed 9028 |G| 160 p2 -3.9004 stages -24.678 -16.984 -13.957 -2.949 -14.352 -7.036 -1.016 -13.878 | succ 544 coll 544 | log2q -94.8501
P1 seed 9028 |G| 160 p2 -3.9004 stages -24.678 -16.984 -13.957 -2.949 -14.352 -7.036 -1.016 -13.561 | succ 678 coll 678 | log2q -94.5324
A0sel seed 9028 |G| 160 p2 -3.9004 stages -24.678 -16.984 -13.957 -2.949 -14.352 -7.036 -1.016 -13.826 | succ 564 coll 564 | log2q -94.7980
A0 seed 9029 |G| 160 p2 -3.9043 stages -24.678 -16.971 -13.919 -3.023 -14.374 -7.030 -1.038 -13.409 | succ 753 coll 753 | log2q -94.4411
P1 seed 9029 |G| 160 p2 -3.9043 stages -24.678 -16.971 -13.919 -3.023 -14.374 -7.030 -1.038 -13.713 | succ 610 coll 610 | log2q -94.7449
A0sel seed 9029 |G| 160 p2 -3.9043 stages -24.678 -16.971 -13.919 -3.023 -14.374 -7.030 -1.038 -13.413 | succ 751 coll 751 | log2q -94.4449
A0 seed 9030 |G| 160 p2 -3.9052 stages -24.678 -17.138 -13.948 -3.023 -15.941 -7.016 -1.001 -14.458 | succ 364 coll 364 | log2q -97.2030
P1 seed 9030 |G| 160 p2 -3.9052 stages -24.678 -17.138 -13.948 -3.023 -15.941 -7.016 -1.001 -13.706 | succ 613 coll 613 | log2q -96.4511
A0sel seed 9030 |G| 160 p2 -3.9052 stages -24.678 -17.138 -13.948 -3.023 -15.941 -7.016 -1.001 -14.552 | succ 341 coll 341 | log2q -97.2972
A0 seed 9031 |G| 160 p2 -3.9026 stages -24.678 -17.015 -13.832 -3.001 -14.982 -7.032 -0.967 -13.894 | succ 538 coll 538 | log2q -95.4008
P1 seed 9031 |G| 160 p2 -3.9026 stages -24.678 -17.015 -13.832 -3.001 -14.982 -7.032 -0.967 -13.806 | succ 572 coll 572 | log2q -95.3124
A0sel seed 9031 |G| 160 p2 -3.9026 stages -24.678 -17.015 -13.832 -3.001 -14.982 -7.032 -0.967 -13.796 | succ 576 coll 576 | log2q -95.3024
A0 seed 9035 |G| 160 p2 -3.8993 stages -24.678 -17.150 -14.011 -2.981 -15.991 -7.061 -0.986 -14.454 | succ 365 coll 365 | log2q -97.3113
P1 seed 9035 |G| 160 p2 -3.8993 stages -24.678 -17.150 -14.011 -2.981 -15.991 -7.061 -0.986 -13.826 | succ 564 coll 564 | log2q -96.6835
A0sel seed 9035 |G| 160 p2 -3.8993 stages -24.678 -17.150 -14.011 -2.981 -15.991 -7.061 -0.986 -14.544 | succ 343 coll 343 | log2q -97.4010
A0 seed 9038 |G| 160 p2 -3.8994 stages -24.678 -16.957 -13.848 -3.080 -15.023 -6.968 -0.991 -13.706 | succ 613 coll 613 | log2q -95.2514
P1 seed 9038 |G| 160 p2 -3.8994 stages -24.678 -16.957 -13.848 -3.080 -15.023 -6.968 -0.991 -13.678 | succ 625 coll 625 | log2q -95.2234
A0sel seed 9038 |G| 160 p2 -3.8994 stages -24.678 -16.957 -13.848 -3.080 -15.023 -6.968 -0.991 -13.644 | succ 640 coll 640 | log2q -95.1892
A0 seed 9039 |G| 160 p2 -3.8977 stages -24.678 -17.039 -13.979 -2.975 -14.988 -7.056 -1.030 -13.582 | succ 668 coll 668 | log2q -95.3278
P1 seed 9039 |G| 160 p2 -3.8977 stages -24.678 -17.039 -13.979 -2.975 -14.988 -7.056 -1.030 -13.630 | succ 646 coll 646 | log2q -95.3761
A0sel seed 9039 |G| 160 p2 -3.8977 stages -24.678 -17.039 -13.979 -2.975 -14.988 -7.056 -1.030 -13.571 | succ 673 coll 673 | log2q -95.3171
~~~

## Appendix Q. The base q3_model: records reproduced from the public proof of e4243e7a (Jbenisek)

Reproduced verbatim as data from the public proof.md of e4243e7a-4f8b-42b6-a64a-e70b2dbe1586 (sha256 9d821b2638253c739eb6e68436e921a47d72625d3a1b55801d740af10c9f1d67), its Appendix Q (per-seed values of the two runs behind q3_model and their registrations) and its Appendix R.1 (the registrations, methods and amendments of those runs as recorded in 9aaf71a2). The quoted text is enclosed in one text block; nothing in it is changed. "Our" inside the quoted text refers to that author. We did not rerun these studies; q3_model is their registered bound, and our own measurement (Appendix P) only shifts it by a paired difference. The memory figures inside this record (that study's sampled resident sets) describe 9aaf71a2's statistical study, which this procedure does not execute; Section 10 states what the peak covers.

~~~~~~text

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


~~~~~~

## Appendix R. Our exact counts and records (Sections 6, 10, 11)

### R.1 The C1 C2 G window counts

`gwin38 base_S.txt fbc00800 fe808000 043ff800` (own code, Appendix S): |F8| = 68,157,440; for every a1 with C1 and C2 (53,096,854 of 2^32, both members' words) and every 2^25-window k of a0, the number of a0 in the window with W8x = w8(a1) - a0 in F8, by range counts over the sorted F8. Recomputed in small memory by `gwin38lm` (the f-space in 8 chunks of 2^29 words): identical in all 128 windows, |F8| and |C1 and C2| (peak resident set 34512 KiB = 2^25.07 bytes). All 128 window counts:

~~~
0:27917059052385  1:28511247400652  2:29047307906207  3:28679028539700  4:27939369866081  5:27878042675600  6:28188052646845  7:28023511215346
8:27917059052230  9:28511247461158  10:29047307906362  11:28679028479194  12:27939369865926  13:27878067425908  14:28188167220178  15:28023583710804
16:27917059048448  17:28511223980299  18:29047307910144  19:28679051960053  20:27939369862144  21:27878129017801  22:28188314352794  23:28023646110717
24:27917059048448  25:28511223992964  26:29047307910144  27:28679051947388  28:27939369862144  29:27878129160134  30:28188314549094  31:28023646374004
32:27917059048448  33:28511223980299  34:29047307910144  35:28679051960053  36:27939369862144  37:27878238812985  38:28188575891510  39:28023757601009
40:27917059048448  41:28511223992964  42:29047307910144  43:28679051947388  44:27939369862144  45:27878214329924  46:28188462037524  47:28023685553736
48:27917059052385  49:28511247400652  50:29047307906207  51:28679028539700  52:27939369866081  53:27878152470784  54:28188314185561  55:28023622705638
56:27917059052230  57:28511247461158  58:29047307906362  59:28679028479194  60:27939369865926  61:27878152595698  62:28188314708608  63:28023622890536
64:27917059052385  65:28511247400652  66:29047307906207  67:28679028539700  68:27939369866081  69:27878042675600  70:28188052646845  71:28023511215346
72:27917059052230  73:28511247461158  74:29047307906362  75:28679028479194  76:27939369865926  77:27878067425908  78:28188167220178  79:28023583710804
80:27917059048448  81:28511223980299  82:29047307910144  83:28679051960053  84:27939369862144  85:27878129017801  86:28188314352794  87:28023646110717
88:27917059048448  89:28511223992964  90:29047307910144  91:28679051947388  92:27939369862144  93:27878129160134  94:28188314549094  95:28023646374004
96:27917059048448  97:28511223980299  98:29047307910144  99:28679051960053  100:27939369862144  101:27878238812985  102:28188575891510  103:28023757601009
104:27917059048448  105:28511223992964  106:29047307910144  107:28679051947388  108:27939369862144  109:27878214329924  110:28188462037524  111:28023685553736
112:27917059052385  113:28511247400652  114:29047307906207  115:28679028539700  116:27939369866081  117:27878152470784  118:28188314185561  119:28023622705638
120:27917059052230  121:28511247461158  122:29047307906362  123:28679028479194  124:27939369865926  125:27878152595698  126:28188314708608  127:28023622890536
~~~

|F7| = 287,309,824 by enumeration of all 2^32 words (`inF7`); P(C1) = 1/8 (C1 is the 3-bit pattern 101 of E5 = a1 + C5, `selftest` item 4).

### R.2 Our preprocessing records (Sections 10, 11)

P8 and S are our own (1a695f0b). The preprocessing record of our accepted-track package 08e2e0d3 (proof.md at bb9c671, sha256 3b8ce2226b0a1f4e1fe400c9e51c7d947477d835e2c0966ef0524c106e532ea8, Section 11), quoted verbatim:

~~~
preprocessing (single-threaded, sequential stages; peak of the summed resident memory of all processes, sampled every 0.2 s):
  Step-1 solve of P8 (joint.py: Python model + Kissat; the S in use, as in 1a695f0b): 279,720 KB = 2^28.0936
  signed search of P8 (stepk.py): at most 2^27.92
  class descriptors (a0cls.c, 32 hash passes): 37,036 KB = 2^25.14; class selection (lp_classes.py with the a0cls member pass): 46,804 KB = 2^25.48
  condition tables and pair (mkvt.py, fromjoint.py): below 2^24
~~~

The class descriptors and class selection belong to the A0-variant procedure and are not used here. The 279,720 KB of the Step-1 solve is the summed resident memory of the Python model builder and Kissat. 377cb363 reran the same Step-1 model and instance class under RLIMIT_AS = 2^28 and measured 221,076 KB = 2^27.7542; the accepted 7cb739f5 and a32131ff charge that cell, and so do we. Our own rerun (2026-10-17) of the solve alone, on the formula of the deterministic model builder (which admits S), `kissat -q --seed=1 S.cnf`: 18 min 17 s, maximum resident set 70,892 KB = 2^26.08 (`/usr/bin/time -v`). The author's accounting of the whole P8 line (search, S, data and development): one 10-core machine, less than 2^22 core-seconds.

## Appendix S. Sources of the tools behind Appendices H, P and R (own code)

The step 3b routine of `p1b38c.c` is that of our residue-table port `p1t38c.c` (identical source lines).

### `p1b38c.c` (sha256 70e2ce60a214bb9aba88b7e07a742503afdbf99e3d85ec7e3e340366b90bd43c)

~~~c
/* p1b38c.c - C port of the bucket claw of p1b38.py (run_cv without the operation counter), for the full-size panel and the memory
 * measurement (own code).  Per chaining value: reset the 2^23 + 3 bucket words (32 bytes each, lane i < 7 at bits 36i..36i+35: 9-bit tag
 * F mod 512 and 27-bit offset, count at bits 252..254), insert the 2^nc candidates n -> a0 = p(rotr2(n + R mod 2^27)) (first 7 per bucket; R
 * from the 11th column of the cvs file, 0 if absent), scan 2^LU
 * words u = u0 + n: per head the buckets b and b + 2 (and b + 1, b + 3 when w >= 507), the field test of p1b38 (r = t + 512 - w, r - 512 in
 * {0, 1, 4, 5}; straddle r in {0, 1, 4, 5}) on every lane, lanes beyond the count being spurious matches; the four post-filters and step 3b
 * on every good pair.  Reports per chaining value: stored lanes, claws, expected claws (2^LU x 160 x stored / 2^32 / 512 x 512), stage
 * counts, spurious matches, straddling words, good pairs sharing an a0 or a u, E16 check, step 3b rows, and (ref = 1) the claws of an
 * independent sorted search.  GOODF: every good pair; CLAWF: every claw (for the cross-check).  Prints VmHWM at the end.
 * usage: p1b38c <cvs file> <nc> <LU> <ref 0|1> [first j] [count] */
#include <stdio.h>
#include <stdint.h>
#include <stdlib.h>
#include <string.h>
typedef uint32_t u32; typedef uint64_t u64;
#include "p1tconst.h"
#define ROR(x, n) (((x) >> (n)) | ((x) << (32 - (n))))
static inline u32 S0(u32 x) { return ROR(x, 2) ^ ROR(x, 13) ^ ROR(x, 22); }
static inline u32 S1(u32 x) { return ROR(x, 6) ^ ROR(x, 11) ^ ROR(x, 25); }
static inline u32 s0(u32 x) { return ROR(x, 7) ^ ROR(x, 18) ^ (x >> 3); }
static inline u32 CH(u32 x, u32 y, u32 z) { return (x & y) ^ (~x & z); }
static inline u32 MAJ(u32 x, u32 y, u32 z) { return (x & y) ^ (x & z) ^ (y & z); }
typedef struct { u32 k0, E0b, PP, QQ, EF, FF, KF, K2, KK7; } Cvc;
static void cvc(const u32 *cv, Cvc *c) {
    u32 a = cv[0], b = cv[1], cc = cv[2], d = cv[3], e = cv[4], f = cv[5], g = cv[6], h = cv[7];
    c->k0 = 0u - S0(a) - MAJ(a, b, cc) - h - S1(e) - CH(e, f, g) - K0;
    c->E0b = d - S0(a) - MAJ(a, b, cc); c->PP = a & b; c->QQ = a | b; c->EF = e ^ f; c->FF = f;
    c->KF = CC2 + c->k0 - g - K1; c->K2 = CC2 + c->k0; c->KK7 = SE7 - 2 * SA3 - a + S0(SA2) - S1(SE6) - K7;
}
static inline u32 Ffun(const Cvc *c, u32 a0) { u32 E0 = a0 + c->E0b; return a0 + c->KF - S0(a0) - (c->PP | (a0 & c->QQ)) - S1(E0) - (c->FF ^ (E0 & c->EF)); }
static inline u32 p_a0(u32 o) { return (o & 0x1ffffffu) | PBASE | ((o >> 25) << 28); }
static inline u32 rotr2(u32 n) { return (n >> 2) | ((n & 3u) << 25); }
#define OMASK 0x7ffffffu
static int pf(const Cvc *c, u32 a0, u32 a1) {
    u32 E5 = a1 + C5; if ((E5 & C1MASK) != C1V) return 0;
    u32 w9 = CW9 - a1; if ((u32)(s0(w9 + D9) - s0(w9)) != T9) return 1;
    u32 E4 = a0 + CE4 - (MA | (a1 & MB)), w8 = KW8 - E4 - (CA ^ (CB & E5)); if ((u32)(s0(w8 + D8) - s0(w8)) != T8) return 2;
    u32 w7 = c->KK7 + MAJ(SA2, a1, a0) - CH(SE6, E5, E4); if ((u32)(s0(w7 + D7) - s0(w7)) != T7) return 3;
    return 4;
}
static void pair_words(const u32 *cv, u32 a0, u32 a1, u32 W[2][16]) {
    for (int m = 0; m < 2; m++) {
        u32 A[20], E[20];   /* index i + 4 */
        for (int i = 0; i < 4; i++) { A[3 - i] = cv[i]; E[3 - i] = cv[4 + i]; }
        A[4] = a0; A[5] = a1; for (int i = 2; i < 16; i++) A[i + 4] = SAv[m][i];
        for (int i = 0; i < 6; i++) E[i + 4] = A[i + 4] + A[i] - S0(A[i + 3]) - MAJ(A[i + 3], A[i + 2], A[i + 1]);
        for (int i = 6; i < 16; i++) E[i + 4] = SEv[m][i];
        for (int i = 0; i < 16; i++) W[m][i] = E[i + 4] - A[i] - E[i] - S1(E[i + 3]) - CH(E[i + 3], E[i + 2], E[i + 1]) - KK[i];
    }
}
static inline u32 s1f(u32 x) { return ROR(x, 17) ^ ROR(x, 19) ^ (x >> 10); }
static void trace38(const u32 *cv, const u32 *w16, u32 T[3][42]) {   /* T[0] = A, T[1] = E (index i + 4), T[2] = W (index i) */
    u32 *A = T[0], *E = T[1], *W = T[2];
    for (int i = 0; i < 16; i++) W[i] = w16[i];
    for (int i = 16; i < 38; i++) W[i] = s1f(W[i - 2]) + W[i - 7] + s0(W[i - 15]) + W[i - 16];
    for (int i = 0; i < 4; i++) { A[3 - i] = cv[i]; E[3 - i] = cv[4 + i]; }
    for (int i = 0; i < 38; i++) {
        E[i + 4] = A[i] + E[i] + S1(E[i + 3]) + CH(E[i + 3], E[i + 2], E[i + 1]) + KK[i] + W[i];
        A[i + 4] = E[i + 4] - A[i] + S0(A[i + 3]) + MAJ(A[i + 3], A[i + 2], A[i + 1]);
    }
}
static inline u32 TV(u32 T[3][42], int k, int i) { return k < 2 ? T[k][i + 4] : T[2][i]; }
static int rowtest(u32 tx[3][42], u32 ty[3][42], int i) {
    for (int k = 0; k < 3; k++) { u32 x = TV(tx, k, i), y = TV(ty, k, i);
        if ((x & CELLv[k][i][0]) != CELLv[k][i][1] || (x ^ y) != CELLv[k][i][2]) return 0; }
    if ((TV(tx, 1, i) ^ TV(tx, 1, i - 1)) & PQEv[i]) return 0;
    for (int t = 0; t < NX2; t++) { const int *c = X2v[t];
        if (c[7] == i && (((TV(tx, c[0], c[1]) >> c[2]) ^ (TV(tx, c[4], c[5]) >> c[6])) & 1) != (c[3] ? 0u : 1u)) return 0; }
    return 1;
}
static int step3b(const u32 *cv, u32 a0, u32 a1) {
    u32 W[2][16], tx[3][42], ty[3][42]; pair_words(cv, a0, a1, W); trace38(cv, W[0], tx); trace38(cv, W[1], ty);
    for (int i = 16; i < 22; i++) if (!rowtest(tx, ty, i)) return i - 16;
    for (int i = 34; i < 38; i++) if (tx[0][i + 4] != ty[0][i + 4] || tx[1][i + 4] != ty[1][i + 4]) return 6;
    return 7;
}

static int in160(u32 x) { int lo = 0, hi = 160; while (lo < hi) { int m = (lo + hi) / 2; if (S160[m] < x) lo = m + 1; else hi = m; } return lo < 160 && S160[lo] == x; }
static int cmpu(const void *a, const void *b) { u32 x = *(const u32 *)a, y = *(const u32 *)b; return x < y ? -1 : x > y; }
static long vmhwm(void) { FILE *f = fopen("/proc/self/status", "r"); char l[256]; long v = -1; while (f && fgets(l, sizeof l, f)) if (!strncmp(l, "VmHWM:", 6)) v = atol(l + 6); if (f) fclose(f); return v; }
#define NBK (1u << 23)
static u64 *T;                                   /* (NBK + 3) words of 4 x u64, little-endian bit order: bit k of the word = bit k % 64 of T[4b + k / 64] */
static inline u64 getbits(const u64 *w, int pos, int len) { int q = pos >> 6, r = pos & 63; u64 v = w[q] >> r; if (r + len > 64) v |= w[q + 1] << (64 - r); return v & ((len == 64) ? ~0ull : ((1ull << len) - 1)); }
static inline void orbits(u64 *w, int pos, u64 v) { int q = pos >> 6, r = pos & 63; w[q] |= v << r; if (r && r + 36 > 64) w[q + 1] |= v >> (64 - r); }
static inline int count_of(const u64 *w) { return (int)((w[3] >> 60) & 7); }
int main(int argc, char **argv) {
    if (!strcmp(argv[1], "-t")) {   /* step 3b test mode, as p1t38c */
        u32 v[10]; while (scanf("%x %x %x %x %x %x %x %x %x %x", &v[0], &v[1], &v[2], &v[3], &v[4], &v[5], &v[6], &v[7], &v[8], &v[9]) == 10) printf("%d\n", step3b(v, v[8], v[9]));
        return 0;
    }
    FILE *fc = fopen(argv[1], "r"); int nc = atoi(argv[2]), LU = atoi(argv[3]), ref = atoi(argv[4]);
    int j0 = argc > 5 ? atoi(argv[5]) : 0, nj = argc > 6 ? atoi(argv[6]) : 1 << 30;
    u64 NC = 1ull << nc;
    T = malloc((size_t)(NBK + 3) * 32);
    u32 *vis = ref ? malloc(sizeof(u32) * (size_t)NBK * 7) : 0;
    u32 *good = malloc(sizeof(u32) * (1 << 20)), *goodu = malloc(sizeof(u32) * (1 << 20));
    u32 DH[20]; for (int h = 0; h < 20; h++) DH[h] = (HEADS[h] - HEADS[0]) >> 9;
    int j; u32 cv[8], u0, R; char line[512];
    FILE *gf = getenv("GOODF") ? fopen(getenv("GOODF"), "w") : 0, *cf = getenv("CLAWF") ? fopen(getenv("CLAWF"), "w") : 0;
    printf("# step 3b on the S pair: %d (7 = accepted)\n", step3b(PCVv, SAv[0][0], SAv[0][1]));
    printf("# j stored claws expected c1 c1c2 c1c2g all4 spurious strad good_shared_a0 good_shared_u bad_e16 refclaws step3b_rows16..21_passed accepted\n");
    while (fgets(line, sizeof line, fc)) {
        R = 0; if (sscanf(line, "%d %x %x %x %x %x %x %x %x %x %x", &j, &cv[0], &cv[1], &cv[2], &cv[3], &cv[4], &cv[5], &cv[6], &cv[7], &u0, &R) < 10) continue;
        if (j < j0) continue;
        if (j >= j0 + nj) break;
        Cvc c; cvc(cv, &c);
        memset(T, 0, (size_t)(NBK + 3) * 32);
        for (u64 n = 0; n < NC; n++) {
            u32 o = rotr2(((u32)n + R) & OMASK), a0 = p_a0(o), F = Ffun(&c, a0), b = F >> 9; u64 *w = T + 4 * (u64)b; int cnt = count_of(w);
            if (cnt < 7) { orbits(w, 36 * cnt, ((u64)o << 9) | (F & 511)); w[3] += 1ull << 60; if (b < 3) memcpy(T + 4 * (u64)(NBK + b), w, 32); }
        }
        u64 stored = 0, nvis = 0;
        for (u64 b = 0; b < NBK; b++) { const u64 *w = T + 4 * b; int cnt = count_of(w); stored += cnt;
            if (ref) for (int i = 0; i < cnt; i++) vis[nvis++] = (u32)(b << 9) | (u32)(getbits(w, 36 * i, 9)); }
        if (ref) qsort(vis, nvis, 4, cmpu);
        u64 claws = 0, st[4] = {0, 0, 0, 0}, spur = 0, strad = 0, bad = 0, refc = 0, ng = 0, rows[7] = {0, 0, 0, 0, 0, 0, 0}, acc = 0;
        for (u64 n = 0; n < (1ull << LU); n++) {
            u32 u = u0 + (u32)n, P = s0(u) - u, W0 = HEADS[0] - P, w = W0 & 511, b0 = W0 >> 9;
            int sd = w >= 507; strad += sd;
            for (int h = 0; h < 20; h++) {
                u32 bh = (b0 + DH[h]) & (NBK - 1);
                for (int pass = 0; pass < 1 + sd; pass++)
                    for (int f = 0; f < 2; f++) {
                        u32 bk = bh + 2 * f + pass; const u64 *wd = T + 4 * (u64)bk; int cnt = count_of(wd);
                        for (int i = 0; i < 7; i++) {
                            u64 e = getbits(wd, 36 * i, 36); u32 t = (u32)(e & 511), r = t + 512 - w;
                            int hit = pass == 0 ? (r >= 512 && ((r - 512) & ~5u) == 0) : (r < 512 && (r & ~5u) == 0);
                            if (!hit) continue;
                            if (i >= cnt) { spur++; continue; }
                            u32 o = (u32)(e >> 9), a0 = p_a0(o), F = (((bk & (NBK - 1)) << 9) | t), a1 = u - F + c.K2 + a0; claws++;
                            if (!in160(F + s0(u) - u)) bad++;
                            if (cf) fprintf(cf, "%d %08x %08x %08x\n", j, a0, a1, u);
                            int p = pf(&c, a0, a1); for (int q = 0; q < p; q++) st[q]++;
                            if (p == 4) { if (ng < (1 << 20)) { goodu[ng] = u; good[ng++] = a0; } int rr = step3b(cv, a0, a1); if (gf) fprintf(gf, "%d %08x %08x %08x %d\n", j, a0, a1, u, rr); for (int q = 0; q < rr && q < 6; q++) rows[q]++; acc += rr == 7; }
                        }
                    }
            }
            if (ref) for (int hh = 0; hh < 160; hh++) { u32 want = S160[hh] - P; u64 lo = 0, hi = nvis; while (lo < hi) { u64 m = (lo + hi) / 2; if (vis[m] < want) lo = m + 1; else hi = m; } while (lo < nvis && vis[lo] == want) { refc++; lo++; } }
        }
        qsort(good, ng, 4, cmpu); u64 shared = 0; for (u64 k = 1; k < ng; k++) if (good[k] == good[k - 1]) shared++;
        qsort(goodu, ng, 4, cmpu); u64 sharedu = 0; for (u64 k = 1; k < ng; k++) if (goodu[k] == goodu[k - 1]) sharedu++;
        double expc = (double)(1ull << LU) * 160.0 * (double)stored / 4294967296.0;
        printf("%d %llu %llu %.1f %llu %llu %llu %llu %llu %llu %llu %llu %llu %lld %llu %llu %llu %llu %llu %llu %llu\n", j, (unsigned long long)stored,
               (unsigned long long)claws, expc, (unsigned long long)st[0], (unsigned long long)st[1], (unsigned long long)st[2], (unsigned long long)st[3],
               (unsigned long long)spur, (unsigned long long)strad, (unsigned long long)shared, (unsigned long long)sharedu, (unsigned long long)bad, ref ? (long long)refc : -1LL,
               (unsigned long long)rows[0], (unsigned long long)rows[1], (unsigned long long)rows[2], (unsigned long long)rows[3], (unsigned long long)rows[4], (unsigned long long)rows[5], (unsigned long long)acc);
        fflush(stdout);
    }
    if (gf) fclose(gf);
    if (cf) fclose(cf);
    printf("# peak resident set VmHWM %ld KiB\n", vmhwm());
    return 0;
}
~~~

### `xcheck_b.py` (sha256 2c430fd990277107519b7071bb9f9f91f8a4e970d03ac438f849603d0604047d)

~~~python
"""xcheck_b.py - runs p1b38.run_cv on the chaining values of a cvs file and writes every claw (j a0 a1 u) and the per-value counts in the
order of p1b38c (own code).  usage: python3 xcheck_b.py <cvs file> <nc> <LU> <first j> <count> <claws out>"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
import p1b38 as P
f, nc, LU, j0, nj, out = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4]), int(sys.argv[5]), sys.argv[6]
with open(out, 'w') as fo:
    for line in open(f):
        t = line.split(); j = int(t[0])
        if j < j0 or j >= j0 + nj: continue
        cv = [int(x, 16) for x in t[1:9]]; u0 = int(t[9], 16); R = int(t[10], 16) if len(t) > 10 else 0
        st = P.run_cv(cv, LU, nc=nc, count=False, ref=True, collect=True, u0=u0, R=R)
        for a0, a1, u, fl in st['allclaws']: fo.write('%d %08x %08x %08x\n' % (j, a0, a1, u))
        print(j, st['stored'], st['claws'], *st['passes'], st['spurious'], st['strad'], st['refclaws'])
~~~

### `mkcvs_r.py` (sha256 f47ec8de2d2950647bb0bd5846591a6f68f9be3374ea65e9eabc82644c3d1b3e)

~~~python
"""mkcvs_r.py - chaining values with u0 and the insertion rotation R for p1b38c (own code).  For j = 0 .. n-1: the first block of
Shake('<label>|<j>'), its 38-step chaining value, u0 = the next u32 and R = the following u32 mod 2^27 (as in p1b38.online_experiment).
usage: python3 mkcvs_r.py <n> <label> <out>"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
import p1b38 as P
n, lab, out = int(sys.argv[1]), sys.argv[2], sys.argv[3]
with open(out, 'w') as f:
    for j in range(n):
        rng = P.Shake('%s|%d' % (lab, j)); M0, cv = P.first_block(rng); u0 = rng.u32(); R = rng.u32() & P.OMASK
        f.write('%d %s %08x %07x\n' % (j, ' '.join('%08x' % x for x in cv), u0, R))
print('wrote %d chaining values to %s' % (n, out))
~~~

### `q3tv3.c` (sha256 65260652429ace66b1bae67d04e36f74d3c80274920f9b41c75645f82bff1496)

~~~c
// Trail-based estimator of the uncontrolled probability of a 38-step SHA-256 characteristic (own code).
// q3tv3: q3tv with the shared prefix (rows 16..22) run once and the final stage run once per variant list from the same generator
// state, giving the output of three separate q3tv runs (usage: q3tv3 <datafile> <seed> <N> <T> <vars1> <out1> <vars2> <out2> <vars3> <out3>).
// q3tv: q3t with the tail drawing a dense-part variant per proposal (env VARS = vsamp output: j a0 a1 a2 w8x w9x w10x;
// member y gets w + dW_i of the base pair) and every success written to env DUMPALL (variant index, W7..W37 of member x).
// q = Pr[rows 16..37 follow the signed trail | dense part, W7 in F7], W0..W6 uniform (Lemma 4 structure).
// Input file (text, hex words): see prep.py. Usage: q3t <datafile> <seed> <N> <T> [g-cache]
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>
#include <stdint.h>
typedef uint32_t u32;
static const u32 K[64] = {
 0x428a2f98,0x71374491,0xb5c0fbcf,0xe9b5dba5,0x3956c25b,0x59f111f1,0x923f82a4,0xab1c5ed5,0xd807aa98,0x12835b01,0x243185be,0x550c7dc3,0x72be5d74,0x80deb1fe,0x9bdc06a7,0xc19bf174,
 0xe49b69c1,0xefbe4786,0x0fc19dc6,0x240ca1cc,0x2de92c6f,0x4a7484aa,0x5cb0a9dc,0x76f988da,0x983e5152,0xa831c66d,0xb00327c8,0xbf597fc7,0xc6e00bf3,0xd5a79147,0x06ca6351,0x14292967,
 0x27b70a85,0x2e1b2138,0x4d2c6dfc,0x53380d13,0x650a7354,0x766a0abb,0x81c2c92e,0x92722c85,0xa2bfe8a1,0xa81a664b,0xc24b8b70,0xc76c51a3,0xd192e819,0xd6990624,0xf40e3585,0x106aa070};
static inline u32 ror(u32 x, int n) { return (x >> n) | (x << (32 - n)); }
static inline u32 S0(u32 x) { return ror(x, 2) ^ ror(x, 13) ^ ror(x, 22); }
static inline u32 S1(u32 x) { return ror(x, 6) ^ ror(x, 11) ^ ror(x, 25); }
static inline u32 s0(u32 x) { return ror(x, 7) ^ ror(x, 18) ^ (x >> 3); }
static inline u32 s1(u32 x) { return ror(x, 17) ^ ror(x, 19) ^ (x >> 10); }
static inline u32 CH(u32 x, u32 y, u32 z) { return (x & y) ^ (~x & z); }
static inline u32 MAJ(u32 x, u32 y, u32 z) { return (x & y) ^ (x & z) ^ (y & z); }
static uint64_t rs[4];
static inline uint64_t rotl(uint64_t x, int k) { return (x << k) | (x >> (64 - k)); }
static uint64_t nxt(void) { uint64_t r = rotl(rs[1] * 5, 7) * 9, t = rs[1] << 17; rs[2] ^= rs[0]; rs[3] ^= rs[1]; rs[1] ^= rs[2]; rs[0] ^= rs[3]; rs[2] ^= t; rs[3] = rotl(rs[3], 45); return r; }
static void seed(uint64_t s) { for (int i = 0; i < 4; i++) { s += 0x9e3779b97f4a7c15ULL; uint64_t z = s; z = (z ^ (z >> 30)) * 0xbf58476d1ce4e5b9ULL; z = (z ^ (z >> 27)) * 0x94d049bb133111ebULL; rs[i] = z ^ (z >> 31); } }
static inline u32 r32(void) { return (u32)(nxt() >> 32); }

typedef struct { u32 A[2][42], E[2][42], W[2][38]; } St;     // A/E index +4
#define AA(s, m, i) (s)->A[m][(i) + 4]
#define EE(s, m, i) (s)->E[m][(i) + 4]
static u32 MA[38], SA[38], ME[38], SE[38], MW[38], SW[38];   // trail: xor mask and x-value on the mask, rows 0..37
static St base; static u32 D7, T7;
typedef struct { int key, n, kind[3], row[3], bit[3]; u32 allowed; } Cond;
static Cond CO[8192]; static int nCO;
static u32 (*VW)[4]; static long nV;

static inline void step(St *s, int i) {
    for (int m = 0; m < 2; m++) {
        u32 a = AA(s, m, i - 1), b = AA(s, m, i - 2), c = AA(s, m, i - 3), d = AA(s, m, i - 4);
        u32 e = EE(s, m, i - 1), f = EE(s, m, i - 2), g = EE(s, m, i - 3), h = EE(s, m, i - 4);
        u32 T1 = h + S1(e) + CH(e, f, g) + K[i] + s->W[m][i];
        EE(s, m, i) = d + T1; AA(s, m, i) = T1 + S0(a) + MAJ(a, b, c);
    }
}
static inline int condok(const St *s, int r) {
    for (int c = 0; c < nCO; c++) {
        if (CO[c].key != r) continue;
        int idx = 0;
        for (int q = 0; q < CO[c].n; q++) { u32 w = CO[c].kind[q] == 2 ? s->W[0][CO[c].row[q]] : CO[c].kind[q] ? EE(s, 0, CO[c].row[q]) : AA(s, 0, CO[c].row[q]); idx |= ((w >> CO[c].bit[q]) & 1) << q; }
        if (!((CO[c].allowed >> idx) & 1)) return 0;
    }
    return 1;
}
static inline int rowok(const St *s, int r) {
    u32 ax = AA(s, 0, r), ex = EE(s, 0, r), wx = s->W[0][r];
    static long dfm = -1;   // DIFFROW=r[,r...]: these rows checked on signed differences only (no derived value conditions)
    if (dfm < 0) { dfm = 0; const char *e = getenv("DIFFROW"); while (e && *e) { int v = atoi(e); if (v > 0) dfm |= 1L << v; while (*e && *e != ',') e++; if (*e) e++; } }
    if (!((dfm >> r) & 1) && !condok(s, r)) return 0;
    return ((ax ^ AA(s, 1, r)) == MA[r]) && ((ax & MA[r]) == SA[r]) && ((ex ^ EE(s, 1, r)) == ME[r]) && ((ex & ME[r]) == SE[r])
        && ((wx ^ s->W[1][r]) == MW[r]) && ((wx & MW[r]) == SW[r]);
}
static inline void sched(St *s, int i) { for (int m = 0; m < 2; m++) s->W[m][i] = s1(s->W[m][i - 2]) + s->W[m][i - 7] + s0(s->W[m][i - 15]) + s->W[m][i - 16]; }
static inline int inF7(u32 w) { return s0(w + D7) - s0(w) == T7; }

static void load(const char *fn) {
    FILE *f = fopen(fn, "r"); if (!f) { perror(fn); exit(1); }
    char key[32];
    while (fscanf(f, "%31s", key) == 1) {
        if (!strcmp(key, "D7")) fscanf(f, "%x", &D7);
        else if (!strcmp(key, "T7")) fscanf(f, "%x", &T7);
        else if (!strcmp(key, "ROW")) { int r; u32 a, b, c, d, e, g; fscanf(f, "%d %x %x %x %x %x %x", &r, &a, &b, &c, &d, &e, &g); MA[r] = a; SA[r] = b; ME[r] = c; SE[r] = d; MW[r] = e; SW[r] = g; }
        else if (!strcmp(key, "ST")) { int m, i; u32 a, e; fscanf(f, "%d %d %x %x", &m, &i, &a, &e); AA(&base, m, i) = a; EE(&base, m, i) = e; }
        else if (!strcmp(key, "COND")) { Cond *c = &CO[nCO++]; fscanf(f, "%d %d", &c->key, &c->n); for (int q = 0; q < c->n; q++) fscanf(f, "%d %d %d", &c->kind[q], &c->row[q], &c->bit[q]); fscanf(f, "%x", &c->allowed); }
        else if (!strcmp(key, "W")) { int m, i; u32 w; fscanf(f, "%d %d %x", &m, &i, &w); base.W[m][i] = w; }
    }
    fclose(f);
}

int main(int argc, char **argv) {
    load(argv[1]); uint64_t sd = strtoull(argv[2], 0, 10); int N = atoi(argv[3]), T = atoi(argv[4]);
    seed(sd);
    u32 dW16 = (s1(base.W[1][14]) + base.W[1][9]) - (s1(base.W[0][14]) + base.W[0][9]);   // W0, W1 carry no difference
    // row 16 exhaustive (cached)
    static u32 G[1 << 20]; long nG = 0;
    char cache[512]; snprintf(cache, sizeof cache, "%s.g16", argv[1]);
    FILE *fc = fopen(cache, "rb");
    if (fc) { nG = fread(G, 4, 1 << 20, fc); fclose(fc); }
    else {
        for (uint64_t w = 0; w < (1ULL << 32); w++) {
            St s; memcpy(s.A, base.A, sizeof s.A); memcpy(s.E, base.E, sizeof s.E);
            s.W[0][16] = (u32)w; s.W[1][16] = (u32)w + dW16; step(&s, 16);
            if (rowok(&s, 16)) { if (nG < (1 << 20)) G[nG] = (u32)w; nG++; }
        }
        if (nG > (1 << 20)) { fprintf(stderr, "G too large %ld\n", nG); nG = 1 << 20; }
        fc = fopen(cache, "wb"); fwrite(G, 4, nG, fc); fclose(fc);
    }
    if (0) {   // row-17 pass counts per G word (sampled W17)
        int live = 0; uint64_t S = 1ULL << 24;
        for (long gi = 0; gi < nG; gi++) {
            St s = base; s.W[0][16] = G[gi]; s.W[1][16] = G[gi] + dW16; step(&s, 16);
            uint64_t pass = 0;
            for (uint64_t k = 0; k < S; k++) {
                St t = s; u32 wx = r32();
                u32 dsch = (s1(t.W[1][15]) + t.W[1][10]) - (s1(t.W[0][15]) + t.W[0][10]) + s0(t.W[1][2]) - s0(t.W[0][2]);
                t.W[0][17] = wx; t.W[1][17] = wx + dsch; step(&t, 17); pass += rowok(&t, 17);
            }
            live += pass > 0;
            printf("G %08x row17 passes %llu / 2^24\n", G[gi], (unsigned long long)pass);
        }
        printf("live G words: %d of %ld\n", live, nG); return 0;
    }
    uint64_t f7 = 0; for (int k = 0; k < 1 << 20; k++) f7 += inF7(r32());
    double lv[8]; lv[0] = nG ? log2((double)nG) - 32 : -INFINITY;
    if (!nG) { printf("seed %llu row16 impossible\n", (unsigned long long)sd); return 0; }
    St *cur = malloc(sizeof(St) * N), *nx = malloc(sizeof(St) * N); int ncur = N;
    for (int k = 0; k < N; k++) { St s = base; u32 w = G[nxt() % nG]; s.W[0][16] = w; s.W[1][16] = w + dW16; step(&s, 16); cur[k] = s; }
    for (int r = 17; r <= 22; r++) {
        uint64_t tries = 0; int got = 0;
        while (got < N) {
            if (tries > (1ULL << 34)) { for (int v = 0; v < 3; v++) { FILE *fo = fopen(argv[6 + 2 * v], "w"); fprintf(fo, "seed %llu stalled at row %d\n", (unsigned long long)sd, r); fclose(fo); } return 0; }
            const St *p = &cur[nxt() % ncur]; tries++;
            u32 wx = r32();
            u32 dsch = (s1(p->W[1][r - 2]) + p->W[1][r - 7]) - (s1(p->W[0][r - 2]) + p->W[0][r - 7]);
            if (r == 22) dsch += T7; else dsch += s0(p->W[1][r - 15]) - s0(p->W[0][r - 15]);
            St s = *p; s.W[0][r] = wx; s.W[1][r] = wx + dsch; step(&s, r);
            if (rowok(&s, r)) nx[got++] = s;
        }
        lv[r - 16] = log2((double)(N - 1) / (double)(tries - 1));
        St *t = cur; cur = nx; nx = t;
    }
    uint64_t rs0[4]; memcpy(rs0, rs, sizeof rs0);                // the generator state after the shared prefix
    double lv7[3];
    for (int v = 0; v < 3; v++) {
        memcpy(rs, rs0, sizeof rs0); nV = 0; if (VW) { free(VW); VW = 0; }
        FILE *fo = fopen(argv[6 + 2 * v], "w");
        {
            FILE *fv = fopen(argv[5 + 2 * v], "r"); long cap = 1 << 22; VW = malloc(sizeof(*VW) * cap); int j; u32 a0, a1, a2, w8, w9, w10;
            while (nV < cap && fscanf(fv, "%d %x %x %x %x %x %x", &j, &a0, &a1, &a2, &w8, &w9, &w10) == 7) { VW[nV][0] = (u32)nV; VW[nV][1] = w8; VW[nV][2] = w9; VW[nV][3] = w10; nV++; }
            fclose(fv); fprintf(fo, "variants %ld\n", nV);
        }
        uint64_t prop = (uint64_t)N * T, succ = 0, coll = 0;
        for (uint64_t k = 0; k < prop; k++) {
            St s = cur[k % N]; u32 w7; do w7 = r32(); while (!inF7(w7));
            s.W[0][7] = w7; s.W[1][7] = w7 + D7;
            long vi = -1;
            if (nV) { vi = nxt() % nV; for (int i = 8; i <= 10; i++) { s.W[0][i] = VW[vi][i - 7]; s.W[1][i] = VW[vi][i - 7] + (base.W[1][i] - base.W[0][i]); } }
            int ok = 1;
            static int relax = -1; if (relax < 0) relax = getenv("RELAX_TAIL") != 0;
            for (int r = 23; r < 38 && ok; r++) { sched(&s, r); step(&s, r); if (!relax) ok = rowok(&s, r); }
            if (relax) { for (int i = 34; i < 38 && ok; i++) if (AA(&s, 0, i) != AA(&s, 1, i) || EE(&s, 0, i) != EE(&s, 1, i)) ok = 0; }
            if (ok) {
                succ++;
                int eq = 1; for (int i = 34; i < 38; i++) if (AA(&s, 0, i) != AA(&s, 1, i) || EE(&s, 0, i) != EE(&s, 1, i)) eq = 0;
                coll += eq;
            }
        }
        lv[7] = succ ? log2((double)succ / prop) : -INFINITY; lv7[v] = lv[7];
        double tot = 0; for (int i = 0; i < 8; i++) tot += lv[i];
        fprintf(fo, "seed %llu |G| %ld p2 %.4f stages", (unsigned long long)sd, nG, log2((double)f7 / (1 << 20)));
        for (int i = 0; i < 8; i++) fprintf(fo, " %.3f", lv[i]);
        fprintf(fo, " | succ %llu coll %llu | log2q %.4f%s\n", (unsigned long long)succ, (unsigned long long)coll, tot, nV ? " (variant tail)" : "");
        fclose(fo);
    }
    return 0;
}
~~~

### `q3tv4.c` (sha256 88af9d2486558e9fe6cdff8f712b7b768569eecea36812fbacacb1fa638d1151)

~~~c
// Trail-based estimator of the uncontrolled probability of a 38-step SHA-256 characteristic (own code).
// q3tv4: q3tv3 with the stage tries evaluated without copying the particle (row r computed into locals, the particle copied only when
// accepted); every decision and the generator stream are unchanged, so the outputs are those of q3tv3 and of three q3tv runs.
// q3tv3: q3tv with the shared prefix (rows 16..22) run once and the final stage run once per variant list from the same generator
// state, giving the output of three separate q3tv runs (usage: q3tv3 <datafile> <seed> <N> <T> <vars1> <out1> <vars2> <out2> <vars3> <out3>).
// q3tv: q3t with the tail drawing a dense-part variant per proposal (env VARS = vsamp output: j a0 a1 a2 w8x w9x w10x;
// member y gets w + dW_i of the base pair) and every success written to env DUMPALL (variant index, W7..W37 of member x).
// q = Pr[rows 16..37 follow the signed trail | dense part, W7 in F7], W0..W6 uniform (Lemma 4 structure).
// Input file (text, hex words): see prep.py. Usage: q3t <datafile> <seed> <N> <T> [g-cache]
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>
#include <stdint.h>
typedef uint32_t u32;
static const u32 K[64] = {
 0x428a2f98,0x71374491,0xb5c0fbcf,0xe9b5dba5,0x3956c25b,0x59f111f1,0x923f82a4,0xab1c5ed5,0xd807aa98,0x12835b01,0x243185be,0x550c7dc3,0x72be5d74,0x80deb1fe,0x9bdc06a7,0xc19bf174,
 0xe49b69c1,0xefbe4786,0x0fc19dc6,0x240ca1cc,0x2de92c6f,0x4a7484aa,0x5cb0a9dc,0x76f988da,0x983e5152,0xa831c66d,0xb00327c8,0xbf597fc7,0xc6e00bf3,0xd5a79147,0x06ca6351,0x14292967,
 0x27b70a85,0x2e1b2138,0x4d2c6dfc,0x53380d13,0x650a7354,0x766a0abb,0x81c2c92e,0x92722c85,0xa2bfe8a1,0xa81a664b,0xc24b8b70,0xc76c51a3,0xd192e819,0xd6990624,0xf40e3585,0x106aa070};
static inline u32 ror(u32 x, int n) { return (x >> n) | (x << (32 - n)); }
static inline u32 S0(u32 x) { return ror(x, 2) ^ ror(x, 13) ^ ror(x, 22); }
static inline u32 S1(u32 x) { return ror(x, 6) ^ ror(x, 11) ^ ror(x, 25); }
static inline u32 s0(u32 x) { return ror(x, 7) ^ ror(x, 18) ^ (x >> 3); }
static inline u32 s1(u32 x) { return ror(x, 17) ^ ror(x, 19) ^ (x >> 10); }
static inline u32 CH(u32 x, u32 y, u32 z) { return (x & y) ^ (~x & z); }
static inline u32 MAJ(u32 x, u32 y, u32 z) { return (x & y) ^ (x & z) ^ (y & z); }
static uint64_t rs[4];
static inline uint64_t rotl(uint64_t x, int k) { return (x << k) | (x >> (64 - k)); }
static uint64_t nxt(void) { uint64_t r = rotl(rs[1] * 5, 7) * 9, t = rs[1] << 17; rs[2] ^= rs[0]; rs[3] ^= rs[1]; rs[1] ^= rs[2]; rs[0] ^= rs[3]; rs[2] ^= t; rs[3] = rotl(rs[3], 45); return r; }
static void seed(uint64_t s) { for (int i = 0; i < 4; i++) { s += 0x9e3779b97f4a7c15ULL; uint64_t z = s; z = (z ^ (z >> 30)) * 0xbf58476d1ce4e5b9ULL; z = (z ^ (z >> 27)) * 0x94d049bb133111ebULL; rs[i] = z ^ (z >> 31); } }
static inline u32 r32(void) { return (u32)(nxt() >> 32); }

typedef struct { u32 A[2][42], E[2][42], W[2][38]; } St;     // A/E index +4
#define AA(s, m, i) (s)->A[m][(i) + 4]
#define EE(s, m, i) (s)->E[m][(i) + 4]
static u32 MA[38], SA[38], ME[38], SE[38], MW[38], SW[38];   // trail: xor mask and x-value on the mask, rows 0..37
static St base; static u32 D7, T7;
typedef struct { int key, n, kind[3], row[3], bit[3]; u32 allowed; } Cond;
static Cond CO[8192]; static int nCO;
static u32 (*VW)[4]; static long nV;

static inline void step(St *s, int i) {
    for (int m = 0; m < 2; m++) {
        u32 a = AA(s, m, i - 1), b = AA(s, m, i - 2), c = AA(s, m, i - 3), d = AA(s, m, i - 4);
        u32 e = EE(s, m, i - 1), f = EE(s, m, i - 2), g = EE(s, m, i - 3), h = EE(s, m, i - 4);
        u32 T1 = h + S1(e) + CH(e, f, g) + K[i] + s->W[m][i];
        EE(s, m, i) = d + T1; AA(s, m, i) = T1 + S0(a) + MAJ(a, b, c);
    }
}
static inline int condok(const St *s, int r) {
    for (int c = 0; c < nCO; c++) {
        if (CO[c].key != r) continue;
        int idx = 0;
        for (int q = 0; q < CO[c].n; q++) { u32 w = CO[c].kind[q] == 2 ? s->W[0][CO[c].row[q]] : CO[c].kind[q] ? EE(s, 0, CO[c].row[q]) : AA(s, 0, CO[c].row[q]); idx |= ((w >> CO[c].bit[q]) & 1) << q; }
        if (!((CO[c].allowed >> idx) & 1)) return 0;
    }
    return 1;
}
static inline int rowok(const St *s, int r) {
    u32 ax = AA(s, 0, r), ex = EE(s, 0, r), wx = s->W[0][r];
    static long dfm = -1;   // DIFFROW=r[,r...]: these rows checked on signed differences only (no derived value conditions)
    if (dfm < 0) { dfm = 0; const char *e = getenv("DIFFROW"); while (e && *e) { int v = atoi(e); if (v > 0) dfm |= 1L << v; while (*e && *e != ',') e++; if (*e) e++; } }
    if (!((dfm >> r) & 1) && !condok(s, r)) return 0;
    return ((ax ^ AA(s, 1, r)) == MA[r]) && ((ax & MA[r]) == SA[r]) && ((ex ^ EE(s, 1, r)) == ME[r]) && ((ex & ME[r]) == SE[r])
        && ((wx ^ s->W[1][r]) == MW[r]) && ((wx & MW[r]) == SW[r]);
}
// row r of a particle p with W[.][r] = (w0, w1), without copying p: the new A, E of both members, and the row test of rowok on them
static inline u32 rowval(const St *p, int k, int m, int row, const u32 *na, const u32 *ne, const u32 *nw, int r) {
    if (row == r) return k == 2 ? nw[m] : k ? ne[m] : na[m];
    return k == 2 ? p->W[m][row] : k ? EE(p, m, row) : AA(p, m, row);
}
static inline int rowok_new(const St *p, int r, const u32 *na, const u32 *ne, const u32 *nw) {
    static long dfm = -1;
    if (dfm < 0) { dfm = 0; const char *e = getenv("DIFFROW"); while (e && *e) { int v = atoi(e); if (v > 0) dfm |= 1L << v; while (*e && *e != ',') e++; if (*e) e++; } }
    static int rowlist[64][256], nrow[64], built = 0;           // the conditions of each row, in the order of CO (same tests, same order)
    if (!built) { for (int c = 0; c < nCO; c++) { int k = CO[c].key; if (k >= 0 && k < 64 && nrow[k] < 256) rowlist[k][nrow[k]++] = c; } built = 1; }
    if (!((dfm >> r) & 1)) {
        for (int ci = 0; ci < nrow[r]; ci++) {
            int c = rowlist[r][ci];
            int idx = 0;
            for (int q = 0; q < CO[c].n; q++) { u32 w = rowval(p, CO[c].kind[q], 0, CO[c].row[q], na, ne, nw, r); idx |= ((w >> CO[c].bit[q]) & 1) << q; }
            if (!((CO[c].allowed >> idx) & 1)) return 0;
        }
    }
    u32 ax = na[0], ex = ne[0], wx = nw[0];
    return ((ax ^ na[1]) == MA[r]) && ((ax & MA[r]) == SA[r]) && ((ex ^ ne[1]) == ME[r]) && ((ex & ME[r]) == SE[r])
        && ((wx ^ nw[1]) == MW[r]) && ((wx & MW[r]) == SW[r]);
}
static inline void sched(St *s, int i) { for (int m = 0; m < 2; m++) s->W[m][i] = s1(s->W[m][i - 2]) + s->W[m][i - 7] + s0(s->W[m][i - 15]) + s->W[m][i - 16]; }
static inline int inF7(u32 w) { return s0(w + D7) - s0(w) == T7; }

static void load(const char *fn) {
    FILE *f = fopen(fn, "r"); if (!f) { perror(fn); exit(1); }
    char key[32];
    while (fscanf(f, "%31s", key) == 1) {
        if (!strcmp(key, "D7")) fscanf(f, "%x", &D7);
        else if (!strcmp(key, "T7")) fscanf(f, "%x", &T7);
        else if (!strcmp(key, "ROW")) { int r; u32 a, b, c, d, e, g; fscanf(f, "%d %x %x %x %x %x %x", &r, &a, &b, &c, &d, &e, &g); MA[r] = a; SA[r] = b; ME[r] = c; SE[r] = d; MW[r] = e; SW[r] = g; }
        else if (!strcmp(key, "ST")) { int m, i; u32 a, e; fscanf(f, "%d %d %x %x", &m, &i, &a, &e); AA(&base, m, i) = a; EE(&base, m, i) = e; }
        else if (!strcmp(key, "COND")) { Cond *c = &CO[nCO++]; fscanf(f, "%d %d", &c->key, &c->n); for (int q = 0; q < c->n; q++) fscanf(f, "%d %d %d", &c->kind[q], &c->row[q], &c->bit[q]); fscanf(f, "%x", &c->allowed); }
        else if (!strcmp(key, "W")) { int m, i; u32 w; fscanf(f, "%d %d %x", &m, &i, &w); base.W[m][i] = w; }
    }
    fclose(f);
}

int main(int argc, char **argv) {
    load(argv[1]); uint64_t sd = strtoull(argv[2], 0, 10); int N = atoi(argv[3]), T = atoi(argv[4]);
    seed(sd);
    u32 dW16 = (s1(base.W[1][14]) + base.W[1][9]) - (s1(base.W[0][14]) + base.W[0][9]);   // W0, W1 carry no difference
    // row 16 exhaustive (cached)
    static u32 G[1 << 20]; long nG = 0;
    char cache[512]; snprintf(cache, sizeof cache, "%s.g16", argv[1]);
    FILE *fc = fopen(cache, "rb");
    if (fc) { nG = fread(G, 4, 1 << 20, fc); fclose(fc); }
    else {
        for (uint64_t w = 0; w < (1ULL << 32); w++) {
            St s; memcpy(s.A, base.A, sizeof s.A); memcpy(s.E, base.E, sizeof s.E);
            s.W[0][16] = (u32)w; s.W[1][16] = (u32)w + dW16; step(&s, 16);
            if (rowok(&s, 16)) { if (nG < (1 << 20)) G[nG] = (u32)w; nG++; }
        }
        if (nG > (1 << 20)) { fprintf(stderr, "G too large %ld\n", nG); nG = 1 << 20; }
        fc = fopen(cache, "wb"); fwrite(G, 4, nG, fc); fclose(fc);
    }
    if (0) {   // row-17 pass counts per G word (sampled W17)
        int live = 0; uint64_t S = 1ULL << 24;
        for (long gi = 0; gi < nG; gi++) {
            St s = base; s.W[0][16] = G[gi]; s.W[1][16] = G[gi] + dW16; step(&s, 16);
            uint64_t pass = 0;
            for (uint64_t k = 0; k < S; k++) {
                St t = s; u32 wx = r32();
                u32 dsch = (s1(t.W[1][15]) + t.W[1][10]) - (s1(t.W[0][15]) + t.W[0][10]) + s0(t.W[1][2]) - s0(t.W[0][2]);
                t.W[0][17] = wx; t.W[1][17] = wx + dsch; step(&t, 17); pass += rowok(&t, 17);
            }
            live += pass > 0;
            printf("G %08x row17 passes %llu / 2^24\n", G[gi], (unsigned long long)pass);
        }
        printf("live G words: %d of %ld\n", live, nG); return 0;
    }
    uint64_t f7 = 0; for (int k = 0; k < 1 << 20; k++) f7 += inF7(r32());
    double lv[8]; lv[0] = nG ? log2((double)nG) - 32 : -INFINITY;
    if (!nG) { printf("seed %llu row16 impossible\n", (unsigned long long)sd); return 0; }
    St *cur = malloc(sizeof(St) * N), *nx = malloc(sizeof(St) * N); int ncur = N;
    for (int k = 0; k < N; k++) { St s = base; u32 w = G[nxt() % nG]; s.W[0][16] = w; s.W[1][16] = w + dW16; step(&s, 16); cur[k] = s; }
    for (int r = 17; r <= 22; r++) {
        uint64_t tries = 0; int got = 0;
        while (got < N) {
            if (tries > (1ULL << 34)) { for (int v = 0; v < 3; v++) { FILE *fo = fopen(argv[6 + 2 * v], "w"); fprintf(fo, "seed %llu stalled at row %d\n", (unsigned long long)sd, r); fclose(fo); } return 0; }
            const St *p = &cur[nxt() % ncur]; tries++;
            u32 wx = r32();
            u32 dsch = (s1(p->W[1][r - 2]) + p->W[1][r - 7]) - (s1(p->W[0][r - 2]) + p->W[0][r - 7]);
            if (r == 22) dsch += T7; else dsch += s0(p->W[1][r - 15]) - s0(p->W[0][r - 15]);
            u32 nw[2] = {wx, wx + dsch}, na[2], ne[2];
            for (int m = 0; m < 2; m++) {
                u32 a = AA(p, m, r - 1), b = AA(p, m, r - 2), c = AA(p, m, r - 3), d = AA(p, m, r - 4);
                u32 e = EE(p, m, r - 1), f = EE(p, m, r - 2), g = EE(p, m, r - 3), h = EE(p, m, r - 4);
                u32 T1 = h + S1(e) + CH(e, f, g) + K[r] + nw[m];
                ne[m] = d + T1; na[m] = T1 + S0(a) + MAJ(a, b, c);
            }
            if (rowok_new(p, r, na, ne, nw)) { St *q = &nx[got++]; *q = *p; for (int m = 0; m < 2; m++) { q->W[m][r] = nw[m]; AA(q, m, r) = na[m]; EE(q, m, r) = ne[m]; } }
        }
        lv[r - 16] = log2((double)(N - 1) / (double)(tries - 1));
        St *t = cur; cur = nx; nx = t;
    }
    uint64_t rs0[4]; memcpy(rs0, rs, sizeof rs0);                // the generator state after the shared prefix
    double lv7[3];
    for (int v = 0; v < 3; v++) {
        memcpy(rs, rs0, sizeof rs0); nV = 0; if (VW) { free(VW); VW = 0; }
        FILE *fo = fopen(argv[6 + 2 * v], "w");
        {
            FILE *fv = fopen(argv[5 + 2 * v], "r"); long cap = 1 << 22; VW = malloc(sizeof(*VW) * cap); int j; u32 a0, a1, a2, w8, w9, w10;
            while (nV < cap && fscanf(fv, "%d %x %x %x %x %x %x", &j, &a0, &a1, &a2, &w8, &w9, &w10) == 7) { VW[nV][0] = (u32)nV; VW[nV][1] = w8; VW[nV][2] = w9; VW[nV][3] = w10; nV++; }
            fclose(fv); fprintf(fo, "variants %ld\n", nV);
        }
        uint64_t prop = (uint64_t)N * T, succ = 0, coll = 0;
        for (uint64_t k = 0; k < prop; k++) {
            St s = cur[k % N]; u32 w7; do w7 = r32(); while (!inF7(w7));
            s.W[0][7] = w7; s.W[1][7] = w7 + D7;
            long vi = -1;
            if (nV) { vi = nxt() % nV; for (int i = 8; i <= 10; i++) { s.W[0][i] = VW[vi][i - 7]; s.W[1][i] = VW[vi][i - 7] + (base.W[1][i] - base.W[0][i]); } }
            int ok = 1;
            static int relax = -1; if (relax < 0) relax = getenv("RELAX_TAIL") != 0;
            for (int r = 23; r < 38 && ok; r++) { sched(&s, r); step(&s, r); if (!relax) ok = rowok(&s, r); }
            if (relax) { for (int i = 34; i < 38 && ok; i++) if (AA(&s, 0, i) != AA(&s, 1, i) || EE(&s, 0, i) != EE(&s, 1, i)) ok = 0; }
            if (ok) {
                succ++;
                int eq = 1; for (int i = 34; i < 38; i++) if (AA(&s, 0, i) != AA(&s, 1, i) || EE(&s, 0, i) != EE(&s, 1, i)) eq = 0;
                coll += eq;
            }
        }
        lv[7] = succ ? log2((double)succ / prop) : -INFINITY; lv7[v] = lv[7];
        double tot = 0; for (int i = 0; i < 8; i++) tot += lv[i];
        fprintf(fo, "seed %llu |G| %ld p2 %.4f stages", (unsigned long long)sd, nG, log2((double)f7 / (1 << 20)));
        for (int i = 0; i < 8; i++) fprintf(fo, " %.3f", lv[i]);
        fprintf(fo, " | succ %llu coll %llu | log2q %.4f%s\n", (unsigned long long)succ, (unsigned long long)coll, tot, nV ? " (variant tail)" : "");
        fclose(fo);
    }
    return 0;
}
~~~

### `p1tconst.py` (sha256 85dd887b50d59e438b2304a598721e6f842526c2b3f5a603fdd7c23f5efdfbef)

~~~python
"""p1tconst.py - writes p1tconst.h (the claw and post-filter constants of p1t38.py) and a chaining-value list for the C port p1t38c.c
(own code).  usage: python3 p1tconst.py <n chaining values> <seed label> <out cvs file>.  Chaining values: first_block of
Shake('<label>|<j>'), j = 0 .. n-1, then u0 = the next u32 of the same stream (as in p1t38.online_experiment)."""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
import p1t38 as P
h = ['/* generated by p1tconst.py from p1t38.py: do not edit */']
def d(name, v): h.append('#define %s 0x%08xu' % (name, v & P.M))
for nm in ('CC2', 'C5', 'CE4', 'MA', 'MB', 'KW8', 'CA', 'CB', 'CW9', 'C1V', 'C1MASK', 'D7', 'D8', 'D9', 'T7', 'T8', 'T9', 'PBASE'):
    d(nm, getattr(P, nm))
d('SA2', P.SA[0][2]); d('SA3', P.SA[0][3]); d('SE6', P.SE[0][6]); d('SE7', P.SE[0][7]); d('K0', P.K[0]); d('K1', P.K[1]); d('K7', P.K[7])
h.append('static const u32 HEADS[20] = {%s};' % ', '.join('0x%08xu' % x for x in P.HEADS))
h.append('static const u32 S160[160] = {%s};' % ', '.join('0x%08xu' % x for x in P.S160))
h.append('static const u32 KK[64] = {%s};' % ', '.join('0x%08xu' % x for x in P.K))
h.append('static const u32 PCVv[8] = {%s};' % ', '.join('0x%08xu' % x for x in P.PCV))
h.append('static const u32 SAv[2][16] = {%s};' % ', '.join('{%s}' % ', '.join('0x%08xu' % P.SA[m][i] for i in range(16)) for m in (0, 1)))
h.append('static const u32 SEv[2][16] = {%s};' % ', '.join('{%s}' % ', '.join('0x%08xu' % P.SE[m][i] for i in range(16)) for m in (0, 1)))
h.append('static const u32 CELLv[3][38][3] = {%s};' % ', '.join('{%s}' % ', '.join('{0x%08xu, 0x%08xu, 0x%08xu}' % P.CELLS[k][i] for i in range(38)) for k in range(3)))
h.append('static const u32 PQEv[38] = {%s};' % ', '.join('0x%08xu' % x for x in P.PQE))
h.append('#define NX2 %d' % len(P.X2))
h.append('static const int X2v[NX2][8] = {%s};' % ', '.join('{%s}' % ', '.join(str(v) for v in t) for t in P.X2))
open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'p1tconst.h'), 'w').write('\n'.join(h) + '\n')
n, lab, out = int(sys.argv[1]), sys.argv[2], sys.argv[3]
with open(out, 'w') as f:
    for j in range(n):
        rng = P.Shake('%s|%d' % (lab, j)); M0, cv = P.first_block(rng); u0 = rng.u32()
        f.write('%d %s %08x\n' % (j, ' '.join('%08x' % x for x in cv), u0))
print('wrote p1tconst.h and %d chaining values to %s' % (n, out))
~~~

### `partners38.c` (sha256 0c7a4413840d3fb4e1dd62183b2c420f9b433786c90e359b656d82d9237f4bc6)

~~~c
/* partners38.c - for every good pair g = (a0, a1, u) of a panel (file of p1t38c GOODF lines "j a0 a1 u code"), all claws (a0, u') of
 * the same a0 over the full scan of 2^32 words u' (the claws of a0 are the u' with s0(u') - u' + F(a0) in S160, F(a0) for the chaining
 * value j), and how many of them are good pairs (post-filters C1, C2, G, F7 on a1' = u' - F + K2 + a0).  One pass over all 2^32 words with
 * a sorted list of the values t - F(a0) of every good pair (own code).  Prints per good pair: j a0 u claws_of_a0 good_partners, and the
 * distances u' - u of the good partners.  usage: partners38 <cvs file> <good file> */
#include <stdio.h>
#include <stdint.h>
#include <stdlib.h>
#include <string.h>
typedef uint32_t u32; typedef uint64_t u64;
#include "p1tconst.h"
#define ROR(x, n) (((x) >> (n)) | ((x) << (32 - (n))))
static inline u32 S0(u32 x) { return ROR(x, 2) ^ ROR(x, 13) ^ ROR(x, 22); }
static inline u32 S1(u32 x) { return ROR(x, 6) ^ ROR(x, 11) ^ ROR(x, 25); }
static inline u32 s0(u32 x) { return ROR(x, 7) ^ ROR(x, 18) ^ (x >> 3); }
static inline u32 CH(u32 x, u32 y, u32 z) { return (x & y) ^ (~x & z); }
static inline u32 MAJ(u32 x, u32 y, u32 z) { return (x & y) ^ (x & z) ^ (y & z); }
typedef struct { u32 k0, E0b, PP, QQ, EF, FF, KF, K2, KK7; } Cvc;
static void cvc(const u32 *cv, Cvc *c) {
    u32 a = cv[0], b = cv[1], cc = cv[2], d = cv[3], e = cv[4], f = cv[5], g = cv[6], h = cv[7];
    c->k0 = 0u - S0(a) - MAJ(a, b, cc) - h - S1(e) - CH(e, f, g) - K0;
    c->E0b = d - S0(a) - MAJ(a, b, cc); c->PP = a & b; c->QQ = a | b; c->EF = e ^ f; c->FF = f;
    c->KF = CC2 + c->k0 - g - K1; c->K2 = CC2 + c->k0; c->KK7 = SE7 - 2 * SA3 - a + S0(SA2) - S1(SE6) - K7;
}
static inline u32 Ffun(const Cvc *c, u32 a0) { u32 E0 = a0 + c->E0b; return a0 + c->KF - S0(a0) - (c->PP | (a0 & c->QQ)) - S1(E0) - (c->FF ^ (E0 & c->EF)); }
static int pf(const Cvc *c, u32 a0, u32 a1) {
    u32 E5 = a1 + C5; if ((E5 & C1MASK) != C1V) return 0;
    u32 w9 = CW9 - a1; if ((u32)(s0(w9 + D9) - s0(w9)) != T9) return 1;
    u32 E4 = a0 + CE4 - (MA | (a1 & MB)), w8 = KW8 - E4 - (CA ^ (CB & E5)); if ((u32)(s0(w8 + D8) - s0(w8)) != T8) return 2;
    u32 w7 = c->KK7 + MAJ(SA2, a1, a0) - CH(SE6, E5, E4); if ((u32)(s0(w7 + D7) - s0(w7)) != T7) return 3;
    return 4;
}
typedef struct { u32 key; u32 g; } Ent;
static int cmpe(const void *a, const void *b) { u32 x = ((const Ent *)a)->key, y = ((const Ent *)b)->key; return x < y ? -1 : x > y; }
int main(int argc, char **argv) {
    static u32 CV[1024][8]; int ncv = 0; { FILE *f = fopen(argv[1], "r"); int j; u32 v[9];
        while (fscanf(f, "%d %x %x %x %x %x %x %x %x %x", &j, &v[0], &v[1], &v[2], &v[3], &v[4], &v[5], &v[6], &v[7], &v[8]) == 10 && j < 1024) { memcpy(CV[j], v, 32); if (j + 1 > ncv) ncv = j + 1; } fclose(f); }
    int ng = 0, cap = 1 << 16; int *gj = malloc(4 * cap); u32 *ga0 = malloc(4 * cap), *gu = malloc(4 * cap), *gF = malloc(4 * cap); Cvc *gc = malloc(sizeof(Cvc) * cap);
    { FILE *f = fopen(argv[2], "r"); char l[256]; while (fgets(l, sizeof l, f) && ng < cap) { int j, r; u32 a0, a1, u; if (sscanf(l, "%d %x %x %x %d", &j, &a0, &a1, &u, &r) != 5) continue;
        gj[ng] = j; ga0[ng] = a0; gu[ng] = u; cvc(CV[j], &gc[ng]); gF[ng] = Ffun(&gc[ng], a0); ng++; } fclose(f); }
    u64 ne = (u64)ng * 160; Ent *E = malloc(sizeof(Ent) * ne); u64 k = 0;
    for (int g = 0; g < ng; g++) for (int t = 0; t < 160; t++) { E[k].key = S160[t] - gF[g]; E[k].g = g; k++; }
    qsort(E, ne, sizeof(Ent), cmpe);
    uint8_t *bits = calloc(1 << 21, 1);   /* filter on the top 24 bits of the key */
    for (u64 i = 0; i < ne; i++) bits[E[i].key >> 11] |= 1 << ((E[i].key >> 8) & 7);
    u32 *nclaw = calloc(ng, 4), *ngood = calloc(ng, 4); u64 tot = 0;
    for (u64 x = 0; x < (1ull << 32); x++) {
        u32 u = (u32)x, ph = s0(u) - u;
        if (!(bits[ph >> 11] >> ((ph >> 8) & 7) & 1)) continue;
        u64 lo = 0, hi = ne; while (lo < hi) { u64 m = (lo + hi) / 2; if (E[m].key < ph) lo = m + 1; else hi = m; }
        for (u64 i = lo; i < ne && E[i].key == ph; i++) {
            int g = E[i].g; if (u == gu[g]) { nclaw[g]++; continue; }
            u32 a1 = u - gF[g] + gc[g].K2 + ga0[g]; nclaw[g]++; tot++;
            if (pf(&gc[g], ga0[g], a1) == 4) { ngood[g]++; printf("P %d %08x %08x %08x du %08x\n", gj[g], ga0[g], gu[g], u, u - gu[g]); }
        }
    }
    u64 sc = 0, sg = 0; for (int g = 0; g < ng; g++) { sc += nclaw[g]; sg += ngood[g]; printf("G %d %08x %08x %u %u\n", gj[g], ga0[g], gu[g], nclaw[g], ngood[g]); }
    printf("# good pairs %d; claws of their a0 over 2^32 words: mean %.3f; good partners sharing a0: %llu (%.6f per good pair)\n", ng, (double)sc / ng, (unsigned long long)sg, (double)sg / ng);
    return 0;
}
~~~

### `gwin38.c` (sha256 feae564923d015656c84c03bfcacd68c16dbeaff6ef92e94909bd2a30f33b527)

~~~c
/* gwin38.c - exact claw post-filter counts per a0 window for P8's base (own code).
 * The claw (A0 = a0, A1 = a1 free) on S's rows 2..15: E5 = a1 + c5, E4 = a0 + c4(a1), W8x = K8(a1) - a0, W9x = c9 - E5.
 *   C1: dW8 = D8 (the CH(E7, E6, E5) difference at the bits where E7 differs), C2: s0(W9y) - s0(W9x) = T9,
 *   G : s0(W8y) - s0(W8x) = T8, i.e. W8x in F8 = {w : s0(w + D8) - s0(w) = T8}.
 * C1 and C2 read a1 only.  For every a1 in C1 and C2 and every window [k 2^b, (k + 1) 2^b) of a0 the number of a0 with
 * K8(a1) - a0 in F8 is a range count over the sorted F8 (|F8| = 68,157,440).  Prints, per window size b and window k, the exact
 * count of (a0, a1) with C1, C2, G and the rate over 2^(b + 32).
 * usage: gwin38 <base file (BASE line)> <D8> <T8> <T9> */
#include <stdio.h>
#include <stdint.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>
typedef uint32_t u32; typedef uint64_t u64;
#define ROR(x, n) (((x) >> (n)) | ((x) << (32 - (n))))
static inline u32 S0(u32 x) { return ROR(x, 2) ^ ROR(x, 13) ^ ROR(x, 22); }
static inline u32 S1(u32 x) { return ROR(x, 6) ^ ROR(x, 11) ^ ROR(x, 25); }
static inline u32 s0(u32 x) { return ROR(x, 7) ^ ROR(x, 18) ^ (x >> 3); }
static inline u32 CH(u32 x, u32 y, u32 z) { return (x & y) ^ (~x & z); }
static inline u32 MAJ(u32 x, u32 y, u32 z) { return (x & y) ^ (x & z) ^ (y & z); }
static const u32 K8 = 0xd807aa98, K9 = 0x12835b01;
static int cmpu(const void *a, const void *b) { u32 x = *(const u32 *)a, y = *(const u32 *)b; return x < y ? -1 : x > y; }
static u32 *F8; static u64 NF8;
static u32 *CB;   /* CB[h] = number of F8 elements below h << 16 (h = 0 .. 65536) */
static u64 cnt_below(u64 x) {   /* number of F8 elements < x, 0 <= x <= 2^32 */
    if (x >= (1ull << 32)) return NF8;
    u32 h = (u32)(x >> 16); u64 lo = CB[h], hi = CB[h + 1];
    while (lo < hi) { u64 m = (lo + hi) / 2; if (F8[m] < (u32)x) lo = m + 1; else hi = m; }
    return lo;
}
int main(int argc, char **argv) {
    FILE *f = fopen(argv[1], "r"); char line[4096]; u32 bx[34], by[34]; int got = 0;
    while (fgets(line, sizeof line, f)) { char *p = strstr(line, "BASE"); if (!p) continue; p += 4;
        for (int k = 0; k < 34; k++) bx[k] = strtoul(p, &p, 16); while (*p == ' ' || *p == '|') p++; for (int k = 0; k < 34; k++) by[k] = strtoul(p, &p, 16); got = 1; break; }
    fclose(f); if (!got) return 1;
    u32 D8 = strtoul(argv[2], 0, 16), T8 = strtoul(argv[3], 0, 16), T9 = strtoul(argv[4], 0, 16);
    u32 A[2][16], E[2][16];
    for (int m = 0; m < 2; m++) { u32 *b = m ? by : bx; for (int i = 2; i <= 15; i++) A[m][i] = b[i - 2]; for (int i = 6; i <= 15; i++) E[m][i] = b[15 + i - 6]; }
    /* F8 sorted */
    NF8 = 0; F8 = malloc(sizeof(u32) * 70000000u);
    for (u64 w = 0; w < (1ull << 32); w++) if ((u32)(s0((u32)w + D8) - s0((u32)w)) == T8) F8[NF8++] = (u32)w;
    fprintf(stderr, "|F8| = %llu\n", (unsigned long long)NF8);   /* already sorted (increasing w) */
    CB = malloc(sizeof(u32) * 65537); { u64 j = 0; for (u64 h = 0; h <= 65536; h++) { while (j < NF8 && F8[j] < (h << 16)) j++; CB[h] = (u32)j; } }
    int B[] = {25, 26, 27, 28}; u64 cnt[4][128]; memset(cnt, 0, sizeof cnt);
    u64 n12 = 0;
    for (u64 v = 0; v < (1ull << 32); v++) {
        u32 a1 = (u32)v, w8[2], w9[2];
        for (int m = 0; m < 2; m++) {
            u32 e5 = A[m][5] + a1 - S0(A[m][4]) - MAJ(A[m][4], A[m][3], A[m][2]);
            u32 c4 = A[m][4] - S0(A[m][3]) - MAJ(A[m][3], A[m][2], a1);   /* E4 = a0 + c4 */
            w8[m] = E[m][8] - A[m][4] - S1(E[m][7]) - CH(E[m][7], E[m][6], e5) - K8 - c4;   /* W8 = w8 - a0 */
            w9[m] = E[m][9] - A[m][5] - e5 - S1(E[m][8]) - CH(E[m][8], E[m][7], E[m][6]) - K9;
        }
        if ((u32)(w8[1] - w8[0]) != D8) continue;                       /* C1 */
        if ((u32)(s0(w9[1]) - s0(w9[0])) != T9) continue;               /* C2 */
        n12++;
        /* G: f = w8 - a0 in F8; a0 in [k 2^25, (k+1) 2^25) <=> f in (w8 - (k+1) 2^25, w8 - k 2^25]: cyclic range of length 2^25 */
        u64 cb[129];
        for (int k = 0; k <= 128; k++) { u32 x = w8[0] - (u32)((u64)k << 25) + 1; cb[k] = cnt_below(x); }   /* count below w8 - k 2^25 + 1 */
        for (int k = 0; k < 128; k++) {
            u64 hi = cb[k], lo = cb[k + 1];   /* range [w8 - (k+1) 2^25 + 1, w8 - k 2^25 + 1) */
            cnt[0][k] += hi >= lo ? hi - lo : NF8 - lo + hi;
        }
    }
    printf("exact 2^25-window counts:"); for (int k = 0; k < 128; k++) printf(" %d:%llu", k, (unsigned long long)cnt[0][k]); printf("\n");
    for (int t = 1; t < 4; t++) { int nk = 1 << (32 - B[t]); for (int k = 0; k < nk; k++) cnt[t][k] = cnt[t - 1][2 * k] + cnt[t - 1][2 * k + 1]; }
    printf("C1 and C2: %llu = 2^%.4f\n", (unsigned long long)n12, log2((double)n12) - 32);
    for (int t = 0; t < 4; t++) {
        int b = B[t], nk = 1 << (32 - b); double best = 0; int kb = -1; u64 tot = 0;
        for (int k = 0; k < nk; k++) { tot += cnt[t][k]; if (cnt[t][k] > best) { best = cnt[t][k]; kb = k; } }
        printf("window 2^%d: total C1C2G %llu = 2^%.4f of 2^64; best k = %d: %llu = 2^%.4f of 2^%d (G|C1C2 2^%.4f)\n", b, (unsigned long long)tot,
               log2((double)tot) - 64, kb, (unsigned long long)cnt[t][kb], log2(best) - (b + 32), b + 32, log2(best / ((double)n12 * (1ull << b))));
        if (b >= 25) { printf("  per window (k: log2 rate of C1C2G over 2^(b+32)):"); for (int k = 0; k < nk; k++) printf(" %d:%.4f", k, log2((double)cnt[t][k]) - (b + 32)); printf("\n"); }
    }
    return 0;
}
~~~

### `gwin38lm.c` (sha256 4894d20d42e057ac85e8974c396e9487004b2614d3d9395e253e81c1dd71b44c)

~~~c
/* gwin38lm.c - the exact C1 C2 G counts of gwin38.c per 2^25-window of a0, recomputed in small memory (own code).
 * The f-space of W8x + a0 (f = w8(a1) - a0 in F8 = {f : s0(f + D8) - s0(f) = T8}) is processed in 8 chunks of 2^29 words; per chunk the
 * F8 elements of the chunk are listed (about 2^23.0 words, sorted by construction) with a per-2^16 prefix index, and every a1 with C1 and C2
 * (both members' words, as in gwin38.c) adds, for each 2^25-window k of a0 = w8(a1) - f, the number of chunk elements in that window's f-range.
 * Prints the 128 window counts (the line format of gwin38.c), |F8|, |C1 and C2| (counted in the first chunk pass), and the peak resident set.
 * usage: gwin38lm <base file (BASE line)> <D8> <T8> <T9> */
#include <stdio.h>
#include <stdint.h>
#include <stdlib.h>
#include <string.h>
typedef uint32_t u32; typedef uint64_t u64;
#define ROR(x, n) (((x) >> (n)) | ((x) << (32 - (n))))
static inline u32 S0(u32 x) { return ROR(x, 2) ^ ROR(x, 13) ^ ROR(x, 22); }
static inline u32 S1(u32 x) { return ROR(x, 6) ^ ROR(x, 11) ^ ROR(x, 25); }
static inline u32 s0(u32 x) { return ROR(x, 7) ^ ROR(x, 18) ^ (x >> 3); }
static inline u32 CH(u32 x, u32 y, u32 z) { return (x & y) ^ (~x & z); }
static inline u32 MAJ(u32 x, u32 y, u32 z) { return (x & y) ^ (x & z) ^ (y & z); }
static const u32 K8 = 0xd807aa98, K9 = 0x12835b01;
#define CB 29                       /* chunk = 2^29 words of f */
static u32 *Fc; static u64 nFc; static u32 IDX[(1 << (CB - 16)) + 1];
static u64 cs;
static inline u64 P(u64 d) {        /* number of chunk elements f < cs + d, 0 <= d <= 2^CB */
    if (d >= (1ull << CB)) return nFc;
    u32 h = (u32)(d >> 16); u64 lo = IDX[h], hi = IDX[h + 1]; u32 x = (u32)(cs + d);
    while (lo < hi) { u64 m = (lo + hi) / 2; if (Fc[m] < x) lo = m + 1; else hi = m; }
    return lo;
}
static long vmhwm(void) { FILE *f = fopen("/proc/self/status", "r"); char l[256]; long v = -1; while (f && fgets(l, sizeof l, f)) if (!strncmp(l, "VmHWM:", 6)) v = atol(l + 6); if (f) fclose(f); return v; }
int main(int argc, char **argv) {
    FILE *f = fopen(argv[1], "r"); char line[4096]; u32 bx[34], by[34]; int got = 0;
    while (fgets(line, sizeof line, f)) { char *p = strstr(line, "BASE"); if (!p) continue; p += 4;
        for (int k = 0; k < 34; k++) bx[k] = strtoul(p, &p, 16); while (*p == ' ' || *p == '|') p++; for (int k = 0; k < 34; k++) by[k] = strtoul(p, &p, 16); got = 1; break; }
    fclose(f); if (!got) return 1;
    u32 D8 = strtoul(argv[2], 0, 16), T8 = strtoul(argv[3], 0, 16), T9 = strtoul(argv[4], 0, 16);
    u32 A[2][16], E[2][16];
    for (int m = 0; m < 2; m++) { u32 *b = m ? by : bx; for (int i = 2; i <= 15; i++) A[m][i] = b[i - 2]; for (int i = 6; i <= 15; i++) E[m][i] = b[15 + i - 6]; }
    Fc = malloc(sizeof(u32) * 16000000u);
    u64 cnt[128]; memset(cnt, 0, sizeof cnt); u64 nF8 = 0, n12 = 0;
    for (int c = 0; c < (1 << (32 - CB)); c++) {
        cs = (u64)c << CB; nFc = 0;
        for (u64 d = 0; d < (1ull << CB); d++) { if ((d & 0xffff) == 0) IDX[d >> 16] = (u32)nFc; u32 w = (u32)(cs + d); if ((u32)(s0(w + D8) - s0(w)) == T8) { if (nFc >= 16000000u) { fprintf(stderr, "chunk overflow\n"); return 2; } Fc[nFc++] = w; } }
        IDX[1 << (CB - 16)] = (u32)nFc; nF8 += nFc;
        for (u64 v = 0; v < (1ull << 32); v++) {
            u32 a1 = (u32)v, w8[2], w9[2];
            for (int m = 0; m < 2; m++) {
                u32 e5 = A[m][5] + a1 - S0(A[m][4]) - MAJ(A[m][4], A[m][3], A[m][2]);
                u32 c4 = A[m][4] - S0(A[m][3]) - MAJ(A[m][3], A[m][2], a1);
                w8[m] = E[m][8] - A[m][4] - S1(E[m][7]) - CH(E[m][7], E[m][6], e5) - K8 - c4;
                w9[m] = E[m][9] - A[m][5] - e5 - S1(E[m][8]) - CH(E[m][8], E[m][7], E[m][6]) - K9;
            }
            if ((u32)(w8[1] - w8[0]) != D8) continue;
            if ((u32)(s0(w9[1]) - s0(w9[0])) != T9) continue;
            if (c == 0) n12++;
            /* f = cs + d, a0 = w8 - f decreases with d; segments of constant window k = a0 >> 25 */
            u64 Aw = (u64)(u32)(w8[0] - (u32)cs) + (1ull << 32);    /* a0 at d = 0, lifted so that Aw - d >= 0 */
            u64 d0 = 0, d1 = (Aw & ((1ull << 25) - 1)) + 1, prev = 0;
            while (d0 < (1ull << CB)) {
                if (d1 > (1ull << CB)) d1 = 1ull << CB;
                u64 pc = P(d1); int k = (int)(((Aw - d0) >> 25) & 127);
                cnt[k] += pc - prev; prev = pc; d0 = d1; d1 = d0 + (1ull << 25);
            }
        }
        fprintf(stderr, "chunk %d: %llu F8 elements\n", c, (unsigned long long)nFc);
    }
    printf("|F8| = %llu\n", (unsigned long long)nF8);
    printf("exact 2^25-window counts:"); for (int k = 0; k < 128; k++) printf(" %d:%llu", k, (unsigned long long)cnt[k]); printf("\n");
    printf("C1 and C2: %llu\n", (unsigned long long)n12);
    printf("# peak resident set VmHWM %ld KiB\n", vmhwm());
    return 0;
}
~~~

### `p1vars38.c` (sha256 1a9d7b25a1166883627deecaea22b56eaa28145654532d7891ca28f6507d4963)

~~~c
/* p1vars38.c - variant lists for the paired q3 runs of the P1 family (own code).
 * mode p1: pairs (a0, a1) drawn uniformly from {a0 in the set P, a1 any word : C1 and C2 and G} by joint rejection, where
 *          P = {a0 : bits 25..27 = 010, bits 30..31 = 00} (2^27 words, the table's a0 set);
 * mode a0: the A0-variant family: a1 = S's A1, a0 uniform over all words with G (C1 and C2 hold for S's A1).
 * Each line: "j a0 a1 0 w8x w9x w10x" (the VARS input of q3tv; member y = x + the base pair's differences, valid under C1).
 * usage: p1vars38 <base file> <p1|a0> <n> <out> <seed> [a1 for mode a0, hex] */
#include <stdio.h>
#include <stdint.h>
#include <stdlib.h>
#include <string.h>
typedef uint32_t u32; typedef uint64_t u64;
#define ROR(x, n) (((x) >> (n)) | ((x) << (32 - (n))))
static inline u32 S0(u32 x) { return ROR(x, 2) ^ ROR(x, 13) ^ ROR(x, 22); }
static inline u32 S1(u32 x) { return ROR(x, 6) ^ ROR(x, 11) ^ ROR(x, 25); }
static inline u32 s0(u32 x) { return ROR(x, 7) ^ ROR(x, 18) ^ (x >> 3); }
static inline u32 CH(u32 x, u32 y, u32 z) { return (x & y) ^ (~x & z); }
static inline u32 MAJ(u32 x, u32 y, u32 z) { return (x & y) ^ (x & z) ^ (y & z); }
static const u32 K8 = 0xd807aa98, K9 = 0x12835b01, K10 = 0x243185be;
static const u32 D8 = 0xfbc00800, T8 = 0xfe808000, T9 = 0x043ff800;
static u32 A[2][16], E[2][16];
static u64 rs;
static inline u64 rnd(void) { u64 z = (rs += 0x9e3779b97f4a7c15ull); z = (z ^ (z >> 30)) * 0xbf58476d1ce4e5b9ull; z = (z ^ (z >> 27)) * 0x94d049bb133111ebull; return z ^ (z >> 31); }
/* W8, W9, W10 of member m for (a0, a1) on the base (Lemma 4.1 with A0, A1 free; E4, E5 from the step equations) */
static void words(int m, u32 a0, u32 a1, u32 *w8, u32 *w9, u32 *w10) {
    u32 e5 = A[m][5] + a1 - S0(A[m][4]) - MAJ(A[m][4], A[m][3], A[m][2]);
    u32 e4 = A[m][4] + a0 - S0(A[m][3]) - MAJ(A[m][3], A[m][2], a1);
    *w8 = E[m][8] - A[m][4] - e4 - S1(E[m][7]) - CH(E[m][7], E[m][6], e5) - K8;
    *w9 = E[m][9] - A[m][5] - e5 - S1(E[m][8]) - CH(E[m][8], E[m][7], E[m][6]) - K9;
    *w10 = E[m][10] - A[m][6] - E[m][6] - S1(E[m][9]) - CH(E[m][9], E[m][8], E[m][7]) - K10;
}
int main(int argc, char **argv) {
    FILE *f = fopen(argv[1], "r"); char line[4096]; u32 bx[34], by[34]; int got = 0;
    while (fgets(line, sizeof line, f)) { char *p = strstr(line, "BASE"); if (!p) continue; p += 4;
        for (int k = 0; k < 34; k++) bx[k] = strtoul(p, &p, 16);
        while (*p == ' ' || *p == '|') p++;
        for (int k = 0; k < 34; k++) by[k] = strtoul(p, &p, 16);
        got = 1; break; }
    fclose(f); if (!got) return 1;
    for (int m = 0; m < 2; m++) { u32 *b = m ? by : bx; for (int i = 2; i <= 15; i++) A[m][i] = b[i - 2]; for (int i = 6; i <= 15; i++) E[m][i] = b[15 + i - 6]; }
    int p1 = !strcmp(argv[2], "p1"); long n = atol(argv[3]); FILE *fo = fopen(argv[4], "w"); rs = strtoull(argv[5], 0, 0);
    u32 a1fix = argc > 6 ? strtoul(argv[6], 0, 16) : 0;
    long got_n = 0; u64 trials = 0;
    while (got_n < n) {
        u64 r = rnd(); trials++;
        u32 a0 = (u32)r, a1 = p1 ? (u32)(r >> 32) : a1fix;
        if (p1) a0 = (a0 & 0x01ffffffu) | (2u << 25) | (((a0 >> 25) & 3u) << 28);   /* a0 uniform in P */
        u32 x8, x9, x10, y8, y9, y10;
        words(0, a0, a1, &x8, &x9, &x10); words(1, a0, a1, &y8, &y9, &y10);
        if (y8 - x8 != D8) continue;                                   /* C1 */
        if ((u32)(s0(y9) - s0(x9)) != T9) continue;                    /* C2 */
        if ((u32)(s0(y8) - s0(x8)) != T8) continue;                    /* G */
        fprintf(fo, "%ld %08x %08x 0 %08x %08x %08x\n", got_n, a0, a1, x8, x9, x10); got_n++;
    }
    fclose(fo);

    printf("%s: %ld pairs from %llu trials\n", argv[2], got_n, (unsigned long long)trials);
    return 0;
}
~~~

### `gensel38.c` (sha256 6f127183000a31d2b43338709da21b7aebf7d7748a71a07d3c432773554e5b57)

~~~c
/* gensel38.c - the variant list of the A0-variant family on which q3_model (-96.0133) was measured: the 196,608 selected
 * variants of 9aaf71a2 (8 classes x 96 class constants x 256 lanes), with A1 = S's A1 (own code; the class data CLASSES, MASK,
 * LB, G1, G3, NB and the formulas bconst / lane_a0 are transcribed as data from the public p1claw38.py of e4243e7a, not executed).
 * Each line: "j a0 a1 0 w8x w9x w10x" (the VARS input of q3tv), in the order ci, b, L.  Reports how many satisfy C1, C2, G.
 * usage: gensel38 <base file (BASE line)> <out> <a1 hex> */
#include <stdio.h>
#include <stdint.h>
#include <stdlib.h>
#include <string.h>
typedef uint32_t u32;
#define ROR(x, n) (((x) >> (n)) | ((x) << (32 - (n))))
static inline u32 S0(u32 x) { return ROR(x, 2) ^ ROR(x, 13) ^ ROR(x, 22); }
static inline u32 S1(u32 x) { return ROR(x, 6) ^ ROR(x, 11) ^ ROR(x, 25); }
static inline u32 s0(u32 x) { return ROR(x, 7) ^ ROR(x, 18) ^ (x >> 3); }
static inline u32 CH(u32 x, u32 y, u32 z) { return (x & y) ^ (~x & z); }
static inline u32 MAJ(u32 x, u32 y, u32 z) { return (x & y) ^ (x & z) ^ (y & z); }
static const u32 K8 = 0xd807aa98, K9 = 0x12835b01, K10 = 0x243185be;
static const u32 D8 = 0xfbc00800, T8 = 0xfe808000, T9 = 0x043ff800;
static const u32 MASK = 0x7fe96c7c;
static const u32 CLS1[8] = {0x9b649791, 0x9b648791, 0x9b609793, 0x9b608793, 0x1b649791, 0x1b648791, 0x1b609793, 0x1b608793};
static const int LB[8] = {11, 2, 3, 6, 13, 14, 16, 19};
static const u32 G1[3] = {0x10, 0x20, 0x30};
static const u32 G3[32] = {0x1b6, 0x1b8, 0x236, 0x238, 0x240, 0x246, 0x248, 0x24e, 0x250, 0x256, 0x258, 0x260, 0x266, 0x268, 0x26e, 0x270,
                           0x3b6, 0x3b8, 0x436, 0x438, 0x440, 0x446, 0x448, 0x44e, 0x450, 0x456, 0x458, 0x460, 0x466, 0x468, 0x46e, 0x470};
static u32 A[2][16], E[2][16];
static void words(int m, u32 a0, u32 a1, u32 *w8, u32 *w9, u32 *w10) {
    u32 e5 = A[m][5] + a1 - S0(A[m][4]) - MAJ(A[m][4], A[m][3], A[m][2]);
    u32 e4 = A[m][4] + a0 - S0(A[m][3]) - MAJ(A[m][3], A[m][2], a1);
    *w8 = E[m][8] - A[m][4] - e4 - S1(E[m][7]) - CH(E[m][7], E[m][6], e5) - K8;
    *w9 = E[m][9] - A[m][5] - e5 - S1(E[m][8]) - CH(E[m][8], E[m][7], E[m][6]) - K9;
    *w10 = E[m][10] - A[m][6] - E[m][6] - S1(E[m][9]) - CH(E[m][9], E[m][8], E[m][7]) - K10;
}
int main(int argc, char **argv) {
    FILE *f = fopen(argv[1], "r"); char line[4096]; u32 bx[34], by[34]; int got = 0;
    while (fgets(line, sizeof line, f)) { char *p = strstr(line, "BASE"); if (!p) continue; p += 4;
        for (int k = 0; k < 34; k++) bx[k] = strtoul(p, &p, 16);
        while (*p == ' ' || *p == '|') p++;
        for (int k = 0; k < 34; k++) by[k] = strtoul(p, &p, 16);
        got = 1; break; }
    fclose(f); if (!got) return 1;
    for (int m = 0; m < 2; m++) { u32 *b = m ? by : bx; for (int i = 2; i <= 15; i++) A[m][i] = b[i - 2]; for (int i = 6; i <= 15; i++) E[m][i] = b[15 + i - 6]; }
    FILE *fo = fopen(argv[2], "w"); u32 a1 = strtoul(argv[3], 0, 16);
    long n = 0, c1 = 0, c2 = 0, g = 0;
    for (int ci = 0; ci < 8; ci++) for (int b = 0; b < 96; b++) {
        u32 c = (CLS1[ci] & ~MASK) | G1[b % 3] | (G3[b / 3] << 20);
        for (int L = 0; L < 256; L++) {
            u32 a0 = c | ((L & 1) ? 0x800 : 0x400);
            for (int k = 1; k < 8; k++) a0 |= (u32)((L >> k) & 1) << LB[k];
            u32 x8, x9, x10, y8, y9, y10;
            words(0, a0, a1, &x8, &x9, &x10); words(1, a0, a1, &y8, &y9, &y10);
            int ok1 = y8 - x8 == D8, ok2 = (u32)(s0(y9) - s0(x9)) == T9, okg = (u32)(s0(y8) - s0(x8)) == T8;
            c1 += ok1; c2 += ok1 && ok2; g += ok1 && ok2 && okg;
            fprintf(fo, "%ld %08x %08x 0 %08x %08x %08x\n", n, a0, a1, x8, x9, x10); n++;
        }
    }
    fclose(fo);
    printf("sel: %ld variants; C1 %ld, C1 C2 %ld, C1 C2 G %ld\n", n, c1, c2, g);
    return 0;
}
~~~

### `q3tv.c` (sha256 e01dbb414ef2a7e0cecf79638bb287130e1309dfa439727b57bc8b32b3957ead)

~~~c
// Trail-based estimator of the uncontrolled probability of a 38-step SHA-256 characteristic (own code).
// q3tv: q3t with the tail drawing a dense-part variant per proposal (env VARS = vsamp output: j a0 a1 a2 w8x w9x w10x;
// member y gets w + dW_i of the base pair) and every success written to env DUMPALL (variant index, W7..W37 of member x).
// q = Pr[rows 16..37 follow the signed trail | dense part, W7 in F7], W0..W6 uniform (Lemma 4 structure).
// Input file (text, hex words): see prep.py. Usage: q3t <datafile> <seed> <N> <T> [g-cache]
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>
#include <stdint.h>
typedef uint32_t u32;
static const u32 K[64] = {
 0x428a2f98,0x71374491,0xb5c0fbcf,0xe9b5dba5,0x3956c25b,0x59f111f1,0x923f82a4,0xab1c5ed5,0xd807aa98,0x12835b01,0x243185be,0x550c7dc3,0x72be5d74,0x80deb1fe,0x9bdc06a7,0xc19bf174,
 0xe49b69c1,0xefbe4786,0x0fc19dc6,0x240ca1cc,0x2de92c6f,0x4a7484aa,0x5cb0a9dc,0x76f988da,0x983e5152,0xa831c66d,0xb00327c8,0xbf597fc7,0xc6e00bf3,0xd5a79147,0x06ca6351,0x14292967,
 0x27b70a85,0x2e1b2138,0x4d2c6dfc,0x53380d13,0x650a7354,0x766a0abb,0x81c2c92e,0x92722c85,0xa2bfe8a1,0xa81a664b,0xc24b8b70,0xc76c51a3,0xd192e819,0xd6990624,0xf40e3585,0x106aa070};
static inline u32 ror(u32 x, int n) { return (x >> n) | (x << (32 - n)); }
static inline u32 S0(u32 x) { return ror(x, 2) ^ ror(x, 13) ^ ror(x, 22); }
static inline u32 S1(u32 x) { return ror(x, 6) ^ ror(x, 11) ^ ror(x, 25); }
static inline u32 s0(u32 x) { return ror(x, 7) ^ ror(x, 18) ^ (x >> 3); }
static inline u32 s1(u32 x) { return ror(x, 17) ^ ror(x, 19) ^ (x >> 10); }
static inline u32 CH(u32 x, u32 y, u32 z) { return (x & y) ^ (~x & z); }
static inline u32 MAJ(u32 x, u32 y, u32 z) { return (x & y) ^ (x & z) ^ (y & z); }
static uint64_t rs[4];
static inline uint64_t rotl(uint64_t x, int k) { return (x << k) | (x >> (64 - k)); }
static uint64_t nxt(void) { uint64_t r = rotl(rs[1] * 5, 7) * 9, t = rs[1] << 17; rs[2] ^= rs[0]; rs[3] ^= rs[1]; rs[1] ^= rs[2]; rs[0] ^= rs[3]; rs[2] ^= t; rs[3] = rotl(rs[3], 45); return r; }
static void seed(uint64_t s) { for (int i = 0; i < 4; i++) { s += 0x9e3779b97f4a7c15ULL; uint64_t z = s; z = (z ^ (z >> 30)) * 0xbf58476d1ce4e5b9ULL; z = (z ^ (z >> 27)) * 0x94d049bb133111ebULL; rs[i] = z ^ (z >> 31); } }
static inline u32 r32(void) { return (u32)(nxt() >> 32); }

typedef struct { u32 A[2][42], E[2][42], W[2][38]; } St;     // A/E index +4
#define AA(s, m, i) (s)->A[m][(i) + 4]
#define EE(s, m, i) (s)->E[m][(i) + 4]
static u32 MA[38], SA[38], ME[38], SE[38], MW[38], SW[38];   // trail: xor mask and x-value on the mask, rows 0..37
static St base; static u32 D7, T7;
typedef struct { int key, n, kind[3], row[3], bit[3]; u32 allowed; } Cond;
static Cond CO[8192]; static int nCO;
static u32 (*VW)[4]; static long nV;

static inline void step(St *s, int i) {
    for (int m = 0; m < 2; m++) {
        u32 a = AA(s, m, i - 1), b = AA(s, m, i - 2), c = AA(s, m, i - 3), d = AA(s, m, i - 4);
        u32 e = EE(s, m, i - 1), f = EE(s, m, i - 2), g = EE(s, m, i - 3), h = EE(s, m, i - 4);
        u32 T1 = h + S1(e) + CH(e, f, g) + K[i] + s->W[m][i];
        EE(s, m, i) = d + T1; AA(s, m, i) = T1 + S0(a) + MAJ(a, b, c);
    }
}
static inline int condok(const St *s, int r) {
    for (int c = 0; c < nCO; c++) {
        if (CO[c].key != r) continue;
        int idx = 0;
        for (int q = 0; q < CO[c].n; q++) { u32 w = CO[c].kind[q] == 2 ? s->W[0][CO[c].row[q]] : CO[c].kind[q] ? EE(s, 0, CO[c].row[q]) : AA(s, 0, CO[c].row[q]); idx |= ((w >> CO[c].bit[q]) & 1) << q; }
        if (!((CO[c].allowed >> idx) & 1)) return 0;
    }
    return 1;
}
static inline int rowok(const St *s, int r) {
    u32 ax = AA(s, 0, r), ex = EE(s, 0, r), wx = s->W[0][r];
    static long dfm = -1;   // DIFFROW=r[,r...]: these rows checked on signed differences only (no derived value conditions)
    if (dfm < 0) { dfm = 0; const char *e = getenv("DIFFROW"); while (e && *e) { int v = atoi(e); if (v > 0) dfm |= 1L << v; while (*e && *e != ',') e++; if (*e) e++; } }
    if (!((dfm >> r) & 1) && !condok(s, r)) return 0;
    return ((ax ^ AA(s, 1, r)) == MA[r]) && ((ax & MA[r]) == SA[r]) && ((ex ^ EE(s, 1, r)) == ME[r]) && ((ex & ME[r]) == SE[r])
        && ((wx ^ s->W[1][r]) == MW[r]) && ((wx & MW[r]) == SW[r]);
}
static inline void sched(St *s, int i) { for (int m = 0; m < 2; m++) s->W[m][i] = s1(s->W[m][i - 2]) + s->W[m][i - 7] + s0(s->W[m][i - 15]) + s->W[m][i - 16]; }
static inline int inF7(u32 w) { return s0(w + D7) - s0(w) == T7; }

static void load(const char *fn) {
    FILE *f = fopen(fn, "r"); if (!f) { perror(fn); exit(1); }
    char key[32];
    while (fscanf(f, "%31s", key) == 1) {
        if (!strcmp(key, "D7")) fscanf(f, "%x", &D7);
        else if (!strcmp(key, "T7")) fscanf(f, "%x", &T7);
        else if (!strcmp(key, "ROW")) { int r; u32 a, b, c, d, e, g; fscanf(f, "%d %x %x %x %x %x %x", &r, &a, &b, &c, &d, &e, &g); MA[r] = a; SA[r] = b; ME[r] = c; SE[r] = d; MW[r] = e; SW[r] = g; }
        else if (!strcmp(key, "ST")) { int m, i; u32 a, e; fscanf(f, "%d %d %x %x", &m, &i, &a, &e); AA(&base, m, i) = a; EE(&base, m, i) = e; }
        else if (!strcmp(key, "COND")) { Cond *c = &CO[nCO++]; fscanf(f, "%d %d", &c->key, &c->n); for (int q = 0; q < c->n; q++) fscanf(f, "%d %d %d", &c->kind[q], &c->row[q], &c->bit[q]); fscanf(f, "%x", &c->allowed); }
        else if (!strcmp(key, "W")) { int m, i; u32 w; fscanf(f, "%d %d %x", &m, &i, &w); base.W[m][i] = w; }
    }
    fclose(f);
}

int main(int argc, char **argv) {
    load(argv[1]); uint64_t sd = strtoull(argv[2], 0, 10); int N = atoi(argv[3]), T = atoi(argv[4]);
    seed(sd);
    u32 dW16 = (s1(base.W[1][14]) + base.W[1][9]) - (s1(base.W[0][14]) + base.W[0][9]);   // W0, W1 carry no difference
    // row 16 exhaustive (cached)
    static u32 G[1 << 20]; long nG = 0;
    char cache[512]; snprintf(cache, sizeof cache, "%s.g16", argv[1]);
    FILE *fc = fopen(cache, "rb");
    if (fc) { nG = fread(G, 4, 1 << 20, fc); fclose(fc); }
    else {
        for (uint64_t w = 0; w < (1ULL << 32); w++) {
            St s; memcpy(s.A, base.A, sizeof s.A); memcpy(s.E, base.E, sizeof s.E);
            s.W[0][16] = (u32)w; s.W[1][16] = (u32)w + dW16; step(&s, 16);
            if (rowok(&s, 16)) { if (nG < (1 << 20)) G[nG] = (u32)w; nG++; }
        }
        if (nG > (1 << 20)) { fprintf(stderr, "G too large %ld\n", nG); nG = 1 << 20; }
        fc = fopen(cache, "wb"); fwrite(G, 4, nG, fc); fclose(fc);
    }
    if (argc > 5 && !strcmp(argv[5], "live")) {   // row-17 pass counts per G word (sampled W17)
        int live = 0; uint64_t S = 1ULL << 24;
        for (long gi = 0; gi < nG; gi++) {
            St s = base; s.W[0][16] = G[gi]; s.W[1][16] = G[gi] + dW16; step(&s, 16);
            uint64_t pass = 0;
            for (uint64_t k = 0; k < S; k++) {
                St t = s; u32 wx = r32();
                u32 dsch = (s1(t.W[1][15]) + t.W[1][10]) - (s1(t.W[0][15]) + t.W[0][10]) + s0(t.W[1][2]) - s0(t.W[0][2]);
                t.W[0][17] = wx; t.W[1][17] = wx + dsch; step(&t, 17); pass += rowok(&t, 17);
            }
            live += pass > 0;
            printf("G %08x row17 passes %llu / 2^24\n", G[gi], (unsigned long long)pass);
        }
        printf("live G words: %d of %ld\n", live, nG); return 0;
    }
    uint64_t f7 = 0; for (int k = 0; k < 1 << 20; k++) f7 += inF7(r32());
    double lv[8]; lv[0] = nG ? log2((double)nG) - 32 : -INFINITY;
    if (!nG) { printf("seed %llu row16 impossible\n", (unsigned long long)sd); return 0; }
    St *cur = malloc(sizeof(St) * N), *nx = malloc(sizeof(St) * N); int ncur = N;
    for (int k = 0; k < N; k++) { St s = base; u32 w = G[nxt() % nG]; s.W[0][16] = w; s.W[1][16] = w + dW16; step(&s, 16); cur[k] = s; }
    for (int r = 17; r <= 22; r++) {
        uint64_t tries = 0; int got = 0;
        while (got < N) {
            if (tries > (1ULL << 34)) { printf("seed %llu stalled at row %d\n", (unsigned long long)sd, r); return 0; }
            const St *p = &cur[nxt() % ncur]; tries++;
            u32 wx = r32();
            u32 dsch = (s1(p->W[1][r - 2]) + p->W[1][r - 7]) - (s1(p->W[0][r - 2]) + p->W[0][r - 7]);
            if (r == 22) dsch += T7; else dsch += s0(p->W[1][r - 15]) - s0(p->W[0][r - 15]);
            St s = *p; s.W[0][r] = wx; s.W[1][r] = wx + dsch; step(&s, r);
            if (rowok(&s, r)) nx[got++] = s;
        }
        lv[r - 16] = log2((double)(N - 1) / (double)(tries - 1));
        St *t = cur; cur = nx; nx = t;
    }
    FILE *dall = getenv("DUMPALL") ? fopen(getenv("DUMPALL"), "w") : 0;
    if (getenv("VARS")) {
        FILE *fv = fopen(getenv("VARS"), "r"); long cap = 1 << 22; VW = malloc(sizeof(*VW) * cap); int j; u32 a0, a1, a2, w8, w9, w10;
        while (nV < cap && fscanf(fv, "%d %x %x %x %x %x %x", &j, &a0, &a1, &a2, &w8, &w9, &w10) == 7) { VW[nV][0] = (u32)nV; VW[nV][1] = w8; VW[nV][2] = w9; VW[nV][3] = w10; nV++; }
        fclose(fv); fprintf(stderr, "variants %ld\n", nV);
    }
    uint64_t prop = (uint64_t)N * T, succ = 0, coll = 0;
    for (uint64_t k = 0; k < prop; k++) {
        St s = cur[k % N]; u32 w7; do w7 = r32(); while (!inF7(w7));
        s.W[0][7] = w7; s.W[1][7] = w7 + D7;
        long vi = -1;
        if (nV) { vi = nxt() % nV; for (int i = 8; i <= 10; i++) { s.W[0][i] = VW[vi][i - 7]; s.W[1][i] = VW[vi][i - 7] + (base.W[1][i] - base.W[0][i]); } }
        int ok = 1;
        static int relax = -1; if (relax < 0) relax = getenv("RELAX_TAIL") != 0;
        for (int r = 23; r < 38 && ok; r++) { sched(&s, r); step(&s, r); if (!relax) ok = rowok(&s, r); }
        if (relax) { for (int i = 34; i < 38 && ok; i++) if (AA(&s, 0, i) != AA(&s, 1, i) || EE(&s, 0, i) != EE(&s, 1, i)) ok = 0; }
        if (ok) {
            succ++;
            if (succ == 1 && getenv("DUMP")) {
                FILE *fd = fopen(getenv("DUMP"), "w");
                for (int m = 0; m < 2; m++) for (int i = 0; i < 38; i++) fprintf(fd, "W %d %d %08x\n", m, i, s.W[m][i]);
                fclose(fd);
            }
            if (dall) { fprintf(dall, "S %ld", vi); for (int i = 7; i < 38; i++) fprintf(dall, " %08x", s.W[0][i]); fprintf(dall, "\n"); }
            int eq = 1; for (int i = 34; i < 38; i++) if (AA(&s, 0, i) != AA(&s, 1, i) || EE(&s, 0, i) != EE(&s, 1, i)) eq = 0;
            coll += eq;
        }
    }
    lv[7] = succ ? log2((double)succ / prop) : -INFINITY;
    double tot = 0; for (int i = 0; i < 8; i++) tot += lv[i];
    printf("seed %llu |G| %ld p2 %.4f stages", (unsigned long long)sd, nG, log2((double)f7 / (1 << 20)));
    for (int i = 0; i < 8; i++) printf(" %.3f", lv[i]);
    printf(" | succ %llu coll %llu | log2q %.4f%s\n", (unsigned long long)succ, (unsigned long long)coll, tot, nV ? " (variant tail)" : "");
    if (dall) fclose(dall);
    return 0;
}
~~~

### `prep.py` (sha256 7550447964f6b5444638db1b60142475ea839cb066e262b6bfeb6d713b957299)

~~~python
"""prep.py <char.json> <pair.json> <out.dat> [inter.json]: data file for q3t.c (own code).
pair.json: {"cv": [8 words], "Wx": [16], "Wy": [16]} (dense pair; if it is a full 38-step
conforming pair and no inter.json is given, intermediates of rows >= 16 are taken from it).
inter.json: {"S1_16": row, ...} intermediate signed outputs from the SAT solution."""
import sys, json
sys.path.insert(0, '/work/m38'); sys.path.insert(0, sys.argv[0].rsplit('/', 1)[0])
from sha38 import trace, s1, M32
from cond import derive, check, intermediates_from_pair
C = {int(k): v for k, v in json.load(open(sys.argv[1])).items()}
P = json.load(open(sys.argv[2]))
cv, Wx, Wy = P['cv'], P['Wx'], P['Wy']
ax, ex, _, _ = trace(cv, Wx, 16); ay, ey, _, _ = trace(cv, Wy, 16)
def ms(row):
    m = sum(1 << (31 - k) for k, c in enumerate(row) if c in 'un'); s = sum(1 << (31 - k) for k, c in enumerate(row) if c == 'u')
    return m, s
def sval(row):   # y - x for the signed row ('u': x = 1, y = 0)
    return sum((-(1 << (31 - k)) if c == 'u' else (1 << (31 - k))) for k, c in enumerate(row) if c in 'un') & M32
out = []
for r in range(16, 38):
    row = C.get(r, {'A': '=' * 32, 'E': '=' * 32, 'W': '=' * 32})
    out.append('ROW %d %08x %08x %08x %08x %08x %08x' % ((r,) + ms(row['A']) + ms(row['E']) + ms(row['W'])))
for m, (A, E) in enumerate(((ax, ex), (ay, ey))):
    for i in range(-4, 16): out.append('ST %d %d %08x %08x' % (m, i, A[i], E[i]))
for m, W in enumerate((Wx, Wy)):
    for i in range(16): out.append('W %d %d %08x' % (m, i, W[i]))
assert all(c not in 'un' for c in C.get(20, {'W': '='})['W']), 'W20 difference not supported'
d7 = (Wy[7] - Wx[7]) & M32
t7 = (sval(C.get(22, {'W': '=' * 32})['W']) - ((Wy[15] - Wx[15]) & M32)) & M32
out = ['D7 %08x' % d7, 'T7 %08x' % t7] + out
# value conditions of the boolean functions of steps 16..37
rows = {}
for i, r in C.items():
    rows[('A', i)] = r['A']; rows[('E', i)] = r['E']; rows[('W', i)] = r['W']
if len(sys.argv) > 4:
    I = json.load(open(sys.argv[4])); inter = {(k.split('_')[0], int(k.split('_')[1])): v for k, v in I.items()}
else:
    fx, fy = trace(cv, Wx, 38), trace(cv, Wy, 38)
    inter = intermediates_from_pair((fx[0], fx[1]), (fy[0], fy[1]), range(16, 38), fx[2], fy[2])
conds, bad = derive(rows, inter, range(16, 38))
assert not bad, ('impossible boolean instances', bad[:5])
Ax, Ex = ax, ex
early = [c for c in conds if c['key'] <= 15]
fails = check(early, lambda k, i: {'A': Ax, 'E': Ex, 'W': dict(enumerate(Wx))}[k][i])
print('conditions: %d (keyed <= 15: %d, violated by the dense pair: %d)' % (len(conds), len(early), len(fails)))
for c in fails[:10]: print('  violated', c['src'], c['refs'], c['allowed'])
for c in conds:
    if c['key'] <= 15: continue
    am = sum(1 << sum(b << q for q, b in enumerate(t)) for t in c['allowed'])
    out.append('COND %d %d %s %x' % (c['key'], len(c['refs']), ' '.join('%d %d %d' % ({'A': 0, 'E': 1, 'W': 2}[k], i, b) for k, i, b in c['refs']), am))
open(sys.argv[3], 'w').write('\n'.join(out) + '\n')
from collections import Counter
print('conditions per key row:', sorted(Counter(c['key'] for c in conds).items()))
print('D7 %08x T7 %08x' % (d7, t7))
~~~
