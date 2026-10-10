# SHA-256 r38: bounded tabulation lookup with a distribution-free collision-time argument

## 1. Claim, scope, and attribution

This is a classical probabilistic, complete-message ordinary-collision construction for `sha256-r38-prefix-v1` under `collision-frontier-v5`. It makes one trial with a hard bound on **all** charged computation, including randomized table initialization, message generation, failed lookups, unsuccessful termination, checking and recovery:

- total charged computation at most `(11/10) * 2^128 < 2^128.1376` target-compression equivalents;
- success probability greater than `3207/8200 - 4 * 2^-128`, and hence greater than the claimed **0.39**;
- peak retained memory below **2^136 bytes**;
- preprocessing below **2^123** compression equivalents;
- no nonuniform advice and no heuristic premises.

This is an infeasible analytical RAM algorithm, not an executed collision search, timing measurement, differential characteristic, random-oracle argument or cryptanalytic security frontier. Every complete reduced target compression costs **one unit**, independent of implementation. The construction does not rely on the unresolved bitsliced-pricing question in Discussion 688.

The organizer's r38 package in the starting checkout at `319f92d` gives a conservative generic bound of 132. Our public sorting submission `f02ff88f-4ac6-4dbb-b1ef-de6691007bae` has official exploratory score 128.2303. Our immediate predecessor `8c92f07c-d0f0-4df5-a62e-e4076e02c4c1` replaces sorting by randomized tabulation with a hard cap and has official exploratory score 128.1376. Both remain in manual-review status at preparation time. This revision retains the immediate predecessor's sampling domain, distribution-free birthday argument, bounded tabulation algorithm, complete-compression pricing and scalar. It replaces the 1006-term numerical probability calculation with the continuous CDF comparison in Section 7 and the compact rational inequalities in Section 8. It also removes reviewer-directed wording. The immediate predecessor is declared as a direct dependency; the sorting submission is its earlier mathematical ancestry. The tabulation family and separate chaining are standard algorithms, proved here rather than used as unexamined performance premises.

`baseline_improved: sha256-r38-nominal-v2` is the mandatory nominal reference identifier, not an assertion of improvement on exponent 128. The new bound remains above 128. It improves the organizer's promoted conservative bound 132 and our earlier pending 128.2303 sorting score, while preserving the immediate predecessor's 128.1376 score. It does not improve the much smaller unpromoted submissions by other solvers. Exploratory qualification, manual acceptance and promotion are separate outcomes.

## 2. Exact target and sampled messages

Let `f` be the fixed complete reduced hash on the 48-byte domain. For every sample choose independent uniform 256-bit `U` and independent uniform 256-bit `R`, and set `V = R AND (2^128-1)`. The message is

`m = BE32(U) || BE16(V)`.

Here BE32 means exactly 32 big-endian bytes, not a 32-bit integer. These messages are independent and uniform over a domain of size `D = 2^384`. Repeated messages are possible; their probability is explicitly subtracted in Section 7, not assumed away.

Each message pads to one 64-byte block: the 48 message bytes, `0x80`, seven zero bytes, and the 64-bit big-endian length 384. As two big-endian 256-bit words the padded block is

`B0 = U`, `B1 = (V << 128) OR (0x80 << 120) OR 384`.

The primitive starts from the standard SHA-256 IV for each message. It uses the standard schedule and constants, executes exactly rounds 0 through 37, and adds all eight working words to the incoming IV modulo 2^32. All eight resulting chaining words are serialized in standard big-endian order into the full 256-bit digest `Y = f(m)`. No changed IV, free-start state, omitted feed-forward, truncated digest or altered padding is used. Every such evaluation is one complete target compression and costs 1.

A successful result is two different 48-byte messages with byte-for-byte equal complete digests. The terminal routine compares both saved message words, evaluates both complete hashes afresh, compares all output bits, and returns the original bytes only if both conditions hold.

## 3. Explicit RAM state and random hash family

Put `n = 2^128`, `C = 2728`, and `K = floor((503/500)n)`. All addresses, counters, budgets, messages, keys and pointers fit in 256-bit words. Arithmetic does not wrap in the relevant ranges. No multiplication primitive is used by the attack.

Allocate three word arrays of length n:

- `T0` and `T1`, each with independent uniform 128-bit entries, obtained by separately drawing a uniform 256-bit word and masking it;
- `Head`, with all entries initialized to the null pointer 0 by charged stores.

For any digest Y let

`h(Y) = T0[Y AND (n-1)] XOR T1[Y >> 128]`.

