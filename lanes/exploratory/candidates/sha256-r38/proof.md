# SHA-256 r38: wider bounded tabulation with a distribution-free collision-time argument

## 1. Claim, scope and attribution

This is a classical probabilistic, complete-message ordinary-collision construction for `sha256-r38-prefix-v1` under `collision-frontier-v5`. One trial has a hard bound on **all** charged computation, including randomized initialization, message generation, failed lookups, unsuccessful termination, checking and recovery:

- total charged computation at most `(109/100) * 2^128 < 2^128.1244` target-compression equivalents;
- success probability greater than `481427/1230000 - 4 * 2^-128`, hence greater than the claimed **0.39**;
- peak retained memory below **2^137 bytes**;
- preprocessing below **2^123** compression equivalents;
- no nonuniform advice and no heuristic premises.

This is an infeasible analytical RAM algorithm, not an executed collision search, timing measurement, differential characteristic, random-oracle argument or cryptanalytic security frontier. Every complete reduced target compression costs **one unit**, independent of implementation. No bitsliced-pricing interpretation is needed.

The organizer's r38 package in the starting checkout at `319f92d` gives a conservative generic bound of 132. Our sorting submission `f02ff88f-4ac6-4dbb-b1ef-de6691007bae` has official exploratory score 128.2303. Submission `8c92f07c-d0f0-4df5-a62e-e4076e02c4c1` replaces sorting by capped randomized tabulation and has official score 128.1376. Our immediate predecessor `1708c3d3-bf7a-4074-b695-4d3698a67400` retains that score but replaces a 1006-term probability calculation by a continuous CDF comparison and compact analytic inequalities. All three remain in manual-review status at preparation time.

This revision retains the sampling domain, distribution-free birthday argument, separate chaining, complete-compression pricing and analytic proof method. It expands the bucket range from n to 4n while keeping the two random tables at length n, reducing the expected unequal-key probes fourfold. Explicit 19n initialization and a 20n probability envelope support a smaller hard cap, `(109/100)n`, with K=n samples. The immediate predecessor is declared as a direct dependency; the sorting and original tabulation submissions are its earlier mathematical ancestry. Tabulation and separate chaining are standard algorithms, with the properties used here proved below.

`baseline_improved: sha256-r38-nominal-v2` is the mandatory nominal reference identifier, not an assertion of improvement on exponent 128. The new bound remains above 128. It improves the promoted conservative bound 132 and our earlier pending scores. It does not improve the much smaller unpromoted submissions by other solvers. Exploratory qualification, manual acceptance and promotion are separate outcomes.

## 2. Exact target and sampled messages

For each sample draw independent uniform 256-bit U and R; set `V = R AND (2^128-1)`. The message is `m = BE32(U) || BE16(V)`, where BE32 means exactly 32 big-endian bytes, not a 32-bit integer. Messages are iid uniform on a domain of size `D=2^384`. Repeated inputs are possible and their probability is subtracted, not assumed zero.

Each message pads to one 64-byte block: its 48 bytes, `0x80`, seven zero bytes and the 64-bit big-endian original bit length 384. As two big-endian 256-bit words the padded block is

`B0 = U`, `B1 = (V << 128) OR (0x80 << 120) OR 384`.

Let f be the fixed complete reduced hash on this domain. For every message it starts from the standard SHA-256 IV, uses the standard schedule and original constants, executes exactly rounds 0 through 37, then adds all eight working words to the incoming IV modulo 2^32. All eight resulting words are serialized in standard big-endian order into the full digest `Y=f(m)`. There is no changed IV, free-start state, omitted feed-forward, digest truncation or altered padding. Every evaluation is one complete selected compression costing 1.

A successful output is two different 48-byte messages with equal complete digests. The terminal routine compares both saved message words, evaluates both complete hashes afresh, compares all output bits, and returns the original bytes only if these conditions hold.

## 3. Explicit state and widened random hash family

Put `n=2^128`, `M=4n=2^130`, `C=2728` and `K=n`. Addresses, counters, budgets, messages, keys and pointers fit in 256-bit words; arithmetic does not wrap in the relevant ranges. The attack needs no multiplication primitive.

Allocate T0 and T1, each of length n, and Head of length M. Each table entry is an independent uniform **130-bit** value, obtained by its own uniform 256-bit draw masked by M-1. All Head entries are initialized to null pointer 0 by charged stores. The digit indices used to read the random tables remain 128 bits; table values and bucket indices are 130 bits. Enlarging Head does not enlarge either random table.

