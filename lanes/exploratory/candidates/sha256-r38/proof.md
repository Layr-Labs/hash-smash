# sha256-r38: sealed v4 in-band budget package

Prepared for review after mechanical completeness checks. The exact native v4 program, complete C source, programmed-RAM model, resource argument, raw selected local receipts, historical probability evidence and self-contained organizer VM are included. The local artifact is CONDITIONAL_LOCAL_GO under its stated assumptions. This package asserts no organizer qualification, human acceptance, ordinary collision witness, submission or official incumbent improvement.

The declared time bound is 82.87826569 target-compressions in log2 and memory bound 28.03552941 bytes in log2, each rounded upward. The separate scalar projection is 90.91379510. Exact local time is 82.878265682273451036253899774258265766560295241372917339616115972680829031092561519170581349491115279529411656; exact memory is28.035529408461116044911937289262113327471081501735232121942130839971926675739072553815974388018697311792308189; exact scalar is90.913795090734567081165837063520379094031376743108149461558246812652755706831634072986555737509812591321719845. These are conditional resource bounds, not a judge-issued score. The baseline_improved field is the required nominal-reference identifier, not a claim of official improvement.

The inherited construction for sha256-r38-prefix-v1 credits:
- Jbenisek's e4243e7a: the P1 sum-claw, its post-filter chain, step 3b, the counted pricing, the registered rate q3_model and the form of H3-P1;
- newjordan's 711c4bf8: all 2^32 scan words per chaining value;
- 0xplemonade's a32131ff: the online memory cell is a measured full-table execution;
- 377cb363: the capped Step-1 memory measurement;
- 0xplemonade's b561f523 and its predecessor e6a33086: a table of seven-entry buckets with exact tags, the observation that all 20 row-16 heads are equal modulo 2^13 (so one w per scan word and constant bucket deltas between heads), and the pairing of a head's two windows with buckets b and b + 2.

Our own work:
- The characteristic P8, its semi-free-start pair and its accepted event are our own (1a695f0b).
- Our previous filing of this line, with the 2^27-candidate residue table, is b79d2f6c-f3cd-4e8d-bc7b-8e2f582ee376.
- The staged program was `experiments/p1b38.py`, standard library only. This package replaces the VM with the v4 assembler and in-band budget. The mathematical data and inherited derivations keep their original credits.



## 1. Target and output

SHA-256 steps 0..37 are applied to every padded block, with the standard IV once, FIPS 180-4 padding, feed-forward and all eight digest words. The procedure outputs two 128-byte messages m = M0||M1 and m' = M0||M1' with a common first block M0. FIPS padding appends the same third block to both.

**Lemma 2 (output).**
- *Statement.* Let cv = F_38(IV, M0). If the second-block computations of M1 and M1' from cv end with equal A34..A37 and E34..E37, then m and m' have equal digests.
- *Proof.* The second-block output is cv + (A37, A36, A35, A34, E37, E36, E35, E34), and the third block is common. The messages are distinct because W7 differs (W7y - W7x = D7 = 0x20000000 for every pair the procedure builds, Section 2).

Step 3b accepts only pairs whose A34..A37, E34..E37 are equal, so every output is a collision of the target.

## 2. Data, the P1 pair and row 16

The `selftest` references in this inherited mathematical description name historical predecessor checks. The copied VM prototype has a different request entry point. No predecessor check is represented as a new draft execution.

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


## 3. Complete v4 program and model

Program SHA256 979ce9bb2d6505f8614aab65a56e8eff830fdb3d02cc36f5569d6321134bb718,290283 eight-byte records, 2322264 bytes. Complete native source SHA256 e4b358784e95303f4fb992a8ccd24e5f054e55bea63d09d844652b720c790df7,94144 bytes; native ELF SHA25636bcfae56cdb977a75a08f98f92e04b71b05110087ae1b9011441bd2f1c4ef86,906840 bytes. The finite banks have 241 constants and 94 mutable named words, including BUDGET; native RAM has 234 words. Code, banks, messages, state, table/mirrors and initialization are charged. Finite instruction fetch/decode and literal operand selection follow the disclosed programmed-RAM convention; actual data LOAD/STORE operations remain charged. This interpretation and inherited narrow/LEGACY pricing remain H5prime conditions.

BUDGET uses full modulo2^256 ADDs. Each of 8960 leaf sites adds its independently decoded full field prefix P_leaf plus 9. The 9 covers C1 at 7, this ADD at 1, and one head unit per marker. Nonfull paths add 7. Reached C2, G, F7 and callback paths add 23,30,31 and4025. These 20480 additions are literal instructions. They require no extra branch or dynamic advice lookup. At each CV boundary one existing ADD adds K=1489431040983 =8321635287+2^32*(88281/256). The controller compares the resulting in-band value to the fixed cap. Histogram sums and an external execution clock never enter its decision.

The no-event base excludes the L/H XOR executed only when a head has markers. One extra budget unit in every leaf covers that per-head instruction without another ADD. Under H1, nonempty L/H heads per scan word are at least20*(507/512)*(63/64)*(1-(127/128)^14)>2. Thus the extra head overcharge is at most35/16-2=3/16. Together with counter ADDs and invalid-marker overcharge, the additional mean budget is at most90547/32768<3. Invalid markers retain at most13 reconstruction plus7 C1 units that were not executed. Full-prefix mean 36 and maximum40 are independently decoded; a nonfull path has six extra old instructions.

The actual N_CV limit is 12014587405061634. Four independent uniform 256-bit RAND words per CV supply M0, u0 and R, with 52 charged coin-preparation operations. The table is reused and all 2^23+8 physical words are reset. QUERY_SETUP falls through into the scanner, and the full-width ADD/CMP/BR tail reaches 2^32 without wrap. All queries of a started CV complete after FOUND; later callbacks pay guard/return and suppress Step3b/output. FOUND stops another coin draw. Equality at the cap is permitted; a strictly larger value stops at the next boundary. Counters fit 128 bits, with BUDGET held as a full 256-bit word.

All 640 callbacks use literal continuation IDs and branches to the same native body, followed by a balanced 639-condition dispatcher with maximum 21 return operations. There is no CALL/RET or computed return. Fixed-IV compression 2022, positive Step3b 3997, maximum recurring callback 4024, terminal suffix 9221 and longest successful callback 13245 retain their measured meanings. FIN 17968 covers the mutually exclusive success suffix or stopping work at most 6. Padding is the common third block, with W0=0x80000000 and W15=1024. The P8 positive remains semi-free-start plumbing; its serialization is separately checked to fail equality from the actual standard IV.

## 4. Self-contained time and cap argument

Let Q=2^32, B=2^23, X~Binomial(2^27,2^-23), s=E[min(X,7)], c=160s/512, and z=160(7-s)/512. H1 gives the bucket/tag law; s<=7 implies c+z=35/16. Exact finite counting gives p12=53096854/2^32. For cost use p12gU=116189231640576/2^59, four times the largest window count, and qpfU=p12gU*287309824/2^32. The smallest-window rates in Section6 remain success lower bounds. H1-P1 explicitly includes transfer of these upper marginal stage bounds to the retained claws, as well as its lower success-rate law.

The nonfull bound Pr[X<=6]<1/128 can be checked without large-number simulation. For k<=6,
Pr[X=k] <=16^k/k! * exp(-16+6/2^23).
For x=16-6/2^23, exp(x) exceeds its positive Taylor sum through 128 terms. Multiplying the reciprocal of that rational lower sum by sum_(k=0)^6 16^k/k! gives an upper value 0.004006047521<1/128. All full-scan phase/tag values have equal frequency; the triangular inverse for the low12 bits of s0(u)-u is exercised by the finite fixtures. The full-prefix average36 is obtained directly from the literal tree depths and split gathers.

A direct upper mean for the v4 budget is the following rational expression. It conservatively replaces every retained-claw expectation by35/16 and every nonfull marker probability by1/128:

```text
mu_direct = K + Q*(35/16)*[
  45 + 7/128 + 23/8 + 30*p12 + 31*p12gU + 4025*qpfU ]
 = 1943795060253.989842903800308704376220703125.
```

Here 45=36+7+1+1 is the full prefix, C1, meter ADD and head coverage. Each remaining coefficient includes its new ADD. This direct check avoids relying on a historical saving-envelope reconstruction for cap domination. It is below the retained conservative sealed mean enclosure mu=1945060328028.9042079394176093300296584467417428959197055872389442998554458646737595245354293807001568868200322.

Fixed work 8321635287 is a conservative bound. The directly visible bound57*2^27 +5*(2^23+8) +600*2^20 +42 +76 +2022 +52 +4 +3 +9 +16 =8321501400 is already smaller. The57/45 builder and inherited scalar blocks remain the explicit LEGACY pricing dependency; transform548 is bounded by600 per8-word block. Mirror work and all physical reset words are included.

Maximum budget scan is 2335626 =2331706+3360+560. The 3360 covers six possible added ADDs at each of 560 fields; the 560 covers the extra head budget unit per marker. With m=8321635287+Q*2335626=10031445607322583, each complete hypothetical CV budget Y_j lies in[0,m]. Under H1 the CVs are independent and Var(Y_j)<=m E[Y_j]. The cap is

```text
V_MAX =23369453903347697850258080090
      >=ceil((65537/65536)*N_CV*mu).
```

Bernstein with eps=1/65536 gives
Pr[sum Y_j>V_MAX] <=exp(-eps^2*N_CV*mu/(2*m*(1+eps/3))).
Using mu>=Q*300 only in the exponent yields a conservative log2 failure upper bound-259.18444137173940668908953602266728028406754731209561908392657659897495608768975366873793178499855210327352850, below the reserved2^-60. Subtracting that failure bound from Section7's inherited success argument preserves conditional success at least0.39. This is algorithmic probability over fresh ideal coins, not confidence in the premises. No enormous cap total was dynamically accumulated in these runs.

The complete charged total is

```text
N=(2^78+2^74+2^70)*2728 +V_MAX +m +17968 +1048576
 =24248692429337297059623672673 word operations.
time=log2(N/2728).
```

All failed/repeated construction and development work is inside the declared H4 allowances. Installation of the full ELF/program and2048 logical state words costs at most205916 operations, within the once-only1048576 reserve. No stored ordinary collision or omitted advice search is used. The advice bound16 covers65536 initialized-state bytes; executable code remains separately counted in whole memory.

## 5. Memory and evidence scope

The guarded native memory is 275128320 bytes: max(all twelve retained native development/final post-exit cgroup and RSS peaks, inherited 269946880, and preprocessing+new ELF/program+2048 state words 273241520)+65536. No bytes are subtracted. The physical table/mirrors are 268435712 bytes. Code, 241 constants, 94 mutable words, 234 native RAM words, messages, counters, allocator/stack, shell, file/cache pages and kernel charges coexist in the whole cgroup peak. Production disables tracing, dumps, inverse verification and per-CV history.

The557-file native freeze preceded every final outcome. Three nc17/LU12 cases and one actual nc27/LU12 case ran once in order, with disjoint fixed inputs and no final replacements. All twelve retained native outcomes contribute to memory, including two superseded development cases. Exact raw summaries/peaks and protocol are included below. Independent replay rebuilt identical source/program/metadata and five binaries, rebound the actual toolchain, and reproduced final reports without another final candidate execution. These are local participant/reviewer receipts, not organizer authentication; deleted unrecorded-trial provenance and historical development completeness remain UNKNOWN or heuristic.

The standard-library-only organizer experiment is a self-contained transport of the expanded VM/generator in Appendix VM. Transport source SHA2565fd97b32edd3b1ad8ebdcd4f554bedf45b5d93761dca2fe87e0cf5a5345dd5ea, 54686 bytes; expanded source SHA2560b72e0a2532d5be6f66b38bcd5b8cbdfdfe8fb39429c802b5712b1b6755b5b10, 88970 bytes. Compression meets the organizer's64KiB source limit. The complete expanded code is reproduced for review; the loader verifies its digest. The native-source replica expands to the exact 94144 C bytes above, while the assembler independently generates all 290283 v4 records and asserts the frozen program hash. It does not compile or execute that C source and does not infer ELF authenticity from a checksum.

The first requested trial executes all fixtures and assertions, all640 literal continuations, both outcomes of639 dispatcher conditions, full-width arithmetic, sparse reset/count/tag/payload and unrelated-window checks, and the admitted in-band controller. It emits only 16 numeric summaries. The next two trials each build 2^16 candidates and scan 2^10 real words in the actual sparse full-address representation. Other rows return null by design. These runs cannot establish full physical native memory, full retention, N_CV/LU32 behavior, rare-event probability, or independent ideal coins. Any returned pair is checked by the organizer against the complete selected target. Execution status belongs to the exact attached organizer artifact, not an assumed claim here.

H2's mean-log/arithmetic transfer gap is preserved in Section9. H3's rare pairwise behavior is unobserved. H4 inventory completeness, H5 inherited narrow/LEGACY pricing and programmed-RAM interpretation, and H6 local-measurement provenance remain declared conditions. No local conditional arithmetic comparison is claimed as an official incumbent improvement.


## 6. The post-filter law q_pf (H1-P1)

Inherited mathematical and statistical material. It is retained as support for the unchanged P8/P1 premise. It supplies no new execution; Section 5 applies its unchanged premise to the sealed v4 ledger.

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

Inherited probability space, second-moment argument and N_CV calculation. The sealed v4 cap and its independently enclosed failure bound are stated in Section 5. No new statistical confidence is added by this documentation update.

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
  - Section 5 combines this inherited parameter with the sealed v4 cap-failure bound, below the reserved 2^-60 budget. The resulting conditional output-success lower bound remains at least 0.39 under the named premises.
  - The predecessor reported the parameter calculation as 0.3900000000000000047332. This is a historical conditional calculation, not a v3 execution or completed bound.

## 8. H3-P1: pairwise behaviour of acceptance over the random chaining value

Inherited H3-P1 statement and full-scan link evidence, preserved with its limitations. The sealed scanner/control implementation supplies no new dependence evidence.

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

Inherited q3 transfer evidence, registrations and limitations. This draft does not rerun or strengthen these studies.

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
- *Confidence.* The three registered statistical statements (level, relaxation ratio, and mean per-seed paired log-difference) together have nominal confidence at least 97% by the registered union bound. This confidence statement does not apply to the online arithmetic acceptance-rate ratio used by H2-P1.
- *What the statistic bounds.*
  - The registered statistic is a lower confidence bound on the mean per-seed log-ratio. The charge uses min(0, D_LB(A0), D_LB(A0sel)), so it never raises q3 above q3_model.
  - It does **not** by itself lower-bound the arithmetic ratio of online acceptance probabilities. Equal weighting of seed log-ratios need not equal prefix- or claw-weighted acceptance, and exponentiating an average log-ratio does not produce an arithmetic-ratio bound.
  - On the same proposals the pooled counts favour P1: log2 of the ratio of total successes, P1 over reference, is +0.117 against A0 and +0.114 against A0sel. Those pooled counts are descriptive because they omit the online prefix/claw weights; they do not repair the inference above.
  - The 17 stalled seeds stall in the rows 16..22 prefix, which is identical in the three families and does not read the variant list. Their registered exclusion is symmetric, but without a prefix-weighted linear analysis it does not establish the online arithmetic ratio.
- *H2-P1 extrapolation.* The statement `q3_P1 >= 2^-96.0438` is therefore an explicit score-critical transfer premise, supported by the registered log-ratio study and descriptive pooled counts rather than proved by their confidence interval. A rigorous replacement would weight the linear acceptance ratios by the actual online prefix/claw law and include stalled prefixes in that estimator.
- *Limitation, stated.* Our estimator conditions on row 22 of the characteristic before the final stage, while the base runs' final stage starts at row 22. W8 first enters the message expansion at W23 = s1(W21) + W16 + s0(W8) + W7, so the family law affects only rows 23..37 in both tools.
- *Limitation, stated.* The P1 pairs are drawn from the exact C1 C2 G law on P, not from claws of the procedure; W7 is drawn uniformly in F7 as in the base runs.


## 11. Allowances and development (H4a, H4b, H4c)

All three inherited H4 allowances remain charged in full in Section 5. The paragraphs below preserve their historical evidence and declared hardware envelope. Sealed v3 development history is included as local provenance. Completeness of the charged development/preprocessing inventory remains a declared premise; this documentation update does not invent an independent machine/date audit.

A_C = 2^78 (the characteristic search behind P8), A_S = 2^74 (its Step-1 solve) and DEV = 2^70 (all development) are charged allowances: upper bounds charged in full. preprocessing = log2(2^78 + 2^74 + 2^70) = 78.09276.

- **A_C and A_S.**
  - The search for P8 and its Step-1 solve are our own computations (1a695f0b). With all of our work on the P8 line, they ran on one 10-core machine for less than 2^22 core-seconds (our accounting, Appendix R.2).
  - At 2^30 target compressions per core-second, above any CPU core (SHA-256 runs at about 2^24 compressions per second per core), that is under 2^52 units, 26 bits under A_C.
  - Our solver-alone Step-1 rerun took 18 min 17 s.
- **DEV (H4c).** The bound is a hardware envelope. Every code execution behind this package ran on one 10-core machine (our own): the exhaustive counts of Section 6, the C ports, the panel, the partner count, the q3 runs, checks and failed runs. That is at most 10 cores for at most 30 days (2.6 x 10^6 s).
  - At most 2^40 word operations per core-second, that is under 2^64.6 operations = 2^53.2 compressions.
  - The development of the predecessors we build on, which was charged in their own DEV and is reproduced in Appendix Q (68 threads and one GPU for 17 days, under 2^56.7 compressions), is also inside DEV = 2^70 by a factor above 2^13.


Historical internal section and appendix references inside quoted records belong to their source documents. Current v4 resources and control are specified in Sections3 through5 and AppendicesV4, VM andR4.

## Appendix H. The full-size panel, the partner count and the memory measurement (Sections 6, 8, 10, 12)

Historical predecessor panel, full-scan link and memory records. They are preserved for probability/predicate support and credits. The C-port and `p1b38.py` references here name predecessor implementations, not the complete v3 program. No peak or count below is a new v3 result.

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

### H.4 The historical memory measurement

The following 269,946,880-byte panel cell is predecessor evidence. It is not the complete v3 peak.

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