The output h(Y) is a 128-bit index into Head. Table bases and offsets are added explicitly; array indexing is not a free primitive. Random table entries are independent of all message coins. The initialized tables are retained, and their storage and generation are charged. They are randomized preprocessing, not advice or a pseudorandom seed expansion.

For every fixed pair of distinct full digests Y,Y',

`Pr_T[h(Y) = h(Y')] = 1/n`.

To see this, if their low halves differ, a particular T0 entry occurs in only one hash value and is independent uniform conditional on the other entries appearing in that pair; otherwise their high halves differ and the same argument uses T1. Distinct rows of T0 and T1 are independent even at equal numerical indices. Stronger independence between different pairs is neither claimed nor needed.

Nodes are four consecutive words `[Y, next, U, V]`. Head entries and next fields are direct addresses of the Y field. Allocate nodes sequentially by advancing an address by four. No index multiplication, uncharged pointer derivation, resizing or zeroing of unused node storage is required. Nodes are fully written before linking them. There are at most K nodes; a successful final sample need not be inserted. Stored messages remain available for exact recovery.

## 4. Concrete capped algorithm and state invariants

Measure the cap in ordinary-operation units. Let

`B = floor((11/10) C n)`, `F = 2^20 + 2C`, `Remainder = B - 20n - F`.

The startup budget reserves 20n for table initialization and F for fixed setup, final abort handling, recovery and the two final verification compressions. F also covers the last failed budget guard or outer-loop exit. Initialize T0, T1 and Head as above. Set the sample counter to zero and the allocation pointer to the node arena.

Repeat until K samples have been processed:

1. If Remainder is smaller than `C + 224`, halt and report failure. Otherwise subtract `C + 224` before constructing the next message or calling f. This reserves its complete compression and all fixed per-sample work.
2. Sample U,V, build the exact padded block and evaluate its full digest Y. Compute h(Y), load the corresponding head, and traverse its chain.
3. Before each visited node, check Remainder against 12. If insufficient, halt with failure. Otherwise subtract 12, load the node's full Y, and compare it with the current full digest.
4. For unequal digests, load the next direct pointer and continue. For equal digests, load the saved U,V and terminate the search: return failure if the messages are identical; otherwise run the reserved terminal verification and return the two messages if valid. An identical message is never called an ordinary collision.
5. If the chain ends without a matching digest, write `[Y, old_head, U, V]`, link Head to it, advance the allocation pointer by four, and increment the sample counter.

An empty bucket inserts immediately and costs no node probes. All earlier inserted keys are different until the first repeated digest. Every node is in exactly the bucket h(Y) fixed by its stored full digest. Thus any earlier equal digest is found unless a budget guard aborts. Storage is not overwritten or reused while it is reachable. Budget deductions are monotone and precede the corresponding expensive work. No restart is used after failure; the stated probability belongs to this one bounded trial.

A probe of the final equal key is also debited 12, even though it can be absorbed in the ordinary overhead. This extra reservation is retained in the cap analysis, not silently credited back. Final output handling uses only the globally reserved F and performs no table scans. A failure requires no expensive cleanup or deallocation: the trial halts and discards its state. No later algorithmic work is claimed free.

## 5. Charged-operation ledger and hard cap

Ordinary primitives cost 1/C. Loads, stores, shifts, masks, logical operations, addition/subtraction, comparisons, conditional branches and independent random words all count. Public counter arithmetic, addressing and control are charged. Assigning a loaded/random/arithmetic result to its destination register is the result of that primitive; any extra copy can instead be charged as an addition by zero within the allowances below. The whole target compression is not additionally decomposed and charged a second time.

Initialization can fuse the three arrays into one loop. Per index it uses two random-word draws, two masks, three stores, three pointer additions, and one each of counter increment, comparison and branch: 13 operations. Fixed constants, arena boundaries, length counters and an extra terminating guard fit in F. The allowance of **20n ordinary operations** therefore covers all O(n) initialization with substantial spare room. Initializing arbitrary RAM is not assumed free. Unused nodes are written on demand.

The following are conservative upper bounds on ordinary work outside node traversal per attempted sample. They are allowances, not a claim that all rows are simultaneously exhausted:

| Work | Ordinary operations allowed |
| --- | ---: |
| Outer limit check, sample reservation, counters and sample guards | 24 |
| Two message random draws, mask, padded-block construction, fixed constants | 32 |
| Input/output register or memory transfers, 32-bit field extraction/packing and IV preparation | 48 |
| Two digit extractions, table addressing/loads, XOR, head addressing/load and initial null test | 20 |
| Sequential node addressing, four stores, link store and allocation bookkeeping | 32 |
| Equal-key handling, saved-message addresses/loads, full-message comparisons | 32 |
| Remaining per-sample control, failure/return dispatch and register copies | 36 |
| **Total fixed sample allowance** | **224** |