For a digest Y, set

`h(Y) = T0[Y AND (n-1)] XOR T1[Y >> 128]`.

The XOR is already a 130-bit index into Head, with no extra output mask. Table bases and offsets are added explicitly. Indexing is not a free primitive. Tables are independent of all message coins and retained in memory. Their generation/storage are charged randomized preprocessing, not nonuniform advice or seeded pseudorandom expansion.

For every fixed pair of distinct full digests Y,Y',

`Pr_T[h(Y)=h(Y')] = 1/M = 1/(4n)`.

If their low halves differ, one T0 entry occurs in only one hash value and is independent uniform conditional on all other entries appearing in that pair. Otherwise their high halves differ and one T1 entry has that property. The conditional XOR difference is uniform on 130-bit words. T0 and T1 entries are independent even at equal numerical indices. Stronger independence between pairs is neither asserted nor needed.

Nodes are four consecutive words `[Y,next,U,V]`. Head and next fields are direct addresses of Y. Nodes are allocated sequentially by advancing a pointer by four; the arena has at most K nodes. No index multiplication, resizing, zeroing of unused node storage or uncharged pointer derivation is required. A node is fully written before linking it. A successful final sample need not be inserted; stored messages remain available for recovery.

## 4. Concrete capped algorithm and invariants

Measure the cap in ordinary-operation units. Let

`B=floor((109/100)Cn)`, `F=2^20+2C`, `Remainder=B-19n-F`.

The startup budget reserves 19n for initialization and F for fixed setup, final abort handling, recovery and two terminal verification compressions. F also covers the last failed guard or outer-loop dispatch. Initialize T0, T1 and Head as described below. Set the sample counter to zero and the allocation pointer to the node arena.

Repeat until K samples have been processed:

1. If Remainder is less than C+224, halt with failure. Otherwise subtract C+224 before constructing the next message or calling f. This reserves its complete compression and all fixed per-sample work.
2. Sample U,V, form the exact padded block and evaluate Y. Compute h(Y), load its head, and traverse its chain.
3. Before each visited node, compare Remainder with 12. If insufficient, halt with failure. Otherwise subtract 12, load the full stored Y, and compare it to the current digest.
4. For unequal digests, load the next direct pointer and continue. For equal digests, load saved U,V and terminate the search: fail if the messages are identical; otherwise execute the reserved terminal verification and return the two messages if valid.
5. If the chain ends without a match, write `[Y,old_head,U,V]`, link Head to it, advance the allocation pointer by four, and increment the sample counter.

An empty bucket inserts immediately without a probe. Prior inserted digests are all distinct until the first repeated digest. Each reachable node is in exactly its stored digest's bucket, so an earlier equal digest is found unless a budget guard aborts. No reachable storage is overwritten or reused. Budget deductions are monotone and precede the corresponding work. There is no restart; the success probability belongs to this one bounded trial.

The final equal-key probe is also debited 12. It is not silently refunded. Recovery/output requires no table scan and uses the reserved fixed sample allowance and F. On failure the trial simply halts and discards its state; no expensive cleanup is performed or left as uncharged later attack work.

## 5. Charged operations and deterministic cap

Loads, stores, shifts, masks, logical operations, addition/subtraction, comparisons, conditional branches and independent random words all cost 1/C. Public counter arithmetic, addressing and control count. A primitive's destination register is its result, not an extra copy operation; any extra register copy can instead be an addition by zero within the allowances below. The selected compression, including schedule and feed-forward, is charged once, not decomposed and charged again.

**Initialization uses exactly 19 operations per loop iteration.** Fuse both random tables and the four n-word portions of Head into one loop of n iterations. Maintain six direct pointers: one each into T0 and T1, and four into Head starting at offsets 0,n,2n,3n. Per iteration perform:

- two independent random draws and two masks by M-1: 4;
- six stores (two table entries and four null heads): 6;
- six pointer additions by one: 6;
- one counter increment, one limit comparison and one conditional branch: 3.