Reproduced verbatim as data from the public proof.md of e4243e7a-4f8b-42b6-a64a-e70b2dbe1586 (sha256 9d821b2638253c739eb6e68436e921a47d72625d3a1b55801d740af10c9f1d67), its Appendix Q (per-seed values of the two runs behind q3_model and their registrations) and its Appendix R.1 (the registrations, methods and amendments of those runs as recorded in 9aaf71a2). The quoted text is enclosed in one text block; nothing in it is changed. "Our" inside the quoted text refers to that author. We did not rerun these studies; q3_model is their registered bound, and our own measurement (Appendix P) only shifts it by a paired difference. The memory figures inside this record (that study's sampled resident sets) describe 9aaf71a2's statistical study, which the online procedure does not execute; current Section 5 states the v4 native memory bound.

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


## Appendix S. Historical tool sources and compact index

All P/Q/R registrations, values, amendments and credits remain unchanged. The canonical q3tv estimator, partner enumeration, low-memory exact-window count, variant selectors and data-preparation source below remain embedded. Old C-port, cross-check, CV/header generators, superseded large-memory window count and two performance-variant q3 bodies are indexed with their original hashes instead of duplicating their code. P/Q/R retain every reported comparison, registration, amendment and probability observation, including how those variants reproduce the canonical estimator. The final complete native C is in Appendix V.1 and the current independent references are in the single experiment source. An indexed omitted body is not claimed to be attached.

| Historical body omitted from this compact appendix | Original SHA256 |
| --- | --- |
| p1b38c.c | 70e2ce60a214bb9aba88b7e07a742503afdbf99e3d85ec7e3e340366b90bd43c |
| xcheck_b.py | 2c430fd990277107519b7071bb9f9f91f8a4e970d03ac438f849603d0604047d |
| mkcvs_r.py | f47ec8de2d2950647bb0bd5846591a6f68f9be3374ea65e9eabc82644c3d1b3e |
| p1tconst.py | 85dd887b50d59e438b2304a598721e6f842526c2b3f5a603fdd7c23f5efdfbef |
| gwin38.c | feae564923d015656c84c03bfcacd68c16dbeaff6ef92e94909bd2a30f33b527 |
| q3tv3.c | 65260652429ace66b1bae67d04e36f74d3c80274920f9b41c75645f82bff1496 |
| q3tv4.c | 88af9d2486558e9fe6cdff8f712b7b768569eecea36812fbacacb1fa638d1151 |

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


## Appendix V4. Complete native source

```c
#define _GNU_SOURCE
#include <stdint.h>
#include <inttypes.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <errno.h>
#include <unistd.h>
#include <fcntl.h>
#include <sys/stat.h>
#include <sys/resource.h>
#include <time.h>
#include <assert.h>

typedef struct { uint64_t x[4]; } W;
_Static_assert(sizeof(W)==32,"word");
enum {LD,ST,ADD,SUB,AND,OR,XOR,NOT,SH,CMP,BR,IMM,LEGACY,RAND,NOPS};
static const char *opnames[NOPS]={"LOAD","STORE","ADD","SUB","AND","OR","XOR","NOT","SHIFT","COMPARE","BRANCH","IMMEDIATE","UNCHANGED_LEGACY","RANDOM"};
static uint64_t ops[NOPS],events,fields,claws,invalids,control_ops,field_max,transform_max,transform_min=UINT64_MAX;
static uint64_t split_gathers,nonfull_fallbacks,normal_heads,strad_heads,errors;
static uint32_t event_id,ret_id,HF;
static W ZERO;
static uint64_t total(void){uint64_t v=0;for(int i=0;i<NOPS;i++)v+=ops[i];return v;}
static uint64_t newops[NOPS];static int active_new;
static void native_primitive_category(unsigned op,uint64_t n);
static void ch(int op,uint64_t n){if(active_new){newops[op]+=n;native_primitive_category(op,n);}else ops[op]+=n;}
static W small(uint64_t v){return (W){{v,0,0,0}};}
static W bit(unsigned p){W v={{0}};v.x[p/64]=UINT64_C(1)<<(p%64);return v;}
static W raw_and(W a,W b){for(int i=0;i<4;i++)a.x[i]&=b.x[i];return a;}
static W wa(W a,W b){ch(AND,1);return raw_and(a,b);}
static W wo(W a,W b){ch(OR,1);for(int i=0;i<4;i++)a.x[i]|=b.x[i];return a;}
static W wx(W a,W b){ch(XOR,1);for(int i=0;i<4;i++)a.x[i]^=b.x[i];return a;}
static W wn(W a){ch(NOT,1);for(int i=0;i<4;i++)a.x[i]=~a.x[i];return a;}
static W ws(W a,W b){ch(SUB,1);W r;uint64_t borrow=0;for(int i=0;i<4;i++){uint64_t t=b.x[i]+borrow,c=t<b.x[i];r.x[i]=a.x[i]-t;borrow=c|(a.x[i]<t);}return r;}
static W add256(W a,W b){ch(ADD,1);W r;uint64_t carry=0;for(unsigned i=0;i<4;i++){uint64_t t=a.x[i]+b.x[i],c=t<a.x[i];r.x[i]=t+carry;carry=c|(r.x[i]<t);}return r;}
static W wl(W a,unsigned n){ch(SH,1);W r={{0}};if(n>=256)return r;unsigned q=n/64,s=n%64;for(int i=3;i>=0;i--){if((unsigned)i>=q){r.x[i]=a.x[i-q]<<s;if(s&&(unsigned)i>q)r.x[i]|=a.x[i-q-1]>>(64-s);}}return r;}
static W wr(W a,unsigned n){ch(SH,1);W r={{0}};if(n>=256)return r;unsigned q=n/64,s=n%64;for(unsigned i=0;i<4;i++){if(i+q<4){r.x[i]=a.x[i+q]>>s;if(s&&i+q+1<4)r.x[i]|=a.x[i+q+1]<<(64-s);}}return r;}
static int raw_eq(W a,W b){return memcmp(&a,&b,sizeof(W))==0;}
static int bnz(W a){ch(CMP,1);ch(BR,1);return (a.x[0]|a.x[1]|a.x[2]|a.x[3])!=0;}
static int blt(W a,W b){ch(CMP,1);ch(BR,1);for(int i=3;i>=0;i--)if(a.x[i]!=b.x[i])return a.x[i]<b.x[i];return 0;}
static int bne(W a,W b){ch(CMP,1);ch(BR,1);return !raw_eq(a,b);}
static int alt(uint32_t a,uint32_t b){ch(CMP,1);ch(BR,1);return a<b;}
static uint32_t aa(uint32_t a,uint32_t b){ch(ADD,1);return a+b;}
static uint32_t am(uint32_t a,uint32_t b){ch(AND,1);return a&b;}
static W load(W *T,uint32_t p){ch(LD,1);return T[p];}
static void store(W *T,uint32_t p,W v){ch(ST,1);T[p]=v;}
static uint64_t get(W a,unsigned p,unsigned n){unsigned i=p/64,s=p%64;uint64_t v=a.x[i]>>s;if(s+n>64)v|=a.x[i+1]<<(64-s);return v&((UINT64_C(1)<<n)-1);}
static void set(W *a,unsigned p,unsigned n,uint64_t v){unsigned i=p/64,s=p%64;uint64_t m=(UINT64_C(1)<<n)-1;v&=m;a->x[i]=(a->x[i]&~(m<<s))|(v<<s);if(s+n>64){unsigned h=s+n-64;uint64_t z=(UINT64_C(1)<<h)-1;a->x[i+1]=(a->x[i+1]&~z)|(v>>(64-s));}}
static uint32_t rr(uint32_t v,unsigned n){return (v>>n)|(v<<(32-n));}
static uint32_t S0(uint32_t v){return rr(v,2)^rr(v,13)^rr(v,22);}
static uint32_t S1(uint32_t v){return rr(v,6)^rr(v,11)^rr(v,25);}
static uint32_t s0(uint32_t v){return rr(v,7)^rr(v,18)^(v>>3);}
static uint32_t s1(uint32_t v){return rr(v,17)^rr(v,19)^(v>>10);}
static uint32_t Ch(uint32_t x,uint32_t y,uint32_t z){return (x&y)^((~x)&z);}
static uint32_t Maj(uint32_t x,uint32_t y,uint32_t z){return (x&y)^(x&z)^(y&z);}

static const W KM[51]={{{UINT64_C(0xbfdfeff7fbfdfeff),UINT64_C(0xdfeff7fbfdfeff7f),UINT64_C(0xeff7fbfdfeff7fbf),UINT64_C(0xf7fbfdfeff7fbfdf)}},{{UINT64_C(0xfffffffffffffff0),UINT64_C(0x0000000000000007),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000)}},{{UINT64_C(0x4020100804020100),UINT64_C(0x2010080402010080),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000)}},{{UINT64_C(0x3e9f4fa7d3e9f4fa),UINT64_C(0x1f4fa7d3e9f4fa7d),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000)}},{{UINT64_C(0x8040201008040201),UINT64_C(0x0020100804020100),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000)}},{{UINT64_C(0x0201008040201000),UINT64_C(0x0100804020100804),UINT64_C(0x0080402010080402),UINT64_C(0x8040201008040201)}},{{UINT64_C(0xe9f4fa7d3e9f4fa0),UINT64_C(0xf4fa7d3e9f4fa7d3),UINT64_C(0xfa7d3e9f4fa7d3e9),UINT64_C(0x7d3e9f4fa7d3e9f4)}},{{UINT64_C(0x0402010080402010),UINT64_C(0x0201008040201008),UINT64_C(0x0100804020100804),UINT64_C(0x0080402010080402)}},{{UINT64_C(0x0201008040201000),UINT64_C(0x0100804020100804),UINT64_C(0x0000000000000002),UINT64_C(0x0000000000000000)}},{{UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0080402010080400),UINT64_C(0x8040201008040201)}},{{UINT64_C(0x0000000000000000),UINT64_C(0x0100804020100800),UINT64_C(0x0080402010080402),UINT64_C(0x0000000000000001)}},{{UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000800),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000)}},{{UINT64_C(0x0000000000000000),UINT64_C(0x0000004000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000)}},{{UINT64_C(0x0000000000000000),UINT64_C(0x0100000000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000)}},{{UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000002),UINT64_C(0x0000000000000000)}},{{UINT64_C(0x0000000000000000),UINT64_C(0x0000800000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000)}},{{UINT64_C(0x0000000000000000),UINT64_C(0x0000000000100000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000)}},{{UINT64_C(0x0000000000000000),UINT64_C(0x0000000020000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000)}},{{UINT64_C(0x0000008000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000)}},{{UINT64_C(0x0200000000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000)}},{{UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000004),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000)}},{{UINT64_C(0x0001000000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000)}},{{UINT64_C(0x0000000000200000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000)}},{{UINT64_C(0x0000000040000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000)}},{{UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000400),UINT64_C(0x0000000000000000)}},{{UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000002000000000),UINT64_C(0x0000000000000000)}},{{UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0080000000000000),UINT64_C(0x0000000000000000)}},{{UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000001)}},{{UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000400000000000),UINT64_C(0x0000000000000000)}},{{UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000080000),UINT64_C(0x0000000000000000)}},{{UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000010000000),UINT64_C(0x0000000000000000)}},{{UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000200)}},{{UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000001000000000)}},{{UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0040000000000000)}},{{UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000),UINT64_C(0x8000000000000000)}},{{UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000200000000000)}},{{UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000040000)}},{{UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000008000000)}},{{UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000080),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000)}},{{UINT64_C(0x0000000000000000),UINT64_C(0x0000000400000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000)}},{{UINT64_C(0x0000000000000000),UINT64_C(0x0010000000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000)}},{{UINT64_C(0x0000000000000000),UINT64_C(0x2000000000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000)}},{{UINT64_C(0x0000000000000000),UINT64_C(0x0000080000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000)}},{{UINT64_C(0x0000000000000000),UINT64_C(0x0000000000010000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000)}},{{UINT64_C(0x0000000000000000),UINT64_C(0x0000000002000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000)}},{{UINT64_C(0x0000000800000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000)}},{{UINT64_C(0x0020000000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000)}},{{UINT64_C(0x4000000000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000)}},{{UINT64_C(0x0000100000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000)}},{{UINT64_C(0x0000000000020000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000)}},{{UINT64_C(0x0000000004000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000)}}};
enum {NB=1u<<23};
static const uint32_t OM=(1u<<27)-1,PBASE=2u<<25;
static const uint32_t CC2=0x7af32e15u;
static const uint32_t C5=0xdf1a2d2bu;
static const uint32_t CW9=0x88887ba8u;
static const uint32_t CE4=0x8cb35ecdu;
static const uint32_t MA=0x08001a4cu;
static const uint32_t MB=0x0ff9ffdfu;
static const uint32_t KW8=0x23206eabu;
static const uint32_t CA=0x82120040u;
static const uint32_t CB=0x11cdedb6u;
static const uint32_t C1MASK=0xe0000000u;
static const uint32_t C1V=0xa0000000u;
static const uint32_t D7=0x20000000u;
static const uint32_t D8=0xfbc00800u;
static const uint32_t D9=0xe0000000u;
static const uint32_t T7=0x03bff800u;
static const uint32_t T8=0xfe808000u;
static const uint32_t T9=0x043ff800u;
static const uint32_t SE7=0xee321249u;
static const uint32_t SE6=0x925a0446u;
static const uint32_t SA3=0x0a893fdcu;
static const uint32_t SA2=0x0d70da4fu;
static const uint32_t KCONST[38]={0x428a2f98u,0x71374491u,0xb5c0fbcfu,0xe9b5dba5u,0x3956c25bu,0x59f111f1u,0x923f82a4u,0xab1c5ed5u,0xd807aa98u,0x12835b01u,0x243185beu,0x550c7dc3u,0x72be5d74u,0x80deb1feu,0x9bdc06a7u,0xc19bf174u,0xe49b69c1u,0xefbe4786u,0xfc19dc6u,0x240ca1ccu,0x2de92c6fu,0x4a7484aau,0x5cb0a9dcu,0x76f988dau,0x983e5152u,0xa831c66du,0xb00327c8u,0xbf597fc7u,0xc6e00bf3u,0xd5a79147u,0x6ca6351u,0x14292967u,0x27b70a85u,0x2e1b2138u,0x4d2c6dfcu,0x53380d13u,0x650a7354u,0x766a0abbu};
static const uint32_t HEADS[20]={0x4b02d320u,0x7b1ab320u,0x7b22b320u,0x7b3ab320u,0xc802f320u,0xc80ad320u,0xc80af320u,0xc812d320u,0xc822f320u,0xc82ad320u,0xc82af320u,0xc832d320u,0xcb12f320u,0xcb1ad320u,0xcb1af320u,0xcb22d320u,0xcb32f320u,0xcb3ad320u,0xcb3af320u,0xfb02b320u};
#define NOT_H0 KM[0]
static void init_constants(void){}


enum {BC_AND=1,BC_OR=2,BC_XOR=3,BC_NOT=4,BC_SUB=5,BC_ADD=6,BC_LEFT=7,BC_RIGHT=8,BC_LOAD=9,BC_CMPNZ=10,BC_CMPLT=11,BC_CMPNE=12,BC_BR=13,BC_LEGACY=14,BC_EVENT=15,BC_BEGIN=16,BC_LEAF=17,BC_END_FIELD=18,BC_EMIT=19,BC_HALT=20,BC_ADDI=21,BC_MEMLOAD=22,BC_MEMSTORE=23,BC_CMPLTI=24,BC_NATIVE_META=25,BC_VSHIFT=26};
enum {R_W0=0,R_U=1,R_W=2,R_BASE=3,R_B1=4,R_WB=5,R_Q0=6,R_Q4=7,R_ADDR=8,R_TAGA=9,R_TAGB=10,R_V=11,R_RR=12,R_BAD=13,R_MM=14,R_X=15,R_OFF=16,R_DELTA=17,R_FULL=18,R_COUNT=19,R_A0=20,R_A1=21,R_F=22,R_PRED=23,R_T0=24,R_T1=25,R_T2=26,R_PHASE=27,R_ZERO=28,R_CONT=29,R_FOUND=30,R_RESULT=31,R_QUERY_INDEX=32,R_QUERY_LIMIT=33,R_U_START=34,R_LU=35,R_BUDGET=36,R_NV0=37,R_NV1=38,R_NV2=39,R_NV3=40,R_NV4=41,R_NV5=42,R_NV6=43,R_NV7=44,R_NV8=45,R_NV9=46,R_NV10=47,R_NV11=48,R_NV12=49,R_NV13=50,R_NV14=51,R_NV15=52,R_NV16=53,R_NV17=54,R_NV18=55,R_NV19=56,R_NV20=57,R_NV21=58,R_NV22=59,R_NV23=60,R_NV24=61,R_NV25=62,R_NV26=63,R_NV27=64,R_NV28=65,R_NV29=66,R_NV30=67,R_NV31=68,R_NV32=69,R_NV33=70,R_NV34=71,R_NV35=72,R_NV36=73,R_NV37=74,R_NV38=75,R_NV39=76,R_NV40=77,R_NV41=78,R_NV42=79,R_NV43=80,R_NV44=81,R_NV45=82,R_NV46=83,R_NV47=84,R_NV48=85,R_NV49=86,R_NV50=87,R_NV51=88,R_NV52=89,R_NV53=90,R_NV54=91,R_NV55=92,R_NV56=93};
#define POSITIVE_SITE 3u
enum {BC_COUNT=290283,REG_COUNT=94,CONST_COUNT=241};
static const W BC_CONST[]={{{UINT64_C(0x00000000000001ff),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000)}},{{UINT64_C(0xfffffffffffffff8),UINT64_C(0xffffffffffffffff),UINT64_C(0xffffffffffffffff),UINT64_C(0xffffffffffffffff)}},{{UINT64_C(0x0000000000000007),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000)}},{{UINT64_C(0xbfdfeff7fbfdfeff),UINT64_C(0xdfeff7fbfdfeff7f),UINT64_C(0xeff7fbfdfeff7fbf),UINT64_C(0xf7fbfdfeff7fbfdf)}},{{UINT64_C(0x0000000000000004),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000)}},{{UINT64_C(0x0000000000000006),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000)}},{{UINT64_C(0x0000000000000100),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000)}},{{UINT64_C(0x00000000000001fb),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000)}},{{UINT64_C(0x0000000000000001),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000)}},{{UINT64_C(0x00000000007fffff),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000)}},{{UINT64_C(0x0000000000000008),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000)}},{{UINT64_C(0xfffffffffffffff0),UINT64_C(0x0000000000000007),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000)}},{{UINT64_C(0x4020100804020100),UINT64_C(0x2010080402010080),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000)}},{{UINT64_C(0x3e9f4fa7d3e9f4fa),UINT64_C(0x1f4fa7d3e9f4fa7d),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000)}},{{UINT64_C(0x8040201008040201),UINT64_C(0x0020100804020100),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000)}},{{UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000)}},{{UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000080),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000)}},{{UINT64_C(0x0000000000000000),UINT64_C(0x0000000400000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000)}},{{UINT64_C(0x0000000000000000),UINT64_C(0x0010000000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000)}},{{UINT64_C(0x0000000000000000),UINT64_C(0x2000000000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000)}},{{UINT64_C(0x000000000000000a),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000)}},{{UINT64_C(0x0000000007ffffff),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000)}},{{UINT64_C(0x0000000000000005),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000)}},{{UINT64_C(0x0000000000000400),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000)}},{{UINT64_C(0x00000000ffffffff),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000)}},{{UINT64_C(0x0000000000000000),UINT64_C(0x0000080000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000)}},{{UINT64_C(0x0000000000000003),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000)}},{{UINT64_C(0x0000000000000000),UINT64_C(0x0000000000010000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000)}},{{UINT64_C(0x0000000000000000),UINT64_C(0x0000000002000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000)}},{{UINT64_C(0x0000000000000009),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000)}},{{UINT64_C(0x0000000000000002),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000)}},{{UINT64_C(0x0000000800000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000)}},{{UINT64_C(0x0020000000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000)}},{{UINT64_C(0x4000000000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000)}},{{UINT64_C(0x0000100000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000)}},{{UINT64_C(0x0000000000020000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000)}},{{UINT64_C(0x0000000004000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000)}},{{UINT64_C(0x0000000000180bf1),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000)}},{{UINT64_C(0x000000003017e000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000)}},{{UINT64_C(0x0000000000180ff1),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000)}},{{UINT64_C(0x00000000301fe000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000)}},{{UINT64_C(0x0000000000181bf1),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000)}},{{UINT64_C(0x000000003037e000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000)}},{{UINT64_C(0x00000000003e8011),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000)}},{{UINT64_C(0x000000007d002000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000)}},{{UINT64_C(0x00000000003e8401),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000)}},{{UINT64_C(0x000000007d080000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000)}},{{UINT64_C(0x00000000003e8411),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000)}},{{UINT64_C(0x000000007d082000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000)}},{{UINT64_C(0x00000000003e8801),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000)}},{{UINT64_C(0x000000007d100000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000)}},{{UINT64_C(0x00000000003e9011),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000)}},{{UINT64_C(0x000000007d202000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000)}},{{UINT64_C(0x00000000003e9401),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000)}},{{UINT64_C(0x000000007d280000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000)}},{{UINT64_C(0x00000000003e9411),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000)}},{{UINT64_C(0x000000007d282000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000)}},{{UINT64_C(0x00000000003e9801),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000)}},{{UINT64_C(0x000000007d300000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000)}},{{UINT64_C(0x0000000000400811),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000)}},{{UINT64_C(0x0000000080102000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000)}},{{UINT64_C(0x0000000000400c01),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000)}},{{UINT64_C(0x0000000080180000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000)}},{{UINT64_C(0x0000000000400c11),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000)}},{{UINT64_C(0x0000000080182000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000)}},{{UINT64_C(0x0000000000401001),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000)}},{{UINT64_C(0x0000000080200000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000)}},{{UINT64_C(0x0000000000401811),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000)}},{{UINT64_C(0x0000000080302000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000)}},{{UINT64_C(0x0000000000401c01),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000)}},{{UINT64_C(0x0000000080380000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000)}},{{UINT64_C(0x0000000000401c11),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000)}},{{UINT64_C(0x0000000080382000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000)}},{{UINT64_C(0x000000000057fff1),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000)}},{{UINT64_C(0x00000000afffe000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000)}},{{UINT64_C(0x0201008040201000),UINT64_C(0x0100804020100804),UINT64_C(0x0080402010080402),UINT64_C(0x8040201008040201)}},{{UINT64_C(0xe9f4fa7d3e9f4fa0),UINT64_C(0xf4fa7d3e9f4fa7d3),UINT64_C(0xfa7d3e9f4fa7d3e9),UINT64_C(0x7d3e9f4fa7d3e9f4)}},{{UINT64_C(0x0402010080402010),UINT64_C(0x0201008040201008),UINT64_C(0x0100804020100804),UINT64_C(0x0080402010080402)}},{{UINT64_C(0x0201008040201000),UINT64_C(0x0100804020100804),UINT64_C(0x0000000000000002),UINT64_C(0x0000000000000000)}},{{UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000800),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000)}},{{UINT64_C(0x0000000000000000),UINT64_C(0x0000004000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000)}},{{UINT64_C(0x0000000000000000),UINT64_C(0x0100000000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000)}},{{UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000002),UINT64_C(0x0000000000000000)}},{{UINT64_C(0x0000000000000000),UINT64_C(0x0000800000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000)}},{{UINT64_C(0x0000000000000000),UINT64_C(0x0000000000100000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000)}},{{UINT64_C(0x0000000000000000),UINT64_C(0x0000000020000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000)}},{{UINT64_C(0x0000008000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000)}},{{UINT64_C(0x0200000000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000)}},{{UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000004),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000)}},{{UINT64_C(0x0001000000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000)}},{{UINT64_C(0x0000000000200000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000)}},{{UINT64_C(0x0000000040000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000)}},{{UINT64_C(0x0000000000180bf0),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000)}},{{UINT64_C(0x0000000000180ff0),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000)}},{{UINT64_C(0x0000000000181bf0),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000)}},{{UINT64_C(0x00000000003e8010),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000)}},{{UINT64_C(0x00000000003e8400),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000)}},{{UINT64_C(0x00000000003e8410),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000)}},{{UINT64_C(0x00000000003e8800),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000)}},{{UINT64_C(0x00000000003e9010),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000)}},{{UINT64_C(0x00000000003e9400),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000)}},{{UINT64_C(0x00000000003e9410),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000)}},{{UINT64_C(0x00000000003e9800),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000)}},{{UINT64_C(0x0000000000400810),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000)}},{{UINT64_C(0x0000000000400c00),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000)}},{{UINT64_C(0x0000000000400c10),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000)}},{{UINT64_C(0x0000000000401000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000)}},{{UINT64_C(0x0000000000401810),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000)}},{{UINT64_C(0x0000000000401c00),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000)}},{{UINT64_C(0x0000000000401c10),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000)}},{{UINT64_C(0x000000000057fff0),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000)}},{{UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0080402010080400),UINT64_C(0x8040201008040201)}},{{UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000200)}},{{UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000001000000000)}},{{UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0040000000000000)}},{{UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000),UINT64_C(0x8000000000000000)}},{{UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000200000000000)}},{{UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000040000)}},{{UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000008000000)}},{{UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000002000000000),UINT64_C(0x0000000000000000)}},{{UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0080000000000000),UINT64_C(0x0000000000000000)}},{{UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000001)}},{{UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000400000000000),UINT64_C(0x0000000000000000)}},{{UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000080000),UINT64_C(0x0000000000000000)}},{{UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000010000000),UINT64_C(0x0000000000000000)}},{{UINT64_C(0x0000000000000000),UINT64_C(0x0100804020100800),UINT64_C(0x0080402010080402),UINT64_C(0x0000000000000001)}},{{UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000400),UINT64_C(0x0000000000000000)}},{{UINT64_C(0x00000000428a2f98),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000)}},{{UINT64_C(0x0000000071374491),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000)}},{{UINT64_C(0x00000000b5c0fbcf),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000)}},{{UINT64_C(0x00000000e9b5dba5),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000)}},{{UINT64_C(0x000000003956c25b),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000)}},{{UINT64_C(0x0000000059f111f1),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000)}},{{UINT64_C(0x00000000923f82a4),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000)}},{{UINT64_C(0x00000000ab1c5ed5),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000)}},{{UINT64_C(0x00000000d807aa98),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000)}},{{UINT64_C(0x0000000012835b01),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000)}},{{UINT64_C(0x00000000243185be),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000)}},{{UINT64_C(0x00000000550c7dc3),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000)}},{{UINT64_C(0x0000000072be5d74),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000)}},{{UINT64_C(0x0000000080deb1fe),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000)}},{{UINT64_C(0x000000009bdc06a7),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000)}},{{UINT64_C(0x00000000c19bf174),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000)}},{{UINT64_C(0x00000000e49b69c1),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000)}},{{UINT64_C(0x00000000efbe4786),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000)}},{{UINT64_C(0x000000000fc19dc6),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000)}},{{UINT64_C(0x00000000240ca1cc),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000)}},{{UINT64_C(0x000000002de92c6f),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000)}},{{UINT64_C(0x000000004a7484aa),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000)}},{{UINT64_C(0x000000005cb0a9dc),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000)}},{{UINT64_C(0x0000000076f988da),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000)}},{{UINT64_C(0x00000000983e5152),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000)}},{{UINT64_C(0x00000000a831c66d),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000)}},{{UINT64_C(0x00000000b00327c8),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000)}},{{UINT64_C(0x00000000bf597fc7),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000)}},{{UINT64_C(0x00000000c6e00bf3),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000)}},{{UINT64_C(0x00000000d5a79147),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000)}},{{UINT64_C(0x0000000006ca6351),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000)}},{{UINT64_C(0x0000000014292967),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000)}},{{UINT64_C(0x0000000027b70a85),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000)}},{{UINT64_C(0x000000002e1b2138),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000)}},{{UINT64_C(0x000000004d2c6dfc),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000)}},{{UINT64_C(0x0000000053380d13),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000)}},{{UINT64_C(0x00000000650a7354),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000)}},{{UINT64_C(0x00000000766a0abb),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000)}},{{UINT64_C(0x000000000d70da4f),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000)}},{{UINT64_C(0x000000000a893fdc),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000)}},{{UINT64_C(0x000000006570ca61),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000)}},{{UINT64_C(0x00000000b609a403),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000)}},{{UINT64_C(0x000000009602afcd),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000)}},{{UINT64_C(0x00000000aafcae6c),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000)}},{{UINT64_C(0x00000000d420c161),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000)}},{{UINT64_C(0x000000001dc08c8c),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000)}},{{UINT64_C(0x00000000b06ef3bf),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000)}},{{UINT64_C(0x00000000863b8134),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000)}},{{UINT64_C(0x000000002f3e4663),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000)}},{{UINT64_C(0x00000000126cb0f8),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000)}},{{UINT64_C(0x000000005630d804),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000)}},{{UINT64_C(0x00000000b48b6892),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000)}},{{UINT64_C(0x00000000925a0446),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000)}},{{UINT64_C(0x00000000ee321249),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000)}},{{UINT64_C(0x00000000d8250ea0),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000)}},{{UINT64_C(0x0000000040a66b14),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000)}},{{UINT64_C(0x00000000486e19d0),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000)}},{{UINT64_C(0x00000000d2aeac9a),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000)}},{{UINT64_C(0x00000000a8c6827f),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000)}},{{UINT64_C(0x00000000881f1577),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000)}},{{UINT64_C(0x00000000cec8ec41),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000)}},{{UINT64_C(0x000000000dbb8287),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000)}},{{UINT64_C(0x00000000cafcae6c),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000)}},{{UINT64_C(0x00000000d461c971),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000)}},{{UINT64_C(0x00000000b06ff3af),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000)}},{{UINT64_C(0x000000008e3b8930),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000)}},{{UINT64_C(0x000000000e1e4061),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000)}},{{UINT64_C(0x00000000326cb0f8),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000)}},{{UINT64_C(0x000000005e32d894),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000)}},{{UINT64_C(0x00000000b60ae892),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000)}},{{UINT64_C(0x000000000e321249),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000)}},{{UINT64_C(0x00000000f0691630),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000)}},{{UINT64_C(0x0000000043b66b1f),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000)}},{{UINT64_C(0x00000000086f19c0),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000)}},{{UINT64_C(0x00000000f62dac9a),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000)}},{{UINT64_C(0x00000000c1e62e7e),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000)}},{{UINT64_C(0x00000000885f1791),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000)}},{{UINT64_C(0x00000000c6caec41),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000)}},{{UINT64_C(0x000000000dbb8a07),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000)}},{{UINT64_C(0x0000000048421a80),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000)}},{{UINT64_C(0x0000000048021200),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000)}},{{UINT64_C(0x0000000040421200),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000)}},{{UINT64_C(0x0000000020000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000)}},{{UINT64_C(0x000000000000001a),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000)}},{{UINT64_C(0x000000000000000e),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000)}},{{UINT64_C(0x000000000000001c),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000)}},{{UINT64_C(0x000000000000000b),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000)}},{{UINT64_C(0x0000000000000010),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000)}},{{UINT64_C(0x000000000000000f),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000)}},{{UINT64_C(0x0000000000000011),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000)}},{{UINT64_C(0x0000000000000017),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000)}},{{UINT64_C(0x0000000000000019),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000)}},{{UINT64_C(0x000000000000001b),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000)}},{{UINT64_C(0x0000000000000014),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000)}},{{UINT64_C(0x0000000000000016),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000)}},{{UINT64_C(0x000000000000001f),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000)}},{{UINT64_C(0x000000000000001d),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000)}},{{UINT64_C(0x0000000000000012),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000)}},{{UINT64_C(0x000000000000000c),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000)}},{{UINT64_C(0x0000000040421a80),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000)}},{{UINT64_C(0x0000000000000800),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000)}},{{UINT64_C(0x0000000000040010),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000)}},{{UINT64_C(0x0000000040461210),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000)}},{{UINT64_C(0x0000000000421200),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000)}},{{UINT64_C(0x000000000000000d),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000)}},{{UINT64_C(0x0000000001808000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000)}},{{UINT64_C(0x0000000000008000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000)}},{{UINT64_C(0x0000000001848010),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000)}},{{UINT64_C(0x0000000021808000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000)}},{{UINT64_C(0x0000000021008000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000)}},{{UINT64_C(0x0000000000000018),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000)}},{{UINT64_C(0x0000000080000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000)}},{{UINT64_C(0x00000000000000ff),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000)}},{{UINT64_C(0x0000015ac90213d7),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000),UINT64_C(0x0000000000000000)}}};
#define METER_FIXED_CONST 240u

enum {SCANNER_END=273087,NATIVE_WORDS=234};
#define M_IV 0u
#define M_M0 8u
#define M_CV 24u
#define M_PAIR 32u
#define M_STEP_DIGEST 64u
#define M_STATE 80u
#define M_PAD 88u
#define M_TERM_DIGEST 104u
#define M_RECOVERED 120u
#define M_REC_DIGEST 152u
#define M_OUTPUT 168u
#define M_U0 232u
#define M_ROT 233u
#define M_WORDS 234u
#define PC_NATIVE_INITIAL 273087u
#define PC_NATIVE_CALLBACK 275111u
#define PC_FIXTURE_FOUND_CLEAR 290270u
#define PC_FIXTURE_FOUND_SET 290272u
#define PC_FIXTURE_POSITIVE_ARGS 290274u
#define PC_FIXTURE_NEGATIVE_ARGS 290279u
#define PC_QUERY_ENTRY 0u
#define PC_QUERY_LOOP_ADD 273083u
static const uint32_t CALLSITE[640]={455,886,1317,1748,2179,2610,3041,3472,3903,4334,4765,5196,5627,6058,6489,6920,7351,7782,8213,8644,9075,9505,9935,10365,10795,11225,11655,12085,12515,12945,13375,13805,14235,14665,15095,15525,15955,16385,16815,17245,17677,18108,18539,18970,19401,19832,20263,20694,21125,21556,21987,22418,22849,23280,23711,24142,24573,25004,25435,25866,26295,26721,27147,27573,27999,28425,28851,29277,29703,30129,30555,30981,31407,31833,32259,32685,33111,33537,33963,34389,34826,35257,35688,36119,36550,36981,37412,37843,38274,38705,39136,39567,39998,40429,40860,41291,41722,42153,42584,43015,43446,43876,44306,44736,45166,45596,46026,46456,46886,47316,47746,48176,48606,49036,49466,49896,50326,50756,51186,51616,52048,52479,52910,53341,53772,54203,54634,55065,55496,55927,56358,56789,57220,57651,58082,58513,58944,59375,59806,60237,60672,61104,61536,61968,62400,62832,63264,63696,64128,64560,64992,65424,65856,66288,66720,67152,67584,68016,68448,68880,69313,69738,70163,70588,71013,71438,71863,72288,72713,73138,73563,73988,74413,74838,75263,75688,76113,76538,76963,77388,77813,78237,78661,79085,79509,79933,80357,80781,81205,81629,82053,82477,82901,83325,83749,84173,84597,85021,85445,85869,86295,86720,87145,87570,87995,88420,88845,89270,89695,90120,90545,90970,91395,91820,92245,92670,93095,93520,93945,94370,94805,95237,95669,96101,96533,96965,97397,97829,98261,98693,99125,99557,99989,100421,100853,101285,101717,102149,102581,103013,103444,103869,104294,104719,105144,105569,105994,106419,106844,107269,107694,108119,108544,108969,109394,109819,110244,110669,111094,111519,111944,112368,112792,113216,113640,114064,114488,114912,115336,115760,116184,116608,117032,117456,117880,118304,118728,119152,119576,120000,120426,120851,121276,121701,122126,122551,122976,123401,123826,124251,124676,125101,125526,125951,126376,126801,127226,127651,128076,128501,128930,129356,129782,130208,130634,131060,131486,131912,132338,132764,133190,133616,134042,134468,134894,135320,135746,136172,136598,137024,137459,137884,138309,138734,139159,139584,140009,140434,140859,141284,141709,142134,142559,142984,143409,143834,144259,144684,145109,145534,145959,146383,146807,147231,147655,148079,148503,148927,149351,149775,150199,150623,151047,151471,151895,152319,152743,153167,153591,154015,154441,154866,155291,155716,156141,156566,156991,157416,157841,158266,158691,159116,159541,159966,160391,160816,161241,161666,162091,162516,162945,163371,163797,164223,164649,165075,165501,165927,166353,166779,167205,167631,168057,168483,168909,169335,169761,170187,170613,171039,171470,171895,172320,172745,173170,173595,174020,174445,174870,175295,175720,176145,176570,176995,177420,177845,178270,178695,179120,179545,179970,180394,180818,181242,181666,182090,182514,182938,183362,183786,184210,184634,185058,185482,185906,186330,186754,187178,187602,188026,188452,188877,189302,189727,190152,190577,191002,191427,191852,192277,192702,193127,193552,193977,194402,194827,195252,195677,196102,196527,196956,197382,197808,198234,198660,199086,199512,199938,200364,200790,201216,201642,202068,202494,202920,203346,203772,204198,204624,205050,205483,205908,206333,206758,207183,207608,208033,208458,208883,209308,209733,210158,210583,211008,211433,211858,212283,212708,213133,213558,213983,214407,214831,215255,215679,216103,216527,216951,217375,217799,218223,218647,219071,219495,219919,220343,220767,221191,221615,222039,222465,222890,223315,223740,224165,224590,225015,225440,225865,226290,226715,227140,227565,227990,228415,228840,229265,229690,230115,230540,230969,231395,231821,232247,232673,233099,233525,233951,234377,234803,235229,235655,236081,236507,236933,237359,237785,238211,238637,239063,239494,239919,240344,240769,241194,241619,242044,242469,242894,243319,243744,244169,244594,245019,245444,245869,246294,246719,247144,247569,247994,248418,248842,249266,249690,250114,250538,250962,251386,251810,252234,252658,253082,253506,253930,254354,254778,255202,255626,256050,256476,256901,257326,257751,258176,258601,259026,259451,259876,260301,260726,261151,261576,262001,262426,262851,263276,263701,264126,264551,264980,265406,265832,266258,266684,267110,267536,267962,268388,268814,269240,269666,270092,270518,270944,271370,271796,272222,272648,273074};
static const uint32_t CONTINUATION[640]={458,889,1320,1751,2182,2613,3044,3475,3906,4337,4768,5199,5630,6061,6492,6923,7354,7785,8216,8647,9078,9508,9938,10368,10798,11228,11658,12088,12518,12948,13378,13808,14238,14668,15098,15528,15958,16388,16818,17248,17680,18111,18542,18973,19404,19835,20266,20697,21128,21559,21990,22421,22852,23283,23714,24145,24576,25007,25438,25869,26298,26724,27150,27576,28002,28428,28854,29280,29706,30132,30558,30984,31410,31836,32262,32688,33114,33540,33966,34392,34829,35260,35691,36122,36553,36984,37415,37846,38277,38708,39139,39570,40001,40432,40863,41294,41725,42156,42587,43018,43449,43879,44309,44739,45169,45599,46029,46459,46889,47319,47749,48179,48609,49039,49469,49899,50329,50759,51189,51619,52051,52482,52913,53344,53775,54206,54637,55068,55499,55930,56361,56792,57223,57654,58085,58516,58947,59378,59809,60240,60675,61107,61539,61971,62403,62835,63267,63699,64131,64563,64995,65427,65859,66291,66723,67155,67587,68019,68451,68883,69316,69741,70166,70591,71016,71441,71866,72291,72716,73141,73566,73991,74416,74841,75266,75691,76116,76541,76966,77391,77816,78240,78664,79088,79512,79936,80360,80784,81208,81632,82056,82480,82904,83328,83752,84176,84600,85024,85448,85872,86298,86723,87148,87573,87998,88423,88848,89273,89698,90123,90548,90973,91398,91823,92248,92673,93098,93523,93948,94373,94808,95240,95672,96104,96536,96968,97400,97832,98264,98696,99128,99560,99992,100424,100856,101288,101720,102152,102584,103016,103447,103872,104297,104722,105147,105572,105997,106422,106847,107272,107697,108122,108547,108972,109397,109822,110247,110672,111097,111522,111947,112371,112795,113219,113643,114067,114491,114915,115339,115763,116187,116611,117035,117459,117883,118307,118731,119155,119579,120003,120429,120854,121279,121704,122129,122554,122979,123404,123829,124254,124679,125104,125529,125954,126379,126804,127229,127654,128079,128504,128933,129359,129785,130211,130637,131063,131489,131915,132341,132767,133193,133619,134045,134471,134897,135323,135749,136175,136601,137027,137462,137887,138312,138737,139162,139587,140012,140437,140862,141287,141712,142137,142562,142987,143412,143837,144262,144687,145112,145537,145962,146386,146810,147234,147658,148082,148506,148930,149354,149778,150202,150626,151050,151474,151898,152322,152746,153170,153594,154018,154444,154869,155294,155719,156144,156569,156994,157419,157844,158269,158694,159119,159544,159969,160394,160819,161244,161669,162094,162519,162948,163374,163800,164226,164652,165078,165504,165930,166356,166782,167208,167634,168060,168486,168912,169338,169764,170190,170616,171042,171473,171898,172323,172748,173173,173598,174023,174448,174873,175298,175723,176148,176573,176998,177423,177848,178273,178698,179123,179548,179973,180397,180821,181245,181669,182093,182517,182941,183365,183789,184213,184637,185061,185485,185909,186333,186757,187181,187605,188029,188455,188880,189305,189730,190155,190580,191005,191430,191855,192280,192705,193130,193555,193980,194405,194830,195255,195680,196105,196530,196959,197385,197811,198237,198663,199089,199515,199941,200367,200793,201219,201645,202071,202497,202923,203349,203775,204201,204627,205053,205486,205911,206336,206761,207186,207611,208036,208461,208886,209311,209736,210161,210586,211011,211436,211861,212286,212711,213136,213561,213986,214410,214834,215258,215682,216106,216530,216954,217378,217802,218226,218650,219074,219498,219922,220346,220770,221194,221618,222042,222468,222893,223318,223743,224168,224593,225018,225443,225868,226293,226718,227143,227568,227993,228418,228843,229268,229693,230118,230543,230972,231398,231824,232250,232676,233102,233528,233954,234380,234806,235232,235658,236084,236510,236936,237362,237788,238214,238640,239066,239497,239922,240347,240772,241197,241622,242047,242472,242897,243322,243747,244172,244597,245022,245447,245872,246297,246722,247147,247572,247997,248421,248845,249269,249693,250117,250541,250965,251389,251813,252237,252661,253085,253509,253933,254357,254781,255205,255629,256053,256479,256904,257329,257754,258179,258604,259029,259454,259879,260304,260729,261154,261579,262004,262429,262854,263279,263704,264129,264554,264983,265409,265835,266261,266687,267113,267539,267965,268391,268817,269243,269669,270095,270521,270947,271373,271799,272225,272651,273077};


typedef struct {uint32_t k0,E0b,PP,QQ,EF,FF,KF,K2,KK7;} Ctx;
static Ctx context(const uint32_t *v){
 uint32_t a=v[0],b=v[1],c=v[2],d=v[3],e=v[4],f=v[5],g=v[6],h=v[7];
 uint32_t k0=0-S0(a)-Maj(a,b,c)-h-S1(e)-Ch(e,f,g)-KCONST[0];
 return (Ctx){k0,d-S0(a)-Maj(a,b,c),a&b,a|b,e^f,f,CC2+k0-g-KCONST[1],CC2+k0,SE7-2*SA3-a+S0(SA2)-S1(SE6)-KCONST[7]};
}
static uint32_t Ffun(Ctx c,uint32_t a0){uint32_t E0=a0+c.E0b;return a0+c.KF-S0(a0)-(c.PP|(a0&c.QQ))-S1(E0)-(c.FF^(E0&c.EF));}
static unsigned pf(Ctx c,uint32_t a0,uint32_t a1){
 ch(LEGACY,7);uint32_t E5=a1+C5;
 if((E5&C1MASK)!=C1V)return 0;
 ch(LEGACY,22);uint32_t w9=CW9-a1;if(s0(w9+D9)-s0(w9)!=T9)return 1;
 ch(LEGACY,29);uint32_t E4=a0+CE4-(MA|(a1&MB));uint32_t w8=KW8-E4-(CA^(CB&E5));if(s0(w8+D8)-s0(w8)!=T8)return 3;
 ch(LEGACY,30);uint32_t w7=c.KK7+Maj(SA2,a1,a0)-Ch(SE6,E5,E4);if(s0(w7+D7)-s0(w7)!=T7)return 7;return 15;
}
static int fd_ctrl=-1,fd_fields=-1,fd_claws=-1;
static int evidence_allow(int fd,size_t n);
static void write_exact(int fd,const void *p,size_t n){if(fd<0||!evidence_allow(fd,n))return;const char *s=p;while(n){ssize_t k=write(fd,s,n);if(k<=0){perror("write");exit(2);}s+=k;n-=k;}off_t off=lseek(fd,0,SEEK_CUR);if(off>=0&&(off%65536)<128){fsync(fd);posix_fadvise(fd,0,off,POSIX_FADV_DONTNEED);}}
static void control(unsigned op){uint32_t row[4]={event_id,op,ret_id,HF};write_exact(fd_ctrl,row,sizeof(row));control_ops++;}
static void emit_claw(uint32_t a0,uint32_t a1,uint32_t u,uint32_t F,unsigned flags){uint32_t row[5]={a0,a1,u,F,flags};write_exact(fd_claws,row,sizeof(row));claws++;}
static void reset(W *T){for(uint32_t i=0;i<NB+8;i++){store(T,i,ZERO);ch(ADD,2);ch(CMP,1);ch(BR,1);}}
static void build(W *T,Ctx c,unsigned nc,uint32_t R){
 for(uint32_t n=0;n<(1u<<nc);n++){
  uint32_t k=(n+R)&OM,o=(k>>2)|((k&3)<<25),a0=(o&0x1ffffffu)|PBASE|((o>>25)<<28),F=Ffun(c,a0),b=F>>9;
  W w=T[b];uint32_t count=(uint32_t)get(w,252,3);
  if(count<7){set(&w,36*count,9,F&511);set(&w,36*count+9,27,o);set(&w,252,3,count+1);T[b]=w;if(b<3)T[NB+b]=w;ch(LEGACY,57+(b<3?2:0));}
  else ch(LEGACY,45);
 }
}

static void transform_block(W *T,uint32_t b,int verify){
uint64_t before=total();W old[8],out[8],back[8];
old[0]=load(T,aa(b,0));
out[0]=wx(ZERO,ZERO);
old[1]=load(T,aa(b,1));
out[1]=wx(ZERO,ZERO);
old[2]=load(T,aa(b,2));
out[2]=wx(ZERO,ZERO);
old[3]=load(T,aa(b,3));
out[3]=wx(ZERO,ZERO);
old[4]=load(T,aa(b,4));
out[4]=wx(ZERO,ZERO);
old[5]=load(T,aa(b,5));
out[5]=wx(ZERO,ZERO);
old[6]=load(T,aa(b,6));
out[6]=wx(ZERO,ZERO);
old[7]=load(T,aa(b,7));
out[7]=wx(ZERO,ZERO);
uint32_t c0=(uint32_t)wr(old[0],252).x[0];
ch(CMP,1);out[0]=wo(out[0],wl(small(c0==7),0));
{W e=wr(old[0],0),tag=wa(e,small(511)),off=wa(wr(e,9),small(OM));
out[0]=wo(out[0],wl(tag,4));
out[2]=wo(out[2],wl(off,0));
}
{W e=wr(old[0],36),tag=wa(e,small(511)),off=wa(wr(e,9),small(OM));
out[0]=wo(out[0],wl(tag,13));
out[2]=wo(out[2],wl(off,27));
}
{W e=wr(old[0],72),tag=wa(e,small(511)),off=wa(wr(e,9),small(OM));
out[0]=wo(out[0],wl(tag,22));
out[2]=wo(out[2],wl(off,54));
}
{W e=wr(old[0],108),tag=wa(e,small(511)),off=wa(wr(e,9),small(OM));
out[0]=wo(out[0],wl(tag,31));
out[2]=wo(out[2],wl(off,81));
}
{W e=wr(old[0],144),tag=wa(e,small(511)),off=wa(wr(e,9),small(OM));
out[0]=wo(out[0],wl(tag,40));
out[2]=wo(out[2],wl(off,108));
}
{W e=wr(old[0],180),tag=wa(e,small(511)),off=wa(wr(e,9),small(OM));
out[0]=wo(out[0],wl(tag,49));
out[2]=wo(out[2],wl(off,135));
}
{W e=wr(old[0],216),tag=wa(e,small(511)),off=wa(wr(e,9),small(OM));
out[0]=wo(out[0],wl(tag,58));
out[2]=wo(out[2],wl(off,162));
}
out[2]=wo(out[2],wl(small(c0),189));
uint32_t c1=(uint32_t)wr(old[1],252).x[0];
ch(CMP,1);out[1]=wo(out[1],wl(small(c1==7),0));
{W e=wr(old[1],0),tag=wa(e,small(511)),off=wa(wr(e,9),small(OM));
out[1]=wo(out[1],wl(tag,4));
out[2]=wo(out[2],wl(off,192));
}
{W e=wr(old[1],36),tag=wa(e,small(511)),off=wa(wr(e,9),small(OM));
out[1]=wo(out[1],wl(tag,13));
out[2]=wo(out[2],wl(off,219));
}
{W e=wr(old[1],72),tag=wa(e,small(511)),off=wa(wr(e,9),small(OM));
out[1]=wo(out[1],wl(tag,22));
out[2]=wo(out[2],wl(off,246));
out[3]=wo(out[3],wr(off,10));
}
{W e=wr(old[1],108),tag=wa(e,small(511)),off=wa(wr(e,9),small(OM));
out[1]=wo(out[1],wl(tag,31));
out[3]=wo(out[3],wl(off,17));
}
{W e=wr(old[1],144),tag=wa(e,small(511)),off=wa(wr(e,9),small(OM));
out[1]=wo(out[1],wl(tag,40));
out[3]=wo(out[3],wl(off,44));
}
{W e=wr(old[1],180),tag=wa(e,small(511)),off=wa(wr(e,9),small(OM));
out[1]=wo(out[1],wl(tag,49));
out[3]=wo(out[3],wl(off,71));
}
{W e=wr(old[1],216),tag=wa(e,small(511)),off=wa(wr(e,9),small(OM));
out[1]=wo(out[1],wl(tag,58));
out[3]=wo(out[3],wl(off,98));
}
out[3]=wo(out[3],wl(small(c1),125));
uint32_t c2=(uint32_t)wr(old[2],252).x[0];
ch(CMP,1);out[0]=wo(out[0],wl(small(c2==7),1));
{W e=wr(old[2],0),tag=wa(e,small(511)),off=wa(wr(e,9),small(OM));
out[0]=wo(out[0],wl(tag,67));
out[3]=wo(out[3],wl(off,128));
}
{W e=wr(old[2],36),tag=wa(e,small(511)),off=wa(wr(e,9),small(OM));
out[0]=wo(out[0],wl(tag,76));
out[3]=wo(out[3],wl(off,155));
}
{W e=wr(old[2],72),tag=wa(e,small(511)),off=wa(wr(e,9),small(OM));
out[0]=wo(out[0],wl(tag,85));
out[3]=wo(out[3],wl(off,182));
}
{W e=wr(old[2],108),tag=wa(e,small(511)),off=wa(wr(e,9),small(OM));
out[0]=wo(out[0],wl(tag,94));
out[3]=wo(out[3],wl(off,209));
}
{W e=wr(old[2],144),tag=wa(e,small(511)),off=wa(wr(e,9),small(OM));
out[0]=wo(out[0],wl(tag,103));
out[3]=wo(out[3],wl(off,236));
out[4]=wo(out[4],wr(off,20));
}
{W e=wr(old[2],180),tag=wa(e,small(511)),off=wa(wr(e,9),small(OM));
out[0]=wo(out[0],wl(tag,112));
out[4]=wo(out[4],wl(off,7));
}
{W e=wr(old[2],216),tag=wa(e,small(511)),off=wa(wr(e,9),small(OM));
out[0]=wo(out[0],wl(tag,121));
out[4]=wo(out[4],wl(off,34));
}
out[4]=wo(out[4],wl(small(c2),61));
uint32_t c3=(uint32_t)wr(old[3],252).x[0];
ch(CMP,1);out[1]=wo(out[1],wl(small(c3==7),1));
{W e=wr(old[3],0),tag=wa(e,small(511)),off=wa(wr(e,9),small(OM));
out[1]=wo(out[1],wl(tag,67));
out[4]=wo(out[4],wl(off,64));
}
{W e=wr(old[3],36),tag=wa(e,small(511)),off=wa(wr(e,9),small(OM));
out[1]=wo(out[1],wl(tag,76));
out[4]=wo(out[4],wl(off,91));
}
{W e=wr(old[3],72),tag=wa(e,small(511)),off=wa(wr(e,9),small(OM));
out[1]=wo(out[1],wl(tag,85));
out[4]=wo(out[4],wl(off,118));
}
{W e=wr(old[3],108),tag=wa(e,small(511)),off=wa(wr(e,9),small(OM));
out[1]=wo(out[1],wl(tag,94));
out[4]=wo(out[4],wl(off,145));
}
{W e=wr(old[3],144),tag=wa(e,small(511)),off=wa(wr(e,9),small(OM));
out[1]=wo(out[1],wl(tag,103));
out[4]=wo(out[4],wl(off,172));
}
{W e=wr(old[3],180),tag=wa(e,small(511)),off=wa(wr(e,9),small(OM));
out[1]=wo(out[1],wl(tag,112));
out[4]=wo(out[4],wl(off,199));
}
{W e=wr(old[3],216),tag=wa(e,small(511)),off=wa(wr(e,9),small(OM));
out[1]=wo(out[1],wl(tag,121));
out[4]=wo(out[4],wl(off,226));
}
out[4]=wo(out[4],wl(small(c3),253));
uint32_t c4=(uint32_t)wr(old[4],252).x[0];
ch(CMP,1);out[0]=wo(out[0],wl(small(c4==7),2));
{W e=wr(old[4],0),tag=wa(e,small(511)),off=wa(wr(e,9),small(OM));
out[0]=wo(out[0],wl(tag,130));
out[5]=wo(out[5],wl(off,0));
}
{W e=wr(old[4],36),tag=wa(e,small(511)),off=wa(wr(e,9),small(OM));
out[0]=wo(out[0],wl(tag,139));
out[5]=wo(out[5],wl(off,27));
}
{W e=wr(old[4],72),tag=wa(e,small(511)),off=wa(wr(e,9),small(OM));
out[0]=wo(out[0],wl(tag,148));
out[5]=wo(out[5],wl(off,54));
}
{W e=wr(old[4],108),tag=wa(e,small(511)),off=wa(wr(e,9),small(OM));
out[0]=wo(out[0],wl(tag,157));
out[5]=wo(out[5],wl(off,81));
}
{W e=wr(old[4],144),tag=wa(e,small(511)),off=wa(wr(e,9),small(OM));
out[0]=wo(out[0],wl(tag,166));
out[5]=wo(out[5],wl(off,108));
}
{W e=wr(old[4],180),tag=wa(e,small(511)),off=wa(wr(e,9),small(OM));
out[0]=wo(out[0],wl(tag,175));
out[5]=wo(out[5],wl(off,135));
}
{W e=wr(old[4],216),tag=wa(e,small(511)),off=wa(wr(e,9),small(OM));
out[0]=wo(out[0],wl(tag,184));
out[5]=wo(out[5],wl(off,162));
}
out[5]=wo(out[5],wl(small(c4),189));
uint32_t c5=(uint32_t)wr(old[5],252).x[0];
ch(CMP,1);out[1]=wo(out[1],wl(small(c5==7),2));
{W e=wr(old[5],0),tag=wa(e,small(511)),off=wa(wr(e,9),small(OM));
out[1]=wo(out[1],wl(tag,130));
out[5]=wo(out[5],wl(off,192));
}
{W e=wr(old[5],36),tag=wa(e,small(511)),off=wa(wr(e,9),small(OM));
out[1]=wo(out[1],wl(tag,139));
out[5]=wo(out[5],wl(off,219));
}
{W e=wr(old[5],72),tag=wa(e,small(511)),off=wa(wr(e,9),small(OM));
out[1]=wo(out[1],wl(tag,148));
out[5]=wo(out[5],wl(off,246));
out[6]=wo(out[6],wr(off,10));
}
{W e=wr(old[5],108),tag=wa(e,small(511)),off=wa(wr(e,9),small(OM));
out[1]=wo(out[1],wl(tag,157));
out[6]=wo(out[6],wl(off,17));
}
{W e=wr(old[5],144),tag=wa(e,small(511)),off=wa(wr(e,9),small(OM));
out[1]=wo(out[1],wl(tag,166));
out[6]=wo(out[6],wl(off,44));
}
{W e=wr(old[5],180),tag=wa(e,small(511)),off=wa(wr(e,9),small(OM));
out[1]=wo(out[1],wl(tag,175));
out[6]=wo(out[6],wl(off,71));
}
{W e=wr(old[5],216),tag=wa(e,small(511)),off=wa(wr(e,9),small(OM));
out[1]=wo(out[1],wl(tag,184));
out[6]=wo(out[6],wl(off,98));
}
out[6]=wo(out[6],wl(small(c5),125));
uint32_t c6=(uint32_t)wr(old[6],252).x[0];
ch(CMP,1);out[0]=wo(out[0],wl(small(c6==7),3));
{W e=wr(old[6],0),tag=wa(e,small(511)),off=wa(wr(e,9),small(OM));
out[0]=wo(out[0],wl(tag,193));
out[6]=wo(out[6],wl(off,128));
}
{W e=wr(old[6],36),tag=wa(e,small(511)),off=wa(wr(e,9),small(OM));
out[0]=wo(out[0],wl(tag,202));
out[6]=wo(out[6],wl(off,155));
}
{W e=wr(old[6],72),tag=wa(e,small(511)),off=wa(wr(e,9),small(OM));
out[0]=wo(out[0],wl(tag,211));
out[6]=wo(out[6],wl(off,182));
}
{W e=wr(old[6],108),tag=wa(e,small(511)),off=wa(wr(e,9),small(OM));
out[0]=wo(out[0],wl(tag,220));
out[6]=wo(out[6],wl(off,209));
}
{W e=wr(old[6],144),tag=wa(e,small(511)),off=wa(wr(e,9),small(OM));
out[0]=wo(out[0],wl(tag,229));
out[6]=wo(out[6],wl(off,236));
out[7]=wo(out[7],wr(off,20));
}
{W e=wr(old[6],180),tag=wa(e,small(511)),off=wa(wr(e,9),small(OM));
out[0]=wo(out[0],wl(tag,238));
out[7]=wo(out[7],wl(off,7));
}
{W e=wr(old[6],216),tag=wa(e,small(511)),off=wa(wr(e,9),small(OM));
out[0]=wo(out[0],wl(tag,247));
out[7]=wo(out[7],wl(off,34));
}
out[7]=wo(out[7],wl(small(c6),61));
uint32_t c7=(uint32_t)wr(old[7],252).x[0];
ch(CMP,1);out[1]=wo(out[1],wl(small(c7==7),3));
{W e=wr(old[7],0),tag=wa(e,small(511)),off=wa(wr(e,9),small(OM));
out[1]=wo(out[1],wl(tag,193));
out[7]=wo(out[7],wl(off,64));
}
{W e=wr(old[7],36),tag=wa(e,small(511)),off=wa(wr(e,9),small(OM));
out[1]=wo(out[1],wl(tag,202));
out[7]=wo(out[7],wl(off,91));
}
{W e=wr(old[7],72),tag=wa(e,small(511)),off=wa(wr(e,9),small(OM));
out[1]=wo(out[1],wl(tag,211));
out[7]=wo(out[7],wl(off,118));
}
{W e=wr(old[7],108),tag=wa(e,small(511)),off=wa(wr(e,9),small(OM));
out[1]=wo(out[1],wl(tag,220));
out[7]=wo(out[7],wl(off,145));
}
{W e=wr(old[7],144),tag=wa(e,small(511)),off=wa(wr(e,9),small(OM));
out[1]=wo(out[1],wl(tag,229));
out[7]=wo(out[7],wl(off,172));
}
{W e=wr(old[7],180),tag=wa(e,small(511)),off=wa(wr(e,9),small(OM));
out[1]=wo(out[1],wl(tag,238));
out[7]=wo(out[7],wl(off,199));
}
{W e=wr(old[7],216),tag=wa(e,small(511)),off=wa(wr(e,9),small(OM));
out[1]=wo(out[1],wl(tag,247));
out[7]=wo(out[7],wl(off,226));
}
out[7]=wo(out[7],wl(small(c7),253));
store(T,aa(b,0),out[0]);
store(T,aa(b,1),out[1]);
store(T,aa(b,2),out[2]);
store(T,aa(b,3),out[3]);
store(T,aa(b,4),out[4]);
store(T,aa(b,5),out[5]);
store(T,aa(b,6),out[6]);
store(T,aa(b,7),out[7]);
ch(ADD,2);ch(CMP,1);ch(BR,1);
uint64_t count=total()-before;if(count>transform_max)transform_max=count;if(count<transform_min)transform_min=count;
if(verify){memset(back,0,sizeof(back));
set(&back[0],0,9,get(out[0],4,9));set(&back[0],9,27,get(out[2],0,27));
set(&back[0],36,9,get(out[0],13,9));set(&back[0],45,27,get(out[2],27,27));
set(&back[0],72,9,get(out[0],22,9));set(&back[0],81,27,get(out[2],54,27));
set(&back[0],108,9,get(out[0],31,9));set(&back[0],117,27,get(out[2],81,27));
set(&back[0],144,9,get(out[0],40,9));set(&back[0],153,27,get(out[2],108,27));
set(&back[0],180,9,get(out[0],49,9));set(&back[0],189,27,get(out[2],135,27));
set(&back[0],216,9,get(out[0],58,9));set(&back[0],225,27,get(out[2],162,27));
set(&back[0],252,3,get(out[2],189,3));if(!raw_eq(back[0],old[0]))errors++;
set(&back[1],0,9,get(out[1],4,9));set(&back[1],9,27,get(out[2],192,27));
set(&back[1],36,9,get(out[1],13,9));set(&back[1],45,27,get(out[2],219,27));
set(&back[1],72,9,get(out[1],22,9));set(&back[1],81,27,(get(out[2],246,10)|(get(out[3],0,17)<<10)));
set(&back[1],108,9,get(out[1],31,9));set(&back[1],117,27,get(out[3],17,27));
set(&back[1],144,9,get(out[1],40,9));set(&back[1],153,27,get(out[3],44,27));
set(&back[1],180,9,get(out[1],49,9));set(&back[1],189,27,get(out[3],71,27));
set(&back[1],216,9,get(out[1],58,9));set(&back[1],225,27,get(out[3],98,27));
set(&back[1],252,3,get(out[3],125,3));if(!raw_eq(back[1],old[1]))errors++;
set(&back[2],0,9,get(out[0],67,9));set(&back[2],9,27,get(out[3],128,27));
set(&back[2],36,9,get(out[0],76,9));set(&back[2],45,27,get(out[3],155,27));
set(&back[2],72,9,get(out[0],85,9));set(&back[2],81,27,get(out[3],182,27));
set(&back[2],108,9,get(out[0],94,9));set(&back[2],117,27,get(out[3],209,27));
set(&back[2],144,9,get(out[0],103,9));set(&back[2],153,27,(get(out[3],236,20)|(get(out[4],0,7)<<20)));
set(&back[2],180,9,get(out[0],112,9));set(&back[2],189,27,get(out[4],7,27));
set(&back[2],216,9,get(out[0],121,9));set(&back[2],225,27,get(out[4],34,27));
set(&back[2],252,3,get(out[4],61,3));if(!raw_eq(back[2],old[2]))errors++;
set(&back[3],0,9,get(out[1],67,9));set(&back[3],9,27,get(out[4],64,27));
set(&back[3],36,9,get(out[1],76,9));set(&back[3],45,27,get(out[4],91,27));
set(&back[3],72,9,get(out[1],85,9));set(&back[3],81,27,get(out[4],118,27));
set(&back[3],108,9,get(out[1],94,9));set(&back[3],117,27,get(out[4],145,27));
set(&back[3],144,9,get(out[1],103,9));set(&back[3],153,27,get(out[4],172,27));
set(&back[3],180,9,get(out[1],112,9));set(&back[3],189,27,get(out[4],199,27));
set(&back[3],216,9,get(out[1],121,9));set(&back[3],225,27,get(out[4],226,27));
set(&back[3],252,3,get(out[4],253,3));if(!raw_eq(back[3],old[3]))errors++;
set(&back[4],0,9,get(out[0],130,9));set(&back[4],9,27,get(out[5],0,27));
set(&back[4],36,9,get(out[0],139,9));set(&back[4],45,27,get(out[5],27,27));
set(&back[4],72,9,get(out[0],148,9));set(&back[4],81,27,get(out[5],54,27));
set(&back[4],108,9,get(out[0],157,9));set(&back[4],117,27,get(out[5],81,27));
set(&back[4],144,9,get(out[0],166,9));set(&back[4],153,27,get(out[5],108,27));
set(&back[4],180,9,get(out[0],175,9));set(&back[4],189,27,get(out[5],135,27));
set(&back[4],216,9,get(out[0],184,9));set(&back[4],225,27,get(out[5],162,27));
set(&back[4],252,3,get(out[5],189,3));if(!raw_eq(back[4],old[4]))errors++;
set(&back[5],0,9,get(out[1],130,9));set(&back[5],9,27,get(out[5],192,27));
set(&back[5],36,9,get(out[1],139,9));set(&back[5],45,27,get(out[5],219,27));
set(&back[5],72,9,get(out[1],148,9));set(&back[5],81,27,(get(out[5],246,10)|(get(out[6],0,17)<<10)));
set(&back[5],108,9,get(out[1],157,9));set(&back[5],117,27,get(out[6],17,27));
set(&back[5],144,9,get(out[1],166,9));set(&back[5],153,27,get(out[6],44,27));
set(&back[5],180,9,get(out[1],175,9));set(&back[5],189,27,get(out[6],71,27));
set(&back[5],216,9,get(out[1],184,9));set(&back[5],225,27,get(out[6],98,27));
set(&back[5],252,3,get(out[6],125,3));if(!raw_eq(back[5],old[5]))errors++;
set(&back[6],0,9,get(out[0],193,9));set(&back[6],9,27,get(out[6],128,27));
set(&back[6],36,9,get(out[0],202,9));set(&back[6],45,27,get(out[6],155,27));
set(&back[6],72,9,get(out[0],211,9));set(&back[6],81,27,get(out[6],182,27));
set(&back[6],108,9,get(out[0],220,9));set(&back[6],117,27,get(out[6],209,27));
set(&back[6],144,9,get(out[0],229,9));set(&back[6],153,27,(get(out[6],236,20)|(get(out[7],0,7)<<20)));
set(&back[6],180,9,get(out[0],238,9));set(&back[6],189,27,get(out[7],7,27));
set(&back[6],216,9,get(out[0],247,9));set(&back[6],225,27,get(out[7],34,27));
set(&back[6],252,3,get(out[7],61,3));if(!raw_eq(back[6],old[6]))errors++;
set(&back[7],0,9,get(out[1],193,9));set(&back[7],9,27,get(out[7],64,27));
set(&back[7],36,9,get(out[1],202,9));set(&back[7],45,27,get(out[7],91,27));
set(&back[7],72,9,get(out[1],211,9));set(&back[7],81,27,get(out[7],118,27));
set(&back[7],108,9,get(out[1],220,9));set(&back[7],117,27,get(out[7],145,27));
set(&back[7],144,9,get(out[1],229,9));set(&back[7],153,27,get(out[7],172,27));
set(&back[7],180,9,get(out[1],238,9));set(&back[7],189,27,get(out[7],199,27));
set(&back[7],216,9,get(out[1],247,9));set(&back[7],225,27,get(out[7],226,27));
set(&back[7],252,3,get(out[7],253,3));if(!raw_eq(back[7],old[7]))errors++;
}
}



/* Standard programmed-RAM emulator. Logical register/constant names and
 * instruction fetch/decode have no extra lookup charge. Code/banks count as
 * memory. Every logical transfer below is an individually metered literal BR.
 * No logical CALL, RET, computed branch, native callback or hidden join exists.
 */
#include <sys/mman.h>
typedef struct {uint8_t op,d,a,b;uint32_t imm;} Ins;
_Static_assert(sizeof(Ins)==8,"8-byte instruction");
static const Ins *BC;static W R[REG_COUNT],NM[NATIVE_WORDS];
static int fd_primitive=-1,fd_branch=-1,fd_native=-1,fd_new=-1,fd_pairs=-1;
static uint32_t primitive_buffer[16384],branch_buffer[16384],new_buffer[16384],native_buffer[16384];
static size_t primitive_used,branch_used,new_used,native_used;
static uint64_t primitive_records,branch_records,decoded_instructions,new_records,native_records;
static uint64_t evidence_bytes;static int trace_truncated;
static int evidence_allow(int fd,size_t n){
 int evidence=fd==fd_primitive||fd==fd_branch||fd==fd_native||fd==fd_new||fd==fd_pairs||fd==fd_ctrl||fd==fd_fields||fd==fd_claws;
 if(evidence){if(evidence_bytes+n>64u*1024u*1024u){trace_truncated=1;return 0;}evidence_bytes+=n;}return 1;
}
static unsigned trace_scope,trace_case;static int trace_enabled,fixture_scope;
static uint32_t input_m0[16],input_cv[8];
static uint64_t step_calls,accepted_pairs,guard_checks,guard_suppressed,step_before,step_cost,call_output;
static void trace_flush(int fd,uint32_t *buf,size_t *used){
 if(fd<0||!*used)return;write_exact(fd,buf,*used*4);*used=0;
 assert(fdatasync(fd)==0);off_t n=lseek(fd,0,SEEK_CUR);assert(n>=0);assert(posix_fadvise(fd,0,n,POSIX_FADV_DONTNEED)==0);
}
static void native_primitive_category(unsigned op,uint64_t n){
 if(fd_new<0)return;for(uint64_t i=0;i<n;i++){if(new_used==16384)trace_flush(fd_new,new_buffer,&new_used);new_buffer[new_used++]=op;new_records++;}
}
static uint64_t newtotal(void){uint64_t n=0;for(unsigned i=0;i<NOPS;i++)n+=newops[i];return n;}
static void nop(unsigned op){int saved=active_new;active_new=1;ch(op,1);active_new=saved;}
static void trace_primitive(uint32_t pc,uint32_t units){
 if(fd_primitive<0)return;if(primitive_used+2>16384)trace_flush(fd_primitive,primitive_buffer,&primitive_used);
 primitive_buffer[primitive_used++]=pc;primitive_buffer[primitive_used++]=units;primitive_records++;
}
static void trace_branch(uint32_t pc,int taken){
 if(fd_branch<0||active_new)return;if(branch_used+4>16384)trace_flush(fd_branch,branch_buffer,&branch_used);
 uint32_t v[4]={pc,(uint32_t)taken,event_id,ret_id};memcpy(branch_buffer+branch_used,v,16);branch_used+=4;branch_records++;
}
static void trace_native(uint32_t pc,unsigned units,uint32_t next,int taken){
 if(fd_native<0||!active_new)return;if(native_used+8>16384)trace_flush(fd_native,native_buffer,&native_used);
 uint32_t row[8]={trace_scope,trace_case,pc,units,next,(uint32_t)(taken+1),(uint32_t)R[R_CONT].x[0],(uint32_t)R[R_FOUND].x[0]};
 memcpy(native_buffer+native_used,row,32);native_used+=8;native_records++;
}
static void open_traces(void){
 if(!trace_enabled)return;
 fd_primitive=open("primitive.bin",O_WRONLY|O_CREAT|O_EXCL,0644);fd_branch=open("branches.bin",O_WRONLY|O_CREAT|O_EXCL,0644);
 fd_native=open("native_program.bin",O_WRONLY|O_CREAT|O_EXCL,0644);fd_new=open("new_primitive.bin",O_WRONLY|O_CREAT|O_EXCL,0644);fd_pairs=open("pairs.bin",O_WRONLY|O_CREAT|O_EXCL,0644);
 assert(fd_primitive>=0&&fd_branch>=0&&fd_native>=0&&fd_new>=0&&fd_pairs>=0);
}
static void close_traces(void){
 trace_flush(fd_primitive,primitive_buffer,&primitive_used);trace_flush(fd_branch,branch_buffer,&branch_used);trace_flush(fd_native,native_buffer,&native_used);trace_flush(fd_new,new_buffer,&new_used);
 int fds[]={fd_primitive,fd_branch,fd_native,fd_new,fd_pairs};for(unsigned i=0;i<5;i++)if(fds[i]>=0){assert(fsync(fds[i])==0);close(fds[i]);}
 fd_primitive=fd_branch=fd_native=fd_new=fd_pairs=-1;
}
static void init_bytecode(void){
 int fd=open("/out/runtime_program.bin",O_RDONLY);assert(fd>=0);struct stat st;assert(fstat(fd,&st)==0&&st.st_size==(off_t)(BC_COUNT*sizeof(Ins)));
 BC=mmap(NULL,st.st_size,PROT_READ,MAP_PRIVATE,fd,0);assert(BC!=MAP_FAILED);close(fd);
 for(uint32_t i=0;i<BC_COUNT;i++){
  Ins v=BC[i];unsigned raw=v.op&63,op=raw>=33?raw-32:raw;assert(op>=BC_AND&&op<=BC_VSHIFT);
  if(op==BC_BR)assert(v.imm<BC_COUNT);
  if(op<=BC_CMPNE){assert(v.d<REG_COUNT&&v.a<((raw>=33&&(v.op&64))?CONST_COUNT:REG_COUNT));if(op<=BC_ADD||op==BC_CMPLT||op==BC_CMPNE)assert(v.b<((v.op&128)?CONST_COUNT:REG_COUNT));}
  if(op==BC_MEMLOAD||op==BC_MEMSTORE)assert(v.imm<NATIVE_WORDS);
 }
}
static int raw_lt(W a,W b){for(int i=3;i>=0;i--)if(a.x[i]!=b.x[i])return a.x[i]<b.x[i];return 0;}
static int raw_nz(W a){return !!(a.x[0]|a.x[1]|a.x[2]|a.x[3]);}
static void native_metadata(unsigned kind){
 if(kind==1){guard_checks++;if(raw_nz(R[R_FOUND]))guard_suppressed++;}
 if(kind==2){step_calls++;step_before=newtotal();call_output=0;}
 if(kind==3)step_cost=newtotal()-step_before;
 if(kind==5){
  const char *path=fixture_scope?"fixture_messages.bin":"/out/messages.bin";int fd=open(path,O_WRONLY|O_CREAT|O_EXCL,0644);assert(fd>=0);
  for(unsigned j=0;j<64;j++){uint32_t word=(uint32_t)NM[M_OUTPUT+j].x[0];write_exact(fd,&word,4);}assert(fsync(fd)==0);close(fd);accepted_pairs++;call_output=1;
 }
 if(kind==6&&fd_pairs>=0){
  uint32_t row[70]={0};row[0]=fixture_scope;row[1]=R[R_A0].x[0];row[2]=R[R_A1].x[0];row[3]=R[R_U].x[0];row[4]=R[R_F].x[0];row[5]=fixture_scope==2?3:15;row[6]=R[R_RESULT].x[0];row[7]=call_output;row[8]=step_cost;row[9]=newtotal()-step_before;
  for(unsigned j=0;j<8;j++)row[10+j]=NM[M_CV+j].x[0];for(unsigned j=0;j<32;j++)row[18+j]=NM[M_PAIR+j].x[0];for(unsigned j=0;j<16;j++)row[50+j]=NM[M_TERM_DIGEST+j].x[0];write_exact(fd_pairs,row,sizeof(row));
 }
 if(kind==7)for(unsigned j=0;j<8;j++)input_cv[j]=NM[M_CV+j].x[0];
}
static uint32_t run_program(W *T,Ctx c,uint32_t start,uint32_t stop){
 uint32_t pc=start,j=0,f=0,lane=0,phase=0,split=0,valid=0,full=0,flags=0;
 uint64_t logical=0,field_start=0,pf_start=0,pf_charge=0;uint32_t E5=0,E4=0;
 for(;;){
  assert(pc<BC_COUNT);if(pc==stop){active_new=0;return pc;}
  Ins v=BC[pc];unsigned raw=v.op&63,op=raw>=33?raw-32:raw;active_new=(raw>=33||op>=BC_ADDI);if(pc==PC_QUERY_LOOP_ADD)active_new=0;
  uint32_t next=pc+1,units=1;int taken=-1;W a=ZERO,b=ZERO;
  if(op<=BC_CMPNE){a=active_new&&(v.op&64)?BC_CONST[v.a]:R[v.a];b=(v.op&128)?BC_CONST[v.b]:R[v.b];if(!active_new&&(v.op&64)){W t=a;a=b;b=t;}}
  decoded_instructions++;
  switch(op){
   case BC_AND:R[v.d]=wa(a,b);break;case BC_OR:R[v.d]=wo(a,b);break;case BC_XOR:R[v.d]=wx(a,b);break;case BC_NOT:R[v.d]=wn(a);break;
   case BC_SUB:R[v.d]=ws(a,b);break;case BC_ADD:R[v.d]=active_new?add256(a,b):small(aa(a.x[0],b.x[0]));break;
   case BC_LEFT:R[v.d]=wl(a,v.imm);break;case BC_RIGHT:R[v.d]=wr(a,v.imm);break;
   case BC_LOAD:R[v.d]=load(T,a.x[0]);break;
   case BC_CMPNZ:ch(CMP,1);R[v.d]=small(raw_nz(a));break;
   case BC_CMPLT:ch(CMP,1);R[v.d]=small(raw_lt(a,b));break;
   case BC_CMPNE:ch(CMP,1);R[v.d]=small(!raw_eq(a,b));break;
   case BC_BR:taken=v.d?1:(raw_nz(R[v.a])^v.b);ch(BR,1);trace_branch(pc,taken);if(taken)next=v.imm;break;
   case BC_ADDI:R[v.d]=add256(R[v.a],small(v.imm));break;
   case BC_VSHIFT:R[v.d]=wl(R[v.a],(unsigned)R[v.b].x[0]);break;
   case BC_CMPLTI:ch(CMP,1);R[v.d]=small(raw_lt(R[v.a],small(v.imm)));break;
   case BC_MEMLOAD:ch(LD,1);R[v.d]=NM[v.imm];break;
   case BC_MEMSTORE:ch(ST,1);NM[v.imm]=(v.op&64)?BC_CONST[v.a]:R[v.a];break;
   case BC_NATIVE_META:units=0;native_metadata(v.d);break;
   case BC_LEGACY:{
    uint32_t a0=R[R_A0].x[0],a1=R[R_A1].x[0];units=v.imm;
    if(v.d==0)ch(ADD,units);
    else{ch(LEGACY,units);
     if(v.d==1){valid=1;uint32_t off=R[R_OFF].x[0];R[R_A0]=small((off&0x1ffffffu)|PBASE|((off>>25)<<28));}
     if(v.d==2)R[R_A1]=small((uint32_t)R[R_U].x[0]-(uint32_t)R[R_F].x[0]+c.K2+a0);
     if(v.d==3){pf_start=logical;flags=0;E5=a1+C5;R[R_T0]=small((E5&C1MASK)!=C1V);}
     if(v.d==4){flags=1;uint32_t w9=CW9-a1;R[R_T0]=small(s0(w9+D9)-s0(w9)!=T9);}
     if(v.d==5){flags=3;E4=a0+CE4-(MA|(a1&MB));uint32_t w8=KW8-E4-(CA^(CB&E5));R[R_T0]=small(s0(w8+D8)-s0(w8)!=T8);}
     if(v.d==6){flags=7;uint32_t w7=c.KK7+Maj(SA2,a1,a0)-Ch(SE6,E5,E4);R[R_T0]=small(s0(w7+D7)-s0(w7)!=T7);}
     if(v.d==7)flags=15;
     if(v.d==8){ops[LEGACY]-=units;ch(ADD,units);}
     if(v.d==9){uint32_t u=(uint32_t)R[R_U_START].x[0]+(uint32_t)R[R_QUERY_INDEX].x[0],p=s0(u)-u;R[R_U]=small(u);R[R_W0]=small(HEADS[0]-p);}

    }break;
   }
   case BC_EVENT:units=0;events++;event_id++;ret_id=v.imm;break;
   case BC_BEGIN:units=0;fields++;field_start=logical;pf_charge=0;valid=0;flags=0;R[R_A0]=R[R_A1]=R[R_F]=ZERO;break;
   case BC_LEAF:{units=0;j=v.imm&255;phase=(v.imm>>8)&255;split=v.imm>>16;f=j/7;lane=j%7;unsigned bucket=(phase+2*f)%8;W src=R[phase>=6&&f?R_TAGB:R_TAGA];full=!!(src.x[0]&(1u<<(bucket/2)));R[R_COUNT]=small(7);if(split)split_gathers++;if(!full)nonfull_fallbacks++;break;}
   case BC_EMIT:units=0;pf_charge=logical-pf_start;if(!fixture_scope)emit_claw(R[R_A0].x[0],R[R_A1].x[0],R[R_U].x[0],R[R_F].x[0],flags);break;
   case BC_END_FIELD:{
    units=0;uint64_t prefix=logical-field_start-pf_charge+1;if(prefix>field_max)field_max=prefix;if(!valid)invalids++;
    uint32_t row[20]={event_id,ret_id,(ret_id-1)%20,phase,(uint32_t)R[R_W0].x[0]&511,((ret_id-1)%80)>=60,j,f,lane,R[R_OFF].x[0],R[R_DELTA].x[0],R[R_F].x[0],R[R_A0].x[0],R[R_A1].x[0],full,R[R_COUNT].x[0],valid,flags,prefix,split};write_exact(fd_fields,row,sizeof(row));break;
   }
   case BC_HALT:units=0;trace_native(pc,0,next,-1);active_new=0;return pc;
   default:assert(0);
  }
  if(active_new)trace_native(pc,units,next,taken);else if(units)trace_primitive(pc,units);
  if(!active_new)logical+=units;pc=next;
 }
}
static void run_queries(W *T,Ctx c,unsigned LU){R[R_LU]=small(LU);trace_scope=0;run_program(T,c,PC_QUERY_ENTRY,UINT32_MAX);}


static uint64_t file_number(const char *path){int f=open(path,O_RDONLY);if(f<0)return 0;char b[128];ssize_t n=read(f,b,127);close(f);if(n<=0)return 0;b[n]=0;return strtoull(b,NULL,10);}
static uint64_t stat_number(const char *key){int f=open("/sys/fs/cgroup/memory.stat",O_RDONLY);if(f<0)return 0;char b[8192];ssize_t n=read(f,b,sizeof(b)-1);close(f);if(n<=0)return 0;b[n]=0;char *p=b;while(*p){char k[80];uint64_t v;if(sscanf(p,"%79s %"SCNu64,k,&v)==2&&strcmp(k,key)==0)return v;p=strchr(p,'\n');if(!p)break;p++;}return 0;}
static double sec(clockid_t c){struct timespec t;clock_gettime(c,&t);return t.tv_sec+t.tv_nsec*1e-9;}
static void summary(const char *mode,double cpu,double wall){
 struct rusage r;getrusage(RUSAGE_SELF,&r);struct stat st;assert(stat("/prototype/bin/prototype",&st)==0);
 /* The runner copies the entire static image inside this cgroup before exec. */
 uint64_t peak=file_number("/sys/fs/cgroup/memory.peak"),rss=(uint64_t)r.ru_maxrss*1024,whole=peak;if(rss>whole)whole=rss;
 printf("{\"status\":\"%s\",\"mode\":\"%s\",\"errors\":%"PRIu64",\"events\":%"PRIu64",\"fields\":%"PRIu64",\"claws\":%"PRIu64",\"invalids\":%"PRIu64",\"control_ops\":%"PRIu64",\"field_max\":%"PRIu64",\"split_gathers\":%"PRIu64",\"nonfull_fallbacks\":%"PRIu64",\"normal_heads\":%"PRIu64",\"strad_heads\":%"PRIu64",\"transform_max\":%"PRIu64",\"transform_min\":%"PRIu64",\"table_bytes\":%zu,\"binary_bytes\":%jd,\"cgroup_memory_peak\":%"PRIu64",\"rss_peak_bytes\":%"PRIu64",\"whole_peak_upper_bytes\":%"PRIu64",\"cgroup_kernel_current\":%"PRIu64",\"cgroup_file_current\":%"PRIu64",\"cpu_seconds\":%.9f,\"wall_seconds\":%.9f,\"op_counts\":{",errors?"FAIL":"PASS",mode,errors,events,fields,claws,invalids,control_ops,field_max,split_gathers,nonfull_fallbacks,normal_heads,strad_heads,transform_max,transform_min,(size_t)(NB+8)*32,(intmax_t)st.st_size,peak,rss,whole,stat_number("kernel"),stat_number("file"),sec(CLOCK_PROCESS_CPUTIME_ID)-cpu,sec(CLOCK_MONOTONIC)-wall);
 for(int i=0;i<NOPS;i++)printf("%s\"%s\":%"PRIu64,i?",":"",opnames[i],ops[i]);puts("}}");
}
static uint32_t mix(uint32_t x){x^=x>>16;x*=0x7feb352du;x^=x>>15;x*=0x846ca68bu;x^=x>>16;return x;}
static void synthetic_block(W *T,uint32_t base,uint32_t salt){for(unsigned r=0;r<8;r++){W w={{0}};unsigned count=(r+salt)%8;for(unsigned i=0;i<count;i++){set(&w,36*i,9,mix(base+r*13+i+salt)&511);set(&w,36*i+9,27,mix(base+r*97+i+salt)&OM);}set(&w,252,3,count);T[base+r]=w;}}

/* Actual bounded outer controller. The ideal algorithm draws independent uniform
 * 256-bit words. The fixture backend supplies retained deterministic words and
 * makes no statistical independence claim. /dev/urandom is an engineering
 * realization, not evidence proving ideal coins. Every draw is charged RAND.
 * Phase transfers are explicit, metered, and have finite literal destinations.
 */
#define N_CV_LIMIT UINT64_C(12014587405061634)
#define CAP_HI UINT64_C(1266860634)
#define CAP_LO UINT64_C(10892272558156595546)
static const uint32_t NIV[8]={1779033703u,3144134277u,1013904242u,2773480762u,1359893119u,2600822924u,528734635u,1541459225u};
static const uint32_t FIXTURE_CV[8]={2510440793u,3020242837u,468731710u,514538364u,1695310803u,3863559483u,3976220445u,3950947027u};
static __uint128_t work_counter,work_cap;static int fd_outer=-1,coin_fd=-1,fixture_coins;
static uint64_t cvidx,completed_cv,coins_drawn,query_index,outer_records;
static uint64_t check_base,check_new;
enum {O_LIMIT=1,O_CAP=2,O_INITIAL_ENTRY=3,O_INITIAL_EXIT=4,O_QUERY_ENTRY=5,O_QUERY_EXIT=6,O_SUCCESS=7,O_LOOP=8,O_COMMIT=9,O_COIN=10,O_STOP=11,O_INJECT=12};
/* These symbolic destinations are a finite programmed-RAM control graph.
 * Native destinations below are actual immutable bytecode indices. */
enum {PC_OUTER_LIMIT=1000000,PC_OUTER_CAP,PC_OUTER_COINS,PC_OUTER_BUILD,PC_OUTER_AFTER_QUERY,PC_OUTER_SUCCESS,PC_OUTER_REPORT,PC_OUTER_STOP};
static void outer_event(unsigned kind,int taken,uint64_t value,uint32_t target){
 if(fd_outer<0)return;assert(outer_records<100000);uint32_t row[16]={kind,(uint32_t)taken,(uint32_t)cvidx,cvidx>>32,(uint32_t)query_index,query_index>>32,(uint32_t)value,value>>32,target,(uint32_t)work_counter,(uint32_t)(work_counter>>32),(uint32_t)(work_counter>>64),(uint32_t)(work_counter>>96),0,0,0};write_exact(fd_outer,row,sizeof(row));outer_records++;
}
static W coin_word(void){
 W w;size_t got=0;while(got<32){ssize_t n=read(coin_fd,(char*)&w+got,32-got);if(n<=0){fputs("coin interface exhausted\n",stderr);exit(2);}got+=n;}
 nop(RAND);coins_drawn++;outer_event(O_COIN,1,coins_drawn,PC_OUTER_COINS);return w;
}
static uint32_t prepare_coins(uint32_t *rotation){
 active_new=1;
 for(unsigned half=0;half<2;half++){
  W packed=coin_word();for(unsigned j=0;j<8;j++){W field=j?wr(packed,j*32):packed;if(j<7)field=wa(field,small(UINT32_MAX));ch(ST,1);NM[M_M0+8*half+j]=field;input_m0[8*half+j]=field.x[0];}
 }
 W u=wa(coin_word(),small(UINT32_MAX));ch(ST,1);NM[M_U0]=u;R[R_U_START]=u;
 W r=wa(coin_word(),small(OM));ch(ST,1);NM[M_ROT]=r;active_new=0;*rotation=r.x[0];return u.x[0];
}
static void finish_work(unsigned future_branch){
 int saved=active_new;active_new=1;R[R_BUDGET]=add256(R[R_BUDGET],BC_CONST[METER_FIXED_CONST]);active_new=saved;
 work_counter=(__uint128_t)R[R_BUDGET].x[0]|((__uint128_t)R[R_BUDGET].x[1]<<64);
 outer_event(O_COMMIT,1,future_branch,PC_OUTER_LIMIT);
}
static void finish_stop(unsigned future_branch){
 int saved=active_new;active_new=1;R[R_BUDGET]=add256(R[R_BUDGET],ZERO);active_new=saved;
 outer_event(O_COMMIT,1,future_branch,PC_OUTER_LIMIT);
}

static void open_evidence(void){
 if(!trace_enabled)return;fd_ctrl=open("control.bin",O_WRONLY|O_CREAT|O_EXCL,0644);fd_fields=open("fields.bin",O_WRONLY|O_CREAT|O_EXCL,0644);fd_claws=open("claws.bin",O_WRONLY|O_CREAT|O_EXCL,0644);assert(fd_ctrl>=0&&fd_fields>=0&&fd_claws>=0);open_traces();
}
static void close_evidence(void){
 close_traces();int fds[]={fd_ctrl,fd_fields,fd_claws};for(unsigned i=0;i<3;i++)if(fds[i]>=0){assert(fsync(fds[i])==0);close(fds[i]);}fd_ctrl=fd_fields=fd_claws=-1;
}
static void dump_table(W *T,uint64_t *stored){
 int fd=trace_enabled?open("table.bin",O_WRONLY|O_CREAT|O_EXCL,0644):-1;if(trace_enabled)assert(fd>=0);
 uint32_t buf[16384];unsigned used=0;*stored=0;
 for(uint32_t b=0;b<NB;b++){unsigned n=get(T[b],252,3);*stored+=n;if(fd>=0)for(unsigned j=0;j<n;j++){buf[used++]=(b<<9)|get(T[b],36*j,9);buf[used++]=get(T[b],36*j+9,27);if(used==16384){write_exact(fd,buf,sizeof(buf));used=0;}}}
 if(fd>=0){write_exact(fd,buf,used*4);assert(fsync(fd)==0);close(fd);}
}
static void diagnostic_inputs(unsigned nc,unsigned LU,uint32_t u,uint32_t rotation){
 if(!trace_enabled)return;uint32_t words[12];memcpy(words,input_cv,32);words[8]=u;words[9]=rotation;words[10]=nc;words[11]=LU;int fd=open("input.bin",O_WRONLY|O_CREAT|O_EXCL,0644);assert(fd>=0);write_exact(fd,words,sizeof(words));close(fd);
 fd=open("m0.bin",O_WRONLY|O_CREAT|O_EXCL,0644);assert(fd>=0);write_exact(fd,input_m0,64);close(fd);
}
static void exercise_callbacks(W *T,Ctx c){
 uint32_t savedcv[8];memcpy(savedcv,input_cv,32);W savedmem[8];for(unsigned j=0;j<8;j++){savedmem[j]=NM[M_CV+j];NM[M_CV+j]=small(FIXTURE_CV[j]);}
 fixture_scope=1;trace_scope=2;trace_case=0;run_program(T,c,PC_FIXTURE_FOUND_CLEAR,UINT32_MAX);run_program(T,c,PC_FIXTURE_POSITIVE_ARGS,UINT32_MAX);
 uint64_t before=accepted_pairs;run_program(T,c,CALLSITE[POSITIVE_SITE],CONTINUATION[POSITIVE_SITE]);assert(accepted_pairs==before+1&&raw_nz(R[R_FOUND]));
 /* Every actual callsite, every dispatcher direction, and repeated found
  * suppression execute through the real bytecode, while the full table lives. */
 for(unsigned i=0;i<640;i++){trace_case=i+1;uint64_t calls=step_calls;run_program(T,c,CALLSITE[i],CONTINUATION[i]);assert(step_calls==calls&&accepted_pairs==before+1);}
 for(unsigned i=0;i<2;i++){trace_case=641+i;run_program(T,c,CALLSITE[0],CONTINUATION[0]);assert(accepted_pairs==before+1);}
 /* PA0+1 has flags3 and fails G. Direct Step3b-boundary injection only. */
 fixture_scope=2;trace_case=643;run_program(T,c,PC_FIXTURE_FOUND_CLEAR,UINT32_MAX);run_program(T,c,PC_FIXTURE_NEGATIVE_ARGS,UINT32_MAX);run_program(T,c,CALLSITE[0],CONTINUATION[0]);assert(R[R_RESULT].x[0]==0);
 run_program(T,c,PC_FIXTURE_FOUND_CLEAR,UINT32_MAX);fixture_scope=0;trace_scope=0;
 for(unsigned j=0;j<8;j++)NM[M_CV+j]=savedmem[j];memcpy(input_cv,savedcv,32);
}
static void cv_summary(FILE *f,unsigned nc,unsigned LU,uint64_t queries,uint64_t stored,uint64_t b0[NOPS],uint64_t n0[NOPS],uint64_t online_new,uint64_t fixture_new,uint64_t initial_new,uint64_t ordinary_found){
 struct rusage ru;getrusage(RUSAGE_SELF,&ru);struct stat st;assert(stat("/out/runtime_binary",&st)==0);
 fprintf(f,"{\"status\":\"%s\",\"mode\":\"holdout\",\"cv_index\":%"PRIu64",\"nc\":%u,\"LU\":%u,\"queries\":%"PRIu64",\"stored\":%"PRIu64",\"errors\":%"PRIu64",\"events\":%"PRIu64",\"fields\":%"PRIu64",\"claws\":%"PRIu64",\"invalids\":%"PRIu64",\"split_gathers\":%"PRIu64",\"field_max\":%"PRIu64",\"transform_min\":%"PRIu64",\"transform_max\":%"PRIu64",\"step_calls\":%"PRIu64",\"accepted_including_fixture\":%"PRIu64",\"ordinary_output\":%"PRIu64",\"guard_checks\":%"PRIu64",\"guard_suppressed\":%"PRIu64",\"table_bytes\":%zu,\"native_RAM_bytes\":%zu,\"binary_bytes\":%jd,\"bytecode_bytes\":%u,\"rss_peak_bytes\":%lu,\"cgroup_memory_peak\":%"PRIu64",\"initial_new\":%"PRIu64",\"online_new\":%"PRIu64",\"fixture_new\":%"PRIu64",\"new_records\":%"PRIu64",\"native_program_records\":%"PRIu64",\"trace_truncated\":%d,\"op_counts\":{",errors?"FAIL":"PASS",cvidx,nc,LU,queries,stored,errors,events,fields,claws,invalids,split_gathers,field_max,transform_min,transform_max,step_calls,accepted_pairs,ordinary_found,guard_checks,guard_suppressed,(size_t)(NB+8)*32,sizeof(NM),(intmax_t)st.st_size,BC_COUNT*8,(unsigned long)ru.ru_maxrss*1024,file_number("/sys/fs/cgroup/memory.peak"),initial_new,online_new,fixture_new,new_records,native_records,trace_truncated);
 for(unsigned i=0;i<NOPS;i++)fprintf(f,"%s\"%s\":%"PRIu64,i?",":"",opnames[i],ops[i]-b0[i]);fputs("},\"new_op_counts\":{",f);for(unsigned i=0;i<NOPS;i++)fprintf(f,"%s\"%s\":%"PRIu64,i?",":"",opnames[i],newops[i]-n0[i]);fprintf(f,"},\"work_counter_hex\":\"%016"PRIx64"%016"PRIx64"\",\"coin_words_consumed\":%"PRIu64"}\n",(uint64_t)(work_counter>>64),(uint64_t)work_counter,coins_drawn);
}
int main(int argc,char **argv){
 if(argc<4||argc>10){fputs("usage: complete coins.bin|ideal nc LU [max_cv] [trace0or1] [fixtures0or1] [cap_after_cv] [synthetic_stop_after_cv]\n",stderr);return 2;}
 unsigned nc=strtoul(argv[2],0,10),LU=strtoul(argv[3],0,10);uint64_t cv_limit=argc>4?strtoull(argv[4],0,10):N_CV_LIMIT;
 trace_enabled=argc>5?strtoul(argv[5],0,10):0;unsigned fixtures=argc>6?strtoul(argv[6],0,10):0;uint64_t cap_after=argc>7?strtoull(argv[7],0,10):0,synthetic_stop=argc>8?strtoull(argv[8],0,10):0;
 if(nc>27||LU>32||cv_limit>N_CV_LIMIT||!cv_limit||trace_enabled>1||fixtures>1||(trace_enabled&&(cv_limit>4||LU>12))||(fixtures&&!trace_enabled)||((cap_after||synthetic_stop)&&!trace_enabled))return 2;
 fixture_coins=strcmp(argv[1],"ideal")!=0;coin_fd=open(fixture_coins?argv[1]:"/dev/urandom",O_RDONLY);if(coin_fd<0)return 2;
 setvbuf(stdout,NULL,_IONBF,0);double cpu=sec(CLOCK_PROCESS_CPUTIME_ID),wall=sec(CLOCK_MONOTONIC);init_constants();init_bytecode();for(unsigned j=0;j<8;j++)NM[M_IV+j]=small(NIV[j]);
 work_cap=((__uint128_t)CAP_HI<<64)|CAP_LO;W *T=NULL;if(posix_memalign((void**)&T,4096,(size_t)(NB+8)*32))return 2;
 if(trace_enabled){fd_outer=open("/out/outer_control.bin",O_WRONLY|O_CREAT|O_EXCL,0644);assert(fd_outer>=0);}
 uint64_t final_queries=0,last_stored=0;__uint128_t total_queries=0;const char *termination="BOUND_EXHAUSTED";uint64_t b0[NOPS],n0[NOPS];
 check_base=total();check_new=newtotal();
LOOP_CHECK:
 nop(CMP);nop(BR);outer_event(O_LIMIT,cvidx<cv_limit,cv_limit,cvidx<cv_limit?PC_OUTER_CAP:PC_OUTER_STOP);if(cvidx>=cv_limit)goto BOUND_STOP;
 nop(CMP);nop(BR);outer_event(O_CAP,work_counter<=work_cap,(uint64_t)work_cap,work_counter<=work_cap?PC_OUTER_COINS:PC_OUTER_STOP);if(work_counter>work_cap)goto CAP_STOP;
 memcpy(b0,ops,sizeof(ops));memcpy(n0,newops,sizeof(newops));
 events=fields=claws=invalids=split_gathers=field_max=step_calls=accepted_pairs=guard_checks=guard_suppressed=0;transform_min=UINT64_MAX;transform_max=0;event_id=ret_id=0;new_records=native_records=primitive_records=branch_records=decoded_instructions=0;trace_truncated=0;evidence_bytes=0;
 if(trace_enabled){assert(chdir("/out")==0);char path[128];snprintf(path,sizeof(path),"/out/cv%06"PRIu64,cvidx);assert(mkdir(path,0777)==0);assert(chdir(path)==0);}open_evidence();
 uint32_t rotation,u0=prepare_coins(&rotation);trace_scope=1;trace_case=cvidx;
 nop(BR);outer_event(O_INITIAL_ENTRY,1,0,PC_NATIVE_INITIAL);uint64_t init0=newtotal();Ctx empty={0};run_program(T,empty,PC_NATIVE_INITIAL,UINT32_MAX);uint64_t initial_new=newtotal()-init0;nop(BR);outer_event(O_INITIAL_EXIT,1,0,PC_OUTER_BUILD);
 Ctx c=context(input_cv);ch(LEGACY,76);diagnostic_inputs(nc,LU,u0,rotation);
 reset(T);build(T,c,nc,rotation);last_stored=0;if(trace_enabled)dump_table(T,&last_stored);for(uint32_t b=0;b<NB;b+=8)transform_block(T,b,trace_enabled);for(unsigned j=0;j<8;j++)store(T,NB+j,load(T,j));
 final_queries=UINT64_C(1)<<LU;
 nop(BR);outer_event(O_QUERY_ENTRY,1,0,PC_QUERY_ENTRY);run_queries(T,c,LU);nop(BR);outer_event(O_QUERY_EXIT,1,0,PC_OUTER_AFTER_QUERY);
 query_index=R[R_QUERY_INDEX].x[0];assert(query_index==final_queries);
 total_queries+=final_queries;
 if(synthetic_stop&&cvidx+1==synthetic_stop){trace_scope=3;trace_case=cvidx;run_program(T,c,PC_FIXTURE_FOUND_SET,UINT32_MAX);outer_event(O_INJECT,1,synthetic_stop,PC_OUTER_SUCCESS);}
 nop(ADD);completed_cv=cvidx+1;
 uint64_t before_fixture=newtotal(),ordinary_found=raw_nz(R[R_FOUND]);
 if(fixtures&&completed_cv==cv_limit&&!ordinary_found)exercise_callbacks(T,c);
 uint64_t fixture_new=newtotal()-before_fixture;
 /* Diagnostics are outside algorithm accounting. Their counter span is
  * skipped before the next real cap commit. */
 check_new+=fixture_new;
 nop(CMP);nop(BR);outer_event(O_SUCCESS,ordinary_found,completed_cv,ordinary_found?PC_OUTER_SUCCESS:PC_OUTER_LIMIT);
 if(ordinary_found)goto SUCCESS_CV;
 finish_work(1);nop(BR);outer_event(O_LOOP,1,completed_cv,PC_OUTER_LIMIT);
 uint64_t online_new=0;for(unsigned i=0;i<NOPS;i++)online_new+=newops[i]-n0[i];online_new-=fixture_new;
 close_evidence();
 if(trace_enabled){FILE *f=fopen("summary.json","wx");assert(f);cv_summary(f,nc,LU,final_queries,last_stored,b0,n0,online_new,fixture_new,initial_new,ordinary_found);assert(fclose(f)==0);}
 cvidx=completed_cv;
 if(cap_after&&completed_cv==cap_after)work_cap=work_counter;
 goto LOOP_CHECK;
BOUND_STOP:
 termination="BOUND_EXHAUSTED";finish_stop(1);nop(BR);outer_event(O_STOP,1,0,PC_OUTER_REPORT);goto REPORT;
CAP_STOP:
 termination="CAP_EXHAUSTED";finish_stop(1);nop(BR);outer_event(O_STOP,1,0,PC_OUTER_REPORT);goto REPORT;
SUCCESS_CV:
 finish_work(0);termination=synthetic_stop?"SYNTHETIC_SUCCESS_STOP":"SUCCESS";
 online_new=0;for(unsigned i=0;i<NOPS;i++)online_new+=newops[i]-n0[i];online_new-=fixture_new;
 close_evidence();
 if(trace_enabled){FILE *f=fopen("summary.json","wx");assert(f);cv_summary(f,nc,LU,final_queries,last_stored,b0,n0,online_new,fixture_new,initial_new,ordinary_found);assert(fclose(f)==0);}
REPORT:
 if(fd_outer>=0){assert(fsync(fd_outer)==0);close(fd_outer);}close(coin_fd);
 struct rusage ru;getrusage(RUSAGE_SELF,&ru);
 char query_decimal[48],rev[48];unsigned digits=0;__uint128_t qprint=total_queries;
 do{rev[digits++]=(char)('0'+qprint%10);qprint/=10;}while(qprint);for(unsigned i=0;i<digits;i++)query_decimal[i]=rev[digits-1-i];query_decimal[digits]=0;
 printf("{\"status\":\"%s\",\"mode\":\"bounded_outer\",\"termination\":\"%s\",\"completed_CVs\":%"PRIu64",\"CV_limit\":%"PRIu64",\"algorithm_N_CV\":%"PRIu64",\"nc\":%u,\"LU\":%u,\"queries\":\"%s\",\"last_stored\":%"PRIu64",\"table_bytes\":%zu,\"native_RAM_bytes\":%zu,\"named_bank_words\":%u,\"coin_words_consumed\":%"PRIu64",\"coin_interface\":\"%s\",\"trace_enabled\":%d,\"trace_truncated\":%d,\"ordinary_output\":%d,\"cgroup_memory_peak\":%"PRIu64",\"rss_peak_bytes\":%lu,\"work_counter_hex\":\"%016"PRIx64"%016"PRIx64"\",\"cpu_seconds\":%.9f,\"wall_seconds\":%.9f}\n",errors?"FAIL":"PASS",termination,completed_cv,cv_limit,N_CV_LIMIT,nc,LU,query_decimal,last_stored,(size_t)(NB+8)*32,sizeof(NM),REG_COUNT+CONST_COUNT,coins_drawn,fixture_coins?"deterministic_fixture_words":"OS_backend_for_abstract_ideal_uniform_primitive",trace_enabled,trace_truncated,strcmp(termination,"SUCCESS")==0,file_number("/sys/fs/cgroup/memory.peak"),(unsigned long)ru.ru_maxrss*1024,(uint64_t)(work_counter>>64),(uint64_t)work_counter,sec(CLOCK_PROCESS_CPUTIME_ID)-cpu,sec(CLOCK_MONOTONIC)-wall);
 free(T);return errors?1:0;
}

```

## Appendix VM. Expanded organizer source

The compressed transport expands to the following exact UTF-8 bytes. It is supplied as inert review text.

```python
"""Single-file organizer experiment prototype, derived from current p1b38.py.

P1 construction, filters and Step 3b retain Jbenisek's credited derivation;
the scan follows newjordan and the bucket/tag layout follows 0xplemonade.
This is reduced semantic evidence, not a new collision or cost certificate.
The bytecode's inherited LEGACY blocks retain their original aggregate prices.
"""
import sys, json, hashlib, struct, bisect, array, base64, zlib
M = 0xffffffff
NR = 38
K = [0x428a2f98, 0x71374491, 0xb5c0fbcf, 0xe9b5dba5, 0x3956c25b, 0x59f111f1, 0x923f82a4, 0xab1c5ed5, 0xd807aa98, 0x12835b01, 0x243185be,
     0x550c7dc3, 0x72be5d74, 0x80deb1fe, 0x9bdc06a7, 0xc19bf174, 0xe49b69c1, 0xefbe4786, 0x0fc19dc6, 0x240ca1cc, 0x2de92c6f, 0x4a7484aa,
     0x5cb0a9dc, 0x76f988da, 0x983e5152, 0xa831c66d, 0xb00327c8, 0xbf597fc7, 0xc6e00bf3, 0xd5a79147, 0x06ca6351, 0x14292967, 0x27b70a85,
     0x2e1b2138, 0x4d2c6dfc, 0x53380d13, 0x650a7354, 0x766a0abb]
IV = [0x6a09e667, 0xbb67ae85, 0x3c6ef372, 0xa54ff53a, 0x510e527f, 0x9b05688c, 0x1f83d9ab, 0x5be0cd19]
def ror(x, n): return ((x >> n) | (x << (32 - n))) & M
def S0(x): return ror(x, 2) ^ ror(x, 13) ^ ror(x, 22)
def S1(x): return ror(x, 6) ^ ror(x, 11) ^ ror(x, 25)
def s0(x): return ror(x, 7) ^ ror(x, 18) ^ (x >> 3)
def s1(x): return ror(x, 17) ^ ror(x, 19) ^ (x >> 10)
def CH(x, y, z): return (x & y) ^ (~x & z & M)
def MAJ(x, y, z): return (x & y) ^ (x & z) ^ (y & z)

def trace(cv, w16, n=NR):
    """A[i], E[i] (i = -4..n-1, dicts) and W[0..n-1] of the first n steps from the chaining value cv."""
    W = list(w16)
    for i in range(16, n): W.append((s1(W[i-2]) + W[i-7] + s0(W[i-15]) + W[i-16]) & M)
    A = {-1-i: cv[i] for i in range(4)}; E = {-1-i: cv[4+i] for i in range(4)}
    for i in range(n):
        E[i] = (A[i-4] + E[i-4] + S1(E[i-1]) + CH(E[i-1], E[i-2], E[i-3]) + K[i] + W[i]) & M
        A[i] = (E[i] - A[i-4] + S0(A[i-1]) + MAJ(A[i-1], A[i-2], A[i-3])) & M
    return A, E, W

def compress(cv, w16, n=NR):
    A, E, W = trace(cv, w16, n)
    f = [A[n-1], A[n-2], A[n-3], A[n-4], E[n-1], E[n-2], E[n-3], E[n-4]]
    return [(cv[i] + f[i]) & M for i in range(8)]

GL = [549441552, 549441553, 549441556, 549441557, 549442576, 549442577, 549442580, 549442581, 1891627024, 1891627025, 1891627028, 1891627029, 1891628048, 1891628049, 1891628052, 1891628053, 2698498064, 2698498065, 2698498068, 2698498069, 2698499088, 2698499089, 2698499092, 2698499093, 2699022352, 2699022353, 2699022356, 2699022357, 2699023376, 2699023377, 2699023380, 2699023381, 2700595216, 2700595217, 2700595220, 2700595221, 2700596240, 2700596241, 2700596244, 2700596245, 3988787216, 3988787217, 3988787220, 3988787221, 3988788240, 3988788241, 3988788244, 3988788245, 3989303312, 3989303313, 3989303316, 3989303317, 3989304336, 3989304337, 3989304340, 3989304341, 3989311504, 3989311505, 3989311508, 3989311509, 3989312528, 3989312529, 3989312532, 3989312533, 3989827600, 3989827601, 3989827604, 3989827605, 3989828624, 3989828625, 3989828628, 3989828629, 3990884368, 3990884369, 3990884372, 3990884373, 3990885392, 3990885393, 3990885396, 3990885397, 3991400464, 3991400465, 3991400468, 3991400469, 3991401488, 3991401489, 3991401492, 3991401493, 3991408656, 3991408657, 3991408660, 3991408661, 3991409680, 3991409681, 3991409684, 3991409685, 3991924752, 3991924753, 3991924756, 3991924757, 3991925776, 3991925777, 3991925780, 3991925781, 4040167440, 4040167441, 4040167444, 4040167445, 4040168464, 4040168465, 4040168468, 4040168469, 4040683536, 4040683537, 4040683540, 4040683541, 4040684560, 4040684561, 4040684564, 4040684565, 4040691728, 4040691729, 4040691732, 4040691733, 4040692752, 4040692753, 4040692756, 4040692757, 4041207824, 4041207825, 4041207828, 4041207829, 4041208848, 4041208849, 4041208852, 4041208853, 4042264592, 4042264593, 4042264596, 4042264597, 4042265616, 4042265617, 4042265620, 4042265621, 4042780688, 4042780689, 4042780692, 4042780693, 4042781712, 4042781713, 4042781716, 4042781717, 4042788880, 4042788881, 4042788884, 4042788885, 4042789904, 4042789905, 4042789908, 4042789909]
PCV = [2510440793, 3020242837, 468731710, 514538364, 1695310803, 3863559483, 3976220445, 3950947027]
PMX = [3171188373, 499730577, 1270760843, 3353099274, 2338469345, 2641768686, 1453171616, 2497556930, 1179538525, 2818885938, 2901196405, 3358065010, 2588764008, 370382130, 3758975641, 1605534331]
PMY = [3171188373, 499730577, 1270760843, 3353099274, 2338469345, 2641768686, 1453171616, 3034427842, 1108237405, 2282015026, 2850925791, 3357543794, 2588764008, 370382130, 3758975641, 1542621819]

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
CELLS = [[(0, 0, 0)] * NR for _ in range(3)]; PQ = [0] * NR; _PL = {}
for _r, _l in enumerate(_ROWS):
    for _k, _s in enumerate(_l.split()):
        m_ = v_ = x_ = p_ = 0
        for _j, _c in enumerate(_s):
            b_ = 1 << (31 - _j); m_ |= b_ * (_c in 'un01'); v_ |= b_ * (_c in 'u1'); x_ |= b_ * (_c in 'un'); p_ |= b_ * (_c == '+')
        CELLS[_k][_r + 7] = (m_, v_, x_); _PL[_r + 7] = _PL.get(_r + 7, 0) | p_
for _i in _PL: PQ[_i] = _PL[_i] & _PL.get(_i - 1, 0)
PQE = list(PQ); PQE[18] = 0
for _i in (7, 8): CELLS[2][_i] = (0, 0, 0)      # W7, W8: only their modular and s0 differences matter (F7, C1, G); not tested by step 3b
X2 = []
for _t in ('E16 7 = E16 26,E16 14 ! E16 28,A15 4 = A16 4,E16 11 = E16 16,A15 7 = A16 7,A14 15 = A16 15,A14 16 = A16 16,A15 17 = A16 17,'
           'A14 23 = A16 23,A14 25 = A16 25,A15 27 = A16 27,E16 3 ! E16 8,E16 4 = E16 23,W16 20 ! W16 27,W16 22 = W16 31,W16 4 ! W16 6,'
           'A15 29 = A16 29,W16 14 = W16 18,W16 8 = W16 25,W16 1 ! W16 12,A17 9 ! A17 20,A16 15 = A17 15,A17 6 = A17 18,A16 16 ! A17 16,'
           'A16 23 = A17 23,A16 25 = A17 25,A17 8 ! A17 17,E18 0 = E18 13,E18 17 = E18 22,E18 5 ! E18 23,A16 29 = A18 29,E18 9 = E18 23,'
           'E21 10 = E21 15,E21 11 = E21 24,E21 2 = E21 16').split(','):
    _a, _b, _e, _c, _d = _t.split()
    X2.append(('AEW'.index(_a[0]), int(_a[1:]), int(_b), int(_e == '='), 'AEW'.index(_c[0]), int(_c[1:]), int(_d), max(int(_a[1:]), int(_c[1:]))))

_tx, _ty = trace(PCV, PMX), trace(PCV, PMY)
SA = [{i: t[0][i] for i in range(-4, 16)} for t in (_tx, _ty)]       # A rows of S, member x (0) and y (1)
SE = [{i: t[1][i] for i in range(-4, 16)} for t in (_tx, _ty)]       # E rows of S
SW = [PMX, PMY]
assert all(SA[0][i] == SA[1][i] for i in range(-4, 7)) and all(SE[0][i] == SE[1][i] for i in range(-4, 7))
D7 = (PMY[7] - PMX[7]) & M; D8 = (PMY[8] - PMX[8]) & M; D9 = (PMY[9] - PMX[9]) & M
T7 = (s0(PMY[7]) - s0(PMX[7])) & M; T8 = (s0(PMY[8]) - s0(PMX[8])) & M; T9 = (s0(PMY[9]) - s0(PMX[9])) & M
def inF7(w): return ((s0((w + D7) & M) - s0(w)) & M) == T7

def pair_words(cv, a0, a1):
    """W0..W15 of both members of the P1 pair: A0 = a0, A1 = a1, A2..A15 and E6..E15 of S, rows -4..-1 from cv (step equations)."""
    out = []
    for m in (0, 1):
        A = {-1: cv[0], -2: cv[1], -3: cv[2], -4: cv[3], 0: a0, 1: a1}; E = {-1: cv[4], -2: cv[5], -3: cv[6], -4: cv[7]}
        for i in range(2, 16): A[i] = SA[m][i]
        for i in range(6): E[i] = (A[i] + A[i-4] - S0(A[i-1]) - MAJ(A[i-1], A[i-2], A[i-3])) & M
        for i in range(6, 16): E[i] = SE[m][i]
        out.append([(E[i] - A[i-4] - E[i-4] - S1(E[i-1]) - CH(E[i-1], E[i-2], E[i-3]) - K[i]) & M for i in range(16)])
    return out

C5 = (SA[0][5] - S0(SA[0][4]) - MAJ(SA[0][4], SA[0][3], SA[0][2])) & M
C9 = (SE[0][9] - SA[0][5] - S1(SE[0][8]) - CH(SE[0][8], SE[0][7], SE[0][6]) - K[9]) & M
C16 = (SA[0][12] + SE[0][12] + S1(SE[0][15]) + CH(SE[0][15], SE[0][14], SE[0][13]) + K[16]) & M
CC2 = (C16 + s1(PMX[14]) + C9 - C5) & M
S160 = sorted((C16 + g) & M for g in GL)          # the E16x values that pass row 16 with all its conditions (exhaustive, 160 words)
R16F = 0x405                                       # the 160 words are 20 heads times the 8 values of bits 0, 2, 10
HEADS = sorted(set(e & ~R16F & M for e in S160))
OFFS = (0, 1, 4, 5, 1024, 1025, 1028, 1029)
assert len(HEADS) == 20 and sorted((h + o) & M for h in HEADS for o in OFFS) == S160

PBASE = 2 << 25
def p_a0(o): return (o & 0x1ffffff) | PBASE | ((o >> 25) << 28)
def p_off(a0): return (a0 & 0x1ffffff) | (((a0 >> 28) & 3) << 25)
def in_P(a0): return (a0 >> 25) & 7 == 2 and a0 >> 30 == 0

def cvc(cv):
    """the claw scalars of one chaining value: k0 (W0 = a0 + k0), E0 base, MAJ and CH helpers, KF (F = a0 + KF - S0 - MAJ - S1 - CH),
    K2 = CC2 + k0 (a1 = u - F + K2 + a0) and the F7 constant KK7 (W7x = KK7 + MAJ(A2, a1, a0) - CH(E6, E5, E4))."""
    a, b, c, d, e, f, g, h = cv
    k0 = (-S0(a) - MAJ(a, b, c) - h - S1(e) - CH(e, f, g) - K[0]) & M
    return dict(k0=k0, E0b=(d - S0(a) - MAJ(a, b, c)) & M, PP=a & b, QQ=a | b, EF=e ^ f, FF=f, KF=(CC2 + k0 - g - K[1]) & M,
                K2=(CC2 + k0) & M, KK7=(SE[0][7] - 2 * SA[0][3] - a + S0(SA[0][2]) - S1(SE[0][6]) - K[7]) & M)
def Ffun(c, a0):
    E0 = (a0 + c['E0b']) & M
    return (a0 + c['KF'] - S0(a0) - (c['PP'] | (a0 & c['QQ'])) - S1(E0) - (c['FF'] ^ (E0 & c['EF']))) & M
def hfun(c, a0): return (Ffun(c, a0) - CC2 - a0 - c['k0']) & M

CE4 = (SA[0][4] - S0(SA[0][3])) & M; MA = SA[0][3] & SA[0][2]; MB = SA[0][3] | SA[0][2]          # E4 = a0 + CE4 - MAJ(A3, A2, a1)
KW8 = (SE[0][8] - SA[0][4] - S1(SE[0][7]) - K[8]) & M; CA = SE[0][7] & SE[0][6]; CB = ~SE[0][7] & M  # W8x = KW8 - E4 - (CA ^ (CB & E5))
CW9 = (C9 - C5) & M                                                                                 # W9x = CW9 - a1
_DCH = ((SE[1][8] - SE[0][8]) - (S1(SE[1][7]) - S1(SE[0][7])) - D8) & M
C1V = [p for p in range(8) if ((CH(SE[1][7], SE[1][6], p << 29) - CH(SE[0][7], SE[0][6], p << 29)) & M) == _DCH]
assert len(C1V) == 1; C1V = C1V[0] << 29; C1MASK = 0xe0000000

def pf_ref(cv, a0, a1):
    """the four post-filters on the real words of the two members: C1 dW8 = D8, C2 s0(W9) diff, G s0(W8) diff, F7 s0(W7) diff (W7y - W7x
    = D7 and W9y - W9x = D9 always); the cumulative stage flags"""
    wx, wy = pair_words(cv, a0, a1)
    c1 = ((wy[8] - wx[8]) & M) == D8; c2 = ((s0(wy[9]) - s0(wx[9])) & M) == T9; g = ((s0(wy[8]) - s0(wx[8])) & M) == T8
    f7 = ((s0(wy[7]) - s0(wx[7])) & M) == T7 and ((wy[7] - wx[7]) & M) == D7
    return (int(c1), int(c1 and c2), int(c1 and c2 and g), int(c1 and c2 and g and f7))

def cellok(k, i, x, y):
    m, v, d = CELLS[k][i]; return (x & m) == v and (x ^ y) == d
def rowok(tx, ty, i):
    (Ax, Ex, Wx), (Ay, Ey, Wy) = tx, ty
    if not (cellok(0, i, Ax[i], Ay[i]) and cellok(1, i, Ex[i], Ey[i]) and cellok(2, i, Wx[i], Wy[i])): return False
    if (Ex[i] ^ Ex[i-1]) & PQE[i]: return False
    for (k1, i1, b1, eq, k2, i2, b2, row) in X2:
        if row == i and (((tx[k1][i1] >> b1) ^ (tx[k2][i2] >> b2)) & 1) != (0 if eq else 1): return False
    return True
def outputs_equal(tx, ty): return all(tx[k][i] == ty[k][i] for k in (0, 1) for i in range(34, 38))
def accepted(tx, ty): return all(rowok(tx, ty, i) for i in range(16, 22)) and outputs_equal(tx, ty)

NBK = 1 << 23; LANE = 36; NL = 7; OMASK = (1 << 27) - 1; W256 = (1 << 256) - 1
def _rep(v, pos): return sum(v << (LANE * i + pos) for i in range(NL))
TM0 = _rep(511, 0); TM1 = _rep(511, 11); LM7 = _rep((1 << 22) - 1, 0)
K512 = _rep(512, 0) | _rep(512, 11); M3FA = _rep(0x3fa, 0) | _rep(0x3fa, 11); G10 = _rep(1, 10) | _rep(1, 21); L0 = _rep(1, 0) | _rep(1, 11)
H0 = HEADS[0]; assert all((h - H0) & 0x1fff == 0 for h in HEADS)
DH = [((h - H0) & M) >> 9 for h in HEADS]                    # bucket deltas of the heads (multiples of 16)
def rotr2(n): return (n >> 2) | ((n & 3) << 25)
def build_table(c, NC, m=None, R=0):
    T = {}
    for n in range(NC):
        o = rotr2((n + R) & OMASK); a0 = p_a0(o); F = Ffun(c, a0); b = F >> 9; wd = T.get(b, 0); cnt = wd >> 252
        if cnt < 7:
            wd = wd | (((o << 9) | (F & 511)) << (LANE * cnt)); wd += 1 << 252; T[b] = wd
            if b < 3: T[NBK + b] = wd
            assert m is None
        elif m: raise AssertionError('unexpanded build price')
    return T
def entries(T):
    """(F, o) of every stored entry (padding words excluded)"""
    out = []
    for b, wd in T.items():
        if b >= NBK: continue
        for i in range(wd >> 252):
            e = (wd >> (LANE * i)) & ((1 << LANE) - 1); out.append(((b << 9) | (e & 511), e >> 9))
    return out

class Shake:
    def __init__(self, seed): self.seed = seed.encode(); self.k = 0; self.buf = b''; self.pos = 0
    def word(self):
        if self.pos + 32 > len(self.buf):
            self.buf = hashlib.shake_256(self.seed + b'|' + str(self.k).encode()).digest(1 << 14); self.k += 1; self.pos = 0
        v = int.from_bytes(self.buf[self.pos:self.pos + 32], 'little'); self.pos += 32; return v
    def u32(self): return self.word() & M
def first_block(rng):
    r0, r1 = rng.word(), rng.word()
    M0 = [(r0 >> (32 * q)) & M for q in range(8)] + [(r1 >> (32 * q)) & M for q in range(8)]
    return M0, compress(IV, M0)

import collections, ast, re, heapq, types



class Instructions:
 def __init__(self):self.raw=bytearray()
 def __len__(self):return len(self.raw)//8
 def append(self,v):self.raw.extend(struct.pack('<4BI',*v))
 def __iter__(self):return struct.iter_unpack('<4BI',self.raw)
 def __getitem__(self,i):
  if i<0:i+=len(self)
  class View:
   def __getitem__(_,j):return struct.unpack_from('<4BI',self.raw,i*8)[j]
   def __setitem__(_,j,v):
    if j<4:self.raw[i*8+j]=v
    else:struct.pack_into('<I',self.raw,i*8+4,v)
  return View()

def native_text():
 lines=[]
 def out(x):lines.append(x)
 def val(x):return str(x&0xffffffff)+'u'
 def name(m,k,i):return f'v{m}{k}{i+4}'
 def a(m,i):return name(m,'a',i)
 def e(m,i):return name(m,'e',i)
 def w(m,i):return name(m,'w',i)
 def add(*xs):
  r=xs[0]
  for x in xs[1:]:r=f'na({r},{x})'
  return r
 def sub(*xs):
  r=xs[0]
  for x in xs[1:]:r=f'ns({r},{x})'
  return r
 def save(v,x):out(f'uint32_t {v}={x};')
 out('static int native_step(const uint32_t cv[8],uint32_t a0,uint32_t a1,uint32_t pair[2][16],uint32_t digest[2][8]){')
 for m in range(2):
  for i in range(4):save(a(m,-1-i),f'nload(cv+{i})');save(e(m,-1-i),f'nload(cv+{4+i})')
  save(a(m,0),'a0');save(a(m,1),'a1')
  for i in range(2,16):save(a(m,i),val(SA[m][i]))
  for i in range(6):save(e(m,i),sub(add(a(m,i),a(m,i-4)),f'nS0({a(m,i-1)})',f'nMaj({a(m,i-1)},{a(m,i-2)},{a(m,i-3)})'))
  for i in range(6,16):save(e(m,i),val(SE[m][i]))
  for i in range(16):
   save(w(m,i),sub(e(m,i),a(m,i-4),e(m,i-4),f'nS1({e(m,i-1)})',f'nCh({e(m,i-1)},{e(m,i-2)},{e(m,i-3)})',val(K[i])))
   out(f'nstore(&pair[{m}][{i}],{w(m,i)});')
 for i in range(16,38):
  for m in range(2):
   save(w(m,i),add(f'ns1({w(m,i-2)})',w(m,i-7),f'ns0({w(m,i-15)})',w(m,i-16)))
   save(e(m,i),add(a(m,i-4),e(m,i-4),f'nS1({e(m,i-1)})',f'nCh({e(m,i-1)},{e(m,i-2)},{e(m,i-3)})',val(K[i]),w(m,i)))
   save(a(m,i),add(sub(e(m,i),a(m,i-4)),f'nS0({a(m,i-1)})',f'nMaj({a(m,i-1)},{a(m,i-2)},{a(m,i-3)})'))
  if i<22:
   for k,fn in enumerate((a,e,w)):
    mask,v,d=CELLS[k][i]
    if mask:out(f'if(nne(nand({fn(0,i)},{val(mask)}),{val(v)}))return {i-16};')
    out(f'if(nne(nx({fn(0,i)},{fn(1,i)}),{val(d)}))return {i-16};')
   if PQE[i]:out(f'if(nne(nand(nx({e(0,i)},{e(0,i-1)}),{val(PQE[i])}),0u))return {i-16};')
   for k1,i1,b1,eq,k2,i2,b2,row in X2:
    if row==i:
     f1=(a,e,w)[k1];f2=(a,e,w)[k2]
     out(f'if(nne(nand(nx(nr({f1(0,i1)},{b1}),nr({f2(0,i2)},{b2})),1u),{0 if eq else 1}u))return {i-16};')
 for k,fn in enumerate((a,e)):
  for i in range(34,38):out(f'if(nne({fn(0,i)},{fn(1,i)}))return 6;')
 for m in range(2):
  for j in range(8):out(f'nstore(&digest[{m}][{j}],na({(a,e)[j//4](m,37-j%4)},nload(cv+{j})));')
 out('return 7;}')
 out('static void native_compress(const uint32_t cv[8],const uint32_t block[16],uint32_t result[8]){')
 for i in range(4):save(a(0,-1-i),f'nload(cv+{i})');save(e(0,-1-i),f'nload(cv+{4+i})')
 for i in range(16):save(w(0,i),f'nload(block+{i})')
 for i in range(38):
  if i>=16:save(w(0,i),add(f'ns1({w(0,i-2)})',w(0,i-7),f'ns0({w(0,i-15)})',w(0,i-16)))
  save(e(0,i),add(a(0,i-4),e(0,i-4),f'nS1({e(0,i-1)})',f'nCh({e(0,i-1)},{e(0,i-2)},{e(0,i-3)})',val(K[i]),w(0,i)))
  save(a(0,i),add(sub(e(0,i),a(0,i-4)),f'nS0({a(0,i-1)})',f'nMaj({a(0,i-1)},{a(0,i-2)},{a(0,i-3)})'))
 for j in range(8):out(f'nstore(result+{j},na({(a,e)[j//4](0,37-j%4)},nload(cv+{j})));')
 out('}')
 return '\n'.join(lines)+'\nstatic void digest_messages('

class NativeCompiler:
 def __init__(self,A):
  self.A=A;self.env={};self.free=[];self.allocated=set();self.first=len(A['regs']);self.high=self.first;self.serial=0;self.memory=A['memory'];self.sections=[]
 def temporary(self):
  if self.free:r=heapq.heappop(self.free)
  else:
   r=self.high;self.high+=1;name='NV'+str(r-self.first);self.A['regs'][name]=r;self.A['register_names'].append(name)
  assert r not in self.allocated;self.allocated.add(r);return ('r',r)
 def release(self,x):
  if x[0]=='r' and x[1]>=self.first and x[1] in self.allocated:self.allocated.remove(x[1]);heapq.heappush(self.free,x[1])
 def constant(self,x):return ('k',self.A['const'](x))
 def reg(self,name):return ('r',self.A['regs'][name])
 def emit(self,op,d=None,a=None,b=None,imm=0):
  native_op=self.A['opcode'][op]+32 if op in self.A['old_names'] else self.A['opcode'][op]
  raw=native_op
  if a and a[0]=='k':raw|=64
  if b and b[0]=='k':raw|=128
  self.A['code'].append([raw,0 if d is None else d[1],0 if a is None else a[1],0 if b is None else b[1],imm]);return len(self.A['code'])-1
 def op(self,op,a=None,b=None,imm=0):
  d=self.temporary();self.emit(op,d,a,b,imm);return d
 def label(self,name):self.A['label'](name)
 def branch(self,target,pred=None,invert=False):
  pc=self.emit('BR',('r',int(pred is None)),pred or ('r',0),('r',int(invert)))
  self.A['fixups'].append((pc,target));return pc
 def cmpbranch(self,a,b,target,invert=False):
  pred=self.op('CMPNE',a,b);self.branch(target,pred,invert);self.release(pred)
 def immediate(self,name,value):self.emit('ADDI',self.reg(name),self.reg('ZERO'),imm=value)
 def load(self,slot):return self.op('MEMLOAD',imm=slot)
 def store(self,slot,x):self.emit('MEMSTORE',a=x,imm=slot)
 def metadata(self,kind,imm=0):self.emit('NATIVE_META',('r',kind),imm=imm)
 def parse(self,text):
  text=re.sub(r'&(pair|digest)\[(\d+)\]\[(\d+)\]',r'ptr_\1_\2_\3',text)
  text=re.sub(r'\b(cv|block|result)\+(\d+)',r'ptr_\1_\2',text)
  text=re.sub(r'\b(\d+)u\b',r'\1',text)
  return ast.parse(text,mode='eval').body
 def expression(self,node):
  if isinstance(node,ast.Constant):return self.constant(node.value),[]
  if isinstance(node,ast.Name):
   if node.id.startswith('ptr_'):return node.id,[]
   assert node.id in self.env,node.id
   return self.env[node.id],[]
  assert isinstance(node,ast.Call) and isinstance(node.func,ast.Name)
  fn=node.func.id;args=[];owned=[]
  for n in node.args:
   v,o=self.expression(n);args.append(v);owned+=o
  out=None
  def op(k,a,b=None,imm=0):
   x=self.op(k,a,b,imm);owned.append(x);return x
  def raw(x):assert x[0]=='k';return self.A['pool'][x[1]]
  if fn=='nload':out=op('MEMLOAD',None,imm=self.ptr[args[0]])
  elif fn=='nstore':self.store(self.ptr[args[0]],args[1])
  elif fn in ('na','ns'):
   t=op('ADD' if fn=='na' else 'SUB',*args);out=op('AND',t,self.constant(0xffffffff))
  elif fn in ('nand','nx','no','nor32','nxx'):out=op({'nand':'AND','nx':'XOR','no':'OR','nor32':'OR','nxx':'XOR'}[fn],*args)
  elif fn in ('nl','nr'):out=op('LEFT' if fn=='nl' else 'RIGHT',args[0],imm=raw(args[1]))
  elif fn=='nmask':out=op('AND',args[0],self.constant(0xffffffff))
  elif fn in ('nS0','nS1','ns0','ns1'):
   a,b,c,small={'nS0':(2,13,22,False),'nS1':(6,11,25,False),'ns0':(7,18,3,True),'ns1':(17,19,10,True)}[fn]
   y=op('OR',op('LEFT',args[0],imm=32),args[0]);x=op('XOR',op('RIGHT',y,imm=a),op('RIGHT',y,imm=b));out=op('AND',op('XOR',x,op('RIGHT',args[0] if small else y,imm=c)),self.constant(0xffffffff))
  elif fn=='nCh':out=op('XOR',args[2],op('AND',args[0],op('XOR',args[1],args[2])))
  elif fn=='nMaj':out=op('XOR',op('AND',args[0],args[1]),op('AND',op('XOR',args[0],args[1]),args[2]))
  elif fn=='nne':
   out=op('CMPNE',*args);target='BOOLEAN_FALLTHROUGH_'+str(self.serial);self.serial+=1;self.branch(target,out);self.label(target)
  elif fn=='nbswap':
   lo=op('LEFT',op('AND',args[0],self.constant(255)),imm=24)
   b1=op('LEFT',op('AND',op('RIGHT',args[0],imm=8),self.constant(255)),imm=16)
   b2=op('LEFT',op('AND',op('RIGHT',args[0],imm=16),self.constant(255)),imm=8)
   hi=op('RIGHT',args[0],imm=24);out=op('OR',op('OR',lo,b1),op('OR',b2,hi))
  else:raise ValueError(fn)
  for x in owned:
   if x!=out:self.release(x)
  return out,([out] if out is not None and out[0]=='r' and out[1]>=self.first else [])
 def lines(self,name,lines,ptr,env,done=None):
  assert not self.allocated,self.allocated
  self.env=dict(env);self.ptr=ptr;start=len(self.A['code']);last={}
  for i,line in enumerate(lines):
   decl=re.match(r'uint32_t (\w+)=(.*);',line.strip());rhs=decl[2] if decl else line
   for n in re.findall(r'\bv\d+[aew]\d+\b',rhs):last[n]=i
  for i,line in enumerate(lines):
   line=line.strip()
   if not line:continue
   m=re.fullmatch(r'uint32_t (\w+)=(.*);',line)
   if m:
    n,text=m.groups();v,owned=self.expression(self.parse(text));self.env[n]=v
    if n not in last:self.release(v)
   else:
    m=re.fullmatch(r'if\((.*)\)return (\d+);',line)
    if m:
     expr=self.parse(m[1]);assert expr.func.id=='nne';args=[];owned=[]
     for node in expr.args:v,o=self.expression(node);args.append(v);owned+=o
     self.cmpbranch(*args,'STEP_FAIL_'+m[2])
     for v in owned:self.release(v)
    elif re.fullmatch(r'return \d+;',line):pass
    else:
     assert line.startswith('nstore(') and line.endswith(';'),line
     _,owned=self.expression(self.parse(line[:-1]))
     for v in owned:self.release(v)
   for n in [n for n,j in last.items() if j==i]:self.release(self.env[n])
  for v in list(self.allocated):self.release(('r',v))
  self.sections.append({'name':name,'start_pc':start,'end_pc':len(self.A['code'])})
 def expr(self,text,ptr=None):
  if ptr is not None:self.ptr=ptr
  return self.expression(self.parse(text))
 def finish(self):
  assert not self.allocated
  return {'native_register_first':self.first,'native_temporary_slots':self.high-self.first,'register_count':self.high,'sections':self.sections}

def emit_native(A):
 C=NativeCompiler(A);R=C.reg;K=C.constant;M=A['memory'];src=native_text()
 def body(name,nextname):
  text=src[src.index('static '+('int' if name=='native_step' else 'void')+' '+name+'('):];text=text[:text.index('\nstatic void '+nextname+'(')];return text[text.index('{')+1:text.rfind('}')].strip().splitlines()
 step=body('native_step','native_compress');comp=body('native_compress','digest_messages')
 def ptr(cv,block=0,result=0):
  p={f'ptr_cv_{i}':cv+i for i in range(8)};p.update({f'ptr_block_{i}':block+i for i in range(16)});p.update({f'ptr_result_{i}':result+i for i in range(8)});p.update({f'ptr_pair_{m}_{j}':M['PAIR']+16*m+j for m in range(2) for j in range(16)});p.update({f'ptr_digest_{m}_{j}':M['STEP_DIGEST']+8*m+j for m in range(2) for j in range(8)});return p
 C.label('NATIVE_INITIAL');C.lines('initial_fixed_IV_compression',comp,ptr(M['IV'],M['M0'],M['CV']),{});C.metadata(7);C.emit('HALT')
 C.label('NATIVE_CALLBACK');C.metadata(1)
 C.cmpbranch(R('FOUND'),K(0),'RETURN_DISPATCH')
 C.metadata(2);C.lines('Step3b',step,ptr(M['CV']),{'a0':R('A0'),'a1':R('A1')})
 C.immediate('RESULT',7)
 C.label('STEP_DONE');C.metadata(3);C.cmpbranch(R('RESULT'),K(7),'CALL_RECORD')
 for j in range(16):C.store(M['PAD']+j,K(0x80000000 if j==0 else 1024 if j==15 else 0))
 for m in range(2):
  C.lines(f'terminal_member{m}_block',comp,ptr(M['CV'],M['PAIR']+16*m,M['STATE']),{})
  C.lines(f'terminal_member{m}_padding',comp,ptr(M['STATE'],M['PAD'],M['TERM_DIGEST']+8*m),{})
 for kind,count,base in [('DIFF',8,M['TERM_DIGEST']),('DISTINCT',16,M['PAIR'])]:
  accum=K(0)
  for j in range(count):
   x=C.load(base+j);y=C.load(base+count+j);pred=C.op('CMPNE',x,y);C.release(x);C.release(y)
   target=f'{kind}_BOOL_{j}';C.branch(target,pred);C.label(target)
   z=C.op('OR',accum,pred);C.release(accum);C.release(pred);accum=z
  C.cmpbranch(accum,K(0),'CALL_RECORD',invert=(kind=='DISTINCT'));C.release(accum)
 for m in range(2):
  for j in range(16):x=C.load(M['PAIR']+16*m+j);C.store(M['RECOVERED']+16*m+j,x);C.release(x)
 for m in range(2):
  for j in range(8):x=C.load(M['TERM_DIGEST']+8*m+j);C.store(M['REC_DIGEST']+8*m+j,x);C.release(x)
 for m in range(2):
  for j in range(32):
   x=C.load((M['M0']+j) if j<16 else (M['RECOVERED']+16*m+j-16));C.env={'x':x};encoded,owned=C.expr('nbswap(x)');C.store(M['OUTPUT']+32*m+j,encoded);C.release(x)
   for v in owned:C.release(v)
 C.immediate('FOUND',1);C.metadata(5)
 C.label('CALL_RECORD');C.metadata(6)
 C.label('RETURN_DISPATCH')
 depths={}
 def tree(lo,hi,depth=0):
  if hi-lo==1:
   depths[lo+1]=depth;C.branch(A['continuations'][lo]['target']);return
  mid=(lo+hi)//2;pred=C.op('CMPLTI',R('CONT'),imm=mid+1);target=f'RETURN_{lo}_{mid}'
  C.branch(target,pred);C.release(pred);tree(mid,hi,depth+1);C.label(target);tree(lo,mid,depth+1)
 tree(0,640)
 for code in range(7):C.label('STEP_FAIL_'+str(code));C.immediate('RESULT',code);C.branch('STEP_DONE')
 C.label('FIXTURE_FOUND_CLEAR');C.immediate('FOUND',0);C.emit('HALT')
 C.label('FIXTURE_FOUND_SET');C.immediate('FOUND',1);C.emit('HALT')
 C.label('FIXTURE_POSITIVE_ARGS');C.immediate('A0',A['B'].SA[0][0]);C.immediate('A1',A['B'].SA[0][1]);C.immediate('U',0);C.immediate('F',A['B'].Ffun(A['B'].cvc(A['B'].PCV),A['B'].SA[0][0]));C.emit('HALT')
 C.label('FIXTURE_NEGATIVE_ARGS');C.immediate('A0',(A['B'].SA[0][0]+1)&0xffffffff);C.immediate('A1',A['B'].SA[0][1]);C.emit('HALT')
 C.metadata(8)
 info=C.finish();info.update({'dispatcher_depths':depths,'positive_fixture_id':min(k for k,v in depths.items() if v==max(depths.values())),'dispatcher_max_depth':max(depths.values()),'dispatcher_uniform_depth_mean':sum(depths.values())/640,'logical_calls':0,'logical_returns':0,'indirect_branches':0,'all_branch_targets':'literal immutable bytecode indices'})
 return info


def meter_v4(raw,pool,handlers,labels,cont,info,regs):
 n=len(raw)//8;inserts={}
 def record(pc,w):
  assert pc not in inserts
  inserts[pc]=struct.pack('<4BI',21,regs['BUDGET'],regs['BUDGET'],0,w)
 def depth(j,lo=0,hi=14):
  if hi-lo==1:return 0
  mid=(lo+hi)//2
  return 1+(depth(j,lo,mid) if j<mid else depth(j,mid,hi))
 for pc,(enc,d,a,b,imm) in enumerate(struct.iter_unpack('<4BI',raw)):
  op=enc&63
  if op==17:
   j=imm&255;sp=imm>>16;record(pc+1,28+2*depth(j)+4*sp+9)
   q=pc+1
   while struct.unpack_from('<B',raw,q*8)[0]&63!=13:q+=1
   record(q+1,7)
  elif op==14 and d in (4,5,6):record(pc,{4:23,5:30,6:31}[d])
 for r in cont:record(r['callsite_pc'],4025)
 assert len(inserts)==20480
 mapping=array.array('I',[0])*(n+1);out=bytearray()
 for pc in range(n):
  if pc in inserts:out.extend(inserts[pc])
  mapping[pc]=len(out)//8;out.extend(raw[pc*8:pc*8+8])
 mapping[n]=len(out)//8
 for pc,(enc,d,a,b,imm) in enumerate(struct.iter_unpack('<4BI',raw)):
  if enc&63 in (13,45):struct.pack_into('<I',out,mapping[pc]*8+4,mapping[imm])
 def remap(x,key=''):
  if isinstance(x,dict):return {k:remap(v,k) for k,v in x.items()}
  if isinstance(x,list):return [remap(v,key) for v in x]
  if isinstance(x,int) and isinstance(key,str) and key.endswith('_pc'):return mapping[x]
  return x
 pool.append(1489431040983)
 return bytes(out),pool,remap(handlers),{k:mapping[v] for k,v in labels.items()},remap(cont),remap(info)

def generate_program():
 B=types.SimpleNamespace(SA=SA,SE=SE,PCV=PCV,Ffun=Ffun,cvc=cvc,DH=DH)
 MASK=(1<<256)-1;NB=1<<23;OM=(1<<27)-1
 old_names=['AND','OR','XOR','NOT','SUB','ADD','LEFT','RIGHT','LOAD','CMPNZ','CMPLT','CMPNE','BR','LEGACY','EVENT','BEGIN','LEAF','END_FIELD','EMIT','HALT']
 names=old_names+['ADDI','MEMLOAD','MEMSTORE','CMPLTI','NATIVE_META','VSHIFT']
 opcode={n:i+1 for i,n in enumerate(names)}
 register_names='W0 U W BASE B1 WB Q0 Q4 ADDR TAGA TAGB V RR BAD MM X OFF DELTA FULL COUNT A0 A1 F PRED T0 T1 T2'.split()
 regs={n:i for i,n in enumerate(register_names)}
 for n in ('PHASE','ZERO','CONT','FOUND','RESULT','QUERY_INDEX','QUERY_LIMIT','U_START','LU','BUDGET'):regs[n]=len(register_names);register_names.append(n)
 code=Instructions();labels={};fixups=[];pool=[];cindex={};sites=[];handlers=[];continuations=[]
 def const(x):
  x&=MASK
  if x not in cindex:cindex[x]=len(pool);pool.append(x)
  return cindex[x]
 def emit(op,d=0,a=0,b=0,imm=0):
  code.append([opcode[op],d,a,b,imm]);return len(code)-1
 def label(n):
  assert n not in labels,n
  labels[n]=len(code)
 def calc(op,d,a,b=None,k=None):
  assert (b is None)!=(k is None)
  i=emit(op,regs[d],regs[a],regs[b] if b is not None else const(k))
  if k is not None:code[i][0]|=128
  return i
 def shift(op,d,a,n):return emit(op,regs[d],regs[a],imm=n)
 def load(d,a):return emit('LOAD',regs[d],regs[a])
 def unary(op,d,a):return emit(op,regs[d],regs[a])
 def branch(target,condition='PRED',invert=False,always=False):
  i=emit('BR',int(always),regs[condition],int(invert));fixups.append((i,target));return i
 def nz(a):return unary('CMPNZ','PRED',a)
 def cmp(op,a,b=None,k=None):return calc(op,'PRED',a,b,k)
 def meta(op,imm=0,d=0,a=0,b=0):return emit(op,d,a,b,imm)
 def mask(n):return (1<<n)-1
 label('QUERY_ENTRY')
 emit('ADDI',regs['QUERY_LIMIT'],regs['ZERO'],imm=1)
 emit('ADDI',regs['QUERY_INDEX'],regs['ZERO'],imm=0)
 emit('VSHIFT',regs['QUERY_LIMIT'],regs['QUERY_LIMIT'],regs['LU'])
 label('QUERY_SETUP');meta('LEGACY',d=9,imm=11)
 setup_first=len(code)
 calc('AND','W','W0',k=511);shift('RIGHT','T0','W0',9)
 calc('AND','BASE','T0',k=MASK^7);calc('AND','T0','T0',k=7)
 meta('LEGACY',d=0,imm=1)
 shift('LEFT','T1','W',9);calc('OR','WB','W','T1')
 for n in (18,36,72,144):shift('LEFT','T1','WB',n);calc('OR','WB','WB','T1')
 H0=sum(1<<(9*i+8) for i in range(28));calc('AND','Q0','WB',k=MASK^H0);shift('LEFT','Q4','Q0',4)
 def head(r,h,kind):
  extra=int(kind=='S');rb=(r+extra)%8;cross=rb>=6;par=rb&1;start=0 if cross else 4;lanes=14 if cross else 28
  H=sum(1<<(start+9*i+8) for i in range(lanes));U=H>>8;A=U*250
  active=H if cross else sum(1<<(4+63*g+9*i+8) for g in (rb//2,rb//2+1) for i in range(7))
  rid=r*80+{'L':0,'H':20,'W':40,'S':60}[kind]+h+1;uid=len(handlers)+1;tag=f'X{uid}';after=f'AFTER_{r}_{kind}_{h}'
  first=len(code)
  calc('ADD','ADDR','B1' if extra else 'BASE',k=B.DH[h]+par);calc('AND','ADDR','ADDR',k=NB-1);load('TAGA','ADDR')
  if cross:
   calc('ADD','T1','ADDR',k=8);load('TAGB','T1');shift('RIGHT','T1','TAGA',193);calc('AND','T2','TAGB',k=mask(63)<<4);shift('LEFT','T2','T2',59);calc('OR','V','T1','T2')
  else:
   pass
  source='V' if cross else 'TAGA'
  calc('OR','T1',source,k=H);calc('SUB','RR','T1','Q0' if start==0 else 'Q4')
  calc('AND','T1','RR',k=A);calc('OR','T1','T1',k=H);calc('SUB','BAD','T1',k=U)
  calc('XOR','OFF',source,'RR')
  if kind=='L':calc('XOR','OFF','OFF',k=H)
  calc('OR','T1','BAD','OFF');calc('AND','BAD','T1',k=active)
  if kind in ('W','S'):
   calc('XOR','MM','BAD',k=active)
   if kind=='S':unary('NOT','T1',source);calc('AND','MM','MM','T1')
   else:calc('AND','MM','MM',source)
   nz('MM');branch(after,invert=True)
  else:
   cmp('CMPNE','BAD',k=active);branch(after,invert=True);calc('XOR','MM','BAD',k=active)
  meta('EVENT',imm=rid,d=extra)
  label(f'HANDLER_{rb}_{tag}');meta('BEGIN');calc('SUB','T1','T1',k=0) if False else None
  calc('SUB','T1','MM',k=0) if False else None
  i=calc('SUB','T1','MM',k=0);code[i][0]|=64
  calc('AND','X','MM','T1')
  positions=[(0 if cross else 4+63*(rb//2))+9*j+8 for j in range(14)]
  def tree(lo,hi):
   if hi-lo>1:
    mid=(lo+hi)//2;cmp('CMPLT','X',k=1<<positions[mid]);branch(f'NODE_{rb}_{lo}_{mid}_{tag}');tree(mid,hi);label(f'NODE_{rb}_{lo}_{mid}_{tag}');tree(lo,mid);return
   j=lo;f,i=divmod(j,7);bucket=(rb+2*f)%8;block_extra=8 if cross and f else 0
   pos=192*bucket+27*i;wi,sh=divmod(pos,256);K=block_extra+2-par+wi;split=int(sh+27>256)
   meta('LEAF',imm=(j|(rb<<8)|(split<<16)))
   calc('ADD','T1','ADDR',k=K);load('OFF','T1');shift('RIGHT','OFF','OFF',sh)
   if split:
    calc('ADD','T1','ADDR',k=K+1);load('T1','T1');shift('LEFT','T1','T1',256-sh);calc('OR','OFF','OFF','T1')
   calc('AND','OFF','OFF',k=OM)
   tagpos=9*j if cross else 4+63*(bucket//2)+9*i
   shift('RIGHT','T1','RR',tagpos);calc('AND','DELTA','T1',k=5)
   calc('AND','T1','TAGB' if cross and f else 'TAGA',k=1<<(bucket//2));nz('T1');branch(f'FULL_{rb}_{j}_{tag}')
   cp=192*bucket+189;cwi,csh=divmod(cp,256);CK=block_extra+2-par+cwi
   calc('ADD','T1','ADDR',k=CK);load('T1','T1');shift('RIGHT','T1','T1',csh);calc('AND','COUNT','T1',k=7)
   cmp('CMPLT','COUNT',k=i);code[-1][0]|=64
   branch(f'CLEAR_{rb}_{tag}',invert=True)
   label(f'FULL_{rb}_{j}_{tag}');meta('LEGACY',d=1,imm=5)
   calc('ADD','F','W0',k=(B.DH[h]<<9)&0xffffffff);calc('ADD','F','F',k=1024*f);calc('ADD','F','F','DELTA');calc('AND','F','F',k=0xffffffff)
   meta('LEGACY',d=2,imm=3);branch(f'PF_{rb}_{tag}',always=True)
  tree(0,14)
  label(f'PF_{rb}_{tag}')
  for stage,n in enumerate((7,22,29,30),3):
   meta('LEGACY',d=stage,imm=n-2);nz('T0');branch(f'PF_DONE_{tag}')
  meta('LEGACY',d=7,imm=0);meta('EMIT')
  callpc=len(code);emit('ADDI',regs['CONT'],regs['ZERO'],imm=uid);branch('NATIVE_CALLBACK',always=True);code[-1][0]+=32
  continuations.append({'id':uid,'callsite_pc':callpc,'target':f'CLEAR_{rb}_{tag}','uid':uid})
  label(f'PF_DONE_{tag}');meta('EMIT')
  label(f'CLEAR_{rb}_{tag}');meta('LEGACY',d=8,imm=1);calc('XOR','MM','MM','X');nz('MM');meta('END_FIELD');branch(f'HANDLER_{rb}_{tag}')
  label(after)
  handlers.append({'uid':uid,'rid':rid,'phase':rb,'query_phase':r,'kind':kind,'head':h,'start_pc':first,'after_pc':len(code),'handler_pc':labels[f'HANDLER_{rb}_{tag}']})
 def phase(r):
  cmp('CMPLT','W',k=256);branch(f'PH{r}_L');cmp('CMPLT','W',k=507);branch(f'PH{r}_H');branch(f'PH{r}_W',always=True)
  for kind in ('L','H','W'):
   label(f'PH{r}_{kind}')
   for h in range(20):head(r,h,kind)
   if kind=='W':
    calc('ADD','B1','BASE',k=8 if r==7 else 0);calc('AND','B1','B1',k=NB-1);meta('LEGACY',d=0,imm=1)
    for h in range(20):head(r,h,'S')
   branch('QUERY_DONE',always=True)
 def phases(lo,hi):
  if hi-lo==1:phase(lo);return
  mid=(lo+hi)//2;cmp('CMPLT','T0',k=mid);branch(f'DISPATCH_{lo}_{mid}');phases(mid,hi);label(f'DISPATCH_{lo}_{mid}');phases(lo,mid)
 code[setup_first+3][1]=regs['PHASE']
 original_cmp=cmp
 def cmp(op,a,b=None,k=None):return original_cmp(op,'PHASE' if a=='T0' and op=='CMPLT' and k in (1,2,3,4,5,6,7) else a,b,k)
 phases(0,8);label('QUERY_DONE');label('QUERY_LOOP_ADD')
 emit('ADDI',regs['QUERY_INDEX'],regs['QUERY_INDEX'],imm=1)
 cmp('CMPLT','QUERY_INDEX',b='QUERY_LIMIT');branch('QUERY_SETUP')
 label('QUERY_HALT');meta('HALT')
 scanner_end=len(code)
 memory={'IV':0,'M0':8,'CV':24,'PAIR':32,'STEP_DIGEST':64,'STATE':80,'PAD':88,'TERM_DIGEST':104,'RECOVERED':120,'REC_DIGEST':152,'OUTPUT':168,'U0':232,'ROT':233,'WORDS':234}
 native_info=emit_native(locals())
 for v in continuations:v['target_pc']=labels[v['target']]
 
 for pc,n in fixups:code[pc][4]=labels[n]
 raw,pool,handlers,labels,continuations,native_info=meter_v4(code.raw,pool,handlers,labels,continuations,native_info,regs)
 assert len(raw)==290283*8 and len(pool)==241 and len(register_names)==94
 assert hashlib.sha256(raw).hexdigest()=='979ce9bb2d6505f8614aab65a56e8eff830fdb3d02cc36f5569d6321134bb718'
 assert len(handlers)==640 and len(continuations)==640
 branches=0
 for enc,d,a,b,imm in code:
  op=enc&63;native=op>=33;op=op-32 if native else op
  assert 1<=op<=26
  if op==13:assert 0<=imm<len(code) and d in (0,1) and b in (0,1);branches+=1
  if op<=12:
   assert d<94 and a<(241 if native and enc&64 else 94)
   if op in (1,2,3,5,6,11,12):assert b<(241 if enc&128 else 94)
  if op in (22,23):assert imm<234
 assert branches==41121
 return raw,pool,handlers,labels,continuations,native_info

class Native:
 def __init__(self):self.h=collections.Counter()
 def op(self,k,v):self.h[k]+=1;return v
 def add256(self,a,b):return self.op('ADD',(a+b)&W256)
 def sub256(self,a,b):return self.op('SUB',(a-b)&W256)
 def low(self,a):return self.op('AND',a&M)
 def a(self,a,b):return self.low(self.add256(a,b))
 def s(self,a,b):return self.low(self.sub256(a,b))
 def x(self,a,b):return self.op('XOR',a^b)
 def k(self,a,b):return self.op('AND',a&b)
 def o(self,a,b):return self.op('OR',a|b)
 def l(self,a,n):return self.op('SHIFT',(a<<n)&W256)
 def r(self,a,n):return self.op('SHIFT',a>>n)
 def ld(self,a):return self.op('LOAD',a)
 def st(self,ls,i,v):ls[i]=self.op('STORE',v)
 def ne(self,a,b):self.h['COMPARE']+=1;return self.op('BRANCH',a!=b)
 def sigma(self,x,a,b,c,small=False):
  y=self.o(self.l(x,32),x)
  return self.low(self.x(self.x(self.r(y,a),self.r(y,b)),self.r(x if small else y,c)))
 def S0(self,x):return self.sigma(x,2,13,22)
 def S1(self,x):return self.sigma(x,6,11,25)
 def s0(self,x):return self.sigma(x,7,18,3,True)
 def s1(self,x):return self.sigma(x,17,19,10,True)
 def ch(self,x,y,z):return self.x(z,self.k(x,self.x(y,z)))
 def maj(self,x,y,z):return self.x(self.k(x,y),self.k(self.x(x,y),z))
 def plus(self,*xs):
  v=xs[0]
  for x in xs[1:]:v=self.a(v,x)
  return v
 def minus(self,*xs):
  v=xs[0]
  for x in xs[1:]:v=self.s(v,x)
  return v
 def total(self):return sum(self.h.values())

def transformed(records):
 """Eight original buckets become two tag words and six offset/count words."""
 out={}
 for base in {b&~7 for b in records}:
  words=[0]*8
  for r in range(8):
   v=records.get(base+r,());count=len(v);par=r&1
   words[par]|=int(count==7)<<(r//2)
   for i,(tag,off) in enumerate(v):
    words[par]|=tag<<(4+63*(r//2)+9*i)
    p=192*r+27*i;wi,sh=divmod(p,256)
    words[2+wi]|=(off<<sh)&W256
    if sh+27>256:words[3+wi]|=off>>(256-sh)
   p=192*r+189;wi,sh=divmod(p,256);words[2+wi]|=count<<sh
  for r in range(8):
   p=192*r+189;wi,sh=divmod(p,256);count=words[2+wi]>>sh&7
   rebuilt=[]
   for i in range(count):
    p=192*r+27*i;wi,sh=divmod(p,256);v=words[2+wi]>>sh
    if sh+27>256:v|=words[3+wi]<<(256-sh)
    rebuilt.append((words[r&1]>>(4+63*(r//2)+9*i)&511,v&OMASK))
   assert rebuilt==list(records.get(base+r,()))
  for i,v in enumerate(words):
   if v:out[base+i]=v
 for i in range(8):
  if i in out:out[NBK+i]=out[i]
 return out

def scalar_query(records,cv,W0,u):
 """Direct stored-record lookup, no packed tag test or bytecode dispatch."""
 c=cvc(cv);w=W0&511;out=[]
 for dh in DH:
  bh=((W0>>9)+dh)&(NBK-1)
  for extra in range(1+int(w>=507)):
   for f in range(2):
    b=(bh+extra+2*f)&(NBK-1)
    for tag,off in records.get(b,()):
     if (tag-w)&511 not in OFFS[:4]:continue
     if w>=507 and ((tag<256)!=bool(extra)):continue
     F=(b<<9)|tag;a0=p_a0(off);a1=(u-F+c['K2']+a0)&M
     fl=pf_ref(cv,a0,a1)
     out.append((a0,a1,u,F,sum(x<<j for j,x in enumerate(fl))))
 return collections.Counter(out)

def original_query(records,cv,W0,u):
 old={b:sum(((off<<9)|tag)<<(36*i) for i,(tag,off) in enumerate(v))|(len(v)<<252) for b,v in records.items()}
 w=W0&511;x=w|(w<<11);x|=x<<36;x|=x<<72;x|=x<<144;x&=LM7;C=K512-x;c=cvc(cv);out=[]
 for dh in DH:
  bh=((W0>>9)+dh)&(NBK-1)
  for extra in range(1+int(w>=507)):
   a=old.get((bh+extra)&(NBK-1),0);b=old.get((bh+extra+2)&(NBK-1),0)
   v=(a&TM0)|((b<<11)&TM1);rr=v+C;y=(rr if extra else rr^K512)&M3FA;mm=(((y|G10)-L0)&G10)^G10
   for i in range(7):
    for f,word in enumerate((a,b)):
     if not mm>>(36*i+10+11*f)&1 or i>=word>>252:continue
     e=word>>(36*i);off=e>>9&OMASK;F=((((bh+extra+2*f)&(NBK-1))<<9)|(e&511));a0=p_a0(off);a1=(u-F+c['K2']+a0)&M
     fl=pf_ref(cv,a0,a1);out.append((a0,a1,u,F,sum(x<<j for j,x in enumerate(fl))))
 return collections.Counter(out)


def reset_fixtures():
 cases=0
 for B in (8,16,64,256):
  for pad in (0,3,8):
   n=Native();words=[W256]*(B+pad);i=0
   while i<len(words):
    n.st(words,i,0);address=n.add256(i,1);i=n.add256(i,1)
    n.op('COMPARE',i<B+pad);n.op('BRANCH',i<B+pad)
    assert address==i
   assert not any(words)
   assert n.h=={'STORE':B+pad,'ADD':2*(B+pad),'COMPARE':B+pad,'BRANCH':B+pad}
   cases+=1
 for pad in (0,3,8):
  B=NBK;count=B+pad
  assert 5*count==count+2*count+count+count
 assert 5*(NBK-(1<<20))==36700160
 return dict(reset_walk_cases=cases,reset_full_bucket_words=NBK,reset_full_mirror_words=8,
             reset_full_store=NBK+8,reset_full_add=2*(NBK+8),reset_full_compare=NBK+8,
             reset_full_branch=NBK+8,reset_full_operations=5*(NBK+8),reset_undercount_rejected=36700160)

def semantic_fixtures():
 cases=0
 for start in (0,4):
  H=sum(1<<(start+9*i+8) for i in range(28));U=H>>8;A=U*250
  last=1<<(start+9*27+8);zeros=H^(1<<(start+8))^(1<<(start+17))^last
  for t in range(512):
   tags=[t,t^511]+[0]*25+[t^255]
   T=sum(v<<(start+9*i) for i,v in enumerate(tags))|((1<<start)-1 if t&1 else 0)
   for q in range(512):
    rr=((T|H)-U*(q&255))&W256;bad=(((rr&A)|H)-U)&W256;off=T^rr
    if q<256:off^=H
    got=((bad|off)&H)^H
    want=(int(((t-q)&511) in (0,1,4,5))<<(start+8))
    want|=int((((t^511)-q)&511) in (0,1,4,5))<<(start+17)
    if (-q)&511 in (0,1,4,5):want|=zeros
    if ((t^255)-q)&511 in (0,1,4,5):want|=last
    assert got==want
    cases+=1
 assert min(256+t-q for t in range(256) for q in range(256))==1
 metadata_cases=0;H=sum(1<<(4+9*i+8) for i in range(28));U=H>>8;A=U*250
 for q in (0,1,255,256,506,507,508,511):
  for offset in (0,1,4,5,6,127,255,256,511):
   tags=[(q+offset+i*129)&511 for i in range(28)];base=sum(v<<(4+9*i) for i,v in enumerate(tags))
   want=sum(1<<(4+9*i+8) for i,t in enumerate(tags) if (t-q)&511 in (0,1,4,5))
   for meta in range(16):
    T=base|meta;rr=((T|H)-U*(q&255))&W256;bad=(((rr&A)|H)-U)&W256;off=T^rr
    if q<256:off^=H
    assert (((bad|off)&H)^H)==want
    metadata_cases+=1
 return dict(tag_query_start_cases=cases,metadata_hostile_cases=metadata_cases,
             no_cross_lane_borrow=1,low_header_bits=4)


def boundary_fixtures(program,pool):
 cv=[0]*8;queries=claws=fields=invalids=0;h=[0]*64;seen=set();counts=set();splits=set()
 requests=[]
 for r in range(8):
  for qi,q in enumerate((0,255,256,506,507,511)):requests.append((r,q,(r+qi)%8,(6*r+qi)%15))
  for j in range(14):requests.append((r,507 if j&1 else 255,7,j))
 for case,(r,q,count,marker) in enumerate(requests):
  W0=((NBK-8+r)<<9)|q;u=(0x80000000+case)&M;extra=int(q>=507 and case&1)
  records={};avoid=(q+128)&511
  for dh in DH:
   bh=((W0>>9)+dh)&(NBK-1)
   for e in range(1+int(q>=507)):
    for f in range(2):records[(bh+e+2*f)&(NBK-1)]=[(avoid,(case*37+i)&OMASK) for i in range(7)]
  f,lane=divmod(marker%14,7);target=((W0>>9)+extra+2*f)&(NBK-1);tag=0 if extra else q
  records[target]=[(tag if marker==14 or i==lane else avoid,(case*64+i//2)&OMASK) for i in range(count)]
  if marker==14:records[(target+2)&(NBK-1)]=list(records[target])
  table=transformed(records)
  got,hq,nf,ni=check_query(program,pool,table,records,cv,W0,u,original=True)
  queries+=1;claws+=sum(got.values());fields+=nf;invalids+=ni
  h=[a+b for a,b in zip(h,hq)]
  seen.add(r);counts.add(count)
  for jj in range(14):
   phase=(r+extra)%8;bp=(phase+2*(jj//7))%8;p=192*bp+27*(jj%7)
   splits.add(int(p%256+27>256))
 assert seen==set(range(8)) and counts==set(range(8)) and splits=={0,1}
 assert h[17]>0 and h[18]>0 and h[19]>0
 rec={0:[(255,17)]*7,2:[(255,17)]*7};T=transformed(rec)
 got,hq,nf,ni=check_query(program,pool,T,rec,cv,255,123,original=True)
 assert got and max(got.values())>=7
 return dict(boundary_queries=queries+1,boundary_claws=claws+sum(got.values()),boundary_fields=fields+nf,
             boundary_invalid_markers=invalids+ni,boundary_phases=len(seen),boundary_counts=len(counts),
             boundary_marker_leaves=14,boundary_split_cases=len(splits),duplicate_multiplicity=max(got.values()),
             boundary_split_gathers_executed=h[17]+hq[17],boundary_full_fast_paths=h[18]+hq[18],
             boundary_valid_nonfull_paths=h[19]+hq[19],
             boundary_ram_instructions=sum(h[1:14])+sum(hq[1:14]),
             boundary_inherited_aggregate_units=h[14]+hq[14])


class VM:
 def __init__(self,program,pool,cv=None):
  self.code=program;self.pool=pool;self.R=[None]*94;self.R[28]=self.R[30]=self.R[36]=0
  self.mem=[None]*234;self.cv=cv or [0]*8;self.mem[24:32]=self.cv
  self.h=[0]*64;self.new=0;self.units=0;self.fields=self.invalids=0;self.claws=[];self.us=[]
  self.calls=self.guards=self.suppressed=0;self.outputs=[];self.directions=set();self.steps=[]
 def read(self,i):
  x=self.R[i];assert x is not None,('uninitialized register',i);return x
 def run(self,start,stop=-1,table=None):
  pc=start;table=table or {};flags=0;valid=False;c=cvc(self.cv)
  while pc!=stop:
   enc,d,a,b,imm=struct.unpack_from('<4BI',self.code,pc*8);raw=enc&63;native=raw>=33;op=raw-32 if native else raw
   active=(native or op>=21) and pc!=LABELS['QUERY_LOOP_ADD'];nxt=pc+1;units=1
   if op<=12:
    av=self.pool[a] if native and enc&64 else self.read(a)
    if op in (1,2,3,5,6,11,12):
     bv=self.pool[b] if enc&128 else self.read(b)
     if not native and enc&64:av,bv=bv,av
    if op==1:self.R[d]=av&bv
    elif op==2:self.R[d]=av|bv
    elif op==3:self.R[d]=av^bv
    elif op==4:self.R[d]=av^W256
    elif op==5:self.R[d]=(av-bv)&W256
    elif op==6:self.R[d]=(av+bv)&(W256 if native else M)
    elif op==7:self.R[d]=(av<<imm)&W256
    elif op==8:self.R[d]=av>>imm
    elif op==9:
     assert 0<=av<NBK+8;self.R[d]=table.get(av,0)
    elif op==10:self.R[d]=int(av!=0)
    elif op==11:self.R[d]=int(av<bv)
    elif op==12:self.R[d]=int(av!=bv)
   elif op==13:
    taken=bool(d or (bool(self.read(a))^bool(b)))
    if taken:nxt=imm
    if LABELS['RETURN_DISPATCH']<=pc<LABELS['STEP_FAIL_0'] and not d:self.directions.add((pc,int(taken)))
   elif op==14:
    units=imm;a0,a1=self.R[20:22]
    if d==1:self.R[20]=p_a0(self.read(16));valid=True;self.h[18]+=self.R[19]==7;self.h[19]+=self.R[19]<7
    elif d==2:self.R[21]=(self.read(1)-self.read(22)+c['K2']+a0)&M
    elif d==3:flags=0;E5=(a1+C5)&M;self.R[24]=int((E5&C1MASK)!=C1V)
    elif d==4:
     flags=1;w9=(CW9-a1)&M;self.R[24]=int((s0((w9+D9)&M)-s0(w9))&M!=T9)
    elif d==5:
     flags=3;E4=(a0+CE4-(MA|(a1&MB)))&M;w8=(KW8-E4-(CA^(CB&E5)))&M
     self.R[24]=int((s0((w8+D8)&M)-s0(w8))&M!=T8)
    elif d==6:
     flags=7;w7=(c['KK7']+MAJ(SA[0][2],a1,a0)-CH(SE[0][6],E5,E4))&M
     self.R[24]=int((s0((w7+D7)&M)-s0(w7))&M!=T7)
    elif d==7:flags=15
    elif d==9:
     u=(self.read(34)+self.read(32))&M;self.R[1]=u;self.R[0]=(HEADS[0]-s0(u)+u)&M;self.us.append(u)
    else:assert d in (0,8)
   elif op==15:units=0;self.h[15]+=1
   elif op==16:units=0;self.fields+=1;valid=False;flags=0;self.R[20:23]=[0]*3
   elif op==17:units=0;self.R[19]=7;self.h[17]+=bool(imm>>16)
   elif op==18:units=0;self.invalids+=not valid
   elif op==19:units=0;self.claws.append((self.read(20),self.read(21),self.read(1),self.read(22),flags))
   elif op==20:return pc
   elif op==21:self.R[d]=(self.read(a)+imm)&W256
   elif op==22:
    v=self.mem[imm];assert v is not None,('uninitialized memory',imm,pc);self.R[d]=v
   elif op==23:self.mem[imm]=self.pool[a] if enc&64 else self.read(a)
   elif op==24:self.R[d]=int(self.read(a)<imm)
   elif op==25:
    units=0
    if d==1:self.guards+=1;self.suppressed+=bool(self.read(30))
    elif d==2:self.calls+=1;self.step_start=self.new
    elif d==3:self.steps.append(self.new-self.step_start)
    elif d==5:
     output=b''.join(x.to_bytes(4,'little') for x in self.mem[168:232]);assert not self.outputs
     self.outputs.append(output)
    elif d==7:self.cv=list(self.mem[24:32]);c=cvc(self.cv)
   elif op==26:self.R[d]=(self.read(a)<<self.read(b))&W256
   else:raise AssertionError((pc,op))
   if units:
    self.h[op]+=units;self.units+=units;self.new+=units*active
   pc=nxt
  return pc

def vm_query(program,pool,table,cv,W0,u,callback=None):
 v=VM(program,pool,cv);v.R[0]=W0;v.R[1]=u
 v.run(4,LABELS['QUERY_DONE'],table)
 return collections.Counter(v.claws),v.h,v.fields,v.invalids

def check_query(program,pool,table,records,cv,W0,u,real=False,callback=None,original=False):
 got,h,nf,ni=vm_query(program,pool,table,cv,W0,u)
 assert got==scalar_query(records,cv,W0,u)
 if original:assert got==original_query(records,cv,W0,u)
 for a0,a1,uq,F,flags in got:
  wx,wy=pair_words(cv,a0,a1);assert in_P(a0) and uq==u
  assert flags==sum(x<<i for i,x in enumerate(pf_ref(cv,a0,a1)))
  if real:assert wx[1]==u and trace(cv,wx,17)[1][16] in S160
 return got,h,nf,ni

def callback_fixtures(program,pool,cont,info):
 v=VM(program,pool,PCV);v.mem[8:24]=[0]*16
 v.run(LABELS['FIXTURE_FOUND_CLEAR']);v.run(LABELS['FIXTURE_POSITIVE_ARGS'])
 site=info['positive_fixture_id']-1;before=v.new
 assert v.run(cont[site]['callsite_pc'],cont[site]['target_pc'])==cont[site]['target_pc']
 assert v.new-before==13245 and v.steps==[3997] and v.calls==1 and v.R[30]==1
 assert v.mem[32:64]==PMX+PMY and v.mem[64:72]==v.mem[72:80]==compress(PCV,PMX)
 pad=[0x80000000]+[0]*14+[1024];digest=compress(compress(PCV,PMX),pad)
 assert v.mem[104:112]==v.mem[112:120]==digest
 expected=struct.pack('>32I',*([0]*16+PMX))+struct.pack('>32I',*([0]*16+PMY))
 assert v.outputs==[expected]
 costs=set()
 for site in cont:
  before=v.new;calls=v.calls
  assert v.run(site['callsite_pc'],site['target_pc'])==site['target_pc']
  costs.add(v.new-before);assert v.calls==calls and v.outputs==[expected]
 assert costs=={23,25} and len(v.directions)==1278
 for _ in range(2):
  before=v.new;v.run(cont[0]['callsite_pc'],cont[0]['target_pc']);assert v.new-before in (23,25)
 assert v.calls==1 and len(v.outputs)==1 and v.suppressed==642
 v.run(LABELS['FIXTURE_FOUND_CLEAR']);v.run(LABELS['FIXTURE_NEGATIVE_ARGS']);before=v.new
 v.run(cont[0]['callsite_pc'],cont[0]['target_pc'])
 assert v.R[31]==0 and v.steps[-1]==1066 and v.calls==2 and len(v.outputs)==1
 pair=v.mem[32:48],v.mem[48:64];assert not accepted(trace(PCV,pair[0]),trace(PCV,pair[1]))
 assert pf_ref(PCV,(SA[0][0]+1)&M,SA[0][1])==(1,1,0,0)
 fixed=compress(IV,[0]*16)
 assert compress(compress(fixed,PMX),pad)!=compress(compress(fixed,PMY),pad)
 v.R[30]=1;v.R[34]=M-2;v.R[35]=3;v.claws=[];calls=v.calls;outputs=list(v.outputs)
 assert v.run(0,table={})==LABELS['QUERY_HALT'] and v.R[32]==8 and len(v.us)==8
 assert v.us==[(M-2+i)&M for i in range(8)] and v.calls==calls and v.outputs==outputs
 v.R[32]=(1<<32)-1;v.R[33]=1<<32
 assert v.run(LABELS['QUERY_LOOP_ADD'])==LABELS['QUERY_HALT'] and v.R[32]==1<<32
 return dict(callsites_executed=640,dispatcher_directions=1278,suppressed_callbacks=642,
             suppressed_cost_min=min(costs),suppressed_cost_max=max(costs),positive_step_ops=3997,
             negative_step_ops=1066,positive_callback_ops=13245,terminal_suffix_ops=9221,
             found_cv_queries_completed=8,query_lu32_tail_reaches=1<<32,fixed_iv_fixture_not_collision=1)

def arithmetic_fixtures(program,pool):
 v=VM(program,pool);vectors=(0,1,M,M+1,1<<64,(1<<128)-1,1<<255,W256);cases=0
 for wanted in (37,38):
  for pc,(enc,d,a,b,imm) in enumerate(struct.iter_unpack('<4BI',program)):
   if enc!=wanted:continue
   nxt,nd,na,nb,_=struct.unpack_from('<4BI',program,(pc+1)*8)
   if nxt&63!=33 or na!=d or not nxt&128 or pool[nb]!=M:continue
   assert a!=b and d not in (a,b)
   for x in vectors:
    for y in vectors:
     v.R[a]=x;v.R[b]=y;before=v.units;v.run(pc,pc+2)
     expect=(x-y if wanted==37 else x+y)&W256
     assert v.R[d]==expect and v.R[nd]==expect&M and v.units-before==2
     cases+=1
   break
  else:raise AssertionError('missing ADD/SUB narrowing site')
 return dict(actual_native_arithmetic_pairs=cases,actual_native_arithmetic_ops=2*cases)

def mixed_window_fixtures(program,pool):
 cv=[0]*8;states=collections.Counter();queries=claws=0
 for phase in range(8):
  for q in (0,255,506,511):
   W0=((NBK-8+phase)<<9)|q;u=0x72930000+queries
   for first,second in ((1,0),(0,1),(1,1),(0,0)):
    records={}
    for dh in DH:
     base=((W0>>9)+dh)&(NBK-1)
     for extra in range(1+int(q>=507)):
      for f in range(2):
       bucket=(base+extra+2*f)&(NBK-1)
       records[bucket]=[((q+32+19*i)&511,(queries*127+i)&OMASK) for i in range(7)]
    b0=W0>>9;b1=(b0+2)&(NBK-1)
    records[b0]=[((q+31+31*i)&511,(queries*97+i)&OMASK) for i in range(7)]
    records[b1]=[((q+81+17*i)&511,(queries*131+i+30000)&OMASK) for i in range(7)]
    if first:records[b0][2]=(q,records[b0][2][1])
    if second:records[b1][5]=(q,records[b1][5][1])
    assert [t for t,o in records[b0]]!=[t for t,o in records[b1]]
    table=transformed(records)
    got,h,nf,ni=check_query(program,pool,table,records,cv,W0,u,original=True)
    union=scalar_query({b0:records[b0]},cv,W0,u)+scalar_query({b1:records[b1]},cv,W0,u)
    assert got==union and sum(got.values())==first+second
    states[(first,second)]+=1;queries+=1;claws+=sum(got.values())
 assert states=={(1,0):32,(0,1):32,(1,1):32,(0,0):32}
 return dict(mixed_window_union_queries=queries,mixed_window_claws=claws,
             mixed_window_first_only=states[1,0],mixed_window_second_only=states[0,1],
             mixed_window_both=states[1,1],mixed_window_neither=states[0,0],
             mixed_window_unrelated_patterns=queries)

def build_records(cv,rotation,nc):
 c=cvc(cv);old=build_table(c,nc,R=rotation);records={};a,b,cc,d,e,f,g,hh=cv
 k0=(-S0(a)-MAJ(a,b,cc)-hh-S1(e)-CH(e,f,g)-K[0])&M
 for n in range(nc):
  k=(n+rotation)&OMASK;o=(k>>2)|((k&3)<<25);a0=p_a0(o);E0=(a0+d-S0(a)-MAJ(a,b,cc))&M
  F=(a0+CC2+k0-g-K[1]-S0(a0)-((a&b)|(a0&(a|b)))-S1(E0)-(f^(E0&(e^f))))&M
  bucket=records.setdefault(F>>9,[])
  if len(bucket)<7:bucket.append((F&511,o))
 actual=[((b<<9)|tag,o) for b,vs in records.items() for tag,o in vs]
 assert sorted(actual)==sorted(entries(old))
 return records,actual

def seeded_experiment(program,pool,rng):
 m0,cv=first_block(rng);rotation=rng.u32()&OMASK;u0=rng.u32();v=VM(program,pool)
 v.mem[:8]=IV;v.mem[8:24]=m0;before=v.new
 assert v.run(LABELS['NATIVE_INITIAL'])==LABELS['NATIVE_CALLBACK']-1 and v.new-before==2022 and v.cv==cv
 records,actual=build_records(cv,rotation,1<<16);table=transformed(records);sorted_F=sorted(F for F,o in actual)
 v.R[34]=u0;v.R[35]=10
 assert v.run(0,table=table)==LABELS['QUERY_HALT'] and len(v.us)==1024
 got=collections.Counter(v.claws);want=collections.Counter();swar=collections.Counter()
 for u in v.us:
  P=(s0(u)-u)&M;W0=(HEADS[0]-P)&M;query=scalar_query(records,cv,W0,u);want.update(query)
  nref=sum(bisect.bisect_right(sorted_F,(t-P)&M)-bisect.bisect_left(sorted_F,(t-P)&M) for t in S160)
  assert nref==sum(query.values())
  needed={((W0>>9)+dh+extra+2*f)&(NBK-1) for dh in DH for extra in range(1+int((W0&511)>=507)) for f in range(2)}
  local={b:records[b] for b in needed if b in records};swar.update(original_query(local,cv,W0,u))
 assert got==want==swar
 for a0,a1,u,F,flags in got:
  wx,wy=pair_words(cv,a0,a1);assert in_P(a0) and wx[1]==u and trace(cv,wx,17)[1][16] in S160
  assert flags==sum(x<<j for j,x in enumerate(pf_ref(cv,a0,a1)))
 transcript=hashlib.sha256(b''.join(struct.pack('<6I',*c,n) for c,n in sorted(got.items()))).hexdigest()
 return dict(seed_candidates=1<<16,seed_queries=1024,stored_lanes=len(actual),claws=sum(got.values()),
             scalar_claws=sum(want.values()),swar_claws=sum(swar.values()),fields=v.fields,invalids=v.invalids,
             inherited_aggregate_units=v.h[14],executed_units=v.units,native_units=v.new,
             claw_hash_int=int(transcript,16),ordinary_outputs=len(v.outputs),inband_budget=v.read(36)),v.outputs


def controller_fixtures(program,pool):
 cap=23369453903347697850258080090;m=Native();fixed=1489431040983
 def phase(v,pc,table=None):
  m.op('BRANCH',pc);end=v.run(pc,table=table)
  assert end==(LABELS['NATIVE_CALLBACK']-1 if pc==LABELS['NATIVE_INITIAL'] else LABELS['QUERY_HALT'])
  return m.op('BRANCH',1000003 if pc==LABELS['NATIVE_INITIAL'] else 1000004)
 v=VM(program,pool);v.mem[:8]=IV;coin=Shake('v4-controller-fixed-fixture');coins=completed=0
 def draw():
  nonlocal coins
  coins+=1;return m.op('RAND',coin.word())
 def run(limit,stop=0,cap_after=0):
  nonlocal completed,coins
  workcap=cap;pc=1000000;checks=[];boundary=m.total()+v.units;startB=v.read(36);commits=[]
  def commit(future):
   nonlocal boundary
   before=v.read(36);v.R[36]=m.add256(before,fixed);assert v.read(36)<1<<128
   commits.append(v.read(36))
   if future:m.op('BRANCH',1000000)
   boundary=m.total()+v.units
  def finish(kind):
   value=v.read(36);v.R[36]=m.add256(value,0);m.op('BRANCH',1000006)
   assert v.read(36)==value
   return completed,coins,checks,kind,m.total()+v.units-boundary,commits
  while True:
   if pc==1000000:
    m.op('COMPARE',completed<limit);take=m.op('BRANCH',completed<limit)
    if not take:return finish('bound')
    pc=1000001
   elif pc==1000001:
    value=v.read(36);m.op('COMPARE',value>workcap);reject=m.op('BRANCH',value>workcap);checks.append((value,reject))
    if reject:return finish('cap')
    pc=1000002
   elif pc==1000002:
    coin_start=m.total();expected=[]
    for half in range(2):
     word=draw();expected.extend(struct.unpack('<8I',word.to_bytes(32,'little')))
     for j in range(8):
      field=m.r(word,32*j) if j else word
      if j<7:field=m.k(field,M)
      m.st(v.mem,8+8*half+j,field)
    u=m.k(draw(),M);m.st(v.mem,232,u);v.R[34]=u
    rotation=m.k(draw(),OMASK);m.st(v.mem,233,rotation)
    assert m.total()-coin_start==52 and v.mem[8:24]==expected
    before=v.new;assert phase(v,LABELS['NATIVE_INITIAL'])==1000003 and v.new-before==2022
    assert v.cv==compress(IV,expected);pc=1000003
   elif pc==1000003:
    words=[W256]*24
    for j in range(24):m.st(words,j,0);m.add256(j,1);m.add256(j,1);m.op('COMPARE',j<23);m.op('BRANCH',j<23)
    records,_=build_records(v.cv,rotation,256);v.R[35]=2;query_start=len(v.us);oldB=v.read(36)
    assert phase(v,0,transformed(records))==1000004 and v.R[32]==4 and len(v.us)-query_start==4
    assert v.read(36)>=oldB;pc=1000004
   elif pc==1000004:
    completed=m.add256(completed,1)
    if stop and completed==stop:v.run(LABELS['FIXTURE_FOUND_SET'])
    m.op('COMPARE',v.R[30]!=0);success=m.op('BRANCH',v.R[30]!=0);commit(not success)
    if cap_after and completed==cap_after:workcap=v.read(36)
    if success:return completed,coins,checks,'success',0,commits
    pc=1000000
   else:raise AssertionError(pc)
 a=run(3);assert a[:2]==(3,12) and a[3]=='bound' and a[4]==4 and a[5][-1]>=3*fixed
 v=VM(program,pool);v.mem[:8]=IV;completed=coins=0
 b=run(3,stop=2);assert b[:2]==(2,8) and b[3]=='success'
 v=VM(program,pool);v.mem[:8]=IV;completed=coins=0
 c=run(3,cap_after=1);assert c[3]=='cap' and completed==2 and coins==8 and c[4]==6
 assert len(c[2])==3 and not c[2][1][1] and c[2][2][1]
 for value,want in ((cap,False),(cap+1,True)):
  m.op('COMPARE',value>cap);assert m.op('BRANCH',value>cap)==want
 v.R[36]=m.add256(cap,1);d=run(3);assert d[3]=='cap' and coins==8 and d[4]==6
 assert m.add256((1<<64)-1,1)==1<<64 and m.add256((1<<128)-1,1)==1<<128
 assert 8321635287+2335626*(1<<32)==10031445607322583
 return dict(controller_completed_cvs=3,controller_coin_words=12,controller_synthetic_stop_cv=2,
             controller_stop_coins=8,controller_equal_accept=1,controller_cap_reject_before_draw=1,
             controller_inband_budget=1,controller_exact_cap=cap,controller_fixed_charge=fixed,
             query_halt_pc=LABELS['QUERY_HALT'],query_halt_target=1000004,
             initial_halt_pc=LABELS['NATIVE_CALLBACK']-1,initial_halt_target=1000003,
             controller_coin_preparation_ops=52,controller_bound_stop_ops=4,controller_cap_stop_ops=6)


NATIVE_SOURCE_B85='c-rlKdw1KmvhV-?6spgvj~LSlL4YI}naPrEIq|I@*|ME<pKNa}N}^&VvZU%^Cv|*2`<)r^O-e~xS32k3x{XNUF&GR6gTW6V_#fS%*B=Iz)~nOY*7@0GbHB0iAN^rxFz*JH-RZ2`AI_d$zet5a!0gL7m}WyU<){!e=(qD>lm75SHY}J-hPkZsVIOj5!+M?JY>=b&W%_J7^Jm4-NiZGFC!HW0Gwa{vLj378m{9%=tP}{N0xZruv&wyC4mGt!YgYOEUR>2G50!Vdjn+97*YC7czUs99dob!%-)Wx5O?~rjH0f??wT)mnzp30GAL!>7di?+{mwS5s^gusr>c7Ij)3Xcx{I$M+@<!il>PIIh`f=k`egB_&6BC`Dy*YoVZA_`4N@p~j&MKX2e^Ple8V~)OVEP_YTzU7K$7l6}O?~tH;;h+#E0ly!mwR}BiuY$t`1zH7p-hZ?eRPP|{j-xdb;`5{W$wR*8(^bxa8$p*z)J|KpT24wv=n0ygsh#NY$lAw(ix3Ij`ZL*7|y18uOAG$Q@u0r@1}Zxc<T@P_&6HQCZj<MlB*Q08~?LDoA|?NZ#22dKlO*+<<aQ{lyFl2wOHtMJm}9_AN<*MFq!JZ(Xclk3|c*ZFlhUoPZ%<}@dvHzz=xutMg4Ag56U*0Ofv+z2?UAvR==xH0=m3DjMKcU{8yuSR^(wen)!q3?Wo_??&H8)&!|BSs_<Ot!+n1jWmD^KZ)>;P9?GhJRf96-lVRny_D~=?4DMoq*1|}n<#%TN+n@!}F(X)VW$07*c+$V=(_P1(1s_I}FV*>Q+W#;Ny3jy+LSD;e?_3k7*(CS<UNtFCyAOF9jjy)7VQq1VKn3VO1cPZ%No9CQ1UZF98B`NtY4@QhpbOpK-|7bb_wbO;((ccas*JV!cOc^XdrWlu^z-}iGh19mnzCPI+U{<3{Ie~z5*fd%O#Hi+KkQcDReT*NYxmif64XpSknLY>d2PBzbo?}(J3k=-62xB1;u51me7&t@GL15szz#s3#SDC1%E0FgtzW-I?B7d?4UrfTLd&$2koVvI5<=4qS7`Ns7>K<Vw|IL5{qL^OM^q6>FPeq?ZmaZq$D8d&HBfvgHg;yUkYeX+RR!(NK<ZIbq`C9EUDL9&4R>%*;IQLQCSO7ZW4&9%r5|!h7vj>-a5>v1ay3O1c$_Tf@oqr;#pMo_AYX@EhKdi}bNIr8%4ji-ILB|^5W0ju^@h+3Qc~u%{tK+c&JK0&xM~^%{|4PKCDonZu6B2)Sju#3E1mE+Z4#<xm~Mw%y?9Zz#m*G!Q(mFT<5#G>Re(l+`?p<@t;_arz+qGuc-m%=B2x<tgZeJ11qu*5b?{rFJYlMv;HGmku5S7IR$Gsq0q_QlZ1(o>_qdPYun)C|yS--0Y>@gIS6}hM)WuX6ex?0XAUK$1G&xVSwBgaLQ`LV8yH_Ocu;*lLM4<}7(h|d5KZTOYT0a`WfaQ3&_4W96DLH?)ogE}qZhr}-uv13_wo3`zEF+LH=l)hZt<Zy!kK@OaizL^Wavi5LUA!M(CAny%oz6y+AfFSYd8>K^*<H-$m3ajpf?2j7jWb;;)g#8Lv)~w5OF1Q~g`=*pJ$wN}<ZaXgQu-f_np@RsW>6h!J50;hh?sh^fGa&c%72T&8?RVg?RLw%srfrEs5e)`o2~z@-hg$|w6E1$yr$}tlydDs&`!F5-*W|AV*!dJR6n8)w_E@HJCcsf8d`*c_Dm*;_S|L~BI?VKf2cUDa&u>>X(c*%ZltKhS%LPgZfgIgE92pfX_iu83n|zU1r|}T$|y`1^Wa1jr1o#D4=>HXm;)9Qa1{Y&lu_8fPAGg%dd8RJ_V+}rpSQjMt?GY&*0z2xBX;6{{9$UJfz-dNUlhUYtm|Fnmy`DvsK@>NeXKpk=XS5#3wk}L7v5-kDl!}8WFxat?QCQ=s@u~Z9`sDPz3iWn$!%o+oMn;5^2mI-!Y~bH7}5xDGP$!+(s;yjdEoX$&v&}vO(r+XL^<6@EH_mfy2<5UB8)#*ZjN#;cUH_IM>@-MCbCeSe7QL>XUolrnP($2QGuI@%trM@vA#LQ%2p|-Sbstok16NOpZSCB`$O8Xq)Nt*weND$+4>sauU9#$>`&BJK5jqyc5d;98sSfs%l>%d|Al(>m+G@zYkk>T$~FJ0`pU-;<&Ta>k45?~(`WIx<+AnG*IY}v;(u`aE{PPYF4tT`edYgzal!bj#{IHLvEKU1b(G8g$F{Gz>T=l{>MPbFXSv4qHP@?GVlCy$KVM(D>Tyu4e*9%?8TZX~`Wtesehynpx#nM0U%7h!*<8y!MXbcXDwi``@4U=hOS$5&uJ1#%b?bD`WAoizljk>L#p?)XCtj73INA==-|W@T8=i^J)}kEy`=)1ncKjYU17^(^CbK+TMPR<!HQS3*y>lU%gg>Y4%f-nW0+V&x+zL9~g~?9pkP164^F?QIsy$5A>$$yNx3@6WFYhEIGr4Klfxn~zSfn(WiOsq=6&A@@ryF$J_Tp6Rq<;PjqzuBQT$1uFB=f(O?7;Do5ovKMtZ1*@A(OW_mHR!6U0{g@Z})o3XkAc=fg~HdI2D#?2)>-wc>{|K0uF5;+$G6uNamWBZwRrt3C`;r3-zVTd)>~GWY`Ccu48n4u|$XV&rZ)T-g9~7-GiMqrEm6JIoF~4FzyK9GQ4kF9RtMQ!~4K(Tiv#A;XQXPyJK2yytmvQW2{H%U6c2u=?lE~+pJ>+T}t1ThU5E+J~Jh^+6JXJ1!vM~2Smp*I!?F4i3hVCSY3zcNTVCHS&!1V?QX}geFyJ5%x(9WN)rgTZMz+!8T8tLaHNg*JxJ8;*s3U_<FihO?z@3&c5JGa@EswA?-L81w&6ntV!;M^$S#Guk_Q&EOsbaTtYh0<5|3eU)9FyP+C9s4dL6}@4cgf5QB}H@@3>4*xZUw>ZV{JEn6ByC6l^+e2ilb+1%|6_GEO8#7ntn!h#iY_5CkKVwq^JZw}fKT_6@(?o-Z_`uN(D)^Y^Bq8oF(mT`(M!waxr?d~ce`J&(gX(lC3;z28mUC*jOY!p&5AGnL*<rRPcdHcQe2KdJB}J@A%<^Hh4CO3&l;J*Xq`4<h-GaPRf$*+uKMfs4(?Rc41pf7qY3NMinQHVwC$K5T4+qtxDhtA2XmF&%Esnx2W*U*U%14G{GN-ke|Vc^2N(4-PyVZ;l&>7oLN6&7)VZFFZ+sXY~Wm#k>8JH>dyQF(bS`zVH}}!W$l=V)mLI<BAq;5cU`q)p*-Dh168qUgOo#smH<s>xUkr5*w!nt;3_nF|bX=HcpNp2bKG}4n>(p$m)@2QmH466JpIY!zbGA?3p}f4^mR;r}c}Yw+%>gQTI&Z;VtcV_Dnk-*qg0)hG*!_)+LAy9zbZ#77gAUZy1OSLQ!DN);|mo7hD9$s);N$K~l}uMg3JB1VuM{D5hrXElQ}_YBo_iNbdlp(`=obpkSJ<Ur{E_*4g193Z&UOXdDBN49Ol|9v`D9nyvk_%Tp2slx3hC;L1=4kO*tvY`tkV4zS`-w1IVoE5n+?)r3l7ir3_aAYt6I?3s!%&^3|nArx`oaU|VroL_>tIg<a!Wuy7e*3s!f<5%3q9t9j9VcT#l@3M7%QE$Qn7J7W?aV&K2^59hi!m!}ew}!_Zx?vudbYptlr5o-EgKmT;7~NQ&FzLqj1g9Iv6M}A}CoH;gJ)tNw!xJHCXdgwJnVwL@8TTwjoe9rU<eBAJiaxVFOBKKz&r&5Y=~=1>=6aSY!!$fgm0>c^3i&rZOO;`A&sJra!n0KwrsdhH4Ab^(Rfg$!wkpGvo~_C-UC&l!aL^}J24|kF%HXDFheG0>qsri*aH<S$d5$WB+n%G!;Ew00GPv{{RR(uGN0lKA&rxLv<~gbiVS0`#LvT-qEg?Lq$`F<(RT;weq$)!=o>XNB=}A?Fa6PHYunbSCGA!mvRfc7HQk7wG&sAku!gIsswmesrVcDL`Q>O3D+4&LmTDUYSe4bb~)g4UNFp;Uot1!S7IynbXykPmU<z0nxqXUuOxswI1b31qb!Wm3%=T3GrLoTxSCnCRr1URdz@49wKJ>ufvpFv#gwUo=&w1UTa?KR1nt-f5R*b7%zU%4iG_4iK0|JQaJt`WKXd!^<7o0S%S<$C4x)@h%uwUjGX-+xQJ(Y4x*m8{_L|7mve|FM<B=+9k~oXr)N`}a!e-z%m6OIJ!4)t5=5-COy*j2p}e)>Yr$TI$<dSAE%9+Ly1XeR&`aw(|NqU1d1dQeR=LqrTEuTYcBkzH)8tE7#G!%ve|Zx@+mb=GywNyO#cIuC4#NYw5q{+WN1%mj27v)PKQ|m8)-G5b>J&FVweVtfRhiZSC7xOZ&=owJ$T)(Z1%|`Y&5c|K)4zzici2m#?k=vbFSIzNY?b;R?gb>+3_IE1m!TeG<vvCy_)D_1`CRtbd*T?~^(He7S$0%<=ch9Dkq8@gwUv>sn7)*Sf~K))&@=^REkUUl;DZF8q02IPkjg*mdEe>%u43g%hp|uUi*xwl4f?T{zOZ@SJtwD*r1^Ap7f1;(VOQzfWxX`^2WdPi$Hq`S(eFf1l)M{I5C5?|;Gx&BkAH5@&R>$IACJgr|tCy4>i*l2w-*osP2deVgG)EUPXzI`w7M<whsWtbBbiJk4g+<whsxth(Ijl%7?W8=VNWa(xa@A6mJc3{N^*{rbK-RcYn@H$1^<)#XN~MXh{X2v4S3dAZ>!SSz3JhevL$-fpPly;fdsc$C=6*R8^1%T{hD!z0pGZYRUz*j8?@!lU0-?r((0%&pvi4v(~3dAZ^7c`F|m!lU|D?$?FK0<PRXhi4G3+@B23J6ySa4$oFxdAZ>^jw>G*!ZRaRJ}!jkQ?9z)=q$|Dk4Ng<&6W4x@L<=Kmm8ityZZKZz_GJek0aTJ>x<Q&N8#Fr>GwJ-ANPGI)DP^Hw{KUNFgII$`!bk@%8u-;-oLVg9&fL_|4N&;CF3i%lV*<x!nXP9@hcl<D!rADzn0Arvs<~G+d{T&>6)v@W7V<cE5|p&Q`J|G$C{QA_-ojw>f3gktz55!v;*dLS6<()=?8wt^;bXd?%2|FR&Spr>oLn&{rorR$e<%uf6iyO-Ik_YeSO#F=h&>{I&2O8Mz6>H)$4Nr{)Wp}zuzoifiPC@Px5v78!!%br7PAjKk|b$_#4KW#{HgQyUbp_J`3K)aewvmeQEcY+gbg&m$unm$GG2Nfo%p(u=;V|>M>{a`(!#c41?<$_kF`zy&o$~=F8RhUun=6xK=-35Nj#-5nciP6Z`s@zoz}|!J6vZSyO%2^gRN$uJ;$#bPh9PYbw`SQ@Lw8mzb?fpV##L6lSlf+;#P%?wZOq*JQ6cYw<VM;9n^xdM*BjSjTt-a<-YdmiHys;!j4ihLxAg)F)uqQQx(c%cNMxISJ;P<ZLoyZS9M~Uj2UWb<WFH{2dc!`5hOUn0KAO^h@T^Cl*f{7ma4?@aWgZf%+_B#T3Ro`iAWJe*N?m;v1(2p6PHyI(qmW)puvjgLBX1B2BAx^tJ+-ljjqoBGb?NZ-IO|;7$FgS>a|n==`Gbrgd=issX&%A{$e`XjG(;C2&xYnKGb0CsBT8WC%1H`)6+(&Bj3m#)Di$oW;s;b9Q<0<`P2fOc|F(#msWuJOjybo(>`rL12o7H}Q99k4}#+j_Su1CDpPN`}O1Fz54zyki=q)Ws*R9U0gOB>XWUl{o_WxS;3ECI>wS@=Zy=M$Sh41e{8efe08o8iqeFqjaT(tLN}98eIT}RdeQu6#VCn6K0AAZU(8jN2bnGU2>kIee)#jfE$|D_!m@NJZJlxE=*$sPH<{z=rp*kU8-nRvIHt~BgX@BGp$o^hbc?yRZrP@z+lD1|TS!;8UDMDVZZX|)q^V2jY`V0C&|Sl^bk{QA$K{sJ3~uAE<H9d9P5iZi3D6yhzZSz^SHLgl4*p8W%7lq|g^hVF1M^xI=CxeRYjezNOU&z-nAfo#sE=fZgkOuh@asB;&hV&i_?6t$O~bS~{MxR7N<+!;Ygsn@y3iv{Q!o&QDFsM_o6>+^hcO+31>_Z$19>g*g5XyGZ>A+}$ZMOxn`t{Hq;!}7Iu50DTo>p_fu%?ZQZii=I5dGN4uXan!><K(;f5<g>P#38{7Me7AS8%2ZKxyXptSI7afszE@XrMY>2o1XTjwAW2)Ar0b#5~T;UHRQNSkOnf<aR{Qa~;VdI-M`$d<c|LtfXiAuq5gb@bg`_?5PyLmrpGuVb1zczhP<0aO(f0hqSnR|p$^r31eZguf0@6Be`a*8)WmHV7Jig@wPUY><TEuY-9d!@N)w{DPX{ufV*nL?y#@H28HOFZ5T5zc%ExOaoNaG6m?W1q>Rx1=`8r*8z34gb7l$gbfM{^+%1h1X8m==%Bb9loo0Wa<iaXkQbC1@`B?5d7*J2uXI6mEf+P=awYHvmEfrF(6l;;7TVngVL&+a1?U1`-wpUhy|RI2hy|fTEQk*~hy{|gh3i5rFbA<v48%ePhy{`m>wt}fUzDv4ju*sA0d)j{f$rHZ2d-?_;Zk=XlEbeBc^zgzI4By1gLvTHM4ApLAKXJGiJcO|xr^aKV7QPNZlV4=q%96q3GQtR!)??n2a1x|moZ#o-5pSH=-n>%Q|P^h3%@Str!+Wdoire+E}<KPL1EAhzyuheEfU%YV!@z6Ea#yA5)=_)L8Ty8ST4j`FgC-lfSxO%A3-ejBT15xP(8SZeuVcfhC@Gsd$_<oG%4J>HiSbN5bhe5z<ccPpxPLYM^EdniI%~I&I$J%Z3x&S4CiQVT){D1ptW%=tS@v3;KT(>$lw?B3x46MLn8psE(ir;q1!<$une&-+7RFmq=DTCYz|G5@B$_XE}#o&`j~^Z7OE^T3G^mR!m%OYB0%rpf<j=}4e?1h44*7UabTn9$)z~ZFnmH~L91#~oMTg*WE6*j#fwXESY5nGjDzAa4)S9hTrrL@i{h9|aV7@^hl>N+3tD1=YQhDE54Z>@A1^{;5&;r`3y2DnK(E3iHcTY&VxuW$VD2!9gT??ZsN2x3VWh!}V`35)I|5uFKaL9UhZkYmYK#D3!Nil|fEqr*BR-iH#eqr1Cr*am<dWjRX5o{tDb8XP2O|hQxfEw}io?DK7wAU#M1}#H&7e5YQ+fjJ!7++s9ZXaN7^Mso>jxGPYz_>j2G$*{xEfkXE*v}=OaeqP34~%2j^>PUG`V;YC~L6h*bZRjO-y2;odk)44aN)DBe*!wa(ICbgcpfI<{(IXk`6Heg2X2mO$x)4AzZu&PEQi!&^qB02oj%Q%*H1W3_ZCN2dv=}(8ecWQXH^}PasHqvMh=NLE;k(#vCsoG`Kh>XLzA89(tF9NkEX81p6*rT=W{?;y5(8GZ-o1Vw;e}LgmK`bOF3b8u@`FCV?RglfYPlNx0==5`n`KT)@!b1qWqx6)4VfP}Y{sD9*Mh&UPsd21k5?(Gj0OYw!trAwIc`;#`a3To>bPgJT?MHOASXTlfTOj!&jRaiD1QMBa=I?hFQU2doFPg^BgEVOWH!*f_%Bg%r%DVG2lbv>Grxpv=$|ViLzjd4g~)OagOsOd?%u2QWhDB*7>FHVONNM3>I6(XhZkfld&*BnDnckkB@$U@%ya%LFbUK7k<d36HqIi=a3mDb6w}&T=TuX3EvFD9&~%&Jh&nNQ#pt#YvmuTt;!OMR6{9WH5Z7vcurZ&{xC0iWd?jm~HGN5(J4!pvz$r=rfoElpd3S)?yMG?7`JThZHUXJ0<A2fk{C0m;?q_Oaj&ylYn)?BodtyhC>NGNpc&ZgPY_rVmrX7f^jgcU>x`w80SL&peIRjrb%&7S$yJ*;<!a|Fk0Y~5EKWD;S+dj_+*irien5u*%rlttbipP>oL%gXjovN!TP~SgNDV0K^T*O<-#N`$^|SX7-hV`5DgcGh8ixmAXgVg2)qb%b`2Aqb?}k6z$D}|frSO?cmZDqE+9xuVxfY;1qwu0nRD`(!ApS)Xc0a+HpM|Z;u8pxo+QPAAn^(60#9IdF%E_<jAJ+~;zdv#2oj&bd%-6VBtC)vf=?hwdU7dFplb{l2^|3(Qm|Hdv2oS{9nioeBuKcRWrtA$y*Riy=z@b5nV1CTCYS_fCz!+)=(d9-!LWcw2u?L#U=jfr9Fgz>{vKRR>_>1BHa$s{H5hh^18Z#1#DU_#9^#W_P#jn!dXf|eHUXc|>4OXON_+xWjGkPI14D#QpqcmtZVNtvZs0`3U>FAz20>3au!BuRR|hT<=N>R=!1{qJin9;Uf2=#l2?Ab7E>KCFfxuvcGJ_}+lUQh|VaSK>h!+cG&C#;p{0B?}UL1)@pd3sBy$h2-Ps1cGDHvCR6zI<2#X$xIIuv-ZDGoFZpFoiGBq<I@MZ7o^2TAb>1c^^LGT=o}9Jz^**`zqzp*V+8oMTa(<5HZYiJU;E5iTxTcDRrrfh5BToPmBXTwE|LU~8aGc!Aj?TukhEaIsMbEsk>pxWM>?7xV;Z{zub55R8sqg@H+6evC<M>PHr68$F>L43jiYaWLTF6U~57GbqkAC=SL9dcv8NX`_3H7YE~PbkOi(Q5^Jmd@=>anKZey(aXS#LveypoUkYkrdGfbOhm8_P%WGb!&C(82UZsbcGOF(JM?poNgR@kEpbKw7l|^1`93Nic*H1A2RHuX#X?zwH-YVdNB$Uif&4mpR3;{Y@-YcF97MSmfD~t^7e}X;^^2pk(-^3b;PInBLqiC4Y-|b~-8iZehh|5h0;i*(ksxo0K!uC*Jp(6h3};{_0u?wLf)*n^mS`r)7=S5|2vkU&>?r~jl7I^Ge#tdO9Y7~kk`pNjsE`CyNCGM(0Tq&f3Q0hPB=19#_aF(VkOWjn0xIy=Mi*G(v>t~oHSBN#D#+d=v|y0V8ZfXEP$3DZaLHbgy}=G|;y{Ez1$9(L9SufV1S)I-DjZT&Ns8tYP$3DZpoT&nbtt98;SGTbNkD}_paRte#%ddZ3Q!gVDkK3F0)YxdieMzL5vTw?L7+ksP$3Yg03|`7!bYG1q>n&_i$DboV_<8*vVva=dVxR%C!j(QP+<{JVG~f{5KtirsBjUe0IfoImLX69{2)-l38)YRR9FO5*aTEK1XM@@DqI38TmmXw0xDbrDqI38TmmXw0xDbrDqI38TmmXw0xDbrDqI38TmmXw0xDbrDqI38TmmXw0xA%kFc4ZW(H}uCloL=P2&k|KsIUpBa0sZ71XQ>PRDjNc;)2rR$Yv5y!3n4k1XNfARM-SmI0RHk0xDbtDg@~}&_|%cA)vxVpaO<E1S&WI6&3*%4gnP|0u`JQP{9ePun4Gd2&ixosDPG2pn?-nVG&T_5K!SFPyuzcX~;*Q!bYG1++hSNYy>JGF9H=d0u>m}&?|=uVYrDtxr1s%Kn32TLyka&jX(v4Td4mIX$t}sHUbqGj>ZRp3YS1f43}7U1S$jp6%v68aFGzGuo0*LtwW$f5KtizsNg066*dADpyvow2m&f30u|7w5U7AyP!5BD3PC`HM4$rPCQ1EBl4KC5kOWk40xBc{6`X(yNk9cBph6N*!3n641XOSWDkK3FoPY{RKm{kDLK0BH38;_+RB!?+&{|=A(Tg+*s1O8H*aTEStb?EwIFL|B1S$jp6*d7CXyg!-0^bp*^$1i51ytAysE`Cypsh7b@_!A2{RpVA6;R<2P=S+D1S%W?Doj%W6%GLv6bD_)A)tcdKv^6DDk#peDNZtq1HsahOL6Ep6HtM12vj%(RA3we6%GLv6vteOGiic_K!v4%3ReLYTmcmh0TnngL!iP^K!vM-3a)?(hkyz+#Rybb3aD@uP{9>Y;Sf-Pb1(!dECp1!3aH=;sBjffArw&IDxg9rpu$x^g-}3+tAGljfC^Uu6+!_Ot^z8A0xDbuR0suBxC*Ec3aD@uP$3jh;VPg)D4>EXpu$x^g+)LG)(?RSM*$UF0Tr$SDl7sja59T7grk58u7C<x0TmVj6)0;2DjWq=a0OJj3aG#&Hu^IJR5%1w;G_+K3WtCSLPS824gnPu=b}kLpaSF2w9}KsI0Pyj0xBpD<^m1@6%=Q>6vqX{0d0qX3W@_e?hsHxah64KmP>Iq`gsUc-~<wZ3ZZ}sNk9coz7VLe38=scBmxye0Tnd3qn}4Wg-t*OjG+Wn2nAF~0xD2H5vZ^UsKEIy0u@356;c5eLID-70xE<8DqICr2nAHQ3aAhYsBjffArw&IDxg9rpu$x^g-}3+tAGljfC^Uu6+!_Ot^z8A0xDbuR7eF>2y#^rdBbjN6HtLh0Otcz0TqIP3X}^16*d7CC^G~qqyj1g0Tno5MWDhapaR<grxQ{E6@q{Yoa7@=VG~e+P7neWTmcnQ0To;U6;c5eTmcnQ0To;U6;c5eTmcnQ0To;U6;c5eTmcnQ0To;U6;c5eTmcnQ0To;U6;c5eTmcmh0TqbpB2Zx|pu$x^1y?|YLqG*~AOtEb1yr~SsNf2ya0sZdmB)vj5`hX=0To;U6%GLvhzui8VJV=(RX_zj5ps%pX(^A<P(X!6Kn2DjP+<{JL2*!qML-3`p{Gtj1;ufT;<!t3Fj2J#sGvBSUn5XKaWKYM1XNI*O@JQ)6&3*%j47bPQ9uP(K!vM-3X6aWkP877jshyU0xDbuRFJDn6LJJ990gQx1yr~SsK6xPG%*EKI0~rX3aGFNsK7}n0u|&jBN9eHg-t*O#i1KOKn2A~NpT<wrhp2YfC`L5pu#4g0^<;<peIRjAV`~l3X0>5;-DWe1ytAsRNy2EfeN933Ub_SoV6fOVG~e+6G#LqgaRsP{Z*n1jzEP?Km|JI2vi6KR7i6CaV~{Gg-t*O&a+H4zed`UfC`-NB2Xa}P{9>YAr(-;6;L4+P{9>YAr(-;6;L4+P{9>YAr(-;6;L4+P{9>YAr(-;6;L4+P{9>YAr(+TPdKm>P$3miAqc3z`k^aoBQ$|X7y%Vh0TqIP3R->@xDJOv1x{EIsE`V%5Cl}9tP!ZN38=scD*_c#0TqIP3PMX@hG;9Gf?x|0Bmxx<0Tsv~0u>Gc6%=P06lV&GGbP1wPH`Yehky!-qs1%)Dk#np6i03%0Tm7b6%?nIh6UOu1ync$RNzET(6SZ*6|Mp*xB@C10xGZrAy8o{pu$x^1y?|YLqG-UAOaPZ0xDbuRB#1U&@>R2>IkT?6j0$Rpn@x)!c{<pP(X#NfC{023ReLYLID-70xE<8DqICr2nAHQ3aAhYsBjffArw&IDxg9rpu$x^g-}3+tAGljfC{dF3ReLY76BDlKLjcq1ypbaRJaPLun4F?#14T9M*$UF0Tr$SDl7sjXocQzX^Eb3TBB!#5F$`v5m1330|FJ!Lv3SYWA<enbc0@HI-ATpv&wypR(vw_hSApFywU&h54~}yA0Fzz!2hQH%P&stp|U^w9OE2tk66bn_&lrTFpnp<+WkiI=zF*CjVrwk7j~t0;9_3sUAXWoJ%Ee2(tB{RuJjLZv9I)NxHwm}6p2rUXY8CCRbSgV@jq65y{&h&o$H-*Rt>bB{p)I=_w*0i&M&k@2}*;^lVCQV3@cS&RJ(_YbqfS^f2*zgU)y@{?;hme-#52E89N^$D!{A?($5>tj``%g&UgH6AaY(eH7xqPVaG)}S0LGkNH{U$hrRi*N}|#ec^FzE@rL2~#&+i^h`knaOwYd@61#@BQ|&x`^X4nuZgrmi;~yH8+)&|%hyR9K2yYx}S}iGkIPHHJ2HncIS1dbq&#;*~*VW_3tNQ*wbw{fuY+0Vqw)ZWNW4~9eHmt3Ec2Yn8Mf=IyXK%HTQ=^v7Z<;9rcdobp&fW1@4f0Qo>YclN;A%T`2ShI1hz85jaMMf(l+Aua>{L(cAOW^@vZtlXklruv<POH~*Z*DJ-`i?f5FZvOw-2N$P-1~HDv)Oi<VKpH<ALOVakf!Mpp|u>>DUCIV9?fj!_pffrtfSYIEuc5^qq*l6SX6=QW^n8RC?W3XEqslJ4}b$UOyOgr{P0q;NRhWEuB8N?RSG=CusSD!RW54Na)l4?*Z^S)Z(<aqkgw?H|fuUR`A*H%%YU4TT<+kagy&ID$wih8ehNulq&)947IQxHI=(_?N2ICrrx-AcikTZRmeUKDSh&&Ow2Wfd?=SsyB;X_IG9XElj<f#Z)&yRbAMI^<#?EGd!K5<9r$?|^?E=8e!amo2tFYZ>}QQ%TKktxq6Kj;JY#DMZ+=Eh&DM5d?xfxKreB5~$e`86qiO$htLJxb`_n*?fW$iPRQt7cSU-5%IygJMIBhfzpzw!`xX^S>MuTeHS4QJhubhnTz$|(9!EG>{wfbFsG}b{Zc=!77p_Z0)*r+;WArX&yRk#H;3`=N@#?$TXTDJ7yraz-LuP*4B$^AUJJ=9}vdjtQ&G{>+73<DL+tRL!>qR1-hSqZNgT;OsNOoLhVUFFFI2pt+UF0Jnwwf^qu-nOjux3@tfW}`_^z0mvme>IwCK<>I)KRD1$y4yc_qcghOYvN6=A=>l)pi715p{<JQI852CCYq`Y4@2N#xLalO-Q8hFs|}HljY?|B@T$Y@rnYr<qK~}lrx!0w?Q6CAX^U&SyQT%U-|(uVE#oum(cfJA`ev_w-hebCNNZs#sp*FvS?~^;0T{s!U%YU^d{o|5?!1fl?W@FebVl>x%!}F6K7i!z(1+2vhB-i?Daoz_;)1xXJDuB4C`fnp!!4NBYqea&HV)zXC=MrTx{89-$bff;U8TLtwTt)A9u$xmH_O?^xR>U0gT{wSC4k<RvVOus<{rRIW!hvm@rP58_D!oj7<E3W)`_dy*3rJ)29tj83&<S9ZGqtdWC^_4Xyy;9TJ2qBH0ZvUSNdo^!%N%me1dCj1A~n#Z!q$^pfkQ-ZR^P12Bw4XyU$hBqEMA6HOr=EQEFD2+RUalqts?;YMxEaqtv`KwaBIxQEE||+RCQ3qSRJtYCD_Sj#AsDshw<UCra%UQYSiUq!jdSQdJFsYNb8>OiokMU8BYrRn?t-H>gf;V3?=^70=OBlik0o1YSZ3`pC@x;NAJ)kEz6{)*2dR41|P%?rLGw*-5(5)8zn-M6zZaX;LH_cq;oLUpfpBk5)Y6%gQ&MQU)CJ@fa}8WeixNlmUj{7k?}cI9tYnWaS(P@rXKLEaLzxTgrlbOf__uvcRoU7EJbts%XijEZC-Ep)5hvVKoHSw2UcWMN`0*m;x44W@*Z-+!U}sYzp$_eA5&#*DN*x`{Tx-jDc?$1Ll@;@JFpd83)U)fhp|tsHLJ|a*e!DM=9m+4;zaz1`}hE<sfV%r<{X7YAi~%#8}3G5ak@m$JA4I83zt4<=_vSiZTuoQ&Gl&D-%nRkB|DZhKqAqOJNo*h56%7gGrWx<t>Hzs7{0JEY(7@WWX>V*Kcs_r5spRDF=_~I7n+L2huF%;88sXS1e<}G~99)9@BMT24Bhpx6_`xiWafOG>vi&AJem7%q(XiG#8~DJgQ^COty>zE)sK*kB>UFrrRuQEqKvd@E`Xpc)7LUkLp(>)}pNXcFBmrAJ?yN>}3qNtdxPrbSn~DQN{pcvXp~IbsSu=lm%gxv+$UnL&{c^^5B@|JUpiF@C|FgT(^{mNA(`QVGm5x{-#0T8m`b~ErKXo1o7kkgCL7w<}HGFRR4i-BMs50XlohlARZfbaF;PqhC7JIbsw0J%Qz?l9>gQN56p6wu~3FQh{tvxY<n3CrO<<TYzM)ymhw=BJ&4D45u{kkLmGU@Cx|+33HV?YO@j5~PJ&f#60Apc624&)O5q3VvEhg1MxhLUupZY@_=Z(T0T6Z^Z7&5NtVi}EQbr@o!eRu%dTc+!wwJL`20>Vl?M5Uvql|?z48nSBFCsA+Wh|sYh<tq1uS-A(yJ#`&A9o^bvKTyXG3>{6B3!;y6U$Ht`*Ga}(=eB^PzFQTkGy`t*ishCa0vU69SPGkmhn&uMA(n)NtmX)l!pX}aN=lZDG*^lvY%mcS<b>jAi{oRFT)hhG7i!}L_R+1*hL`1DOwEY$9)W^++sM7>tiGqqpbdANQCpaE=I~=lyOi7ML3VV!jagEG7d_y2<MS~h?Ko3<)I9Wa30x-NZE^09?HN7=aIdLZ&-v<Fv59cH{u&MAp=G%FbYl#MnwCQ!o4QCGC%nUrXpA&!c-AvA%d$2UWgDXLKGq_6=4-3Y!zV_A{-UrV8qgWRmnyiwHGPehqI%$<<z1LNH3DjJvaVmE%W42ia6<RDzZP+GEZUB4M-d91iA@saHA6L^U;lHe;Gbe6W|sm+5&|8M08ij4N~DSAaqoyObXih6eYn$q7eJYB*NDN({vaw62cAW8A|x3MUfP~b(kh)nnhB$(>y~8cXk&^;X!Q~TAUSW(H{5=F``~1hR4ojWMz~P!|m=FV#q@oHJO*ZTS86dh0k!edXXBwZl0lL$s#qi0X;(vUuY<yMw{Ex>F_W(wVn5;iGSA$eyc`l)iw)FqkX2hZ!txRWz~xn)r%F?i@8OfSWdxMiGr~*1;clMinKBs#!57dMH*I36T{c-4DD+ihD#tgo88^TS#`dUtnRTA-D3saLnzxR<2b8(tVH)%LHB@|5T(RqzE#{3Vp-M0)ecrhEUS5}MDtid^MIHuONnI^52XPa%M_0(#bXN;&n(zA+sScd<}{BAD>7vkO`BsENr`;@@SV95T6x<hts<?gZKKr<vy4{3xVfT8tf*k7;g(X%TQ@xOrbteySh@?C^xj*lTi`l?j=jRn_X@Mb?BOf4#bUC`hq!tf&jqW;Ojab8Q$AcK5T(>I$_L48R;qiZ(miv5?(u@rE9f52=^mC<WQiAzUP1MEUiE;K%gRXQZC*k1cwX}mL}#*$R>8CtG>;cFkCp|jQfhhIR@6LRFm6cBF-ytity@vUc$tPV*DWJgux~{j<7GNVuUVFm%PX0Q2b7d(8CP1y7igI%SU7y?Hp`dDshL&gyNNR2%`H;Os+m>lyosWL!&jsWw6c0;m3nWY#K1AjDH6-+nN{k(i82Fc+a=VpYG#%DZ=%eQIaUcdnQwtI2TqikGAWAWa%yIkdvGGJX4Ya4PAD}K3)IXi7_*|9Sw%G~^Wm&AAI>e(Dk@ru6K53-T2a%if){6%cyab(FU~44bwwSt3OZ<)x^Y&SsVnH9RnS4Z)Q_{uEL}kbt%3^LrH-6cX6OnUXcaWjF7@QByaL*bJvmD$ptV2&?V_D?^P_{EQ$V}im9vYM4$s;s&=UC?micma$vl;@BC)Kgv&)@1yTsPv3DN~>MLjF?=Ijz<hv&Hz$>qE`yTqGw7J74bi4nwO%8JEgHP9*Z=Ijy^h-dQ@h~*T}DfQ;;yaGB4y*XRypS?i;oT33N=%16*Kd024bBgw_sD4gf{hU&N&MBG07PQaFYoAl@&^aYmuBd%ZLHnF?kIpGEb4BfQ3TDnJ_voAwJ6F^)r%cPrJUXYu&=vK}DbuqukIpGkv_&4BqcqLQXd1omx3Tf;N#%Uz54--PTNzJAA140IP0-zG)=w(I&3xd`Mw6$N<I#tH#~)NC!H52I7EGSeYr+0-RvG#?!L$PTH!4pm{h>Nbpg$T`dcmx7{j3{wM%|!t?cWBK;iwXPo=yD9U^MzPAJa?4AA+ZqeMs@F?GHaq6=qrSr%3E3xEW2pJgqctgUJ`jqc~9TV=$?-gTd&o(#Nu)+;0E2-<|t|!57E}3<llGpbuBbvDbWx<W5I14g6$;UTHQibSUs<JfA`8Hqh-{>rkIrA9#gi0~B3lG^t$oyWL<|`8etip#o6<DH43P@gMzRXE2A_?M}Z;pWWQ}!>89TN>5dg_>%Kj@9MtZPF@!6-`vz5Do4X<ZKHKg?_IY1=`@(ksv&9$QJUvTeN*nVzs!QPcsI4&QIn9i@?>wn76!hnG~YKHuUh+Om!}t3`svC0^cPvKYPlEE$CLg|A1fZdh_0j&J}8ky55Zk{H}?CJ%**O=#bRo$_Phse^&Zb&0(VbQ%>@F%e28Dn8y6D3b)FP4p9bBCGTkFVb>qhgGCUGGo)DOTicY%Ih(`3NG`HJI34KbmqXZ%O@Ud7z{8l}--L#exIOs401Jz;2pQV`lj<@~qH!`WbUf1)|?f3O-7@}$uKPqOE$KWo$r*@2=@GbWEK^;zz#Nqql>MV$e0Xjw?Thr~~3tP;e-~o5xuXdlSvBzrh*%1%9+}^PEkQ@q8Jk3Ipns!FxKv(x2e;O3U8w~yS0JNaj{|v;!97SF25263JZVb?~D_uQwZs`T(e0zf38@JFdOm)B03C2(lB|H7Y9E@kHa~*U(MGw>YcsvQFsD_kJEx)My&S*N*kx&cFHWXOPzjY1V_XhLnb=3OFkt)z9B3*cbdQJKepW~o{!h;*Kul(znlj5HUtwuK<p4$-`oL<+T`O$$2o@Zz^buz=S{9J}G*YE|V3?E8PVHlR4!9e6UvakP#eJSabs3sr4{HIT5(Bq~U#`Q)`-Zi2+M@IutB6U2$P@PQxi6gt<d1O+ww4fEClr7S?qU2gFWuc<L?d>aXG_Ix00Uew0P*563p;q9qn(Cwm6%Nc1w^8-N!xYZmoD;)C=m){wXgq!2zl!?GFn2J+a5T;yT!HE`g^{-FL8GG-fkZ92g<jXWu7VtymJX#HInqitadRZ+EsRsAG0cbk*)(a1ICat<5Ro<1+vbZ>;m4`;{MeyyWhvlE1%>e?R|quDxKsO%R8)gnVJJ}EQBfYsre=ge_QwAdq%=~c!VZ}TIVF(PP_-?}r4jlfnc-63N@dj2ry||b8706=veSh)(&J-G)R`p@HSnl9<1f_=-R<<yd8;#9tED;gL@hfmE|QJv!C6I#bd$uK=*<wkz%s!p5@g9rC6^k{w`IBHRFbR*0bSY8s88m&6bZ5`A5wIx0&-3aC(^AF-`h+}g@Lz)AI7`5qHRUF2>P&^ig|$Y!)C}Zxt-#X4rbvd7@kyxJz2{-9L0tJ_J=Lve;S$_lI%~J@i3C-M%L}ayw%P4`Dwd9+|<un@0w?)$N&6#*4l42>KAZr{JMXv8@7N!Bykf}X7vzEzb7x19{QCkcRT{n4CFh@NAneC2TS~;+$#q*tU2C)ALsFqnG{GT6vgt0o>Z0Mr{FHSrNUm641=A)Xd2|3@K2b^AGa$%-k-jE7~Kdb8`JmD<uVmXSWAiwNk!6nC>t#;8Y;<n;5dmAy^mTabY?JIc^o9$C<ITz$>@Kg%!y)#3YMAbWZSC`=7HQ+oGK)Jj;a|d)-&+&o`K&x>)#Z#yLo_m7JE>=F6l%#al~@qCyvBtbgQ<eGpx`ST%S&7E%XLGuS)KkR^8iIGrlLO86?66mA!orCaB};=_O2klbrgS=GjFHwERFnslRExX&$|;Uo>>|-eR`)_J8s)^00n%j7Mlif}~ztJP#^jLHS)96`GmedVBlm$;1sf@$bCbr=#(f&GpgPgU1&h=P%*9!_DV#iAo=hUqIeg{q$gKYc$@)`?u$>j}9-Q^OPVr2JSVrFvsmvm{`YbB*`f6{>huuMyw^bPrJMEEO~3|_Nl*Ht%kg8ZB-S6LepN->3%BN^EiV7T0+A0gM+VMLtdbe<BRkY6d9M;h9ZbCZUJ9N_#sodlg7#MSv@HLp3g7NnvHCg(=+_&K&RBS2mzr19^~cg?<#F|mKTQiJznd-z_#1j!OrBvK-Itc$!pU!I?qmp?yA7l>@8oy@OLahyAM<R^b^rDuD;@hsf(#D{7S2pP6KX&nU52aq`!aa52N7>Z^4Dv?$fg_7z`mQEI%1?H7!3IBR4%EW8$f0(X<ZYQgbygcHKeclgXNAWC(CAp3<c<?4;<_QmHNK5a}cJ#{LXUPI`*^ax;3o0gn9-;eh&FS&~dxEp2I#(l^GgtepW)GB))iRPE!gEovXJ<0hveg0qp@M16YlKKk74_DAK@<focjm_>*39&*MwYlv|YlAcC`_|tM`q``^o?Cj8)Ipqx<IR`(gVm#FF9&WSKehg$+9%@G22)V{EGYn&?Fs{NbQ$a!n9j1b;ToIs4FZpw3QKYTXHyh`d#}}zg&Xt#*_lN#xtU(muUM*InvIdjXUQ|H?TEwFU+J752PDvJSCV6C>2S2jBEElumTvk$2>O0B{^dSUE3a1Tbo7d46)-6V5N@`bf*eVRR(LkFyP%w&z^pjco5vR_nS;4sDsU*OI-h+Pwe;B}Jd<~NVxK77|K9~Xh)*tk{m}EW}-~~@wBupiq<cD}OMk0{bBC<%Sm%ddnIOI$pyK3kSLBvohwHm2=1hjNggB#AUJD#U1k($&Sk%@+h@I!hK9(R6h6i!G+10#+?FTx@3DCVH>*=8-nO}e+@bP6Wu+e}Tbpr^-^LG-a;`0(i9x;9<P$L|!vks7F9l3?&4UKq-+o;T@IYkR2yH<hBTQnasVy`+?&cK@z2^Zc6cwSmkGPpzy}%8+54ja4esyZ($I7HY2w&LS(yd7+ZJSGfP(*V{P94*XBGD8X4Xjvtl9|C&nhxh%oy*+raSSoNdmG!y5SdvTI!84YN&C_y5NmwvZvS~jJBu6ES>emJD-ZMtY>r5!g86OJH{PA*Em$mY?j*GaNTK3Rq!_&-s~=)^-+d`V)|lK*<1?2ZrfDgHw*!Pge#Jib_#6FexC#iCLhi}FV6af>qVHJ_^<0C`@r=ZP<aDy;n*)HJopKLbaNJGuf=P>t0c^)M1;NlDmk<AzqPt4ayq$WTpC#-nn)Q_ULYi_NyC`qQ#@IleghhIq@EDI*p-#YpY=AVmy@2+DO;o`)P~%yfQ%nc~#mx2#BkSm<w`G%o7Tl_fK3c@GviD(@b6@al825~(B7jf{t)`z-67s6te`QcisB;%OJXs_>l<1<9&NJmmF0Ipj4R6=wuDS`A|?8GZ0I9W3_jF!Faorov{zxn}u^xxHR;X0DpTq>3`Nur3jq3`7=sTRS=6Ooie>=;pR><hkeCeLR$gV{I)OhU25lk<LZJeEtmcJevY0Mnr;@onoFPR(ha$o}d*G<h4I|l6kSv!lCB*LhYzf=SPn<FBVof;XGd$xNb^fR<3=dc8@C<N&&BSLbyGvsySM2YUVNbayrsFzo<7ue|kF`r+km2(}TvZVdoip!17$%nb(wlg*BS1D!z-W__|R)I7ihRBQwO!L(*X%(!I9vwgJ=hsH+pajst&$v%{@I+83JMy~eAf)0lu-U4>j}?=aHiv||{0nz3$2{W0oLs;ek(sm#{Y51-#hg??1bZJCx;Qy#6du`gaojRKW>8-{_;-}62`b86%RfBe}=e8={@^C_5lRU)!&KIv&cOYq&MlMe7hfiGyz_7e1|{tA2#ywqW4f$s88KUE<iHPjXz-d$DXo|#&x@M_~i*hY>zZXY?*=(qI&X1l>8ocI5PG_~Pqh}Tvx+`560N*dWlJUL3*Fp+X7_npX~D7xtxo|YWfp0Uzt6RoFgnVzy>YIaaI5;RT^T8BrC<AZ202suk_R0x2Ln7@>+?8Mw}Gqu!)DPO1*_*P$h=cy>F6DbqSspuN|t+}bRX`~Om4^O<Ws_PEZem29&P;QyyT__Pe#ayqZ(n~`FT`=^IdXFYkdS-Z`r-R1vMZH9BizSV1ttXnI0;y6;*t)8-nywX2z*l{*I4NDw^IzAG6Q#*4c!Bq2s0E^(?6PWl28N`%LC>ELX3xV}oEpqRm@l>5l_#EBfeO7mI=me+DFd2csg1HkxMzAPE!3gyXx+2pA>AxesE+)HDfDmiVA2n!rDyUVUuyR#`s3KFLP#yOjE1#OO~Wtrjvh}C!G<>fsb3zQUV!GD)PE(jTUa>n^#{Q8{H7gDs(HXnt#tP?xL1Uw<7z;>09`R^l&k$7=6+YT=#v#g4_dif?dfg&&|r*6QRX3jyCTlrem}fQS`wyvvk|CWwXGA5&W!ZuR+4=p{;Z7iPr;WA<D1WL+gNY<tn*<qnvb7_``s}6=C>;(nQNBTD0<^oLw)>a%|fBV^j3Y?;|WY%DeTjGX<Q{%=#~udwBrxK&gh#zJMOgd^XB>f>D(6jCw=Qy0}l_^Bqp7karKjqmGzSHZfh_cL)`TQa{uSQhX1MdD2_GN-^K{b7BS`SXx<(Km1)qacJK=X{Vu-NjF2s@kl>QabR2Xlvl>OWJ_Iuit9JCQnHDwL?CI>b1thlVW(aprSg_;fkmu?A=Ek3V$u!sv%<}b+ht7B&-QIz|<NQA4VlqcSwlb+f>FU1PygaYJYP8N9$A|jXWYLNaE$D1MgFZ4F;ikc7?fx)%+Kd)@up>WvQn|Peuv-p;Nd-C>bj%72fE6&&{Yg-XF!&qfqz}Ec8$fh_T2ZPMev_dRd=5HKapz)c8ytw=OZT+}T8Zg4HGMLjdhre$ZSr(7$KeG+X``2ZcRd;e9;PKYemZ?YA({$@XSI1_IO|n6@Bg)lY|p3v+I;@6&7a|-|7#OPo_<!lRUzc(%{R>>&@~Dq$14}840<k*Hmv2sqLDA3H2F?T8D*?yE<EFi<l+jxNFja#X0vq-oi-l@%HnrRV=^!4FOKUE^KrQFuXfjA%<ppu16>1kPXa%7Q3llHE!E^LY{ncVXh8~2@}(lFkyZ43JPszMiNYd21(RVgXm#e33AAN-8q&%IDaLc`(xai0(NnjF<s-6Q2pu7`K3Dp3zo{#Qdbx><nVZiy-_*~~H+AahDn@OZnd+f`pgxonsf?ad5<ON6J);PEq3QK>W9zBr)iVvMXPQv2D$A}_@%uX36K?9bSO@7KEVX`%;>KR7x}KgMdp4Djq1R?YQLGpSMs@%AZ2y<mo95Ym<NUm}|K{@I=%mp)I?#5|+$AYa&Q8xR&Q6c^wH-2kAuO#H4>Q}=qRx%o_vdum>;0FTItYAIAB}0t`1}5quC}*nwefs5t!_R%Y-(kA{!RaLvc~*byZ`)e?=#IzK0on{&rUCBbIa_`Yhk#h!lke~zAf8vxE&1$pYx{w%Me-)cVCx&<_7)TWU;^>%)+lA#TYvJ2fMO1!BsQ-BGCQ4@$it$lfq8|O|~g7%#lhqGK2?i&_|TwkN@;_SI4>|2iub;jBoc9jr>=F`sxcoskE*Wr#(BtFK!jS97Nv@qQv;Epoa%~51`(e&HX{84GFrqrEor@(S~$>5KNxZAOvFzr11wIM&MCj-&DF2=pwiSKLDqu3!Mk2FsR13>E5*LopxU>B2HEQa86ahz5y93xHdb$@eG>B@1sn*xPc$~K!1vDL|LO33~s;$p5luH)PNWdyd-6JV4xoO{hOziXWiiT*&KRQcXSiJBoGWg0C{j~haZp>I39!k?>?gUI#5jZRO4F^w~#2TX=eljYV;NYRu;*rX;-(>te+mx+XZiMJ`}&40Oiqe3l;11XL|HXf{xWt??Uu&>qrp4qtFeYE<<7_dbt4R3&3vWw6*`Xb$kSq)(X1JFz)VGnQ1Wm45u*gqq{a2TAX~p{-*W%D4o={rEL__9G|7q7}7OO2PXd#zs>Agmaw(#+XZn4I6ZnxTjrSKxCZBr!RI>155sa{I?f!wvCdum_PRL-opkUMr;ZKx48LuR-=uZt_%%&K;)hkmT(?XKiEM7o@te{3C2P~P<`1<6#UCF1dU4rofJ}%B`kuJJ&+Y;j`1xvKN)BA$N3uD7c^L`-np|=l%EGVGa)zJFh13$twD6n2aPI<(CJ?gl-oj648m5zCqSZnMU<#p@!#}AJC79^y!5`PMZ&Ogm!M7w(cUrwJy)Y3%38YTN&E*|XzRx<ojWP&uMZ9xMnWrt(xS@`du`exD^v^m`U;NquZHQ=**;2Q-33wv_^Iy3?Q<~&4m|uVvcqUwrPLD2*>c?tY=J9mMuaHzgKx*FRS;;d-+wgdPxsL;g=fFL#{&^C~pPgVyF5MoTdd$F-7ZA%BmGOTX`@o0^QdZtAbf4*$oAzjcj(@5<P*?J!4wHLBDKt(M2peCk*L>9bI~fY<RUx9IEL{KQW=>vFCEC12uMl;DDY?f=STJEdyS!*LBbgcWr^mq{z|;fO@jQ9lyF5BRNFM8l_)B6-0z<JS0nNsnv*txA0Z8j1`*MJ4d-74Tn`4sww8<`ca9ZZ6v1^7VYnE)cC0fZ|?P$MMTDx{trBe_!?HRD4>rtWk9mmOYsL%NO;srV{aZFm3Q}?-4ig)^@7{z=lL8c$3_U5L;F{idT(iTf1U0c%){I38Vk%WrKQATi?&AIPr3~Av&7Vi-RN1+zZ-9L<QQ<0i}!~HHdlaFhL^ZL+^=v5qdo@iTl+mKM_<_=tvx&3`lIZ~J!O;IrE`5hdFuKoEGjLN@;o8Ss|!O=~9j1wr(D>obTIsuMn_|3}L@<2t>I;T3b&N9X++X>={_g$GYH=YDzKQe=fTlWN}z0_GzHkmgTHnMwOuKhs|q=lDVlP=*d!*`W2Iuu<mk+oJ^xTORfHS*uRk1y{gRh3i!2wt}KTs@#rKkhmTLd8{kx(OF0Q`i+P%El{+C#@4>TRtJSKH>%;$Wx2oFv>-!wY3M@2J@~m$3jxPf4itl<H`#cH^PMxctlc@a#D2CUY11j3^Gl!sAb#~-Xz?(q?&V{-*7_)3C;5K8VmZANV+$tp-!z&M>}GdznFs6*t<M<)woD4O2<KZydrzjKt%&LpmCr=u1elz*~pC2UNtp-YbmN~Ut)DhG`rf}wQ19Lz7yc!2HhZ2Q$0IkXbWV8dv*RwS*h<mmI&pK)}i>4LF6ib`!$2;W5){d42SFQ+@BwQ8d+sk58s(neMdPg6Ysw#U$U<sIga+~t8$|!B1XF>(=S^r*vDUxQf7O<R?BXOr_To`D-%&+r5oS*pV;^wwMZi1%!jA573t1z#x3%cl4&vd7EkDO%Jg>kO!L1~vZtKiA^Yb$w1Ab>p!{ytWJ*5oMQ;TsuNbKp8bh|?opVVZ2x{-1?$z3~xi$W{u!nEY<0o{ZkMxEVa7-lmV&Nsj$WRR<$V&7wS+%{p>uO(Pf-p1xsJmJ%ohB1W({>uZ)2}7om%O+cVfynPZWmBheRy~XJvnOrl3dZ-p5NGon_v9t_WcjT5zeh!G;~d?nQt*CYe1!6r%n&#3#~$CbMf>&Gq0j|(<mT*50~D8QfVZPZtB*BF)J)33}G-74m;5UyYh}NGkc>qiQo?z0aCi0P!)4wW6*<^dmSPw@5cDkg+*=y9{ijxB=-sN&%vbAp9Zbyz=HIGU1nP=jRNY`=1|sQNLJeKR6<CCDHl6XajMLw+*)!QE)1q->>tDTZZg}ZS!UVLtR?T?m9HU2^k{>BYyY@WZ)VmKmt?`0k!i<Pz4_`qlPR?z5^ny_ZcQ&x#S<ieSmS+66Q8bhd<F36^s;_&batAHi<>)3+VfP2+iYvA<oyM;_@lt5aPms;DuAl!l|W%q{pr}B!CZd=w=n-uh!!GE;A;o?x;>b}IpSw9J&xXlz!N%fIS5>W%ItbFnt!;a1tmnq;z_Yyp;-w<Af{bWbLIg!7HXngDH)q=VJIXs)sp>fmMkR_|6cOi#bV+1a{}!rLQJxIw55K!wY5mDO6iJ>ngup(!M6L0*)ekL7~gJFDjOQ`P2JdLFnO6)Xm0|i=IQzU!L;(~Y2|>Lt#S@^;_V%RUwvrU{_vw}&B|yv_!0^{(|I!8#TNXLJIrb0RlU5!{1F-D--rm;Hva(2Ss@s?jRzZx-;zjMr^J3m_As`Ckzqu8nD^{%ThUVS;n8uU@}#FP8y!jE!<`g*YKH*27|C<nc#kV6SE&OI3L&5Z{UQ1DdTNh^l0zmCak9QY$Ogh#r560i5|pf7&lfIV&%d#LoqoSjttw`gu6yB<P*4BHitqJk&;?o)2vR0cD8Fjj!2n#oJid(XLg5w`QBlJAb>o#SCNEnWUbLLNbOm?G%5P!`a}lvkQpXhahaXy@!sHUh%AsCM%EhK%vn!2CUatF&b?0z@bhCc)Jqyy&K$HZ}OIM)>^Y2-`PW6nu1mezBXso!0<#jPR`Xe8cd6RuXqTGQv7~B2M)oKN;g0TS`6PcFKqI}O9c6PNoS;fvSKWCSw7ax6-H7wsa38%QG9s1IzCtCUPcKklGOkOgm3`WBb+GL*JeDeLfSkfjkWmnVYbn!t?damiTTB&ytFNvoN;E$||@4%pd{!WPLK7=ZlQ;?okd(^VyGiP>&QSmVaWFd{KwXVrP16hOFNc1zPcKTkK@(72Vws0+Pev>s54+u&pJBk(|^c0za{8Iol4bnK>yYc%&+Lho>K6G@oiR%g6--eS>4Bi!AzvA@;O8|2k_MTUw)wgiT7cA0OwFEruz<6GHkJ{O}y{fz?4KPL%2KS-TOvA^HKW_Owln$j#_7))Om&Bx@_z+(;(N#?O5?;955V^ip$I1iC(CM=gJd8;B*SD<!?gsU!n&M@=Ymw56F#YpnVY#-EJu*vWv|eV)v7&rN0=h(XR~hVV20N7@as5LXs2om?Hz&@bX9cH{%Up7qlt9fp?7T3YuV0TZUvTs5*GLR6l8S!)`coA8^=qceFWA?wQEl)(3q@^hRby&`3c&C5LaHds)>aPZfVgU0*{@%-wb2U6wO9ud51*9K3pZ3!ec6@1Nea2C{e)XL!^LGn95T6HhRL6Arnf=lHkF3ildYv#_%xW^w&y+Y?a&ufyIfn~$L}5Dfe^`FNN?%(Asu%Kd1d>DYII^oba<o!LDNTQELpN4-~A|sEZ|lIgcKsQ-yeHfEMM(~AO!!b+VfCDY{bJ_(SCV4u?&U=7#Kecs|3?Nd7^Dy=)!RA;%Jp=rUG1fA20l;4*pP(`wzh02?$MD2^f0VNN<ZC!oU>{`}A%y4wVt;nck>CZ;&S`Yw4Y>YJZJd<=Nb$SytoM*Y(Tui^jobtvD}<rXx`AWP5=ZpN<f1Ge{qqutDzu@4s&B|MFa|E$*MZ(Q0_J*VJ;0iqt!mW3wCeG(B~b4u6?mfPbD@ELVC>YtCMjT>CJZjVh{+n5OnkW^i3UJ=E-ak$x4%A_yu^`7*mETEb>#po_98W>Hr|R-+TU4D<>jZwYQSEt<3rjd0M8V$~BNN6HWMLYQA+{E;8%W&A)dc~vBZtmIIQv~%a>ojWxRPkk9G++G9|_FDGqQbzp3lo!4(Wuy<%^Rn)iS2&%`%N|JPmA#G~g96EslUQu}ph?dt?ZsgS>|A&I6V-_~L%<w+4!&#<zDqC+JtKPmAe245oS>_&-?{zSup?iKlrrw!H=mF=Wi%YeQS>tf6CnzI$S%0$&M#9axIQ<$?85q148v!@5thb_h^MeS6njBtTaeCl+V~Q_@fyaZd=9kYM!NeW{v6zlXJ6Er92ty<!i(fG5KkGLkv<oL3aovD^<Qay)5vYhK@k!>?x9@{KF?y{hnB~~*JT|W#=F8wh?;fH4Ly<XMg=+mF6-b*Pk+!Q5DU^JDY7=YpmM1-whMhLl~}7STEg;V>N9L=*Xo7d*0XdM52ewU<zQg@sE04pe<X{M9bS?hg4*ux@#R8YNx#<<$~zUL(8B0-B9sokEVPtTq2W>+sF2Onz9Fyl?a!z;r4xFY$|0G|5V@U=SH>ahxNU7wpV?-fm-Fb-M+kbn*vq~Na-KIXGWws_XxuFaBFPq8*h{8G`*`sDjaqs)p%-#qT<VBGp;Yh6&Fa14x`dKW;{IleipO5?b92CB$#NBlBeMXLnuVu3e3n_YEOHR{Pqj-BghsEvB%70A1j8Y=Km0(OkNcBKIOJBQV>~x}suo2)^~Ym;rB%HqgUcQGVw_qGfngbEhEN@az{lRswwGe{+ipd)-7kljWVU=}<6h>Q_jzG+2AzzO6*0LGVFsA_s7@X4(P0Z+FmTssUssBqVsRyK^fwN&O%kR~v{mRrEs5L7$uhTrLMt7rLjd0EDTh16<)40>j=;^{y!*VFxYN)X65zfUf@hijp7x}5@VCIPS^y1Y(4(yE<MN{S?!3@{r{3qKg{x{5&k+k<D2j+ZO)u>+LT+m3#L2F0Bt9-U+{-=u^iHIO8iACuR#<IN)oN6<dZ=wg-fF&34F8LYOtkxXR=YviX&$oH^5y3FKTj`SH!hC$qYgy{Za&`(A2)H6)ZdEz1B$I$<auUGaoKJp6_ee05{A_tR6vMFphSLTZE8bJY1KdvQ-MCr=HCl>rB8xeye4Q>xBo%Cznz{X|3+TCm+=IEW_NUt`BfI$+=HcP)&Dg9b6aKk88J6?`^;lT?LlqeRUxIQtRhCbljXL5<t2sfupLmKYyuT?MKhM~dwnu|g-3~)qEh`Log=Y2`)~7W6#H-0FrHsmibmHKB5OaiL>CvE(#b!wXoR?Rw}qb$Q4n)f;x|C&C`G(SI?Y<9FGlM!i<WDOD`$W3JxW@^`UB|tcfJToFnj50Qc5p!ub)KlOM;)K7M)_{%$S#@3q0}hrrW7QPcs|IvmoYX<~^{;^Ha?V?4O;t!dJ+^Mon6N8{e$#Af5nTTPu7AEjburGdnxVuj1$-(3%!UJS?Ey`hn%8Z?07Rk@b#0`@ZHR2yluTBAB5nFoez@HvTWl%wh!'
def native_source_check():
 data=zlib.decompress(base64.b85decode(NATIVE_SOURCE_B85))
 assert len(data)==94144 and hashlib.sha256(data).hexdigest()=='e4b358784e95303f4fb992a8ccd24e5f054e55bea63d09d844652b720c790df7'
 body=data.split(b'static void finish_work(unsigned future_branch){',1)[1].split(b'static void finish_stop',1)[0]
 assert b'total(' not in body and b'R[R_BUDGET]=add256' in body
 return int(hashlib.sha256(data).hexdigest(),16)

def run_request(req):
 global LABELS
 assert req.get('schema_version')==1 and len(req['trials'])<=256
 p,k,handlers,LABELS,cont,info=generate_program();out=[]
 for i,tr in enumerate(req['trials']):
  rec=dict(trial=tr['trial'],message_a_hex=None,message_b_hex=None)
  if i==0:
   obs=dict(program_instructions=290283,program_bytes=len(p),program_constants=len(k),program_registers=94,
            program_handlers=640,program_callsites=640,program_literal_branches=41121,indirect_call_ret=0,
            program_hash_int=int(hashlib.sha256(p).hexdigest(),16),full_physical_reset_executed=0)
   obs.update(reset_fixtures());obs.update(semantic_fixtures());obs.update(boundary_fixtures(p,k))
   obs.update(callback_fixtures(p,k,cont,info));obs.update(arithmetic_fixtures(p,k))
   obs.update(controller_fixtures(p,k));obs.update(mixed_window_fixtures(p,k))
   obs['native_source_hash_int']=native_source_check();obs['all_gates_pass']=1
   summary_keys=(
    'all_gates_pass',
    'program_hash_int',
    'program_instructions',
    'program_bytes',
    'program_literal_branches',
    'callsites_executed',
    'dispatcher_directions',
    'positive_callback_ops',
    'negative_step_ops',
    'controller_completed_cvs',
    'controller_cap_reject_before_draw',
    'reset_full_operations',
    'mixed_window_union_queries',
    'controller_inband_budget',
    'native_source_hash_int',
    'fixed_iv_fixture_not_collision',
   )
   rec['observations']={name:obs[name] for name in summary_keys}
  elif i<3:
   obs,outputs=seeded_experiment(p,k,Shake(req['experiment_id']+'|'+tr['seed']));rec['observations']=obs
   if outputs:rec['message_a_hex']=outputs[0][:128].hex();rec['message_b_hex']=outputs[0][128:].hex()
  out.append(rec)
 return dict(schema_version=1,trials=out)

if __name__=='__main__':
 json.dump(run_request(json.load(sys.stdin)),sys.stdout,sort_keys=True,separators=(',',':'));sys.stdout.write('\n')

```

## Appendix R4. Selected raw local receipts

These bytes are selected local records, not a trusted organizer report or the full archive.


File `PREREG.md`, SHA256`85fb5978a08036a9ec2386e04abbe19e9a58379fbc2349ceb3daf874d761f408`.

````text
# In-band budget v4 protocol

The direct program uses a charged 256-bit BUDGET register. Each literal leaf and reached late stage adds its static upper work, including the counter ADD. A fixed full-CV base is added once at the boundary. The cap receives no histogram, elapsed-time, or external supervisor input. The approved design and exact arithmetic are in PLAN.md, code/meter.py and code/score_v4.py.

Development code and inputs are sealed before the first executable case in FREEZE_DEV.json. Every attempted development case is retained, including failures and repaired revisions. Development may repair a failed verifier or implementation before the final freeze, with a new named attempt and recorded source identities. A development failure is never relabeled as a final pass.

The final order is holdout_0, holdout_1, holdout_2, full_final, each once in a fresh cgroup. The first three use nc17/LU12; the final one uses the actual nc27 table and LU12. Each has one CV and callback fixtures with its table live. No final case is rerun, replaced or selected after observing outcomes. A failure or unavailable required check seals HOLD. Remaining cases still run once after a failure.

Final inputs are SHAKE256 of the distinct v4 domain in holdouts/seeds.json and labels, generated before any outcome. Their M0 blocks and coin streams are checked disjoint from all sealed v3 development/final inputs and inherited input registries, and from every v4 development stream. Deterministic expansion proves plumbing only; the ideal algorithm still specifies four independent uniform 256-bit RAND words per CV.

Before final outcomes, FREEZE.json binds source, all literal program bytes and metadata, binaries, toolchain, model, protocol, exact ledger, independent check sources and inputs, runners and every retained development result. Gates must pass first: byte-identical stripped v3 semantics, admitted literal meter and dataflow, all640 continuations and639 dispatcher conditions, full-size independent retention representation, field/claw scalar and original-SWAR replay, actual instruction/operand/branch/next-PC histograms, controller equality and larger-cap rejection, success stop before another coin draw, production diagnostics off, and unrelated-window union fixtures.

Native containers use the existing pinned amd64 python image digest2986c55feb36e6cae00fa1fefb454283e4b33f35e75ff8bdd123b134130be301, network none, read-only root, uid/gid65534, one CPU,384MiB memory and swap,32 PIDs, no capabilities, no-new-privileges, IPC none, and16MiB noexec tmpfs. The static executable and exact program are copied into each cgroup before execution. IDs, intervals, Config/HostConfig, image and exit states are retained. Container outcomes cannot authenticate the absence of deleted unrecorded external trials; that provenance remains UNKNOWN.

Whole memory is max(all v4 final/development post-exit cgroup and RSS peaks, inherited 269946880, inherited preprocessing plus complete new ELF/program and2048 state words)+65536. Nothing is subtracted. All code, named banks, native RAM, table/mirrors, messages, allocator/stack, shell, file/cache pages and kernel charges remain included. Verification-only reviewer memory is separate. The design target is274931712 guarded bytes; the exact score's maximum memory ceiling is authoritative. Both exact-incumbent and displayed91.02075 gains must be at least0.1005 bits.

Preprocessing charges2^78+2^74+2^70 target-compressions in full, including failed and repeated development. Installation reserves2^20 word operations. All actual new counter additions and fixed transfers are priced. Mean cost uses maximum-window stage rates; minimum-window rates remain success lower bounds. The counter maximum, cap, overshoot, FIN and full total must reproduce exactly. Bernstein loss must be below2^-60 under H1.

H1, H1-P1, H2-P1, H3-P1, historical preprocessing and development completeness, inherited narrow/LEGACY pricing and any non-authenticated memory provenance remain explicit conditions. No ordinary collision, full N_CV/LU32 execution, new rare-event probability/confidence, organizer qualification, candidate integration or submission is claimed. Verification-only reproduction may rebuild and consume retained records; it must not execute a final candidate case.

````


File `RESOURCE_LEDGER.tsv`, SHA256`f8159b7c38b77ec9b2708bbff8acf8cb57072ce4cd2d3143b1e152799734da83`.

````text
quantity	value	basis
C	2728	selected reference
N_CV	12014587405061634	inherited conditional success budget
physical_table_bytes	268435712	(2^23+8)*32
program_bytes	2322264	290283 eight-byte records
ELF_bytes	906840	complete static native image
constant_words	241	finite named bank
mutable_words	94	finite named bank including BUDGET
native_RAM_words	234	full 256-bit words
literal_meter_updates	20480	8960 leaf +8960 nonfull +4*640 late stages
fixed_CV_budget_charge	1489431040983	8321635287+2^32*88281/256
mean_meter_extra_upper	90547/32768	including nonempty-head overcharge
reserved_mean_extra	3	operations per scan word
maximum_budget_scan	2335626	includes560 conservative head-coverage budget units
online_cap	23369453903347697850258080090	ceil((65537/65536)*N_CV*mu)
overshoot	10031445607322583	one complete maximum budget CV
FIN	17968	once-only terminal/failure
INSTALL	1048576	once-only reserve
installation_upper	205916	full ELF/program+2048 initialized words
preprocessing_word_ops	879238525979567763757203456	all retained charged allowances
total_word_ops	24248692429337297059623672673	complete capped construction
guarded_memory	275128320	all retained whole peaks and floors+65536
exact_scalar	90.913795090734567081165837063520379094031376743108149461558246812652755706831634072986555737509812591321719845	time plus max(0, memory_log2-20)
gain_exact_incumbent	0.10694021625535722187841819604207267408655621090395497049965339933113253487275194290176287925389460826715396864	staged exact product, not current remote verification

````


File `DEVELOPMENT_HISTORY.json`, SHA256`7d8548b425ece230ca352f7356b19b6e9a97cc1ace47cf02aa5a7a751193af2b`.

````text
{
  "attempts": [
    {
      "stage": "generate1",
      "exit": 1,
      "outcome_bearing": false,
      "reason": "Metadata remapper received integer dispatcher-depth keys; added string-key guard. No executable or final case ran."
    },
    {
      "stage": "build_independent1",
      "exit": 1,
      "outcome_bearing": false,
      "reason": "Copied reviewer scalar_constants.h was omitted by setup extension filter; restored sealed v3 header before build."
    },
    {
      "stage": "static_checks1",
      "exit": 1,
      "candidate_executed": false,
      "reason": "Mixed-head interpreter did not skip zero-unit EVENT metadata; inherited semantic checker did not normalize native opcodes. Both verifier-only defects retained in development_revisions/0001."
    },
    {
      "stage": "dev_small_r1",
      "exit": 0,
      "case": "dev_small",
      "implementation_revision": 1,
      "reason": "Bounded native success retained; later static review found missing nonempty L/H head XOR in budget. Not a final run."
    },
    {
      "stage": "dev_multi_r1",
      "exit": 0,
      "case": "dev_multi",
      "implementation_revision": 1,
      "reason": "Three-CV native success retained; same pre-final budget omission. Not a final run."
    },
    {
      "stage": "replay_adaptation1",
      "candidate_executed": false,
      "exit": 1,
      "reason": "Copied scanner_model bank assertion still named v3 counts, fixed to metadata94/241. Dependent claw/outer checks had missing scanner result; later replays passed."
    },
    {
      "stage": "budget_revision2",
      "candidate_executed": false,
      "reason": "Added1 budget unit per existing leaf to cover event-only L/H XOR; rational expected overcharge<=3/16, total overhead90547/32768<3. No added instruction; same cap and code sizes."
    }
  ],
  "final_outcomes": 0,
  "scope": "New v4 development only; all attempted cases and repairs will be retained.",
  "current_revision": 2,
  "current_development_cases": [
    "dev_small_r2",
    "dev_multi_r2",
    "dev_cap",
    "dev_stop",
    "dev_full",
    "dev_production"
  ],
  "all_current_native_and_independent_gates": "PASS",
  "superseded_native_cases_retained": [
    "dev_small",
    "dev_multi"
  ],
  "superseded_native_peaks_included": true,
  "revision2_budget_maximum_note": "Added560 to per-scan budget maximum for per-marker head coverage; charged-instruction maximum addition remains3360. Same cap, larger conservative OVER."
}

````


File `POSTFREEZE_NOTES.json`, SHA256`9faae8a14977d3e6b1024c83ca41f790fc9d034fee0569ddd51d71483cd1315c`.

````text
{
  "events": [
    {
      "event": "verification_exit_marker_corrected",
      "reason": "An exit0 marker was written while the verification tool session was still running. It was removed; the final marker will be written only after the actual tool exit is observed. No candidate run or substantive report changed.",
      "timestamp_ns": 1792740627091634587
    },
    {
      "event": "verification_wrapper_manifest_path_repair",
      "reason": "First replay rebuilt identical source/program/five binaries, then stopped because it expected toolchain manifests in toolchain/. The frozen bind script wrote them to bin/. Corrected only the post-freeze wrapper comparison path. All first-attempt logs and outputs remain retained; no frozen input or native run changed.",
      "timestamp_ns": 1792740669911727576
    }
  ]
}

````


File `REPLAY_RESULTS.json`, SHA256`5f0c3c427186dcfbc8a95ab31e8dd43463cb4b8435fdeaeb10a9b612abc1a32d`.

````text
{
  "status": "PASS",
  "candidate_executions": 0,
  "verification_only": true,
  "directory": "replay/independent-1792740671344750348",
  "steps": 34,
  "byte_identical_source_program_metadata_and_five_binaries": true,
  "same_toolchain_inputs": true,
  "all_replayed_final_semantic_reports_identical": true,
  "frozen_inputs_unchanged": true
}

````


File `review/installation.json`, SHA256`340d0984c3d776221b9bce855b065ca9a3a0b18c7710113327185659f6d4b108`.

````text
{
  "status": "PASS",
  "ELF_bytes": 906840,
  "program_bytes": 2322264,
  "named_words": 335,
  "native_RAM_words": 234,
  "state_initialization_words_upper": 2048,
  "installation_operations_upper": 205916,
  "installation_reserve": 1048576,
  "inherited_preprocessing_peak_plus_all_new_code_and_state": 273241520
}

````


File `review_final/meter-check.json`, SHA256`76350953308565edff154c86f31f208e4dcfab98437bc537c69c058e5688d0c6`.

````text
{
  "external_clock_required": false,
  "fixed_CV_charge": 1489431040983,
  "full_prefix_max": 40,
  "full_prefix_mean": 36,
  "histogram_input_to_cap": false,
  "kinds": {
    "C2": 640,
    "F7": 640,
    "G": 640,
    "callback": 640,
    "leaf": 8960,
    "nonfull": 8960
  },
  "program_sha256": "979ce9bb2d6505f8614aab65a56e8eff830fdb3d02cc36f5569d6321134bb718",
  "scope": "Independent literal record, prefix formula and controller-dataflow check; dynamic operand replay is separate.",
  "status": "PASS",
  "updates": 20480
}

````


File `review_final/mixed-windows.json`, SHA256`603279eb7a3a68304da58319b682d8b56d580d359d0428056f93631bd263b0cc`.

````text
{
  "all_640_literal_heads": true,
  "case_digest": "69619e4516a8a31c9286deb4ccbe0a9a2ef0b9e35d76386568059254646e6fe4",
  "cases": 81920,
  "cross_block_and_wrap_addresses": true,
  "headers": 16,
  "program_sha256": "979ce9bb2d6505f8614aab65a56e8eff830fdb3d02cc36f5569d6321134bb718",
  "scope": "Actual decoded head-prefix words against independently constructed separate-window tag membership. Count/payload/callback paths are checked by other gates.",
  "separate_window_lanes": true,
  "status": "PASS",
  "truth_combinations": {
    "00": 20480,
    "01": 20480,
    "10": 20480,
    "11": 20480
  }
}

````


File `review_final/integrity.json`, SHA256`a69cf6b32b7e12007e1ae87d177d484eb2a78c5b7ced7956c0a79dae7e901ecc`.

````text
{
  "status": "PASS",
  "zero_final_outcomes_at_freeze": true,
  "freeze_sha256": "e20b5c043a1fb821d0ff992cdc676831525d38be93ca47e4450e8485bf79db0d",
  "frozen_files": 557,
  "program_sha256": "979ce9bb2d6505f8614aab65a56e8eff830fdb3d02cc36f5569d6321134bb718",
  "binary_sha256": "36bcfae56cdb977a75a08f98f92e04b71b05110087ae1b9011441bd2f1c4ef86",
  "generated_source_sha256": "e4b358784e95303f4fb992a8ccd24e5f054e55bea63d09d844652b720c790df7",
  "runs": [
    {
      "label": "holdout_0",
      "nc": 17,
      "LU": 12,
      "CVs": 1,
      "queries": 4096,
      "stored": 131072,
      "events": 641,
      "fields": 8683,
      "claws": 21,
      "guard_suppressed": 642,
      "cgroup_peak": 275062784,
      "rss_peak": 270925824,
      "start_ns": 1792740339320909254,
      "end_ns": 1792740346093604637,
      "container_id": "efab5156d212003dcac79c81c629d24968a76ae20d3024d8c349d99ede093180",
      "raw_summary_sha256": "d02067778998665f23723e4c8e889c2a12b8f25ae53d66ce7912d421c26341af"
    },
    {
      "label": "holdout_1",
      "nc": 17,
      "LU": 12,
      "CVs": 1,
      "queries": 4096,
      "stored": 131072,
      "events": 596,
      "fields": 8122,
      "claws": 16,
      "guard_suppressed": 642,
      "cgroup_peak": 274567168,
      "rss_peak": 271056896,
      "start_ns": 1792740346254059659,
      "end_ns": 1792740353019869592,
      "container_id": "231ee97a9fa66f34e8f1b41a7c6822b24621f51e7619d259fa694e25bffd51bf",
      "raw_summary_sha256": "22ee9ee8adb649fb6ac7f3ca6b181f64dbf84bebfd4b0cc5cda0c25cc5d59b04"
    },
    {
      "label": "holdout_2",
      "nc": 17,
      "LU": 12,
      "CVs": 1,
      "queries": 4096,
      "stored": 131072,
      "events": 623,
      "fields": 8408,
      "claws": 23,
      "guard_suppressed": 642,
      "cgroup_peak": 273768448,
      "rss_peak": 271187968,
      "start_ns": 1792740353175093384,
      "end_ns": 1792740359950725860,
      "container_id": "ba8a87cd55988234fd0a5cf86f2807730db4fa171d2a4acff0f94f6b55243163",
      "raw_summary_sha256": "8fddca5a50b2bbb0adcde989c28087443cc43a9cc4a542384c5dcb338317c772"
    },
    {
      "label": "full_final",
      "nc": 27,
      "LU": 12,
      "CVs": 1,
      "queries": 4096,
      "stored": 58670746,
      "events": 8519,
      "fields": 8935,
      "claws": 8922,
      "guard_suppressed": 642,
      "cgroup_peak": 274296832,
      "rss_peak": 271187968,
      "start_ns": 1792740360096227844,
      "end_ns": 1792740396456237175,
      "container_id": "8cca7a36f0e88bb3d9e333d264bef6c43b1e0445d2dd3a930d2564a33fe269f2",
      "raw_summary_sha256": "91735cf67320ddecbc2a2c5da1461665c3118dcf68307c1a68891273a5b899b9"
    }
  ],
  "guarded_memory": 275128320,
  "sealed_v3_unchanged": true,
  "final_cases": 4,
  "final_retries": 0,
  "strict_order": true,
  "ELF_architecture": "amd64",
  "raw_coin_derivation": "PASS",
  "external_budget_supervisor": false,
  "budget_in_band": true,
  "provenance_limit": "A local archive cannot externally authenticate absence of deleted unrecorded trials. The immutable runner refuses retries and every retained record agrees."
}

````


File `review_final/full_final-outer.json`, SHA256`3fafbd19743c9197ef222f9d19e315658e573d229798e3f56468863670de4f91`.

````text
{
  "status": "PASS",
  "label": "full_final",
  "CVs": 1,
  "fresh_fixture_words": 4,
  "fixture_inputs_verified": true,
  "actual_cap_controller_and_success_stop": "PASS",
  "diagnostic_work_isolated": true,
  "cap_equality_and_next_rejection": false,
  "stopping_operations": 4,
  "steps": [
    {
      "CV": 0,
      "work": 7362301614,
      "counter": 1489431472897,
      "fixture_excluded": 29623
    }
  ],
  "event_records": 16,
  "fixed_phase_exits": {
    "NATIVE_INITIAL_HALT": "metered BR to OUTER_BUILD",
    "QUERY_HALT": "metered BR to OUTER_AFTER_QUERY"
  },
  "counter_widths": {
    "global_work": 128,
    "CV_index": 64,
    "aggregate_queries": 128
  },
  "ideal_coin_boundary": "Deterministic fixture bytes verify plumbing only; abstract RAND is an independent uniform 256-bit word and charged once per draw."
}

````


File `results/full_final/cv000000/summary.json`, SHA256`b029a92c88c45db42d46bc6166a898a2d923c0c147a11e28ec77f6910518065c`.

````text
{"status":"PASS","mode":"holdout","cv_index":0,"nc":27,"LU":12,"queries":4096,"stored":58670746,"errors":0,"events":8519,"fields":8935,"claws":8922,"invalids":13,"split_gathers":610,"field_max":46,"transform_min":548,"transform_max":548,"step_calls":2,"accepted_including_fixture":1,"ordinary_output":0,"guard_checks":644,"guard_suppressed":642,"table_bytes":268435712,"native_RAM_bytes":7488,"binary_bytes":906840,"bytecode_bytes":2322264,"rss_peak_bytes":271187968,"cgroup_memory_peak":274296832,"initial_new":2022,"online_new":12321,"fixture_new":29623,"new_records":41944,"native_program_records":42541,"trace_truncated":0,"op_counts":{"LOAD":8509358,"STORE":16777232,"ADD":35816325,"SUB":174575,"AND":117780240,"OR":138709922,"XOR":8529914,"NOT":900,"SHIFT":264345021,"COMPARE":17993768,"BRANCH":9618223,"IMMEDIATE":0,"UNCHANGED_LEGACY":6744033811,"RANDOM":0},"new_op_counts":{"LOAD":368,"STORE":266,"ADD":13095,"SUB":604,"AND":4750,"OR":1088,"XOR":2920,"NOT":0,"SHIFT":3957,"COMPARE":6799,"BRANCH":8093,"IMMEDIATE":0,"UNCHANGED_LEGACY":0,"RANDOM":4},"work_counter_hex":"00000000000000000000015ac908ab01","coin_words_consumed":4}

````


File `results/dev_small/summary.json`, SHA256`6073ae5c1d9aea228fc3e05a7cb789d16bdf956feaf78e0784462ba7831f3f03`.

````text
{"status":"PASS","mode":"bounded_outer","termination":"BOUND_EXHAUSTED","completed_CVs":1,"CV_limit":1,"algorithm_N_CV":12014587405061634,"nc":17,"LU":12,"queries":"4096","last_stored":131072,"table_bytes":268435712,"native_RAM_bytes":7488,"named_bank_words":335,"coin_words_consumed":4,"coin_interface":"deterministic_fixture_words","trace_enabled":1,"trace_truncated":0,"ordinary_output":0,"cgroup_memory_peak":275013632,"rss_peak_bytes":271056896,"work_counter_hex":"00000000000000000000015ac909b410","cpu_seconds":6.116586047,"wall_seconds":6.740962651}

````


File `results/dev_multi/summary.json`, SHA256`7aaca00c0cfecb296a830e836efe4998f661e6e17bf8440dbba51dbba6d1f3a0`.

````text
{"status":"PASS","mode":"bounded_outer","termination":"BOUND_EXHAUSTED","completed_CVs":3,"CV_limit":3,"algorithm_N_CV":12014587405061634,"nc":17,"LU":12,"queries":"12288","last_stored":131072,"table_bytes":268435712,"native_RAM_bytes":7488,"named_bank_words":335,"coin_words_consumed":12,"coin_interface":"deterministic_fixture_words","trace_enabled":1,"trace_truncated":0,"ordinary_output":0,"cgroup_memory_peak":274333696,"rss_peak_bytes":271056896,"work_counter_hex":"0000000000000000000004105b1b932d","cpu_seconds":18.354042756,"wall_seconds":19.958167116}

````


File `results/dev_small_r2/summary.json`, SHA256`c81377e75f7c94791716421fabe8d76bf4d62541ce15855622147fba82c81376`.

````text
{"status":"PASS","mode":"bounded_outer","termination":"BOUND_EXHAUSTED","completed_CVs":1,"CV_limit":1,"algorithm_N_CV":12014587405061634,"nc":17,"LU":12,"queries":"4096","last_stored":131072,"table_bytes":268435712,"native_RAM_bytes":7488,"named_bank_words":335,"coin_words_consumed":4,"coin_interface":"deterministic_fixture_words","trace_enabled":1,"trace_truncated":0,"ordinary_output":0,"cgroup_memory_peak":274735104,"rss_peak_bytes":271056896,"work_counter_hex":"00000000000000000000015ac906fa7c","cpu_seconds":5.935964505,"wall_seconds":6.451551763}

````


File `results/dev_multi_r2/summary.json`, SHA256`07a656585006e97820ab2bc0e80f9a877c8e259d56c4fc65b1a6b7e9ab9a284b`.

````text
{"status":"PASS","mode":"bounded_outer","termination":"BOUND_EXHAUSTED","completed_CVs":3,"CV_limit":3,"algorithm_N_CV":12014587405061634,"nc":17,"LU":12,"queries":"12288","last_stored":131072,"table_bytes":268435712,"native_RAM_bytes":7488,"named_bank_words":335,"coin_words_consumed":12,"coin_interface":"deterministic_fixture_words","trace_enabled":1,"trace_truncated":0,"ordinary_output":0,"cgroup_memory_peak":274300928,"rss_peak_bytes":271056896,"work_counter_hex":"0000000000000000000004105b1b1df2","cpu_seconds":17.235163765,"wall_seconds":18.754017381}

````


File `results/dev_cap/summary.json`, SHA256`146074ac00c0a8ab6afd0deac780d74a05d90d77891ecef83d02cc2bd6b159f9`.

````text
{"status":"PASS","mode":"bounded_outer","termination":"CAP_EXHAUSTED","completed_CVs":2,"CV_limit":3,"algorithm_N_CV":12014587405061634,"nc":17,"LU":12,"queries":"8192","last_stored":131072,"table_bytes":268435712,"native_RAM_bytes":7488,"named_bank_words":335,"coin_words_consumed":8,"coin_interface":"deterministic_fixture_words","trace_enabled":1,"trace_truncated":0,"ordinary_output":0,"cgroup_memory_peak":273768448,"rss_peak_bytes":270925824,"work_counter_hex":"0000000000000000000002b592157a69","cpu_seconds":11.664402756,"wall_seconds":12.679397458}

````


File `results/dev_stop/summary.json`, SHA256`d73568ac9444a917910514e51e35a8acd1d5b288e2015efc98bea7580617a418`.

````text
{"status":"PASS","mode":"bounded_outer","termination":"SYNTHETIC_SUCCESS_STOP","completed_CVs":2,"CV_limit":3,"algorithm_N_CV":12014587405061634,"nc":17,"LU":12,"queries":"8192","last_stored":131072,"table_bytes":268435712,"native_RAM_bytes":7488,"named_bank_words":335,"coin_words_consumed":8,"coin_interface":"deterministic_fixture_words","trace_enabled":1,"trace_truncated":0,"ordinary_output":0,"cgroup_memory_peak":274567168,"rss_peak_bytes":270925824,"work_counter_hex":"0000000000000000000002b592110b49","cpu_seconds":12.104712153,"wall_seconds":13.352383089}

````


File `results/dev_full/summary.json`, SHA256`3d377f495804546c8b43273a3c8e5f41a67ab651d27ebb312799ab142348b1a2`.

````text
{"status":"PASS","mode":"bounded_outer","termination":"BOUND_EXHAUSTED","completed_CVs":1,"CV_limit":1,"algorithm_N_CV":12014587405061634,"nc":27,"LU":12,"queries":"4096","last_stored":58670886,"table_bytes":268435712,"native_RAM_bytes":7488,"named_bank_words":335,"coin_words_consumed":4,"coin_interface":"deterministic_fixture_words","trace_enabled":1,"trace_truncated":0,"ordinary_output":0,"cgroup_memory_peak":274313216,"rss_peak_bytes":270794752,"work_counter_hex":"00000000000000000000015ac908b185","cpu_seconds":25.836733530,"wall_seconds":38.782036146}

````


File `results/dev_production/summary.json`, SHA256`111c436f0004810e8d58737337185f6b867eec550c6d4d8e068250c14217eb52`.

````text
{"status":"PASS","mode":"bounded_outer","termination":"BOUND_EXHAUSTED","completed_CVs":3,"CV_limit":3,"algorithm_N_CV":12014587405061634,"nc":17,"LU":12,"queries":"12288","last_stored":0,"table_bytes":268435712,"native_RAM_bytes":7488,"named_bank_words":335,"coin_words_consumed":12,"coin_interface":"deterministic_fixture_words","trace_enabled":0,"trace_truncated":0,"ordinary_output":0,"cgroup_memory_peak":274296832,"rss_peak_bytes":270794752,"work_counter_hex":"0000000000000000000004105b19cb01","cpu_seconds":16.627274646,"wall_seconds":16.661147683}

````


File `results/holdout_0/summary.json`, SHA256`d02067778998665f23723e4c8e889c2a12b8f25ae53d66ce7912d421c26341af`.

````text
{"status":"PASS","mode":"bounded_outer","termination":"BOUND_EXHAUSTED","completed_CVs":1,"CV_limit":1,"algorithm_N_CV":12014587405061634,"nc":17,"LU":12,"queries":"4096","last_stored":131072,"table_bytes":268435712,"native_RAM_bytes":7488,"named_bank_words":335,"coin_words_consumed":4,"coin_interface":"deterministic_fixture_words","trace_enabled":1,"trace_truncated":0,"ordinary_output":0,"cgroup_memory_peak":275062784,"rss_peak_bytes":270925824,"work_counter_hex":"00000000000000000000015ac908f78d","cpu_seconds":5.840095729,"wall_seconds":6.421786718}

````


File `results/holdout_1/summary.json`, SHA256`22ee9ee8adb649fb6ac7f3ca6b181f64dbf84bebfd4b0cc5cda0c25cc5d59b04`.

````text
{"status":"PASS","mode":"bounded_outer","termination":"BOUND_EXHAUSTED","completed_CVs":1,"CV_limit":1,"algorithm_N_CV":12014587405061634,"nc":17,"LU":12,"queries":"4096","last_stored":131072,"table_bytes":268435712,"native_RAM_bytes":7488,"named_bank_words":335,"coin_words_consumed":4,"coin_interface":"deterministic_fixture_words","trace_enabled":1,"trace_truncated":0,"ordinary_output":0,"cgroup_memory_peak":274567168,"rss_peak_bytes":271056896,"work_counter_hex":"00000000000000000000015ac908859d","cpu_seconds":5.852804784,"wall_seconds":6.440835118}

````


File `results/holdout_2/summary.json`, SHA256`8fddca5a50b2bbb0adcde989c28087443cc43a9cc4a542384c5dcb338317c772`.

````text
{"status":"PASS","mode":"bounded_outer","termination":"BOUND_EXHAUSTED","completed_CVs":1,"CV_limit":1,"algorithm_N_CV":12014587405061634,"nc":17,"LU":12,"queries":"4096","last_stored":131072,"table_bytes":268435712,"native_RAM_bytes":7488,"named_bank_words":335,"coin_words_consumed":4,"coin_interface":"deterministic_fixture_words","trace_enabled":1,"trace_truncated":0,"ordinary_output":0,"cgroup_memory_peak":273768448,"rss_peak_bytes":271187968,"work_counter_hex":"00000000000000000000015ac908bfbc","cpu_seconds":5.892833069,"wall_seconds":6.469001982}

````


File `results/full_final/summary.json`, SHA256`91735cf67320ddecbc2a2c5da1461665c3118dcf68307c1a68891273a5b899b9`.

````text
{"status":"PASS","mode":"bounded_outer","termination":"BOUND_EXHAUSTED","completed_CVs":1,"CV_limit":1,"algorithm_N_CV":12014587405061634,"nc":27,"LU":12,"queries":"4096","last_stored":58670746,"table_bytes":268435712,"native_RAM_bytes":7488,"named_bank_words":335,"coin_words_consumed":4,"coin_interface":"deterministic_fixture_words","trace_enabled":1,"trace_truncated":0,"ordinary_output":0,"cgroup_memory_peak":274296832,"rss_peak_bytes":271187968,"work_counter_hex":"00000000000000000000015ac908ab01","cpu_seconds":23.360056680,"wall_seconds":35.929296473}

````


File `results/dev_small/cgroup-final-peak`, SHA256`3624c9ffed6af67746631b792d96751551e795c5b07c7f477c094e9d1e35a3bb`.

````text
275013632

````


File `results/dev_multi/cgroup-final-peak`, SHA256`db38e228fd3efb967db99f55648675c8fa1afb3232f4ef63621b0cb34c989df3`.

````text
274333696

````


File `results/dev_small_r2/cgroup-final-peak`, SHA256`aa3948fe7b159cd89f4d733294f8f8acf512d10ab8cd9ef97a186243348df96e`.

````text
274735104

````


File `results/dev_multi_r2/cgroup-final-peak`, SHA256`37274a605ee84cf4a84fc631d5814aad09d22bbe393a40cca738e8600a936a9c`.

````text
274300928

````


File `results/dev_cap/cgroup-final-peak`, SHA256`81d131a504a18baed6de87d56383855d3246b17d487e1e4c36cf64db4fc154f8`.

````text
273768448

````


File `results/dev_stop/cgroup-final-peak`, SHA256`d70bb8e3fccd31829da423124cc7e48d385e4660a72607ecdbc3a673c171068e`.

````text
274567168

````


File `results/dev_full/cgroup-final-peak`, SHA256`427022cdf99339c81f4917f9058609b15a1a57a16ccf75f71149264c5713e749`.

````text
274313216

````


File `results/dev_production/cgroup-final-peak`, SHA256`43dcc8b7cb0e0114372d4bbdce1a7e5ff56689d3f0ec88c64155f70f3710ca43`.

````text
274296832

````


File `results/holdout_0/cgroup-final-peak`, SHA256`5b8135626e50f8d524de97f70fdc8010dc3266cbabcab35064e37eaa1135f2a5`.

````text
275062784

````


File `results/holdout_1/cgroup-final-peak`, SHA256`d70bb8e3fccd31829da423124cc7e48d385e4660a72607ecdbc3a673c171068e`.

````text
274567168

````


File `results/holdout_2/cgroup-final-peak`, SHA256`81d131a504a18baed6de87d56383855d3246b17d487e1e4c36cf64db4fc154f8`.

````text
273768448

````


File `results/full_final/cgroup-final-peak`, SHA256`43dcc8b7cb0e0114372d4bbdce1a7e5ff56689d3f0ec88c64155f70f3710ca43`.

````text
274296832

````