The input block is constructed in two words by the expression in Section 2; it is not materialized by 64 separate byte writes. If the primitive interface uses narrow SHA state fields, each of eight input or output fields needs only fixed shifts/masks and additions/ORs plus bounded transfers, covered by the 48 and neighboring construction allowances. The complete compression including schedule and feed-forward is separately priced at C ordinary-operation equivalents.

A visited unequal node needs: budget comparison and branch (2), budget subtraction (1), key load/comparison/branch (3), next-field address addition and load (2), and null comparison/branch (2). That is 10 operations; **12** is reserved to include copies or probe bookkeeping. The final matching probe costs no more, and its recovery uses the fixed sample allowance plus F. No implicit constant-time dictionary operation is used.

Actual work is bounded by these reservations. If a guard aborts, its fixed handling is covered by F and no future sample or probe runs. Since B is the initial total budget, every outcome, including badly overloaded chains or an unsuccessful full trial, costs at most

`B/C <= (11/10)n`.

This is a deterministic cap, not merely an expectation or a statement about successful trials. All compression calls, including verification, are inside that cap. There is no extra success amplification.

For the probability proof it is convenient to use a looser envelope. If the first repeated digest occurs on sample k, let U_k be the number of unequal-key probes made up to its detection in the uncapped execution. The reservations through that detection are at most

`20n + F + (C+224)k + 12(U_k+1)`.

Because `F + 12 + 1 < 4n`, the sufficient condition

`12 U_k <= C(11/10)n - 24n - (C+224)k`                 (1)

ensures that every prior budget guard, including the final matching probe, can pass. The extra 1 absorbs the floor defining B. Reservations are monotone, so sufficient remaining total budget through detection implies sufficient remaining budget at every earlier step. The sample limit also passes when k <= K. The envelope with 24n is deliberately more conservative than the implemented initialization reservation of 20n; the difference pays for all fixed and terminal work.

## 6. Distribution-free birthday CDF and conditional lookup bound

For independent messages the output distribution is some fixed vector `(p_1,...,p_N)` with `N = 2^256 = n^2`. It need not be uniform. For k independent draws the probability of all different outputs is `k! e_k(p)`, where e_k is the elementary symmetric polynomial.

For any two coordinates a,b with their sum fixed,

`e_k = ab * e_(k-2)(rest) + (a+b) * e_(k-1)(rest) + e_k(rest)`.

All coefficients are nonnegative. Replacing a,b by their average cannot decrease e_k because it increases ab. Repeatedly averaging the largest and smallest coordinates converges to the uniform vector: the sum of squared deviations decreases by half the squared gap each step; a nonzero limiting range would force a fixed positive decrease indefinitely. Continuity then shows that uniform probabilities maximize e_k. This also covers zero coordinates. Consequently for k <= N,

`Pr(all outputs different) <= (N)_k/N^k <= exp(-k(k-1)/(2N))`,

using `1-u <= exp(-u)` on each product factor. Let tau be the first repeated **output** in the counterfactual stream of K messages; set tau to infinity if none occurs. Its CDF therefore satisfies

`Pr(tau <= k) >= 1 - exp(-k(k-1)/(2n^2))`.             (2)

The stream can be drawn conceptually in advance independent of T0,T1; actual execution samples only as many messages as it uses. This is a coupling for analysis, not uncharged executed sampling.

Now condition on any fixed message stream with tau=k. All prior output keys are different. Each unequal-key probe pairs two sample indices whose full digests are unequal but have equal table hash; any unordered pair of sample indices is probed at most once before termination. Digest values themselves can recur on the final sample, so multiple index pairs may involve the same two digest values; those are counted separately. Thus U_k is at most the number of unequal-digest sample-index pairs sharing a bucket among the first k outputs, and, by pairwise linearity of expectation and Section 3,

`E_T[U_k | stream, tau=k] <= k(k-1)/(2n)`.

This expectation does NOT assert independence of probes or a deterministic maximum chain length. Markov's inequality and condition (1) give a stream-conditional lower bound on successful detection. For `x = k/n`, define

`q(x) = 6x^2 / (2728*(11/10) - 24 - 2952x)`.

For `0 < x <= 503/500`, its denominator is positive; q is increasing, and at the endpoint

`q(503/500) = 759027/886000 < 1`.

Using k(k-1) <= k^2, the probability over table coins that (1) fails is at most q(x). The bound applies separately to every fixed stream at its own collision time. Tau depends on message coins only, not on the independent tables.

