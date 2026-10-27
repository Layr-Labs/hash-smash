# Blocks of 64 representatives: opened lists and dead blocks, over chunks, a pending batch and the test of (1) first — current amendment

This amendment defines the current candidate. It has fourteen layers over the inherited dossier below: (A) the natural-bit descriptor layout of promoted submission 1e179f43; (B) a recalibration of four declared premise margins against evidence that the dossier already reports (submission 785acf86); (C) a second copy of the opened-cluster code, paid for by memory below the existing peak; (D) opened clusters charged by the partner lanes they walk; (E) steps 2 and 3 charged at the instruction counts of their emitted code (Section 19; submission 034414ab); (F) refunds of the unexecuted part of a row's prelude at its early exits, with H5_exec a measured premise (submission 41128eca); (G) the descriptor table of a context in packed fields (submission 0ea30357); (H, I, K) cluster tests at the high half of omega (submissions aec9831b, fef8fa3c, 0728415d), now historical; (J) chunk A of seven survivors, a pending batch for the others and prepaid fills, which retire G_BUDGET and the premise H_G_cluster (submission e8bc190d); (L) the test of (1) first in chunk A and pending lanes, which retires E_BUDGET (submission c6d1a197); (M) a two-bit pre-test of Y9 before that read (submission 53570f13); and, new in this package, (N) a walk by blocks of 64 representatives: each block is first tested, with at most two table reads, for whether any member can pass test (2) at all (44 per cent cannot), and a block that is kept runs only its 26 opened representatives, read from one of four lists that the context computes once (Lemma NA), so the 2,341 representative batches with their gate words and gate tests, the state tests, the tests of H, I and K, A_BUDGET and NP_BUDGET are gone; H_LZ is re-measured (v11). Layers A to G are those of submission 0ea30357, B condensed. The target, construction, advice record, filter, gate values, walk of an opened cluster, solver code and success event are unchanged. Every inherited number that depends on the changed constants (FACTOR at 97/100, 0.49594, the slack 0.001 and rho_c <= 0.0065, the factor 1.01 of H5_exec on the old u_U, the fill mean 7,198, the units 16 of entry and return, 104 of the chunks, 168 and 93 of U_OPEN as the charge of every opened cluster, 614, 2,304, 1,354, 20, 4, 64, 48, 80 and 120 of the solver, 15,012 and 4,272, u_U, L_PL and PL_BUDGET, the context charges 57,162, 57,226 and 57,373, the batch charges 52, 55, 40 and 43, U_HEAD, U_2ND, U_NP, U_FB, the L_Z of H to M, A_BUDGET, NP_BUDGET, E_BUDGET and the E lane as a counted event, the fill budget G_BUDGET with the mean 7,164 of H_G_cluster and the fill as a counted event, RUN_CONTEXTS, RUN_STEPS, s, the budgets, m_C, CREDIT, WB, W_CTX, N and time_log2, and the ledger programs of Section 18 of the predecessors) is historical and superseded by the values here.


## A. Descriptor layout (1e179f43, unchanged)

In the ordinary search the descriptor branch is reached only with gate value 1 and `mk=True`: the cluster does not straddle and the low seven bits of omega lie in S7. There PXR only mapped that condition and omega bit 8 to a descriptor. The layout stores the descriptor of carry index ix and b8 at `DB + ixoff(ix) + (b8 << 8)`, DB = 2^32; chunk headers at offsets 0 and 4, payloads at 1, 2 and 5, 6; ix occupies bits 9, 10, 17 and 25, disjoint from bit 8 and from the offsets. Each representative batch ORs a precomputed DB marker into its seven 36-bit lanes once (all markers fit below bit 249; masking removes other lanes); selection is `(IX >> shift & (IXM | DB)) + (omega & 256)`. No PXR or PXT table exists. Forced-open diagnostics alone keep empty headers at the address plus 128; they authorize no shortcut in the attack. Costs: one unit less per non-straddling opened cluster, one OR per representative batch (2,341 per context): U_IX 18, selection 5, U_OPEN 167 (165 after C), straddling surcharge U_FB 209 (straddling path 376, 374 after C), U_CONTEXT 93,258. Removing PXR (65,536 words) and adding two instructions puts the search phase below 29,848,320 bytes. Its equivalence checks are those of 1e179f43.

## B. Recalibrated premise margins

**B1. Rate factor of H1' (i): 98/100.** FACTOR = floor(98 * 138,512,695,296 / 100) = 135,742,441,390, q = 2^-91.0179. Evidence (Section 13): the preregistered 8-bit end-to-end rerun found 40,882 collisions against 40,800.63 predicted (1.00199 +- 0.00496, one-sided 97.7 per cent lower bound 0.99213, which its pre-fixed rule accepts for 100/98); the 32-bit whole-class E1 measurements give 1.0020 +- 0.0086 and 0.9988 +- 0.0070. Limits: the 8-bit bound at 1 - 10^-9 is 0.97256, the older sub-class E1 measurement has a two-sigma bound 0.9756, and the joint event at 2^-91 is not measured: a score-critical assumption. Effect: -0.01477.

**B2. Dependence clause of H1' (ii) and run length.** P(no valid trial of the run is listed good) <= exp(-0.49436) + 0.000038 = 0.6099992, sufficient condition rho_c = E[N_c (N_c - 1)] / E[N_c] <= 2^-12 (Lemma S8: b(rho_c) >= 1 - 2^-13, probability at most 0.6099980); success >= 1 - 0.6099992 - 2 * 10^-8 = 0.3900008 > 0.39 with the tails of the amendment. The cross-member part fails only if listed good trials cluster by context more than about 2^39 times (measured ratios at most 1.94, Section 13); the within-step part rho_w is not measured. Effect: -0.00460.

**B3. H5_exec factor 1.001** on the old u_U (superseded by E and F). Effect: -0.00304.

**B4. H_G_cluster mean 7,164** (empirical Bernstein at 10^-9 on the preregistered 2^24-context sample, mean 7,159.2660): historical, the premise is retired by J. Effect then: -0.00103.

## C. Two copies of the opened-cluster code

The code of an opened cluster (9.9, Section 12: fewer than 2^17 instructions, with a return tree of fewer than 2^7) is written twice, identical except for the immediates of its return tree. Copy 1 serves 19 of the 28 representative lane sites of the loop body; copy 2 serves the other 9 and the 10 sites of the last batch. A site that opens a cluster sets K and the base and jumps to its own copy (3 units, as before); each copy's return tree selects among its 19 continuations by a balanced tree of five comparisons of K with an immediate, each with its branch (10 units, 2^4 < 19 <= 2^5), in place of six for 38 targets. Entry and return cost 3 + 10 + 1 in reserve = 14 in place of 16: U_OPEN = 165, U_FALLBACK = 371, the straddling surcharge stays 209 (straddling path 374). Registers, words, lane reads and the order of work are those of 9.9; nothing is stored differently. Memory: the second copy and its return tree add fewer than 2^17 + 2^7 = 131,200 instructions, 4,198,400 bytes, so the search phase is below 29,848,320 + 4,198,400 = 34,046,720 bytes, still below the historical construction peak 37,928,960; memory_log2_bytes is unchanged. The Python experiment does not model code layout and charges U_RET = 14. Effect: -0.00722.

## D. Opened clusters charged by the partner lanes they walk

An opened cluster that does not straddle walks only the survivors of Lemma XF (c), in its two chunks. Since j -> o(IX, j) is a bijection (Lemma XF (a)), their number is exactly popcount(LW[b8]) - alive16 of the representative, that is 8 or 9 minus 0 or 1, where b8 is bit 8 of the representative's omega. Section 11 charged every such cluster the worst case, 104 = c(n_A) + c(n_B) with n_A + n_B = 9. This amendment charges two chunk headers, 32, in U_OPEN, which becomes 93, and 8 more for each partner lane that a chunk walks. The additions to W: chunk A's dispatch leaf adds u_O + 8 n_A in the one addition that U_BOOK already pays, and chunk B's leaf adds 8 n_B in one more addition, paid by the unit in reserve of U_RET (C). The 8 is the lane test (7 in lane 0); the omega side of each chunk is in the 32. For each chunk this is at least c(n) = 16 + 8 n, and 16 more for an empty chunk. Straddling clusters keep their path of 374 and pay U_FB = 374 - 93 = 281.

The partner lanes had the budget PL_BUDGET under the measured premise H_PL, E[L(C)] <= 54,846 partner lanes per context (2^27 i.i.d. SHAKE256 samples, protocol SHA-256 e917c6ce...ce8ab, mean 3.3451954 per cluster, empirical Bernstein bound at 10^-9; 851,971 recounts with 0 mismatches), with the eighth tail of 10.4; Section 11 had charged 59,916. Effect: -0.02621. This budget and premise are historical: H and I charge the partner lanes inside Z, with Z_BUDGET in place of PL_BUDGET and H_LZ in place of H_PL.

## E. Steps 2 and 3 charged at the instruction counts of their emitted code

Section 19 emits the code of steps 2 and 3 from `emit_b3z7.py`: the joint solver of the six rows of S with (G7), (G15) and the root certificate, the entry stubs and the global ledger. Its machine charges one unit per instruction. Every branch is forward, except the seven stub jumps to the common entry, so no instruction runs twice in a call.

Section 11 charged allowances for these blocks. This amendment charges each block the largest instruction count the emitter reports for blocks of its kind, meter debits included:

| Block | Old allowance | New charge |
| --- | ---: | ---: |
| Global ledger | 614 | 184: emitted 152 (stub at most 22, entry 60, the six row tests 12, exit 58) plus 32 for the lane-side call and return (below) |
| Family | 2,304 | 0 (each row's code repeats the family formulas) |
| Row | 1,354 | 1,089 |
| Forced node | 20 | 16 (10 to 16) |
| Selected node, position 20 | 4 | 0 (14 in all) |
| Position-15 surcharge | 64 | 11 (27 in all) |
| Free node | 48 | 17 |
| Leaf | 80 | 35 |
| Root | 120 | 88 |

The six row preludes (set-up and descriptors, with (G7) and the (G15) words) have 1,084, 1,039, 1,089, 1,037, 1,038 and 1,030 instructions.

The emitted `RET` stands for one branch back to the calling lane site; the dispatch among the call sites is lane code, which Section 19 does not emit. It is charged 32 inside the global 184: the site sets its number K and the lane words r0 to r8 that it already holds (at most 10 moves), and the return reaches its site through a tree of at most 10 comparisons of K with an immediate, each with its branch (fewer than 2^10 call sites: 2 * 202 + 38 lane sites), 20; 1 + 10 + 20 = 31 <= 32. The emitted meter reads these constants from frontline.py, so V = U of Lemma ME holds as before, and every call executes at most what it debits. As a result:

- A(T) = 184 + 1,089 r.
- ROW_CAP is 2,326 for a row with three free positions and 3,516 for one with four.
- CM(T) <= CM(0x52) = 7,115 for every T that occurs (was 15,012). L_C and the preflight reserve use 7,115.
- Lemma CP: every call has U >= 1,273 (was 4,272), and CALL_BUDGET = ceil(m_C / 1,273) + 2^19 s.

Model value:

- From the n_X certificate of 10.3, E_M[A(T) | call] = 184 + 1,089 * 354,874,366,665 / 279,070,422,111 = 1,568.81 exactly.
- Every new node charge is at most 4/5 of its old one (16/20, 27/84, 17/48, 35/80, 88/120). So the tree part is at most 4/5 of GPT-6 Astra's 22,422,672 / 266,237 per call, that is 67.38.
- Hence u_U' = p_call (1,568.81 + 67.38) <= 114,152,488,153,336 / 2^48 = 0.405551. H5_exec is restated as E[U] <= 1.01 u_U'. The factor is 1.01 again, not B3's 1.001, because the evidence for the new ledger is indirect.

Validation used an independent interpreter of the Section 19 machine, written by the participant from the emitter's opcode list and not part of the package. It ran in the pinned networkless image:

- With the historical charges, on 957 real calls captured from the walk of frontline.py and 600 planted-root cases, it matched frontline.py's solver in every case: the same roots in the same order, the same debits, and the 57 saved registers restored. Every planted root was returned.
- With the charges of this amendment, on 1,944 real calls and 600 planted cases, every call executed at most its debit. Real calls executed 834 (the stub counted at its 22) instructions on average against a mean debit of 1,546.
- A uniform sample of 2^30 outer steps (F) gives 0.3947528 per outer step for this ledger, 0.9734 of u_U'. (The walk of the experiment covers a fixed, unrepresentative set of clusters and is not used as evidence.)

The historical Section 13 measurements of U still describe the call frequency and the T law: calls are 0.99604 of the model frequency, and the pre-check keeps 0.249980 of passing outer steps. Effect: -0.24208.

## F. Refunds of early exits from a row's prelude

A row's prelude (set-up and descriptors, at most 1,089 instructions) is charged in full by A(T), but it stops early at 47 exit branches to the row's end label when the row can hold no joint root (the guesses of (a), the tests of (b) and (e), the phase checks). The post-pass `emit_dyn.py` (Section 19) redirects each such branch to a two-instruction stub at the end of the code: an addition of the refund 1,089 - L - 2 to the credit register and a jump to the end label, where L is the longest path, in instructions and branch included, from the prelude's first instruction to that branch (a longest path in the prelude's forward-branch graph). A call that leaves a row at that exit is therefore debited L + 2 for it, at least what it executed there, and a row that reaches its tree is still debited 1,089. Nothing else changes: the same roots, the same traversal and node debits, A(T) and CM(T) as in E, and the preflight. The exits charge 68 to 578 (rows 175 to 685), so every call has U >= 184 + 68 = 252 (Lemma CP), and CALL_BUDGET = ceil(m_C / 252) + 2^19 s. The code grows by 94 instructions to 17,361 (3,008 bytes; the search phase stays below 34,049,728 bytes).

The ledger U of H5_exec is now this refunded debit, and there is no exact model value for it, so **H5_exec is restated as a measured premise**: for a uniform outer step, E[U] <= u_U = 65,117,111,395,830 / 2^48 = 0.2313425, and m_C = ceil(RUN_STEPS u_U). The value comes from a participant measurement under a protocol fixed before the run (SHA-256 dba4dc7256796297e20bb248b0c7b5e38ac5c149ea0486dfaa3deb691b94f070), in the pinned networkless image. It drew 2^30 i.i.d. uniform outer steps (SHAKE256 words; seven outer words and a uniform member) and ran each call on the participant's interpreter of the code of Section 19 with this post-pass. Every call was checked: the same roots in the same order as frontline.py's solver, executed instructions plus 53 at most the refunded debit, and that debit at most the debit of E (0 failures in 265,740 calls). Results:

| Quantity | Value |
| --- | --- |
| Calls per outer step | 0.00024749 (0.99849 of the model's p_call) |
| Rows per call | 1.27116 (model 1.27163) |
| Mean refunded ledger per outer step | 0.2290168 (standard error 0.0004896) |
| Declared u_U = mean + 4.75 SE (one-sided normal, 1 - 10^-6) | 0.2313425 |
| Mean ledger of E per outer step | 0.3947528 (SE 0.0008061), 0.9734 of E's model value 0.405551 |

The last row is a direct, unbiased check of E's premise. The time bound charges the whole credit whatever the premise; if it fails, the credit can halt the run with failure, which lowers the success probability only. Effect: -0.06126.

## G. The descriptor table of a context in packed fields

Section 9.9 charged the descriptor table 48,896 a context. The window arithmetic of o(IX, j) has no carry out of five bits, so for one IX all 32 values j are computed at once in 8-bit fields of one word (field j starts as 16 + j): XOR with the broadcast window of C0.b1, addition of that of -C0.c1 plus c17, AND with 31 in every field, likewise for C0.d1 and K' + c25, S15' and -S0 - S5 + c9a, and the word of 1 + 2 (j mod 16) + c9b: 11 operations. Bit o of LW[0] is set exactly when ((o + 3) mod 32) AND 24 = 0, and of LW[1] when (((o + 4) mod 32) + 7) AND 48 = 0; their zero fields are the survivors. `ds_build` of frontline.py computes the table this way (checked against the earlier construction on 3,000 random contexts). Charge: nine broadcast words 128; 24 per IX, 384; at most 289 per descriptor (two scans of field tests, the chunk choice, the placement of each survivor, six stores and initialisation), charged 320, 10,240; setup 2,048: 12,800 a context. Effect: -0.02488.

## H, I and K. Cluster tests (historical; retired by N)

Layers H, I and K (submissions aec9831b, fef8fa3c and 0728415d) read, at each opened cluster, a table at the high part of the representative's omega (and, in a shadow context, of a shadow member j*) and skipped the clusters in which no member can pass test (2). Layer N tests whole blocks first; on the measured stream 99.93 per cent of the opened clusters of the blocks that N keeps were found live by these tests (H_LZ v10 below), so N drops them, with HE, HE3, HR, HS, the shadow word om', j*, HM, U_2ND, U_NP and NP_BUDGET. Two facts of H remain in use. *Plain contexts:* with R_j = ((16 + j) XOR b[17..22]) + 64 b[23] for j = 0 to 31 and Cc = c[17..23] (b = C0.b1, c = C0.c1, d = C0.d1), a context is *plain* when all 32 values R_j are below Cc or all are above it, which has probability 5/8. *Lemma HX (its first step):* member j of any cluster has r_j[17..23] = R_j, where r = ROL(y, 7) XOR b, since ROL(y_j, 7) has bits 17 to 22 equal to 16 + j and bit 23 equal to y[16] = 0 (Lemma XF (a)).

## J. Chunk A of seven, a pending batch and prepaid fills

This layer was submitted as e8bc190d. It changes only how the survivors of a live cluster are grouped into batches; every survivor is walked exactly once, with its lane test, E handler and passing lane as before.

*Chunks.* A live non-straddling cluster has S = popcount(LW[b8]) - alive16 of the representative survivors (Lemma XF (c)), and S is 7, 8 or 9 since LW[0] and LW[1] have 8 and 9 bits. The descriptor of 9.9 now puts the first seven survivors, in increasing j, in chunk A, always a full batch of seven lanes (no dispatch), and the S - 7 <= 2 others in chunk B. The lanes of chunk B are appended to the *pending batch* of the context, two words U and E and a count n_P in memory: when n_P + n_B > 7 the pending batch is first run (*flushed*) as a batch of 9.8 with n_P lanes and its own cache, then the chunk-B lanes are appended. Every flush inside a context therefore runs at least 6 lanes; the last pending batch of a context is flushed after its last block. All lanes of a pending batch belong to one context, so the omega side and the Y9 path of 9.8, which read the words of the context, give their values (Lemma MB: lane values are U and E of the member, ROL(y_j, 7) = ROL(y_0, 7) + 2^17 j and e_j = e_0 + 2^10 j, Lemma XF (a)); only the order of the outer steps changes.

*Units.* A live cluster, under N: the representative's lane test 8, W and the end jump 3, the descriptor selection 5, the broadcasts 5 (N), the omega side of chunk A 16, its JU and JE 5, the load and test of n_B 3, the entry and return 14 (C) and the fill of chunk A, 56, prepaid whether or not it occurs: U_LIVE = 115 (J charged 122 with the state test 3, the test of H 5 and broadcasts of 4); its 7 + n_B lanes as in L and M. A cluster with n_B > 0 adds U_BN = 23: the dispatch on n_B 2, the load of JU_B with its address 2, U_B and E_B from the broadcasts with their lane masks 5, the load, test and branch of n_P 3, two loads, shifts, ORs and stores of the pending words 8, the update of n_P 2 and its addition to W 1. A flush costs at most 83 (two loads 2, the dispatch on n_P 6, the omega side 17, the reset of n_P 1, the return 1 and the fill 56; its lane tests are paid by their clusters); it runs at least 6 lanes, so each chunk-B lane prepays U_BL = 14 >= 83 / 6, and the last flush of a context, 83, written once more after the block loop so that it returns to no caller, is in U_CONTEXT. G_BUDGET, its tail and the premise H_G_cluster are not used: fills are inside Z, U_SC and U_CONTEXT. Checks of J (participant): on 512 trials of the earlier layout the same members, E lanes, passes and calls as I, 0 skipped passes and 0 mismatches. Memory: 3 words.

## L. The test of (1) first in chunk A and the pending batch

This layer was submitted as c6d1a197. In a chunk A or pending batch the fill of J is prepaid and its Y9 path runs in any case; L reads the mask of (1) first. Each lane of such a batch shifts the cached Y9 to lane 0 (1), ANDs with 2^34 + 2^16 - 1 (1), loads R1 (1), ANDs with 2^26 - 1 (1), adds (1), loads L1 (1), compares and branches (2): 8 units. Only when the mask of (1) is not 0 does the lane run the test of (2) on its omega (shift, AND, load of R2, AND, addition, load of L2: 6), AND the two masks, compare and branch (3) and add to W (1): U_M2 = 10; a nonzero AND then runs the passing lane of 9.8 as before. *Lossless:* a lane passes the filter exactly when the masks of (1) and (2) meet (Section 8, Lemma MB (c)), so a lane whose mask of (1) is 0 cannot pass, whatever its mask of (2), and the order of the two reads changes no decision, no pass, no call and no N_o. The cached Y9 is exact in every used lane (the proof of Lemma MB is lane by lane). Representative lanes keep the order of 9.8 (lane test, then the E handler and the fill of their batch); straddling partner batches keep it too, with their 31 E handlers prepaid in U_SC. E lanes are no longer a counted event: E_BUDGET, its tail and the E-lane share of H4' are not used (H4' still gives PASS_BUDGET).

## M. A two-bit pre-test of Y9

This layer was submitted as 53570f13. **Lemma M2.** If bit 0 or bit 1 of a word x is 1, the mask of (1) of x, restricted to S, is 0. *Proof.* A finite check on the automaton of (1) of Section 8: from the state after any first byte b with b AND 3 not 0, no entry of the following byte tables reaches a nonzero final mask (`frontline.py --selftest`, item M2bit, all 192 such bytes and every continuation; Lemma J0's proof: Q[0] = Q[1] = 0). QED. So in a chunk A or pending lane the mask of (1) is read only when Y9 mod 4 = 0: the lane ANDs the cached Y9 with 3 shifted to its lane (an immediate), compares and branches (3 units); a lane with a nonzero result cannot pass, and the others run the read of L (8) with an addition to W (1): U_T1 = 9. A lane of chunk A or of the pending batch therefore costs 3 + 9 [Y9 mod 4 = 0], and 10 more when its mask of (1) is not 0; a chunk-B lane prepays 3 + 14. Lossless by Lemma M2.

## N. Blocks of 64 representatives: opened lists and dead blocks

New in this package. It replaces the loop of 2,341 representative batches of 9.9 (with their gate words, gate tests and state tests) and the cluster tests of H, I and K by a loop over the 256 *blocks* of a context. Every outer step that it walks is walked as before, with the same lane tests, chunks, passing lanes and solver; only the order and the skipped work change.

*Blocks.* Cluster g (9.9) is g = u + 64 beta with u = e[2..7] of its representative and beta < 256 carrying e[20], e[21] and e[26..31]. The representatives of block beta are e_u = e_beta + 4 u and y_u = y_beta + 4 u, where e_beta, y_beta are those of u = 0: e mod 2^10 = 303 + 4 u > 181 = Y3 mod 2^10 (hexadecimal), so no borrow of y = e - Y3 passes bit 9 and y mod 2^10 = 182 + 4 u < 2^10; hence ROL(y_u, 7) = ROL(y_beta, 7) + 2^9 u. Every member of the block has the same e[16..31] (the class fixes bits 16 to 19 and 22 to 25, beta the others), the same i = e[20..21] and, by Lemma OR (a), the same r0 = r[0..7] = (ROL(y_beta, 7) XOR b) mod 256 and p8 = p[8..15] = ((r0 - c) mod 256) XOR d[8..15]; the block *straddles* when p8 = A[8..15] and hbad_i = 1, and then every cluster of it straddles.

**Lemma NA (the opened list of a block).** Fix a context and a block that does not straddle. Put br8 = [r0 < c[0..7]], br16 = [p8 < A[8..15]] when p8 != A[8..15] and br16 = [lo0_i < A[0..7]] when they are equal, with lo0_i of 9.9. Then the representative u of the block has gate value 1 when u lies in OL(br8, br16) = {u < 64 : (1 + 2 z + P(z)) mod 128 lies in S7, z = (2 u - 63) mod 128}, with P(z) of Lemma OR (b) built from these two borrows and the six slices b[8..14], c[8..14], d[16..22], A[16..22], L[0..6] and (S0 + S5)[0..6] of the context, and gate value 0 otherwise; OL(br8, br16) has 26 elements.
*Proof.* Lemma OR (b) proves omega mod 128 = (1 + 2 z + P(z)) mod 128 for the representatives of a block that does not straddle, with br8 the borrow into bit 8 of v = r - c, which is [r0 < c[0..7]] since r0 is common to the block, and br16 the borrow into bit 16 of x = p - A, which is common to the block (proof of Lemma CL): it is [p8 < A[8..15]] when p8 != A[8..15]; when they are equal it is [p[0..7] < A[0..7]] with p[0..7] in {lo0_i, lo1_i}, and hbad_i = 0 says exactly that A[0..7] does not separate the two, so it is [lo0_i < A[0..7]]. Off straddle the gate value is 1 exactly when omega mod 128 lies in S7 (9.9), and Lemma OR (b) shows that 26 of the 64 do. QED. `frontline.py --selftest` item NA compares OL with the gate values computed from step CO on every block of six contexts (1,536 blocks), and the program compares them on every block it walks.

**Lemma NB (the high half of omega on a block).** Fix a context and a block, and put lo_0 = lo0_i, lo_1 = lo1_i, X_l = (2^8 p8 + lo_l - A) mod 2^16 and h_l = ((X_l XOR L[16..31]) + e_beta[16..31] - (S0 + S5)[16..31]) mod 2^16 for l = 0, 1. (a) Every member of the block has omega >> 16 = h_l + delta modulo 2^16 for some l in {0, 1} and delta in {-1, 0, 1}, and delta != 1 when (S0 + S5) mod 2^16 > 7fff. (b) In a plain context every member of every block has l = l* = [R_0 < Cc].
*Proof.* (a) For every member r[24..31] = T_i XOR b[24..31] (proof of Lemma CL), so v[24..31] is H_i or H_i - 1 and p[0..7] = lo_l with l the borrow into bit 24 of v = r - c; with p[8..15] = p8, x mod 2^16 = (p - A) mod 2^16 = X_l. ROL(x, 16) has high half x mod 2^16, so omega = (ROL(x, 16) XOR L) + C with C = e - S0 - S5 gives omega >> 16 = (X_l XOR L[16..31]) + C[16..31] + kappa modulo 2^16, kappa in {0, 1} the carry out of the low halves, and C[16..31] = e[16..31] - (S0 + S5)[16..31] - lambda, lambda = [e mod 2^16 < (S0 + S5) mod 2^16]; e[16..31] = e_beta[16..31], and delta = kappa - lambda. Bit 15 of e is 0, so e mod 2^16 <= 7fff and lambda = 1 when (S0 + S5) mod 2^16 > 7fff. (b) r_j[17..23] = R_j (H); in a plain context R_j is never Cc and lies on the side of R_0, so the borrow into bit 24 is [r_j[17..23] < Cc] = l* for every member of every cluster. QED.
*Dead blocks.* HE16[h] = 1, for h < 2^16, when some state of the automaton of (2) after bits 0 to 15 (any of the 7 rows of its third byte table) gives a nonzero mask, restricted to S, on the high half h; HW[h] = HE16[h - 1] OR HE16[h] OR HE16[h + 1] and HM[h] = HE16[h - 1] OR HE16[h], indices modulo 2^16 (33,696, 35,424 and 34,560 ones). A word x with T2[x] != 0 has HE16[x >> 16] = 1. A context uses H* = HM when (S0 + S5) mod 2^16 > 7fff and H* = HW otherwise, and the set Lambda = {l*} when it is plain and {0, 1} otherwise. A block is *dead* when H*[h_l] = 0 for every l in Lambda; by Lemma NB no member of a dead block has T2[omega] != 0, so none is an E lane, passes the filter or holds a listed good trial (Lemmas MB (c) and F), and skipping it changes no E lane, fill of a walked batch, pass, call, debit or N_o, outer step by outer step (as for Lemma CL). On the measured stream 44.0 per cent of the blocks are dead.

*The walk of a context (replaces the representative loop of 9.9).* *Once (step 0):* the block records, for each beta, R0 = ROL(y_beta, 7) mod 256, the address of the class words of its i, e_beta >> 16 and the broadcast words Ub and Eb of ROL(y_beta, 7) and e_beta (5 words, below 2^14 units for all); HW and HM (2^17 words, below 2^21 units, added to ONCE); and ten fixed batch words for the straddling path (the u of each of its batches of 7, 2^9 u in lane t). *A context (N0)* forms the six slices, the four lists OL(br8, br16) in increasing u, for each four batch words JU (2^9 u in lane t of batch k for the (7k + t)-th element; JE = JU >> 7) and 26 broadcast offsets BO (2^9 u in all seven lanes), and for each i the X offsets (lo_l - A) mod 2^16 of Lambda, the borrow word [lo0_i < A[0..7]] and hbad_i, and picks H* and the code copy: on packed 8-bit fields, 2 * 15 operations per list for P(z) and S7, 280 for the field constants, 3 a field to scan the 64 fields of each list, 3 per element for JU, 9 per BO with its store, 32 for the JU stores and 120 for the class words and the context words: 120 + 280 + 768 + 312 + 936 + 32 + 120 = 2,568, charged U_N0 = 2,688. The plain test of H (64) stays in U_CONTEXT; j* and the class rule of I are gone.
*A block*, its code written out twice, once with Lambda = {l*} for plain contexts and once with Lambda = {0, 1}. *Test* (scalar; an address base + immediate is one addition, as in 9.9): reload the six context words it uses, b[0..7], -c[0..7], d[8..15], -(S0 + S5)[16..31], L[16..31] and the base of H*, from fixed addresses (6; they are not kept in registers, so the register count of the batches is not raised), load R0 at q (1), XOR with b[0..7] (1), add -c[0..7] and AND 255 (2), XOR with d[8..15] (1), shift left 8 (1), load the class-word address at q + 1 (2) and the X offset of l there (1), add and AND with ffff (2), load e_beta >> 16 at q + 2 (2) and add -(S0 + S5)[16..31] (1), XOR with L[16..31], add and AND with ffff (3), add the base of H* and load (2), compare and branch (2), and add the block's units to W (1): 28 units, 38 with the second l (2 + 2 + 3 + 2 and an OR), and the loop step 3 (address, end, branch): U_BT = 31 in the plain copy and 41 in the other. A dead block ends here. *Class:* c[0..7] and A[8..15] reloaded (2), br8 by a comparison (1), p8 against A[8..15] (comparison and branch, 2), br16 (1), the list index br8 + 2 br16 (2) and the list address (2): U_CMB = 10; when p8 = A[8..15], hbad_i is loaded and tested and br16 is the loaded borrow word: U_BSL = 8 more. *A straddling block* runs its 64 representatives in ten batches from the fixed words (Ub and Eb at q + 3 and q + 4, 4; each batch its fixed JU with its address 2, U 1, E 2, the omega side 17 and the loop step 3, 25: 254 <= 4 * 64 for the block), and every cluster takes the straddling path of 9.9 (five partner batches, prepaid fills and E handlers): U_SC = 4 + 8 + 12 + 9 + 4 * 72 + 40 + 5 * 56 + 31 * 10 + 25 + 14 = 990 per cluster (the block share 4; the representative's lane test 8, E handler 12 and fill share 9; the five batches, fills and E lanes; 25 for the partner words: the representative's broadcasts, the fixed offset word of its u with its address, its load and the additions and shift of the broadcasts, 5, the five partner offsets 2^17 j and 2^10 j as immediates added to the two broadcasts, 10, and W, 1, 16 of the 25; entry and return 14), with FB_BUDGET. *Otherwise* Ub and Eb are loaded at q + 3 and q + 4 (4) and the four batches of 7, 7, 7 and 5 opened representatives run: JU loaded at the list address plus k (2), U = Ub + JU (1), E = Eb + (JU >> 7) (2), the omega side (17), the carry word IX with its marker (18) and the reset of the cache flag (1): 41 each, U_LB = 4 + 4 * 41 = 168 per live block. Each lane site runs the opened-cluster code of 9.9, J, L and M without the gate test, the state test and the tests of H, I and K: U_LIVE = 115; the broadcasts are Ub plus the BO word of its site, at the list address plus an immediate (address, load, addition), and Eb plus BO >> 7 (shift, addition): 5. A representative E lane costs U_E + 2 = 12 (the cache flag is tested and branched on in place of the not-ready chain of 9.8, so a batch has 7 lane sites, not 28) and the first fill of a batch 56 + 1 = 57 (the flag is set). Every outer step of a block that is neither dead nor straddling is that of an opened cluster (Lemma NA), a closed cluster whose members all have T2 = 0 (Lemma CL) or a member left out by Lemma XF.
*Code, registers and memory.* Two block copies of 26 lane sites and the straddling batch of 7 make 59 sites over the two copies of C (at most 30 each, so a return tree of five comparisons, U_RET = 14 as before). The gate words t, g, c and AW and the register HM are gone (5); Ub, Eb, the list address and the cache flag take their places (4), the block pointer replaces the list address p of the old loop, and the eight scalar context words of the block test and class are reloaded at each block (charged above), so the register count of 9.8, H and I does not rise. Memory: the member lists (201,290 words), HE, HE3, HR and HS (20,480 words) are not built; HW and HM (131,072 words), the block records (2,048 words with padding), the lists and class words of a context (below 256 words) and the code change (the old loop body and last batch, 19,456 instructions, out; two block copies of 26 sites, the straddling batch and the block tests, below 31,232, in) give a search phase below 34,803,616 - 6,441,280 - 655,360 + 4,194,304 + 65,536 + 8,192 + 376,832 = 32,351,840 bytes.

*Budgets.* Z(C) is now, for a context C, the sum over its 256 blocks of X_beta: U_BT; for a block that is not dead, U_CMB and U_BSL [p8 = A[8..15]]; for one that also does not straddle, U_LB and, for each of its 26 opened clusters, U_LIVE + U_BN [n_B > 0] + U_BL n_B, 3 + 9 [Y9 mod 4 = 0] + 10 [T1[Y9] != 0] for each survivor walked in chunk A or B, and 12 when the representative has T2 != 0, and 57 for each of its four batches with such a representative. 0 <= X_beta <= Z_BLK = 41 + 10 + 8 + 168 + 26 * (115 + 23 + 28 + 9 * 22 + 12) + 4 * 57 = 10,231, so 0 <= Z(C) <= Z_MAX = 256 Z_BLK = 2,619,136; Z_BUDGET = L_Z RUN_CONTEXTS + Z_MAX s and Z_MAX enters W_CTX. The Z(C) are independent over contexts (Lemma CX), so Hoeffding's inequality bounds an overflow by exp(-2 s^2 / RUN_CONTEXTS) <= exp(-20). The straddling clusters keep FB_BUDGET (Lemma OR) at U_SC. A_BUDGET (no unit outside Z is paid per opened cluster) and NP_BUDGET are retired with their tails; five tails remain (Z, passes, calls, straddling clusters and the credit), 5 exp(-20) < 2 * 10^-8, and the success bound of B2 holds under H1', H4', H5_exec and H_LZ.

**Premise H_LZ (v12; supporting).** For a context with uniform outer words, E[Z(C)] <= L_Z = 791,586.
Evidence (participant, untrusted), under a protocol fixed before the run (SHA-256 11372db30633f9998156560b8d91b443194dd3fc41206e9dd660a1fb956e484f): 2^25 i.i.d. (context, block) samples, sample k taking the 32 bytes of SHAKE256("hashsmash-blake3-r2-HLZ-v12" || le64(k)) as the seven outer words and, from the top byte of word 7, the block, with X_beta as above, survivors and n_B from the members' own omega (Lemma XF (c)) and T1, T2 from the byte automata, so E[Z(C)] = 256 E[X_beta]. Sum X = 103,651,156,445, sum X^2 = 568,149,382,994,449, mean 3,089.045180, unbiased variance 7,389,971.171; the empirical Bernstein bound (Maurer and Pontil 2009, Theorem 4) for X in [0, 10,231] at delta = 10^-9 is 3,092.131806, and 256 times it, rounded up, is L_Z. Per context: 112.8 dead blocks, 143.2 blocks walked, 3,723.8 opened clusters, 30,662.5 survivors, 7,665.9 with Y9 mod 4 = 0, 848.8 with a nonzero mask of (1), 891.8 representatives with T2 != 0 and 153.0 representative fills. The sampler is participant C code, not in the package (SHA-256 of its source b8033415...6113); before the run it gave the same X_beta as the declared program, driven with the same words, on 1,000 of 1,000 samples of another tag, and after it on 10,000 of 10,000 samples of this tag. Earlier protocols: v10 (SHA-256 87ea9e36...7634) measured the design with the tests of H, I and K kept inside the walked blocks (L_Z 808,644); its counts showed those tests idle (99.93 per cent of opened clusters live), which is why N drops them; v11 (SHA-256 360bf801...4122, L_Z 784,554) measured the present design with unit constants that an advisory review then found short (address additions, the per-block addition to W, reloads of the block-test constants, the broadcasts); v12 differs from v11 in those constants only. v10 and v11 are reported and not used. Not a proof: one generator, i.i.d. blocks in place of whole contexts (the mean of a sum).

*Checks.* One organizer trial is now one context and one block (the top byte of word 7 of the trial's context stream picks it). `frontline.py` runs the block test, recomputes the omega of every member of a dead block from step CO and checks that it lies in the window of Lemma NB (delta in {-1, 0} where H* = HM) and that T2 (bit-serially at every ninth member) is 0, and of every 31st member of a walked block the window; compares OL with the gate values of the 64 representatives; checks U and E of each batch against the packed members and each broadcast against Ub + BO; and walks the opened clusters as before (every member recomputed straight-line, every left-out partner bit by bit). On the organizer request of 256 trials with our own seeds: 0 mismatches and 0 skipped passes in 411,706 checks; `--selftest` returns ok, with item NA (1,536 of 1,536 blocks), the halt drills and gate drills in which the dead-block test is disabled (an opened list of all 64, the closed members bit by bit) with the same E lanes and passes. A participant scan found four straddling blocks in 72 contexts; the program walked the two that are not dead (64 clusters, 2,048 members each) with 0 mismatches. Effect of N: -0.36156 in time_log2.

## Revised exact ledger

The formulas of 9.1 and Section 11 with the unit costs of A, C, D, E, F, G, J, L, M and N and the constants of B, E, F and N; Section 18 lists the program that recomputes them. RUN_STEPS_MIN = ceil(0.49436 * 2^128 / (FACTOR (2^21 - 1))) = 590,931,867,153,450,501,380; RUN_CONTEXTS = 1,127,113,088,900,472 (2^50.0016); RUN_STEPS = 590,931,867,153,450,663,936; s = 106,165,583. PASS_BUDGET = 586,042,493,902,474,223, FB_BUDGET = 2,536,018,039,220,686, Z_BUDGET = 791,586 RUN_CONTEXTS + 2,619,136 s = 892,207,219,652,469,424,880, m_C = ceil(RUN_STEPS u_U) = 136,707,627,336,736,912,199 with the u_U of F, CREDIT = 136,712,143,855,319,043,944, CALL_BUDGET = 542,546,246,010,770,826. Units: context U_CONTEXT = 509 + 160 + 12,800 + 16 + 3 + 64 + 83 + 2,688 + 2 = 16,325 (the itemization of Section 11 without the carry words and slow paths of the 2,341 representative batches, with the plain test of H, the last flush of J, N0 and the choice of the block copy); in Z the block test 31 or 41, the class 10 and 8, the live block 168, an opened cluster 115, chunk B 23 and 14 per lane, lane 3 and 9 more when Y9 mod 4 = 0, a read of (2) after (1) 10, a representative E lane 12 and a representative fill 57; a straddling cluster 990, a passing lane 43, a call 6. WB = 43 PASS_BUDGET + 6 CALL_BUDGET + 990 FB_BUDGET + Z_BUDGET = 923,172,982,225,168,920,565 and W_CTX = 49 * 2^19 + 990 * 128 + 2,619,136 = 28,435,968.

N = contexts 16,325 (RUN_CONTEXTS + 1) + WB + W_CTX + CREDIT + ONCE 1,125,918,444,093,480 (with 2^21 for HW, HM and the block records) + S_old 5,486,510,246,044,225,536 + 430 * 2^38 = 1,083,773,001,618,804,927,138 machine units. In integers 430^100000 * 2^6112835 <= N^100000 < 430^100000 * 2^6112836, so time_log2 = 61.12836 (log2(N / 430) = 61.1283598). Five tails, each at most exp(-20) (N).

## Memory, scalar and validation

Memory is unchanged: the historical advice construction, 37,928,960 bytes (37,928,960^100000 < 2^2517680), stays the peak, so memory_log2_bytes = 25.17680; the search phase is below 32,351,840 bytes (N) and the output phase below 136,256. preprocessing_log2 54, advice 2^7 bytes and success 0.39 are unchanged. The projected scalar is 61.12836 + 5.17680 = 66.30516, against 67.80014 promoted and 66.66672 for 53570f13, a conditional claim and not an official score. `experiments/frontline.py` differs from that of 53570f13 in the block walk of N (block records, HW and HM, the opened lists, the block test, class and straddling path, the block copies, the cache flag of a representative batch, U_LIVE 115, U_BCAST 5, U_SC, L_Z, Z_BLK, Z_BUDGET, U_CONTEXT, WB, W_CTX, N, its asserted integers, the trial of one context and one block and the self-test item NA), and it no longer holds HE3, HR, HS, the gate words, j*, om', A_BUDGET, NP_BUDGET or E_BUDGET. Run locally with the organizer's request format on 256 trials of our own seeds (the participant has no Docker image here; the organizer runs the pinned one), it returns 0 mismatches and 0 skipped passes, and `--selftest` returns ok, including the W, C, R and WB halt drills and the gate drills. H1', H4', H5_exec (measured, F) and H_LZ (measured, N) remain heuristic, and the success bound 0.39 of B2 holds under these four; no full attack has run.

---

# Inherited historical baseline dossier

Source: reviewed submission 3b9c6ced-7ada-4564-969b-98d8753daed5, commit 47a7289622138f64d0dc038ff190f2629808613e. This reviewed result is distinct from promoted submission 40087647-1a84-4a2b-bb18-5b8edf0edefa / source 55dfae1cfb429015a293db48c7c9f88f566641e2. All baseline numerical outputs below retain their original meaning and are superseded only for the changed path and resource totals explicitly specified above.

# A last-chunk half-collision and a chunk-counter search for 2-round BLAKE3

The scalar below is `time_log2` under `collision-frontier-v5`. Memory is a separately reported resource bound.
This exploratory package targets blake3-r2-prefix-v1. It has an exact part and a heuristic part, and it keeps them apart. It is the counter search of our entry 415e792c on the whole class of eta with the outcome set S of six outcomes of beta*, 175020a0, 185020a0, 275020a0, 285020a0, 385020a0 and 685020a0, with the exact filter and the s-pattern pre-check of that entry, and with nine changes: (1) *the member loop and the direct tables*, after entry e9b6649e of hecmas: one fresh word per *context*, the 39 context lines run once, all 2^19 members walked, the masks of the filter read from direct tables over all 2^32 words (9.8); (2) *the guards (G7) and (G15) and a root certificate of four one-word tests* (G7 of our entry 0bc5f130): with the global ledger of 614 machine units the proved cap of the solver's work is 15,012 machine units (9.7, Section 11); (3) *the omega-first batch*: a batch of seven members computes only the lines that lead to omega, folded into 17 machine units, and the Y9 lines run only for a batch with a lane whose test on omega passes: 72 machine units per partner batch, 90,917 per context, 43 per passing lane (9.8); (4) *the straddle cluster gate*: the 32 members that differ only in bits 10 to 14 of e1 form a cluster, and a gate value computed per representative with no table skips it when no member can pass test (2) (Lemmas A9 and CL; GPT Luna 5.6, gate logic); Lemma OR proves that on average the gate opens on at most 0.40633153915... of the clusters, so the budget of opened clusters needs no premise (9.9); (5) *the masked partner walk*: a table of 64 descriptors per context lists, in at most two chunks of seven, the partners whose omega survives test (2) on its low 16 bits, the others are proved to fail, and the clusters that straddle take the earlier walk of five partner batches (Lemma XF); each lane reads the one copy of R1, L1, R2 and L2 after a shift of its address word to lane 0; a representative batch of seven costs 52 machine units and an opened cluster 168, its two chunks and its entry and return priced together (9.9, Section 11); (6) *the cached Y9*: the packed Y9 lines of a batch run once, at its first lane whose test on omega passes: 56 machine units per such batch, the *fill*, and 10 per lane that passes, the *E lane*, with a budget on the fills (9.8); (7) *the metered credit*: the credit of the solver is debited, block by block, with exactly the work that a call executes, after a test that the remaining credit covers the whole cap of the call, at most 15,012; it is set by the exact bound of GPT-6 Astra on the mean of the solver's ledger (9.7, 10.3, Section 11); (8) *one work register and the layout of this row*: the six counted events add their charges to one register W, tested once per context against a fixed bound WB (9.1); the frame words stay in registers (entry 73d5265f of 0xshikhar); a passing lane computes its rotations on scalar words; T1 and T2 sit at fixed word addresses; the representative batches run in a loop whose body, with the entry into one copy of the code of an opened cluster, is written out (9.6 to 9.9, Section 11); (9) *memory*: T2 and T1 are held in two small levels whose second levels have one row per class of states that give the same masks, 4 and 35 (Lemmas DT and T26), in one copy read after a shift, the gate, the rotations and the broadcasts need no table, the code of an opened cluster is written once, and the final step writes the two messages a chunk at a time and holds neither, so the search phase holds fewer than 31,945,408 bytes, the three transition arrays being packed eight entries to a word, and the historical construction phase is the peak, held below 37,928,960 < 2^25.17680 bytes (Section 12).
The exact filter (Section 8) skips every outer step that cannot hold a success with an outcome of S, and the joint solver (9.4) finds the successes of a passing outer step without enumerating its trials. The heuristics are H1', H4', H5_exec and H_G_cluster, stated for the walk by contexts; part (ii) of H1' takes the context as the unit, a stronger clause than one stated per outer step (10.3). The values that the search reads are a fixed record of nonuniform advice, stated in full (Section 12): the success analysis uses only properties of this record that this text verifies exactly. The record is declared directly as 73 bytes of nonuniform advice; the historical selection procedure that found it is provenance and is not part of the claimed algorithm. The layout of the solver, its cap, the guards (G7) and (G15), the root certificate, the pre-check, the cluster gate, the masked partner walk, the cache and the meter are proved allowances, charged in machine units; the declared experiment
`frontline-search` executes this search in the organizer's sandbox, one context per trial with 32 of its clusters, the work
register, the cache and the metered credit of this row included, and checks it in the same run against a straight-line recomputation (9.2). Section 15 lists the earlier entries in one line each, and Section 16 credits the people and models whose work is used.
**Exact part.** An explicit construction maps seven 32-bit words, a member y of the class of eta, a set of 524,288 values, and one more word c1 to a number t and to a 55-byte string A and a 63-byte string B. When t is not zero, F || A and F || B, with F a string of t full chunks of 1,024 bytes, are messages of 1024 t + 55 and 1024 t + 63 bytes whose last chunks are A and B, and the 2-round compressions of these last chunks, with chunk counter t and flags 3, give chaining values that agree on their words 0, 2, 5 and 7, that is on 128 of their 256 bits. There is no search in this and no probability: it holds for every choice (Sections 7 and 8). In the organizer's tree mode the digest of such a message depends on F and on the chaining value of its last chunk alone (Lemma TR), so a pair whose last-chunk chaining values agree in all eight words is a collision of two complete messages. The number t is not chosen: it is the chunk counter that the round-0 call K0 reads, solved per trial as t = ROL(K0.d1,16) XOR K0.a1.
It takes up the freedom of the message word w0, and that is what lets the construction prescribe c1, the third value of the round-1 call E1, next to y. The search holds c1 inside the set Q* of the 2^21 words for which the first-half b difference of E1 is beta* = 18b0e098, the difference of the solution with which the constants were found (Section 12).
**Heuristic part.** A collision needs the other four words of the chaining value to agree as well. The algorithm walks 598,932,067,520,076,054,528 = 2^69.021 outer steps of 2^21 trials each: 1,142,372,260,131,981 = 2^50.021 contexts drawn at random, each with all 2^19 members of the class in 16,384 clusters of 32, seven members to a batch. An exact filter, two carry automata on two words of the outer step, skips every outer step that cannot hold a collision with an outcome of S (Lemma F); it passes 2^-9.9782 of uniform pairs of words. A gate computed once per cluster skips the clusters in which no member can pass the second automaton, exactly and without loss (Lemma CL); in the other clusters a table of the context skips the partners that provably fail it (Lemma XF), and the second automaton, read from a table in two levels at omega, is tested in every other lane; the member lines that lead only to Y9, and the first automaton, run only in a lane whose omega passes the second, 2^-4.1998 of uniform words. In a passing outer step three bits of E1.b1 that every success shares are a function of the words of the outer step, and they allow an outcome of S for only two of their eight values: the pre-check skips the joint solver in the other passing outer steps, exactly and without loss (Lemma VP). The joint solver, one depth-first traversal over the bits of one internal word with guards that exact counts of the class prove lossless and with the guards (G7) and (G15) (Lemmas G7 and G15), returns every value of that word that meets the conditions of an outcome of S, and a certificate of four one-word tests decides for each whether its trial completes the collision (Lemma RC). Together they find exactly the trials of the outer step that complete the collision with an outcome of S, at a cost of at most 15,127 machine units for a passing outer step whatever its words: 10 for its E lane, 56 for the fill of its batch, 43 and 6 for its lane and 15,012 for steps 2 and 3 with the meter (Sections 9 and 11; Lemmas V, RC, VP, G7, G15, CV, FX, ME). The six budgets, through one work register, and the credit of the solver are halts, charged at their bounds, so the time bound contains no mean of a count. Four heuristics are declared for the success, each for the instance that the stated advice record of Section 12 fixes and each stated in full in 10.3. H1': the valid trials (t not zero) complete the collision with an outcome of S at a rate no lower than 134,357,314,437 * 2^-128 = 2^-91.126, 97/100, rounded down, of the model's rate for this prescription and these outcomes, and the listed good trials of one context are not clustered beyond a stated bound. H4': a lane whose omega passes the second automaton and a passing outer step occur with probability at most 1.000026 and 1.000176 times their exact shares. H5_exec: averaged over the outer steps, the ledger U of the work that steps 2 and 3 execute for the outcomes kept by the pre-check is at most 1.01 times 335,060,079,487,497 / 2^48 = 1.1904, its mean in model M. H_G_cluster: a context has on average at most 7,198 fills of the masked walk. Each budget and the credit add to these means a reserve over the independent contexts that Hoeffding's or Bernstein's inequality proves sufficient (10.3). The budgets of opened clusters and of straddling clusters need no premise: Lemma OR proves
that on average the gate opens on at most 0.40633153915... of the clusters of a context and that at most 9/4 of them straddle (9.9). Under these four the search succeeds with probability at least 0.39. The search rows, streamed final step and conservative charge for the historical construction of the advice total 3,059,650,683,180,925,199,092 machine units, or 2^62.6256640945... target-compression units, so time_log2 = 62.62567. The search holds fewer than 31,945,408 bytes, its tables and its code included. Once a root is certified, the program
releases the search's words before the final step, so the final step and the search are never held together; the final step hashes the two messages and then writes them to its output a chunk at a time, producing the t zero chunks of F from one chunk of zero bytes, and holds neither message. The output phase holds fewer than 136,256 bytes. The historical construction phase is bounded by 37,928,960 bytes, so memory_log2_bytes = 25.17680 (Section 12).
The rate in H1' is an assumption. Under the seven-word model of Section 13, with Y4 uniform in the class, prescribing c1 in Q* multiplies by 2^11 the part of beta* in the rate of the class: counting the six outcomes of S, the rate is 2^11 * 67,633,152 = 138,512,695,296 times 2^-128, which is 853.61 times the model rate of a trial of the class (Lemma S1, proved by another AI model, GPT Sol 6.1). The figure 67,633,152 is the sum of six exact outcome counts of the participant's counting program, printed with its output in Section 17. Whether the trials of the construction realise that conditional law, to at least 97/100 of its rate, is not proved, and it is declared as H1'; Lemmas S2 to S4 prove parts of it, and Lemma S8 states how weak the dependence has to be. On real counter trials the participant's measurements agree with the model for events down to about 2^-31.7 per trial, and in a preregistered scaled-down end-to-end run with 40,882 real collisions of complete messages the counter arrangement realises 1.00199 +- 0.00496 of the predicted count, with a one-sided 97.7 per cent lower bound of 0.99213, above 10/11 (Section 13). No run reaches a collision at 32 bits.
Part (ii) of H1', the dependence, is stated with the context as the unit, as entry e9b6649e states it: the 2^19 outer steps of a context share their seven outer words, and only the contexts are independent. It is an assumption, which cannot be measured at full size; it fails only if listed good trials cluster by context about 2^44 times more than independent members would, while the events that every listed good trial meets cluster by a factor between 1.14 and 1.25 at every depth measured, and the two halves of a listed good trial show no clustering across members in a preregistered run (10.3, Section 13).
No full 2-round collision is exhibited, and the search is far beyond feasible computation. The declared experiment executes the search of 9.1 on organizer seeds, one context per trial, and returns for each trial the root-instance pair of the same construction, single chunks of 55 and 63 bytes compressed with counter 0 and flags 11, whose half-collision the organizer's runner checks on the digests; no digest experiment can show the half-collision of the counter instance, whose colliding chunk is not the root (6.4). Its observations, the program's own counts, are untrusted (9.2).

## 1. Exact complete hash on the messages used

H is unkeyed BLAKE3-256 with only rounds 0 and 1 kept in every compression. Every message of the root instance (Sections 4 to 6) has n = 55 or n = 63 bytes. A message of n <= 64 bytes is one chunk consisting of one block, with no parent node, so H evaluates exactly one compression. The block is the message followed by 64 - n zero bytes, used only for loading words. The compression has flags CHUNK_START | CHUNK_END | ROOT = 11, true block length n, and chunk counter and root-output counter both zero. There is no key and no derivation flag.
Decode the zero-filled block into sixteen little-endian 32-bit words w[0..15]. The IV is
    6a09e667 bb67ae85 3c6ef372 a54ff53a
    510e527f 9b05688c 1f83d9ab 5be0cd19.
Initialize v[0..7] = IV, v[8..11] = IV[0..3] and v[12..15] = (0, 0, n, 11). The block length n is the initial value of v[14] and enters nowhere else. All additions and subtractions on state and message words are modulo 2^32. ROR and ROL rotate a 32-bit word.
G(a,b,c,d,x,y) is
    v[a] = v[a]+v[b]+x;  v[d] = ROR(v[d] XOR v[a],16)
    v[c] = v[c]+v[d];    v[b] = ROR(v[b] XOR v[c],12)
    v[a] = v[a]+v[b]+y;  v[d] = ROR(v[d] XOR v[a],8)
    v[c] = v[c]+v[d];    v[b] = ROR(v[b] XOR v[c],7).
A round is four column calls followed by four diagonal calls on the current schedule s, and between rounds s is replaced by s[P[i]] with P = (2,6,3,10,7,0,4,13,1,11,12,5,9,14,15,8). Written out for the two retained rounds, with names used throughout:
    round 0   K0 = G(0,4,8,12, w0, w1)     K1 = G(1,5,9,13, w2, w3)
              K2 = G(2,6,10,14, w4, w5)    K3 = G(3,7,11,15, w6, w7)
              D0 = G(0,5,10,15, w8, w9)    D1 = G(1,6,11,12, w10, w11)
              D2 = G(2,7,8,13, w12, w13)   D3 = G(3,4,9,14, w14, w15)
    round 1   C0 = G(0,4,8,12, w2, w6)     C1 = G(1,5,9,13, w3, w10)
              C2 = G(2,6,10,14, w7, w0)    C3 = G(3,7,11,15, w4, w13)
              E0 = G(0,5,10,15, w1, w11)   E1 = G(1,6,11,12, w12, w5)
              E2 = G(2,7,8,13, w9, w14)    E3 = G(3,4,9,14, w15, w8)
S denotes the state after K0..K3, X the state after round 0, Y the state after C0..C3 and Z the final state. The compression output is o[i] = Z[i] XOR Z[i+8] and o[i+8] = Z[i+8] XOR IV[i] for i = 0..7. The digest H(m) is the first 32 output bytes, LE4(o[0]) || ... || LE4(o[7]).
This is the complete hash of the target profile restricted to inputs of 55 and 63 bytes: standard IV, standard flags, true block length, both retained rounds with the standard permutation, standard feed-forward and the full 256-bit digest. It is not a free-start, chosen-IV, compression-only or truncated-output setting.
*The same compression in a last chunk.* Sections 7 to 9 use the same compression, with the same names, as the compression of the last chunk of a longer message: there v[12..15] = (t mod 2^32, t >> 32, n, 3), with the chunk counter t and the flags CHUNK_START | CHUNK_END = 3, and the output words o[0], .., o[7] are the chaining value of the chunk (Lemma TR). Nothing else changes: the IV, the block, the two rounds and the output.

## 2. Inverting one G call

Consider one call G(a,b,c,d,x,y) with input values A, B, C, D and name its eight assignments
    a1 = A + B + x           d1 = ROR(D XOR a1, 16)
    c1 = C + d1              b1 = ROR(B XOR c1, 12)
    a2 = a1 + b1 + y         d2 = ROR(d1 XOR a2, 8)
    c2 = c1 + d2             b2 = ROR(b1 XOR c2, 7).
Its outputs are (a2, b2, c2, d2). The values a1, d1, c1, b1 are called the first, second, third and fourth value of the call, a2 the fifth, and so on.
**Fact 1.** Reading the assignments backwards,
    b1 = ROL(b2, 7) XOR c2       c1 = c2 - d2       d1 = ROL(d2, 8) XOR a2
    B  = ROL(b1, 12) XOR c1      C  = c1 - d1
    a1 = ROL(d1, 16) XOR D       y  = a2 - a1 - b1      x = a1 - A - B.
Each line is one assignment solved for another of its terms. A set of words A, B, C, D, x, y, a1, d1, c1, b1, a2, d2, c2, b2 is the execution of one call exactly when the eight assignments hold, in whatever order and for whichever of their terms they were solved. The constructions below use nothing else: every line of theirs is one assignment of one call, solved for the name on its left.

## 3. Three ingredients

**3.1 The length is cancelled inside K2.** K2 is the only call of round 0 that reads the block length n, the initial value of v[14], and it overwrites that word; it is also the only call of round 0 that reads w4 and w5. Its inputs are (IV[2], IV[6], IV[2], n). Put K = IV[2] + IV[6] = 5bf2cd1d. For lengths 55 and 63, whose XOR is 8, define for any w4, w5
    w4' = ((K + w4) XOR 8) - K        w5' = w5 + w4 - w4'.
**Lemma L.** K2 with block length 55 and words (w4, w5) leaves the same four state words as K2 with block length 63 and words (w4', w5').
Proof. Let a1 = K + w4. In the second execution the first assignment gives K + w4' = a1 XOR 8, so the second gives ROR(63 XOR a1 XOR 8, 16) = ROR(55 XOR a1, 16) because 63 XOR 8 = 55: the same d1. The third and fourth depend only on d1 and constants. The fifth gives (a1 XOR 8) + b1 + w5' = a1 + b1 + w5 because w5' - w5 = w4 - w4' = a1 - (a1 XOR 8). The last three depend only on values already shown equal. QED.
Hence two messages of 55 and 63 bytes that share every word except w4, w5, related as above, have the same state S after the column step and the same state X after round 0, since no other call of round 0 reads v[14], w4 or w5 before K2 has made the states equal.
*Which words must be zero.* For both messages to be honest byte strings of their lengths with the same words w6..w15, the bytes 55 to 63 of the block must be zero in both. In the 55-byte message they are zero fill. In the 63-byte message bytes 55 to 62 are its last eight bytes, which are chosen to be zero, and byte 63 is zero fill. Byte 55 is the top byte of w13, bytes 56 to 59 are w14 and bytes 60 to 63 are w15. So the family needs
    w14 = 0,   w15 = 0,   top byte of w13 = 0,
and nothing else: bytes 0 to 54 are free in both messages.
**3.2 A pinned call C3.** Fix the six constants
    X3 = bf1c5f38   X7 = c0e3a0c8   X11 = c4036000   X15 = c0c5fb02
    W4 = 7ffffffa   W13 = 00074004
The top byte of W13 is zero. K + W4 = f33a2355 and W4' = ((K + W4) XOR 8) - K = 97475640, so W4 - W4' = fffffff8, that is -8 modulo 2^32. Evaluate C3 = G(3,7,11,15, w4, W13) on the inputs (X3, X7, X11, X15) with w4 = W4 and with w4 = W4':
    w4 = W4    a1=7ffffff8 d1=7af83f3a c1=befb9f3a b1=01200183
               a2=ff27c181 d2=bbfbdffe c2=84f77f38 b2=76f7aefd
    w4 = W4'   a1=80000000 d1=8500c0c5 c1=c90420c5 b1=fed77e78
               a2=7edf3e7e d2=bbfbdffe c2=850000c3 b2=76f7aefd
**Fact P.** The two executions give the same d output bbfbdffe and the same b output 76f7aefd. They differ in the a output (ff27c181, 7edf3e7e) and in the c output (84f77f38, 850000c3). This is a finite computation on the displayed constants.
**3.3 Half of the digest does not see the difference.**
**Lemma H.** Take two executions of the 2-round compression that have the same state X after round 0 and the same message words except w4 and w5. Suppose (X[3], X[7], X[11], X[15]) = (X3, X7, X11, X15), w13 = W13, and w4 is W4 in the first execution and W4' in the second. Then the two digests agree on digest words 0, 2, 5 and 7.
Proof. C0, C1, C2 read neither w4 nor w5 and act on identical states, so they leave identical values in both executions. C3 reads state words 3, 7, 11, 15 and the words w4, w13; by Fact P it leaves the same v[7] and v[15] in both executions and may differ only in v[3] and v[11]. So Y agrees except possibly in Y[3] and Y[11]. E0 reads Y[0], Y[5], Y[10], Y[15] and w1, w11. E2 reads Y[2], Y[7], Y[8], Y[13] and w9, w14. None of these is Y[3], Y[11], w4 or w5, so E0 and E2 produce identical outputs Z[0], Z[5], Z[10], Z[15] and Z[2], Z[7], Z[8], Z[13]. Finally o[0] = Z[0] XOR Z[8], o[2] = Z[2] XOR Z[10], o[5] = Z[5] XOR Z[13] and o[7] = Z[7] XOR Z[15] use only those eight words. QED.
The remaining digest words o[1] = Z[1] XOR Z[9], o[3] = Z[3] XOR Z[11], o[4] = Z[4] XOR Z[12] and o[6] = Z[6] XOR Z[14] are computed from the outputs of E1 and E3 only. The **residual** of a pair is the 128-bit string R = (o[1] XOR o'[1], o[3] XOR o'[3], o[4] XOR o'[4], o[6] XOR o'[6]). The pair is a collision exactly when R = 0.

## 4. Construction: the message from eight words, in three levels

This section, Section 5 and Section 6 build the root instance of the construction, whose messages are single chunks compressed with counter 0 and flags 11 (Section 1). The counter instance, which the claim uses, is built in Section 8 from the same constants (6.4).
The construction places the six constants of 3.2 where Lemma H needs them and gives Y4, the b output of C0, a prescribed value y.
Its input is eight free words. Six form an *outer step*: C0.c1 and C0.d1 (the third and the second value of the round-1 call C0), D3.d1 (the second value of the round-0 call D3), S15 and S9 (words of the state S) and the message word w5. The seventh is X2, a word of the state X; with it the six are a *context*. The eighth is y. X3, X7, X11, X15 are the constants, w4 = W4, w13 = W13 and w14 = w15 = 0.
*Names.* TAG.a1, TAG.d1, TAG.c1, TAG.b1 are the first to fourth value of the call TAG (Section 2); its outputs carry the names of the state S, X or Y they are written to. Arithmetic is modulo 2^32.
**Step O (the outer step; 29 lines).**
    K2, forwards from w5; its first four values are constants:
        K2.a1 = IV[2] + IV[6] + W4;   K2.d1 = ROR(55 XOR K2.a1, 16)
        K2.c1 = IV[2] + K2.d1;   K2.b1 = ROR(IV[6] XOR K2.c1, 12)
        S2 = K2.a1 + K2.b1 + w5;   S14 = ROR(K2.d1 XOR S2, 8)
        S10 = K2.c1 + S14;   S6 = ROR(K2.b1 XOR S10, 7)
    D3 with w14 = w15 = 0, from D3.d1, its inputs S9, S14, its output X3:
        D3.a1 = ROL(D3.d1,16) XOR S14;   D3.c1 = S9 + D3.d1
        D3.b1 = X3 - D3.a1;   S4 = ROL(D3.b1,12) XOR D3.c1
        S3 = D3.a1 - S4;   X14 = ROR(D3.d1 XOR X3, 8)
        X9 = D3.c1 + X14;   X4 = ROR(D3.b1 XOR X9, 7)
    K3, backwards from its outputs S3, S15:
        K3.d1 = ROL(S15,8) XOR S3;   K3.c1 = IV[3] + K3.d1
        K3.b1 = ROR(IV[7] XOR K3.c1, 12);   S11 = K3.c1 + S15
        S7 = ROR(K3.b1 XOR S11, 7);   K3.a1 = ROL(K3.d1,16) XOR 11
        w6 = K3.a1 - IV[3] - IV[7];   w7 = S3 - K3.a1 - K3.b1
    C0, third assignment and fourth value; D2, backwards from X7, X8, S7:
        X8 = C0.c1 - C0.d1;   C0.b1 = ROR(X4 XOR C0.c1, 12)
        D2.b1 = ROL(X7,7) XOR X8;   D2.c1 = ROL(D2.b1,12) XOR S7
        X13 = X8 - D2.c1
**Step M (the middle step; 21 lines, from X2).**
    D2, rest:
        D2.a1 = X2 - D2.b1 - W13;   D2.d1 = ROL(X13,8) XOR X2
        S13 = ROL(D2.d1,16) XOR D2.a1;   S8 = D2.c1 - D2.d1
        w12 = D2.a1 - S2 - S7
    K1, backwards from its outputs S9, S13:
        K1.c1 = S9 - S13;   K1.d1 = K1.c1 - IV[1]
        K1.a1 = ROL(K1.d1,16);   K1.b1 = ROR(IV[5] XOR K1.c1, 12)
        S1 = ROL(S13,8) XOR K1.d1;   S5 = ROR(K1.b1 XOR S9, 7)
        w2 = K1.a1 - IV[1] - IV[5];   w3 = S1 - K1.a1 - K1.b1
    K0, backwards from its outputs S4, S8:
        K0.b1 = ROL(S4,7) XOR S8;   K0.c1 = ROL(K0.b1,12) XOR IV[4]
        K0.d1 = K0.c1 - IV[0];   K0.a1 = ROL(K0.d1,16)
        S12 = S8 - K0.c1;   S0 = ROL(S12,8) XOR K0.d1
        w0 = K0.a1 - IV[0] - IV[4];   w1 = S0 - K0.a1 - K0.b1
**Step Y (the member; 10 lines, from y and the outer step, without X2).**
    C0, backwards from its b output y:
        Y8 = ROL(y,7) XOR C0.b1;   Y12 = Y8 - C0.c1
        Y0 = ROL(Y12,8) XOR C0.d1;   C0.a1 = Y0 - C0.b1 - w6
        X12 = ROL(C0.d1,16) XOR C0.a1
    D1, backwards from its outputs X11, X12, with its inputs S6, S11:
        D1.c1 = X11 - X12;   D1.b1 = ROR(S6 XOR D1.c1, 12)
        X6 = ROR(D1.b1 XOR X11, 7);   D1.d1 = D1.c1 - S11
        X1 = ROL(X12,8) XOR D1.d1
**Step T (the four words w8..w11; 12 lines).**
    C0, its first assignment:
        X0 = C0.a1 - X4 - w2
    D0, backwards from its outputs X0, X15:
        D0.d1 = ROL(X15,8) XOR X0;   D0.c1 = S10 + D0.d1
        X10 = D0.c1 + X15;   D0.b1 = ROR(S5 XOR D0.c1, 12)
        X5 = ROR(D0.b1 XOR X10, 7);   D0.a1 = ROL(D0.d1,16) XOR S15
        w8 = D0.a1 - S0 - S5;   w9 = X0 - D0.a1 - D0.b1
    D1, rest:
        D1.a1 = ROL(D1.d1,16) XOR S12;   w10 = D1.a1 - S1 - S6
        w11 = X1 - D1.a1 - D1.b1
**Step S2.** w4' = W4' and w5' = w5 + W4 - W4', all modulo 2^32. For the constants of 3.2 that is w5' = w5 + fffffff8, the same as w5 - 8.
**Step S3.** A is the first 55 bytes of the little-endian encoding of w0..w15; B is the first 63 bytes of that of the same words with w4', w5' for w4, w5.
*Round 1, forwards (24 lines).* The tests of 6.3 read these values of round 1 of message A. Y3 and Y11 are the constants of Fact P for w4 = W4, and Y4 = y.
    C1, the call G(X1, X5, X9, X13; w3, w10):
        C1.a1 = X1 + X5 + w3;   C1.d1 = ROR(X13 XOR C1.a1, 16)
        C1.c1 = X9 + C1.d1;   C1.b1 = ROR(X5 XOR C1.c1, 12)
        Y1 = C1.a1 + C1.b1 + w10;   Y13 = ROR(C1.d1 XOR Y1, 8)
        Y9 = C1.c1 + Y13;   Y5 = ROR(C1.b1 XOR Y9, 7)
    C2, the call G(X2, X6, X10, X14; w7, w0):
        C2.a1 = X2 + X6 + w7;   C2.d1 = ROR(X14 XOR C2.a1, 16)
        C2.c1 = X10 + C2.d1;   C2.b1 = ROR(X6 XOR C2.c1, 12)
        Y2 = C2.a1 + C2.b1 + w0;   Y14 = ROR(C2.d1 XOR Y2, 8)
        Y10 = C2.c1 + Y14;   Y6 = ROR(C2.b1 XOR Y10, 7)
    E1 on A, with its c input Y11; third and fourth assignment in one line:
        E1.a1 = Y1 + Y6 + w12;   E1.d1 = ROR(Y12 XOR E1.a1, 16)
        E1.b1 = ROR(Y6 XOR (Y11 + E1.d1), 12);   E1.a2 = E1.a1 + E1.b1 + w5
    E3 on A, with its a input Y3 and w15 = 0; first and second in one line:
        E3.h1 = ROR(Y14 XOR (Y3 + Y4), 16);   E3.g1 = Y9 + E3.h1
        E3.f1 = ROR(Y4 XOR E3.g1, 12);   E3.e2 = (Y3 + Y4) + E3.f1 + w8
These 24 lines define nothing of the message. E3.h1, E3.g1, E3.f1, E3.e2 are the h1, g1, f1, e2 of 6.2.
**The order and the levels.** The 29 + 21 + 10 + 12 + 24 = 96 lines above are taken in the printed order. Lines of step O are
*outer*, of step M *middle*, of step Y *table* lines; the 12 lines of step T and the 24 of round 1 are the 36 *trial* lines. Table C gives each call's eight assignments by their left sides.

| Call | 1st | 2nd | 3rd | 4th | 5th | 6th | 7th | 8th |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| K0 | w0 | K0.a1 | K0.d1 | K0.c1 | w1 | S0 | S12 | K0.b1 |
| K1 | w2 | K1.a1 | K1.d1 | K1.b1 | w3 | S1 | K1.c1 | S5 |
| K2 | K2.a1 | K2.d1 | K2.c1 | K2.b1 | S2 | S14 | S10 | S6 |
| K3 | w6 | K3.a1 | K3.c1 | K3.b1 | w7 | K3.d1 | S11 | S7 |
| D0 | w8 | D0.a1 | D0.c1 | D0.b1 | w9 | D0.d1 | X10 | X5 |
| D1 | w10 | D1.a1 | D1.d1 | D1.b1 | w11 | X1 | D1.c1 | X6 |
| D2 | w12 | S13 | S8 | D2.c1 | D2.a1 | D2.d1 | X13 | D2.b1 |
| D3 | S3 | D3.a1 | D3.c1 | S4 | D3.b1 | X14 | X9 | X4 |
| C0 | X0 | X12 | X8 | C0.b1 | C0.a1 | Y0 | Y12 | Y8 |
| C1 | C1.a1 | C1.d1 | C1.c1 | C1.b1 | Y1 | Y13 | Y9 | Y5 |
| C2 | C2.a1 | C2.d1 | C2.c1 | C2.b1 | Y2 | Y14 | Y10 | Y6 |

The inputs, message words and outputs of the eleven calls are those of Section 1 for n = 55: Ki (i = 0..3) maps (IV[i], IV[i+4], IV[i], d) with d = 0, 0, 55, 11 to (S[i], S[i+4], S[i+8], S[i+12]); D0..D3 map (S0, S5, S10, S15), (S1, S6, S11, S12), (S2, S7, S8, S13), (S3, S4, S9, S14), and C0..C2 map (X0, X4, X8, X12), (X1, X5, X9, X13), (X2, X6, X10, X14), to the X and the Y words of the same indices.
**Lemma T2.** (a) *Triangular.* In the printed order every line assigns a name that no earlier line assigns and that is neither one of the eight words nor a constant, and it reads only constants, the eight words (the eighth under the name Y4 in the lines of round 1) and names of earlier lines. A line of step O reads no word other than the six of the outer step, a line of step M reads neither y nor a name of step Y, and a line of step Y reads neither X2 nor a name of step M. Every line is one assignment of one call, solved for the name on its left; the two exceptions are the lines for E1.b1 and for E3.h1, each of which is two assignments with the first substituted into the second (c1 = Y11 + E1.d1 and e1 = Y3 + Y4 + w15), and the line for E3.e2 uses the same e1. By Table C the 96 lines are, each exactly once: the eight assignments of each of the eleven calls K0..K3, D0..D3, C0..C2, with the inputs and the message words of Section 1 for block length 55, with w4 = W4, w13 = W13, w14 = w15 = 0, and with the constants X3, X7, X11, X15 as the a output of D3, the b output of D2, the c output of D1 and the d output of D0; and the first five assignments of E1 and of E3 for message A.
(b) *The calls.* For every choice of the eight words, the names of steps O, M, Y and T are the executions of the eleven calls as listed after Table C, each with its two message words; C0 has first, second, third and fourth value C0.a1, C0.d1, C0.c1, C0.b1 and outputs (Y0, y, Y8, Y12); and E1.a1, E1.d1, E1.b1, E1.a2 and E3.h1, E3.g1, E3.f1, E3.e2 are the first, second, fourth and fifth value of E1 and the second, third, fourth and fifth value of E3 in the compression of message A.
(c) *The levels.* An outer line is a function of the six words alone. A middle line is a function of the six words and X2 and does not depend on y. A table line is a function of the six words and y and does not depend on X2. In particular the sixteen message words of two trials of one context differ at most in w8, w9, w10, w11.
(d) *Admissible blocks.* Call a block (w0, .., w15) *admissible* if w4 = W4, w13 = W13, w14 = w15 = 0 and round 0 on it with block length 55 ends with (X[3], X[7], X[11], X[15]) equal to the four constants. The map of this section from the eight words to the block of A is a bijection onto the admissible blocks.
Proof. (a) is read off the displays, each formula compared with Section 2 and its call's inputs, outputs and message words; Table C has one name in each of its 88 cells, all different, and with the eight of E1 and E3 they are the 96.
(b) An assignment solved for one of its terms is an equivalent equation modulo 2^32 (Fact 1), so a line's assignment holds once it has run, and by (a) no later line changes its names. By (a) and Table C all eight assignments of each call hold, a constant output in its place (lines D3.b1, X14; D2.b1; D1.c1, X6; D0.d1, X10) and y as the b output of C0 (line Y8); by Fact 1 the names are the execution of the call. The E1 and E3 lines are those of 6.2 for message A with Y11, Y3 of Fact P, run forwards from A's Y1, Y6, Y12, Y4, Y9, Y14.
(c) By induction over the printed order, with (a): an outer line reads only constants, the six words and outer lines; a middle line in addition only X2 and middle lines; a table line in addition only y and table lines. w6, w7 are outer and w0..w3, w12 middle lines, w5 is one of the six words, w4, w13, w14, w15 are constants; only w8..w11 are trial lines.
(d) By (b), round 0 with block length 55 on an output block leaves the state X of the names, with the constants as X[3], X[7], X[11], X[15], and the pinned words are constants: the block is admissible. *Injective:* by (b) each of the eight words is a value in the compression of A, so a function of the block. *Onto:* the forward values of an admissible block (block length 55) satisfy every equation of (a): they execute the calls, the constant outputs hold by admissibility, and C3 has the inputs X3, X7, X11, X15, W4, W13, so Y3, Y11 are those of Fact P. Run on the eight words taken from them, each line returns the forward value of its name, by induction, since an assignment has exactly one solution for any one term given the others. So the lines return the block. QED.

## 5. The half-collision

**Theorem.** For every choice of the seven words of a context (C0.c1, C0.d1, D3.d1, S15, S9, w5, X2) and of the word y, steps O, M, Y, T, S2 and S3 output two distinct messages A and B, of 55 and 63 bytes, whose complete 2-round digests agree on digest words 0, 2, 5 and 7; and in both compressions the b output of C0 is Y4 = y.
Proof. The sixteen words of steps O, M, Y and T have w14 = w15 = 0 and w13 = W13, whose top byte is zero. So bytes 55 to 63 of their encoding are zero: A, the first 55 bytes, is an honest 55-byte message whose zero-filled block is the sixteen words, and B is an honest 63-byte message that ends in eight zero bytes and whose zero-filled block is the sixteen words with w4, w5 replaced (3.1). Run round 0 on the words of A with block length 55. By Lemma T2 (b) the column calls leave the state S of the names and the diagonal calls, which act on disjoint state words, leave the state X of the names. So the state after round 0 has (X[3], X[7], X[11], X[15]) equal to the four constants, and w4 = W4, w13 = W13. By Lemma L the compression of B has the same state X after round 0. The two compressions share every word except w4, w5, so Lemma H gives the four digest words. C0 reads X0, X4, X8, X12 and w2, w6, which are the same in both compressions, and has b output y by Lemma T2 (b). The messages are distinct because their lengths differ. QED.
Distinct choices of the eight words give distinct messages A: C0.c1 and C0.d1 are values inside C0, D3.d1 is a value inside D3, S15 and S9 are state words after the column step of round 0, w5 is a message word, X2 is a state word after round 0 and y is a state word after the column step of round 1, and all of them are functions of the message (Lemma T2 (d)). The construction yields 2^256 different half-colliding pairs.

## 6. The root instance: trials, tests and the packed machine

**6.1 Trials.** A *context* is the six words of an outer step (C0.c1, C0.d1, D3.d1, S15, S9, w5), a word X2, and everything that steps O and M compute from them. The class and the sub-class defined next are sets of values of Y4. A **trial** is a context and a member y of the sub-class; its messages A and B are the output of steps O, M, Y, T, S2 and S3 for the context's seven words and y.
Only steps Y and T depend on y: the trials of one context differ in the four message words w8..w11 and in nothing else of the message (Lemma T2 (c)). Step Y does not read X2: its ten names depend on the outer step and the member only.
*The class.* The first message word of E3 is w15 = 0, so the first assignment of E3 is e1 = Y3 + Y4 for message A and e1' = Y3' + Y4 for message B, with Y3 = ff27c181 and Y3' = 7edf3e7e from Fact P. Put DY3 = Y3' - Y3 = 01b77cfd. The second assignment is h1 = ROR(Y14 XOR e1, 16), so the XOR difference between A and B of E3's first-half d value is
    eta = h1 XOR h1' = ROR((Y3 + Y4) XOR (Y3 + Y4 + DY3), 16),
a function of Y4 alone. Fix eta = 830303cf. The *class* is the set of all words Y4 that give this eta.
**Lemma Q.** The class is the set of all Y4 with
    ((Y3 + Y4) AND 03cf8303) = 010c0303.
It has 524,288 members: the 19 bits of e1 = Y3 + Y4 at the positions where 03cf8303 has a zero are free, bit 31 among them, and Y4 = e1 - Y3.
Proof. Put x = ROL(eta,16) = 03cf8303, which has no bit 31. Y4 is in the class exactly when e1 XOR (e1 + DY3) = x, that is when (e1 XOR x) - e1 = DY3 modulo 2^32. For words e and x, (e XOR x) - e is, modulo 2^32, the sum over the bits i of x of 2^i where bit i of e is 0 and of -2^i where it is 1, which is 2 ((NOT e) AND x) - x. So the condition is 2 ((NOT e1) AND x) = DY3 + x = 01870000 modulo 2^32. As (NOT e1) AND x has no bit 31, the doubling is exact and the condition is ((NOT e1) AND x) = 01870000 >> 1 = 00c38000. All bits of 00c38000 lie in x, so this fixes the 13 bits of e1 on x to (e1 AND x) = (NOT 00c38000) AND x = 010c0303 and leaves the other 19 bits free. QED.
*The sub-class.* The search uses only the members of the class whose e1 = Y3 + Y4 has bit 21 and bit 26 equal to zero. With Lemma Q that is the set of all Y4 with
    ((Y3 + Y4) AND 07ef8303) = 010c0303.
**Lemma Q2.** The sub-class is a subset of the class and has 131,072 members: the 17 bits of e1 at the positions 2 to 7, 10 to 14, 20 and 27 to 31, where 07ef8303 has a zero, are free, and Y4 = e1 - Y3.
Proof. 07ef8303 = 03cf8303 OR 04200000, and 04200000 has the bits 21 and 26, which are two of the 19 positions that Lemma Q leaves free. The value 010c0303 has zeros at both. So the condition is the condition of Lemma Q together with bit 21 = bit 26 = 0, and 17 positions stay free. QED.
Member number k of the sub-class, for 0 <= k < 131072, is the Y4 whose e1 has the bits of k at its 17 free positions, in increasing order of position. From here on "member" means a member of the sub-class. A part of the class is searched and not all of it because, under the model of Section 13, the rate of collisions differs from member to member and is higher on this part.
Nothing exact depends on that.
**Lemma T.** For every context and every member y of the class, and so for every member of the sub-class, the messages A and B of the trial are distinct messages of 55 and 63 bytes whose complete 2-round digests agree on digest words 0, 2, 5 and 7; in both compressions Y4 = y; and the XOR difference between A and B of E3's first-half d value is eta = 830303cf.
Proof. The first two statements are the theorem of Section 5. In both compressions w15 = 0 and Y14 is the same, the a input of E3 is Y3 for A and Y3' for B by Fact P, and Y4 = y is a member of the class, so the difference is eta by the definition of the class.
QED.
**6.2 The residual of a trial.** With Y3, Y3', Y11, Y11' the a and c outputs of C3 from Fact P (ff27c181, 7edf3e7e, 84f77f38, 850000c3), delta = W4 - W4' = fffffff8 and the trial's words and state:
    (.., Y4, .., Y12) = C0 = G(X0, X4, X8, X12, w2, w6)
    (Y1, .., Y9, ..)  = C1 = G(X1, X5, X9, X13, w3, w10)
    (.., Y6, .., Y14) = C2 = G(X2, X6, X10, X14, w7, w0)
    E1 on A:  G(Y1, Y6, Y11,  Y12, w12, w5)
    E1 on B:  G(Y1, Y6, Y11', Y12, w12, w5 + delta)
    E3 on A:  G(Y3,  Y4, Y9, Y14, w15, w8)
    E3 on B:  G(Y3', Y4, Y9, Y14, w15, w8)
and R is formed from the eight output words of E1 and E3 as in 3.3. Y4 = y and Y12 are known from step Y without evaluating C0 forwards. Write a1, d1, c1, b1, a2, .. for the assignments of E1 and e1, h1, g1, f1, e2, h2, g2, f2 for those of E3 in the order a, d, c, b; a prime marks message B.
**6.3 Two tests of a trial.** Two tests of a trial of the root instance are used by the measurements of Section 13: rule A, a condition on one word of E3, and the E1 test, a 32-bit condition on E1 alone (Lemma N).
**Lemma N.** For a trial of 6.1 put beta = b1 XOR b1' and eps = c2 XOR c2', both taken from E1, and
    n = eps XOR ROL(beta XOR eps, 1) XOR eta.
Let D3 and D6 be the XOR differences between A and B of digest words 3 and 6, which are the second and the fourth word of R. Then n = D3 XOR ROL(D6, 8) for every trial. In particular R = 0 implies n = 0.
Proof. Digest word 3 is Z[3] XOR Z[11], the a output of E3 and the c output of E1, so D3 = (e2 XOR e2') XOR eps. Digest word 6 is Z[6] XOR Z[14], the b output of E1 and the d output of E3, so D6 = (b2 XOR b2') XOR (h2 XOR h2'). In E1, b2 = ROR(b1 XOR c2, 7), so b2 XOR b2' = ROR(beta XOR eps, 7). In E3, h2 = ROR(h1 XOR e2, 8), and h1 XOR h1' = eta for every Y4 in the class (Lemma T), so h2 XOR h2' = ROR(eta XOR e2 XOR e2', 8). Rotating D6 left by 8 gives ROL(D6, 8) = ROL(beta XOR eps, 1) XOR eta XOR (e2 XOR e2').
The XOR with D3 cancels e2 XOR e2' and leaves n. QED.
A trial *passes the E1 test* when n = 0. The word n needs the first seven assignments of E1 for both messages and nothing of E3, whose eta is the constant of the class.
*Rule A.* Let h1 be the second value of E3 on message A, as in 6.2, and write h[i] for bit i of h1, bit 0 being the lowest. A trial *satisfies rule A* when all of the following hold:
    h[0] = 0;    h[1] = 1;    h[16] = 0;    h[17] = 0;
    h[2] XOR h[10] = 1;    h[3] XOR h[11] = 1;
    h[3] XOR h[12] XOR h[24] = 0;    h[6] XOR h[13] XOR h[25] = 0.
Each of the eight conditions contains a bit that no other contains (bits 0, 1, 16, 17, 10, 11, 12 and 13), so they are independent and a uniform word satisfies rule A with probability 2^-8.
Rule A can lose solutions: there are solutions of R = 0 with Y4 in the sub-class that violate it. The counter search of this package does not use rule A.
**6.4 The root instance and the declared experiment.** Sections 4 to 6 build the *root instance* of the construction: its messages are single chunks of 55 and 63 bytes, and the colliding compression is the root compression, with counter 0 and flags 11 (Section 1). The claim of this package is made for the *counter instance* of Sections 7 to 9, whose messages have 1024 t + 55 and 1024 t + 63 bytes and whose colliding compression is that of the last chunk, with counter t and flags 3. The two instances share the six constants, Fact P, Lemmas L and H, the class, Lemma N and the machine of 6.5; the sub-class and rule A belong to the root instance, not to the counter search of this package. The instances differ in the counter and the flags that the compression reads, and in the order in which the construction solves the assignments of rounds 0 and 1 (Sections 4 and 8).
An experiment of the organizer's harness returns pairs of complete messages and tests an event on their two digests, while the half-collision of the counter instance is an agreement of four words of the chaining value of a chunk that is not the root. The parent and root compressions above that chunk mix all eight words, so the digests of a counter pair are not expected to agree on the masked words, and on two counter pairs with t = 1 they do not (Section 7). No digest experiment can show a half-collision of a non-root chunk's chaining value. The declared experiment `frontline-search` (9.2) therefore executes the counter search of 9.1 on each trial and returns a pair of the root instance of the same lines: for the trial's context and its first passing member (member 0 if none), steps CO and CT of Section 8 with the flags 11 of the root in the line for K3.d1 and the c1 for which t = 0 (Lemma IP) give single chunks of 55 and 63 bytes, compressed as the root with counter 0 and flags 11. Theorem C, read with 11 in place of 3 in that line, as Lemma S2 reads steps O and M, predicts that every pair agrees on digest words 0, 2, 5 and 7, which the organizer recomputes.
**6.5 Seven trials in one word.** A packed word holds seven lanes of 36 bits at bit offsets 0, 36, .., 216. A lane represents its value modulo 2^32; bits 32..35 are carry guards. A constant is placed in all seven lanes before the batches that use it. Additions are single 256-bit additions. A rotation of every lane by r is the five operations
    PROR(z, r) = ((z >> r) AND A_r) OR ((z << (32-r)) AND B_r)
with A_r selecting the low 32-r bits of every lane and B_r the next r bits; the masks discard guard bits and bits shifted in from the neighbouring lane, so the result is reduced below 2^32. With M = 2^32 - 1 in every lane, the complement of the low 32 bits of a lane is an XOR with M, a difference x - y of a constant x and a lane y is (y XOR M) + (x + 1), and subtracting a constant y is one addition of the constant -y.
*The machine.* A load/store machine with 16 registers. One operation is charged for every addition, XOR, AND, OR and shift of 256-bit words, for every comparison and for every branch, so PROR = 5. One load is charged every time a word is fetched from memory, from a list or from a table into a register, and one store every time a register is written to memory or to a table. Shift distances are fixed in the instruction, and a register may hold a memory word across several operations. While no lane reaches 2^36 no carry leaves a lane and the low 32 bits of every lane equal the scalar value modulo 2^32; Lemma MB bounds the values of the batches of 9.8 below 2^36.

## 7. The tree lemma: the last chunk decides the digest

The claim is made for messages of more than one chunk. This section shows, from the organizer's reference code, that for such a message the digest is a function of the prefix and of the chaining value of the last chunk alone.
The organizer's hash, `verifier/blake3.py`, computes `blake3(data, rounds)`, with rounds = 2 for this target, by these lines of its code:
    chunk_count = max(1, (len(data) + 1023) // 1024)
    stack = []
    for counter in range(chunk_count - 1):
        output = _chunk_output(data[counter * 1024:(counter + 1) * 1024], counter, rounds)
        cv = _compress(*output, rounds)[:8]
        total = counter + 1
        while total & 1 == 0:
            cv = _compress(*_parent_output(stack.pop(), cv), rounds)[:8]
            total >>= 1
        stack.append(cv)
    output = _chunk_output(data[(chunk_count - 1) * 1024:], chunk_count - 1, rounds)
    while stack:
        output = _parent_output(stack.pop(), _compress(*output, rounds)[:8])
    cv, words, _, block_len, flags = output
    root_words = _compress(cv, words, 0, block_len, flags | ROOT, rounds)
    return struct.pack("<8I", *root_words[:8])
There `_chunk_output(chunk, counter, rounds)` compresses every block of a chunk but the last, starting from the chaining value IV, and returns the last block as a descriptor (cv, words, counter, len(block), flags | CHUNK_END), where flags is CHUNK_START = 1 when that block is the first of its chunk; its last block starts at `last_offset = max(0, (len(chunk) - 1) // 64 * 64)`.
`_compress(cv, words, counter, block_len, flags, rounds)` is the compression of Section 1 with v[0..7] = cv and v[12..15] =
(counter mod 2^32, counter >> 32, block_len, flags); it returns sixteen output words, of which the first eight are the chaining value. `_parent_output(left, right)` is the descriptor (IV, left + right, 0, 64, PARENT) of a parent node.
**Lemma TR (the last chunk decides).** Let t >= 1 and let F be any string of 1024 t bytes. For a string A of 1 to 64 bytes write words(A) for the sixteen little-endian words of A followed by zero bytes up to 64 bytes, and CV_t(A) for `_compress(IV, words(A), t, len(A), 3, 2)[:8]`.
(a) The last chunk of F || A is A, and the organizer's code compresses it once, as `_compress(IV, words(A), t, len(A), 3, 2)`: the compression of Section 1 with block A, block length len(A), counter t and flags CHUNK_START | CHUNK_END = 3. It is not the root compression.
(b) blake3(F || A, 2) is a function of F and of CV_t(A) alone.
(c) For strings A and B of 1 to 64 bytes with CV_t(A) = CV_t(B), blake3(F || A, 2) = blake3(F || B, 2).
Proof. (a) F || A has 1024 t + len(A) bytes with 1 <= len(A) <= 64, so chunk_count = t + 1 and the last chunk is data[t * 1024:] = A. In `_chunk_output(A, t, 2)`, last_offset = 0, so that function stops at its first block, offset 0, and returns (IV, words(A), t, len(A), CHUNK_START | CHUNK_END). The final loop of blake3 compresses this descriptor once, in its first pass, which runs because the stack is not empty (b).
(b) The loop over counter = 0, .., t - 1 reads data[counter*1024:(counter+1)*1024], which lies inside F, and no other byte of the message; so the stack that it leaves depends on F alone. Each pass appends one value and pops values only while total is even, so after t >= 1 passes the stack holds as many values as t has one bits, at least one. The final loop therefore runs at least once.
Its first pass forms `_parent_output` of the top of the stack and CV_t(A), and every later pass forms a parent descriptor from the next value of the stack and the chaining value of the descriptor before it. The root compression reads the last descriptor. So the digest is computed from the stack, which depends on F alone, and from CV_t(A).
(c) follows from (b). QED.
The code accepts messages shorter than 2^61 bytes; the messages of this package are shorter than 2^42 bytes (Section 8). The tree, its counters and flags and its root output are those of the target profile. The two messages of a pair are complete messages of the domain, and a pair with equal digests is an ordinary collision, not a free-start or compression-only one. The converse of (c) is not used.
*The digest does not show a partial agreement.* When CV_t(A) and CV_t(B) agree on four words only, the parent and root compressions over them mix all eight, and the two digests are not expected to agree on a fixed set of words. On two counter pairs of Section 8 with t = 1, messages of 1,079 and 1,087 bytes, the chaining values agree on words 0, 2, 5 and 7, and the two digests do not agree on digest words 0, 2, 5 and 7 (participant computation with the organizer's code). This is why the declared experiment returns pairs of the root instance (6.4).
*Participant checks with the organizer's code.* In each of the following the organizer's `verifier/blake3.py` was imported unchanged; they are participant computations, which the organizer has not run. (1) For 2,000 trials of the counter construction of Section 8 in 40 outer steps, 8 of them with outer words 0 or ffffffff, `_chunk_output` of the last chunk returned (IV, the block words, t, 55 or 63, 3) for A and for B, and `_compress` returned the chaining value that entry 26ebba63's program computes, in 2,000 of 2,000; words 0, 2, 5 and 7 of the two chaining values were equal in all 2,000 and all eight words in none; and 204,000 internal words of the construction were equal to a separately written forward computation of the compression. (2) For five counter trials with t = 1, 3, 3, 4 and 16,383, the complete messages F || A and F || B, with F a string of t chunks of pseudorandom bytes, were hashed by `blake3(m, 2)`. In each, the messages have 1024 t + 55 and 1024 t + 63 bytes; the code makes exactly one compression with block length 55 or 63, and its inputs are (IV, the block words, t, 55 or 63, 3); its chaining values agree on words 0, 2, 5 and 7 and not on all eight; the two digests differ; and when the output of that compression of F || B is replaced by the output of the one of F || A, blake3 returns the digest of F || A, and the other way round.

## 8. The counter construction

*Words and constants.* The construction has nine free words: the seven *outer words* C0.d1, D2.a1, D2.b1, S11, S4, X9 and w6; a member y of the class of 6.1 (Lemma Q), which becomes the value of Y4; and the *inner word* c1, which becomes the third value of E1 on message A. The constants are those of Section 4: X3, X7, X11 and X15, w4 = W4, w13 = W13, w14 = w15 = 0, the four constant first values K2.a1, K2.d1, K2.c1 and K2.b1 of K2 given in step O, and Y3, Y11 of Fact P. The compression reads three more values besides the message and the IV. K3 reads the flags, here 3 (the line for K3.d1); K1 reads v[13], here 0 (the line for K1.a1); and K0 reads the counter v[12], which is not fixed in advance: the line for t solves K0's second assignment for it. The names are those of Section 4.
*The cube Q*.* Q* is the set of the 2^21 words c with (c AND 0e09818b) = 0c008000. Member number j of Q*, for 0 <= j < 2^21, is the word whose bits at the 21 positions where 0e09818b has a zero are the bits of j, in increasing order of position.
*Members.* In Sections 8 to 12 a *member* is a member of the class of Lemma Q, not of the sub-class of 6.1. Member number k of the class, for 0 <= k < 2^19, is the Y4 whose e1 = Y3 + Y4 has the bits of k at the 19 positions where 03cf8303 has a zero, in increasing order of position, and Y4 = e1 - Y3. The search of this package uses every member; it has no sub-class and no rule A.
**Step CO (the outer step; 77 lines, from the seven outer words and y).**
    X2 = D2.a1 + D2.b1 + W13;   X8 = ROL(X7,7) XOR D2.b1
    C0.c1 = X8 + C0.d1;   K3.a1 = IV[3] + IV[7] + w6
    K3.d1 = ROR(K3.a1 XOR 3,16);   K3.c1 = IV[3] + K3.d1
    S15 = S11 - K3.c1;   S3 = ROL(S15,8) XOR K3.d1
    K3.b1 = ROR(IV[7] XOR K3.c1,12);   D3.a1 = S3 + S4
    S7 = ROR(K3.b1 XOR S11,7);   D3.b1 = X3 - D3.a1
    D2.c1 = ROL(D2.b1,12) XOR S7;   D3.c1 = ROL(D3.b1,12) XOR S4
    X4 = ROR(D3.b1 XOR X9,7);   X13 = X8 - D2.c1
    X14 = X9 - D3.c1;   C0.b1 = ROR(X4 XOR C0.c1,12)
    D2.d1 = ROL(X13,8) XOR X2;   D3.d1 = ROL(X14,8) XOR X3
    Y8 = ROL(Y4,7) XOR C0.b1;   S13 = ROL(D2.d1,16) XOR D2.a1
    S9 = D3.c1 - D3.d1;   Y12 = Y8 - C0.c1
    K1.c1 = S9 - S13;   Y0 = ROL(Y12,8) XOR C0.d1
    K1.d1 = K1.c1 - IV[1];   C0.a1 = Y0 - C0.b1 - w6
    K1.a1 = ROL(K1.d1,16);   w2 = K1.a1 - IV[1] - IV[5]
    X0 = C0.a1 - X4 - w2;   S14 = ROL(D3.d1,16) XOR D3.a1
    K1.b1 = ROR(IV[5] XOR K1.c1,12);   S10 = K2.c1 + S14
    D0.d1 = ROL(X15,8) XOR X0;   S5 = ROR(K1.b1 XOR S9,7)
    D0.c1 = S10 + D0.d1;   D0.b1 = ROR(S5 XOR D0.c1,12)
    X10 = D0.c1 + X15;   X5 = ROR(D0.b1 XOR X10,7)
    S1 = ROL(S13,8) XOR K1.d1;   w3 = S1 - K1.a1 - K1.b1
    X12 = ROL(C0.d1,16) XOR C0.a1;   D1.c1 = X11 - X12
    D1.d1 = D1.c1 - S11;   S8 = D2.c1 - D2.d1
    K0.b1 = ROL(S4,7) XOR S8;   S2 = ROL(S14,8) XOR K2.d1
    S6 = ROR(K2.b1 XOR S10,7);   X1 = ROL(X12,8) XOR D1.d1
    K0.c1 = ROL(K0.b1,12) XOR IV[4];   D1.b1 = ROR(S6 XOR D1.c1,12)
    C1.a1 = X1 + X5 + w3;   S12 = S8 - K0.c1
    w7 = S3 - K3.a1 - K3.b1;   X6 = ROR(D1.b1 XOR X11,7)
    C1.d1 = ROR(X13 XOR C1.a1,16);   D1.a1 = ROL(D1.d1,16) XOR S12
    C1.c1 = X9 + C1.d1;   C2.a1 = X2 + X6 + w7
    w10 = D1.a1 - S1 - S6;   C1.b1 = ROR(X5 XOR C1.c1,12)
    C2.d1 = ROR(X14 XOR C2.a1,16);   w12 = D2.a1 - S2 - S7
    Y1 = C1.a1 + C1.b1 + w10;   C2.c1 = X10 + C2.d1
    Y13 = ROR(C1.d1 XOR Y1,8);   C2.b1 = ROR(X6 XOR C2.c1,12)
    K0.d1 = K0.c1 - IV[0];   Y9 = C1.c1 + Y13
    S0 = ROL(S12,8) XOR K0.d1;   D0.a1 = ROL(D0.d1,16) XOR S15
    w8 = D0.a1 - S0 - S5;   w5 = S2 - K2.a1 - K2.b1
    w9 = X0 - D0.a1 - D0.b1;   w11 = X1 - D1.a1 - D1.b1
    Y5 = ROR(C1.b1 XOR Y9,7)
**Step CT (the trial; 16 lines, from c1 and the names of step CO).**
    E1.d1 = c1 - Y11;   E1.a1 = ROL(E1.d1,16) XOR Y12
    Y6 = E1.a1 - Y1 - w12;   Y10 = ROL(Y6,7) XOR C2.b1
    Y14 = Y10 - C2.c1;   E1.b1 = ROR(Y6 XOR c1,12)
    Y2 = ROL(Y14,8) XOR C2.d1;   E3.h1 = ROR(Y14 XOR (Y3 + Y4),16)
    w0 = Y2 - C2.a1 - C2.b1;   E3.g1 = Y9 + E3.h1
    K0.a1 = IV[0] + IV[4] + w0;   E3.f1 = ROR(Y4 XOR E3.g1,12)
    t = ROL(K0.d1,16) XOR K0.a1;   w1 = S0 - K0.a1 - K0.b1
    E1.a2 = E1.a1 + E1.b1 + w5;   E3.e2 = Y3 + Y4 + E3.f1 + w8
**Step CS (the messages).** If t = 0 the trial is invalid and is dropped: a message with no full chunk before its last chunk has that chunk as its root, compressed with counter 0 and flags 11 and not with the flags 3 that the line for K3.d1 used. Otherwise the words w0 to w12 of the lines, with w4 = W4 and w13 = W13, and w14 = w15 = 0 form the block of A; A is the first 55 bytes of its little-endian encoding, and B the first 63 bytes of that of the same words with w4' = W4' and w5' = w5 + fffffff8 in place of w4 and w5, as in steps S2 and S3 of Section 4. F is the string of 1024 t zero bytes, and the two messages are F || A, of 1024 t + 55 bytes, and F || B, of 1024 t + 63 bytes.
*The order and the calls.* Table CT gives each call's eight assignments by the name that the line for that assignment assigns; the cells K2.a1, K2.d1, K2.c1 and K2.b1 are the four constant values. E1's first five assignments are the lines for Y6, E1.a1, E1.d1, E1.b1 and E1.a2, in the order of the assignments; E3's first two assignments are the line for E3.h1, and its third to fifth the lines for E3.g1, E3.f1 and E3.e2.

| Call | 1st | 2nd | 3rd | 4th | 5th | 6th | 7th | 8th |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| K0 | K0.a1 | t | K0.d1 | K0.c1 | w1 | S0 | S12 | K0.b1 |
| K1 | w2 | K1.a1 | K1.d1 | K1.b1 | w3 | S1 | K1.c1 | S5 |
| K2 | K2.a1 | K2.d1 | K2.c1 | K2.b1 | w5 | S2 | S10 | S6 |
| K3 | K3.a1 | K3.d1 | K3.c1 | K3.b1 | w7 | S3 | S15 | S7 |
| D0 | w8 | D0.a1 | D0.c1 | D0.b1 | w9 | D0.d1 | X10 | X5 |
| D1 | w10 | D1.a1 | D1.d1 | D1.b1 | w11 | X1 | D1.c1 | X6 |
| D2 | w12 | S13 | S8 | D2.c1 | X2 | D2.d1 | X13 | X8 |
| D3 | D3.a1 | S14 | S9 | D3.c1 | D3.b1 | D3.d1 | X14 | X4 |
| C0 | X0 | X12 | C0.c1 | C0.b1 | C0.a1 | Y0 | Y12 | Y8 |
| C1 | C1.a1 | C1.d1 | C1.c1 | C1.b1 | Y1 | Y13 | Y9 | Y5 |
| C2 | C2.a1 | C2.d1 | C2.c1 | C2.b1 | w0 | Y2 | Y14 | Y10 |

The order was found by a solver search of the participant's helper agents for an order in which Y4 and E1.d1 are both free words.
**Lemma CT (the counter order).** (a) *Triangular.* In the printed order, step CO and then step CT, every line assigns a name that no earlier line assigns and that is neither one of the nine free words nor a constant, and it reads only constants, the nine words and names of earlier lines; a line of step CO reads neither c1 nor a name of step CT. Every line is one assignment of one call solved for the name on its left; the exceptions are the line for E3.h1, which is the first two assignments of E3 with the first substituted into the second (e1 = Y3 + Y4 + w15, w15 = 0), and the line for E3.e2, which uses the same e1. By Table CT the 93 lines and the four constant values of K2 are, each exactly once, the eight assignments of each of the eleven calls K0..K3, D0..D3, C0..C2, with the inputs and the message words of Section 1 for block length 55, counter v[12] = t, v[13] = 0 and flags v[15] = 3, with w4 = W4, w13 = W13, w14 = w15 = 0, and with the constants X3, X7, X11, X15 as the a output of D3, the b output of D2, the c output of D1 and the d output of D0; and the first five assignments of E1 and of E3 for message A, E1 with c input Y11 and E3 with a input Y3.
(b) *The calls.* For every choice of the nine words, the names of the lines are the executions of these calls. In particular round 0 on the block of A, with block length 55, counter t, v[13] = 0 and flags 3, leaves the state X of the names, with the four constants as X[3], X[7], X[11] and X[15]; C0 has outputs (Y0, y, Y8, Y12); and in the compression of A, E1.c1 = c1, since E1's third assignment is E1.c1 = Y11 + E1.d1.
(c) *The levels.* A line of step CO is a function of the seven outer words and y. Of the message words only w0 and w1 are lines of step CT, and so is the counter t; every other message word is a line of step CO or a constant. So the trials of one outer step differ in w0, w1 and t and in nothing else of their two messages.
Proof. (a) is read off the displays, each formula compared with Section 2 and with its call's inputs, outputs and message words (Section 1, with v[12] = t, v[13] = 0 and v[15] = 3); Table CT has one name in each of its 88 cells, all different, the four constant values of K2 among them, and with the five names of E1 and the four lines of E3 they are the 93 lines and the four constants. (b) As in Lemma T2 (b): an assignment solved for one of its terms is an equivalent equation modulo 2^32 (Fact 1), so a line's assignment holds once it has run, and by (a) no later line changes its names. By (a) and Table CT all eight assignments of each call hold, a constant output in its place (the lines for D3.b1 and D3.d1; X8; D1.c1 and X6; D0.d1 and X10) and y as the b output of C0 (the line for Y8); by Fact 1 the names are the execution of the call. (c) By induction over the printed order, with (a): a line of step CO reads only constants, the seven outer words, y and lines of step CO; w2, w3, w5 and w7 to w12 are lines of step CO, w6 is an outer word, w4, w13, w14 and w15 are constants, and w0, w1 and t are lines of step CT. QED.
**Theorem C (the last-chunk half-collision).** For every choice of the seven outer words, of a member y of the class and of a word c1, steps CO and CT give a counter t. If t is not zero, step CS outputs two distinct messages F || A and F || B of 1024 t + 55 and 1024 t + 63 bytes, with 1 <= t < 2^32, such that
(i) their last chunks are A and B, compressed with counter t, v[13] = 0 and flags 3 (Lemma TR (a));
(ii) the chaining values CV_t(A) and CV_t(B) agree on words 0, 2, 5 and 7;
(iii) in both last-chunk compressions Y4 = y, and the XOR difference between A and B of E3's first-half d value is eta = 830303cf; (iv) in the compression of A, E1.c1 = c1; and if c1 is in Q*, the XOR difference between A and B of E1's first-half b value is beta* = 18b0e098.
Proof. t is the XOR of two 32-bit words, so t < 2^32 and t >> 32 = 0, the value v[13] = 0 that the line for K1.a1 used. The sixteen words have w14 = w15 = 0 and w13 = W13, whose top byte is zero, so A and B are honest strings of 55 and 63 bytes whose zero-filled blocks are the sixteen words and the same words with w4 and w5 replaced, as in Section 5. By Lemma TR (a) the last chunks are compressed with counter t, v[13] = 0, flags 3 and block lengths 55 and 63. By Lemma CT (b) round 0 on the block of A leaves the state X of the names, with the four constants as X[3], X[7], X[11] and X[15]. The counter, v[13] and the flags are the same in both compressions, and K2 is the only call of round 0 that reads the block length, w4 or w5; Lemma L, whose proof concerns K2 alone, therefore gives the same state X for B. Lemma H gives (ii): its proof uses only round 1 and o[i] = Z[i] XOR Z[i + 8] for i = 0, 2, 5 and 7, and the chaining value is (o[0], .., o[7]). (iii) As in the proof of Lemma T: C0 reads the same words of X and w2, w6 in both compressions and has b output y by Lemma CT (b); w15 = 0, Y14 is the same in both, the a input of E3 is Y3 for A and Y3' for B by Fact P, and y is in the class, so the difference is eta by the definition of the class (6.1). (iv) E1.c1 = c1 is Lemma CT (b). E1 has inputs (Y1, Y6, Y11, Y12) and message words (w12, w5) for A, and (Y1, Y6, Y11', Y12) and (w12, w5 + delta) for B. Its first and second values are the same for both, so its third values are c1 and c1 + DY11, with DY11 = Y11' - Y11 = f608818b, and its fourth values are ROR(Y6 XOR c1, 12) and ROR(Y6 XOR (c1 + DY11), 12). Their XOR is ROR(c1 XOR (c1 + DY11), 12), which is beta* exactly when c1 XOR (c1 + DY11) = ROL(beta*, 12) = 0e09818b. For words c and x, (c XOR x) - c = x - 2 (c AND x) modulo 2^32, which is the identity of the proof of Lemma Q; with x = 0e09818b this holds exactly when 2 (c1 AND 0e09818b) = 0e09818b - DY11 = 04010000. As 0e09818b has no bit 31 the doubling is exact, and it holds exactly when (c1 AND 0e09818b) = 0c008000, that is when c1 is in Q*. The messages are distinct because their lengths differ. QED.
*The counter is the free word.* In the root instance the second assignment of K0 reads the counter 0, so K0.a1 = ROL(K0.d1,16) follows from the context, and with it the message word w0. Here that assignment is solved for the counter instead, which leaves K0.a1, and with it w0, free. The word w0 enters round 1 only in the fifth assignment of C2, and the lines for Y2, Y14, Y10, Y6, E1.a1 and E1.d1 of step CT map their running word one to one, so every value of E1.d1, and so of c1, can be prescribed in one outer step. With the counter fixed, no order of the assignments has both Y4 and E1.d1 among its free words, and with the counter free no order has Y4, E1.d1 and E3.h1 all free: the counter buys one prescribed word. These two statements are results of a participant search over the orders, decided by an exact peeling test that was checked against brute force; nothing below uses them.
**Lemma IP (the inner permutations and the member with t = 0; GPT Sol 6.1).** Fix the seven outer words and y. (a) The maps c1 -> E3.h1 and c1 -> t given by step CT are permutations of the 32-bit words. (b) So the 2^21 members of Q* give 2^21 different values of E3.h1 and of t, and at most one member of Q* has t = 0.
Proof. With the names of step CO fixed, the lines for E1.d1, E1.a1, Y6, Y10, Y14 and E3.h1, with e1 = Y3 + y, each map their running word one to one. Read backwards: Y14 = ROL(E3.h1,16) XOR e1, Y6 = ROR((Y14 + C2.c1) XOR C2.b1, 7), E1.a1 = Y6 + Y1 + w12 and c1 = Y11 + ROR(E1.a1 XOR Y12, 16). For the counter, Y2 = ROL(Y14,8) XOR C2.d1 = ROL(E3.h1,24) XOR ROL(e1,8) XOR C2.d1, and the lines for w0, K0.a1 and t give t = ROL(K0.d1,16) XOR (Y2 + IV[0] + IV[4] - C2.a1 - C2.b1), where K0.d1, C2.a1, C2.b1, C2.d1 and e1 are names of step CO. That is a composition of permutations of E3.h1. Its only zero is at E3.h1 = ROR((ROL(K0.d1,16) - IV[0] - IV[4] + C2.a1 + C2.b1) XOR ROL(e1,8) XOR C2.d1, 24), and the inverse above gives its one value of c1, which may or may not lie in Q*. QED.
So an outer step has 2^21 or 2^21 - 1 valid trials. Lemma IP bounds the number of trials that the rule t != 0 drops, one in 2^21 at most; it does not bound the share of the collision mass that the dropped trial carries (10.3). In the participant's checks the member with t = 0 was constructed by the inverse above in 40 outer steps and rejected by the program of entry 26ebba63 in 40 of 40; over 8,192 further outer steps it lay in Q* 4 times, against 4.0 expected, and was rejected 4 times out of 4.
*The length of the messages.* Within one outer step the 2^21 members of Q* give 2^21 different values of t below 2^32 (Lemma IP); over 2,000 trials of the participant's check t ran from 891,836 to 4,291,586,422 with a mean of log2 t of 30.56. A pair found by the search has messages of 1024 t + 55 and 1024 t + 63 bytes, shorter than 2^42 bytes and about 2^41 on average. A small t cannot be chosen: it is the value of a permutation of c1 at the member that the search finds.
**The outer filter.** Number the seven outcomes of beta* whose tau ends in 5020a0 (10.1) j = 1 to 7 in the order of the table of 10.1: 175020a0, 185020a0, 275020a0, 285020a0, 385020a0, 675020a0 and 685020a0, the seven of entry 26ebba63. This search lists six of them, the set S = {1, 2, 3, 4, 5, 7}: all but 675020a0 (j = 6). In the hexadecimal masks below, with bit j - 1 for outcome j, S is 5f. Beta* has seven more outcomes on the class, the same seven with bit 14 of tau set (j = 8 to 14 of 10.1); this search does not list them either. Let tau_j be the tau of outcome j, sigma_j = tau_j XOR ROR(tau_j, 1) and theta_j = ROL(sigma_j, 12); all seven have eps = 6e21be55. For an outer step put omega = Y3 + y + w8, with Y3 of Fact P, y the member of the outer step and w8 the name of step CO; DY3 = Y3' - Y3 = 01b77cfd is that of Section 6. For a word x:

- condition (1)_j holds for x when some word h gives (x + h) XOR (x + (h XOR eta)) = theta_j;
- condition (2)_j holds for x when some word f gives (x + f) XOR ((x + DY3) + (f XOR sigma_j)) = eps.

An outer step *passes* the filter when for some j in S both (1)_j holds for its Y9 and (2)_j holds for its omega. Y9 and w8 are names of step CO and y is drawn with the outer words, so whether an outer step passes depends on the outer step alone and on no c1.
**Lemma F (the outer filter; GPT Sol 6.1, answers AC and AN).** Fix an outer step that does not pass the filter. Then no trial of the outer step, for any word c1, has R = 0 with an E1 outcome in S. (A trial with R = 0 whose E1 outcome is another outcome of beta* on the class may lie in a rejected outer step; the search does not count it.)
Proof. Take a trial with R = 0 whose E1 outcome is outcome j. Write h, g, f and e2 for E3.h1, E3.g1, E3.f1 and E3.e2 in the compression of A, and h', g', f' and e2' for the same values in that of B. Y9 and w8 are the same in both compressions: w8 is a line of step CO and a word of both blocks, and Y9 is an output of C1, which reads words of the state X, the same for A and B (proof of Theorem C), and the message words w3 and w10, which the two blocks share. Both compressions have Y4 = y and h' = h XOR eta (Theorem C (iii)), and the a input of E3 is Y3 for A and Y3' for B (Fact P). The conditions of R = 0 (Section 13, how r is counted) give that the XOR difference of E3's first-half b values is psi = tau_j XOR ROR(tau_j, 1) = sigma_j, and that of its a outputs is eps' = eps. Now g = Y9 + h and g' = Y9 + (h XOR eta); f = ROR(y XOR g, 12) and f' = ROR(y XOR g', 12), so f XOR f' = ROR(g XOR g', 12) = sigma_j gives g XOR g' = theta_j, and h witnesses (1)_j for Y9. With w15 = 0, e2 = Y3 + y + f + w8 = omega + f and e2' = Y3' + y + f' + w8 = (omega + DY3) + (f XOR sigma_j), and e2 XOR e2' = eps, so f witnesses (2)_j for omega. So the outer step passes, against the hypothesis. QED.
The lemma uses no law of the words: no uniformity, no independence and no relation between h and f besides the two equations. It does not use the rule t != 0, and it holds for any list of outcomes, S among them. The filter can pass
outer steps that hold no success, since (1)_j and (2)_j are solved with separate witnesses; it cannot reject an outer step that holds a success with an outcome of S.
**The exact share (GPT Sol, answers AC, AN and AW; recounted by the participant).** Let pi be the share of the 2^64 pairs (x1, x2) of words such that for some j in S condition (1)_j holds for x1 and (2)_j for x2. Then
    pi = 18,289,159,183,466,496 / 2^64 = 279,070,422,111 / 2^48,
about 0.00099145731 = 2^-9.978162. With all seven outcomes j = 1 to 7 in place of S the share is 20,504,986,129,465,344 / 2^64 = 312,881,258,079 / 2^48 = 2^-9.813176, which is the share of the seven-outcome filter of entry 26ebba63 and is not used here. Let pi_E be the share of the 2^32 words x for which (2)_j holds for some j in S: pi_E = 233,715,456 / 2^32, about 0.054416120 = 2^-4.199822.
*Method.* Whether (1)_j holds for x is decided bit by bit from bit 0 upwards. At bit i the XOR of the two sum bits prescribes the XOR of the two incoming carries; the state is the set of incoming carry pairs that some choice of the lower bits of the witness reaches with the lower bits of x, and the next state is the set of carry pairs out of bit i that some witness bit gives from a pair of the set that meets the prescription. The condition holds when the set is still nonempty after bit 31, which has no outgoing carry to prescribe because the arithmetic is modulo 2^32. For (2)_j the carry of x + DY3 is carried as well. The seven sets for the seven outcomes are carried together over the same bits of x, each with its own witness (a subset construction), so one pass over the bits of x gives its *mask*, the set of j for which the condition holds; equal states add their counts of prefixes of x, and witnesses are never counted. A pair passes exactly when the mask of x1 under (1) and the mask of x2 under (2) intersect, so the number of passing pairs is the sum, over pairs of intersecting masks a and b, of the number of words with mask a under (1) times the number of words with mask b under (2).
*Certificate.* Masks are written in hexadecimal with bit j - 1 for outcome j (bit 0 for 175020a0, bit 6 for 685020a0). The numbers of words with each nonzero seven-bit mask m are 7,936 a_m under (1), a_m the second column, and 1,082,016 b_m under (2), b_m the fourth and the sixth columns:

| mask, (1) | words / 7,936 | mask, (2) | words / 1,082,016 | mask, (2) | words / 1,082,016 |
| --- | ---: | --- | ---: | --- | ---: |
| 01 | 266 | 01 | 10 | 36 | 30 |
| 02 | 2,044 | 02 | 18 | 41 | 10 |
| 04 | 1,778 | 03 | 5 | 43 | 1 |
| 08 | 254 | 09 | 10 | 49 | 10 |
| 10 | 2,032 | 12 | 22 | 53 | 1 |
| 12 | 2,044 | 13 | 5 | 5b | 2 |
| 18 | 1,524 | 16 | 30 | 62 | 1 |
| 20 | 2,016 | 1b | 2 | 63 | 4 |
| 21 | 1,512 | 1e | 2 | 72 | 1 |
| 40 | 504 | 1f | 8 | 73 | 4 |
| 42 | 1,512 | 22 | 15 | 7e | 2 |
| 52 | 1,512 | 32 | 15 | 7f | 8 |

No other nonzero seven-bit mask occurs; 134,896,128 words satisfy some (1)_j and 233,715,456 some (2)_j. Every mask of (2) in the table meets 5f, so the same 233,715,456 words satisfy (2)_j for some j in S. The sum of a_m b_n over the pairs of masks m and n with m AND n AND 5f not zero is 2,129,896, and over all pairs of intersecting masks it is 2,387,944. So the number of pairs that pass for S is 7,936 * 1,082,016 * 2,129,896 = 18,289,159,183,466,496, and for all seven 7,936 * 1,082,016 * 2,387,944 = 20,504,986,129,465,344 (the participant's arithmetic on the table; GPT Sol's answer AW 3 gives the same 279,070,422,111 and 233,715,456). With the seven other outcomes of beta* on the class added, GPT Sol's certificate of the fourteen-outcome filter gives 99,669,577,442,459,648 passing pairs, 2^-7.531997; that filter is not used here.
*The automata.* The subset construction above is built as four byte tables: a state is the carry of x + DY3 (zero for (1)) and, per outcome, the set of reachable carry pairs, four bits; the table of byte p maps a state and byte p of x to the next state, and the table of the last byte maps to the mask. The search builds the two automata for the seven outcomes of entry 26ebba63 once (step 0 of 9.1) and ANDs every entry of their last tables with 5f, so that every mask it reads is restricted to S; the states and the number of table loads do not change. The construction has 1, 18, 43, 37 and 1, 3, 7, 7 states at the four byte boundaries and tables of 25,344 and 4,608 entries (a participant run of the program of entry 26ebba63). Its count of passing pairs for the seven outcomes is 20,504,986,129,465,344.

## 9. The counter search

**9.1 The algorithm.** The search uses these constants. FACTOR = floor(97 * 138,512,695,296 / 100) = 134,357,314,437 is the factor of H1' (10.3): 97/100, rounded down, of the count in 10.1 of the six outcomes of S. RUN_STEPS_MIN = ceil(0.49594 * 2^128 / (FACTOR * (2^21 - 1))) = 598,932,067,520,075,621,629 is the least number of outer steps that yields 0.49594 = 24797 / 50000 expected listed good trials at the rate of H1' (10.4). RUN_CONTEXTS = ceil(RUN_STEPS_MIN / 2^19) = 1,142,372,260,131,981, about 2^50.021, counts the contexts of a run (9.8), and RUN_STEPS = 2^19 * RUN_CONTEXTS = 598,932,067,520,076,054,528, about 2^69.021, its outer steps, 432,899 more than RUN_STEPS_MIN, with 2^90.021 trials in all. A context has 16,384 clusters of 32 members in 2,341 = ceil(16,384 / 7) representative batches (9.9), so a run has 2,341 * RUN_CONTEXTS representative batches, about 2^61.214, and its opened clusters have the budget A_BUDGET = ceil(852,139 * RUN_CONTEXTS / 2^7) + 16,384 * ceil(sqrt(10 * RUN_CONTEXTS)) = 7,605,157,652,531,425,333, about 2^62.722 (9.9). SHARE = 18,289,159,183,466,496 is the number of pairs that pass the filter for S (Section 8), whose share pi is therefore SHARE / 2^64, and E_COUNT = 233,715,456 the number of words that pass the automaton of (2) for S (Section 8). Each of the two budgets is the bound of H4' on the expected number of its outer steps in a run, rounded up, plus the reserve 2^19 s with the same s = ceil(sqrt(10 * RUN_CONTEXTS)) = 106,881,817:
    E_BUDGET    = 32,592,462,706,762,850,655   (about 2^64.915)
                = ceil(1000026 * RUN_STEPS * E_COUNT / (1000000 * 2^32)) + 2^19 s = 32,592,406,669,908,779,359 + 56,036,854,071,296,
    PASS_BUDGET = 593,976,122,525,029,364      (about 2^59.137)
                = ceil(1000176 * RUN_STEPS * SHARE / (1000000 * 2^64)) + 2^19 s = 593,920,085,670,958,068 + 56,036,854,071,296.
The batches of a context that can hold a lane with a nonzero mask of (2) are its 2,341 representative batches and, for each of its 16,384 clusters, its two partner chunks or, on a straddling cluster, its five partner batches (9.9), at most 84,261 in all; a batch is *filled* at its first such lane (9.8). The fills have the budget G_BUDGET, the bound 7,198 of H_G_cluster on the mean number F(C) of fills that the masked walk executes in a context (10.3; F(C) is at most the number of filled batches of the walk with five partner batches per opened cluster, context by context, Lemma XF (d)), times RUN_CONTEXTS, plus the reserve 84,261 s with the same s:
    G_BUDGET    = 8,222,804,534,398,781,475   (about 2^62.928)
                = ceil(7,198 * RUN_CONTEXTS) + 84,261 s = 8,773,722,828,845,975,250 + 9,302,777,733,432.
Further, the table CT of 9.7 holds, for every subset T of S, the metered cap CM(T) of the call in bits 0 to 15 of its word, with A(T) of 9.7 above them: CM(T) is the proved cap (Section 11) of steps 2 and 3 with the guards (G7) and (G15) and the certificate of step 3 on the outcomes of T, with one tree per family (Lemma FX), and CM(T) = 0 when T is empty; CM(T) <= 15,012 for every T that occurs (Lemma ME). u_U = 335,060,079,487,497 / 2^48 = 1.1903725... is the mean, over all outer steps, of the ledger U of this row in the model M of 10.3: GPT-6 Astra's exact bound 727,329,595,507,749 / 2^49 on the mean of the ledger U0 = U + 410 of the earlier layout, less 410 times the call probability 279,070,422,111 / 2^50 of M (10.3). The meter debits exactly the ledger U in every call (Lemma ME), so the credit of the solver is m_C, the bound of H5_exec on the expected sum of U over a run, at 1.01 times u_U, rounded up, plus a reserve in L_C = 15,012 * 2^19 = 7,870,611,456, the most that one context can debit, plus the preflight reserve 15,012, the largest metered cap:
    m_C         = ceil(101 * RUN_STEPS * 335060079487497 / (100 * 2^48)) = 720,081,801,874,515,573,539,
    CREDIT      = 720,096,858,523,588,089,938   (about 2^69.287)
                = m_C + ceil(sqrt(40 L_C m_C)) + 14 L_C + 15,012 = 720,081,801,874,515,573,539 + 15,056,649,072,501,387 + 15,012.
A *call* is a passing outer step whose pre-check keeps a nonempty T. Every call has U >= 4,272 (Lemma CP), so the calls of a run have the budget, again with the reserve 2^19 s:
    CALL_BUDGET = 168,614,511,075,633,931   (about 2^57.320)
                = ceil(m_C / 4,272) + 2^19 s = 179,851,891,994,636,224 + 57,883,655,929,856.
The six counted events of a run, opened clusters, E lanes, fills, passing lanes, calls and straddling clusters, add their units of Section 11, u_O = 168, u_E = 10, u_G = 56, u_P = 43, u_C = 6 and u_F = 208, to one register W, the *work register*, which starts at
0. A straddling cluster, an opened cluster that walks the five old partner batches (9.9), is an opened cluster and also a straddling one: it adds u_O + u_F = 376. The straddling clusters have the budget, with the same reserve over the contexts (Lemma OR, 9.9):
    FB_BUDGET   = 2,570,351,266,169,534   (about 2^51.284)
                = ceil(9 * RUN_CONTEXTS / 4) + 128 s = 2,742,550,203,515,344 + 14,131,751,936.
A context tests W once, at its start, against
    WB    = u_O A_BUDGET + u_E E_BUDGET + u_G G_BUDGET + u_P PASS_BUDGET + u_C CALL_BUDGET + u_F FB_BUDGET = 2,091,155,460,017,633,054,404,
and one context adds at most W_CTX = 16,384 u_O + 2^19 u_E + 84,261 u_G + 2^19 (u_P + u_C) + 128 u_F = 38,430,744 to W, for its 16,384 clusters, 2^19 members, 84,261 batches and at most 128 straddling clusters (Lemma XF (e)). The program of the declared experiment computes these constants by the same formulas and asserts the budgets, the credit and N against the figures of this text (9.2).
0. Once, before the first context: the two automata of the outer filter for the seven outcomes are built, with the entries of
   their last tables ANDed with S (Section 8); at the word
   addresses f of Lemma DT, in one copy, the two levels of the direct tables T1, R1 at f = 2^34 + l and L1 at f = 2^34 + 2^26 + s + 2^16 h', l < 2^16, s < 35 and h' < 2^10, with the mask of (1), restricted to S, of every 32-bit word (Lemma T26), and T2,
   R2 at f = 2^35 + l, l < 2^16, and L2 at f = 2^33 + s + 2^16 h, s < 4 and h < 2^16, which give the mask of (2),
   restricted to S, of every 32-bit word, and the table PXR at f = 2^35 + 2^16 + l are written; so are the member lists in
   cluster order with the broadcast words of the representatives (9.9), the table CT of the metered caps
   (9.7), the three transition arrays, the static row descriptors of the six outcomes of S and the written-out code of the walk
   and of the joint solver with the guards (G7) and (G15) (9.4, 9.7, 9.8, 9.9, Section 11). The credit register starts at CREDIT
   and W at 0. Nothing built here depends on an outer word.
1. Walk the contexts one after another, RUN_CONTEXTS of them. A context first compares W with WB and halts the run with failure
   when W > WB. It takes one fresh uniform 256-bit word: its 32-bit words 0 to 6 are the outer words C0.d1, D2.a1, D2.b1, S11, S4,
   X9 and w6, and word 7 is unused. The 39 context lines of step CO (Lemma Y) run once, and the words of the context are prepared
   (9.8), with the four flags hbad_i and the word AW of the gate (9.9). The context then runs its 2,341 representative batches one
   after another, the first 2,340 in a loop and the last after it; lane i of representative batch b carries the representative of cluster 7 b + i. The context also builds the descriptor
   table of its masked partner walk (9.9). *Gate (9.9):* the omega side of a representative batch also gives the three gate words
   and the carry word IX, and each used lane computes from them the gate value of its representative. On 0 the whole cluster of
   the lane is skipped, with no read of T2 (Lemma CL). Otherwise the representative is walked with the omega of its batch, as below. Then the
   gate value is used: on 2 or 3 the cluster straddles, u_O + u_F is added to W, and its 31 partners are walked in the five partner
   batches of the earlier layout; on 1 u_O is added to W and the descriptor of the context's table at the carries and the omega prefix of the
   representative gives at most two chunks of at most seven partners, which are walked as batches, and the other partners, which
   fail test (2) (Lemma XF), are not. All this comes before the gate test of the next lane. The outer step of a lane is the
   context together with the member of the lane. *Test (2):* the 8 member-dependent lines of step CO on which omega depends, and
   omega = Y3 + y + w8, are computed for all lanes at once on packed words; each used lane, lane 0 first, then reads the mask of
   (2) of its omega, restricted to S, from R2 and L2, after moving its lane to lane 0 by a shift (9.8). When that mask is zero the
   outer step of the lane is finished. *E lane:* a lane with a nonzero mask of (2) adds u_E to W. *Fill:* the first such lane of
   its batch adds u_E + u_G instead, in one addition, C0.a1 and D0.d1 of the batch are rebuilt, and the 17 member-dependent lines
   on which only Y9 depends are computed on packed words for all lanes of the batch, two of them in one line, and kept in a
   register as the batch's *cached Y9* (9.8). Then the cached Y9 is shifted so that the Y9 of the lane is in lane 0, its mask of (1),
   restricted to S, is read from R1 and L1 at the low 16 and the low 26 bits of the lane's Y9, and the AND of the two masks is the mask X of the outer step. When X is
   zero the outer step is finished. Otherwise the outer step *passes* (Section 8): C2.a1, C2.d1, C2.c1 and C2.b1 are computed from
   the words of the batch (9.6). *Pre-check:* compute the word nu of 9.7 from Y9, e1, C2.c1 and C2.b1; T = X when nu is 3 or 4,
   and T = 0 otherwise. If T is zero, u_P is added to W and the outer step ends there (it holds no listed good trial, Lemma VP).
   Otherwise the outer step is a call: u_P + u_C is added to W, and CM(T) is read from the table CT; halt with failure when it
   exceeds the remaining credit (the *preflight*), and else run steps 2 and 3 for this outer step under the meter of 9.7, which
   subtracts from the credit A(T) at the start of the call and the unit cost of each block as the block runs.
2. *Roots:* run the joint solver of 9.4 with the guards (G7) and (G15) of 9.7 on Y9, y and omega for every outcome j whose bit is
   set in T. It returns the joint roots of these outcomes that satisfy (G7) and (G15), each a word h with the outcome of which it
   is a root, at most 16 per outer step (9.4).
3. *Certificate (Lemma RC, 10.2; GPT Sol, answer CF 6):* for each returned root h, with its outcome j, in turn, at its leaf:
   compute from h, with the names of step CO and all sums modulo 2^32, the lines of step CT backwards (Lemma IP), Y14 = ROL(h,16)
   XOR (Y3 + y), Z = (Y14 + C2.c1) XOR C2.b1, Y6 = ROR(Z, 7), E1.a1 = Y6 + Y1 + w12, E1.d1 = ROR(E1.a1 XOR Y12, 16), c1 = Y11 +
   E1.d1, E1.b1 = ROR(Y6 XOR c1, 12) and E1.a2 = E1.a1 + E1.b1 + w5, and t by the lines Y2, w0, K0.a1 and t of step CT; put s =
   E1.b1 AND beta*, p = ((tau_j - beta* + 8 + 2 s) mod 2^32) >> 1 and z = ROR(E1.d1 XOR E1.a2, 8). The root is *certified* when
       (Q)  c1 AND 0e09818b = 0c008000,
       (A)  E1.a2 AND tau_j = p,
       (C)  (c1 + z) XOR ((c1 + DY11) + (z XOR ROR(tau_j, 8))) = eps,
       (T)  t != 0,
   with DY11 = Y11' - Y11 = f608818b and eps = 6e21be55. For the first certified root, form the blocks A and B by steps CT and
   CS for its c1 (no table is read: these are lines on the names of step CO, c1 and constants) and keep them, with t, in the
   words of the final step. *Release:* the program then releases every other word it holds, the tables,
   the member lists, the descriptor table and the other data of step 0, and the code of the walk and of the joint solver; it
   keeps only the routine of the final step and its words (Section 12). The release executes no word operation; no released
   word is read again. Only then evaluate blake3 of F || A and of F || B in full, each streamed a chunk at a time, the t chunks of
   F from one chunk of zero bytes and then the last chunk A or B, check that the two digests agree, write the pair to the output
   in the same way, a chunk at a time, and halt. No message is held: each chunk is produced in one chunk word, compressed or
   written, and overwritten by the next (Section 12).
4. If no pair has been output when the last context ends, halt with failure.
There are exactly three ways for the run to halt with failure, each a test on a value kept by the algorithm: W exceeds WB at the start of a context, the metered cap CM(T) of an outer step that reaches the solver exceeds the remaining credit, or the contexts run out. W is the sum of u_O, u_E, u_G, u_P, u_C and u_F times the counts of opened clusters, E lanes, fills, passing lanes, calls and straddling clusters so far. A context starts only when W <= WB and adds at most W_CTX, so W <= WB + W_CTX at every moment of a run: the units of these six events add up to at most WB + W_CTX (Section 11). If none of the six counts exceeds its budget, A_BUDGET, E_BUDGET, G_BUDGET, PASS_BUDGET, CALL_BUDGET or FB_BUDGET, then W <= WB; so W halts the run only on the union of the six overflow events of 10.4. The metered debits of the outer steps that run steps 2 and 3 add up to at most CREDIT: a call starts only when the credit left covers CM(T), and it debits at most CM(T) (Lemma ME), so the credit never goes below zero. Steps 2 and 3 need no budget of their own, since the joint solver returns at most 16 roots and, whatever the words of an outer step, their work in it is at most its CM(T) and its debit is that work (9.4, 9.7, Section 11). The work of every run is therefore bounded by the counts of Section 11, and a pair of messages is formed and hashed at most once, for a certified root.
A trial is *valid* when its t is not zero; a valid trial with R = 0 is *good*; a good trial is *listed* when its E1 outcome is in S (Section 8, 10.1). A listed good trial is found unless the run ends before its outer step is reached, by the work register W, by the credit or by the output of another pair: its outer step passes the filter by Lemma F, its cluster is opened by Lemma CL, its member is walked by Lemma XF, its lane is taken as passing by Lemmas MB and DT, the pre-check keeps its outcome by Lemma VP, the joint solver returns its E3.h1 as a root of its outcome by Lemmas G7, G15 and CV, and step 3 certifies it (Lemmas RC and CV, 10.2). Every certified root is the E3.h1 of a listed good trial (Lemma CV). A good trial that is not listed is not found, and Section 10 does not count it; by the count of 10.1 beta* has eight more outcomes on the class, 675020a0 and the seven with bit 14 of tau set, which carry 4,065,280 of its 71,698,432 (5.7 per cent) and are not listed. When the run outputs a pair, the pair is a collision of two complete messages: the certified trial has R = 0 (Lemma V, 10.2), step 3 has checked both digests, and Lemma TR (c) says that R = 0 with the half-collision of Theorem C gives equal digests.
**9.2 The declared experiment.** `experiments/frontline.py` (Python 3, standard library only, no BLAKE3 library) holds this search: steps CO, CT and CS; the automata of the filter restricted to S; the walk of 9.8, 9.9 and the amendment (gate, tables read through each lane's shift, descriptors, high-part tests, chunk A and the pending batch, the order of the reads of L and M); fills, passing lanes, pre-check, preflight and meter; the joint solver of 9.4 with (G7) and (G15); the certificate of step 3; the halts; and the constants of this section and the amendment, computed by their formulas and asserted equal to this text. Table entries and broadcast words are computed on demand by the rules that fill them, and the units are added per event.
One organizer trial is one context: seven outer words from the trial's seed, the context lines, representative batches 0 to 3 and the last batch (32 clusters) with the partners of every live cluster. A trial starts with W = 0 and the full CREDIT, so neither WB nor the credit is reached. Every walked quantity is recomputed or compared as the manifest's scope lists (members straight-line, gate values and descriptors against scalar words, table reads against bit-serial decisions, every member of a closed or dead cluster and every left-out partner bit-serially, passing lanes against a scalar rebuild, debits against the ledger, every solver call repeated without (G15), and a joint root planted at every eighth trial). The returned pair is that of 6.4, and the 16 observations are untrusted counts. Not exercised at this scale: a root of the search and a halt; the machine layout is kept in variables with the same decisions; the entry and return of an opened cluster's code (14) have no statement.
**9.3 The self-test.** `python3 experiments/frontline.py --selftest`, which the organizer does not run, checks the constants of 9.1 and the amendment against this text; both automata against brute force at width 8; SHARE and E_COUNT from the tables; T1 and T2 against bit-serial decisions on 4,000 random words, with T2(x) = 0 off S7, and HE3 there (H) with the counts of HE, HE3, HR and HS (K); the residues of Lemma A9; the cluster map as a bijection; the pre-check against nu and VMASK; the straddle rule of hbad_i against the prefixes of Lemma KP (69,632 cases); the gate entry and the packed gate words (3,584 cases); the reads of R1, L1, R2 and L2 through each lane's shift, Lemma T26 and the classes of Lemma DT; the omega side and the fill against step CO (224 lanes); halt drills for W, WB, the credit and the preflight reserve; and on 8 seeds that the gate, a gate that opens every cluster and the walk without the mask give the same E lanes and passes. The program asserts CM(T) <= CM_MAX for every T of a call.
**9.4 The joint solver (GPT Sol, answers AE, AF, AI, AL, AO and AR).** Fix a passing outer step and write Q = Y9, y for its member, E = omega = Y3 + y + w8 and E' = E + DY3; x[i] is bit i of a word x, bit 0 the lowest, and maj is the majority of three bits. Put e1 = Y3 + y and b = e1[2], u = e1[21] and v = e1[26], three bits that are free in the class (in the sub-class of entry 26ebba63, u = v = 0). For an outcome j of beta* (10.1) put sigma = sigma_j and theta = theta_j (Section 8), eps = 6e21be55, gamma = eta XOR theta, D = (sigma XOR eps) AND 7fffffff, kappa = sigma XOR eps XOR E XOR E' and mu = ROR(eta XOR eps, 8) = 9aed22bd. For a word h put g = Q + h, f = ROR(y XOR g, 12), e2 = E + f and h2 = ROR(h XOR e2, 8): for E3.h1 = h these are E3.g1, E3.f1 and E3.e2 of step CT and the d output of E3 on message A (6.2). The *static descriptor* of outcome j holds sigma, theta, gamma, D and the positions of its constants and guards; the static descriptors of the six outcomes of S depend on no outer word and are formed once per run.
*Joint roots.* A word h is a *joint root* of outcome j when
    (J1)  (Q + h) XOR (Q + (h XOR eta)) = theta,
    (J2)  (E + f) XOR (E' + (f XOR sigma)) = eps,
    (J3)  (g + h2) XOR ((g XOR theta) + (h2 XOR mu)) = tau_j.
(J1) and (J2) are the conditions (1)_j and (2)_j of Section 8, with the two witnesses tied by f = ROR(y XOR (Q + h), 12). By (J1) theta is a function of h, and then so is the left side of (J3); the seven values of tau are different, so no word is a joint root of two outcomes. There is no rule A: a joint root is any word that satisfies (J1) to (J3).
*Carries.* Write u[i] and u'[i] for the carries into bit i of Q + h and of Q + (h XOR eta), and a[k] and a'[k] for those into bit k of E + f and of E' + (f XOR sigma), all 0 into bit 0. Bit by bit, (J1) holds exactly when u'[i] = u[i] XOR gamma[i] for every i, and (J2) exactly when a'[k] = a[k] XOR kappa[k] for every k. Bit i of h gives g[i] = Q[i] XOR h[i] XOR u[i] and bit k = (i + 20) mod 32 of f, f[k] = y[i] XOR g[i]. So the solver chooses h from bit 0 to bit 31 and runs both pairs of additions along it: those of (J1) on bits 0 to 31, and those of (J2) on bits 20 to 31 and then 0 to 19. The carry a[20] is not known at the start; it is guessed for the constants of (a) below, and the check of (J2) as a word at each leaf enforces that bits 0 to 19 give the right carry into bit 20 (one traversal, below). At a bit k < 31 with D[k] = 1, the *prescription* of f[k] is f[k] = E[k] XOR sigma[k] XOR kappa[k+1] if a[k] = E[k], and f[k] = E'[k] XOR kappa[k+1] otherwise: from carries a[k] and a[k] XOR kappa[k], it is the only value of f[k] that gives the carries into bit k + 1 the difference kappa[k+1] (Lemma S5).
*The phase equations.* The participant's counter, run on the class with its E3 count split by the pattern of h on the sixteen bits 0 to 3, 6 to 13, 16, 17, 24 and 25 and by (b, u, v), records for each of the eight values of (b, u, v) every pattern that occurs in a solution of E3 with an outcome of beta* (records of the participant, not in the package). GPT Sol checked every recorded pattern against
    h[0] = 0,  h[1] = 1,  h[2] = 1 XOR b,  h[10] = b,  h[16] = h[17] = 0,
    h[11] = 1 XOR h[3],  h[24] = h[3] XOR h[12] XOR u                   (PHASE)
and found no violation in any of the eight cells, whose sets have 88, 88, 108, 132, 108, 132, 88 and 88 patterns in the order b + 2u + 4v. Each of the fourteen outcomes of beta* on the class has an E1 count L_j > 0 that depends neither on y nor on h, so a zero count outside (PHASE) means that no joint root of any of them, the six of S among them, violates (PHASE). The equations are consequences of the count, which the solver uses as guards; they are not a rule that drops members or solutions.
*The parity certificate.* Call the outcomes j = 1 to 7, whose tau ends in 20a0, the *old rows*, and j = 8 to 14, whose tau ends in 60a0 and has bit 14 set, the *new rows*; a row is also named by the first three hexadecimal digits of its tau. Every joint root h of outcome j, for y in the class, satisfies
    h[6] XOR h[13] XOR h[25] = u XOR tau_j[14],                        (P*)
that is h[6] XOR h[13] XOR h[25] = u on the old rows and u XOR 1 on the new rows. This search lists only the old rows, on which (P*) reads h[6] XOR h[13] XOR h[25] = u; the certificate is stated for all fourteen rows as it was proved. The proof is an exact finite count. The count N3_j of 10.1 counts the quadruples (Y4, E3.h1, Y9, w8), Y4 in the class, that meet the E3 conditions of outcome j, and by the proof of Lemma V (10.2) these are exactly the quadruples whose E3.h1 is a joint root of outcome j for Q = Y9, y = Y4 and E = Y3 + Y4 + w8. GPT Sol split every N3_j by the phase (b, u, v) of Y4 and by the parity pi = h[6] XOR h[13] XOR h[25] of the root. The split is a sum of nonnegative integers over an exact enumeration of submasks, through the identity (z XOR m) - z = m - 2 (z AND m) modulo 2^32 and a carry recurrence with two states in integers, in coordinates of E3 that are a bijection of the counted quadruples; nothing is sampled. With a = 24, 16, 4, 24, 32, 1 and 6 for the rows 175, 185, 275, 285, 385, 675 and 685:

| rows | phases (b, u, v) with a nonzero count | count in each such phase | pi | count with the other pi |
| --- | --- | ---: | --- | ---: |
| old, all seven | all eight | a * 2^49 | u | 0 |
| new 185, 285, 385, 685 | u XOR v = 1 | a * 2^47 | u XOR 1 | 0 |
| new 175, 275, 675 | u XOR v = 1 and b = 1 | a * 2^47 | u XOR 1 | 0 |

Every other cell has count 0. Every joint root adds at least 1 to the cell of its phase and its parity, so a cell of count 0 holds no root at all: (P*) holds for every joint root of the fourteen outcomes on the whole class, pointwise and not on average, and it drops no member and no root. The cells add up to the fourteen N3_j of 10.1 exactly: 8 * a * 2^49 = a * 2^52 on the old rows, 4 * a * 2^47 on the new rows 185, 285, 385 and 685, and 2 * a * 2^47 on the new rows 175, 275 and 675 (checked by a helper agent of the participant). In the phase b = 1, u = 0, v = 1, the 2^16 members of the class with e1 AND 07ef8307 = 070c0307, a separate exact count of a helper agent of the participant, with the function N3_count of the counting program of Section 17 and the parity as one more condition, gives all fourteen counts with pi = 0 on the old rows, pi = 1 on the new rows and the count 0 with the other pi, as the table says. The cells of the other seven phases are GPT Sol's evaluation and were not re-run by the participant. The count shows as well that a new row has no joint root when u = v, and a new row 175, 275 or 675 none when b = 0; the search of this package lists no new row.
*The guard on the third addition.*
**Lemma J0.** Every joint root h of every one of the seven outcomes has h2[0] = 0, that is h[8] = e2[8].
Proof. For all seven outcomes tau_j[0] = tau_j[1] = 0, theta_j[0] = theta_j[1] = 1 and gamma[1] = gamma[2] = 0, and mu[0] = 1, mu[1] = 0. By (PHASE) h[0] = 0 and h[1] = 1. In (J1) both carries into bit 0 are 0. Since eta[0] = eta[1] = 1 and gamma[1] = 0, the carry Q[0] AND (h[0] XOR 1) = Q[0] of the second addition into bit 1 must equal the carry Q[0] AND h[0] = 0 of the first, so Q[0] = 0 and g[0] = 0; since gamma[2] = 0, the carry maj(Q[1], 0, 0) = 0 of the second addition into bit 2 must equal the carry maj(Q[1], 1, 0) = Q[1] of the first, so Q[1] = 0 and g[1] = 1. Both additions of (J3) have carry 0 into bit 0. At bit 0, g + h2 adds 0 and h2[0], with sum bit h2[0] and carry 0 out; (g XOR theta) + (h2 XOR mu) adds 1 and h2[0] XOR 1, with sum bit h2[0] and carry 1 XOR h2[0] out. At bit 1, g + h2 adds 1, h2[1] and 0, with sum bit 1 XOR h2[1]; the other adds g[1] XOR theta[1] = 0, h2[1] XOR mu[1] = h2[1] and 1 XOR h2[0], with sum bit h2[1] XOR 1 XOR h2[0]. (J3) at bit 1 requires the XOR of the two sum bits, which is h2[0], to be tau_j[1] = 0. So h2[0] = 0, and h2[0] is bit 8 of h XOR e2. QED. The zero carries into bit 0 are those of addition modulo 2^32; nothing is guessed. The participant checked the bits that the proof reads for all fourteen outcomes of beta* on the class, the six of S among them. e2[8] is produced at position i = 20 of the traversal (k = 8): e2[8] = E[8] XOR f[8] XOR a[8] with f[8] = y[20] XOR Q[20] XOR h[20] XOR u[20], and every term but h[20] is known when position 20 is reached, h[8] among them. So Lemma J0 is a forward guard that sets h[20] = h[8] XOR E[8] XOR a[8] XOR y[20] XOR Q[20] XOR u[20]. It holds for every joint root, so no root is lost, and position 20, which no constant and no carry prescribes on any row, is no longer free.
*The constants and guards of an outcome.* For y in the class, every joint root of outcome j has the following values, which the solver computes from Q, y, E and the outcome before it branches, or checks during the traversal. Every member of the class has y[0] = 0, y[1] = 1 and bits 16 to 19 of y equal to 0, 0, 1, 0, so f[20] = f[21] = 0, bits 4 to 7 of f are the constant 2, the carry u[20] is Q[19], and the first addition is reset as in the sub-class. (a) *The carry into bit 22.* For each guess a[20] = 0 and a[20] = 1, with a'[20] = a[20] XOR kappa[20], run bits 20 and 21 of both additions of (J2) with f[20] = f[21] = 0, and keep the guess only if a'[21] = a[21] XOR kappa[21] and a'[22] = a[22] XOR kappa[22]. If no guess is kept, the outcome has no joint root. Two kept guesses have the same carries into bit 21, and so into bit 22: all seven outcomes have sigma[20] = sigma[21] = 1, eps[20] = 0 and eps[21] = 1, and the cases E[20] = E'[20], E[20] = 0 with E'[20] = 1, and E[20] = 1 with E'[20] = 0 give, in turn, at most one guess that passes bit 21, equal carries into bit 21 for both guesses, and at most one guess that passes bit 22. Write a[22] for the common carry. (b) f[22] is its prescription (D[22] = 1). If gamma[3] = 0, then D[23] = 1 and f[23] is its prescription; if gamma[3] = 1, f[23] = 1 XOR Q[3] XOR y[3]. Run bits 22 and 23 of (J2); if a'[23] is not a[23] XOR kappa[23] or a'[24] is not a[24] XOR kappa[24], the outcome has no joint root. This gives a[24]. (c) h[0] = 0, h[1] = 1 and u[2] = 0; h[2] = y[2] XOR f[22] XOR Q[2], and the outcome has no joint root unless h[2] = 1 XOR b; u[3] = maj(h[2], Q[2], 0); h[3] = y[3] XOR f[23] XOR Q[3] XOR u[3] and u[4] = maj(h[3], Q[3], u[3]); h[10] = b and h[11] = 1 XOR h[3]; u[11] = maj(h[10], Q[10], Q[9]) if gamma[10] = 0 and u[11] = Q[10] if gamma[10] = 1; u[12] = maj(h[11], Q[11], u[11]). (d) f[0] is its prescription with a[0] = 0 (D[0] = 1), and a[1] = maj(E[0], f[0], 0); h[12] = y[12] XOR f[0] XOR Q[12] XOR u[12], u[13] = maj(h[12], Q[12], u[12]) and h[24] = h[3] XOR h[12] XOR u. (e) Bit 16 of h2 is 0, so f[24] = h[24] XOR E[24] XOR a[24]; h[4] = y[4] XOR f[24] XOR Q[4] XOR u[4] and u[5] = maj(h[4], Q[4], u[4]). Run bit 24 of (J2); if a'[25] is not a[25] XOR kappa[25], the outcome has no joint root. f[25] is its prescription (D[25] = 1), a[26] = maj(E[25], f[25], a[25]) and h[5] = y[5] XOR f[25] XOR Q[5] XOR u[5]. (f) Bits 6, 13, 25 and 26 depend on the kind of the outcome; (P*) is used on every row. The outcomes of S are old rows of two kinds (675020a0, an old row that this search does not list, is described with them).

- *Low old rows, 175020a0, 275020a0 and 675020a0:* if E[1] = a[1], the carry into bit 2 is E[1], f[2] is its prescription (D[2]
  = 1) and e2[2] = E[2] XOR f[2] XOR E[1]; otherwise the outcome has no joint root if kappa[2] = 1, and e2[2] = E[2] XOR
  kappa[3] if kappa[2] = 0. Then h[26] = 1 XOR h[2] XOR e2[2] XOR Q[26] XOR Q[25], f[26] = h[26] XOR E[26] XOR a[26] and h[6] =
  f[26] XOR y[6] XOR gamma[7]. By (P*), h[25] = h[6] XOR h[13] XOR u: a forward guard, set once bit 13 of h is chosen.
- *High old rows, 185020a0, 285020a0, 385020a0 and 685020a0:* h[25] = e2[1], where e2[1] = E[1] XOR f[1] XOR a[1]
  and f[1] = y[13] XOR Q[13] XOR h[13] XOR u[13]. With (P*), h[6] = h[13] XOR h[25] XOR u = y[13] XOR Q[13] XOR u[13] XOR E[1] XOR
  a[1] XOR u, in which h[13] cancels: h[6] is fixed by (c) and (d), which give u[13] and a[1]. The guard of position 25 is then
  h[25] = h[6] XOR h[13] XOR u, the same as h[25] = e2[1]. h[26] = e2[26] (bit 18 of h2 is 0), and e2[26] is given by position 6,
  whose value is now fixed, so h[26] is a constant of the row.
(g) h[16] = h[17] = 0, h[18] = 1 XOR Q[18], h[19] = Q[19], and, if gamma[7] = 1, h[7] = 1 XOR gamma[8] XOR h[6], now a constant on every row.
On every row h[29] = 1 XOR e2[29] (bit 21 of h2 is 1), where e2[29] is known once bit 9 of h is chosen, and h[20] is set by Lemma J0. These are the *constants and guards* of the outcome. On every row h[0] to h[6] are fixed before the traversal; the guards that read bits chosen during the traversal are those of position 20 (every row), position 25 (the old rows) and position 29 (every row). In entry 26ebba63 the parity h[25] = h[6] XOR h[13] was a condition of rule A on the sub-class; here (P*) is not a rule but a consequence of the count of the class, true of every joint root.
*One traversal.* Every carry guess a[20] that (a) keeps reaches, after the constants h[0] to h[6], the same state: the same bits h[0] to h[6], the same carries u[7] and a[27], and the same e2[26]; the values e2[20] and e2[21], which depend on the guess, are not used by any guard. So the solver walks bits 0 to 6 under both kept guesses with the tests of (a), (b) and (e), then drops the guesses and starts one depth-first traversal for each searched outcome at depth 7 from that state, and checks (J1), (J2) and (J3) as words at each leaf, which enforces the closure of the carries that the guess stood for. Every joint root survives a guess and reaches this common state, and a single traversal over the bits of h reaches every h at most once.
*Transitions.* For each position i = 7, .., 31, with k = (i + 20) mod 32, each pair (u[i], a[k]) of incoming carries and each value v of h[i], put g[i] = Q[i] XOR v XOR u[i], u[i+1] = maj(Q[i], v, u[i]) and u'[i+1] = maj(Q[i], v XOR eta[i], u[i] XOR gamma[i]), and require u'[i+1] = u[i+1] XOR gamma[i+1] if i < 31; put f[k] = y[i] XOR g[i], e2[k] = E[k] XOR f[k] XOR a[k], a[k+1] = maj(E[k], f[k], a[k]) and a'[k+1] = maj(E'[k], f[k] XOR sigma[k], a[k] XOR kappa[k]), and require a'[k+1] = a[k+1] XOR kappa[k+1] if k < 31. A value that passes is an arc to the pair (u[i+1], a[k+1]), or to (u[i+1], 0) if k = 31, since both carries into bit 0 of (J2) are 0 (kappa[0] = 0: E'[0] differs from E[0], eps[0] = 1 and sigma[0] = 0 for all seven outcomes); the arc records v and e2[k]. The *descriptor* of a position is 14 bits: Q[i], y[i], E[k], E'[k], eta[i], gamma[i], sigma[k], kappa[k], gamma[i+1], kappa[k+1], whether the position has a constant and its value, and whether i = 31 and k = 31. The solver reads the arcs from three arrays built once per run, each entry computed by the relation above, which is the same relation and not an approximation; an arc is five bits: validity (bit 4), next carry pair (bits 3 and 2), h[i] (bit 1), e2[k] (bit 0). Each array is packed eight entries to a word of 256 bits, one per 32-bit field: the word is addressed by the 11 descriptor bits other than eta[i], gamma[i] and gamma[i+1], then the carry pair (and the desired bit), and the entry is its field j = 4 eta[i] + 2 gamma[i] + gamma[i+1], a constant of the position and the row; the solver takes the bits of the entry out of the loaded word by constant masks and shifts:

| array | key | words | entry |
| --- | --- | ---: | --- |
| forced | descriptor and carry pair | 2^13 | the one passing arc, or invalid |
| dual | descriptor and carry pair | 2^13 | both arcs, in ten bits of the field |
| selected | descriptor, carry pair and a desired bit | 2^14 | the passing arc whose e2[k] is the desired bit, or invalid |

A position with a constant reads the forced array with the constant in its descriptor. A position i < 31 with gamma[i] = 1, or with k < 31 and D[k] = 1, has at most one passing value by Lemma S5 and reads the forced array as well. A position with a guard on bits chosen during the traversal, 25 on the old rows and 29 on every row, reads the forced array with the value of the guard written into the constant field of its key: 1 XOR e2[29], from the saved bit e2[29], and h[6] XOR h[13] XOR u, from bit 13 of the prefix of h. Position 20 reads the selected array with the desired bit h[8] (Lemma J0); as e2[8] changes with h[20], at most one arc has it. A free position (below) reads the dual array. So a position that is not free has at most one child.
*The search.* From the common state at depth 7, search depth first over the positions 7 to 31: a node at depth d has a child at depth d + 1 for each arc of position d from its carry pair that meets the guards of the position. A node at depth 32 is a *leaf*; it gives a root when its h satisfies (J1), (J2) and (J3) as words. The root is returned with the outcome j.
*Counts.* Call a position i >= 7 *free* when it has no constant and no guard, gamma[i] = 0 or i = 31, and D[(i + 20) mod 32] = 0, and *prescribed* otherwise. For a row with the set F of free positions put n_i = 2^(the number of free positions p with 7 <= p < i), for i = 7, .., 32. A traversal of the row has at most n_i nodes at depth i: at most the sum of n_i over the prescribed positions *forced* nodes, the sum over the free positions *free* nodes, n_20 *selected* nodes among the forced ones (position 20 is prescribed on every row, by Lemma J0), and n_32 = 2^|F| leaves (GPT Sol, answer AR 6.5; recomputed by the participant from the free positions):

| tau | free positions | forced nodes | free nodes | selected nodes | leaves |
| --- | --- | ---: | ---: | ---: | ---: |
| 175020a0 | 7, 13, 15, 30 | 142 | 15 | 8 | 16 |
| 185020a0 | 13, 15, 30 | 72 | 7 | 4 | 8 |
| 275020a0 | 9, 13, 15, 30 | 140 | 15 | 8 | 16 |
| 285020a0 | 7, 9, 13, 15, 30 | 278 | 31 | 16 | 32 |
| 385020a0 | 9, 13, 15, 30 | 140 | 15 | 8 | 16 |
| 675020a0 | 13, 15, 30 | 72 | 7 | 4 | 8 |
| 685020a0 | 7, 13, 15, 30 | 142 | 15 | 8 | 16 |

These are counts of the static trees: an arc that fails a carry test or a guard only removes nodes, and the trees that occur may be smaller. The row 675020a0 is not in S: its line is kept as proved, and this search does not build its tree.
*The trees with the guard (G7).* The guard (G7) of 9.7 fixes position 7 on every row before the traversal, so with it position 7 is free on no row. The rows 175020a0, 285020a0 and 685020a0 lose the free position 7 that the table gives them: with (G7) they have 72, 140 and 72 forced nodes, 7, 15 and 7 free nodes, 4, 8 and 4 selected nodes and 8, 16 and 8 leaves, and the other rows of S are unchanged. These trees with (G7) are those of our entry 0bc5f130; the table above is that of the solver without (G7).
*The trees with the guards (G7) and (G15).* The guard (G15) of 9.7 prescribes position 15, which is free on every row of S with (G7). With both guards the rows 175020a0, 185020a0 and 685020a0 have the free positions 13 and 30, 42 forced nodes, 3 free nodes, 2 selected nodes, 2 nodes at position 15 and 4 leaves, and the rows 275020a0, 285020a0 and 385020a0 the free positions 9, 13 and 30, 80 forced nodes, 7 free nodes, 4 selected nodes, 4 nodes at position 15 and 8 leaves (the counts of the table's rule; a node at position 15 is a forced node). These trees with (G7) and (G15) are the trees of the solver of this package.
The outcomes searched in an outer step that reaches the solver have their bits set in T, a subset of the mask of Y9 under (1) and of S. By the certificate of Section 8 every nonzero mask under (1) is one of the twelve nonzero seven-bit masks of its table, and each of these is a subset of {275020a0}, {175020a0, 675020a0}, {285020a0, 385020a0} or {185020a0, 385020a0, 685020a0}. So the searched outcomes are among the rows of one of these four sets restricted to S: {275020a0}, {175020a0}, {285020a0, 385020a0} and {185020a0, 385020a0, 685020a0}. With (G7) alone they have (140, 15, 8), (72, 7, 4), (280, 30, 16) and (284, 29, 16) forced, free and selected nodes and 16, 8, 32 and 32 leaves. With (G7) and (G15), in the solver of this package, they have (80, 7, 4), (42, 3, 2), (160, 14, 8) and (164, 13, 8) forced, free and selected nodes, 4, 2, 8 and 8 nodes at position 15, and 8, 4, 16 and 16 leaves. A leaf gives at most one root. So an outer step has at most 3 searched outcomes, 16 leaves and 16 roots, whatever its words.
*Families.* Within one of the four sets the rows fall into *families* by two marks: low row (175, 275, 675) or high row (185, 285, 385, 685), and the bit gamma[10] (on the class the new rows, which this search does not list, would form families of their own). gamma[3] is 0 on the low rows and 1 on the high rows, gamma[10] is 1 on the rows 675 and 685 and 0 on the others, and sigma[20] to sigma[26] and sigma[0] to sigma[3] are the same on all low rows and on all high rows; gamma[10] fixes the reset of u[11] in (c). So the formulas of (a) to (e) and the walks of bits 0 to 5 under both guesses are the same for the rows of a family and are evaluated once per family. Restricted to S the four sets have 1, 1, 1 and 2 families, and at most two rows of a set share a family. gamma[7] can differ within a family, so bit 6 and its outgoing carries, h[6], h[7] and h[26] are computed for each row: no prefix of seven bits is shared.
*What is proved and by whom.* The phase equations, the guards of (c), (d) and (e), the single traversal and the common state are GPT Sol's, on the constants of answers AE 2.1, AF 1.2 to 1.4 and AN 6 and the transition relation of answer AI 1; the parity certificate (P*), Lemma J0, the guards of (f) with (P*), the three arrays, the families and the counts of the static trees are GPT Sol's answer AR (1, 2 and 6.1 to 6.5); the restriction of the solver to the outcomes of S, with the four sets above, is its answer AW 2, the same solver visiting only the outcomes of T, with the same proofs; the guard (G7), with its trees above, is its answer AX 1; and the guard (G15), with its trees above, is its answer CF 7, with the row-set caps of Section 11, which Lemma FX of 9.7 lowers. The participant recomputed the free positions, the node, leaf and selected counts of the table and of the four sets, the families, the bits that Lemma J0 reads, and the sums of the parity certificate against the counts of 10.1; the other constants and guards were not re-derived by the participant. At positions 25 and 29 the guard selects the candidate before the table read (GPT Sol's corrected answer AR 6.3): these positions are not prescribed by the carries, so the value of the guard is written into the key before the read, within the same allowance and the same proved cap (Section 11). Lemma CV (10.2) states what the solver returns. The layout is specified and charged by this text; it is not an implementation (9.5).
**9.5 Checks of the joint solver.** The solver of 9.4 with the guards (G7) and (G15), the certificate of step 3, and the pre-check, the preflight and the meter of 9.7 are executed by the declared program (9.2) on every passing outer step of its trials, with each solver call repeated by the traversal without (G15) and planted joint roots returned by both; no root of the search itself occurs at that scale. The completeness of the solver rests on the proofs cited in 9.4, on Lemmas G7, G15 and RC, on the count of the class and on the parity certificate; its cap of 15,012 machine units rests on the schedule of Section 11 and on Lemma FX, an upper allowance written out block by block, which the program checks against its own count of nodes on every call, as it checks the metered debit against Lemma ME; and the pre-check rests on Lemma VP, whose bit identity was checked on real trials (9.7).
**9.6 Packed words and the shortcut of a passing lane (GPT Sol, answer AQ; our audit).** The walk of 9.8 and Section 11 use the packed words of 6.5, lane i being bits 36 i to 36 i + 35 of a word. The low 32 bits of a lane are the scalar value modulo 2^32, and every lane of every sum stays below 2^36, so that no carry leaves its lane; where an interval bound of a sum could reach 2^36, an AND with the word M that has the low 32 bits of every lane set is made first, and charged. x - z is formed as x + (z XOR M) + 1, never by a packed subtraction, whose borrows could cross lanes. A rotation by r is PROR: ((x >> r) AND A_r) OR ((x << (32 - r)) AND B_r), five operations, with A_r and B_r the masks of its two parts in every lane; since A_r and B_r keep only bits that come from the low 32 bits of the same lane, PROR gives in the low 32 bits of each lane the rotation of the low 32 bits of that lane, whatever its guard bits. On packed words an XOR, an OR and an AND with a constant act on each bit, and an addition acts on each lane separately while no lane reaches 2^36. The addition of a constant is kept pending until the value is read by an XOR, an OR, a shift, a rotation or a table index, and the one addition that then forms it is charged. All interval bounds depend on the lines and the constants only, not on the words.
*The shortcut of a passing lane.* A passing lane needs, for the pre-check of 9.7, only bit 18 of Q = Y9, e1, C2.c1 and C2.b1, and the source bank of steps 2 and 3 needs C2.a1 and C2.d1 as well (Section 11). The lines X12 = ROL(C0.d1, 16) XOR C0.a1, D1.c1 = X11 - X12, D1.b1 = ROR(S6 XOR D1.c1, 12), X6 = ROR(D1.b1 XOR X11, 7), C2.a1 = X2 + X6 + w7, C2.d1 = ROR(X14 XOR C2.a1, 16), D0.c1 = S10 + D0.d1, X10 = D0.c1 + X15, C2.c1 = X10 + C2.d1 and C2.b1 = ROR(X6 XOR C2.c1, 12) of step CO read, besides constants, only C0.a1 and D0.d1, which the cache of the batch holds packed (9.8), the packed operands ROL(C0.d1, 16) and S10, and the names S6, X14 and X2 + w7, which the context holds in three registers. The rotations run on scalar words, at four units each (two shifts, an OR and a mask, Section 11), and the two of D1.b1 and X6 are one: a rotation commutes with an XOR, so X6 = ROR(ROR(S6 XOR D1.c1, 12) XOR X11, 7) = ROR(S6 XOR D1.c1, 19) XOR ROR(X11, 7), with ROR(X11, 7) an immediate, and D1.b1 has no other use in the lane. On the machine of Section 11: X12, the XOR of the packed words and the shift of lane i out, 2; D1.c1 = (X12 XOR M) + (X11 + 1), masked, 3, since X11 - x = (2^32 - 1 - x) + X11 + 1 modulo 2^32 and the bits of X12 above its low 32 do not reach them; X6, the XOR with S6, the rotation by 19 and the XOR with the immediate, 6; C2.a1, 2; C2.d1, the XOR and the rotation, 5; X10 = (lane i of D0d1 + S10) + X15, masked, 4; C2.c1, 2; C2.b1, the XOR and the rotation, 5; e1 out of lane i of E[b], 2; and r' = (((Y9' >> (36 i + 16)) XOR e1) AND 4) XOR 3, the word of the pre-check (9.7), 4: 35 units, 32 for lane 0, which needs three shifts fewer. The rotation tables of the earlier layout (Grok, jobs 58 and 59; GPT Luna 5.6, answer D25) are not used, and no table is read by the shortcut. Every value is the scalar value of step CO for the outer step of the lane: the low 32 bits of each lane of C0a1 and D0d1 are C0.a1 and D0.d1 (Lemma MB), and every line is evaluated modulo 2^32. The lane uses at most six temporaries. W and the credit live in registers for the whole run, and the lane neither stores nor reloads them (9.8).
**9.7 The s-pattern pre-check with the guards (G7) and (G15), and the credit of the solver (GPT Sol, answers AW 1, 2 and 5, AX 1, CF 7 and CD 10; a helper agent of the participant found the pre-check).** Fix a passing outer step, with mask X, and write Q = Y9, e1 = Y3 + y and, for a trial of it, s = E1.b1 AND beta*. By the lines of step CT read backwards, Y14 = ROL(E3.h1, 16) XOR e1, Y10 = Y14 + C2.c1, Y6 = ROR(Y10 XOR C2.b1, 7) and E1.b1 = ROR(Y6 XOR c1, 12), so for each bit p of beta*
    s[p] = Z[(p + 19) mod 32] XOR c1[(p + 12) mod 32],   Z = (Y14 + C2.c1) XOR C2.b1.
At p = 13, 14 and 15 the bits of c1 are fixed by Q* (c1 AND 0e09818b = 0c008000), with the values 1, 0 and 0, and the bits of Z are 0, 1 and 2. Every joint root h has h[16] = h[17] = 0 and h[18] = 1 XOR Q[18] ((PHASE) and (g) of 9.4), and every member of the class has e1[0] = e1[1] = 1. So when E3.h1 is a joint root the low three bits of Y14 are 1, 1 and 1 XOR Q[18] XOR e1[2], and the number nu = s[13] + 2 s[14] + 4 s[15] is a function of the outer step:
    r  = (((Q >> 16) XOR e1) AND 4) XOR 7,
    nu = (((r + C2.c1) XOR C2.b1) XOR 1) AND 7.                          (V)
r is exactly the low three bits of Y14 at a joint root. The identity is used only at joint roots; it says nothing of the other trials of the outer step.
*The allowed values.* For an outcome j of beta*, a pattern s is compatible when E1 can give the differences beta*, tau_j and eps with that s. With Delta(s) = beta* - 2 s - 8 modulo 2^32, the relation a XOR (a + Delta) = tau has a solution exactly when d = (tau - Delta) mod 2^32 is even and d / 2 has no bit outside tau, since a XOR tau - a = tau - 2 (a AND tau) modulo 2^32 and tau[31] = 0. GPT Sol enumerated the 2,048 submasks of beta* with this exact criterion for the fourteen outcomes:

| rows | compatible s, rows 175, 185, 275, 285, 385, 675, 685 | allowed nu |
| --- | --- | --- |
| old, tau ending in 20a0 | 16, 32, 8, 16, 32, 8, 16 | 3, 4 |
| new, tau ending in 60a0 | 32, 64, 16, 32, 64, 16, 32 | 2, 3, 4, 5 |

Every compatible s has s[3] = s[4] = 1. In the order (s[13], s[14], s[15]), nu = 3 is 110 and nu = 4 is 001. As a table over the fourteen outcomes, bit j - 1 for outcome j, VMASK = [0, 0, 3f80, 3fff, 3fff, 3f80, 0, 0] for nu = 0 to 7. Every outcome of S is an old row, so for this search T = X AND VMASK[nu] is X when nu is 3 or 4 and empty otherwise. A helper agent of the participant found the same allowed values from the exact E1 counts L_j split by s (the function L_count of the counting program of Section 17): 16, 32, 8, 16, 32, 8 and 16 patterns with a nonzero count on the old rows, each with nu = 3 or nu = 4, half of the count of the row on each, and every row sum equal to its L_j of 10.1.
**Lemma VP (the pre-check is lossless).** Fix a passing outer step with mask X and let nu be given by (V). Every listed good trial of the outer step has its outcome in T = X AND VMASK[nu]. So an outer step or an outcome that the pre-check skips holds no listed good trial, and the count N_o of H1' of every outer step is the same, pointwise, as without the pre-check.
Proof. Let a listed good trial have outcome j in S and E3.h1 = h. By the proof of Lemma F, bit j - 1 is set in both masks, so j is in X; by Lemma V, h is a joint root of outcome j. By (PHASE) and (g) of 9.4, h[16] = h[17] = 0 and h[18] = 1 XOR Q[18], and e1[0] = e1[1] = 1 for every member, so by the identity above the bits s[13], s[14] and s[15] of the trial are those of nu. The trial's E1 gives beta*, tau_j and eps, so its s is compatible with outcome j, and by the enumeration above nu is allowed for j: VMASK[nu] has bit j - 1. So j is in T. QED. The lemma uses no law of the words. It says which outcomes a passing outer step can hold; it does not say how often nu takes a value, which enters only the credit (H5_exec).
*The charge.* On a passing lane, e1, C2.c1 and C2.b1 come from the shortcut of 9.6, and bit 18 of Q from the cached Y9. Every outcome of S is an old row, so VMASK[nu] AND S is S for nu = 3 and 4 and 0 otherwise, and T is X or 0 with no table. For u = (Y9' >> (36 i + 16)) XOR e1 the bit 2 is Q[18] XOR e1[2], since the bit 2^34 of Y9' and the lanes above do not reach it; r' = (u AND 4) XOR 3 is r + 4 modulo 8, with r of (V), and an addition of 4 modulo 8 changes bit 2 only, which commutes with the XORs; so with w = (r' + C2.c1) XOR C2.b1, nu = (w XOR 5) AND 7, and ((w XOR 5) + 5) AND 6 = 0 exactly when nu is 3 or 4 (a check over the eight values of w modulo 8). The four operations of r' are in the shortcut; the pre-check is the addition of C2.c1, the XOR of C2.b1, the XOR with 5, the addition of 5, the AND with 6, the comparison with zero and the branch: 7 units, inside the 35 of the lane (Section 11), paid by every passing lane, also when T is empty; a nonzero result adds u_P to W and ends the outer step, and a zero one adds u_P + u_C and falls through to the preflight. The pre-check never enlarges T, so the cap of 9.4 holds for every T.
*Guard (G7), GPT Sol's answer AX 1, as used in our entry 0bc5f130.* Every compatible s has s[3] = s[4] = 1 (above). At p = 3 and p = 4 the bits of c1 that Q* fixes are 1 and 0 and the bits of Z are 22 and 23, so s[3] = Z[22] XOR 1 and s[4] = Z[23]: every listed good trial has Z[22] = 0 and Z[23] = 1. Write C = C2.c1, B = C2.b1, and a22 and a23 for the carries into bits 22 and 23 of Y14 + C. Bit 22 of Y14 = ROL(h, 16) XOR e1 is x = h[6] XOR e1[22], and bit 23 is h[7] XOR e1[23]. The two required sum bits give
    a22  = x XOR C[22] XOR B[22],
    a23  = maj(x, C[22], a22),
    h[7] = e1[23] XOR 1 XOR C[23] XOR B[23] XOR a23.                     (G7)
**Lemma G7.** Let a listed good trial of an outer step have outcome j and E3.h1 = h. Then h[7] is the value that (G7) gives from h[6], e1, C2.c1 and C2.b1.
Proof. The trial's E1 gives beta*, tau_j and eps, so its s is compatible with outcome j and s[3] = s[4] = 1 by the enumeration above; that is, Z[22] = 0 and Z[23] = 1 with Z = (Y14 + C) XOR B. Bit 22 of Y14 + C is x XOR C[22] XOR a22, and it equals Z[22] XOR B[22] = B[22]; this gives a22. The carry out of bit 22 is a23 = maj(x, C[22], a22). Bit 23 of Y14 + C is h[7] XOR e1[23] XOR C[23] XOR a23, and it equals Z[23] XOR B[23] = 1 XOR B[23]; this gives h[7]. QED. The unknown carry a22 is fixed by the required bit 22 and need not be computed from the lower 22 bits; a trial whose true carry differs is not a success, and the E1 test of step 3 would reject it. The lemma uses no law of the words.
*Use in the solver.* h[6] is fixed on every row before the traversal (9.4), so after it the solver computes h[7] by (G7) for each searched row. On a row on which position 7 is otherwise free, it becomes prescribed with that value; on a row on which h[7] is already a constant ((g) of 9.4), the row is dropped for this outer step when the two values differ. By Lemma G7 no listed good trial is lost; joint roots that would fail the E1 test of step 3 may be dropped early, so the solver returns the joint roots of the outcomes of T that satisfy (G7), and these contain the root of every listed good trial (Lemma CV). Position 7 is then free on no row (the trees with (G7) of 9.4). h[7] is computed after the row's own patch of h[6] and is never shared across a family.
*The charge of (G7).* 128 more units for each searched row: the six source bits e1[22], e1[23], C[22], C[23], B[22] and B[23], the loads and addresses of the three source words, x, the carry a22, the majority, h[7], the comparison with an existing constant and its branch, and the insertion of the value into the descriptor of position 7, fewer than 16 blocks of at most 8 units; the scratch words are released before the 32 descriptors are resident, so the traversal uses no more registers. (G7) and (G15) load e1, C2.b1 and C2.c1 from the bank of the global ledger, which stores them before any row (Section 11); the caller stores nothing. The extra prescribed bit of the written-out rows is inside the once-only allowance. (G7) adds no budget and no premise of its own: its work is inside the 1,354 of each row, which the meter debits with A(T) before (G7) runs.
*Guard (G15), GPT Sol's answers CF 7 and CD 10.* Write C = C2.c1, B = C2.b1, V = Y12 and A = (Y1 + w12) mod 2^32, so that Z = (Y14 + C) XOR B, Y6 = ROR(Z, 7), E1.a1 = Y6 + A, E1.d1 = ROR(E1.a1 XOR V, 16) and c1 = Y11 + E1.d1 (step CT), with Y11 = 84f77f38, whose bit 0 is 0. Let a22 be the carry into bit 22 of Y14 + C, as in (G7), and v16 the carry into bit 16 of Y6 + A, and put
    a22 = h[6] XOR e1[22] XOR C[22] XOR B[22],
    v16 = V[16] XOR 1 XOR A[16].
For the prefix H of the bits h[0] to h[14] of a node at position 15 (its higher bits zero), with all words of 32 bits:
    L     = (H >> 6) XOR (e1 >> 22),
    zeta  = (((L + (C >> 22) + a22) XOR (B >> 22)) >> 1) AND 1ff,
    p15   = (zeta + ((A >> 16) AND 1ff) + v16) AND 1ff,
    cstar = (Y11 AND 1ff) + (p15 XOR ((V >> 16) AND 1ff)),
    (G15)  cstar AND 08b = 0  and  h[15] = bit 8 of cstar.
**Lemma G15.** Let a listed good trial of an outer step have outcome j and E3.h1 = h. Then h satisfies (G15).
Proof. The trial has Z[22] = 0 and Z[23] = 1 (proof of Lemma G7) and c1 in Q*, so c1[0] = c1[1] = c1[3] = c1[7] = c1[8] = 0 (the mask 0e09818b and the value 0c008000). Bit 22 of Y14 + C is h[6] XOR e1[22] XOR C[22] XOR a22 and equals Z[22] XOR B[22] = B[22], which gives a22. c1[0] = 0 and Y11[0] = 0 give E1.d1[0] = 0, that is E1.a1[16] = V[16]; Y6[16] = Z[23] = 1; and bit 16 of Y6 + A is 1 XOR A[16] XOR v16 = V[16], which gives v16. Bits 22 to 31 of Y14 = ROL(h, 16) XOR e1 are h[6] to h[15] XOR e1[22] to e1[31], which are L when h[15] = 0. Adding C[22..31] with the carry a22 and XORing B[22..31] gives Z[22..31], and the shift drops Z[22]: zeta is Z[23..31] = Y6[16..24]. Adding A[16..24] with the carry v16 gives E1.a1[16..24], so p15 XOR V[16..24] is E1.d1[0..8], and adding Y11[0..8] with no carry into bit 0 gives c1[0..8]. So the low nine bits of cstar are c1[0..8] of the trial with h[15] set to 0. Changing h[15] alone flips Y14[31], hence Z[31], Y6[24], E1.a1[24], E1.d1[8] and c1[8], and no lower bit of these words. As c1[0] = c1[1] = c1[3] = c1[7] = 0, cstar AND 08b = 0; as c1[8] = 0, h[15] = bit 8 of cstar. QED. The carries a22 and v16 are those of a listed good trial: a word whose true carries differ is not a success, and step 3 still tests every root in full (Lemma RC). The lemma uses no law of the words.
*Use in the solver.* For each searched row, after (G7), the solver stores five words in fixed memory: e1 >> 22, (C >> 22) + a22, B
>> 22, ((A >> 16) AND 1ff) + v16 and (V >> 16) AND 1ff; a22 needs h[6], fixed on the row. At each node of position 15 it computes
cstar from the prefix of the node, drops the prefix when cstar AND 08b is not 0, and otherwise prescribes h[15] = bit 8 of cstar in a temporary copy of the descriptor of position 15, which the forced transition array then reads; the stored descriptor is not changed, since another prefix may need the other value. Position 15 is then free on no row (the trees with (G15) of 9.4). By Lemma G15 no listed good trial is lost; the solver returns the joint roots of the outcomes of T that satisfy (G7) and (G15) (Lemma CV).
*The charge of (G15) (GPT Sol, answer CF 7.2; charged at its itemized 74, Grok, jobs 58 and 59, and GPT Luna 5.6, answer D25).* 74 more units for each searched row, for its five words: the loads and addresses of their sources, at most 24; the additions, masks, shifts and the two carries, at most 24; five stores with their addresses, 10; row control and addresses, 16: 74. 64 more units at each node of position 15, besides its 20 as a forced node: five loads with their addresses, 10; the shift, XOR, addition, XOR, shift and AND of zeta, 6; the addition, AND, XOR and addition of p15 and cstar, 4; the test of cstar AND 08b and its branch, 3; bit 8 taken out and the temporary key patched, at most 6; copies and control, at most 16: 45. It uses the ten temporaries of the traversal and spills nothing (Section 11). Its code, the layout of the five words and the updated CT are inside one more once-only allowance of 2^20 (Section 11).
*The metered credit.* For a nonempty subset T of S, with r rows and F families (9.4; 175020a0 and 275020a0 never occur together and count as two), A(T) = 614 + 2,304 F + 1,354 r is the part of steps 2 and 3 paid once per call and per row, 614 the global ledger of Section 11. For one call, the *ledger* U is A(T) + 20 n_f + 48 n_d + 4 n_20 + 64 n_15 + 80 n_l + 120 n_o, with n_f, n_d, n_20, n_15, n_l and n_o the forced, free, selected and position-15 nodes, leaves and roots that the call executes, each at its unit cost of Section 11; U = 0 when T is empty. The ledger with the global part of 1,024 of the earlier layout, U0 = U + 410 when T is not empty and 0 otherwise, is the ledger of the earlier layout, on which the bound of model M is stated (10.3); the ledger of H5_exec is U.
**Lemma FX (one row per family; GPT-6 Astra, Batch 17).** In every call at most one row of each family of T reaches depth 7: the setup of 9.4 with (G7) drops every other row of the family.
Proof. Restricted to S, a family with two rows of one of the four sets of 9.4 is {185, 385} or {285, 385}; 685 is in the other high family and each low family has one row. For the high rows 185, 285 and 385, gamma[10] = 0 and the bits of sigma that (a) to (e) read agree, so (a) to (e) give them the same h[4], h[5] and u[6], and the high-row formula of (f) gives them the same h[6]. At bit 6 the transition of 9.4 with h[0] to h[6] fixed requires u[6] = Q[6] XOR gamma[7]. For 185 and 385 gamma[7] = 1 for both, and (g) gives h[7] = 1 XOR h[6] on 185 (gamma[8] = 0) and h[7] = h[6] on 385 (gamma[8] = 1); (G7) gives one value of h[7] from their common h[6] and the words of the outer step, so it drops one of the two. For 285 and 385 gamma[7] is 0 and 1, and their common u[6] meets the condition of at most one. QED. The rows of A(T) are still paid for every row of T; only the trees below depth 7 are excluded.
So, with a tree of 1,920 units for a row with four leaves (20 * 42 + 48 * 3 + 4 * 2 + 64 * 2 + 200 * 4) and 3,808 for a row with eight (20 * 80 + 48 * 7 + 4 * 4 + 64 * 4 + 200 * 8), U <= CM(T) = A(T) plus, for each family of T, the largest tree of its rows, in every call: since every executed count is at most the static one of the surviving row and roots are at most leaves. CM(T) = 0 when T is empty. The table CT holds, for each of the 128 values of the seven-bit mask T, the word CM(T) OR (A(T) << 16), both fields below 2^16; it is built once, inside the once-only allowance of Section 11.
**Lemma CP (the cap transfer; GPT Sol, answer D13; GPT Luna 5.6, answer D25).** In every outer step, U = U0 - 410 when T is not empty and U = U0 = 0 otherwise; in every call, U >= 4,272.
Proof. The first statement is the definition of U0 above. A call has a nonempty T, so at least one row and one family, and U >= A(T) = 614 + 2,304 F + 1,354 r >= 614 + 2,304 + 1,354 = 4,272. QED. Both hold pointwise, before any mean is taken, and use no law of the words and no rate of calls.
The remaining credit lives in the 64th register for the whole run: no code of the walk names it (9.8), the traversal uses 63 (Section 11), the credit register is in no saved parent, and the helpers of the leaf, the root and (G15) use only their ten temporaries. *Preflight:* when T is not zero the lane forms the address of CT[T] and loads it (2), takes out A(T) (1), which one subtraction in the global ledger debits (Section 11), takes out CM(T) (1), and compares it with the credit register and branches to the halt when CM(T) exceeds the credit (2): 6 units, the u_C = 6 that the lane adds to W with u_P on this side of the pre-check. *Meter:* every forced, free and root block that the call executes subtracts from the credit register its unit cost in one operation with an immediate operand, the 4 of a selected node and the 64 of a node at position 15 added to the immediate of their forced block, and a forced block at position 31 subtracts, in a second operation, the 80 of the leaf below it when its arc is valid. Every leaf is the child of a node at position 31, and position 31 is forced on every row of S (the trees of 9.4). Each such operation lies inside the unit cost of its block, whose itemized work leaves room for it (Section 11: a forced block does at most 19 units of work of its 20, 14 at position 31, a free block 36 of its 48, a root 113 of its 120); a free block pays for its own two-child control, not for its children; and a leaf block spends its 80 on its work and subtracts nothing. The call therefore debits
    V = A(T) + 20 n_f + 48 n_d + 4 n_20 + 64 n_15 + 80 n_l + 120 n_o = U.
**Lemma ME (the meter).** In every call, whatever its words: (a) V = U <= CM(T) <= 15,012; (b) if the credit before the call is at least CM(T), the credit stays nonnegative throughout the call.
Proof. (a) V = U by the display: every block that the call executes is debited exactly its unit cost, once, by itself or, for a leaf, by its parent at position 31. U <= CM(T) by Lemma FX and the counts above; the largest CM(T) over the T that occur is 15,012, for 185, 385 and 685 (Section 11). (b) The debits of the call are subtractions of positive amounts that add up to V <= CM(T). QED. The lemma uses no law of the words.
An outer step whose CM(T) exceeds the remaining credit halts the run with failure before steps 2 and 3; the failed test is part of the preflight of its lane (Section 11). The credit is a halt like the work register of 9.1, so the time bound depends on no mean: the debits of the run add up to at most CREDIT. Whether the credit suffices is the premise H5_exec (10.3), which bears on the success probability alone. The preflight reserve of 15,012 in CREDIT is needed because the preflight tests the whole metered cap: on the event that the unhalted sum of the debits is at most m_C + t (10.3), the credit left before every call is at least 15,012
>= CM(T), so no preflight fails and the meter loses no trial.
**9.8 The member loop, the direct tables and the omega-first batch.** This subsection defines the walk of step 1 of 9.1. The member loop and the direct tables are those of entry e9b6649e of the participant hecmas, described here in our own words and checked by a separate reimplementation of the participant; the omega-first order of the batch is GPT Sol's answer CA, whose partition, listings, registers and charge the participant derived from the printed lines of step CO and checked by programs (below); the fused line of the Y9 path, the allowance of a context and the layout of a passing lane are GPT Sol's audit of that charge, answer CD (sections 1 and 3), and the E count held in a register, with the frame of a passing lane, is its answer CD (sections 6 and 8.1). The walk uses the packed words, lanes, guard bits and masked rotation PROR of 6.5 and 9.6 and the machine of Section 11. The layout of this row, with the work register W, T1 and T2 at fixed word addresses, the frame in registers and the written-out code, is our audit; keeping the frame words in registers follows entry 73d5265f of the participant 0xshikhar.
*Contexts.* The seven outer words C0.d1, D2.a1, D2.b1, S11, S4, X9 and w6 of step CO together are called a *context*. Fixing a context and a member y of the class fixes an outer step, whose trials are its 2^21 values of c1 in Q* (Section 8). The member loop changes only the order and the grouping in which outer steps are visited; each outer step, with its filter, pre-check, guards (G7) and (G15), solver and certificate, is that of Sections 8 and 9.
**Lemma Y (the lines that read the member).** Call a line of step CO *needed* when Y9 or w8 depends on it, directly or through other lines; 64 of the 77 lines are needed. Call a needed line *member-dependent* when one of its operands is y = Y4 or a member-dependent line. Exactly 25 needed lines are member-dependent; in the order in which step CO prints them, numbered here, they are
     1 to  5:   Y8     Y12    Y0     C0.a1  X0
     6 to 10:   D0.d1  D0.c1  D0.b1  X10    X5
    11 to 15:   X12    D1.c1  D1.d1  X1     C1.a1
    16 to 20:   C1.d1  D1.a1  C1.c1  w10    C1.b1
    21 to 25:   Y1     Y13    Y9     D0.a1  w8
The remaining 39 needed lines, in the same printed order,
     1 to  8:   X2     X8     C0.c1  K3.a1  K3.d1  K3.c1  S15    S3
     9 to 16:   K3.b1  D3.a1  S7     D3.b1  D2.c1  D3.c1  X4     X13
    17 to 24:   X14    C0.b1  D2.d1  D3.d1  S13    S9     K1.c1  K1.d1
    25 to 32:   K1.a1  w2     S14    K1.b1  S10    S5     S1     w3
    33 to 39:   S8     K0.b1  S6     K0.c1  S12    K0.d1  S0
depend on the seven outer words and on constants only. Besides these, omega = Y3 + y + w8 depends on the member.
*Proof.* Both statements are finite checks on the printed text of step CO. Walking the lines in printed order and marking a line when an operand is y or a marked line gives the first list; Y8 is the first line marked. Each line of the second list has as operands only outer words, constants (IV, the six constants of 3.2 and the four constant values of K2) and earlier unmarked lines. Collecting the lines on which Y9 and w8 depend gives the 64. QED. A participant program that parsed step CO from its printed lines and computed both sets reproduces the two lists in this order; it checks the lists and is not part of the proof (Section 13).
Hence, within one context, the 39 context lines can run once; per member, only the 25 member-dependent lines and omega remain.
**Lemma CX (contexts and the class).** Let a run draw its contexts as in step 1 of 9.1. (a) Different contexts read different fresh words, so the contexts are independent, and within a context the seven outer words are independent and uniform. (b) The member lists of 9.9 hold every member of the class in exactly one lane, so a context walks every member once, except the members of the clusters that its gate skips and the partners that its descriptor table leaves out, whose outer steps have a zero mask of (2) (Lemmas CL and XF). (c) For any function g of an outer step with a finite mean, let G be its sum over the 2^19 outer steps of one context. Then E[G] = 2^19 E[g(U)], with U an outer step whose seven outer words are uniform and whose member is uniform on the class and independent of them: the outer step that step 1 of entry 415e792c draws. The values of G for the contexts of a run are independent and identically distributed. (d) If 0 <= g <= c on every outer step, then 0 <= G <= 2^19 c.
*Proof.* (a) holds by the construction of step 1. (b) The representative lists hold the 16,384 representatives once each and the partner lists the 31 partners of every cluster once each (9.9); the clusters partition the class. (c) G is the sum over all members y of g at the outer step (context, y). For each fixed y the outer words of the context are uniform and do not depend on y, so the mean of that term is E[g(W, y)] with W uniform; summing over the 2^19 values of y gives 2^19 E[g(U)]. G is a function of the fresh word of its context only, so (a) gives the independence and the equal laws. (d) is immediate. QED. By Lemmas CL and XF, each quantity whose totals 10.3 and 10.4 use, the indicators of the E count and of the pass count, the ledger U and N_o, is zero on the outer steps that the gate and the descriptor table skip (Lemma XF), so its total over the outer steps that a context walks is its G.
What the member loop does to the law of the run is therefore limited to dependence. The means that the heuristics use, the rate of H1', the shares of H4' and the mean of H5_exec, are those of a uniform outer step, exactly as in entry 415e792c; but the 2^19 outer steps that share a context also share its seven words, so independence holds between contexts and not between outer steps. 10.3 states the dependence part of H1' for contexts, states H_G_cluster for contexts, and proves the tails of H4', H5_exec and H_G_cluster over contexts.
**Lemma DT (the direct tables).** The tables T2 and T1 have one entry for each 32-bit word x: T2[x] = (mask of (2) on x) AND 5f and T1[x] = (mask of (1) on x) AND 5f. Each is stored in two levels, in one copy, at the word addresses f below. For l < 2^16 let st(l) < 4 be the class of the state of the automaton of (2) after the low 16 bits l: the states are the 7 rows of the third byte table of the automaton (Section 8), two states are in one class when they give the same mask, restricted to S, on every high 16 bits h, and the 4 classes are numbered in the order of their first rows. The first level R2 holds at f = 2^35 + l the word 2^33 + st(l) - l, and the second level L2 holds at f = 2^33 + s + 2^16 h, for s < 4 and h < 2^16, the mask that the automaton of (2) gives on the high 16 bits h from the states of class s, restricted to S. For T1 let st1(l) < 35 be the class, in the same sense on the bits 16 to 25, of the state of the automaton of (1) after the low 16 bits l, among the 43 rows of the third byte table of that automaton: 35 classes. R1 holds at f = 2^34 + l the word 2^34 + 2^26 + st1(l) - l, and L1 holds at f = 2^34 + 2^26 + s + 2^16 h', for s < 35 and h' < 2^10, the mask that the automaton of (1) gives on the bits 16 to 25 h' from the states of class s, restricted to S. Then for every 32-bit word x = l + 2^16 h: (i) the word of R2 at 2^35 + l plus x is 2^33 + st(l) + 2^16 h, the address of L2 whose entry is T2[x]; (ii) the word of R1 at 2^34 + l plus (x mod 2^26) is 2^34 + 2^26 + st1(l) + 2^16 h', h' = (x >> 16) mod 2^10, the address of L1 whose entry is T1[x]. Lane i of a packed word P (6.5) is moved to lane 0 by P >> 36 i (one operation; none for lane 0); the lanes above it then lie from bit 36 on, and the ANDs of 9.8 with masks below 2^36 drop them and keep the marker and the low 16 bits l of the lane, 2^35 + l (2^34 + l for R1), and its value x (x mod 2^26 for R1). A lane therefore reads, after one shift, with two loads for T2 and two for T1, the same masks restricted to S that the two automata of Section 8 give. The table PXR holds at f = 2^35 + 2^16 + l the word DB + 4 PX[l mod 512] of 9.9. The words of R1, of L1, of R2 and PXR, and of L2 have f in the disjoint bands from 2^34 below 2^34 + 2^16, from 2^34 + 2^26 below 2^34 + 2^27, from 2^35 below 2^35 + 2^17, and from 2^33 below 2^33 + 2^32, so no two words of the tables are at one address.
*Proof.* The automaton of (2) of Section 8 runs over the bits of x from bit 0 upward, so its final mask is a function of its state after the low 16 bits and of the high 16 bits h, and the byte tables of step 0 give that state as one of the seven rows of the third byte table and the mask from it over the third and fourth bytes, which by the definition of the classes is the mask from every state of its class; L2 holds that mask at the address of (i), which is the sum stated, since (2^33 + st(l) - l) + (l + 2^16 h) = 2^33 + st(l) + 2^16 h. (ii) is the same for the last two byte tables of (1), the sum being (2^34 + 2^26 + st1(l) - l) + (l + 2^16 h') = 2^34 + 2^26 + st1(l) + 2^16 h', and bits 26 to 31 of x change no mask (Lemma T26). The bands: 2^34 + 2^16 < 2^34 + 2^26, 2^34 + 2^27 < 2^35, 2^35 + 2^17 < 2^36 and 2^33 + 2^32 < 2^34. QED. Cost of the build: R1 and L1, 2^16 and 35 * 2^10 words, each from at most four byte-table loads, the load of a class and three additions, the AND with S, the store with its address and the loop, fewer than 32 units, 3,244,032 units, below the 2^25 that Section 11 charges; R2, L2 and PXR, 2^16, 4 * 2^16 and 2^16 words, each from at most two byte-table loads and the load of a class or the load of PX, the arithmetic of its value and address, the store and the loop, fewer than 32 units, 12,582,912 units, and, once, the class maps, by comparing the masks of each state with those of the classes found so far, at most 7 * 4 * 2^16 + 43 * 35 * 2^10 pairs of entries at 8 units each, 27,009,024 units: 39,591,936 together, below the 2^27 that Section 11 charges. They hold (2^16 + 35 * 2^10) + (2^16 + 4 * 2^16 + 2^16) = 494,592 words, 15,826,944 bytes as words of 256 bits (Section 12). Since every entry is the automaton's mask, the share of passing pairs read through the tables is SHARE / 2^64, as in Section 8.
**Lemma T26 (the mask of (1) reads only the low 26 bits).** For every 32-bit word x, T1[x] = T1[x mod 2^26].
*Proof.* The automaton of (1), restricted to S, reads the bytes of x from the lowest, and its fourth byte table (Section 8) has 37 rows of 256 entries; in every row the entry at a byte b equals the entry at b AND 3, a finite check of 9,472 entries, so the final mask depends on bits 24 and 25 of x and not on bits 26 to 31. QED. The declared program checks all 9,472 entries in its self-test (9.3); a participant run over all 2^32 words, not part of the package, found T1[x] = T1[x mod 2^26] for every x, and T1[x] different from T1[x mod 2^25] for 118,897,152 words, so 26 bits are needed.
*The member lists.* Step 0 of 9.1 writes the member lists of 9.9 as pairs of adjacent words (U[b], E[b]). In U[b], lane i is ROL(y, 7) for the member y of the lane, the word that the line Y8 reads, and in E[b] it is e1 = Y3 + y, the word that omega needs; the unused lanes of a last word hold copies of its last member and are never tested.
*The words of a context.* Once the 39 context lines have run on scalar words, a context prepares the sixteen operands that the member-dependent lines take from it, C0.b1, -C0.c1, C0.d1, -C0.b1 - w6, ROL(C0.d1, 16), K = X11 + 1 - S11, S12, K' = -C0.b1 - w6
- X4 - w2, -S1 - S6, S15' = S15 XOR ROR(X15, 8), S10, S5, w3, X13, X9 and -S0 - S5 (subtractions modulo 2^32), and copies each
  into all seven lanes, the packed -S0 - S5 with the marker 2^35 added in every lane, which every lane of cg and om carries (Lemma MB). These sixteen packed words occupy sixteen registers while the batches of the context run. Every other
  operand of those lines is fixed for the whole search: ROL(X15, 8), X15, the lane mask M (the low 32 bits of every lane) and the
  masks of PROR are written into the instructions. The context also loads S6, X14 and X2 + w7, which the shortcut of a passing
  lane reads (9.6), into three registers, forms S2 = ROL(S14, 8) XOR K2D, w5 = S2 - K2A - K2B and w12 = D2.a1 - S2 - S7 and stores
  them with the names that steps 2 and 3 reload, and its packed copy of X9 is X9' = X9 + 2^34 in every lane,
  which only the Y9 path reads (below).
*The omega-first batch.* The 25 member lines split in two. The 8 lines Y8, Y12, Y0, C0.a1, X0, D0.d1, D0.a1 and w8, with omega, are those that omega needs: the *omega side*. The other 17, D0.c1, D0.b1, X10, X5, X12, D1.c1, D1.d1, X1, C1.a1, C1.d1, D1.a1, C1.c1, w10, C1.b1, Y1, Y13 and Y9, are needed by Y9 alone: the *Y9 path*. Every member line is in exactly one of the two, and the Y9 path reads of the omega side only C0.a1 (in X12) and D0.d1 (in D0.c1). On packed words the omega side is folded: X0 = C0.a1 - X4 - w2 = Y0 + K' and, since D0.d1 = X0 XOR ROL(X15, 8), ROR(D0.d1, 16) = ROR(X0, 16) XOR ROR(X15, 8), so D0.a1 = ROR(X0, 16) XOR S15'; C0.a1 and D0.d1 are not formed, and omega = e1 + D0.a1 + (-S0 - S5) is summed as D0.a1 + (e1 + (-S0 - S5)), the same integer in every lane. For batch b of a context, on packed words, with the units of each line (one for each operation and load, five for PROR, where PROR(x, r) rotates the low 32 bits of every lane right by r):
    U    = load [p]                        1   (p: the list address of the batch)
    Y8   = U XOR C0.b1                     1
    Y12  = Y8 + (-C0.c1)                   1
    Y0   = PROR(Y12, 24) XOR C0.d1         6
    X0   = Y0 + K'                         1
    D0a1 = PROR(X0, 16) XOR S15'           6
    E    = load [p + 1]                    1   (and 1 for the address p + 1 in a representative batch)
    cg   = E + (-S0 - S5)                  1
    om   = D0a1 + cg                       1   (omega = Y3 + y + w8)
The six lines and omega cost 17 units; the pair of a representative batch costs 3, the two loads and the address p + 1, and the pair of an old partner batch, two loads and their addresses, is paid by the opening of its cluster (9.9). Next come seven *lane tests*, for i = 0 to 6. Lane i shifts om right by 36 i (1; none in lane 0), which moves the lane to lane 0 (Lemma DT); it ANDs the shifted word with 2^35 + 2^16 - 1, which keeps the marker and the low 16 bits l of the lane's omega, 2^35 + l, the word address of R2, and loads the word there; it ANDs the shifted word with 2^32 - 1, which keeps the lane's omega x without its guard bits and marker, adds the two, which gives the word address of L2 at x (Lemma DT (i)), loads the mask of (2) there, compares it with zero and branches: 8 units per lane, 7 in lane 0, 55 in all. A partner batch of seven lanes therefore executes *72 units*, its omega side and its lane tests, a batch of n lanes 16 + 8 n, and the fifth old partner batch of a cluster, with three lanes, 40. The representative of an opened cluster runs the same lane test in its lane of the representative batch (9.9), charged 8 units, and the address of R2 that it formed stays in its register. X0, Y0, Y12 and om stay in registers through the lane tests.
A lane whose mask of (2) is not zero is an *E lane* and runs its E handler right after its lane test. The handler adds u_E = 10 to W, one addition with an immediate. *The fill (GPT Sol, answer CM 5A).* At the first E lane of a batch the handler adds u_E + u_G = 10 + 56 in that one addition instead, rebuilds C0a1 = Y0 + (-C0.b1 - w6) and D0d1 = X0 XOR ROL(X15, 8), 2 units, builds the Y9 path on packed words for all seven lanes at once from them and the words of the context, and keeps the result, with C0a1, D0d1 and the packed Y1, in registers: the batch's *cached Y9*. The second column gives the units of a line of the Y9 path and the third their running sum:
    X12  = C0a1 XOR ROL(C0.d1, 16)        1    1
    D1d1 = (X12 XOR M) + K                2    3   (= X11 - X12 - S11)
    X1   = PROR(X12, 24) XOR D1d1         6    9
    D1a1 = PROR(D1d1, 16) XOR S12         6   15
    w10  = D1a1 + (-S1 - S6)              1   16
    D0c1 = D0d1 + S10                     1   17
    D0b1 = PROR(S5 XOR D0c1, 12)          6   23
    X10  = D0c1 + X15                     1   24
    X5   = PROR(D0b1 XOR X10, 7)          6   30
    C1a1 = X1 + X5 + w3                   2   32
    C1d1 = PROR(X13 XOR C1a1, 16)         6   38
    C1c1 = X9 + C1d1                      1   39
    C1b1 = PROR(X5 XOR C1c1, 12)          6   45
    Y1   = C1a1 + C1b1 + w10              2   47
    Y13  = PROR(C1d1 XOR Y1, 8)           6   53
    Y9   = C1c1 + Y13                     1   54
Step CO forms D1.c1 = X11 - X12 and then D1.d1 = D1.c1 - S11; D1.c1 has no other use among the 25 lines of Lemma Y (D1.b1, which also reads it, is not needed), so the line D1d1 forms D1.d1 at once from K = (X11 + 1 - S11) mod 2^32, which the context prepares in place of -S11. The 17 lines of the Y9 path, D1.c1 and D1.d1 in one line, cost 54 units and the two rebuilt words 2, so a fill costs *56 units*. With X9' = X9 + 2^34 of the context in place of X9, the line C1c1 gives C1.c1 + 2^34 in every lane and the line Y9 gives Y9 + 2^34; C1.c1 is read only by Y9 and by the PROR of C1b1, which drops the guard bits, so no other value changes (Lemma MB). Every E lane, the first included, then shifts the cached Y9 right by 36 i (1; none in lane 0), which moves its lane to lane 0, ANDs the shifted word with 2^34 + 2^16 - 1 (1), which gives 2^34 + (Y9 mod 2^16), the word address of R1, loads the word there (1), ANDs the shifted word with 2^26 - 1 (1), which keeps Y9 mod 2^26 without its marker, adds the two (1), which gives the word address of L1 at its Y9 (Lemmas DT and T26), loads the mask of (1) there (1), and ANDs it with the mask of (2), compares with zero and branches (3). An E lane therefore costs *10 units*, 9 in lane 0: 1 for W, 1 for the shift, 5 for the ANDs, the addition and the loads, and 3, and its batch's fill 56 more once. The fill computes the same packed values that a Y9 path built at any later lane of the batch would compute: they depend only on X0, Y0 and the words of the context, which no lane test, E handler or passing lane changes.
*The code of a batch.* It is written out lane by lane as a *not-ready chain*, run until the batch's first E lane, whose E handlers contain the fill, and, after the E handler of each lane i of that chain, a *ready tail* for the lanes i + 1 to 6, whose E handlers read the cached Y9 only; a passing lane is written inline after each E handler. In the chain and in every tail, the lane test of lane i branches past its E handler when its mask of (2) is zero and otherwise falls through into it; an E handler falls through into its passing lane when X is not zero and otherwise branches to the lane test of the next lane; a passing lane falls through, or returns from steps 2 and 3, to the lane test of the next lane; and a not-ready E handler with its passing lane continues in the ready tail that follows it. The exits of the last lane are the branches of its lane test, its E handler and its pre-check and the return of steps 2 and 3, all aimed at the code that follows the batch. So whether the cache is ready is a position in the code, held by no flag and tested by no instruction, and every transfer is a fall-through or a branch that is charged in its lane (Section 11); at a representative lane site the code enters the one copy of the code of an opened cluster and continues at the site's continuation when that copy returns (9.9). The fifth old partner batch of a cluster has three used lanes, the last representative batch four and a chunk the n lanes of its dispatch leaf (9.9), and their code has those lanes only. The written-out code is paid in the once-only allowances of Section 11.
*Registers (our audit; the frame in registers after entry 73d5265f; GPT Sol, answer D14 3).* The tables R1, L1, R2, L2 and PXR are read at their word addresses, and the list addresses are the loop's list address p plus immediate offsets (9.9). Live through a partner batch or chunk: at most 18 words of the context (its sixteen packed operands, X9' among them, the gate word AW of 9.9 and the context count), the three registers S6, X14 and X2 + w7, 13 of the representative batch (the gate words t, g and c, E[b], om, Y0, X0, its list address, its cached Y9 with C0a1, D0d1 and Y1, and Y12), 11 of the partner batch (its address, E[b], om, C0a1, D0d1, its cached Y9, Y1, Y12, the mask of the current lane and two temporaries of the lane tests; a partner's Y0 and X0 give way to its C0a1 and D0d1), W and the credit: 47; and eight words of the masked walk of 9.9, IX', the representative's U and six reusable words (the carries, the broadcast U and E, the descriptor address, JU and the metadata): 55 of the 64 registers. A lane test uses the two temporaries of the lane tests, the mask of (2) staying in one of them from the lane test into the E handler, and an E lane takes one more for the shifted word of its Y9, 56 of the 64 (after its fill, whose temporaries are free again). A fill adds at most six packed values of the Y9 path live at once (a liveness count on the listing above) and the two temporaries of PROR, 63; a passing lane adds at most six temporaries of the shortcut and its mask X, 62. The representative's address of R2, which waits for the descriptor selection (9.9), is live only while the representative's own lane runs, when no partner batch is: at most 45 words then, 53 with a fill. So nothing is spilled; the frame of the representative batch stays in its registers through the partner batches, the counts of 9.1 are the one register W, and no code of the walk names the credit register.
**Lemma MB (the packed batch is exact).** Take any used lane i of any batch, and let (context, y) be its outer step. (a) The low 32 bits of lane i of om equal omega = Y3 + y + w8 as step CO computes it for that outer step, and the lane test, after moving its lane to lane 0, reads R2 and L2 at that value, which gives T2 at omega (Lemma DT (i)). (b) If the lane is an E lane, the low 32 bits of lane i of the cached Y9 of its batch equal the Y9 of step CO for the same outer step, bit 34 of the lane is 1 and bit 35 is 0, and the E handler, after moving its lane to lane 0, reads R1 and L1 at Y9 mod 2^16 and Y9 mod 2^26, which gives T1 at that Y9 (Lemmas DT and T26). (c) The lane is taken as passing exactly when its outer step passes the filter of Section 8. (d) No lane of any packed value reaches 2^36, so bits 252 to 255 of every packed word are zero; in every lane, om is the marker 2^35 plus a value below 3 * 2^32, the marker coming from the packed -S0 - S5 through cg.
*Proof.* The two listings contain the member-dependent lines of Lemma Y and omega, D1.c1 and D1.d1 in one line, C0.a1, X0, D0.d1 and D0.a1 of the omega side by the identities of F1 above and C0a1 and D0d1 rebuilt by the fill, each written with packed operands: a word of the context appears as the packed word that repeats its scalar value in every lane, subtracting such a word is adding its negation modulo 2^32, and the one subtraction of a member-dependent value, in D1.d1 = (X11 - X12) - S11, is written (X12 XOR M) + K with K = (X11 + 1 - S11) mod 2^32; X12 XOR M flips the low 32 bits of each lane and keeps its guard bits, and (2^32 - 1 - x) + X11 + 1 - S11 = X11 - x - S11 modulo 2^32, so the low 32 bits of the result are the D1.d1 of step CO. An XOR acts on each bit; an addition acts on each lane separately while no lane reaches 2^36, and then the low 32 bits of a lane are the sum modulo 2^32; PROR gives in the low 32 bits of each lane the rotation of the low 32 bits of that lane, whatever its guard bits (9.6). Lane i of U[b] and of E[b] holds ROL(y, 7) and Y3 + y for the member of the lane; the marker 2^35 of the packed -S0 - S5 is above the low 32 bits of every lane and reaches only cg and om, whose low 32 bits it does not change. By induction over the printed order the low 32 bits of each lane of each line are its scalar value. The Y9 path reads the values C0a1 and D0d1 of the omega side of the same batch, which the lane tests, the E handlers and the passing lanes do not change, so the order of the two parts changes no value, and the cached Y9 read by a later E lane of the batch is the value that a Y9 path built at that lane would give. The cached Y9 is the batch's own: it is filled only at the batch's first E lane, read only by E lanes of the same batch, kept across the steps 2 and 3 of a passing lane in the saved words of the batch and across the partner batches of an opened cluster in the frame of 9.9, and a new batch starts in the not-ready copy. The lane test and the E handler take the low 32 bits of lane i, and Lemma DT gives the masks. When the mask of (2) is zero the AND of the two masks is zero whatever the mask of (1), so leaving out the Y9 path and the mask of (1) in such a lane changes no decision; in any other lane the decision is that AND, as in Section 8. *Bounds.* Every loaded word and every word of the context is below 2^32 in every lane, and so is the output of PROR. Carry an exclusive upper bound through the lines: an addition of values below A and B is below A + B - 1, and an XOR of values below A and B is below the least power of two that is at least the larger of A and B. These bounds are functions of the lines alone, not of the words. Among the sums, om = D0a1 + cg has the largest bound, below 2^35 + 3 * 2^32 < 2^35.59 (the marker, and D0a1 + e1 + (-S0 - S5) below 3 * 2^32), and Y1 the next, below 9 * 2^32 < 2^35.17; among the XORs, the input of the PROR of Y13 has the largest, at most 2^36; Y9 stays below 3 * 2^32. The chunks of 9.9 form their U and E as the broadcast words of the representative plus offsets 2^17 j and 2^10 j with j < 32 in each lane, which are the U and E of the partners: ROL(y_j, 7) = ROL(y_0, 7) + 2^17 j and e_j = e_0 + 2^10 j with no carry out of bit 22 or 14 (Lemma XF), all below 2^32. With X9' < 2^34 + 2^32 in place of X9, C1c1 stays below 2^34 + 2^33, the input of the PROR of C1b1 below 2^35, and Y9 below 2^34 + 3 * 2^32 = 7 * 2^32 with its bit 34 set and bit 35 clear, since Y9 - 2^34 is the value of the original line, below 3 * 2^32 < 2^34. So no lane reaches 2^36, and no AND with M is needed before a sum. QED. The bounds are those of the member loop of entry e9b6649e, whose lines are the same; the participant recomputed them for this order and for the fused line, whose bound, 3 * 2^32 - 1, is below the 4 * 2^32 - 2 of the two lines it replaces, and a participant simulation of the order with the two lines apart asserted every value of every operation below 2^36 (below).
*A context.* Drawing the fresh word, the 39 context lines on scalar words, forming and copying the sixteen packed operands, storing the names for steps 2 and 3, the gate base of 9.9, X9', X2 + w7, the three registers of the shortcut, S2, w5 and w12 and the test of W come to at most 509 units; with the four flags of the gate (160), the descriptor table of 9.9, the carry word of every representative batch, with the slow path of the gate and the loop of the representative batches, itemized in Section 11, a context is charged 90,917.
*A passing lane.* A lane that passes computes e1, C2.a1, C2.d1, C2.c1, C2.b1 and the word r' of the pre-check by the shortcut of 9.6 (35) and runs the pre-check of 9.7 (7); when T is zero it adds u_P = 43 to W, one addition, and ends; otherwise it adds u_P + u_C = 43 + 6 in one addition, runs the preflight of 9.7 (6) and, when the credit covers CM(T), calls steps 2 and 3 under the meter, which may use all 64 registers: the global ledger saves the live words of the batch, W among them, at its entry and reloads them before its return (Section 11). The lane is written inline after its E handler, so it keeps no return link and makes no jump of its own; the credit stays in its register and is never restored from a copy. Section 11 itemizes the lane at 43 units, 1 + 35 + 7, and a call at 6 more (GPT Sol, answers CD 3, CI 1.5, CK3 2, CM 5A and D9; GPT Luna 5.6, answer D25; our audit).
*The participant checks.* Three participant programs, not part of the package. (1) A reimplementation of the member loop of entry e9b6649e (research/impl/memberloop) found the two lists of Lemma Y from the printed lines and, on 100,000 random pairs of a context and a member, compared Y9, omega, both masks, the pass decision and all 25 member-dependent lines with the full step CO: 0 differences. (2) A Python program (research/frontline/ca) ran 142,858 batches of seven consecutive members in 1,429 contexts on scalar words and as a packed simulation with seven 36-bit lanes that executes and counts every operation, load and PROR and asserts every lane value below 2^36, against the full member loop: 0 different pass decisions, 0 different masks of (2) or Y9 in the 54,067 lanes with a nonzero mask of (2); the simulation executed 67 units in every batch, with the two list words loaded apart (the pair saves one address), and 78 in every Q path, the Q path of answer CA, with 16 for the E count and D1.c1 and D1.d1 apart; the largest lane value was 2^35.02. (3) A graphics-card version (RTX 3090) walked 120,000 contexts (62,914,560,000 outer steps), every member, with the omega-first batch and the full member loop on every outer step: 0 different pass decisions, masks of (2) or values of Y9 in the 3,418,392,488 lanes with a nonzero mask of (2), and 62,294,500 passes. Lanes with a nonzero mask of (2) were 0.054334 of the outer steps, against the exact share 0.054416 and the share 0.054418 that E_BUDGET allows.
**9.9 The cluster gate and the masked partner walk (GPT Sol, answers CI 1, CJ 1 to 5, D12, D14, D16 and D18; the layout, our audit).** This subsection fixes the order in which a context walks its members, lets it skip, with one table read, a group of 32 members that is proved to fail test (2), and, in a group that it opens, skips the members that a table of the context proves to fail it. Every outer step that is walked is that of 9.8, with the same batch, lane test, E handler and passing lane.
*Clusters.* Write e = Y3 + y for the word e1 of a member y. The class fixes the 13 bits of e in 03cf8303 and leaves the other 19 free (Lemma Q); bits 10 to 14 are free and bit 15 is fixed at 0. Let g run over the 2^14 settings of the 14 free bits other than 10 to 14, and let e_g have these bits and bits 10 to 14 zero. The *cluster* of g is the 32 members with e = e_g + j * 2^10, 0 <= j < 32; its *representative* is the member with j = 0, and the other 31 are its *partners*. The 16,384 clusters partition the class.
In one context put b = C0.b1, c = C0.c1, d = C0.d1, A = C0.b1 + w6 + X4 + w2, L = ROL(X15, 24) XOR S15 and C = e - S0 - S5, all modulo 2^32. With r = ROL(y, 7) XOR b, v = r - c (the line Y12), p = ROL(v, 8) XOR d (the line Y0) and x = p - A (the line X0), the omega side of 9.8 gives
    omega = (ROL(x, 16) XOR L) + C,
since D0.a1 = ROL(X0 XOR ROL(X15, 8), 16) XOR S15 and omega = e + D0.a1 - S0 - S5. The term ROL(X15, 24) of L is part of the identity.
**Lemma KP (two prefixes per cluster).** Fix a context and a cluster. Let p_0 be the p of its representative, u = (((p_0 >> 16) AND 1ff) - ((A >> 16) AND 1ff)) mod 512, and W_l = (C + (((u - l) mod 512) XOR (L AND 1ff))) mod 512 for l = 0 and 1. Then every member of the cluster has omega mod 512 in {W_0, W_1}.
*Proof.* The members of a cluster differ only in bits 10 to 14 of e, so C mod 512 is the same for all of them. Bit 15 of e is 0, so e mod 2^16 < 32,768, while Y3 mod 2^16 = c181 = 49,537: the subtraction y = e - Y3 borrows into bit 16 in every member, and bits 16 to 31 of y, like bits 0 to 9, are the same for all members; only bits 10 to 15 differ. Then r differs only in bits 17 to 22, so bits 0 to 16 of v = r - c are the same for all members, and its bits 24 to 31 take at most two values, which differ by the borrow into bit 24. Hence bits 8 to 24 of p = ROL(v, 8) XOR d are the same for all members and only its low byte varies. Bits 16 to 24 of x = p - A are ((p >> 16) AND 1ff) - ((A >> 16) AND 1ff) - l modulo 512, where l in {0, 1} is the borrow of (p mod 2^16) - (A mod 2^16) into bit 16; the first term is that of the representative, so these bits are (u - l) mod 512. Bits 0 to 8 of ROL(x, 16) are bits 16 to 24 of x, and bits 0 to 8 of a sum depend only on bits 0 to 8 of its terms, so omega mod 512 = W_l. QED. The two values may be equal, and one of them may not occur: the lemma is a cover, not a rate.
**Lemma A9 (dead residues of test (2)).** Let S7 be the 52 residues 25 to 3e and 45 to 5e (hexadecimal) modulo 128. If omega mod 128 is not in S7, then (2)_j fails for omega for every j in S, and T2[omega] = 0.
*Proof.* A word f with (omega + f) XOR ((omega + DY3) + (f XOR sigma_j)) = eps (Section 8) satisfies the equation modulo 2^9, whose bits depend only on omega and f modulo 2^9. For the six outcomes of S, sigma_j mod 2^9 = f0 (the low twelve bits of every tau_j are 0a0), DY3 mod 2^9 = fd and eps mod 2^9 = 55. The finite check
    [r for r in range(512)
     if any((((r + f) ^ (r + 0xfd + (f ^ 0xf0))) & 511) == 0x55 for f in range(512))]
lists the residues r of omega modulo 2^9 for which the equation modulo 2^9 has a solution: 208 residues, exactly those whose value modulo 128 lies in S7. For any other omega no j in S satisfies (2)_j, and by Lemma DT the mask of (2), restricted to S, is zero. QED.
*The straddle gate (GPT Sol, answers D14 and D16; its third state, GPT Luna 5.6, answer D25).* Write w[k..l] for bits k to l of a word w as a number. For i = 0 to 3 let T_i = f2, fa, 02 and 0a (hexadecimal), that is (8 i - 14) mod 256, and put
    H_i = ((T_i XOR b[24..31]) - c[24..31]) mod 256,   lo0_i = H_i XOR d[0..7],   lo1_i = ((H_i - 1) mod 256) XOR d[0..7],
    hbad_i = [min(lo0_i, lo1_i) < A[0..7] <= max(lo0_i, lo1_i)],   Hbad = hbad_0 + 2 hbad_1 + 4 hbad_2 + 8 hbad_3.
These depend on the context alone. The cluster of a representative with word e and line Y0 = p *straddles* when p[8..15] = A[8..15] and hbad_i = 1 for i = e[20..21]. The *gate entry* at an index w + 2^8 m + 2^16 h + 2^20 i + 2^22 a, for 0 <= w < 128, 0 <= m, a < 256, 0 <= h < 16 and 0 <= i < 4, is F + 2 B, with F = 1 when w lies in S7 and 0 otherwise and B = 1 when m = a and bit i of h is 1 and 0 otherwise. The *gate value* of a representative is the gate entry at w = omega mod 128, m = p[8..15], h = Hbad, i = e[20..21] and a = A[8..15]. No table holds it: the representative batch computes it from three packed words (below), with this identity, a finite check over the 128 residues: w lies in S7 exactly when bit 7 of (((w + 5b) mod 128) AND 5f) + 66 is 0 (hexadecimal), since (w + 5b) mod 128 = (w - 25) mod 128 and S7 holds exactly the residues whose difference from 25 modulo 128, with its bit 5 cleared, is at most 19. The gate value is 0 exactly when its omega mod 128 does not lie in S7 and its cluster does not straddle, 1 when its omega mod 128 lies in S7 and its cluster does not straddle, and 2 or 3 when its cluster straddles.
**Lemma CL (the gate is lossless).** Fix a context and a cluster. If the cluster does not straddle, every member has the omega mod 512 of the representative. If the gate value of the representative is 0, then every member of the cluster has T2[omega] = 0; none of its outer steps runs a Q path or passes the filter, and none holds a listed good trial.
*Proof.* Member j has e = e_0 + 2^10 j. Since e mod 2^10 >= 303 > 181 = Y3 mod 2^10 (hexadecimal) and e[10..15] = j < 48 = Y3[10..15], y = e - Y3 has y[10..15] = 16 + j. Bits 15 and 16 of e are 0, so e[0..16] < 2^15 and y[0..16] = e[0..16] + 2^17 - 1c181 < 2^16: y[16] = 0, and the subtraction borrows into bit 17. With e[17..24] = 134 + 8 i (the class fixes e[17..19], e[22..24] and leaves e[20..21] = i) and Y3[17..24] = 147, y[17..24] = (134 + 8 i - 147 - 1) mod 256 = T_i for every member. So r = ROL(y, 7) XOR b has r[24..31] = T_i XOR b[24..31], the same for all members, and the high byte of v = r - c is H_i or (H_i - 1) mod 256, by the borrow out of its low 24 bits; p = ROL(v, 8) XOR d has p[8..24] common to the cluster (Lemma KP) and the low byte lo0_i or lo1_i. The borrow of x = p - A into bit 16 is [p mod 2^16 < A mod 2^16]: when p[8..15] differs from A[8..15] it does not depend on the low byte, and when they are equal it differs between the low bytes lo0_i and lo1_i exactly when hbad_i = 1. So when the cluster does not straddle, every member has the borrow of the representative, x[16..24] is common, and by omega = (ROL(x, 16) XOR L) + C, with C mod 2^10 common, omega mod 512 is the representative's. When the gate value is 0 the cluster does not straddle and the representative's omega mod 128 is not in S7, so no member's is, and Lemma A9 gives T2[omega] = 0. A lane with a zero mask of (2) is no E lane and does not pass (Lemma MB (c)), and by Lemma F an outer step that does not pass holds no listed good trial. QED. The lemma uses no law of the words. The participant's arithmetic program checks y[10..24] and the borrow into bit 17 on all 2^19 members, and on 20,000 random clusters, half of them with A[8..15] = p[8..15], the straddle rule against the borrows of the two low bytes, the common omega mod 512 and the gate against the word equations of every member; the declared program compares the gate value of every representative it walks with S7 and the two exact prefixes of Lemma KP (9.2).
Hence skipping a cluster whose gate value is 0 loses nothing: the E count, the pass count, the work of passing lanes and of steps 2 and 3, the debits of the credit and the number N_o of 10.3 are zero on every outer step that the gate skips, so their totals over the outer steps that a context walks equal their totals over all 2^19 outer steps of the context, outer step by outer step. In the same way the fills of a context in the walk with the five partner batches of every opened cluster, before any halt, are exactly those of its 84,261 batches (its representative batches and the five partner batches of each cluster) that hold a member with a nonzero mask of (2): a skipped cluster holds none, so its partner batches and its representative's lane would not be filled. This count, G(C), is a function of the context alone; Lemma XF (d) bounds the fills of the masked walk below by it.
*The carries of a cluster.* Fix a context and a cluster, with members e_j = e_0 + 2^10 j and y_j, j = 0 the representative. For a member let c17, c25, c9a and c9b be the carries into bit 17 of Y8 + (-C0.c1), into bit 25 of Y0 + K', into bit 9 of D0.a1 + (-S0 - S5) and into bit 9 of e1 + w8, and IX = c17 + 2 c25 + 4 c9a + 8 c9b. With five-bit windows, all modulo 32, put
    o(IX, j) = (((((((16 + j) XOR (C0.b1 >> 17)) + ((-C0.c1) >> 17) + c17) XOR (C0.d1 >> 25)) + (K' >> 25) + c25)
               XOR (S15' >> 9)) + ((-S0 - S5) >> 9) + c9a) + 1 + 2 (j mod 16) + c9b,
and let alive16(w), for w < 2^16, be 1 when w mod 128 is in S7 and bit (w >> 9) mod 32 of LW[(w >> 8) mod 2] is 1, with LW = (e000001f, f000001f), whose words have 8 and 9 bits set.
**Lemma XF (the masked partner walk).** Fix a context and a cluster that does not straddle, and let W and b8 be omega mod 512 and its bit 8 for the representative. (a) Every member has the same IX and the same omega mod 512, and bits 9 to 13 of the omega of member j are o(IX, j); for each IX, j -> o(IX, j) is a bijection of the 32 values of j. (b) If T2[omega] is not 0, then alive16(omega mod 2^16) = 1. (c) So the partners j with T2[omega_j] not 0 are among the *survivors*, the j from 1 to 31 with W mod 128 in S7 and bit o(IX, j) of LW[b8] set, and there are at most 9 survivors. (d) Let chunk A be the survivors in the partner batch of the earlier walk (j from 1 to 7, 8 to 14, 15 to 21, 22 to 28 or 29 to 31) that holds the most of them, the first such batch, and chunk B the other survivors: each has at most 7 members, and walking the representative and then the two chunks, each a batch of 9.8 with its own cache, fills at most as many batches as walking the five partner batches, outer step by outer step. (e) The representatives with p[8..15] = A[8..15], and so the clusters that straddle, are at most 128 of the 16,384 of a context.
*Proof.* (a) Bits 0 to 9 of e_j are those of e_0, and e_0 mod 2^10 = 303 + 4 m (hexadecimal, m < 64) is at least 303 > 181 = Y3 mod 2^10, so y_j = y_0 + 2^10 j with bits 10 to 15 of y_j equal to 16 + j and bit 16 equal to 0 (as in Lemma KP), and ROL(y_j, 7) = ROL(y_0, 7) + 2^17 j, with bits 17 to 22 equal to 16 + j and every other bit that of the representative. So bits 0 to 16 of Y8 = ROL(y, 7) XOR C0.b1 are common and c17 is common; bits 0 to 16 of Y12 are common, so bits 8 to 24 of Y0 = ROL(Y12, 8) XOR C0.d1 are common, and only its low byte varies. The carry into bit 16 of Y0 + K' = Y0 - A is the borrow of p - A into bit 16: when bits 8 to 15 of Y0 differ from those of A it does not depend on that byte, and when they are equal it is the same for the two low bytes that the members' Y0 can have, since the cluster does not straddle (proof of Lemma CL); so bits 16 to 24 of X0 and c25 are common; then bits 0 to 8 of D0.a1 = ROR(X0, 16) XOR S15', of w8 and of e1 are common, and so are omega mod 512, c9a and c9b. Following the windows, bits 17 to 21 of Y8 are ((16 + j) XOR (C0.b1 >> 17)) mod 32; adding (-C0.c1) >> 17 and c17 gives bits 17 to 21 of Y12; the XOR with C0.d1 >> 25 gives bits 25 to 29 of Y0; adding K' >> 25 and c25 gives those of X0; the XOR with S15' >> 9 gives bits 9 to 13 of D0.a1; adding (-S0 - S5) >> 9 and c9a gives those of w8; and adding bits 9 to 13 of e1, 1 + 2 (j mod 16), and c9b gives those of omega: o(IX, j). In every step but the last, bit i of the result is bit i of j XOR a function of the bits of j below i; the last adds 2 (j mod 16), whose bit i is bit i - 1 of j, which keeps that form; so j -> o(IX, j) is triangular with unit diagonal, a bijection. (b) The bits 0 to 15 of the equation (2) depend only on omega and f modulo 2^16, so a solution of (2) is one modulo 2^16; the w < 2^16 for which (2) has a solution modulo 2^16 for some row of S were listed exhaustively by a carry-pair walk over the 65,536 values (the participant's arithmetic program): 7,072 of them, exactly those with alive16(w) = 1. (c) follows from (a) and (b); LW[b8] has at most 9 bits set and j -> o(IX, j) is a bijection, so at most 9 values of j survive. (d) If chunk A holds m survivors and there are at most 9 in five batches, then m >= 2 or there are at most 5, so chunk B has at most 7; chunk A, inside one batch, has at most 7. A chunk is filled only when it holds a member with T2[omega] not 0; chunk A's members are in its old batch and chunk B's in old batches other than A's, so a filled chunk A maps to its filled old batch and a filled chunk B to a different filled old batch; the representative batch is the same in both walks. (e) Bits 8 to 15 of Y0 are bits 0 to 7 of Y8 + (-C0.c1) XOR bits 8 to 15 of C0.d1, a bijection of bits 0 to 7 of Y8 = ROL(y, 7) XOR C0.b1, which carry y[25..31] and y[0] = 0. The class fixes e1[22..25] = 0011 (from bit 22 up) and leaves e1[26..31] and e1[20], e1[21] free, and y[25..31] = (e1[25..31] - Y3[25..31] - [e1[21] = 0]) mod 128: for a fixed e1[21] the 64 values of e1[26..31] give 64 different values, all of one parity, and the two values of e1[21] give opposite parities. So the byte A[8..15] is hit by at most one value of (e1[26..31], e1[21]), and with the 2^7 values of e1[2..7] and e1[20] by at most 128 clusters; a cluster that straddles is one of them. QED. The lemma uses no law of the words; the participant's arithmetic program also checks (a) on 3,000 random clusters, half of them with p[8..15] = A[8..15] (the straddling ones left out), and the bijection for every IX, the chunk sizes, and (e) on 24 random contexts, and the declared program compares every partner of every walked descriptor with (a) and (c) (9.2).
So the masked walk loses nothing: every partner with a nonzero mask of (2) is in a chunk, so the E lanes, passing lanes, solver calls, debits and listed good trials of a context are those of the walk with five partner batches, outer step by outer step, and only their order inside a cluster can differ, when its two chunks both hold passing lanes.
*The walk of a context.* Step 0 of 9.1 writes the member lists in cluster order (9.8), interleaved: for each representative batch b, the pair (U[b], E[b]) of its representatives, lane i holding the representative of cluster 7 b + i (lanes 0 to 3 in the last pair), followed by the *broadcast words* of its representatives, for each used lane i the word that holds ROL(y, 7) of the representative of lane i in all seven lanes and the word that holds its e1 in all seven lanes, and by the five partner pairs of each of its clusters in lane order, holding its partners j = 1 to 31 in order, seven to a pair and three in the fifth: 86 words for a full batch, 50 for the last; 201,290 words, every member in exactly one lane of a pair. Besides the sixteen operands of 9.8 a context prepares A = -K', its four flags hbad_i, stored as four words at fixed addresses, the *gate word* AW = 2^8 A[8..15] in every lane, and the *descriptor table* of its masked walk: for each of the 16 values of IX and each b8 with W mod 128 in S7, the survivors of Lemma XF (c) in two chunks as in (d), the chunk that holds the least survivor first, at word address DB + a(IX) + 128 b8 + 256 with DB = 2^36 + 2^30 and a(IX) = 2^17 IX_0 + 2^25 IX_1 + 2^9 IX_2 + 2^10 IX_3, IX_k the four carries c17, c25, c9a and c9b of Lemma XF (a), each at the place where it arises: n_0, JU_0 and JE_0 in its words 0 to 2 and n_1, JU_1 and JE_1 in its words 4 to 6, n the size of the chunk, JU the sum of 2^(36 t + 17) j_t and JE that of 2^(36 t + 10) j_t over its members j_t in increasing order; JE = JU >> 7, since every j_t < 32 lies in bits 36 t + 17 to 36 t + 21 of JU. The other 32 descriptors (the same IX and b8, W mod 128 outside S7, at DB + a(IX) + 128 b8) have n_0 = n_1 = 0, and a real descriptor has n_0 >= 1, so n_0 = 0 forces n_1 = 0. With PX[w] = 32 (bit 8 of w) + 64 [w mod 128 in S7], the table PXR of Lemma DT holds DB + 4 PX[l mod 512] at 2^35 + 2^16 + l, built once. The 2,341 *representative batches* of a context run as a loop over the first 2,340, with the list address p of the batch in a register, advanced by 86 at the end of each batch and compared with the end of the lists, and the last, of four lanes, after the loop; the body of the loop and the last batch are written out, and each batch runs:

- the pair and the omega side of 9.8, which give X0, Y0, Y12, Y8, D0a1, cg and om in every lane;
- the three *gate words*, 8 operations, every constant in every lane (hexadecimal): t = ((om + 5b) AND 5f) + 66, whose bit 7
  in lane i is 1 exactly when omega mod 128 does not lie in S7 (the identity above: the low 7 bits of om + 5b are
  (omega + 5b) mod 128, the AND keeps six of them and the sum stays below 2^8); g = ((Y0 XOR AW) AND ff00) + ff00, whose bit 16
  in lane i is 1 exactly when p[8..15] differs from A[8..15]; and c = (g >> 9) AND t, whose bit 7 in lane i is the AND of these
  two bits; no lane of these sums reaches 2^36 (Lemma MB);
- the carry word IX' = ((Y12 XOR Y8 XOR (-C0.c1)) AND N17) OR ((X0 XOR Y0 XOR K') AND N25) OR ((w8 XOR D0a1 XOR (-S0 - S5)) AND N9)
  OR (((om XOR E XOR w8) << 1) AND N10), with w8 = D0a1 + (-S0 - S5) and N9, N10, N17 and N25 the words with bit 9, 10, 17 or 25 of
  every lane: the four carries of Lemma XF, c17, c25, c9a and c9b, each in the place where it arises (the carry into bit k of a sum is
  bit k of the sum XOR its two terms; the marker 2^35 of w8 and om cancels in these XORs), c9b moved up one place so that it does not
  meet c9a, the sum a(IX) of lane i in place in lane i of IX', 17 operations (eight XORs, the addition of w8, four ANDs, one shift
  and three ORs), which the context pays;
- for each used lane in order, the *gate test*: c ANDed with 2^(36 i + 7), compared with zero and branched on, 3 units; on 1
  the gate value is 0 and the cluster is skipped: T2 is not read (Lemma CL). Otherwise the *state test*: g ANDed with
  2^(36 i + 16), compared with zero and branched on, 3 units; on 1 p[8..15] differs from A[8..15], so the cluster does not
  straddle and, bit 7 of c being 0, omega mod 128 lies in S7: the gate value is 1. On 0, p[8..15] = A[8..15], and the lane takes
  the *slow path*: e[20..21] taken out of lane i of E[b] by a shift and an AND (2), the stored flag hbad_i at that index loaded
  with its address (2), compared with zero and branched on (2); on 1 the gate value is 2 or 3; on 0 bit 7 of t in lane i is
  tested (3), and the gate value is 1 when it is 0 and 0 otherwise, which skips the cluster. Only lanes with p[8..15] = A[8..15]
  take the slow path, at most 128 of a context (Lemma XF (e)), and the context pays 12 units for each of 128, their state tests
  included (Section 11). A cluster whose gate value is not 0 is *opened*: the representative's lane test (9.8) reads R2 and L2
  at its om, with its E handler and passing lane as in 9.8, and the address of R2 that it formed stays in its register. On a
  gate value of 2 or 3 the cluster straddles: u_O + u_F is added to W and the five partner pairs at p + 16 + 10 i to
  p + 25 + 10 i run as five batches of 9.8, each with its lane tests, E handlers, fill and cached Y9 and passing lanes. Otherwise
  u_O is added to W, and the *descriptor selection* runs: the bits a(IX) of lane i of IX' are taken out by a shift and an AND,
  the representative's address of R2 plus the immediate 2^16 is the address of PXR at the same l, whose word
  is loaded, and the descriptor address is their sum, DB + a(IX) + 4 PX[l mod 512] = DB + a(IX) + 128 b8 + 256 [W mod 128 in S7],
  since l mod 512 = omega mod 512; and n_0 is loaded there. Then the representative's U and E are *broadcast* to the seven
  lanes: its two broadcast words are loaded from the member lists, each at p plus an immediate offset, an addition and a load;
  then each chunk in turn: its n (n_0, still in its register, for the first chunk; n_1, loaded at the descriptor
  address plus 4, for the second) is decoded by a depth-three tree of comparisons whose leaves are the code for n lanes, JU is
  loaded and added to the broadcast U and JU >> 7 = JE to the broadcast E, which gives the U and E of a batch whose lane t holds
  the partner j_t (Lemma MB), and the chunk runs as a batch of 9.8 with n used lanes and its own cache; the leaf 0 of either chunk
  ends the cluster, so a cluster with no surviving partner ends at its first tree. All this precedes the gate test of the next
  lane. The representative batch is one batch of 9.8 for the cache: it is filled at most once, at its first representative E lane.
The code of an opened cluster, its straddling branch and its chunks included, is written once. Its state test, slow path, descriptor selection and broadcasts read lane i of the representative's words at a shift of 36 i or at an immediate that depends on i, and stay at each of the 38 representative lane sites (28 in the body of the loop, the chain of 7 lane sites and the tails of 6 + 5 + 4 + 3 + 2 + 1 = 21 after the E handlers; 10 in the last batch); the branch of the gate test skips the site. A site that opens a cluster sets the register K to its number (1) and the base address p + 16 + 10 i of the cluster's partner words (1) and jumps to the one copy (1); K is held in the register of the carries, which the descriptor selection has finished with, and the base in that of the descriptor address, so no live word is added (9.8, Section 11). The code of a chunk at each leaf of a dispatch tree ends with one jump to the end of the copy: a return tree of six comparisons of K with an immediate, each with its branch, 12, that reaches the site's continuation, the gate test of the next lane in the not-ready chain or in the ready tail (38 targets). These 15 units and one in reserve are the 16 of an opened cluster, straddling or not. The words of the representative batch, its gate words, E[b], om, Y0, X0, Y12 and its cached Y9, stay in their registers through the partner batches and chunks, which use other registers (9.8), so nothing is stored or reloaded around them and no count is restored from a copy.
*Charges (Section 11).* A representative batch costs 52: 3 for the pair, the load at the list address p and the load of E[b] at p + 1 with that address; 17 for the omega side; 8 for the gate words; 21 for the seven gate tests; and 3 for the loop step, the advance of p, its comparison with the end and the branch. The last representative pair has four used lanes and costs 40, its gate tests being 4 * 3 = 12, and no loop step. The carry word, 17 units per representative batch, and the slow path, 12 units for each of at most 128 lanes, are paid by the context. An opened cluster costs 168: 3 for its state test; 8 for the representative's lane test; 3 for the addition of u_O to W and the jumps at the ends of the two chunks; 6 for the descriptor selection (the lane extraction and mask of IX', 2; the address of PXR, an addition of an immediate to the representative's address of R2, and its load, 2; the addition, 1; the load of n_0 at that address, 1), 5 in lane 0, which needs no shift; 4 for the broadcasts (for each of U and E the address of its broadcast word, p plus an immediate, and its load), the same in every lane; at most 104 for the omega sides and lane tests of the two chunks, c(n_A) + c(n_B) with c(n) = 16 + 8 n, n_A, n_B <= 7 and n_A + n_B <= 9 (Lemma XF); and 11 + 13 for their addressing (for each chunk the dispatch, three comparisons and branches, 6, JU, an addition of its offset to the descriptor address, a load and an addition to the broadcast U, 3, and JU >> 7 added to the broadcast E, 2; the second chunk also loads n_1, 2, and costs 8 when it is empty; a first chunk with n_0 = 0 costs its dispatch, 6); and 16 for the entry into the one copy of the code of the cluster and the return from it (below): 3 + 8 + 3 + 6 + 4 + 104 + 11 + 13 + 16 = 168. A chunk of n lanes runs its omega side, 17, and its lane tests, 8 per lane but 7 in lane 0, so it costs c(n) = 17 + 8 n - 1 = 16 + 8 n; by Lemma XF (c) and (d) the two chunks have n_A, n_B <= 7 and n_A + n_B <= 9, so c(n_A) + c(n_B) = 32 + 8 (n_A + n_B) <= 104 when both are used, with equality when n_A + n_B = 9, and c(n_A) <= 72 when the second is empty. The parts do not overlap: the 104 prices only the omega sides and lane tests, the 11 + 13 the operands and the dispatch of the chunks, the 6 the descriptor address and the load of n_0, which the first chunk reuses, and the 3 the addition to W and the two end jumps; a cluster with no surviving partner ends at the first dispatch, and an empty second chunk at its dispatch. A straddling cluster costs 8 for its representative's lane test, 21 for its five partner pairs, two loads each with their addresses, and its addition to W, and 4 * 72 + 40 for its five batches, 357, its entry and return, 16, and its state test, 376; its one addition to W, after the representative's lane, adds 376 = u_O + u_F where an opened cluster adds u_O = 168, so the straddling clusters carry the surcharge u_F = 208, which has its own budget (Lemma OR below; 9.1) and, in W_CTX, the 128 that a context can hold (Lemma XF (e)). E lanes, fills and passing lanes of the representative and of the partners are charged in their own rows. The descriptor table of a context costs at most 48,896 (superseded by 12,800, amendment G), the charge: 16 * 32 * 50 for the masks of the 16 carry indices at the 32 values of j (21 for the window arithmetic, 12 for the two tests of LW and 17 for decoding, the store and control), 32 * (32 * 10 + 5 * 8 + 9 * 32 + 16) for the 32 descriptors with W mod 128 in S7 (the 31 positions at 10, five steps of the largest batch at 8, at most 9 survivors placed at 32 and the stores at 16), and 2,048 for its setup, the reset of n_0 and n_1 of the 32 other descriptors (224) and the save and reload of 64 words around it (256). The flags and the gate word cost a context at most 132 units, charged 160: at each of the four sites H_i (an XOR, a subtraction and an AND, 3), lo0_i (1) and lo1_i (3), the minimum and maximum with a branch and two assignments (4), the two range comparisons and their AND (3) and the store of hbad_i with its address (2), 16 a site; 10 for the cuts of b, c, d and A and for A; 10 for AW, A AND ff00 and its copy into seven lanes by three shifts and ORs; 32 for addressed loads and stores of context words; and 16 for staging and control. No gate table and no broadcast table is built: the gate value is computed from the gate words, and the broadcast words are written once with the member lists (Section 11).
**Lemma OR (the opening rate of the gate).** Let the seven outer words of a context be independent and uniform, as in a run (Lemma CX (a)). Then the number A(C) of clusters of the context whose gate value is not 0 has
    E[A(C)] <= 6,656 + (38/64) * 16,384 * 9/65,536 = 852,139 / 2^7 = 6657.3359375,
so the mean share of opened clusters is at most p* = 852,139 / 2^21 = 0.40633153915...; no independence between the clusters of a context is used. The straddling clusters of the context are G(C) = 64 B(C) of them, at most 128, with E[G(C)] <= 16,384 * 9/65,536 = 9/4.
*Proof.* (a) *Blocks.* The free bits of a representative's e other than 10 to 14 are e[2..7], e[20..21] and e[26..31]. Fix e[20..21] and e[26..31] and let u = e[2..7] run over its 64 values: a *block* of 64 representatives, 256 blocks to a context. Since e mod 2^10 = 303 + 4 u > 181 = Y3 mod 2^10 (hexadecimal), u changes no bit of y = e - Y3 from bit 10 up, and y[0] = 0. So on a block i = e[20..21] is fixed, and so is p[8..15] = v[0..7] XOR d[8..15], since v[0..7] depends only on r[0..7] = (y[25..31] and y[0]) XOR b[0..7]: the straddle flag is constant on a block. (b) *A block that does not straddle opens on exactly 26.* Put z = y[1..7]. As u runs over its 64 values, y mod 256 = (4 u - 126) mod 256 and z = (2 u - 63) mod 128 run through the 64 odd residues, with e mod 128 = (1 + 2 z) mod 128. Every representative of the block has r[24..31] = T_i XOR b[24..31], so its p has the low byte lo0_i or lo1_i and the block's p[8..15]; off straddle the borrow into bit 16 of x = p - A is therefore the same for all of them, as in the proof of Lemma CL, and so is the borrow into bit 8 of v = r - c, which depends on r[0..7] alone. With b8, c8, d16, A16, L7 and SS7 the seven-bit slices b[8..14], c[8..14], d[16..22], A[16..22], L[0..6] and (S0 + S5)[0..6], and br8 and br16 the two borrows, the identity omega = (ROL(x, 16) XOR L) + e - S0 - S5 gives
    omega mod 128 = (1 + 2 z + P(z)) mod 128,   P(z) = ((((((z XOR b8) - c8 - br8) XOR d16) - A16 - br16) XOR L7) - SS7) mod 128.
An XOR with a constant and a subtraction of a constant change bit k of their input by a function of the bits below k alone, and so does the addition of 2 z, whose bit k is bit k - 1 of z; so z -> (1 + 2 z + P(z)) mod 128 is triangular with a unit diagonal, a bijection of the 128 residues, and its bit 0 is z[0] plus a constant, so the 64 odd z go onto the 64 residues of one parity. S7 holds 26 residues of each parity, so exactly 26 representatives of the block have omega mod 128 in S7, and these are the ones whose gate opens. (c) *Per context.* With B(C) the number of straddling blocks of the context and G(C) = 64 B(C), pointwise
    A(C) <= 26 (256 - B(C)) + 64 B(C) = 6,656 + (38/64) G(C).
(d) *The straddle probability.* Condition on w6, S11 and S4. The lines of step CO give c = C0.c1 = X8 + C0.d1 with X8 = ROL(X7, 7) XOR D2.b1, and b = C0.b1 = ROR(X4 XOR c, 12) with X4 = ROR(D3.b1 XOR X9, 7), where D3.b1 depends only on w6, S11 and S4; so (C0.d1, D2.b1, X9) -> (d, c, b) is a bijection, b, c and d are independent and uniform, and the outer word x = D2.a1 is uniform and independent of them. Given b, c and d, the word p of the representative, the flags hbad_i and K = b + w6 + X4 are fixed, and A = K + w2. With B = D2.b1 + W13, the context's X13 and R = S9 - IV[1], also fixed, the lines X2, D2.d1, S13, K1.c1, K1.d1, K1.a1 and w2 give
    s13 = ROL(ROL(X13, 8) XOR (x + B), 16) XOR x,   w2 = ROL(R - s13, 16) - IV[1] - IV[5].
For a fixed low half of x the high half of s13 is a constant XOR the high half of x, a bijection, and the high half of R - s13 is R[16..31] - s13[16..31] - br with br in {0, 1}, so one value of it comes from at most two values of s13[16..31], whatever br does. So each value of w2 mod 2^16, and of A mod 2^16 = (K + w2) mod 2^16, comes from at most 2 * 2^16 of the 2^32 values of x: probability at most 2 / 2^16. The cluster straddles exactly when A mod 2^16 = 2^8 p[8..15] + a with min(lo0_i, lo1_i) < a <= max(lo0_i, lo1_i), which are gap = |lo0_i - lo1_i| values, so given b, c and d it straddles with probability at most 2 gap / 2^16. H_i is uniform, b[24..31] being uniform and independent of c, and d[0..7] is uniform and independent of H_i. For H_i not 0 with t trailing zero bits, H_i XOR d[0..7] and (H_i - 1) XOR d[0..7] differ exactly in bits 0 to t, where they are complements, and the mean of their distance is 2^t; 2^(7 - t) values of H_i have t trailing zeros, for t = 0 to 7; for H_i = 0 the two bytes are complements, mean 128. So
    E[gap] = (sum over t = 0 to 7 of 2^(7 - t) 2^t + 128) / 256 = 9/2,   Pr(straddle) <= 2 E[gap] / 2^16 = 9/65,536.
(e) Summing over the 16,384 representatives, E[G(C)] <= 16,384 * 9/65,536, and (c) gives E[A(C)] <= 6,656 + (38/64) * 16,384 * 9/65,536 = 852,139/128. QED. The law of the outer words enters only in (d), as the independent uniform outer words of Lemma CX (a). The participant's arithmetic program checks (a) and (b) on 3,000 random blocks (each that does not straddle opens on exactly 26 of its 64), the bijection of (b) for 2,000 random settings of the slices, E[gap] exactly over the 65,536 pairs (H_i, d[0..7]), 294,912 / 65,536 = 9/2, the two-preimage bound of (d) for 6 random settings over all 2^16 high halves, and the bound and the budget below in exact fractions. As a check, not used here: in the declared program's run of 4,096 trials (9.2) the gate opened on 0.4024 of 131,072 clusters.
*The budget.* With s = ceil(sqrt(10 * RUN_CONTEXTS)) = 106,881,817, the opened clusters enter WB (9.1) with the budget
    A_BUDGET = ceil(852,139 * RUN_CONTEXTS / 2^7) + 16,384 * s
             = 8,114,701,346,782,505,236 + 1,808,864,247,808
             = 7,605,157,652,531,425,333.
The A(C) of the contexts of a run are independent and identically distributed, each between 0 and 16,384 (Lemma CX (a)); by Lemma OR their total has mean at most 852,139 * RUN_CONTEXTS / 2^7, and it bounds the opened count of the run. Hoeffding's inequality puts the probability that the opened count exceeds A_BUDGET at most exp(-2 (16,384 s)^2 / (RUN_CONTEXTS * 16,384^2)) = exp(-2 s^2 / RUN_CONTEXTS) <= exp(-20) < 2.1 * 10^-9. No premise enters: the budget bears on the success probability alone (10.4), and the time bound charges u_O A_BUDGET in WB, with W_CTX, whatever the words.
*The budget of straddling clusters.* The straddling clusters of a context are the G(C) = 64 B(C) of (c): the straddle flag is constant on a block, and a cluster whose gate value is 2 or 3 is a straddling one (Lemma CL). By Lemma XF (e) G(C) <= 128, and by (e) above E[G(C)] <= 16,384 * 9/65,536 = 9/4, with no premise. The G(C) of the contexts of a run are independent and identically distributed, each between 0 and 128 (Lemma CX (a)); so their total has mean at most 9 RUN_CONTEXTS / 4, and the straddling clusters of the run have the budget
    FB_BUDGET = ceil(9 RUN_CONTEXTS / 4) + 128 s = 2,742,550,203,515,344 + 14,131,751,936 = 2,570,351,266,169,534,
which Hoeffding's inequality exceeds with probability at most exp(-2 (128 s)^2 / (RUN_CONTEXTS * 128^2)) = exp(-2 s^2 / RUN_CONTEXTS) <= exp(-20). A straddling cluster adds u_O + u_F = 376 to W, of which u_O = 168 is counted with the opened clusters (A_BUDGET) and u_F = 208 enters WB as u_F FB_BUDGET and W_CTX as 128 u_F (9.1, Section 11).

## 10. The rate of a counter trial and the success probability

**10.1 The model rate.** The seven-word model M of Section 13 treats the residual of a trial as a function of seven words, E1.d1, E1.b1 and E1.a2 of message A and Y4, Y9, w8 and E3.h1. In this package Y4 is uniform in the class of eta, not in the sub-class, and the other six are independent uniform words, so M has 2^192 * 2^19 = 2^211 inputs. Under M the rate of the class is 85074516985129 / 524288 = 162,266,763.66 (Section 13): a trial has R = 0 with probability that number times 2^-128. The part of a value beta of E1's first-half b difference in it is written r(beta); the part of beta* is 71,698,432, and the part of the six outcomes of S that this search lists (below) is 67,633,152. A trial of Section 8 has c1 in Q* and so the difference beta* (Theorem C (iv)); under M the event that c1 = Y11 + E1.d1 lies in Q* has probability 2^-11 and is the event that the difference is beta* (Lemma S1). The rate at which a trial that M conditions on c1 in Q* has R = 0 with an outcome of S is therefore
    p = 2^11 * 67,633,152 * 2^-128 = 138,512,695,296 * 2^-128 = 1,032 * 2^-101,
about 2^-90.989. It is 853.61 = 2^9.738 times the model rate of a trial of the class.
*The outcomes of beta*.* In the count of Section 13 an outcome of beta is a pair (tau, eps) of the differences of E1's a and c outputs. For an outcome j of beta*, L_j is the number of triples (E1.c1, E1.b1, E1.a2) of words for which E1 on A and on B (6.2) gives the differences beta*, tau_j and eps_j; and N3_j is the number N3 of step 3 of the count for that outcome: the number of quadruples (Y4, E3.h1, Y9, w8), Y4 in the class, for which E3 on A and on B gives the differences eta and tau_j XOR ROR(tau_j, 1) of its first-half d and b values and tau_j and eps_j of its c and a outputs. Every input of the 2^211 of the model falls into one outcome, so r(beta*) = sum over j of L_j N3_j / 2^83. Beta* has fourteen outcomes on the class, all with eps = 6e21be55; this search lists the six of S, j = 1 to 5 and 7:

| j | tau | L_j | N3_j | L_j * N3_j / 2^83 |
| ---: | --- | ---: | ---: | ---: |
| 1 | 175020a0 | 562,949,953,421,312 | 108,086,391,056,891,904 | 6,291,456 |
| 2 | 185020a0 | 2,251,799,813,685,248 | 72,057,594,037,927,936 | 16,777,216 |
| 3 | 275020a0 | 562,949,953,421,312 | 18,014,398,509,481,984 | 1,048,576 |
| 4 | 285020a0 | 2,251,799,813,685,248 | 108,086,391,056,891,904 | 25,165,824 |
| 5 | 385020a0 | 1,125,899,906,842,624 | 144,115,188,075,855,872 | 16,777,216 |
| 6 | 675020a0 | 140,737,488,355,328 | 4,503,599,627,370,496 | 65,536 |
| 7 | 685020a0 | 562,949,953,421,312 | 27,021,597,764,222,976 | 1,572,864 |
| 8 | 175060a0 | 281,474,976,710,656 | 6,755,399,441,055,744 | 196,608 |
| 9 | 185060a0 | 1,125,899,906,842,624 | 9,007,199,254,740,992 | 1,048,576 |
| 10 | 275060a0 | 281,474,976,710,656 | 1,125,899,906,842,624 | 32,768 |
| 11 | 285060a0 | 1,125,899,906,842,624 | 13,510,798,882,111,488 | 1,572,864 |
| 12 | 385060a0 | 562,949,953,421,312 | 18,014,398,509,481,984 | 1,048,576 |
| 13 | 675060a0 | 70,368,744,177,664 | 281,474,976,710,656 | 2,048 |
| 14 | 685060a0 | 281,474,976,710,656 | 3,377,699,720,527,872 | 98,304 |
| sum, S: j = 1 to 5 and 7 (listed) | | | | 67,633,152 |
| sum, j = 1 to 7 (the seven of the program) | | | | 67,698,688 |
| sum, all fourteen | | | | 71,698,432 |

The rows j = 1 to 7 have the L_j of the sub-class of entry 26ebba63 and four times its N3_j, so on this scale they carry exactly its 67,698,688 = 1,033 * 2^16. S leaves out row 6, 675020a0, with 65,536 = 2^16, and carries 67,633,152 = 1,032 * 2^16, so p = 1,032 * 2^-101 exactly; the rows j = 8 to 14, with bit 14 of tau set, add 3,999,744, 5.6 per cent of the part of beta*, and are not listed either. The integers L_j and N3_j are those of the participant's counting program, printed in Section 17 with the six rows of its output that this search lists; it prints L_j N3_j / 2^81, four times the last column, and the six listed rows sum to 270,532,608 = 4 * 67,633,152 there, and the scale 2^83 is that of a trial with Y4 uniform in the 2^19 members of the class. Of the 52 values of tau that pass the screens of the count, 30 have N3_j > 0 and 14 have L_j N3_j > 0. The count uses no rule on h1.
*Why S.* S = 5f is part of the stated advice record of Section 12, and what the analysis uses of it is verified here: its count, 67,633,152 = 1,032 * 2^16 (the table above, Section 17), its certificate with SHARE and E_COUNT (Section 8) and its charge (Section 11). It is not claimed to be least under Section 11; the historical SEL procedure described for provenance in Section 12 chose it under the ledger of entry 415e792c.
*Why beta*.* Beta* = 18b0e098 is a value of the stated advice record, and what the analysis uses of it is verified here: its cube of c1, k = 11 fixed bits, mask 0e09818b and value 0c008000 (Theorem C (iii) and (iv)), and its fourteen outcomes on the class with their counts (the table above). It is the beta of the solution with which the solver found the six constants.
**10.2 Lemmas on the counter sampler.** The following lemmas were proved by GPT Sol 6.1 for this construction, Lemma S9 by GPT Sol in its answer AC, and are given with their hypotheses; each is exact mathematics under the hypotheses stated. The participant compared Lemmas S1 to S4 and Lemma IP with the construction line by line; the carry Lemma S5 was not re-derived by the participant. They do not prove the rate of H1' or the success probability; 10.3 states what remains a premise. The proofs of Lemmas S1 and S9 hold for any fixed set of members; here the set is the class.
**Lemma S1 (conditioning the model).** *Hypotheses:* under M the six words E1.d1, E1.b1, E1.a2, Y9, w8 and E3.h1 are independent uniform words, independent of Y4, which is uniform in the class; c1 = Y11 + E1.d1. *Statement:* c1 lies in Q* with probability 2^-11, and that is the event that E1's first-half b difference is beta*. Conditional on it, E1.d1 is uniform on Q* - Y11, E1.b1 and E1.a2 keep their independent uniform laws, and (Y4, Y9, w8, E3.h1) keeps its law and stays independent of (E1.d1, E1.b1, E1.a2). Hence, with G_S the event that R = 0 with an outcome of S, Pr_M(G_S | c1 in Q*) = 2^11 Pr_M(G_S and c1 in Q*) = 2^11 * 67,633,152 * 2^-128 = p, the last step by the count of 10.1.
*Proof.* Translation by Y11 makes c1 uniform and independent of every other coordinate. By the identity of the proof of Theorem C (iv), c1 lies in Q* exactly when the difference is beta*, and Q* fixes 11 bits of c1, so the probability is 2^-11. The event depends on E1.d1 alone, so for every event G1 of the words of E1 and G3 of the words of E3, Pr_M(G1 and G3 | c1 in Q*) = Pr_M(G1 | c1 in Q*) Pr_M(G3). No independence of the output differences inside E1 or inside E3 is used. QED. The finite counts behind 67,633,152 are those of the counting program of Section 17 and are not proved by this lemma.
**Lemma S2 (the outer chart).** *Hypotheses:* y and c1 are fixed; the seven outer words are independent uniform words; the names obey the assignments of step CO, with flags 3 and v[13] = 0. *Statement:* the seven outer words are in bijection with the seven context words (C0.c1, C0.d1, D3.d1, S15, S9, w5, X2) of Section 4. These are therefore independent uniform words, and their law does not depend on c1 or y.
*Proof.* Given the context words, these assignments, which are lines of steps O and M of Section 4 with flags 3 in place of 11, return the outer words: S2 = K2.a1 + K2.b1 + w5; S14 = ROR(K2.d1 XOR S2, 8); D3.a1 = ROL(D3.d1,16) XOR S14; D3.b1 = X3 - D3.a1; D3.c1 = S9 + D3.d1; S4 = ROL(D3.b1,12) XOR D3.c1; S3 = D3.a1 - S4; X14 = ROR(D3.d1 XOR X3, 8); X9 = D3.c1 + X14; K3.d1 = ROL(S15,8) XOR S3; w6 = (ROL(K3.d1,16) XOR 3) - IV[3] - IV[7]; S11 = IV[3] + K3.d1 + S15; X8 = C0.c1 - C0.d1; D2.b1 = ROL(X7,7) XOR X8; D2.a1 = X2 - D2.b1 - W13. Substituted into K2, D3, K3 and D2 they return w5, D3.d1, S9, S15, X2, C0.c1 and C0.d1, and the lines of step CO, run on the outer words they return, give the context words back. Both maps are inverse bijections between two sets of 2^224 elements, and the uniform law is carried to the uniform law. QED.
**Lemma S3 (two independent offsets).** *Hypotheses:* those of Lemma S2. *Statement:* (w5, D3.a1, Y12, S15, X2, X8, C0.d1) is another chart of the outer words, so these seven are independent uniform words; in particular Y12 and w5, which E1 reads, are independent uniform words.
*Proof.* The chart is reached by replacements of coordinates, each a bijection with the other coordinates held fixed: (w6, S11) by (S3, S15), with inverse K3.d1 = ROL(S15,8) XOR S3, w6 = (ROL(K3.d1,16) XOR 3) - IV[3] - IV[7], S11 = IV[3] + K3.d1 + S15; (D2.a1, D2.b1) by (X2, X8), with D2.b1 = ROL(X7,7) XOR X8 and D2.a1 = X2 - D2.b1 - W13; (S3, S4, X9) by (D3.a1, S4, S14), with inverse D3.b1 = X3 - D3.a1, D3.d1 = ROR(S14 XOR D3.a1, 16), X14 = ROR(D3.d1 XOR X3, 8), D3.c1 = ROL(D3.b1,12) XOR S4, X9 = D3.c1 + X14, S3 = D3.a1 - S4; S14 by w5, with S2 = K2.a1 + K2.b1 + w5 and S14 = ROR(K2.d1 XOR S2, 8); at fixed D3.a1 and S14, S4 by X4, with inverse X9 = ROL(X4,7) XOR D3.b1, D3.c1 = X9 - X14, S4 = ROL(D3.b1,12) XOR D3.c1; and last, with C0.c1 = X8 + C0.d1, X4 by Y12, with C0.b1 = (Y12 + C0.c1) XOR ROL(y,7) and X4 = ROL(C0.b1,12) XOR C0.c1. The composition proves the chart and the uniform law. It says nothing about the independence of Y12 and w5 from functions that also depend on them, such as the residual. QED.
**Lemma S4 (a marginal and the physical conditioning).** *Hypotheses:* those of Lemmas S2 and S3, and c1 independent of the outer words. *Statement:* (a) At each fixed c1 and y, E1.a1 and E1.a2 - E1.b1 are independent uniform words. (b) For two members c1 and c1' of Q* in one outer step, put m4 = ROL((c1 - Y11) XOR (c1' - Y11), 16); then the difference of their values of E1.a2 - E1.b1 is m4 - 2 (E1.a1 AND m4), E1.a1 being that of c1, and conditional only on the value of E1.a2 - E1.b1 at c1 it is uniform on the values m4 - 2 s, s a submask of m4 AND 7fffffff, which are all different. (c) Let a baseline sampler draw t as a uniform 32-bit word, t = 0 included as an algebraic trace, with flags 3, the same constants and the same outer words, and solve c1 from it; then c1 is uniform and independent of the outer words and y, and the sampler of Section 8, c1 uniform in Q*, is exactly the baseline conditioned on c1 in Q*: for every event of the trace, its probability under the sampler of Section 8 is 2^11 times the probability under the baseline that it happens and c1 lies in Q*.
*Proof.* (a) By Lemma S3, Y12 and w5 are independent uniform, so E1.a1 = ROL(E1.d1,16) XOR Y12 and w5 are, and E1.a2 - E1.b1 = E1.a1 + w5 by E1's fifth assignment; replacing (E1.a1, w5) by (E1.a1, E1.a1 + w5) is a bijection. (b) The same outer words give c1' the first value E1.a1 XOR m4 and the same w5, and (X XOR m4) - X = m4 - 2 (X AND m4) modulo 2^32. Conditional on the first value, E1.a1 stays uniform, its bits under m4 AND 7fffffff give the uniform law stated, and different submasks below 2^31 have different doubles. (c) By Lemma IP, c1 -> t is a permutation for every outer step and y, so a uniform t makes c1 uniform and independent of them; conditioning on c1 in Q*, an event of probability 2^-11, leaves the outer words and y unchanged, and step CT run forwards from c1 is the same trace. QED. Statement (c) is about the construction's own sampler and does not identify it with M; it lets an event include t != 0 but does not say how much of the rare success mass the rule t != 0 removes.
**Lemma S5 (a carry prescription).** *Statement:* let x, s, s', a and d be words of w bits with (x + s) XOR ((x XOR a) + s') = d. Every bit i < w - 1 at which a and d differ is determined by the lower bits of x and by the constants; so at most 2^(w - n1) words x solve the equation, n1 being the number of bits of (a XOR d) AND (2^(w - 1) - 1).
*Proof.* Write u_i and u'_i for the carries into bit i of the two additions. Equality at bit i gives a_i XOR d_i = s_i XOR s'_i XOR u_i XOR u'_i. If its left side is 1, exactly one of the pairs (s_i, u_i) and (s'_i, u'_i) has unequal bits; the carry out of that addition is its variable input bit, x_i or x_i XOR a_i, and the carry out of the other addition is its fixed common bit. Equality at bit i + 1 prescribes the XOR of the two carries out, which fixes x_i. Counting the choices from the low bits to the high bits gives the bound; bit w - 1 has no next bit, which is why it is left out. QED.
**Lemma S8 (success from a mean and a factorial moment).** *Statement:* let N_o be a count with values in {0, 1, ..}, mu = E[N_o] > 0 and rho = E[N_o (N_o - 1)] / mu. Then Pr(N_o > 0) >= mu b(rho), where b(rho) = (2 r_o - rho) / (r_o (r_o + 1)) and r_o = floor(rho) + 1; for 0 <= rho <= 1 this is 1 - rho / 2, and b decreases with rho. If the outer steps of a run are independent and each has mean at least mu and ratio at most rho, the probability that some outer step has N_o > 0 is at least 1 - exp(-mu b(rho) times the number of outer steps).
*Proof.* For integers r_o >= 1 and z >= 0, the indicator of z > 0 is at least (2 r_o z - z (z - 1)) / (r_o (r_o + 1)): with equality at z = 0, and for z >= 1 the inequality is (z - r_o)(z - r_o - 1) >= 0, which holds for integers. Taking expectations gives the first statement. For independent outer steps, the probability that none has N_o > 0 is the product of the values 1 - Pr(N_o > 0) of the outer steps, at most exp(-mu b(rho) times their number). QED. The proof uses only that the units are independent and that each count takes values in {0, 1, ..}; it holds as well for the contexts of 9.8, with the count N_c of a context in place of N_o (10.3).
**Lemma S9 (the success mass lies on passing outer steps; GPT Sol, answer AC).** (a) *No hypothesis.* In every outer step that does not pass the filter, the count N_o of H1' (10.3) is zero. Let pi_o be the probability that an outer step of step 1 of 9.1 passes the filter, the share of the 2^256 values of its random word whose outer step passes. If pi_o > 0, then E[N_o | the outer step passes] = E[N_o] / pi_o. (b) *Hypotheses:* those of Lemma S1. Under M, also conditional on c1 in Q*, Y9 and omega = Y3 + Y4 + w8 are independent uniform words, and the filter passes with probability pi. G_S, the event that R = 0 and the E1 outcome is in S, has probability p under M given c1 in Q* (Lemma S1 and the count of 10.1), and it lies inside the event that the filter passes. So Pr_M(G_S | c1 in Q* and the filter passes) = p / pi = 1,032 / (279,070,422,111 * 2^53), about 2^-81.011, and Pr_M(the filter passes | c1 in Q*) times this conditional rate is p: conditioning on the pass loses no part of p.
*Proof.* (a) A listed good trial has R = 0 with an outcome of S, so by Lemma F its outer step passes; N_o is a count that is zero off the event that the outer step passes, and E[N_o] = pi_o E[N_o | the outer step passes]. (b) Under M, Y9 and w8 are independent uniform words, independent of Y4; for fixed Y4, w8 -> omega is a translation, so (Y9, omega) is uniform on all 2^64 pairs and independent of Y4, and Lemma S1 leaves the law of (Y4, Y9, w8, E3.h1) unchanged under c1 in Q*. The proof of Lemma F uses only the assignments of E3 and the conditions of R = 0, which hold for the model words, so it gives the inclusion; by 10.1 p is the part of the outcomes of S. Dividing by the probability pi of the pass gives the conditional rate. QED. Statement (a) uses the pass probability pi_o of the sampler itself; that pi_o equals pi is not proved (H4'). Statement (b) is about M and says nothing about the sampler.
*The search lists exactly the listed good trials.* The two lemmas below concern the search of 9.1. Lemma V follows from 3.3 and is the participant's; Lemma CV rests on the constants and guards of 9.4, proved by GPT Sol, among them the parity certificate (P*) and Lemma J0, which hold for every joint root on the class.
**Lemma V (the certificate of a root).** Fix an outer step, a word c1 in Q* and an outcome j of beta*, and let h be E3.h1 of the trial. The trial has R = 0 with E1 outcome j exactly when E1 on A and on B gives the XOR differences tau_j and eps = 6e21be55 of its a and c outputs and h satisfies the joint conditions (J1), (J2) and (J3) of outcome j (9.4).
*Proof.* Write tau, eps and beta for the XOR differences between A and B of E1's a output, c output and first-half b value, and eta, psi, tau' and eps' for those of E3's first-half d and b values and its c and a outputs, as in Section 13. beta = beta* because c1 is in Q* (Theorem C (iv)), and eta = 830303cf (Theorem C (iii)). By 3.3, R is formed from o[1] = Z[1] XOR Z[9], o[3] = Z[3] XOR Z[11], o[4] = Z[4] XOR Z[12] and o[6] = Z[6] XOR Z[14], where Z[1], Z[6], Z[11] and Z[12] are the a, b, c and d outputs of E1 and Z[3], Z[4], Z[9] and Z[14] those of E3. The first two values of E1 are the same for A and B (proof of Theorem C (iv)), so the d and b outputs of E1 differ by ROR(tau, 8) and ROR(beta XOR eps, 7); by the last three assignments of E3, its b and d outputs differ by ROR(psi XOR tau', 7) and ROR(eta XOR eps', 8). So R = 0 exactly when tau' = tau, eps' = eps, psi = tau XOR ROR(tau, 1) and eta = eps XOR ROL(beta XOR eps, 1), the conditions of Section 13. For E1 outcome j, tau = tau_j and eps = 6e21be55, and the last condition holds: 6e21be55 XOR ROL(18b0e098 XOR 6e21be55, 1) = 830303cf. As in the proof of Lemma F, with h' = h XOR eta, g' = Y9 + h' and f' = ROR(y XOR g', 12), psi = f XOR f' = ROR(g XOR g', 12), so psi = sigma_j exactly when (J1) holds. Then f' = f XOR sigma_j and the a output of E3 on B is (omega + DY3) + f', so eps' = eps exactly when (J2) holds. Then the d output of E3 on B is ROR(h XOR eta XOR e2 XOR eps, 8) = h2 XOR mu and g' = g XOR theta_j, so tau' = tau_j exactly when (J3) holds. QED.
**Lemma RC (the root certificate; GPT Sol, answers CF 6 and 6.1).** Fix an outer step, an outcome j of S and a word h, and let c1 be the word that step 3 of 9.1 computes from h, that of the trial with E3.h1 = h (Lemma IP). The four tests (Q), (A), (C) and (T) of step 3 hold exactly when c1 is in Q*, t is not zero, and E1 on A and on B (6.2) gives the XOR differences tau_j and eps = 6e21be55 of its a and c outputs.
*Proof.* The lines of step 3 are those of step CT read backwards from E3.h1 = h, so they give the trial's Y14, Y6, E1.a1, E1.d1, c1, E1.b1, E1.a2 and t. (Q) is the definition of Q*, and (T) is t != 0. Suppose (Q), and write a1, d1, c1, b1, a2, d2, c2 for the assignments of E1 on A and primes for B (6.2). E1 on B has the same a, b and d inputs and the same first message word, so a1' = a1 and d1' = d1; its c input is Y11' = Y11 + DY11, so c1' = c1 + DY11; and b1' = b1 XOR beta* (Theorem C (iv)), which is b1 + beta* - 2 s with s = b1 AND beta*. With its second message word w5 + fffffff8, a2' = a2 + Delta(s), Delta(s) = beta* - 2 s - 8 (as in 9.7). Now a2 XOR a2' = tau_j exactly when a2 + Delta(s) = a2 XOR tau_j, that is when Delta(s) = (a2 XOR tau_j) - a2 = tau_j - 2 (a2 AND tau_j) modulo 2^32, that is when 2 (a2 AND tau_j) = (tau_j - Delta(s)) mod 2^32. Since tau_j[31] = 0, 2 (a2 AND tau_j) is below 2^32, and tau_j - Delta(s) = tau_j - beta* + 8 + 2 s is even, as tau_j and beta* are; so this is (A). Given (A), a2' = a2 XOR tau_j, so d2 = ROR(d1 XOR a2, 8) = z and d2' = ROR(d1 XOR a2', 8) = z XOR ROR(tau_j, 8); with c2 = c1 + d2 and c2' = c1' + d2', c2 XOR c2' = eps is (C). The same identities give (A) and (C) back from the two differences when c1 is in Q*. QED. The lemma uses no law of the words; with Lemma V it says that a root is certified exactly when it is the E3.h1 of a listed good trial of outcome j.
**Lemma CV (coverage of the search).** Fix an outer step that passes the filter, with T = X AND VMASK[nu] of 9.7. (a) When T is not empty, step 2 of 9.1 returns every joint root that satisfies (G7) and (G15) of every outcome whose bit is set in T, each once, and nothing else. (b) Run over the whole list, step 3 certifies exactly the roots that are the E3.h1 of a listed good trial of the outer step, and the E3.h1 of every listed good trial of the outer step is among the roots; when T is empty the outer step holds no listed good trial (Lemma VP). Hence a passing outer step has as many certified roots as its count N_o of H1' (10.3), the number of its listed good valid trials over all of Q* (none when T is empty), and N_o <= 16.
*Proof.* (a) A leaf yields a root only if (J1), (J2) and (J3) hold as words, so each returned word is a joint root of the outcome with which it is returned. Conversely, take a joint root h of a searched outcome, with h satisfying (G7) and (G15). By (PHASE), (P*), Lemma J0, the guards (G7) and (G15) and the constants and guards of 9.4 its bits take those values, and its carries pass every test of (a), (b) and (e) there: its own carry into bit 20 is a kept guess, every kept guess reaches the common state at depth 7, and the single traversal follows the arcs of its bits from the carry pairs that its own carries give, each read from the array of its position with the guard values that its own bits give (at position 15 its prefix passes the test of (G15) and the prescribed bit is its h[15]), and reaches its leaf, where the three conditions hold. A depth-first traversal reaches each node once, so h is returned once. No word is a joint root of two outcomes (9.4). (b) Let c1 in Q* give a listed good trial with outcome j, and let h be its E3.h1. By the proof of Lemma F, h witnesses (1)_j for Y9 and the trial's f witnesses (2)_j for omega, so bit j - 1 is set in both masks, and by Lemma VP it is set in T; in particular T is not empty. By Lemma V, h satisfies (J1) to (J3) of outcome j, so it is a joint root; Lemmas G7 and G15 give (G7) and (G15) for it, and by (a) step 2 returns it. Step 3 maps it to c1, since it computes the inverse of the permutation c1 -> E3.h1 of Lemma IP; c1 is in Q*, its t is not zero and its E1 outcome is j, so the root is certified (Lemma RC). Conversely, by Lemma RC a certified root h of outcome j gives a c1 in Q* with t not zero whose E1 differences are tau_j and eps, and h satisfies (J1) to (J3), so by Lemma V the trial of c1 has R = 0 with outcome j: it is a listed good trial. Different roots give different c1 (Lemma IP), and no outer step has more than 16 roots (9.4). QED.
So in every passing outer step that it reaches, the search of 9.1 certifies precisely the listed good valid trials that an enumeration of all of Q* in that outer step finds, with the same outer steps, the same members y and the same filter. The count N_o of every outer step is the same, and with it the joint law of the counts of the outer steps of a run: H1' is about these counts, H4' about two counts of the outer steps, H5_exec about the ledger of the calls that the pre-check keeps and H_G_cluster about the batches with an E lane, and none of them changes. No law of the words is used by Lemmas V, RC, VP, G7, G15 and CV. The guards of the solver are lossless: (PHASE) and (P*) are consequences of exact counts of the class, (P*) with a count of 0 for the other parity in every phase and every outcome (9.4), and Lemma J0 is algebra; none drops a member or a joint root. The pre-check and the guards (G7) and (G15) lose no listed good trial (Lemmas VP, G7 and G15), and walking the outer steps by contexts changes no outer step (Lemmas CX and MB).
**10.3 Heuristics.**
The four premises H1', H4', H5_exec and H_G_cluster below concern the instance that the stated advice record of Section 12 fixes: the six constants of 3.2, eta = 830303cf, beta* = 18b0e098 with its cube, the outcomes of beta* with the filter's values of tau and eps, and S = 5f. Each is a statement about the run for this record and for no other. How the nonuniform advice was found is outside the claimed algorithm; Section 12 preserves that history only as provenance.
**Heuristic H1' (score-critical).** The coins of the run are its RUN_CONTEXTS independent fresh words (step 1 of 9.1); each gives the seven outer words of one context, and every context walks all 2^19 members of the class, except those of clusters that hold no listed good trial (9.8, 9.9, Lemmas CX and CL). Let N_o be the number of listed good valid trials (9.1) of one outer step, counted over all of Q* whether or not the outer step passes the filter or the pre-check, and let N_c be the sum of N_o over the 2^19 outer steps of a context. (i) *Rate:* for a uniform outer step U, whose seven outer words are uniform and whose member is uniform on the class, independently (the outer step of entry 415e792c), E[N_o(U)] >= (2^21 - 1) q, with q = FACTOR * 2^-128, just under 97p / 100, about 2^-91.126; by Lemma CX (c), E[N_c] = 2^19 E[N_o(U)]. (ii) *Dependence, with the context as the unit:* the probability that no valid trial of the run is a listed good trial is at most exp(-0.49594) + 0.001; that is, listed good trials are not clustered, neither among the trials of one outer step nor among the outer steps (members) of one context, beyond what this bound allows.
This is the premise of entry 415e792c, rate and dependence, restated for the walk by contexts as entry e9b6649e restates it: part (i) is the same statement, since N_c is a sum over the whole class (Lemma CX (c)), and part (ii) is stated for the contexts, the independent units of this run. Neither the filter, nor the pre-check, nor the guards (G7) and (G15) change it: they skip only outer steps, outcomes and words that hold no listed good trial (Lemmas F, VP, G7 and G15), so N_o is the same count, pointwise.
In the terms of Lemmas S1 to S4 the premise is this: the construction's pushforward of the uniform outer words and members, with c1 running over all of Q*, onto the seven model words (E1.d1, E1.b1, E1.a2, Y4, Y9, w8, E3.h1) carries at least the share FACTOR / 138,512,695,296, just under 97/100, of the complete-success integral p of the conditional law of Lemma S1; that stays true after the member with t = 0 is dropped (Lemma IP); and the dependence between trials that share a context, in one outer step or in two outer steps of it, is weak enough for the stated success at the declared run length. The two parts are separate: neither follows from the other, and neither follows from the model or from Lemmas S1 to S5, S8 and S9. The factor FACTOR = 134,357,314,437 is assumed; 10.1 gives what it is set against, the count 138,512,695,296 of the six outcomes of S, of which it is 97/100 rounded down. The filter does not change it. The evidence for this margin is the preregistered scaled-down run of Section 13, whose one-sided 97.7 per cent lower bound on the realised share of the predicted collisions is 0.99213, above 10/11; it is evidence at 8 bits, not a proof at 32.
*The rate on passing outer steps.* By Lemma S9 (a), N_o is zero on every outer step that the filter rejects, so (i) says E[N_o | the outer step passes] >= (2^21 - 1) q / pi_o, with pi_o of Lemma S9. Per member of Q* of a passing outer step the rate is then at least about q / pi_o; for pi_o = pi it is q / pi = 134,357,314,437 / (279,070,422,111 * 2^80), about 2^-81.148: the rate of H1' divided by the pass share, with no part of the counted mass lost (Lemma S9). The success argument below uses (i) per context and needs no value of pi_o; pi_o enters only the pass budget (H4').
*What is proved and what is not.* Proved (Lemmas S2 to S4): the outer words of a step are uniform in the chart of the seven context words of Section 4; Y12 and w5 are independent uniform words; E1.a1 and E1.a2 - E1.b1 are independent uniform words at every fixed c1; and the sampler of Section 8 is exactly the uniform-counter sampler conditioned on c1 in Q*. Proved as well (Lemmas V, RC, G7, G15 and CV, 10.2 and 9.7): in every passing outer step that it reaches, the search of 9.1 certifies exactly the listed good valid trials of the outer step, so N_o is the same count for it as for an enumeration of all of Q*. Not proved: that E1.b1, E1.a2, E3.h1, Y9 and w8 have the model's joint law with the rest; GPT Sol 6.1 reduces part (i) to one success-weighted density of seven words that the outer step fixes, Y12, Y1 + w12, C2.b1, C2.c1, w5, Y9 and w8, and that density has not been counted. Not proved either: how much of the success mass the member with t = 0 carries (Lemma IP bounds the number of dropped trials, one in 2^21, not their mass), and the dependence inside an outer step and across the members of a context.
*Part (ii) for contexts.* The contexts of a run are independent and identically distributed (Lemma CX), and by part (i) the run has RUN_CONTEXTS * E[N_c] = RUN_STEPS * E[N_o(U)] >= RUN_STEPS * (2^21 - 1) * FACTOR * 2^-128 = 0.4959400000... >= 0.49594. Lemma S8, applied to the contexts with N_c in place of N_o, therefore gives part (ii) as soon as rho_c = E[N_c (N_c - 1)] / E[N_c] is at most 0.0065: in that case b(rho_c) >= 0.99675, Lemma S8's exponent is no less than 0.4943281, and exp(-0.4943281) < 0.609981 < exp(-0.49594) + 0.001. Write N_c as the sum of the counts N_o(m) of the members m of the context. Then
    rho_c = rho_w + rho_x,  rho_w = E[sum over m of N_o(m) (N_o(m) - 1)] / E[N_c],
                            rho_x = E[sum over m != m' of N_o(m) N_o(m')] / E[N_c],
where, by Lemma CX (c), rho_w equals E[N_o(U) (N_o(U) - 1)] / E[N_o(U)], the factorial ratio of a uniform outer step that the clause of entry 415e792c bounds, and rho_x is the part that pairs of different members of one context add. Both are at least zero, so rho_c <= 0.0065 implies rho_w <= 0.0065: *the clause of this package is stronger than the per-step clause of entry 415e792c*. It contains that clause and adds the dependence across the members of a context, which the member loop creates by letting 2^19 outer steps share their seven words.
*Part (ii) is an assumption.* That rho_c <= 0.0065 is assumed. It is not measured, and it cannot be measured at full size: a context holds a listed good trial with probability at most E[N_c] = 2^19 E[N_o(U)], about 2^19 * 2^21 * 2^-91.126 = 2^-51.126, so no run of feasible length sees one in a context, let alone two. The margin is wide. Write v for the clustering ratio of listed good trials by context, rho_x = v * (2^19 - 1) E[N_o(U)], so that v = 1 when the listed good trials of different members of a context are independent; then rho_x is about v * 2^-51.126, and the clause fails only if v exceeds about 2^44, or if one listed good trial makes another in the same context, at the same member or at another, far more likely than its rate.
*What is known of it.* An outer step has N_o <= 16 (Lemmas CV, G7 and G15), so rho_w <= 15, which does not help at this run length. GPT Sol 6.1 proves the bound 2^-13 for rho_w in a model in which E1.b1, E1.a2 and E3.h1 are drawn afresh for every member of Q*, and proves as well that the construction's own pair law is not of that kind (for two members of one outer step the second member's three words take at most 2^62 values given the first's, not 2^96), so that bound does not transfer. For v, the participant measured the same ratio, (E[n(n-1)]/E[n]) / ((2^19 - 1) p) for the count n of an event in a context and its share p per member, for every event that a listed good trial meets and that is frequent enough to count, each run with a control arm of independent outer steps (Section 13). From the filter to the roots of the solver it stays between 1.14 and 1.25 (the controls near 1), and it does not grow with depth; the factor comes from condition (2), whose omega = Y3 + y + w8 has w8 fixed by the context. A preregistered run went deeper, to the two halves of a listed good trial, over 262,144 contexts and 2^46 trials per arm: the cross-member factor Rx is 0.999 +- 0.054 (upper limit 1.162) for the listed E1 outcome at 2^-32.29 per trial and 0.90 +- 0.24 (upper limit 1.94) for (J1) and (J2) of the E3 half at 2^-34.58, and every upper limit lies at least 43 bits below the 2^43.86 that the clause allows. The joint event, about 2^-91 per trial, is not reachable, so carrying Rx near 1 to it remains the premise, and v itself is not measured.
*No budget for steps 2 and 3.* Whenever an outer step reaches them, whatever its words, the joint solver returns no more than 16 roots and steps 2 and 3 cost no more than CM(T) <= 15,012 machine units (9.4, 9.7, Section 11), which the meter debits from the credit as they run, exactly that work, after a preflight against CM(T) (Lemma ME); the final pair is formed and hashed at most once, for a certified root (Lemma V). The run halts with failure only when W exceeds WB, which needs one of the six counts of 9.1 above its budget: the E count or the pass count, which H4' covers, the fill count, which H_G_cluster covers, the call count, which H5_exec covers, or the opened count or the straddling count, which Lemma OR bounds with no premise (9.9); when the credit does not cover the CM(T) of an outer step, which H5_exec covers, or after the last context, which H1' covers.
**Heuristic H4' (supporting; GPT Sol, answers AW 3 and 5 and CK 2).** For an outer step of the run, before any halt, let I_E be 1 when the mask of (2) of its omega meets S and I_2 be 1 when its mask X is not zero (it passes the filter, Section 8); let N_E and N_2 be the sums of I_E and I_2 over the RUN_STEPS outer steps. H4' says: for a uniform outer step U (that of entry 415e792c), and hence for the mean over the outer steps of one context (Lemma CX (c)), Pr(I_E(U) = 1) <= 1.000026 p_E and Pr(I_2(U) = 1) <= 1.000176 pi, where p_E = 233,715,456 / 2^32 = 2^-4.199822 is the exact share of words omega that pass the automaton of (2) for S and pi = 279,070,422,111 / 2^48 = 2^-9.978162 the exact share of pairs (Y9, omega) that pass the filter (Section 8), both for uniform independent words. The two indicators of one outer step may depend on each other in any way. The factors are not proved: Y9 and omega of a uniform outer step are not proved independent and uniform.
*Use (proved, given H4').* The contexts of a run are independent and identically distributed (Lemma CX), and N_E and N_2 are sums over the RUN_CONTEXTS contexts of per-context counts between 0 and 2^19. Under H4' their means are at most 1.000026 RUN_STEPS p_E and 1.000176 RUN_STEPS pi, and the budgets of 9.1 exceed these means by 2^19 s, s = ceil(sqrt(10 * RUN_CONTEXTS)). Hoeffding's inequality over the contexts, with range 2^19, puts the probability that a count exceeds its budget at most exp(-2 (2^19 s)^2 / (RUN_CONTEXTS * 2^38)) = exp(-2 s^2 / RUN_CONTEXTS) <= exp(-20) for each. No law of the members inside a context is used. The number of outer steps that reach the solver has no clause here: its budget and the credit that pays the solver follow from H5_exec. A count above its budget can make W exceed WB and halt the run with failure; the time bound charges WB + W_CTX and is not affected.
*Evidence and the choice of the factors.* Our preregistered sample of Section 13 (prereg7, 2^39 real outer steps of the whole class) counted 29,915,698,553 lanes with a nonzero mask of (2), against 29,915,578,368 at p_E, and 545,067,537 passing outer steps, against 545,059,418.18 at pi. For a proposed mean p0 = alpha p and m = 2^39 p0, the lower-tail Chernoff bound for k events, Pr(N <= k) <= exp(-(m - k)^2 / (2 m)), is at most exp(-7) when (m - k)^2 >= 14 m. On the grid of one part per million, alpha_E = 1,000,026 / 1,000,000 and alpha_P = 1,000,176 / 1,000,000 are the least factors that pass this test: in exact rational arithmetic each passes and the factor one part per million lower fails. Under independent draws a true share above the declared bound would have produced counts this low with probability below exp(-7) for each. The sample's words come from a pseudorandom generator (Philox4x32-10), so this is evidence for the declared factors, not a proof; every other measured share of the two counts, with and without the member loop, lies between 0.998 and 1.001 times its nominal value (Section 13).
**Heuristic H5_exec (supporting; GPT Sol, answer CK3; GPT-6 Astra, Batch 11).** For an outer step of the run, before any halt, its *ledger* U is that of 9.7 for its call of steps 2 and 3: A(T) = 614 + 2,304 F + 1,354 r plus the unit cost of every block that the joint solver with (G7) and (G15) and the certificate execute on the words of the outer step, for the outcomes T = X AND VMASK[nu] that its pre-check keeps; U = 0 when T is empty, in particular when the outer step fails the filter. The premise is that of entry 50d28015, stated on the ledger of this row, whose searched rows are charged 1,354 (9.7) and whose global part is 614: for a uniform outer step (that of entry 415e792c), and hence for the mean over the outer steps of one context (Lemma CX (c)), the mean E[U] is at most 1.01 * u_U, where u_U = 335,060,079,487,497 / 2^48 = 1.1903725... is the mean of U over all outer steps, passing or not, with the zeros counted, in model M below. It is a statement about the joint law of all the words that the solver reads, not about T alone, and it is not a consequence of H4'.
*The model value.* Model M draws Q = Y9, E = omega, C2.c1, C2.b1, Y1 + w12 and Y12 as independent uniform words and the member uniformly from the class, independently, and computes nu, the pre-check, the guards and every other word from them as the search does. In M a call happens when the filter passes and nu is 3 or 4, with probability p_call = 279,070,422,111 / 2^50, a quarter of pi (9.7), and then T is the mask X with probability n_X / 279,070,422,111, n_X the counts of the certificate of Section 8. The part of U0 paid per call and per row, A(T) + 410 = 1,024 + 2,304 F + 1,354 r, has the exact mean

| X | n_X | A(X) |
| --- | ---: | ---: |
| 01 | 18,637,049,340 | 4,682 |
| 02 | 96,560,460,360 | 4,682 |
| 04 | 18,637,049,340 | 4,682 |
| 08 | 5,457,993,021 | 4,682 |
| 10 | 56,709,878,706 | 4,682 |
| 12 | 57,936,276,216 | 6,036 |
| 18 | 4,792,384,116 | 6,036 |
| 40 | 10,830,033,396 | 4,682 |
| 42 | 5,943,311,010 | 8,340 |
| 52 | 3,565,986,606 | 9,694 |

E_M[A(T) | call] = 1,431,155,678,957,082 / 279,070,422,111 = 1365342094/266237 = 5128.29..., as the participant recounted it in integers from the certificate. GPT-6 Astra proves in M, from exact counts of the rows that survive the setup of 9.4 and bounds on the nodes and leaves that use only coordinates that are fresh at each node, that the blocks of the trees add at most 22422672/266237 = 84.22... per call; that proof is cited, not reproduced here. Hence E_M[U0] <= p_call (1365342094/266237 + 22422672/266237) = 727,329,595,507,749 / 2^49, exactly. By Lemma CP, U = U0 - 410 in every call, so E_M[U] = E_M[U0] - 410 p_call <= (727,329,595,507,749 - 205 * 279,070,422,111) / 2^49 = 670,120,158,974,994 / 2^49 = u_U, exactly. Model M is a model: it is not proved that the sampler gives its words that law, and H5_exec states the bound, with the factor 1.01, for the sampler.
*Use (proved, given H5_exec; GPT Sol, answers CK3 3 and 4 and D13).* In every call the meter debits V = U, 0 <= V <= CM(T) <= 15,012 (Lemma ME). Let D_C be the sum of the debits over the 2^19 outer steps of a context, taken without halts: the D_C of the contexts of a run are independent and identically distributed (Lemma CX), each between 0 and L_C = 15,012 * 2^19 = 7,870,611,456. Under H5_exec their total has mean at most m_C = 720,081,801,874,515,573,539 >= 1.01 * RUN_STEPS * u_U, and, since D_C^2 <= L_C D_C, a variance of at most L_C m_C. With t = ceil(sqrt(40 L_C m_C)) + 14 L_C = 15,056,649,072,501,387, expansion gives t^2 >= 40 L_C m_C + (40/3) L_C t, and Bernstein's inequality bounds the probability that the total exceeds m_C + t = 720,096,858,523,588,074,926 by exp(-t^2 / (2 L_C m_C + (2/3) L_C t)) <= exp(-20); the exponent is 20.00. The run debits in order and stops at the first halt, so outside that event the credit left before any call is at least CREDIT - (m_C + t) = 15,012 >= CM(T), every preflight passes, and the credit never halts the run. V = U holds pointwise (Lemma ME), so no second premise enters; no law of the members inside a context is used. That E[U] is at most 1.01 u_U is not proved.
*The call budget (proved, given H5_exec; GPT Luna 5.6, answer D25).* A call has U >= 4,272 (Lemma CP), and an outer step without a call has U = 0, so its call indicator is at most U / 4,272. Under H5_exec the calls of a run have mean at most m_C / 4,272; their counts per context, taken without halts, are independent and between 0 and 2^19 (Lemma CX), and CALL_BUDGET exceeds that mean by 2^19 s, so Hoeffding's inequality puts the probability that they exceed CALL_BUDGET at most exp(-2 s^2 / RUN_CONTEXTS) <= exp(-20). Calls above their budget can make W exceed WB and halt the run with failure; the time bound charges WB + W_CTX and is not affected.
*Evidence.* A participant measurement (Section 13): on 2^32 real outer steps with the lines of the searched instance and as many with flags 11, with fresh words for every step, the ledger U0 of a reimplementation of this solver, with each searched row charged 1,408, at least 54 more than in this row in every call, averaged at most 1.300375 per outer step; the ledger U of this row is at most that less 464 for each call, at most 1.1853 per outer step, against the bound 1.01 u_U = 1.2023. It is evidence from a pseudorandom generator, not a proof.
**Heuristic H_G_cluster** (historical): the mean number of fills of the masked walk in a context was at most 7,164 (B4), giving G_BUDGET. It is retired by amendment J, whose fills are prepaid in Z, U_FB and U_CONTEXT, so no fill budget remains.
*Use and evidence:* in the proof.md of 0ea30357 (10.3, Section 13).
*Status:* not a premise of this candidate.
**10.4 Success probability.** The probability space is the RUN_CONTEXTS fresh words of step 1 of 9.1, independent uniform 256-bit words, for the fixed target and the stated advice record of Section 12; the algorithm is otherwise deterministic. Under H1', H4', H5_exec and H_G_cluster it outputs a collision with probability at least 1 - (exp(-0.49594) + 0.001) - 2 * 10^-8 = 0.390001800132... > 0.39 (GPT Sol, answers AW 3 and 5, CJ 1.2, CK 2.2, CK3 4 and CM 6, with the tails of 10.3 and 9.9 over contexts). This is the union bound over the events "no valid trial is a listed good trial", "the E count exceeds E_BUDGET", "the pass count exceeds PASS_BUDGET", "the fills exceed G_BUDGET", "the calls exceed CALL_BUDGET", "a preflight fails", "the opened count exceeds A_BUDGET" and "the straddling count exceeds FB_BUDGET", which need not be independent; a halt by W needs one of the six counts above its budget (9.1): H1' bounds the first by exp(-0.49594) + 0.001; given the means of H4', H_G_cluster and H5_exec and, for the last two, with no premise (Lemma OR), Hoeffding's and Bernstein's inequalities over the independent contexts bound each of the other seven by exp(-20), and 7 exp(-20) < 1.45 * 10^-8 is below the allowance 2 * 10^-8 kept for them. A listed good trial lies in a passing outer step (Lemma F), in a cluster whose gate opens (Lemma CL), in a chunk of its cluster (Lemma XF), which its lane takes as passing (Lemmas MB and DT), whose pre-check keeps its outcome (Lemma VP) and whose solver with (G7) and (G15) returns its root (Lemmas G7, G15 and CV); the search certifies it unless the run ends before its outer step is reached, by the work register, by the credit or by the output of another pair (9.1, Lemma CV). When the algorithm outputs a pair, the pair is a genuine collision: its trial is certified, so R = 0 (Lemmas RC and V), step 3 checks both complete digests, and the messages have different lengths. The run is the shortest of this form that gives 0.39: RUN_STEPS_MIN is the fewest outer steps that give 0.49594 expected listed good trials, 0.49594 is the smallest number of five decimals for which the bound reaches 0.39 (with 0.49593 in its place the bound is below 0.389996), and RUN_CONTEXTS rounds RUN_STEPS_MIN up to whole contexts.
The heuristics are not proved; Section 13 gives the evidence for H1', H4', H5_exec and H_G_cluster.

## 11. Charged time

One 2-round target compression costs one unit, and every other primitive word operation, every load and every store included, costs 1/430 of a unit. The rows below are in operations, loads and stores, called machine units here; 430 of them make one unit of time.
*The machine.* The search is charged on the load/store machine of 6.5, with its 256-bit words, its packed lanes, its masked rotation and one unit for every operation, load and store. It has 64 registers, and every constant is an immediate operand, written in its instruction and not loaded. The cost model of the track charges primitive word operations and sets no register count; this text charges as well a load for every other word fetched from memory into a register and a store for every word written to memory, spills included. The batches of seven members, their E handlers and fills run on packed words (9.8); the context, the shortcut of a passing lane, the joint solver and step 3 run on scalar words of the same machine, one 32-bit value to a word. Every schedule of this section is an upper bound written out by blocks, after GPT Sol's answers AL 2, AQ 2, AR 3 and 6.2 to 6.6, AT 1 and 4, AW 2, 4 and 5, AX 1, CA, CD (sections 1, 3, 6, 8, 10 and 11), CF (sections 6 and 7), CI (section 1) and CJ (sections 2 to 5), and not counts of an executed program, with these exceptions: the 67 units of a batch, which participant programs executed with a count of every operation and load (9.8); and the omega side (17), PROR (5), the carry word (17), the chunk addressing (11 for the first chunk, which reuses n_0, or 6 when n_0 is 0, and 13, or 8 when it is empty, for the second), the fill (56), the pre-check (7), the preflight (6) and the additions to W (1), which a participant tool counted in the declared program of the preceding layout as it ran the public request and its self-test: every data word wrapped so that each operation, comparison, branch, load and address that the program executes on it is counted, and the counts attributed to the program's own statements; every occurrence equalled the declared count. For the rows that this layout changes, the gate words (8), the gate test (3), the state test (3), the slow path (12 with its state test), the pair of a representative batch (3) and its loop step (3), the lane tests (8 each, 7 in lane 0, a representative's included), the omega sides and lane tests of the two chunks of a cluster together (c(n_A) + c(n_B), at most 104, 9.9), the descriptor selection (6, 5 for lane 0), the broadcasts (4), the E lane (10, 9 in lane 0) and the shortcut (35, 32 for lane 0), the count is that of the statements of the program as it stands, one unit to each operation, comparison, branch and table load, four to a scalar rotation and five to a PROR; the program keeps the loop over the representative batches and its list addresses in variables (9.2). The end jump of a chunk (9.9), a transfer of the written-out code, has no statement in the program, whose chunks are a loop; it is charged in the 3 of an opened cluster and is not part of that count; nor are the entry into the one copy of an opened cluster and the return from it, which the program, with its loop, has no statement for: they are charged as the 16 of an opened cluster (9.9) and are not part of that count. The 54 of the Y9 path in a fill are the Y9 part of the executed Q path of answer CA, two of its lines fused into one (9.8).
**The cost, with every term.** Every row is machine units times an upper bound on how often a run executes it, except the counted events, charged together through the work register W: their units add up to at most WB + W_CTX (9.1). The predecessor's table of rows (context 90,917, representative batch 52, opened cluster 168, straddling surcharge 208, E lane 10, fill 56, passing lane 43, call 6, the credit and the one-time work, total 2^71.465) is historical; the current rows and units are those of the revised exact ledger of the amendment, with the derivations of A to L.
















*Why the counted rows are charged WB + W_CTX, and the credit once.* W is the sum of the units of the counted events so far, each added by one instruction in its stage. A context starts only when W <= WB and adds at most W_CTX, so W <= WB + W_CTX whenever the run halts or ends (9.1). An outer step that runs steps 2 and 3 is metered: it starts only when the credit left covers its cap CM(T) and debits at most that (Lemma ME), so the debits add up to at most CREDIT. Both are fixed numbers enforced by halts; no mean of a count of work enters the time bound.
*A context, 90,917*, bound in words. Allowances: 16 to draw the fresh word and split off the seven outer words; 158 for the 39 context lines on scalar words (20 lines contain a rotation at five units and at most one more operation, the other 19 at most two operations; a direct schedule needs 139); 24 to form the sixteen packed operands, K, K' and S15' among them, which need at most 24; 96 to copy them into seven lanes, three shift and OR doublings, 6 per operand; 128 to save up to 64 scalar names for steps 2 and 3; 16 for the context loop; 40 for the gate word AW of 9.9 with its masks, its copy into seven lanes, A[8..15] and its stored metadata; 1 for X9' = X9 + 2^34 in the packed copy of X9; 6 to form X2 + w7 and store it with its address; 2 for the test of W against the immediate WB and its branch; 16 for S2, w5 and w12 (5 + 2 + 3) and their stores with addresses; and 6 to load S6, X14 and X2 + w7 into their registers. These add up to 509. The gate adds 160 for its four flags hbad_i, stored, and AW (at most 132, 9.9) and 128 * 12 = 1,536 for the slow path of at most 128 lanes (9.9, Lemma XF (e)); the masked walk adds 48,896 for the descriptor table (9.9), 17 for the carry word of each of the 2,341 representative batches and 16 for its setup; and 3 more pay the marker 2^35 added to the packed -S0 - S5 (1) and the list address and end of the representative loop (2): 509 + 160 + 1,536 + 48,896 + 17 * 2,341 + 16 + 3 = 90,917. The premiums of the straddling clusters are paid through W (9.1). The context leaves W as it is: W runs over the whole run.
*A partner batch or chunk, 72* (9.8; GPT Sol, answers CA, CD 1, CJ 3 and D9): 17 for the omega side (two rotations at five units, each with an XOR, and five single operations) and 8 per lane test (7 in lane 0): the shift that moves the lane to lane 0, the AND that keeps the marker and the low 16 bits of omega, the load of R2, the AND that keeps omega, the addition, the load of L2, the comparison and the branch. Under J and L a chunk A or pending lane pays 8 for the test of (1) instead, and the test of (2) only after a nonzero mask (1).
*A representative batch and an opened cluster* are derived in 9.9 (historical 52 and 168) and amended by A to L (55, 43 for the last; U_HEAD and U_LIVE).
*An E lane, 10, and a fill, 56* (9.8; GPT Sol, answers CA, CD 1, 6 and 8.1 and CM 5A). The E handler: 1 to add to W, 1 to shift the cached Y9 to lane 0, 1 to keep 2^34 + (Y9 mod 2^16), the address of R1, 1 to load it, 1 to keep Y9 mod 2^26, 1 to add, 1 to load L1 (Lemmas DT and T26), and 3 to combine the masks, compare and branch. The fill: C0.a1 and D0.d1 rebuilt (2) and the Y9 path (54). Under J and L these remain for representative lanes; chunk A and pending lanes read (1) first (L), and fills are prepaid (J).
*A passing lane, 43, and a call, 6, outside steps 2 and 3*: 35 for e1, C2.a1, C2.d1, C2.c1, C2.b1 and the word r' by the shortcut of 9.6 (32 for lane 0); 7 for the pre-check of 9.7; and 1 for the addition to W on either side of the pre-check, u_P where it ends the outer step and u_P + u_C where it falls through: 43, paid by every passing lane, also when T is empty. A call adds 6 for the preflight of 9.7, the address and load of CT[T], A(T) and CM(T) taken out, the comparison with the credit register and the branch: 6. The lane is written inline after its E handler and keeps no return link; the call and return edges of steps 2 and 3 are inside the global ledger (below). W and the credit stay in their registers, and the global ledger saves the live words of the batch around steps 2 and 3.
*Steps 2 and 3 (historical allowances 614, 2,304 per family, 1,354 per row and per-node charges with CM(T) <= 15,012) are superseded by amendment E: CM(T) <= 7,115.*
*The meter and CM(T) (Lemma ME; GPT Sol, answers CD 11.3, CK3 2 and 3 and D12; our audit).* Every T that occurs lies inside a mask X of Section 8 (T is X or empty), and each of the ten masks X lies inside one of the four sets of rows of 9.4, {275}, {175}, {285, 385} and {185, 385, 685}, so the nonempty T that occur are the nonempty subsets of these four sets. The predecessor's table of A(T) and CM(T) under the allowances above (CM(T) <= 15,012, with equality on 185, 385 and 685) is historical; under amendment E, `frontline.py` computes A(T) and CM(T) for every T from the emitted charges and the trees of 9.4 and asserts CM(T) <= 7,115. V = U in every call (9.7). The meter needs no premise: its debits are the unit costs of the blocks that a call executes, whatever its words.
*Registers of steps 2 and 3*. The search of 9.4 is written out statically for each row and each prefix of free choices: a node at a prescribed position has at most one child, whose code follows that of its parent, and a leaf label jumps to the leaf check; a node at a free position, at most five on a path, saves its parent in one register, the prefix of h and, above bit 32, the two carries and the bit e2[29], the only earlier output bit that a later guard reads (the guard of position 25 reads bit 13 of the prefix). The registers of the traversal are the 32 descriptors, five saved parents, six context words, eight constants, array bases and control words, two words of the current state and ten temporaries: 63 of the 64; the 64th holds the remaining credit (9.7), and no other register holds a copy of it. A leaf keeps the descriptors and the saved parents and uses the others for its check, after which the context words are reloaded (the 16 above). The certificate of a root and the test of (G15) use only the ten temporaries. For the certificate, t is formed first; then the live values fit seven temporaries in each phase: Y14 with at most four loaded words; Y6, E1.a1, E1.d1, c1, E1.b1, s and a loaded word; E1.a2, E1.d1, c1, s, p and a test word; z, c1, two sums and z XOR ROR(tau_j, 8). One more temporary takes the shifted part of a rotation, which is formed first so that a rotation may overwrite a source that dies, one holds an address and one a comparison. The prefix h is read without overwriting the protected word of the current state. For (G15): the five words, an accumulator, the temporary descriptor, a test word, an address and a prefix temporary. On both outcomes every other register of the traversal is kept as it was, with no spill. The formulas of a family run before the descriptors are built, in at most 58 registers: at most 35 bits and carries, five source and context words, eight table, literal and control words and ten temporaries. The stores into the bank of the global ledger run before that, with the live words of the batch already saved, so the 63 registers other than the credit's are free for them; the bank is memory, and only the five source words of a family are live when its formulas run. No register is addressed by a value: every position and register is named in the code.
*Once.* R1 and L1 are charged 2^25, and R2, L2 and PXR with the class maps 2^27 (Lemma DT), as the seven lanes of the earlier layout were. The member lists of 9.9, in cluster order, are charged 2^26 + 2^20: for each of the 2^19 members, the deposit of its 19 bits at the free positions of e1, at most 3 units a bit, 57; the subtraction of Y3 and the rotation by 7, at most 6; and for each of the two lists the shift of the value to its lane and the OR into the packed word, 2, with the store of each packed word and its address, below 2 per member; and the loop, 3: below 2^7 units per member, below 2^26 for the lists; and at most 64 units per cluster, 2^20 in all, to place its representative and its five partner words; and 2^20 for the broadcast words, two for each representative, each its member word copied into seven lanes by three shifts and ORs and stored with its address, below 64 units per cluster. The six static rows of the outcomes of S, with the static fields of their descriptors at the 32 positions and the metadata of the batches, are charged 2^20. 2^26 for the two automata of the filter for the seven outcomes, built and composed into eight byte tables whose entries hold the base address of the next table, with the entries of the last tables ANDed with S: their states at each of the 32 bits are images of those of the fourteen-outcome automata, at most 146, so the allowance of answer AN 2 covers them. 2^26 for the three transition arrays of 9.4: their 2^18 entries at most 256 operations each, the enumeration of the keys, both candidate arcs, the test for an invalid or a second arc, the selection, the shift of the entry to its field and its OR into the packed word included, and the store of each of the 2^15 words. 2^26 for writing the code of the search: 432 static nodes over the six rows of S, with the prescribed bits of (G7) and (G15) at positions 7 and 15, fewer than 2^14 labels, at most 256 operations each with their set-up. And 2^26 for the row metadata, the absolute bases of the arrays and their initialisation, a fourth allowance that GPT Sol keeps for safety, which also covers the enumeration of the compatible patterns of 9.7 and the 128 words of CT, below 2^23 operations. 2^50, the once-only reserve of GPT Sol's answer AW 5 for the exact mask histograms, the model means and the table CT, charged in full whether or not it is used. 32 for loading the resident constants and array bases into their registers and 8 for the test of the final halt. 2^20 for each of eleven parts of the earlier layout: the E count in a register; the root certificate, with the immediates of the rows and at most 1,024 units to form the last blocks of the first returned pair; (G15), with its unrolled code and the layout of its five words; the global ledger, with its bank and labels; the labels of the gate; the representative's T2 test on opening; the pointer and end constants of the list pairs; the frame of 9.9; and the constants of the budgets and the credit, of the run and of the opening bound. Three more of 2^20 (answers CK2 1, CK3 2 and 4 and CM 5A): the constants of the credit bound; the meter, with the packed words of CT, the immediates of the block debits and the preflight; and the cache with its fill code. Fourteen more of 2^20 for the layout of this row: the frame of 9.9 in registers (three), the save of the batch words in the global ledger, the guard words from its bank, the pass count in a register, the credit in its register, the pre-check with immediates, the shortcut of 9.6, X9' with R1 at 2^34, the gate words, the interleaved lists, W with its test, and the meter without slack. Two of 2^22 for the code of the opened cluster, written once, and of the passing lanes written out after their E handlers, and 2^29 for writing out the body of the representative loop and the last batch with them, an allowance kept from the layout that wrote an opened cluster at each representative lane site: fewer than 2^23 instructions at most 2^6 units each, and the code now holds 233,459 instructions (Sections 12 and 19). And 2^34 for the finite checks of Lemma OR (9.9), an allowance kept although the 128 residues of (b) and the 65,536 pairs of (d) need far less. And 2^28 + 2^20 for the masked partner walk: 2^28 for its finite certificate alive16 and its constant tables, PX among them, and 2^20 for its layout generator and metadata. The gate table, the lane replicas of T2', T1 and the gate table, PXF', the three rotation tables and BT of the earlier layout are not built: the gate value and the rotations are computed and the broadcasts are read from the member lists (9.6, 9.9).
*One-time items.* The items above are in the last row. The final step, once: steps CT and CS for the trial found, the release of 9.1 step 3, which executes no word operation and adds nothing, writing the two messages, shorter than 2^42 bytes each, a chunk at a time, and two complete evaluations of blake3, streamed the same way; each message has at most 2^32 chunks of 16 compressions each and fewer than 2^32 parent compressions, below 2^37.1 compressions for both, and writing them is below 2^38 machine units: below 2^38 units of time in all. Preprocessing includes the fixed deterministic setup itemised in *Once*, 1,125,918,437,277,736 machine units already present in the search rows, and a conservative charge for all historical work that constructed the 73-byte advice. The retained construction allowance is S_old = 5,486,510,246,044,225,536 machine units, below 2^53.503 target-compression units. It accounts for the completed searches, model processing, exact counters and later replay; it is not a premise that a fresh capped replay returns the record. Thus preprocessing_log2 = 54.
Total: the search rows, S_old and the 430 * 2^38 numerator of the final step give 430 T = N of the revised exact ledger of the amendment, and time_log2 is log2(N / 430) rounded up at the fifth decimal, certified there in integers; the historical totals of this section (2^62.62567 and its integers) are superseded. The bound holds in the worst case for the algorithm as stated: every run halts with its counted events within WB + W_CTX, within its credit and within its RUN_CONTEXTS contexts, and steps 2 and 3 are bounded in every outer step that reaches them. No mean of a count of work enters it, since CREDIT is a fixed number enforced by a halt; H1', H4', H5_exec, H_G_cluster, H_LZ and Lemma OR bear on the success probability only. The claim rests on this 64-register schedule: no figure for 16 registers is claimed, and this schedule is not claimed to be the cheapest.
Nothing is sorted and nothing is looked up by value: each root is tested against the conditions of its own outcome, and no certified trial is compared with another. The reads at positions that words give are: per batch, the words U[b] and E[b]; per used lane of a partner batch or chunk, the entries of R2 and L2 of its lane at its omega, and in a representative batch, for a lane that takes the slow path of the gate, the stored flag hbad_i; per opened cluster that is not a straddling one, PXR next to its representative's address of R2, its two broadcast words and the words n_0, n_1 and JU of its descriptor; per E lane, the entries of R1 and L1 at its Y9; per opened cluster, the R2 and L2 entries of its representative; per passing outer step, the three names stored for the shortcut and, when T is not zero, CT[T]; in an outer step that reaches the solver, the names saved for its context and the bank, the packed words of the transition arrays at the keys of the searched rows, the five words of (G15) of each searched row, the family records and the static rows of the outcomes. Every such read is charged as one load: a partner batch counts its 14 loads of R2 and L2 inside its 72 units, the opening of its cluster the 10 loads of its partner pairs or the loads of PXR, of the broadcast words and of the descriptor, a representative batch its 2 list loads inside its 52, the slow path its load of hbad_i inside its 12, an E lane its loads of R1 and L1 inside its 10, and the loads of a context, of a passing lane, of the joint solver and of step 3 are inside the allowances above. No table grows with the trials.

## 12. Memory, preprocessing and advice

The program of the search is the lines of steps CO, CT and CS, the outer filter, the walk of 9.8 and 9.9, a loop over the representative batches of a context whose body is written out with, at each representative lane site, its gate test and the entry into one copy of the code of an opened cluster, and the passing lanes inline, the last batch written out after the loop with the same entry, the joint solver of 9.4 with its statically written traversal and the guards (G7) and (G15), and a compression routine for step 3 and the final check. Its size: a lane site has fewer than 2^8 instructions, its lane test 8, its E handler with the fill 66, its passing lane 53 and the call of steps 2 and 3; a batch of n lanes, a not-ready chain of n lane sites with a ready tail after each, has n (n + 1) / 2 lane sites, at most 28, and its omega side; an opened cluster, its five old batches with 4 * 28 + 6 = 118 lane sites and, for each of its two chunks, the seven dispatch leaves for n = 1 to 7 with 1 + 3 + 6 + 10 + 15 + 21 + 28 = 84 lane sites, 286 in all, with its omega sides, dispatch and slow path, fewer than 2^17 instructions, and its return tree of 38 targets, at most 2 * 38 < 2^7, written once: fewer than 2^17 + 2^7; the body of the loop, at most 28 representative lane sites, each with its lane site, its gate test, state test, slow path, descriptor selection, broadcasts and entry, fewer than 2^9 instructions, and the one copy: fewer than 28 * 2^9 + 2^17 + 2^7 = 145,536; the last batch, at most 10 such sites, fewer than 10 * 2^9 = 5,120; these lane sites, the one copy and the last batch are kept as bounds, 145,536 + 5,120 = 150,656 instructions; the joint solver, the context, the entry stubs of steps 2 and 3 with the global ledger and the routine of step 3 are counted from the program that emits them (Section 19): 17,267 instructions; the rest (the outer filter's table walk, the loops of the walk and the gate, the table and list builders), fewer than 2^16: fewer than 2^6 pieces of fewer than 2^10 instructions each, the builders of the tables, lists, automata, transition arrays and CT, the loops of the walk and the gate, and blocks of immediates; a builder or loop has a straight-line body charged above at no more than 2^8 units an iteration, so no more than 2^8 instructions, and a block of immediates is one instruction a word; a bound, as 2^20 was, not an emitted count: 150,656 + 17,267 + 2^16 = 233,459 instructions, 7,470,688 bytes at 32 bytes an instruction. Data, one word of 256 bits each unless said otherwise, at fixed word addresses: at the word addresses f of Lemma DT, R1 at f = 2^34 + l, R2 at f = 2^35 + l and PXR at f = 2^35 + 2^16 + l for l < 2^16, L1 at f = 2^34 + 2^26 + s + 2^16 h' for s < 35 and h' < 2^10, and L2 at f = 2^33 + s + 2^16 h for s < 4 and h < 2^16: 2^16 + 2^16 + 2^16 + 35 * 2^10 + 4 * 2^16 = 494,592 words, each at an address f with 2^33 <= f < 2^36; from 2^36 + 1, the member lists with their broadcast words, 201,290 words; the 29,952 entries of the tables of the filter's two automata; the three transition arrays of 9.4, packed eight entries of 32 bits to a word, 2^15 words (2^13, 2^13 and 2^14); fewer than 4,096 words for the joint solver (the descriptors of the positions of a row, the six static descriptors of S, the records of the families, the bank of 32 words of Section 11 and scratch); fewer than 1,024 words for the names of step CO, the stored names and the four flags hbad_i of a context, the saved words of a batch, the five words of (G15) of each row, the constants and masks, the 128 words of CT and the cells of step 3; 89 words for the class maps of Lemma DT (the classes of the 7 + 43 states and the first states of the 4 + 35 classes); in the last 2^13 words below 2^36 + 2^24, PX, 512 words; from DB = 2^36 + 2^30 to below 2^36 + 2^30 + 2^26, the descriptor table of a context, 64 descriptors of 8 words at the addresses DB + a(IX) + 128 b8 + 256 [W mod 128 in S7] (9.9). Every word from 2^36 + 1 on is below 2^37, so none is a word of the tables, which lie below 2^36. The memory of the program is counted as the words it holds, stored and not yet released, not as its highest address; the code is counted at 32 bytes an instruction. Nothing grows with the number of trials.
**Memory, phase by phase.** The program has two phases, separated by the release of step 3 (9.1); no word is held across it except the routine of the final step and its words. Every count below is of words held; a word is 32 bytes.

| Phase | Held | Words | Bytes |
| --- | --- | --- | --- |
| Search (step 0, steps 1 to 3 up to the release) | R1 and L1, 2^16 + 35 * 2^10 | 101,376 | |
| | R2, L2 and PXR, 2^16 + 4 * 2^16 + 2^16 | 393,216 | |
| | subtotal of the tables (Lemma DT) | 494,592 | 15,826,944 |
| | member lists with their broadcast words 201,290; automata 29,952; transition arrays 2^15 words; joint solver fewer than 4,096; names, flags, constants, CT and cells fewer than 1,024; PX 512; descriptor table of a context 64 * 8 = 512; class maps 89 | fewer than 270,243 | fewer than 8,647,776 |
| | code, 233,459 instructions (Sections 12 and 19) | | 7,470,688 |
| | **search phase** | | **fewer than 31,945,408** |
| Release | nothing is stored; the search's words and code are given up | | |
| Output (rest of step 3) | one chunk word of 1,024 bytes, from which the t zero chunks of F are produced, one at a time, and written or hashed | 32 | 1,024 |
| | the two digests | 2 | 64 |
| | routine of the final step (lines of steps CT and CS, the compression, the tree of blake3, writing and output), fewer than 2^12 instructions | | fewer than 131,072 |
| | its words: A, B, t, c1, the names it reads, the block, the state and the stack of at most 33 chaining values, fewer than 128 | fewer than 128 | fewer than 4,096 |
| | **output phase** | | **fewer than 136,256 < 2^17.05597** |
| Historical advice construction | solver working set, bounded CNF and record files | | at most 37,928,960 = 35,651,584 + 1,228,800 + 1,048,576 < 2^25.17680 |

The peak is the historical advice construction: at most 37,928,960 bytes, and 37,928,960^100000 < 2^2517680, so memory_log2_bytes = 25.17680. The attack search phase holds fewer than 31,945,408 bytes and the output phase is below 2^17.05597. The phases are never held together: the messages are produced only after the release, which reads and writes nothing, and the historical construction ran separately. The final step holds no message: blake3 reads a message chunk by chunk, so the step produces each zero chunk of F in its chunk word, compresses it at its counter and pushes its chaining value on the stack of at most 33, and reuses the chunk word for the next; the last chunk A or B is in its words; it compares the two digests and then writes the pair to the output in the same way, a chunk at a time, never reading back a written chunk. A message written to the output is not a word that the program holds, and no output byte is read again. The time of Section 11 is unchanged by the streaming: each byte is written once and each compression runs once, as the final step is charged.
**The advice record.** The search reads a fixed record, stated here in full, which this package treats as nonuniform advice: the six constants X3 = bf1c5f38, X7 = c0e3a0c8, X11 = c4036000, X15 = c0c5fb02, W4 = 7ffffffa and W13 = 00074004 of 3.2, 24 bytes; eta = 830303cf, 4 bytes; beta* = 18b0e098 with the mask 0e09818b and the value 0c008000 of its cube, 12 bytes; the seven values of tau of the filter's automata, 175020a0, 185020a0, 275020a0, 285020a0, 385020a0, 675020a0 and 685020a0, and eps = 6e21be55, 32 bytes; and the mask 5f of S, 1 byte: 73 bytes, so nonuniform_advice_log2_bytes = 7.
The success analysis of 10.3 and 10.4 uses only properties of this stated record, and this text verifies each of them exactly, whatever the way the record was found: Fact P, the equal d and b outputs of C3 for W4 and W4' (3.2); Lemma Q, the class of eta with exactly 524,288 members; Theorem C (iii) and (iv), by which c1 gives the difference beta* exactly when c1 AND 0e09818b = 0c008000; the fourteen outcomes of beta* on the class, all with eps = 6e21be55, and the count 67,633,152 = 1,032 * 2^16 of the six of S (10.1, with the program of Section 17); the certificate of the filter for S, with SHARE and E_COUNT (Section 8); and, for the search itself, the allowed patterns of the pre-check (9.7) and the guards, trees and caps of the joint solver for this class and S (9.4, Lemmas J0, G7 and G15, Section 11). H1', H4', H5_exec and H_G_cluster are stated for this record (10.3). Nothing in the success analysis depends on how the record was found, on a selection returning it, or on any record of the runs that found it.
**Historical advice-construction provenance.** The advice record was found by three deterministic generator, Kissat and exact-counter attempts. This history is preserved so that later work can trace the constants, but it is not an algorithmic phase, a heuristic premise, or evidence required by the claim. The submitted attack takes the 73-byte record above as nonuniform advice and verifies the exact properties it uses. The three observed terminal statuses were `counter_cap`, `counter_oom` and `counted`; attempt 2 returned beta `18b0e098`, eta `830303cf`, the stated seven-word model and exact part 71,698,432. The selected CNF SHA-256 is `797e10698bcda6a75025dc38e832b8fee464096df5808b03d77f012f76eda2ee`; selected model SHA-256 `29b9bbdd5f62db12adaf00764ceabcb585cfa0cf67a134719cb0aaf559f3c907`; Kissat SHA-256 `20cbb879177d7395631cdd9b01cf238a8db172b828927cf77f540a5cc6caeef0`; counter source SHA-256 `fa70205c25e5b6b4552a7c36ce38ef37dba5b083734294dfb33539bde3863694`. Their construction work is conservatively charged by S_old in `time_log2` and `preprocessing_log2`, and their bounded peak is included in `memory_log2_bytes`. The success analysis does not depend on replaying them or on any selector returning the record within a cap.
The direct tables R1, L1, R2 and L2, PXR and the member lists with their broadcast words, like the descriptor tables, the tables of the filter's automata, CT, the three transition arrays, the descriptors and the traversal, are not advice: they are computed from the record. SHARE and E_COUNT are counts from the certificate of Section 8, the metered caps of CT are computed from the trees, and the budgets and the credit of 9.1 are computed from them, from u_U, from the bound 7,198 of H_G_cluster, from the factor 1.01 of H5_exec and from the other constants of 9.1. The flags 3 and the counter rule are part of the algorithm. There is no other stored data and no stored collision.

## 13. Evidence, scope and field meanings

Throughout this text costs and bounds are rounded up, and margins, rooms and the whole numbers of the count that the claim uses are rounded down. Counts printed with decimals are rounded to the nearest.
**What is exact.** Sections 2 to 5, 7 and 8; Lemmas L, H, Q, Q2, T, T2, N, TR, CT, IP, F, J0, V, RC, VP, G7, G15, CV, FX, CP, Y, CX, DT, MB, KP, A9, CL, XF, OR and ME and Theorem C; the count of passing pairs of Section 8 and the allowed patterns of the pre-check and the table CT of the metered caps (9.7); the parity certificate (P*), an exact count, and the constants and caps of the joint solver (9.4) with its schedule (Section 11), as upper bounds, with the meter's debit equal to the ledger; the flat mean 1365342094/266237 of model M, recounted in integers; and Lemmas S1 to S5, S8 and S9 under their stated hypotheses. The tree part 22422672/266237 of the bound on the mean of U0 is GPT-6 Astra's bound in model M, cited and not proved in this text; H5_exec declares the number u_U itself, so neither the time bound nor the statement of the premise depends on that proof. The declared experiment
`frontline-search` executes the search of 9.1 on one context per organizer seed (9.2) and returns a pair of the root instance of
the same lines, whose two digests the organizer recomputes; Theorem C predicts that every pair agrees on the 128 masked digest bits (6.4). The counter instance itself has no organizer-run digest check (6.4).
*How it was checked.* The participant's checks are computations, not proofs: the counter construction against the organizer's own functions on 2,000 trials and complete messages hashed by the organizer's code (Section 7); the declared program's in-run references and self-test (9.2, 9.3); all 2^21 members of Q*, each giving the difference beta*; the free positions, static trees, families and caps of the solver against the counts of 10.1 (9.4); the word nu of the pre-check against 324,098 real trials (9.7); the member lines and pass decisions of the member loop and the omega-first batch against the full outer step (9.8); and the finite checks of Lemmas A9, CL, XF and OR against the word equations (9.9). No person has read any part of this text.
**The seven-word model.** By 6.2 the residual of a trial, of the root instance or of the counter instance, is a function of the constants and of seven 32-bit words: for E1 its first-half values d1 and b1 and its a output a2 on message A, and for E3 the words Y4, Y9, w8 and its first-half value h1 on A. The model M says that over the trials the six words other than Y4 behave like independent uniform words, independent of Y4, which is uniform in the sub-class. Under M a trial has R = 0 with probability r * 2^-128, where r * 2^81 is the number of solutions of R = 0 among the 2^209 values of the seven words with Y4 in the sub-class. Call r the *rate of the sub-class*. Rule A is a condition on h1, so under M the trials with R = 0 that satisfy rule A have a rate of the same kind, r_A, counting only the solutions that satisfy rule A; r_A is at most r. The counter search prescribes c1 = Y11 + d1 in Q*, and under M that is a conditioning on d1 (Lemma S1); its rate p is formed from the part of beta* in r (10.1). On the outer steps that pass the filter of Section 8 the rate under M is p / pi, and no part of p lies on the others (Lemma S9). M and the count give the rate of a single trial. They do not give the probability that a run has a good trial, which also depends on how the good trials of a run cluster; a model of the single trial says nothing about that.
Given M, the rates are properties of the constants, the sub-class and beta* alone and can be counted without sampling; the count says nothing about whether M holds. The six words are not free in a trial. In the counter search Y4, Y9 and w8 are fixed for the 2^21 trials of an outer step, and so are Y12 and w5, which E1 reads; the trials of an outer step differ in d1 and in what follows from it (Lemma CT (c)), and E1.b1, E1.a2 and E3.h1 move with d1. M is a statement about averages over the outer steps of a run. Lemmas S2 to S4 show which parts of it hold exactly for the construction, and H1' declares the rest. The measurements below show where M fails inside one context and inside one outer step.
**How r is counted (participant computation, not organizer-verified).** Write tau, eps, beta for the XOR differences between A and B of E1's a output, c output and first-half b, and eta, psi, tau', eps' for those of E3's first-half d and b and its c and a outputs. Because E1's a1 and d1 are the same for A and B, R = 0 holds exactly when tau' = tau, eps' = eps, psi = tau XOR ROR(tau, 1) and eta = eps XOR ROL(beta XOR eps, 1); for Y4 in the class the left side of the last equation is the constant 830303cf. The counter works in integers (128-bit unsigned integers; exact fractions for the products and sums), has no sampling branch, and needed no fallback on any outcome of the count below; no floating-point number is on the path of a figure printed below as a fraction.
1. *The betas.* beta is a function of d1 alone: with c1 = Y11 + d1 and DY11 = Y11' - Y11 = f608818b, beta = ROR(c1 XOR (c1 +
   DY11), 12). As in Lemma Q, the d1 with a given beta are a share 2^-k of all d1, k being the number of bits of the mask
   ROL(beta,12) AND 7fffffff.
2. *The outcomes of one beta.* An outcome is a pair (tau, eps); the admissible tau are enumerated with a carry automaton, with no
   bound on the weight of tau. A beta for which beta XOR ROR(eta, 1) has odd weight contributes nothing; every other has two
   candidates for eps.
3. *The E3 side.* N3 is the number of quadruples (Y4, h1, Y9, w8) for which E3 produces eta, psi, eps and tau; all of them have Y4
   in the class.
4. *The E1 side.* P1 is the probability that E1 produces tau and eps when d1 is uniform among the values with this beta and b1 and
   a2 are uniform.
5. *The sum.* For the sub-class, N3 counts only the quadruples with Y4 in the sub-class, and the part of a beta in r is 2^(15 - k)
   times the sum over its outcomes of P1 * N3, where 15 is the number of bits that Lemma Q2 fixes, so that the sub-class is a
   share 2^-15 of all Y4: the sum of N3 over all 2^96 values of (d1, b1, a2) is r * 2^81, and 2^96 / 2^81 = 2^15. r is the sum of
   the parts over all betas. Parts are not negative, so the sum over any set of betas is a lower bound for r. For r_A, N3 counts
   only the quadruples whose h1 satisfies rule A.
**The count of the class and of the sub-class (participant computation).** The count runs over the 60 words beta that have a part in the rate of the whole class, the list of entry c66f230d: of the 133,742 words that occur as beta, the 4,550 with k at most 14 were enumerated, and for the 129,192 others a SAT solver was asked whether the whole system has a solution with that beta and answered no for 129,147, without certificates. The integer enumeration of GPT Sol 6.1 over every beta finds the same 60. For the whole class the rate is 85074516985129/524288 = 162,266,763.66, from 60 betas and 453 outcomes with a nonzero product. For the sub-class of the root instance it is r = 194382080300609/1048576 = 185,377,197.55, about 2^27.47, so that under M a trial of the root instance has R = 0 with probability about 2^-100.53. A few betas carry most of the count (beta* = 18b0e098 alone 36.5% of r, the four heaviest 98.8%), so the count rests on few paths; the claim of this package uses only the part of beta* on the class (10.1).
**Checks of the counter (participant computations).** Complete enumeration with 8-bit words of every quadruple (Y4, h1, Y9, w8) through both executions of E3 and every triple of the E1 side, over random constants, classes and rules: none different from the counter. At 32 bits two functions agree on all 687 outcomes both counted; for the whole class a helper agent counted both factors of all 453 outcomes with two programs written from the definitions of 6.2 and 6.3: the same total, 85074516985129/524288, and the same parts for 60 of 60 betas.
**Measurements of the premises (participant, untrusted evidence; the organizer's harness does not run them and their programs are not in the package).** Real messages in the counter arrangement (2^45 trials, graphics card): every real trial had the difference beta*; the listed E1 outcome is 10,129 against 10,176.0 (sub-class) and 15,139 against 15,264 (both classes), the listed partial E3 event 3,626 against 3,569. A single outer step differs strongly (the trials of one outer step that satisfy rule A have a variance 572 times their mean), and only averages over outer steps agree with M. No event is deeper than about 2^-40; none is the joint event of H1', at about 2^-91.
A scaled-down end-to-end run on an eight-bit version of the hash (eight sets of toy constants fixed beforehand, every collision rebuilt as two complete messages and confirmed by two tree hashes): root instance 67 collisions against 64.0 predicted, counter with d1 in the set of the heaviest beta 251 against 255.0, control 54 against 47.8; 372 collisions, no failed check; realised fraction of the predicted gain of the prescription 0.94 +- 0.13. It tests the mechanism, not the size of the factor at 32 bits, and has no rule A, sub-class or packed batch.
The preregistered rerun, the evidence for the factor 97/100 of H1': the protocol file PREREG.txt (SHA-256 c5895dd64b07710f9fb386b0f9d4f6b5cb38b14b502a4cc80e51c60584432a4e) fixed the code, the sets, the model counts, the seeds, the size and the rule (margin m is supported when the one-sided 97.7 per cent Poisson lower bound on found / predicted is at least 1/m). One run, no interim look, 3,235,715,578,385 counted trials: 40,882 collisions against 40,800.63 predicted, 1.00199 +- 0.00496 (z = +0.40), lower bound 0.99213 >= 97/100 (0.97256 at 1-1e-9; 32-bit sub-class E1 0.9954, 2-sigma 0.9756), all confirmed as complete toy messages. It is 8-bit evidence under uniform free words; it does not test the 32-bit factor, the filter or the solver.
Real counter trials on the whole class (2^46 trials per class, graphics card; control: the sub-class of entry 26ebba63 with rule A and the seven-outcome filter): every quantity matches the exact model within 1.5 clustered standard errors, among them the E1 outcome among the seven of entry 59f8915e, whole class, 1.0020 +- 0.0086 of the model (sub-class control 1.0126 +- 0.0086), all fourteen 0.9988 +- 0.0070, and the pass rates of the filters 0.99990 +- 0.00007 and 1.00012 +- 0.00016; no excess clustering of E1 outcomes by outer step. The E1 event of S (six of the seven, 52/53 of the measured event) was not counted alone, and there is no counter of the E3 side or of the joint event of H1' (about 2^-91 per trial).
Clustering by context at every depth (made after the design, not preregistered; ratio 1 for independent members, control arm of independent outer steps): condition (1) alone 1.000175; condition (2) alone 1.1433 +- 0.0008; passes the filter 1.1513 +- 0.0009; pre-check keeps an outcome 1.1572 +- 0.0010; the solver reaches a leaf 1.153 +- 0.003; returns a root 1.2486 +- 0.0806 (control 1.0367 +- 0.0718). At the cuts of the solver between the leaf and the root the ratio stays between 1.14 and 1.25. The clustering comes from condition (2): omega = Y3 + y + w8, and w8 depends on the context only. No root of these runs passed the certificate of step 3 (0 of 763): no listed good trial is observed, and the ratio of listed good trials themselves is not measured.
Clustering of the deepest events across members, a preregistered run (PREREG.txt, SHA-256 248838947f505b89c3927b7da829548acef92a540e474a9eefe3bd04c06cb92e): 262,144 contexts per arm, each of all 2^19 members with 512 values of c1 per outer step, 2^46 trials per arm, from two generators (Philox4x32-10 and SHA-256 in counter mode); the control arm draws fresh words; Rx, the cross-member factor, is 1 for independent members. Listed E1 outcome (share 2^-32.29): Rx 0.999 +- 0.054, upper limit U 1.162 (control 1.068 +- 0.064). (J1) and (J2) of the E3 half for an outcome of S (2^-34.58): Rx 0.90 +- 0.24, U 1.94 (control 1.12 +- 0.27). R24, the low 24 bits of the difference of chaining-value word 1 zero (2^-23.76): Rx 1.0002 +- 0.0001, U 1.0006. U is Rx plus three standard errors (a jackknife over 128 groups), or the 99.865 per cent Poisson limit when fewer than 30 pairs occur. Only the filter events cluster by context (test (2) 1.1439, the pass 1.1522, control 1.0000). Every upper limit lies at least 43 bits below the factor 2^43.86 that part (ii) allows; the joint event is not reachable and the two halves are measured separately, so carrying Rx near 1 to it remains the premise.
The shares of H4', a preregistered sample (prereg7; PREREG.txt SHA-256 92d16cda1cd13aacb287470b968ff2d914362b12fefb680c94960280a7471131): the sampler is the program's outer step of the whole class as a graphics-card kernel (Philox4x32-10 words), matched to the unchanged Python code on 65,536 outer steps. The sample ran once, with no interim look, on 2^39 = 549,755,813,888 outer steps: 545,067,537 passed the filter for S against 545,059,418 expected (z = +0.35), 29,915,698,553 had a nonzero mask of (2) against 29,915,578,368, and the pre-check kept 136,255,727 of the passing outer steps, 0.249980 (z = -1.10). The factors of H4' are the least that these counts support (10.3); one pseudorandom generator, not a proof.
H5_exec on the declared program of our preceding layout (SHA-256 4f87cfe2937913258697ab7348840a526ebd1944e0d4d9c00d3ca5c06a15995c), a preregistered sample of whole contexts (PREREG.txt SHA-256 3b3fdad4108a5be903c8af5b504b538828debdb803d7dda5ffa728dec66da8b7, one-sided level 1 - 10^-6), with the ledger U0 of 9.7 charging each searched row 1,408, at least 54 more than the U0 of this row in every call: 51,549 whole contexts of 2^19 outer steps from two generators that agree on every mean per context. The ledger U0 averaged 1.294334 +- 0.002348 per outer step over 6,671,108 calls (5,243.71 per call, largest 12,764), one-sided upper bound 1.30550; less 464 for each of its 0.000247 calls per outer step (the 54 that this row saves and the 410 between U0 and U), 0.1145, the mean of the ledger U of this row is at most 1.17980 and the bound 1.19097, below 1.01 u_U = 1.202276 (u_U = 1.190373). In the same sample every exception count (guard rejects, ledger above C_G(T), meter breaches, lost or extra roots, mismatches) was 0 over 692,644,553 in-run checks. Limits: pseudorandom generators, not the law of model M.
The ledger of H5_exec on real outer steps (all 2^32 outer steps with T not zero, flags 3 and flags 11, recomputed in Python; a reimplementation of the joint solver charged U0 with each searched row at 1,408): 1,063,703 and 1,065,105 calls; mean of U0 per outer step 1.298456 and 1.300374 (standard error about 0.0013); less 464 on each call, the means of the ledger U of this row are at most 1.18354 and 1.18531, below u_U = 1.190373. Limits: the ledger counts each executed block at its upper unit cost; the solver is a reimplementation, not the declared program; one pseudorandom generator.
The fills of the retired H_G_cluster: a preregistered sample of 2^24 contexts, mean 7,159.266 (B4); details in the proof.md of 0ea30357.
The premise value moves the time bound only through G_BUDGET (8,222,804,534,398,781,475 for the declared 7,198); the Hoeffding bound holds for any law of F on [0, 84,261] and is computed from one i.i.d. sample of one generator, evidence and not a proof; the run tests the mean of F only, not H1', H4' or H5_exec.
**What does not exist.**

- No organizer-run digest check of the counter instance (6.4, Section 7): its checks are participant computations with the
  organizer's functions imported (Section 7) and the declared program's in-run step-CT compressions (9.2).
- No measurement of the joint event of H1', at about 2^-91 per trial; the deepest counter events measured are the listed E1
  outcome at 2^-31.7 and that outcome together with rule A, 55 events at about 2^-39.8. No separate count of the E1 rate of the
  six outcomes of S: it is a sub-event of the measured seven.
- No proof of the open parts that H1' declares (10.3), of the shares of the two counts of H4', of the mean of the ledger of
  H5_exec or of the mean of F of H_G_cluster; these are measured (above), the shares on a preregistered sample of 2^39 real outer
  steps.
- No measurement of rho_x or of the clustering ratio v of listed good trials by context (10.3), which no run of feasible size can
  observe; the ratio was measured for the events that every listed good trial meets, from the filter to the roots of the solver,
  and its cross-member part, preregistered, for the two halves of a listed good trial (above).
- No scaled-down run of the counter search with the outer filter or the joint solver, and no complete message of a found pair; the
  complete messages hashed (Section 7) are trials, with t from 1 to 16,383.
- No run of the search at full scale, and no root of the search itself: the declared program walks 32 clusters of one context per
  trial (9.2); its solver calls return planted roots only. Its units are added per event from the ledger; every row of Section 11
  is bounded in words, except the 67 of a batch of 9.8, which participant programs executed and counted, and the omega side, key,
  carry word, gate tests, state test, descriptor selection, broadcasts, chunk addressing, lane tests, E lane, fill, shortcut,
  pre-check and preflight of this row, which a participant tool counted in the declared program as it ran (Section 11).
**Limits of the evidence.** H1' is an assumption (10.3); beyond it:

- M fails inside one context and one outer step: the count of rule A per outer step has a variance 572 times its mean. Where it
  was measured it holds on averages over outer steps. The counter search fixes Y4, Y9, w8, Y12 and w5 for the 2^21 trials of an
  outer step; a context, in turn, holds its seven outer words fixed for all its 2^19 outer steps. Success therefore comes from
  many independent contexts, 2^50.021 of them, with 2^69.021 outer steps walked, about 2^59.04 of them passing and 2^57.04
  reaching the solver, and it rests on the premise that a context rarely holds more than one listed good trial.
- The shares of H4', the ledger of H5_exec and the fills of H_G_cluster are measured on pseudorandom generators, and the quarter
  share of the pre-check and u_U are exact only in model M; none of them is proved for the sampler. Lemmas F and VP need no law of
  the words, and the time bound needs none either: a reached budget or an exhausted credit halts the run, which lowers the success
  probability and not the time bound.
- The model is checked on real messages to about 2^-40, not at 2^-91; the scaled-down whole-collision runs of the counter
  arrangement are level (0.94 +- 0.13 of the predicted gain; preregistered, 1.00199 +- 0.00496 of the predicted count).
- The constants and the class were chosen by the count, and beta* with them, so they favour any choice that the model overrates; S
  was chosen by the charge. The six outcomes of S carry 41.7 per cent of the count of the class, with one value of eps. Most
  measurements of this section are on the sub-class and the seven outcomes of entry 26ebba63; on the whole class the E1 side of
  those seven outcomes, which contain S, was measured (2^46 trials), and their E3 side was not.
- The count rests on programs that are not in the package and on a list of values of beta that is complete only by uncertified
  solver answers and the other model's enumeration.
- Helper agents of the participant wrote and checked the counter construction, the filter and this text, and another AI model
  proved Lemmas IP, F, S1 to S5, S8 and S9 and derived the count of passing pairs; no person has read it.
The required baseline_improved identifier blake3-r2-nominal-v2 names the organizer's nominal display reference 128, not an established attack, qualified baseline or security bound; the claimed 62.62567 lies below it. Whether a qualified result improves the Yukon incumbent is decided separately; no Pareto dominance claim follows.

## 14. The records of SEL

Provenance only, not part of the attack or a premise; its work is charged by S_old, and the full run table and source hashes are in Section 14 of the proof.md of submissions 3b9c6ced and 1e179f43. The log trail5_lx.log (116 lines, SHA-256 ae0fc528b515c0fbd7b17693b79f73855fd3c15df331f5e3b2514068f7224771) has one line per run of the generator trailmin5.py (with r2_sat.py and r2_trail.py) and `kissat -q --sat --seed=S --time=T` on one core, T at most 9,000 s; the exact counter pair_calc_sub (gcc -O2, one thread) was called once per returned instance on the whole class of its eta, 65 calls, all exiting 0 with no outcome uncounted. Of the 116 runs, 84 ended by themselves (6 UNSAT, 13 at a time cap, 65 SAT) and 32 were stopped from outside; no logged wall time exceeds 9,000 s. Run 20 (lx 8, bound 104, seed 506, 4,770 s, SAT, beta 18b0e098, exact part 71,698,432) returns the record; its log line:

```text
RES model=pin-lx8 bound=104 fixed=no seed=506 t=4770s status=SATISFIABLE cost=100 x1w=13 PIN=29d4fa98,bee3af28,44036000,40c58500,97475638,0007c006 D3=fdb77cfd D11=0a08818b delta=fffffff8 Y3=8127c181 Y11=7af77f38 eta=830303cf beta=18b0e098 tau=185020a0 eps=6e21be55 parts=A1:11,A4:13,A5:21,A3:14,A6:23,A7:18 sol=27e956dc,027077ff,800817b3,e614819a,615469a6,9ff1dcb4,6fc881ad
```

## 15. Earlier entries

Entries of the participant of the inherited dossier (base f72e1782, 62.62567), from c66f230d (97.6: the constants, eta, Fact P and Lemmas L, H, Q, T, N) through e7b17fd1 (the counter construction), 26ebba63 (the program, the filter, the solver), 415e792c (S and the pre-check) and a402a477 to a08a006c (the counter search, its gate, walk, budgets and ledger); the one-line list with what each contributes is Section 15 of the proof.md of 0ea30357.

## 16. Credit

One line per contributor; the long form is in Section 16 of the proof.md of 0ea30357. Nobody named here has reviewed this package, and a credit is not an endorsement.

- **Jbenisek**: the half-collision, the class search, the counter construction (from 17bba2ae on), the guard (G7) and the inherited dossier; with **GPT Sol 6.1** and **GPT-6 Astra** (OpenAI), **Grok** (xAI), **GPT Luna 5.6** and helper agents run by Jbenisek: the cluster gate (Lemmas KP, A9, CL, OR), the masked walk (XF), the cached Y9, the omega-first batch, the meter (ME), the certificate (RC), (G7), (G15), the pre-check, the joint solver and its lemmas (F, S1 to S9, IP, FX, CP), the cuts of the masked opening and the ternary gate.
- **hecmas** (e9b6649e): the member loop and direct tables. **Th0rgal** (77818485, df8bd46d, 8c81a219): the credit at a model mean and coding steps. **winglock** (18a7fc52), **5kyguy** (404d14df), **0xshikhar** (73d5265f), **tekkac** (2bf40fb) and the participant of dd91b2f6: sub-class selection, masks and frame words in registers, the lane layout, the fourteen outcomes.
- **jungjipdo** (1e179f43): layer A. **mpjunior92** (785acf86, 034414ab, 41128eca, 0ea30357, aec9831b, fef8fa3c, e8bc190d): layers B to J; layer K is this package, written by Claude Opus 5.5 in Claude Code for that submitter.









## 17. The counting program for 67,633,152

The program below computes the part of beta* = 18b0e098 in the rate of the class of eta (Section 10.1), outcome by outcome, in exact integer arithmetic, with the standard library only: every tau (taus), both roots eps (eps_roots), the E1 count L_j (L_count) and the E3 count N3_j (N3_count), each as an exact carry count over all bit positions, with Y4 over all 524,288 members of the class (Lemma Q) and no rule on h1. Nothing is sampled, capped or delegated to a solver. It is the program printed by entry 26ebba63 with these changes only: the header comment, the member list (the class in place of the sub-class) with its size check, the empty rule, and the final check. Run as `python3 -B count.py`, it printed the outcome table below in about 2.5 minutes (Python 3.14). Its column L*N3/2^81 is four times the last column of the table of 10.1; its column "rule A" is the count with the empty rule and equals N3 in every row. Its self-test, a brute force at width 6 that follows the listing in the file, ran 12 seeds with no mismatch. The program prints all fourteen outcomes of beta* on the class and their sum; this package lists the six outcomes of S, and only their rows are shown below, in the program's order. They sum to 270,532,608 = 4 * 67,633,152 on the program's scale 2^81, that is 67,633,152 on the scale 2^83 of a trial with Y4 uniform in the class (10.1). The eight rows that are left out, 675020a0 and the seven with tau ending in 5060a0, sum to 16,261,120 = 4 * 4,065,280 and are listed, with their L_j and N3_j, in the table of 10.1; the sum and check lines of the program, which follow the rows, are those of all fourteen. This listing is a separate program, not experiments/frontline.py and not shipped; its functions are its own, and in the listing those named ror, rol, bit and solve are written cror, crol, cbit and csolve (a renaming of the program that ran, nothing else changed) so that they are not taken for those of frontline.py.

```python
# count.py of Section 17 with comments and docstrings removed (same output; run: python3 -B count.py [--beta HEX]; --selftest: brute force at width 6)
import sys, time
from collections import Counter
from functools import lru_cache
from itertools import product

class Inst:

 def __init__(s, n, r16, r12, r8, r7, Y3, Y3B, Y11, Y11B, delta, eta, Y4s, rule):
  s.n, s.m, s.r16, s.r12, s.r8, s.sh = (n, (1 << n) - 1, r16, r12, r8, r8 - r7)
  s.Y3, s.Y11, s.delta, s.eta, s.Y4s, s.rule = (Y3, Y11, delta, eta, Y4s, rule)
  s.DY3, s.DY11 = (Y3B - Y3 & s.m, Y11B - Y11 & s.m)

def cror(c, x, r):
 r %= c.n
 return (x >> r | x << c.n - r) & c.m

def crol(c, x, r):
 return cror(c, x, c.n - r % c.n)

def wt(x):
 return bin(x).count('1')

def subs(X):
 p = X
 while True:
  yield p
  if p == 0:
   return
  p = p - 1 & X

def sgn(c, p, X):
 return X - 2 * p & c.m

def pats(c, X, d):
 w = X - d & c.m
 if w & 1 or w >> 1 & ~X:
  return []
 top = 1 << c.n - 1
 return [w >> 1, w >> 1 | top] if X & top else [w >> 1]

def cbit(x, i):
 return x >> i & 1

def adv(S, base, plus_ok, minus_ok):
 return {base + cy + x - y >> 1 for cy in S for x in range(plus_ok + 1) for y in range(minus_ok + 1) if (base + cy + x - y) % 2 == 0}

def eps_roots(c, beta):
 y = cror(c, c.eta, c.sh) ^ beta
 return [e for e in (csolve(c, y, 0), csolve(c, y, 1)) if e is not None]

def csolve(c, y, x0):
 x, i = (x0, 0)
 for _ in range(c.n):
  j = (i + c.sh) % c.n
  b = cbit(x, i) ^ cbit(y, i)
  if j == 0:
   return x if b == x0 else None
  x |= b << j
  i = j

def taus(c, beta, eps):
 n, r8 = (c.n, c.r8)
 K1, K2, out = (beta + c.delta & c.m, eps - c.DY11 & c.m, [])

 def rec(t, tau, S1, S2):
  if t == n:
   for j in range(n - r8, n):
    S2 = adv(S2, cbit(K2, j) - cbit(tau, (j + r8) % n), cbit(tau, (j - 1 + r8) % n), cbit(eps, j - 1))
    if not S2:
     return
   out.append(tau)
   return
  for b in (0, 1):
   tau2 = tau | b << t
   T1 = adv(S1, b - cbit(K1, t), cbit(beta, t - 1) if t else 0, cbit(tau, t - 1) if t else 0)
   if not T1:
    continue
   T2, j = (S2, t - r8)
   if j >= 0:
    T2 = adv(S2, cbit(K2, j) - b, cbit(tau, t - 1) if j else 0, cbit(eps, j - 1) if j else 0)
    if not T2:
     continue
   rec(t + 1, tau2, T1, T2)
 rec(0, 0, {0}, {0})
 return out

def L_count(c, beta, tau, eps):
 Bc, R8 = (crol(c, beta, c.r12), cror(c, tau, c.r8))
 mult = Counter((pa for q in subs(beta) for pa in pats(c, tau, sgn(c, q, beta) + c.delta & c.m)))
 tot = 0
 for qc in pats(c, Bc, c.DY11):
  for pa, w in mult.items():
   for pd in subs(R8):
    for pc in pats(c, eps, c.DY11 + sgn(c, pd, R8) & c.m):
     tot += w * e1_dp(c, Bc, qc, tau, crol(c, pd, c.r8) ^ pa, R8, pd, eps, pc)
 return tot << c.n - wt(beta)

def e1_dp(c, Bc, qc, tau, need, R8, pd, eps, pc):
 S = {(0, 0): 1}
 for i in range(c.n):
  T = Counter()
  for (bo, ca), w in S.items():
   for x in (cbit(qc, i),) if cbit(Bc, i) else (0, 1):
    v = x - cbit(c.Y11, i) - bo
    if cbit(tau, i) and v & 1 != cbit(need, i):
     continue
    for z in (cbit(pd, i),) if cbit(R8, i) else (0, 1):
     s = x + z + ca
     if cbit(eps, i) and s & 1 != cbit(pc, i):
      continue
     T[1 if v < 0 else 0, s >> 1] += w
  S = T
 return sum(S.values())

def N3_count(c, tau, eps):
 A, E, T = (c.eta, eps, tau)
 psi = tau ^ cror(c, tau, c.sh)
 Psi = crol(c, psi, c.r12)
 B = A ^ E
 B8 = cror(c, B, c.r8)
 AE = A | E
 D1 = {}
 for ph in subs(A):
  pg = pats(c, Psi, sgn(c, ph, A))
  if pg:
   D1.setdefault(sgn(c, ph, A), ([], pg))[0].append(ph)
 D2 = [(pf, pe) for pf in subs(psi) for pe in pats(c, E, c.DY3 + sgn(c, pf, psi) & c.m)]
 if not D1 or not D2:
  return (0, 0)
 RB = 0
 for mk, _ in c.rule:
  RB |= mk
 X = A & E | E & ~A & RB
 Yc = Counter((y & Psi for y in c.Y4s))
 W = {pg: Counter() for _, pgs in D1.values() for pg in pgs}
 for pg, Wg in W.items():
  for pf, pe in D2:
   Wg[pe & X] += Yc[crol(c, pf, c.r12) ^ pg]
 tot = totA = 0
 for d1, (phs, pgs) in D1.items():
  D3 = [(pb, pt) for pt in subs(T) for pb in pats(c, B8, sgn(c, pt, T) - d1 & c.m)]
  for ph in phs:
   for pg in pgs:
    for x, y in W[pg].items():
     if not y:
      continue
     for pb, pt in D3:
      kb = crol(c, pb, c.r8)
      g = g_dp(c, pg, Psi, kb | (ph ^ x) & A & E, AE, pt, T)
      tot += y * g
      totA += y * g * rule_count(c, ph | (x ^ kb) & E & ~A, AE)
 return (tot << c.n - wt(AE), totA)

@lru_cache(maxsize=None)
def g_dp(c, pg, Psi, kfix, AE, pt, T):
 S = [1, 0]
 for i in range(c.n):
  j = (i + c.r8) % c.n
  nxt = [0, 0]
  for ca in (0, 1):
   for x in (cbit(pg, i),) if cbit(Psi, i) else (0, 1):
    for z in (cbit(kfix, j),) if cbit(AE, j) else (0, 1):
     s = x + z + ca
     if cbit(T, i) and s & 1 != cbit(pt, i):
      continue
     nxt[s >> 1] += S[ca]
  S = nxt
 return S[0] + S[1]

@lru_cache(maxsize=None)
def rule_count(c, hfix, AE):
 F = 0
 for mk, _ in c.rule:
  F |= mk & ~AE
 ok = sum((all((wt((hfix | f) & mk) % 2 == v for mk, v in c.rule)) for f in subs(F)))
 return ok << c.n - wt(AE) - wt(F)

def solvable(c, eqs, masks):
 S = {(0,) * len(eqs)}
 for i in range(c.n):
  nS = set()
  for ch in product(*[(0, 1) if i and cbit(mk, i - 1) else (0,) for mk in masks]):
   for st in S:
    nxt = []
    for (consts, coefs), cy in zip(eqs, st):
     d = cy + sum((s * cbit(w, i) for s, w in consts)) + sum((s * ch[v] for v, s in coefs))
     if d % 2:
      break
     nxt.append(d >> 1)
    else:
     nS.add(tuple(nxt))
  S = nS
  if not S:
   return False
 return True

def e3_screen(c, tau, eps):
 A, psi = (c.eta, tau ^ cror(c, tau, c.sh))
 Psi, B8 = (crol(c, psi, c.r12), cror(c, c.eta ^ eps, c.r8))
 ac = [([(1, Psi), (-1, A)], [(0, 1), (1, -1)]), ([(1, tau), (-1, A), (-1, B8)], [(0, 1), (3, 1), (2, -1)])]
 b = [([(1, eps), (-1, c.DY3), (-1, psi)], [(0, -1), (1, 1)])]
 return solvable(c, ac, [A, Psi, tau, B8]) and solvable(c, b, [eps, psi])

def beta_part(c, beta, show=print):
 tot = totA = 0
 rows = []
 for eps in eps_roots(c, beta):
  ts = taus(c, beta, eps)
  ts3 = [tau for tau in ts if e3_screen(c, tau, eps)]
  show(f'eps {eps:08x}: {len(ts)} tau pass N1 and N2, {len(ts3)} also the E3 screen')
  for tau in ts3:
   n3, n3a = N3_count(c, tau, eps)
   if n3 == 0:
    continue
   L = L_count(c, beta, tau, eps)
   show(f'  tau {tau:08x}  L {L}  N3 {n3}  N3_ruleA {n3a}')
   if L:
    rows.append((tau, eps, L, n3, n3a))
   tot += L * n3
   totA += L * n3a
 return (rows, tot, totA)

def inst32():
 Y3, Y3B, Y11, Y11B = (2166866305, 2128559742, 2063040312, 2231369923)
 W4, W4B = (2538034744, 2538034752)
 Y4s = [(51118851 | f) - Y3 & 4294967295 for f in subs(~63931139 & 4294967295)]
 rule = []
 c = Inst(32, 16, 12, 8, 7, Y3, Y3B, Y11, Y11B, W4 - W4B & 4294967295, 2198012879, Y4s, rule)
 assert len(Y4s) == 524288 and all((cror(c, (Y3 + y ^ Y3B + y) & c.m, 16) == c.eta for y in Y4s))
 return c

def main32(beta):
 t0 = time.perf_counter()
 c = inst32()
 rows, tot, totA = beta_part(c, beta)
 print(f'beta {beta:08x}: {len(rows)} outcomes with L * N3 > 0')
 print('tau       eps       L                  N3                 L*N3/2^81  rule A')
 for tau, eps, L, n3, n3a in sorted(rows):
  q, rem = divmod(L * n3, 2 ** 81)
  print(f"{tau:08x}  {eps:08x}  {L:<17}  {n3:<17}  {q:<9}{('' if rem == 0 else ' +rem')}  {('all' if n3a == n3 else n3a)}")
 q, rem = divmod(tot, 2 ** 81)
 qA, remA = divmod(totA, 2 ** 81)
 print(f'part = sum / 2^81 = {q} remainder {rem}; with rule A {qA} remainder {remA}')
 print(f'seconds {time.perf_counter() - t0:.1f}')
 return (tot, totA)
if __name__ == '__main__' and '--selftest' not in sys.argv:
 beta = int(sys.argv[sys.argv.index('--beta') + 1], 16) if '--beta' in sys.argv else 414245016
 tot, totA = main32(beta)
 if beta == 414245016:
  q83, r83 = divmod(tot, 2 ** 83)
  print(f'sum / 2^83 = {q83} remainder {r83}  (= sum / 2^81 divided by 2^19 / 2^17 = 4)')
  assert tot == 286793728 << 81 and tot == 71698432 << 83 and (totA == tot)
  print('CHECK whole class, no rule: sum / 2^81 = 286,793,728; sum / 2^83 = 71,698,432 (rival dd91b2f6)')
```

Output of that run, the outcome table restricted to the six rows of this package (the program's other lines are unchanged):

```text
beta 18b0e098: 14 outcomes with L * N3 > 0
tau       eps       L                  N3                 L*N3/2^81  rule A
175020a0  6e21be55  562949953421312    108086391056891904  25165824   all
185020a0  6e21be55  2251799813685248   72057594037927936  67108864   all
275020a0  6e21be55  562949953421312    18014398509481984  4194304    all
285020a0  6e21be55  2251799813685248   108086391056891904  100663296  all
385020a0  6e21be55  1125899906842624   144115188075855872  67108864   all
685020a0  6e21be55  562949953421312    27021597764222976  6291456    all
part = sum / 2^81 = 286793728 remainder 0; with rule A 286793728 remainder 0
seconds 141.6
sum / 2^83 = 71698432 remainder 0  (= sum / 2^81 divided by 2^19 / 2^17 = 4)
CHECK whole class, no rule: sum / 2^81 = 286,793,728; sum / 2^83 = 71,698,432 (rival dd91b2f6)
exit 0
```

**End of Section 17.**

## 18. The ledger program and its output

`ledger.py` (Python standard library; integers only) recomputes the constants, budgets and total of the current amendment (A to N) from its formulas, and prints them; it replaces the predecessors' programs, whose outputs were historical ledgers. Listing, then output:

```python
from math import isqrt, log2
cd = lambda a, b: -(-a // b)
FACTOR = 98 * 138512695296 // 100
RC = cd(cd(12359 << 128, 25000 * FACTOR * ((1 << 21) - 1)), 1 << 19)
STEPS, s = RC << 19, isqrt(10 * RC - 1) + 1
P_B = cd(1000176 * STEPS * 18289159183466496, 10 ** 6 << 64) + (s << 19)
F_B = cd(9 * RC, 4) + 128 * s
L_Z, ZMAX = 791586, 256 * (41 + 10 + 8 + 168 + 26 * (115 + 23 + 2 * 14 + 9 * (3 + 9 + 10) + 12) + 4 * 57)
Z_B = L_Z * RC + ZMAX * s
UU, CMX = 65117111395830, 7115
MC = cd(STEPS * UU, 1 << 48)
LC = CMX << 19
CREDIT = MC + isqrt(40 * LC * MC - 1) + 1 + 14 * LC + CMX
C_B = cd(MC, 184 + 68) + (s << 19)
U_SC = 4 + 8 + 12 + 9 + 4 * 72 + 40 + 5 * 56 + 31 * 10 + 25 + 14
U = dict(pas=43, call=6, strad=U_SC, z=1)
B = dict(pas=P_B, call=C_B, strad=F_B, z=Z_B)
M1 = dict(pas=2 ** 19, call=2 ** 19, strad=128, z=ZMAX)
CTX = 509 + 160 + 12800 + 16 + 3 + 64 + 83 + 2688 + 2
WB, WCTX = sum(U[k] * B[k] for k in U), sum(U[k] * M1[k] for k in U)
ONCE, S_OLD = 1125918437277736 + 2 ** 22 + 2 ** 19 + 2 ** 21, 116 * 5 * 2 ** 53 + 116 * (2 ** 51 + 2 ** 10) + 2 ** 50
N = CTX * (RC + 1) + WB + WCTX + CREDIT + ONCE + S_OLD + 430 * 2 ** 38
print('RC', RC, 's', s, 'budgets', P_B, F_B, Z_B, C_B, 'ZMAX', ZMAX, 'U_SC', U_SC, 'CTX', CTX)
print('m_C', MC, 'CREDIT', CREDIT, 'WB', WB, 'W_CTX', WCTX, 'N', N)
a = (N ** 100000 // 430 ** 100000).bit_length() - 1
print('2^%d <= (N/430)^100000 < 2^%d' % (a, a + 1), (1 << a) * 430 ** 100000 <= N ** 100000 < (2 << a) * 430 ** 100000)
print('log2(N/430) = %.7f' % (log2(N) - log2(430)))
```

```text
RC 1127113088900472 s 106165583 budgets 586042493902474223 2536018039220686 892207219652469424880 542546246010770826 ZMAX 2619136 U_SC 990 CTX 16325
m_C 136707627336736912199 CREDIT 136712143855319043944 WB 923172982225168920565 W_CTX 28435968 N 1083773001618804927138
2^6112835 <= (N/430)^100000 < 2^6112836 True
log2(N/430) = 61.1283598
```

The printed values are those of the amendment. `experiments/frontline.py` computes the same constants and asserts them.

## 19. The emitter of the counted code

The code of the joint solver (9.4) for the six outcomes of S, of the entry stubs of steps 2 and 3 with the global ledger, of the context and of the routine of step 3 is counted from the program that emits it, listed below (`emit_b3z7.py`, 19,632 bytes, SHA-256 c86676749d18953ac8131d747b9eccaae7ff49f94e6a6d9424878c572d36406b as listed). It imports the constants of `experiments/frontline.py` of this package (`import frontline as F`: the unit charges U_*, IV, ETA and the functions that the context and routine mirror), and `python3 -B -c "import emit_b3z7 as X; print(len(X.build()[0]))"` run next to that file prints 17267.
Machine of Section 11 (64 registers: r0 to r59 allocated, r60 the constant c1, r61 the ledger A(T), r62 the trial counter T, r63 the credit; constants as immediates; one unit and 32 bytes an instruction): ADD XOR AND OR, SHL SHR, MOV, LI, LD LDA STA, BZ BNZ JMP RET HALT; no subtraction (x - y is x + (y XOR M) + 1), no rotation (4 instructions), no indirect jump, no call; a comparison with a branch is two units. A node loads the packed word of an array at its key and takes the bits of its entry out of it by AND, SHR and SHL with constants of the instruction (9.4); the masks are immediates of at most 229 bits, like the lane masks of 9.8. The lane code owns r0 to r8, the 57 live words r0 to r56 are stored and reloaded by the emitted ledger, and RET is one branch back to the calling lane site; the dispatch among call sites is lane code, which is not emitted.
Counts: joint solver for the six outcomes 15,401 (set-up 3,387; descriptors 2,924; forced nodes 4,260; free nodes 402; leaf tests 1,260; the root certificate of Lemma RC inline at each of the 36 leaves 3,168); entry stubs (7 lanes) and ledger 281; context 233; routine of step 3 1,352; total 17,267 instructions, 552,544 bytes. The solver has 432 static nodes, 366 forced, 30 free and 36 leaves, the 432 of 9.4. Kept as the bounds above: the lane sites, the one copy of an opened cluster and the last batch (150,656), and 2^20 for the remaining code, whole although part of what it covered is now emitted.
Every static block is inside the historical charge of Section 11, in parentheses below; amendment E charges exactly the maxima (forced 16 and 11 more at position 15, free 17, leaf 35, root 88, row 1,089, entry and ledger 152): a forced node is 10 instructions, at most 16 (charge 20; 27 at position 15 against 84), a free node 13 or 17 (48), a leaf test 35 (80), the root certificate 88 (120), a row's set-up and descriptors 1,030 to 1,089 (1,354 per row), the entry and ledger at most 152 (614). Participant checks, not organizer-run, through an interpreter of this machine: 14,000 synthetic cases and 993 real solver calls recorded from the walk of `frontline.py` returned the same roots in the same order and debited the credit register by exactly the ledger of Section 11, with the 57 words restored (14,993 of 14,993); 200 of 200 certified roots reached the routine and gave the same two messages, both compressions and halt code; the context (2,000 cases) and the routine (2,000 cases) matched `frontline.py`; 17,255 of 17,267 instructions were executed (the 12 not executed repeat code that is executed at other leaves). Not tested: the equal-chaining-value branch exists only by forcing registers, as no real collision exists; the interface to the lane code is a convention of the emitter; the 150,656 and 2^20 parts are bounds. The listing is the compact form of the checked file (docstrings, comments and the interpreter removed, statements joined, identifiers shortened); it emits the same instruction stream, SHA-256 of its repr beginning afad1f1c09d10119.

```python
import sys, weakref; sys.dont_write_bytecode = True; import frontline as F; dK = (1 << 256) - 1; an = 4294967295; cJ = ['ADD', 'SUB', 'XOR', 'AND', 'OR', 'ADDI', 'XORI', 'ANDI', 'ORI', 'SHLI', 'SHRI', 'MOV', 'LI', 'LD', 'LDA', 'ST', 'STA', 'SEQ', 'SNE', 'SEQI', 'SNEI', 'SLT', 'BZ', 'BNZ', 'JMP', 'CALL', 'RET', 'HALT']
dn = {n: i for i, n in enumerate(cJ)}; dU, dV, dW, dX, OR, dL, dM, dN, dY, dO, dP, dZ, LI, LD, d_, ST, ec, ed, ef, dQ, dR, eg, BZ, do, cK, dc, eh, dS = range(len(cJ))
aY = {BZ: 1, do: 1, cK: 0, dc: 0}

class dp:

 def __init__(self):
  self.Y, self.ad, self.av, self.nl = ([], {}, 'x', 0)

 def I(self, op, a=0, b=0, c=0):
  self.Y.append([dn[op], a, b, c, self.av])

 def ab(self, aI):
  assert aI not in self.ad, aI; self.ad[aI] = len(self.Y)

 def at(self, dd='L'):
  self.nl += 1; return '%s%d' % (dd, self.nl)

 def bW(self):
  Y, ad = (self.Y, dict(self.ad)); aO = True
  while aO:
   aO = False
   for k, c in enumerate(Y):
    if c[0] == cK and ad[c[1]] == k + 1:
     del Y[k]
     for n in ad:
      if ad[n] > k: ad[n] -= 1
     aO = True; break
  cL = []
  for c in Y:
   c = list(c)
   if c[0] in aY: c[1 + aY[c[0]]] = ad[c[1 + aY[c[0]]]]
   cL.append(tuple(c))
  return (cL, ad)

class R:
 __slots__ = ('n', 'g', 'own', '__weakref__')

 def __init__(self, n, g=None, own=False):
  self.n, self.g, self.own = (n, g, own)

 def __del__(self):
  if self.own and self.g is not None: self.own = False; self.g._push(self.n)

class bv(dp):
 CREDIT = 63; bX = 60

 def __init__(self):
  super().__init__(); self.bY = 0; self.ag()

 def ag(self):
  self.aJ = list(range(self.bX - 1, -1, -1)); self.aC = {}; self.dT = {}

 def _push(self, n):
  self.aC.pop(n, None); self.aJ.append(n); self.aJ.sort(reverse=True)

 def S(self):
  n = self.aJ.pop(); r = R(n, self, True); self.aC[n] = weakref.ref(r); self.bY = max(self.bY, self.bX - len(self.aJ)); return r

 def free(self, *rs):
  for r in rs:
   if isinstance(r, R) and r.own: r.own = False; self._push(r.n)

 def bF(self):
  return {n for n, w in self.aC.items() if w() is not None and w().own}

 def aG(self, m, keep=()):
  kn = {r.n for r in keep if isinstance(r, R)}
  for n in list(self.aC):
   o = self.aC[n]()
   if o is not None and o.own and (n not in m) and (n not in kn): self.free(o)

 def cM(self, x):
  if isinstance(x, R): return x
  r = self.S(); self.I('LI', r.n, x); return r

 def bM(self, d, s):
  if isinstance(s, R): self.I('MOV', d.n, s.n)
  else:
   self.I('LI', d.n, s)

 def bp(self, op, dq, a, b, de, df=True):
  if not isinstance(a, R) and (not isinstance(b, R)): return de(a, b)
  if not isinstance(a, R) and df: a, b = (b, a)
  d = self.S()
  if isinstance(b, R): self.I(op, d.n, a.n if isinstance(a, R) else self.cM(a).n, b.n)
  else:
   self.I(dq, d.n, a.n, b)
  return d

 def G(self, a, b):
  if not isinstance(a, R) and a == 0: return b
  if not isinstance(b, R) and b == 0: return a
  return self.bp('XOR', 'XORI', a, b, lambda x, y: x ^ y)

 def O(self, a, b):
  if not isinstance(a, R) and a == 0 or (not isinstance(b, R) and b == 0): return 0
  return self.bp('AND', 'ANDI', a, b, lambda x, y: x & y)

 def ai(self, a, b):
  if not isinstance(a, R) and a == 0: return b
  if not isinstance(b, R) and b == 0: return a
  return self.bp('OR', 'ORI', a, b, lambda x, y: x | y)

 def aP(self, a, b):
  if not isinstance(a, R) and a == 0: return b
  if not isinstance(b, R) and b == 0: return a
  return self.bp('ADD', 'ADDI', a, b, lambda x, y: x + y)

 def ac(self, a, b):
  t = self.aP(a, b)
  if isinstance(t, R): d = self.S(); self.I('ANDI', d.n, t.n, an); return d
  return t & an

 def Z(self, *cC):
  aK, ak = (0, None)
  for t in cC:
   bZ = isinstance(t, tuple); x = t[1] if bZ else t
   if not isinstance(x, R): aK += -x if bZ else x; continue
   if bZ: nx = self.S(); self.I('XORI', nx.n, x.n, an); aK += 1; x = nx
   if ak is None: ak = x
   else:
    d = self.S(); self.I('ADD', d.n, ak.n, x.n); ak = d
  if ak is None: return aK & an
  if aK & an: d = self.S(); self.I('ADDI', d.n, ak.n, aK & an); ak = d
  e = self.S(); self.I('ANDI', e.n, ak.n, an); return e

 def au(self, a, n):
  if n == 0: return a
  if not isinstance(a, R): return a >> n
  d = self.S(); self.I('SHRI', d.n, a.n, n); return d

 def aR(self, a, n):
  if n == 0: return a
  if not isinstance(a, R): return a << n
  d = self.S(); self.I('SHLI', d.n, a.n, n); return d

 def ay(self, a, n):
  n &= 31
  if n == 0: return a
  if not isinstance(a, R): return (a >> n | a << 32 - n) & an
  t1, t2, d = (self.S(), self.S(), self.S()); self.I('SHRI', t1.n, a.n, n); self.I('SHLI', t2.n, a.n, 32 - n); self.I('OR', d.n, t1.n, t2.n)
  self.I('ANDI', d.n, d.n, an); self.free(t1, t2); return d

 def aZ(self, a, n):
  return self.ay(a, 32 - (n & 31))

 def am(self, x, i):
  if not isinstance(x, R): return x >> i & 1
  d = self.S()
  if i: self.I('SHRI', d.n, x.n, i); self.I('ANDI', d.n, d.n, 1)
  else:
   self.I('ANDI', d.n, x.n, 1)
  return d

 def aq(self, a, b, c):
  for p in range(3):
   v = (a, b, c)[p]
   if not isinstance(v, R): o = [x for q, x in enumerate((a, b, c)) if q != p]; return self.O(o[0], o[1]) if v == 0 else self.ai(o[0], o[1])
  t1 = self.O(a, b); t2 = self.G(a, b); t2 = self.O(t2, c); d = self.ai(t1, t2); self.free(t1, t2); return d

 def aS(self, bG):
  d = self.S(); self.I('LDA', d.n, bG); return d

 def a_(self, bG, r):
  self.I('STA', bG, self.cM(r).n)

 def ld(self, aB, ax):
  d = self.S(); self.I('LD', d.n, aB.n, ax); return d

 def aV(self, n):
  if n: self.I('ADDI', self.CREDIT, self.CREDIT, -n)

 def bz(self, r, aD):
  self.I('BZ', r.n, aD)

 def aH(self, r, aD):
  self.I('BNZ', r.n, aD)

 def ba(self, aD):
  self.I('JMP', aD)
bw, dg, bH = (1048576, 2097152, 3145728); BK = {n: 4096 + k for k, n in enumerate('Y9 Y4 omega Ep e1 C2_c1 C2_b1 C2_a1 C2_d1 Y1 Y12 w12 w5 K0_d1 OW0 OW1 OW2 OW3 OW4 OW5 OW6'.split())}
cd = 8192; cD = 57; dJ = dict(forced=F.U_FORCED, sel=F.U_SELECTED, g15=F.U_G15, free=F.U_FREE, leaf=F.U_LEAF, root=F.U_ROOT); dr = F.IV[0] + F.IV[4] & an

def jf(aj, i):
 return (F.ETA >> i & 1) << 2 | (aj.gamma >> i & 1) << 1 | (aj.gamma >> i + 1 & 1 if i < 31 else 0)

def aA(g, bN, w, sh):
 if sh: g.I('SHRI', bN.n, w.n, sh); g.I('ANDI', bN.n, bN.n, 1)
 else:
  g.I('ANDI', bN.n, w.n, 1)

def bb(g, X, n, p):
 t = g.au(X, n - p) if n >= p else g.aR(X, p - n); r = g.O(t, 1 << p)
 if t is not X: g.free(t)
 return r

class dt:
 pass

def ce(g, aj, W, i, cv):
 Q, y, E, Ep, bm = W; k = (i + 20) % 32; bt = lambda x, n: x >> n & 1; ax = bt(aj.sigma, k) << 8 | (cv is not None) << 5 | (i == 31) << 3 | (k == 31) << 2
 aW = [bb(g, Q, i, 12), bb(g, y, i, 11), bb(g, E, k, 10), bb(g, Ep, k, 9), bb(g, bm, k, 7)]
 if k < 31: aW.append(bb(g, bm, k + 1, 6))
 if cv is not None:
  if isinstance(cv, R): aW.append(bb(g, cv, 0, 4))
  else:
   ax |= (cv & 1) << 4
 ak = aW[0]
 for p in aW[1:]: n = g.ai(ak, p); g.free(ak, p); ak = n
 n = g.ai(ak, ax)
 if n is not ak: g.free(ak)
 return n

def bx(g, tau, h, af):
 ld = lambda n: g.aS(BK[n]); cf = g.G(g.aZ(h, 16), ld('e1')); y6 = g.ay(g.G(g.ac(cf, ld('C2_c1')), ld('C2_b1')), 7); a1 = g.ac(g.ac(y6, ld('Y1')), ld('w12'))
 d = g.ay(g.G(a1, ld('Y12')), 16); c = g.ac(F.Y11, d); g.aH(g.G(g.O(c, F.QSTAR_MASK), F.QSTAR_VALUE), af); t = g.G(g.aZ(ld('K0_d1'), 16), g.Z(dr, g.G(g.aZ(cf, 8), ld('C2_d1')), ('-', ld('C2_a1')), ('-', ld('C2_b1'))))
 g.bz(t, af); del t, cf; b = g.ay(g.G(y6, c), 12); del y6; a = g.Z(a1, b, ld('w5')); del a1; s = g.O(b, F.BETA); del b; z = g.ay(g.G(d, a), 8)
 del d; cN = g.au(g.ac(g.aR(s, 1), tau - F.BETA + 8 & an), 1); g.aH(g.G(g.O(a, tau), cN), af); del a, s, cN; u1 = g.ac(c, z); u2 = g.ac(g.ac(c, F.DY11), g.G(z, F.ror(tau, 8)))
 g.aH(g.G(g.G(u1, u2), F.EPS), af); g.I('MOV', 60, c.n); g.ba('FOUND')

def bI(g, tau, ao):
 aj = F.ROWS[tau]; sg, gm, low = (aj.sigma, aj.gamma, aj.low); by = 'END%x' % tau; bt = lambda x, n: x >> n & 1; g.av = 'setup'; ci = len(g.Y)
 Q, y, E, Ep, e1, C, B = (g.aS(BK[n]) for n in ('Y9', 'Y4', 'omega', 'Ep', 'e1', 'C2_c1', 'C2_b1')); bm = g.G(g.G(E, Ep), sg ^ F.EPS); W = (Q, y, E, Ep, bm)
 ax = g.bF(); Eb, aT, kb = (lambda k: g.am(E, k), lambda k: g.am(Ep, k), lambda k: g.am(bm, k)); Qb, yb = (lambda i: g.am(Q, i), lambda i: g.am(y, i))
 sb = lambda k: bt(sg, k)

 def aL(Ek, cO, sk, du, a):
  x2 = g.G(cO, du); d = g.G(g.G(Ek, cO), sk); eq = g.G(g.G(a, Ek), 1); return g.G(x2, g.O(eq, d))

 def az(x, aD=by):
  if isinstance(x, R): g.aH(x, aD)
  elif x:
   g.ba(aD)

 def cj():
  b, u = (g.am(e1, 2), g.am(e1, 21)); k0, k1, bO = (g.S(), g.S(), g.S())
  for bA, kf in ((0, k0), (1, k1)):
   g.I('LI', kf.n, 0); bJ = g.at('gd'); a, ap = (bA, g.G(kb(20), bA))
   for k in (20, 21):
    a1 = g.aq(Eb(k), 0, a); cP = g.aq(aT(k), sb(k), ap); x = g.G(cP, g.G(a1, kb(k + 1)))
    if isinstance(x, R): g.aH(x, bJ)
    elif x:
     g.ba(bJ)
    a, ap = (a1, cP)
   g.I('LI', kf.n, 1); g.bM(bO, a); g.ab(bJ)
  t = g.ai(k0, k1); g.bz(t, by); ck = aL(Eb(22), aT(22), sb(22), kb(23), bO); dv = g.aq(Eb(22), ck, bO); cQ = aL(Eb(23), aT(23), sb(23), kb(24), dv) if bt(gm, 3) == 0 else g.G(g.G(Qb(3), yb(3)), 1)
  a = bO
  for k, fk in ((22, ck), (23, cQ)):
   a1 = g.aq(Eb(k), fk, a); dw = g.aq(aT(k), g.G(fk, sb(k)), g.G(a, kb(k))); az(g.G(dw, g.G(a1, kb(k + 1)))); a = a1
  cm = a; h2 = g.G(g.G(yb(2), ck), Qb(2)); az(g.G(g.G(h2, b), 1)); u3 = g.aq(h2, Qb(2), 0); h3 = g.G(g.G(g.G(yb(3), cQ), Qb(3)), u3)
  u4 = g.aq(h3, Qb(3), u3); bP = b; bQ = g.G(h3, 1); dx = g.aq(bP, Qb(10), Qb(9)) if bt(gm, 10) == 0 else Qb(10); cR = g.aq(bQ, Qb(11), dx)
  f0 = aL(Eb(0), aT(0), sb(0), kb(1), 0); cS = g.aq(Eb(0), f0, 0); bB = g.G(g.G(g.G(yb(12), f0), Qb(12)), cR); dA = g.aq(bB, Qb(12), cR)
  bR = g.G(g.G(h3, bB), u); cn = g.G(g.G(bR, Eb(24)), cm); h4 = g.G(g.G(g.G(yb(4), cn), Qb(4)), u4); cq = g.aq(Eb(24), cn, cm)
  az(g.G(g.aq(aT(24), g.G(cn, sb(24)), g.G(cm, kb(24))), g.G(cq, kb(25)))); u5 = g.aq(h4, Qb(4), u4); cT = aL(Eb(25), aT(25), sb(25), kb(26), cq)
  dB = g.aq(Eb(25), cT, cq); h5 = g.G(g.G(g.G(yb(5), cT), Qb(5)), u5)
  if low:
   ev = g.G(Eb(1), cS); f2 = aL(Eb(2), aT(2), sb(2), kb(3), Eb(1)); eq = g.G(ev, 1); cV = g.G(Eb(2), kb(3)); az(g.O(ev, kb(2))); dC = g.G(cV, g.O(eq, g.G(g.G(g.G(Eb(2), f2), Eb(1)), cV)))
   bn = g.G(g.G(g.G(g.G(h2, dC), Qb(26)), Qb(25)), 1); h6 = g.G(g.G(g.G(g.G(bn, Eb(26)), dB), yb(6)), bt(gm, 7))
  else:
   h6 = g.G(g.G(g.G(g.G(g.G(yb(13), Qb(13)), dA), Eb(1)), cS), u); bn = None
  cr = g.G(Qb(18), 1); cu = Qb(19); x = g.G(h6, g.am(e1, 22)); v7 = g.G(g.G(g.G(g.G(g.am(e1, 23), 1), g.am(C, 23)), g.am(B, 23)), g.aq(x, g.am(C, 22), g.G(g.G(x, g.am(C, 22)), g.am(B, 22))))
  if bt(gm, 7): az(g.G(g.G(h6, 1 ^ bt(gm, 8)), v7))
  return (u, h2, h3, h4, h5, h6, bP, bQ, bB, cr, cu, bR, bn, v7, k0, k1)
 u, h2, h3, h4, h5, h6, bP, bQ, bB, cr, cu, bR, bn, v7, k0, k1 = cj(); hh = {0: 0, 1: 1, 2: h2, 3: h3, 4: h4, 5: h5, 6: h6}; D0 = [ce(g, aj, W, i, hh[i]) for i in range(7)]
 aX, cW = (g.S(), g.S()); w0, bS = (g.at('w0'), g.at('wd'))
 for bA, kf, cX in ((1, k1, w0), (0, k0, by)):
  if bA == 0: g.ab(w0)
  g.bz(kf, cX); wf = g.at('wf'); cp = bA
  for i in range(7):
   aB = g.ai(D0[i], cp); sh = 32 * jf(aj, i); w = g.ld(aB, bw); g.bz(g.O(w, 16 << sh), wf); aE = g.S(); g.I('SHRI', aE.n, w.n, sh + 2)
   g.I('ANDI', aE.n, aE.n, 3); cp = aE
   if i == 6: aA(g, cW, w, sh)
  g.bM(aX, cp); g.ba(bS); g.ab(wf); g.ba(cX)
 g.ab(bS)
 if not low: bn = cW
 ar = 2
 for i, hv in ((2, h2), (3, h3), (4, h4), (5, h5), (6, h6)): ar = g.ai(ar, g.aR(hv, i))
 bq = g.S(); g.bM(bq, g.G(h6, u)); bC = {7: v7, 10: bP, 11: bQ, 12: bB, 16: 0, 17: 0, 18: cr, 19: cu, 24: bR, 26: bn}; ar = ar if isinstance(ar, R) else g.li(ar)
 g.aG(ax, keep=[aX, ar, h6, bq] + [v for v in bC.values() if isinstance(v, R)]); g.av = 'desc'; Dr = {}
 for i in range(7, 32): Dr[i] = ce(g, aj, W, i, bC.get(i))
 A = g.ac(g.aS(BK['Y1']), g.aS(BK['w12'])); V = g.aS(BK['Y12']); cF = g.G(g.G(g.G(h6, g.am(e1, 22)), g.am(C, 22)), g.am(B, 22)); dD = g.G(g.G(g.am(V, 16), 1), g.am(A, 16))
 bd = []
 for ev in (g.au(e1, 22), g.aP(g.au(C, 22), cF), g.au(B, 22), g.aP(g.O(g.au(A, 16), 511), dD), g.O(g.au(V, 16), 511)):
  r = g.S(); g.bM(r, ev); bd.append(r)
 g.aG(ax, keep=[aX, ar, bq] + list(Dr.values()) + bd); g.free(e1, C, B, bm); J = dt(); J.aj, J.D, J.bd, J.c25, J.W = (aj, Dr, bd, bq, (Q, y, E, Ep))
 J.free = [p for p in aj.free if p != 15]; J.lv = [(aX, ar)] + [(g.S(), g.S()) for _ in range(len(J.free))]; J.AA = [g.S() for _ in range(len(J.free))]
 J.E29 = g.S(); J.nroot = 0; J.ao = ao; g.stats.append(('prelude', tau, len(g.Y) - ci)); g.ab('TREE%x' % tau); g.ctxs[tau] = J
 aw(g, J, 7, 0, by); g.ab(by); return J

def aw(g, J, i, bo, af):
 cp, aF = J.lv[bo]; D = J.D
 if i == 32: return bD(g, J, aF, af)
 if i in J.free:
  g.av = 'free'; n0 = len(g.Y); g.aV(F.U_FREE); aB = g.ai(D[i], cp); aa = J.AA[bo]; sh = 32 * jf(J.aj, i); g.I('LD', aa.n, aB.n, dg)
  l0 = g.at('c0'); g.bz(g.O(aa, 16 << sh + 5), l0); aE, bT = J.lv[bo + 1]; g.I('SHRI', aE.n, aa.n, sh + 7); g.I('ANDI', aE.n, aE.n, 3)
  g.I('ORI', bT.n, aF.n, 1 << i)
  if i == 9: aA(g, J.E29, aa, sh + 5)
  g.free(aB); n1 = len(g.Y) - n0; aw(g, J, i + 1, bo + 1, l0); g.ab(l0); g.av = 'free'; n2 = len(g.Y); g.bz(g.O(aa, 16 << sh), af)
  g.I('SHRI', aE.n, aa.n, sh + 2); g.I('ANDI', aE.n, aE.n, 3); g.I('MOV', bT.n, aF.n)
  if i == 9: aA(g, J.E29, aa, sh)
  g.stats.append(('free', i, n1 + len(g.Y) - n2)); return aw(g, J, i + 1, bo + 1, af)
 g.av = 'forced'; m = g.bF(); n0 = len(g.Y); dE = F.U_FORCED + (F.U_SELECTED if i == 20 else 0) + (F.U_G15 if i == 15 else 0); g.aV(dE); ax = bw
 if i == 15:
  dF, dh, dG, di, dH = J.bd; t = g.G(g.au(aF, 6), dF); t = g.aP(t, dh); t = g.G(t, dG); dk = g.O(g.au(t, 1), 511); x = g.G(g.O(g.aP(dk, di), 511), dH)
  cs = g.aP(x, F.Y11 & 511); g.aH(g.O(cs, 139), af); bE = g.aR(g.O(g.au(cs, 8), 1), 4); aB = g.ai(g.ai(g.ai(D[i], bE), 32), cp)
 elif i == 20:
  ax = bH; dl = g.O(g.au(aF, 8), 1); aB = g.ai(g.aR(g.ai(D[i], cp), 1), dl)
 elif i == 25:
  bE = g.aR(g.G(g.O(g.au(aF, 13), 1), J.c25), 4); aB = g.ai(g.ai(g.ai(D[i], bE), 32), cp)
 elif i == 29:
  bE = g.aR(g.G(J.E29, 1), 4); aB = g.ai(g.ai(g.ai(D[i], bE), 32), cp)
 else:
  aB = g.ai(D[i], cp)
 sh = 32 * jf(J.aj, i); w = g.ld(aB, ax); g.bz(g.O(w, 16 << sh), af); g.I('SHRI', cp.n, w.n, sh + 2); g.I('ANDI', cp.n, cp.n, 3); t = g.O(w, 2 << sh)
 t = g.aR(t, i - 1 - sh) if i - 1 >= sh else g.au(t, sh + 1 - i); g.I('OR', aF.n, aF.n, t.n)
 if i == 9: aA(g, J.E29, w, sh)
 if i == 31: g.aV(F.U_LEAF)
 g.stats.append(('forced', i, len(g.Y) - n0)); g.aG(m); return aw(g, J, i + 1, bo, af)

def bD(g, J, h, af):
 aj = J.aj; Q, y, E, Ep = J.W; sg, bU, tau = (aj.sigma, F.theta_of(aj.tau), aj.tau); g.av = 'leaf'; m = g.bF(); n0 = len(g.Y); gg = g.ac(Q, h)
 t = g.ac(Q, g.G(h, F.ETA)); g.aH(g.G(g.G(gg, t), bU), af); f = g.ay(g.G(y, gg), 12); e2 = g.ac(E, f); t = g.ac(Ep, g.G(f, sg))
 g.aH(g.G(g.G(e2, t), F.EPS), af); h2 = g.ay(g.G(h, e2), 8); s1 = g.ac(gg, h2); s2 = g.ac(g.G(gg, bU), g.G(h2, F.MU)); g.aH(g.G(g.G(s1, s2), tau), af)
 g.stats.append(('leaf', 32, len(g.Y) - n0)); g.av = 'root'; n0 = len(g.Y); aD = 'ROOT%x_%d' % (tau, J.nroot); J.nroot += 1; g.ab(aD)
 J.ao[aD] = (tau, h.n); g.aV(F.U_ROOT); g.aG(m); bx(g, tau, h, af); g.stats.append(('root', 32, len(g.Y) - n0)); g.ba(af)

def br(g, ao, aC=cD):
 g.av = 'glob'; g.ag(); g.ab('ENTRY')
 for k in range(aC): g.I('STA', cd + k, k)
 t = g.S(); g.I('XORI', t.n, 61, an); g.I('ADD', bv.CREDIT, bv.CREDIT, t.n); g.I('ADDI', bv.CREDIT, bv.CREDIT, 1 - (1 << 32)); g.free(t)
 dm = [(j, tau) for j, tau in enumerate(F.TAUS) if F.S_MASK >> j & 1]
 for j, tau in dm: g.av = 'glob'; g.ag(); t = g.S(); g.I('ANDI', t.n, 62, 1 << j); g.bz(t, 'END%x' % tau); bI(g, tau, ao)
 g.av = 'glob'; g.ab('EXIT')
 for k in range(aC): g.I('LDA', k, cd + k)
 g.I('RET')
cG = 3840; cz = {}; _a = 4352
for _n in [n for n, _ in F.LINES]: cz[_n] = _a; _a += 1
for _n, _b in (('w5', 'w5'), ('w12', 'w12'), ('K0.d1', 'K0_d1')): cz[_n] = BK[_b]
aU = set(); cY = 16384

def aM(g, ae, ah, store=None, keep=()):
 bV = [n for n, _ in F.LINES if n in ae]; cA = {}
 for k, n in enumerate(bV):
  for d in F.deps(F.DEF[n], set()): cA[d] = k
 for k, n in enumerate(bV):
  ah[n] = aQ(g, F.DEF[n], ah)
  if store and n in store: g.a_(store[n], ah[n])
  for d in list(F.deps(F.DEF[n], set()) | {n}):
   if d in ah and d not in keep and (cA.get(d, -1) <= k): del ah[d]
 return ah

def aQ(g, e, ah):
 if isinstance(e, int): return e & an
 if isinstance(e, str): return ah[e]
 if e[0] == 'sum': return g.Z(*[('-', aQ(g, t[1], ah)) if isinstance(t, tuple) and t[0] == 'neg' else aQ(g, t, ah) for t in e[1]])
 if e[0] == 'xor': return g.G(aQ(g, e[1], ah), aQ(g, e[2], ah))
 if e[0] == 'ror': return g.ay(aQ(g, e[1], ah), e[2])
 raise ValueError(e)

def aN(ae):
 bK, st = (set(), list(ae))
 while st:
  n = st.pop()
  if n in F.DEF and n not in bK: bK.add(n); st += F.deps(F.DEF[n], set())
 return bK

def bh(g):
 g.av = 'context'; g.ag(); g.ab('CONTEXT'); f = g.aS(cG); ah = {'fl': F.FLAGS}
 for k, n in enumerate(F.OUTER_WORDS): ah[n] = g.O(g.au(f, 32 * k), an); g.a_(BK['OW%d' % k], ah[n])
 del f; ae = set(F.CONTEXT_LINES) | {'S2', 'w5', 'w12'}; ae = aN(sorted(ae)) - {n for n in F.MEMBER_LINES}; assert len(ae) == 42, len(ae)
 aM(g, ae, ah, store={n: cz[n] for n in ae}); g.I('RET'); aU.update(ae); return ae

def bs(g):
 for L in range(7):
  g.av = 'glob'; g.ag(); g.aJ = [59, 58, 57]; g.ab('ENTRY%d' % L)
  for dI, aI in ((0, 'Y9'), (1, 'Y1'), (2, 'Y12')): g.a_(BK[aI], g.O(g.au(R(dI), 36 * L), an))
  g.a_(BK['Y4'], g.Z(R(3), -F.Y3 & an)); g.a_(BK['Ep'], g.Z(R(4), F.DY3))
  for k, aI in ((3, 'e1'), (4, 'omega'), (5, 'C2_a1'), (6, 'C2_b1'), (7, 'C2_c1'), (8, 'C2_d1')): g.I('STA', BK[aI], k)
  g.ba('ENTRY')

def cH(g, v, a, b, c, d, x, y):
 v[a] = g.Z(v[a], v[b], x); v[d] = g.ay(g.G(v[d], v[a]), 16); v[c] = g.Z(v[c], v[d]); v[b] = g.ay(g.G(v[b], v[c]), 12); v[a] = g.Z(v[a], v[b], y)
 v[d] = g.ay(g.G(v[d], v[a]), 8); v[c] = g.Z(v[c], v[d]); v[b] = g.ay(g.G(v[b], v[c]), 7)

def bi(g, m, t, n, cI):
 v = list(F.IV) + list(F.IV[:4]) + [t, 0, n, cI]; s = list(m)
 for r in range(2):
  for i, (a, b, c, d) in enumerate(F.GCALLS): cH(g, v, a, b, c, d, s[2 * i], s[2 * i + 1])
  s = [s[p] for p in F.PERM]
 return [g.G(v[i], v[i + 8]) for i in range(8)]
bj = ('Y1', 'Y12', 'w12', 'C2.b1', 'C2.c1', 'C2.a1', 'C2.d1', 'K0.d1', 'K0.b1', 'S0', 'w2', 'w3', 'w5', 'w6', 'w7', 'w8', 'w9', 'w10', 'w11')

def bl(g):
 g.av = 'found'; g.ag(); g.ab('FOUND'); ah = {'fl': F.FLAGS, 'Y4': g.aS(BK['Y4'])}
 for k, n in enumerate(F.OUTER_WORDS): ah[n] = g.aS(BK['OW%d' % k])
 c1 = R(60); ae = aN(bj); aM(g, ae, ah, keep=bj); w = lambda n: ah[n]; cB = g.G(g.aZ(g.Z(c1, -F.Y11 & an), 16), w('Y12'))
 Y6 = g.Z(cB, ('-', w('Y1')), ('-', w('w12'))); cZ = g.G(g.aZ(Y6, 7), w('C2.b1')); c_ = g.Z(cZ, ('-', w('C2.c1'))); Y2 = g.G(g.aZ(c_, 8), w('C2.d1'))
 w0 = g.Z(Y2, ('-', w('C2.a1')), ('-', w('C2.b1'))); bL = g.Z(w0, F.IV[0] + F.IV[4] & an); t = g.G(g.aZ(w('K0.d1'), 16), bL); w1 = g.Z(w('S0'), ('-', bL), ('-', w('K0.b1')))
 ma = [w0, w1, w('w2'), w('w3'), F.W4, w('w5'), w('w6'), w('w7'), w('w8'), w('w9'), w('w10'), w('w11'), w('w12'), F.W13, 0, 0]; mb = list(ma); mb[4], mb[5] = (F.W4B, g.Z(w('w5'), F.DELTA5))
 for k in range(16): g.a_(cY + k, ma[k]); g.a_(cY + 16 + k, mb[k])
 del ah, w, cB, Y6, cZ, c_, Y2, w0, w1, bL; ca = bi(g, ma, t, F.LEN_A, F.FLAGS); del ma; cb = bi(g, mb, t, F.LEN_B, F.FLAGS); g.ab('FINALCMP')
 g.cmpregs = ([x.n for x in ca], [x.n for x in cb]); ak = g.G(ca[0], cb[0])
 for i in range(1, 8): ak = g.ai(ak, g.G(ca[i], cb[i]))
 g.aH(ak, 'NOTEQ'); g.I('HALT', 2); g.ab('NOTEQ'); g.I('HALT', 3)

def build():
 g = bv(); g.stats = []; g.ctxs = {}; ao = {}; br(g, ao); bs(g); bh(g); bl(g); Y, ad = g.bW()
 return (Y, ad, ao, g)

```

The refund post-pass of amendment F, `emit_dyn.py` (SHA-256 d03754929695bb79980cefaf9e39a393cd09fed1cbfb54fe9241380a68148322), applied to the output of `build()` above:

```python
import emit_b3z7 as X
F = X.F
ADDI, BZ, BNZ, JMP, RET, HALT = (X.dn[n] for n in ('ADDI', 'BZ', 'BNZ', 'JMP', 'RET', 'HALT'))


def build():
    Y, ad, ao, g = X.build()
    Y = [list(c) for c in Y]
    ex = []
    for j, tau in enumerate(F.TAUS):
        if not F.S_MASK >> j & 1:
            continue
        end, tree = ad['END%x' % tau], ad['TREE%x' % tau]
        start = max(k for k in range(tree) if Y[k][0] == BZ and Y[k][2] == end and k < tree and Y[k - 1][0] == X.dn['ANDI'] and Y[k - 1][2] == 62) + 1
        dist = {start: 1}
        for pc in range(start, tree):
            if pc not in dist:
                continue
            op = Y[pc][0]
            succ = [] if op in (JMP, RET, HALT) else [pc + 1]
            if op in (BZ, BNZ):
                succ.append(Y[pc][2])
            elif op == JMP:
                succ.append(Y[pc][1])
            for s in succ:
                if start <= s < tree:
                    dist[s] = max(dist.get(s, 0), dist[pc] + 1)
        assert max(dist.values()) <= F.U_ROW
        for pc in range(start, tree):
            op = Y[pc][0]
            tgt = Y[pc][2] if op in (BZ, BNZ) else Y[pc][1] if op == JMP else None
            if tgt == end and pc in dist:
                refund = F.U_ROW - dist[pc] - 2
                k = len(Y)
                Y += [[ADDI, 63, 63, refund, 'refund'], [JMP, end, 0, 0, 'refund']]
                if op == JMP:
                    Y[pc][1] = k
                else:
                    Y[pc][2] = k
                ex.append((tau, pc, dist[pc], refund))
    return [tuple(c) for c in Y], ad, ao, g, ex
```