Their sum is 19. The four Head portions are disjoint and exhaust Head; every head is explicitly initialized once. Fixed initial offsets 2n,3n can be obtained by additions. Constants, pointers, loop counter setup, an optional initial empty-loop guard and terminating dispatch are fixed work covered by F. The final comparison/branch are already included in the 19n count. Stores write supplied register values directly. The actual algorithm uses this loop, rather than assuming initialization at an unimplemented constant. Unused nodes are written on demand.

The unchanged conservative ordinary-work allowances per attempted sample, outside traversal, are:

| Work | Operations allowed |
| --- | ---: |
| Outer limit check, reservation, counters and sample guards | 24 |
| Two message random draws, mask, padded block construction, constants | 32 |
| Input/output transfers, 32-bit field extraction/packing and IV preparation | 48 |
| Two digit extractions, table addresses/loads, XOR, head address/load, initial null test | 20 |
| Sequential node addressing, four stores, head-link store, allocation bookkeeping | 32 |
| Equal-key handling, saved-message addresses/loads, message comparisons | 32 |
| Remaining sample control, failure/return dispatch and copies | 36 |
| **Fixed sample allowance** | **224** |

These are upper allowances, not a claim all rows are simultaneously exhausted. The algorithm uses the priced target-compression primitive with the packed two-word padded input B0,B1, the fixed standard IV and the full 256-bit output Y. The block's sixteen 32-bit SHA message words are distinct from the eight state/output words; their internal schedule, feed-forward and serialization are part of that complete priced compression, not unpriced extra attack work or a different narrow-field interface. Input/output loads, stores, IV transfers and any fixed extraction/packing at the boundary are covered by the 48 and neighboring allowances. The input block is not constructed with 64 separate byte stores. Increasing bucket indices to 130 bits changes no operation count in the 256-bit model. Every complete compression remains separately priced at C ordinary-operation equivalents.

A visited unequal node uses budget comparison/branch (2), subtraction (1), key load/comparison/branch (3), next-field address/load (2), and null comparison/branch (2): 10 operations. Reserve **12** to cover copies/bookkeeping. The final matching probe costs no more; equal-key recovery is in the fixed sample allowance and F.

Actual work is bounded by reservations. Failed-guard dispatch is in F and no future sample/probe then runs. Consequently every outcome, including overloaded chains and unsuccessful full trials, costs at most

`B/C <= (109/100)n`.

This is a deterministic cap on all computation, not just an expectation or successful-run bound. Terminal verification is inside it. There is no additional success amplification.

For probability analysis let U_k count unequal-key probes through detection if the first repeated digest occurs on sample k in the uncapped execution. Reservations through that detection are at most

`19n + F + (C+224)k + 12(U_k+1)`.

Since `F+12+1<n`, the sufficient condition

`12U_k <= C(109/100)n - 20n - (C+224)k`                 (1)

ensures all guards through detection pass. The 1 pays for B's floor. Monotone reservations imply that sufficient total budget through detection is sufficient at every earlier step. The sample limit passes for k<=K. The 20n envelope is deliberately larger than the actual 19n initialization reservation; the difference pays fixed/terminal work, the matching probe and the floor correction. No real work is removed from the cap.

## 6. Distribution-free birthday CDF and conditional lookup loss

Independent messages induce some fixed digest distribution `(p_1,...,p_N)` with `N=2^256=n^2`. Uniformity is not assumed. For k iid outputs, the all-different probability is `k! e_k(p)`, where e_k is the elementary symmetric polynomial.

For two coordinates a,b with fixed sum,

`e_k = ab e_(k-2)(rest) + (a+b)e_(k-1)(rest) + e_k(rest)`.

Coefficients are nonnegative. Averaging a,b cannot decrease e_k. Repeatedly averaging the largest/smallest coordinates converges to the uniform vector: squared deviations decrease by half the squared gap each step, and a nonzero limiting range would force indefinitely many fixed positive decreases. Continuity therefore shows uniform probabilities maximize e_k, including at vectors with zero coordinates. For k<=N,

`Pr(all outputs distinct) <= (N)_k/N^k <= exp(-k(k-1)/(2N))`.

The last inequality uses `1-u<=exp(-u)` in each factor. Let tau be the first repeated output in a counterfactual stream of K messages, infinity if there is none. Then

`Pr(tau<=k) >= 1-exp(-k(k-1)/(2n^2))`.                (2)

The stream can be conceptually drawn in advance independently of T0,T1. Actual execution draws only used messages: this is an analysis coupling, not executed free sampling.