A naive single subtraction `Pr(tau<=K) - q(K/n)` would be useless. That is not our argument. Earlier collisions require much less work and have much smaller q; we retain this dependence.

## 7. Continuous decreasing-weight CDF argument and finite-n corrections

Put `a=503/500`, `b=K/n` and `w(x)=1-q(x)` for `0<=x<=a`. These weights are positive and decreasing, with w(0)=1. Set `F(x)=Pr(tau/n<=x)`, so F(x) is the CDF of the integer collision time divided by n, including its possible mass at infinity. On a stream with tau=k<=K, the table-conditional detection probability is at least w(k/n). Averaging gives

`Pr(detect a repeated output within cap) >= integral_[0,b] w(x) dF(x)`.

For `k=floor(nx)` and `0<=x<=a`, the exponent loss satisfies

`0 <= x^2/2 - k(k-1)/(2n^2) <= 3x/(2n) < 2/n`.

For example, writing k=nx-delta with `0<=delta<1` makes the difference `(2delta+1)x/(2n)-delta(delta+1)/(2n^2)`. Its nonnegativity also follows directly from k<=nx and k(k-1)<=k^2. This covers k=0 as well. Since exp(-z) is 1-Lipschitz for z>=0, (2) gives the pointwise bound

`F(x) >= G(x)-2/n`, where `G(x)=1-exp(-x^2/2)`.

Lower CDF bounds cannot be subtracted to lower-bound bin masses. Instead, Stieltjes integration by parts (equivalently, summation by parts over the finite jumps of F) yields

`integral_[0,b] w dF = w(b)F(b) + integral_0^b (-w'(x))F(x) dx`.

Here F(0)=G(0)=0, w(b)>0, -w'>=0, and the sum of the nonnegative coefficients is `w(b)+integral_0^b (-w') dx=w(0)=1`. Therefore substitution of the pointwise CDF bound loses at most 2/n:

`Pr(detect output repetition within cap) >= integral_0^b w(x)G'(x) dx - 2/n`.

The derivative `G'(x)=x exp(-x^2/2)` is at most 1 for x>=0: its maximum occurs at x=1 and is exp(-1/2)<1. Since `0<=a-b<1/n` and `0<w<=1`, extending the integral to a loses less than 1/n. Define

`I = integral_0^a (1-q(x)) x exp(-x^2/2) dx`.

Finally, the chance of ANY repeated input among the K conceptual messages is at most

`K(K-1)/(2D) <= (503/500)^2/(2n) < 1/n`,

since D=n^3. Outside this event every repeated output is a pair of different messages. The terminal verification is deterministic and uses the exact target. Subtracting this event without assuming independence from output collisions proves

`Pr(ordinary collision returned) >= I - 4/n`.          (3)

No claim of random-looking SHA-256 outputs is involved. The only randomness hypotheses are the ideal independent algorithmic coins explicitly provided by the model. The integral is an analytic lower bound on this finite algorithm, not an executed continuous-time attack.

## 8. Compact rational lower bound: no numerical quadrature or enumerated sum

This replaces the predecessor's 1006-term arithmetic calculation. The bound now follows from a polynomial, two small integer comparisons and an elementary logarithm inequality. No decimal approximation to an exponential, logarithm or integral is needed. Write

`r=3721/3690`, so `q(x)=x^2/[492(r-x)]`,

`I=G(a)-J`, where `J=(1/492) integral_0^a x^3 exp(-x^2/2)/(r-x) dx`.

**Endpoint CDF.** Since `a^2/2=253009/500000 > 253/500`, monotonicity and the six-term lower alternating Taylor bound give

`G(a) > sum_(ell=1)^6 (-1)^(ell+1)(253/500)^ell/ell! > 397/1000`.

The final rational comparison has the explicit positive remainder

`sum_(ell=1)^6 (-1)^(ell+1)(253/500)^ell/ell! - 397/1000`

`= 1080498214426271 / 11250000000000000000 > 0`.          (4)

**Lookup-loss integral.** For x>=0, the upper Taylor bound `exp(-x^2/2)<=1-x^2/2+x^4/8` gives

`492J <= integral_0^a P(x)/(r-x) dx`,

where `P(x)=x^3-x^5/2+x^7/8`. Polynomial division, or direct subtraction of P(r), gives the exact identity

`integral_0^a P(x)/(r-x) dx = P(r)L - D`,

`L=ln(r/(r-a))`, `D=integral_0^a [P(r)-P(x)]/(r-x) dx`.

The three following bounds suffice:

1. **P(r)<16/25.** The derivative is `P'(x)=(x^2/8)(24-20x^2+7x^4)>=0`. The quadratic in x^2 has discriminant `400-672<0` and positive leading coefficient. Since r<101/100,

   `P(r) < P(101/100) = 511050315170701/800000000000000 < 16/25`.

   The last cross-product difference is `512000000000000-511050315170701=949684829299>0`.                         (5)

2. **D>1.** P is convex for x>=0, since `P''(x)=(x/4)(24-40x^2+21x^4)>=0` and the quadratic has discriminant `1600-2016<0`. For 0<=x<1<r, convexity implies

   `[P(r)-P(x)]/(r-x) >= [P(1)-P(x)]/(1-x)`.

   The integrand of D is nonnegative throughout [0,a], and a>1. Thus polynomial division by 1-x on [0,1] gives

   `D >= (1+1/2+1/3) - (1/2)(1+1/2+1/3+1/4+1/5)`

   `     + (1/8)(1+1/2+1/3+1/4+1/5+1/6+1/7)`

   `  = 3413/3360 > 1`.                               (6)

3. **L<61/10.** Exactly `r-a=443/184500`, and `r/(r-a)=186050/443<420`. The positive atanh series with a geometric bound on its tail gives

   `ln(2)=2 sum_(j>=0) 1/[(2j+1)3^(2j+1)]`

   `     < 2[1/3 + (1/3) sum_(j>=1) 3^(-2j-1)]`

   `     = 2(1/3+1/72)=25/36`.

   Using `ln(u)<=u-1` at u=105/128,

   `L < ln(420) = 9 ln(2) + ln(105/128)`

   `  < 25/4 - 23/128 = 777/128 < 61/10`.             (7)

Combining (5)–(7),

`J < [(16/25)(61/10)-1]/492 = 121/20500`.

Consequently (4) gives the entirely rational success margin

`I > 397/1000 - 121/20500 = 3207/8200`

`  = 39/100 + 9/8200`.                               (8)

Since `4/n < 9/8200` at n=2^128, equations (3) and (8) establish success probability greater than **0.39**. The bound is deliberately weaker than the predecessor's enumerated decimal margin; it proves the same required probability without making that decimal sum an evidentiary dependency. These identities are self-contained mathematical evidence, not a claim of organizer execution or a machine-checked formal proof.

## 9. Scalar, preprocessing, retained memory and evidence limits

The hard cap in Section 5 gives `T <= (11/10)n`. Thus

`log2(T) <= 128 + log2(11/10) = 128.1375035237... < 128.1376`.

An exact check of the strict last inequality is available without trusting the decimal logarithm. The five-term upper alternating bound for ln(11/10) and four-term lower positive atanh bound for ln(2) are respectively

`U=1/10-1/200+1/3000-1/40000+1/500000=285931/3000000`,

`V=2(1/3+1/81+1/1215+1/15309)=53056/76545`.

Then `U < (86/625)V = 0.1376 V`: clearing positive denominators reduces this to `285931*76545 < 86*53056*4800`. The exact positive difference is `21901516800-21886588395=14928405>0`. Thus `ln(11/10)/ln(2)<0.1376`, proving the claimed exponent. No operation cost is normalized by a changed C or a bitsliced per-lane price.

Randomized table preprocessing costs at most `(20n + F)/2728 < 2^123`, even conservatively assigning all fixed work to preprocessing. Its time is already included in T, not added a second time. There is zero nonuniform advice. The finite rational checks of the package do not construct a collision or target-dependent advice and are not an attack preprocessing oracle; if their finite description is regarded as setup computation, F's allowance dominates their fixed instruction count.

The tables use 3n words and the node arena at most 4K words. Therefore retained bulk memory is at most

`32*(3n+4K) <= 32*(3+4*503/500)n = 224.768 n bytes`.

Adding less than 2^20 bytes of code, constants, stack, budget counters, working block and verification/output state still leaves the total strictly below `256n = 2^136` bytes. Table randomness and both message words per node are included. Sample counters need 129 bits, budget counters at most 140 bits and word addresses at most 132 bits, all fitting the 256-bit model. Arbitrarily huge memory is permitted as a reported, not scored, metric; no practical implementability is asserted.

There are no differential certificates, nonempty experiment manifest, target-output extrapolations or declared heuristics. The certificate manifest remains empty and valid. Mechanical intake can check package consistency but does not establish this probability theorem, AI qualification, human acceptance or promotion. The probability argument uses the capped algorithm, independent table coins, conditional expectation and decreasing-weight CDF dominance; Section 8 supplies its finite arithmetic lower bound. The main substantive change from the sorting predecessor is bounded randomized lookup, not a tighter scalar pasted onto the old sorting proof.