Condition on any fixed message stream with tau=k. Prior output keys are distinct. Each unequal probe pairs two sample indices with unequal full digests and equal bucket hashes; every unordered index pair is probed at most once before termination. The final digest can repeat a prior digest, so some different index pairs can involve the same digest pair, and are counted separately. Pairwise expectation and Section 3 give

`E_T[U_k | stream,tau=k] <= k(k-1)/(2M) = k(k-1)/(8n)`.

No probe independence or deterministic chain-length bound is required. Markov's inequality with (1), using k(k-1)<=k^2 and x=k/n, gives a stream-conditional upper bound on cap failure:

`q(x) = (3/2)x^2 / (2728*(109/100)-20-2952x)`.

For `0<x<=1` the denominator is positive, q is increasing and

`q(1)=75/76<1`.

Thus detection at each stream's own collision time has probability at least `1-q(k/n)` over independent table coins. Tau depends on message coins only. A single subtraction `Pr(tau<=K)-q(K/n)` is not used: earlier collisions have much smaller lookup loss.

## 7. Decreasing-weight CDF comparison and finite-n corrections

Put `a=b=K/n=1`, `w(x)=1-q(x)` on [0,1] and `F_cdf(x)=Pr(tau/n<=x)`. The weights are positive and decreasing with w(0)=1. Averaging the conditional detection probabilities gives

`Pr(detect output repetition within cap) >= integral_[0,1] w(x) dF_cdf(x)`.

For k=floor(nx) and 0<=x<=1,

`0 <= x^2/2-k(k-1)/(2n^2) <= 3x/(2n) < 2/n`.

Writing k=nx-delta with 0<=delta<1 gives the difference `(2delta+1)x/(2n)-delta(delta+1)/(2n^2)`. Nonnegativity follows from k<=nx and k(k-1)<=k^2, also covering k=0. Since exp(-z) is 1-Lipschitz for z>=0, equation (2) implies

`F_cdf(x) >= G(x)-2/n`, where `G(x)=1-exp(-x^2/2)`.

Lower CDF bounds cannot be subtracted to obtain lower bin masses. Instead Stieltjes integration by parts, equivalently summation by parts over F_cdf's finite jumps, yields

`integral_[0,1] w dF_cdf = w(1)F_cdf(1) + integral_0^1 (-w')F_cdf dx`.

F_cdf(0)=G(0)=0. All coefficients are nonnegative and their total is `w(1)+integral_0^1(-w')dx=w(0)=1`. Substituting the pointwise bound therefore loses at most 2/n. Define

`I = integral_0^1 (1-q(x)) x exp(-x^2/2) dx`.

The output-repeat detection probability is at least I-2/n. There is no endpoint-floor correction since K=n exactly; retaining a looser I-3/n bound is harmless. Among K conceptual messages the chance of any repeated input is at most

`K(K-1)/(2D) < 1/(2n) < 1/n`, since `D=n^3`.

Outside that event every repeated output belongs to different messages. Subtracting it, with no independence assumption relative to output repeats, proves the conservative bound

`Pr(ordinary collision returned) >= I-4/n`.           (3)

Verification is deterministic and uses the exact target. No random-looking SHA-256-output premise is involved. Only ideal independent algorithmic coins supplied by the model are required. The continuous integral is an analytic lower bound on this finite algorithm, not a continuous-time attack.

## 8. Compact rational success certificate

Write

`r=36919/36900`, so `q(x)=x^2/[1968(r-x)]`,

`I=G(1)-J`, `J=(1/1968) integral_0^1 x^3 exp(-x^2/2)/(r-x) dx`.

**Endpoint CDF.** The six-term lower alternating Taylor bound gives

`G(1) > sum_(ell=1)^6 (-1)^(ell+1)(1/2)^ell/ell! = 18131/46080 > 1967/5000`.

The final exact positive remainder is

`18131/46080-1967/5000 = 391/5760000 > 0`.             (4)

**Lookup-loss integral.** For x>=0, `exp(-x^2/2)<=1-x^2/2+x^4/8`. Put `P(x)=x^3-x^5/2+x^7/8`. Polynomial division gives

`1968J <= integral_0^1 P(x)/(r-x) dx = P(r)L-D`,

`L=ln(r/(r-1))`, `D=integral_0^1 [P(r)-P(x)]/(r-x) dx`.

Three elementary bounds suffice:

1. **P(r)<16/25.** The derivative `P'(x)=(x^2/8)(24-20x^2+7x^4)` is nonnegative because the quadratic in x^2 has discriminant 400-672<0 and positive leading coefficient. Since r<101/100,

   `P(r)<P(101/100)=511050315170701/800000000000000<16/25`.

   The last cross-product difference is `512000000000000-511050315170701=949684829299>0`.                   (5)

2. **D>1.** P is convex for x>=0: `P''(x)=(x/4)(24-40x^2+21x^4)` is nonnegative since the quadratic has discriminant 1600-2016<0. For 0<=x<1<r, the secant comparison gives

   `[P(r)-P(x)]/(r-x) >= [P(1)-P(x)]/(1-x)`.

   This applies on the whole interval, with the endpoint interpreted by continuity. Dividing by 1-x and integrating gives

   `D >= (1+1/2+1/3) - (1/2)(1+1/2+1/3+1/4+1/5)`

   `     + (1/8)(1+1/2+1/3+1/4+1/5+1/6+1/7)`

   `  = 3413/3360 > 1`.                              (6)

3. **L<77/10.** Exactly `r-1=19/36900` and `r/(r-1)=36919/19<2048=2^11`, since 36919<38912. The positive atanh series and a geometric tail bound give

   `ln(2)=2 sum_(j>=0) 1/[(2j+1)3^(2j+1)]`

   ` < 2[1/3+(1/3)sum_(j>=1)3^(-2j-1)] = 2(1/3+1/72)=25/36`.

   Consequently `L<11ln(2)<275/36<77/10`.             (7)

Combining (5)-(7),

`J < [(16/25)(77/10)-1]/1968 = 491/246000`.

Thus (4) proves

`I > 1967/5000-491/246000 = 481427/1230000`

`  = 39/100 + 1727/1230000`.                          (8)

Since `4/n<1727/1230000` for n=2^128, equations (3) and (8) establish success greater than **0.39** at the smaller hard cap. These are self-contained analytic inequalities, not numerical quadrature, an executed finite experiment or a machine-checked formal proof. A yet smaller cap is not asserted merely because it is close to this one.

## 9. Scalar, preprocessing, memory and evidence limits

The hard cap gives `T<=(109/100)n`, so

`log2(T) <= 128+log2(109/100) = 128.1243281350... < 128.1244`.

An exact certificate avoids reliance on this decimal. A five-term upper alternating bound for ln(109/100) and a four-term lower positive atanh bound for ln(2) are

`U=9/100-(9/100)^2/2+(9/100)^3/3-(9/100)^4/4+(9/100)^5/5 = 1077222231/12500000000`,

`V=2(1/3+1/81+1/1215+1/15309)=53056/76545`.

The exact comparison is

`(311/2500)V-U = 9220865621/191362500000000 > 0`.

Hence `ln(109/100)/ln(2)<311/2500=0.1244`, proving the submitted exponent. C and the price of every compression/ordinary primitive are unchanged.

Randomized preprocessing costs at most `(19n+F)/2728<2^123`, conservatively assigning all fixed work to it. This time is already included in T. There is zero nonuniform advice. The fixed rational description checks do not construct a collision or target-dependent advice; if counted as setup computation their fixed instruction count is dominated by F.

T0,T1 use 2n words, Head 4n words and the node arena at most 4K=4n words. Bulk retained memory is

`32*(2n+4n+4n)=320n bytes`.

All 130-bit entries occupy full 256-bit words; no packing discount is assumed. Less than 2^20 bytes of code, constants, stack, working block and verification/output state keeps the total below `512n=2^137` bytes. Table randomness and both message words per node are included. Sample counters need 129 bits, budgets at most 140 bits, and word addresses at most 132 bits, all fitting the model. The higher memory bound is explicit; enormous memory is permitted as a reported metric, not claimed practical hardware.

There are no differential certificates, declared experiments, target-output extrapolations or heuristic premises. The certificate manifest remains empty and valid. Mechanical intake validates package consistency, not this probability theorem, AI qualification, human acceptance or promotion. The substantive change from the immediate predecessor is a larger explicitly initialized bucket array and a smaller re-proved hard cap; the 224-operation sample and 12-operation probe allowances are unchanged. No work is repriced or hidden in unreported memory.
