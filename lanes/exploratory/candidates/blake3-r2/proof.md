# Salted distinguished-point rho search on 2-round BLAKE3 (generic birthday bound)

## 0. Summary

This exploratory package claims a **generic** collision search for blake3-r2-prefix-v1,
priced under collision-frontier-v5 with C = 430 for blake3-r2:

- total charged time T < 2^128.0975, claimed as time_log2 = 128.1;
- success probability at least 0.39, under the single declared heuristic H1
  (salted random-mapping model, Section 5, with a scaled experiment declared in
  experiments/manifest.json for the organizer to execute at submission);
- peak memory at most 2^118 bytes (a cap; the expected use is below 2^104 bytes);
- preprocessing (fixed setup) below 2^12 units; nonuniform advice zero.

It is a van Oorschot-Wiener style distinguished-point rho walk on one function
chosen at random from a salted family. It is not a cryptanalytic advance on BLAKE3.
Section 9 explains why no attack below the birthday bound is claimed. The time
bound is a worst-case cap on the program below: every run halts within it, whether
it succeeds or fails. Only the success probability depends on H1. Whenever the
algorithm outputs a pair, a final check guarantees that the pair is a valid
collision, with no heuristic involved (Section 3).

## 1. Exact target and the walk map

The hash H is unkeyed BLAKE3-256 with prefix rounds 0 and 1 in every compression,
as in the target profile. The algorithm only evaluates messages of exactly 64 bytes.
For such a message there is one chunk with one full block, no parent node, and one
root compression with counter 0, block length 64, and flags
CHUNK_START | CHUNK_END | ROOT = 1 | 2 | 8 = 11. There is no key and no extra
padding block.

Decode the message into little-endian 32-bit words w[0..15]. Set v[0..7] = IV,
v[8..11] = IV[0..3], and v[12..15] = (0, 0, 64, 11), where IV is

    6a09e667 bb67ae85 3c6ef372 a54ff53a 510e527f 9b05688c 1f83d9ab 5be0cd19.

Additions are mod 2^32 and ROR rotates a 32-bit lane right.
G(a,b,c,d,x,y) performs these updates in order:

    v[a]=v[a]+v[b]+x; v[d]=ROR(v[d]^v[a],16); v[c]=v[c]+v[d]; v[b]=ROR(v[b]^v[c],12)
    v[a]=v[a]+v[b]+y; v[d]=ROR(v[d]^v[a],8);  v[c]=v[c]+v[d]; v[b]=ROR(v[b]^v[c],7)

Each of the two rounds applies, with the current schedule s (initially s = w):

    G(0,4,8,12,s0,s1)   G(1,5,9,13,s2,s3)   G(2,6,10,14,s4,s5)   G(3,7,11,15,s6,s7)
    G(0,5,10,15,s8,s9)  G(1,6,11,12,s10,s11) G(2,7,8,13,s12,s13) G(3,4,9,14,s14,s15)

Between rounds, s is replaced by s[P[i]] with P = (2,6,3,10,7,0,4,13,1,11,12,5,9,14,15,8).
After exactly 2 rounds the digest lanes are o[i] = v[i] XOR v[i+8], for i = 0..7.
H(m) = LE4(o[0]) || ... || LE4(o[7]) is the first 32 bytes of the root output.
This matches the organizer reference verifier/blake3.py with rounds = 2 on 64-byte
inputs. The feed-forward lanes o[8..15] are not part of the 32-byte digest.

**Walk map.** Write a point x as eight 32-bit lanes (x_0, ..., x_7); there are
N = 2^256 points. A salt s is eight 32-bit lanes (s_0, ..., s_7). Define the message

    M_s(x) = LE4(x_0) || ... || LE4(x_7) || LE4(s_0) || ... || LE4(s_7)   (64 bytes)

and f_s(x) = (o[0], ..., o[7]) of H(M_s(x)), the digest read as eight lanes.
For a fixed s, the map x -> M_s(x) is injective. Hence if f_s(p) = f_s(q) and p != q,
then M_s(p) != M_s(q) and H(M_s(p)) = H(M_s(q)): an ordinary collision of the complete
hash on two distinct 64-byte messages. A point x is **distinguished** (DP) if x_0 = 0.
The DP set has exactly theta*N points, with theta = 2^-32.

## 2. Algorithm

Parameters, all public constants in the program:

- k' = 2^128 and k = k' + 2^37 (walk length);
- D_max = 2^110 (record cap);
- g = 2^37 (window) and the gap bound 2^38.

The only coins are 16 fresh independent uniform 256-bit words from the RAM primitive.
Each is masked to 32 bits, giving the salt s and the start point x^(0), both uniform.
No PRNG is used.

1. **Walk.** Store record (pack(x^(0)), 0) in array A. For i = 1, ..., k compute
   x^(i) = f_s(x^(i-1)). If x^(i) is a DP, append the record (pack(x^(i)), i) to A.
   If A would exceed D_max records, halt with failure. Here pack(x) is the 256-bit
   word sum_j x_j * 2^(32j), which is injective. A is therefore in increasing index
   order. There is no early exit: exactly k compressions are made.
2. **Sort.** Copy A to A1. Stable bottom-up merge sort of A1 by the packed value,
   alternating between A1 and A2. Equal values keep increasing index order.
3. **First revisit.** Scan the sorted array. For every record that has the same value
   as its predecessor, form the candidate (i, j): i is the index of the first record
   of that equal-value group and j is the index of the record itself. Keep the
   candidate with the smallest j, called (i*, j*). If there is none, or i* = 0,
   halt with failure. Set lambda = j* - i*.
4. **Neighbours.** Binary-search A, which is sorted by index, for i* and j*. Let a be
   the index of the record just before i*, and b the index of the record just before
   j*. If i* - a > 2^38 or j* - b > 2^38, halt with failure.
5. **Relocate.** Unpack x^(a) and x^(b) from their records.
   - If b - lambda > a, set p = f_s applied (b - lambda - a) times to x^(a), and
     q = x^(b).
   - Otherwise, set p = x^(a) and q = f_s applied (a + lambda - b) times to x^(b).

   If p = q, halt with failure. Then repeat at most 2^38 times: if f_s(p) = f_s(q)
   (all eight lanes), go to step 6; otherwise set p = f_s(p) and q = f_s(q).
   If the cap is reached, halt with failure.
6. **Verify and output.** Form M_s(p) and M_s(q), and recompute both complete hashes
   from scratch (two root compressions). Check that p != q and that all 256 digest
   bits are equal. If so, output the two messages; otherwise halt with failure.

## 3. Correctness of any output (no heuristic)

Step 6 directly checks message distinctness, since M_s is injective and p != q.
It also checks equality of the complete 256-bit hash of Section 1. Every output is
therefore an ordinary collision of blake3-r2 on two 64-byte messages in the profile
domain. It is not free-start, compression-only, truncated or semi-free-start.
The probability analysis below concerns only how often step 6 is reached and passes.

## 4. Success in the random-function model

In this section, f is a uniformly random function on the N points and x^(0) is
uniform and independent of it. Section 5 states the heuristic that transfers this
to (f_s, x^(0)) with a random salt.

Let rho be the first index with x^(rho) in {x^(0), ..., x^(rho-1)}. Write
x^(rho) = x^(mu), with tail length mu and cycle length lambda_c = rho - mu.
So x^(i) = x^(i + lambda_c) exactly when i >= mu.

**Lemma 1 (symmetry).** Conditioned on (mu, lambda_c), the tuple
(x^(0), ..., x^(rho-1)) is uniform over ordered tuples of rho distinct points.
For each i, x^(i) is marginally uniform.

*Proof.* For any permutation sigma of the points, (sigma f sigma^-1, sigma(x^(0)))
has the same law as (f, x^(0)). It maps the trajectory to its image under sigma
and preserves (mu, lambda_c). Permutations act transitively on ordered tuples of
distinct points, and on single points. QED.

**Lemma 2.** Pr[rho > j] = prod_{i=1..j} (1 - i/N) <= exp(-j(j+1)/(2N)). Given
rho = r, mu is uniform on {0, ..., r-1}.

*Proof.* While the points are distinct, each new point x^(i) = f(x^(i-1)) is a fresh
uniform value of f, because f has not yet been queried at x^(i-1). It is new with
probability 1 - i/N. The inequality uses 1 - t <= e^-t. Given that the r-th value
falls among the r earlier points, it is uniform over them. QED.

Define these events:

- (A) rho <= k';
- (B) mu >= 1;
- (C) lambda_c > 2^38;
- (D) some DP index lies in [mu, mu + g);
- (E) mu <= g, or some DP index lies in [mu - g, mu);
- (F) some DP index lies in [mu + lambda_c - g, mu + lambda_c);
- (G) the walk produces at most D_max records.

**Lemma 3 (the program succeeds on A-G).** Let d be the first DP index >= mu.
By (C) and (D), d < mu + g <= mu + lambda_c. A point is revisited only if it lies
on the cycle, so a repeated record value appears first at index
j* = d + lambda_c = rho + (d - mu) < k' + g = k. That index is inside the walk, and
its earlier occurrence is i* = d >= 1. Records are taken only at index 0 and at DP
indices, and there is no DP in [mu, d). So a < mu, and a = 0 is possible because
mu >= 1. By (E), mu - a <= g, so i* - a < 2g = 2^38. Symmetrically, there is no
DP in [mu + lambda_c, j*), so b < mu + lambda_c, and by (F) j* - b < 2g. The
checks in step 4 pass. Step 5 starts p at index s1 = max(a, b - lambda) < mu and
q at index s1 + lambda, with lambda = lambda_c. The walk lengths are b - lambda - a
< i* - a and a + lambda - b < j* - b, both below 2^38. Since s1 < mu, p != q:
x^(s) = x^(s+lambda) with s < mu would contradict the minimality of rho. In
lockstep, f(p) = f(q) first holds when p = x^(mu-1) and q = x^(mu-1+lambda), at
check number mu - s1 <= mu - a <= g < 2^38. These are distinct points with equal
images. Step 6 passes. QED.

**Failure bounds** (random-function model):

- Not A: Lemma 2 with j = k' = 2^128 gives at most
  exp(-2^128 (2^128 + 1)/2^257) < exp(-1/2) < 0.6065307.
- Not B or not C: Pr[rho <= 2^100] <= 2^100 (2^100 + 1)/(2N) < 2^-56. Given
  rho = r > 2^100, Lemma 2 gives Pr[mu = 0] = 1/r < 2^-100 and
  Pr[lambda_c <= 2^38] = 2^38/r < 2^-62. The total is below 2^-55.
- Not D, E or F, given C: by Lemma 1, each named window holds g specific positions
  among the rho distinct points. The probability that none is a DP is
  prod_{i=0..g-1} (N - theta N - i)/(N - i) <= (1 - theta)^g <= exp(-theta g)
  = exp(-32), for each window. Together they contribute at most 3 e^-32 < 4 * 10^-14.
- Not G: by Lemma 1, E[#records] = 1 + k*theta = 2^96 + 33. Markov's inequality
  gives Pr[#records > 2^110] <= (2^96 + 33)/2^110 < 6.11 * 10^-5.

Hence Pr[failure] < 0.6065307 + 0.0000611 + 10^-13 < 0.6066, so the success
probability is above 0.3934 in the random-function model. The claim uses 0.39.
The difference of 0.0034 is a small allowance, not a statistically certified
margin: the measurements of Section 5 resolve the relevant probability only to
about 0.001-0.03 and show agreement within about 2 s.e.; they cannot rule out a
deviation of the real family larger than 0.0034. The 0.39 figure therefore rests on H1, not on the data.
For a reader weighing the trade-off: with k' = 1.05 * 2^128 the same computation
gives failure below exp(-1.05^2/2) + 0.000065 + 10^-13 < 0.5763 (the Markov term
grows to (1.05 * 2^96 + 33)/2^110), i.e. success above 0.42, at a time cost of
a factor about 1.05 (log2 1.05 < 0.071). We do not use this variant.

## 5. Declared heuristic H1 and its evidence

**H1 (salted random-mapping model; score-critical).** For a uniformly random salt
s and an independent uniform start x^(0), the failure probability of the events
A-G for the actual map f_s is at most the bound computed in Section 4 for a
uniformly random function, up to a negligible amount. Equivalently, the walk
statistics that matter (rho, mu, lambda_c, the positions of distinguished points
and their number) behave as for a random mapping, averaged over the salt.

Role: the success probability 0.39 depends on H1. Correctness of outputs and the
time cap do not.

**5.1 Why a salt; the generic premise.** For one fixed function, the probability
over x^(0) that rho is at most k' depends on that function's particular large
cycle. It need not equal the random-mapping average; our unsalted measurements in
5.5 show exactly this. The random salt makes the function itself part of the
algorithmic coins, so the relevant probability is the average over the family
{f_s}. That average is what the random-mapping computation predicts. This is the
standard treatment of rho-type collision search (Pollard's rho; van Oorschot and
Wiener, "Parallel collision search with cryptanalytic applications", J. Cryptology
12(1):1-28, 1999), and the usual premise for generic collision searches on 256-bit
hashes. No property specific to reduced BLAKE3 is used.

**5.2 What the experiments can and cannot detect.** Every experiment below either
restricts the walk to a few bits per lane and truncates the output (5.3, 5.5), or
measures one output lane (5.4). A restrict-then-truncate map looks like a random
mapping almost regardless of the global structure of the full 256-bit map: even if
f_s were a permutation of the 2^256 points, its truncations would show
random-mapping rho statistics. **The experiments therefore cannot detect the
failure mode "f_s is materially closer to a permutation (or otherwise has far fewer
collisions) than a random mapping".** For that mode, H1 rests only on the generic
premise of 5.1 and on the structural remarks in 5.6. What the experiments do test
is (i) that the actual 2-round compression, with the salt as coins, drives a
complete run of the algorithm (walk, distinguished points, sort, first revisit,
relocation, lockstep, verification) with the success rate a random function would
give at small scale, (ii) that the salt-averaged rho statistics match the
random-mapping law, and (iii) that the distinguished-point rate of digest lane
o[0] along real trajectories is as for uniform values, at the bit-widths reachable.

**5.3 Organizer-executed experiment `b3r2-scaled-walk` (experiments/manifest.json).**
The organizer runs it at submission; it has not been run by the organizer yet. The
stdlib-only program experiments/b3r2_scaled_walk.py runs, for each organizer
seed, one complete scaled copy of Steps 1-6 on the exact target compression:

- coins: the first 17 of the 24 little-endian words of SHA-256("b3r2-scaled-walk-v1"
  || seed || byte i), i = 0, 1, 2: per-trial constants C_0..C_7, salt S_0..S_7,
  and a word whose low 16 bits are the start point;
- point x: 16 bits, two in each of the eight walk lanes (N_t = 2^16). Message word
  j < 8 is C_j with its low two bits replaced by bits 2j, 2j+1 of x; words 8..15 are
  the salt. So all eight walk lanes carry point bits, and the unused bits are fresh
  random constants rather than zeros;
- f_t(x): bits 2j, 2j+1 are the low two bits of digest lane o[j], j = 0..7, of the
  complete 2-round hash of the 64-byte message (one root compression, flags 11);
- distinguished point: the two bits from lane 0 are zero (theta = 1/4), the
  analogue of x_0 = 0;
- k' = 2^8 = sqrt(N_t), g = 2^5 (theta * g = 8), gap bound 2g, k = k' + g,
  D_max = 2^9 (not binding, since there are at most k + 1 records);
- Steps 2-5 exactly as in Section 2 (stable sort, first revisit, neighbours, gap
  checks, relocation, lockstep capped at 2g); Step 6 recomputes both digests.

A success returns M(p), M(q): distinct messages whose digests agree on the low two
bits of all eight lanes. The organizer recomputes this event (mask 03000000
repeated eight times, expected zero) for every returned pair; a failure returns two
nulls; success counts reported by the program are not used.

*Prediction.* The program's model mode runs the identical attempt() on a lazily
sampled uniformly random function on 2^16 points. Over 10^6 trials (five runs of
2 * 10^5 with seeds 11-15) it succeeded in 449085 trials: 0.4491 (s.e. 0.0005).
Failure codes: no revisit 547445, i* = 0 862, p = q 2608, all others 0. (A pilot
of 20000 trials, seed 1, gave 0.4454 (s.e. 0.0035).) This exceeds 0.3934 because
at this scale g = k'/8 is not negligible against k', so the walk is 12.5% longer
than k'; the experiment compares the program with its own random-function value,
not with 0.3934. The parameters were fixed before any run on the real map, and
this is the only configuration we ran.

*Our local run of the organizer protocol (not organizer-run).* We ran the
repository's experiments/runner.py run_experiments() unchanged except that the
Docker call was replaced by a local CPython 3.12 subprocess, with the public seed
"hashsmash-public-seed-v1", no holdout nonce, the blake3-r2-exploratory target
configuration, and the organizer digest callback:

| trials | checked successes | frequency (s.e. at 0.4491) | no revisit | i* = 0 | p = q | other failures |
|---:|---:|---:|---:|---:|---:|---:|
| 256 (default) | 119 | 0.465 (0.031) | 135 | 0 | 2 | 0 |
| 4096 (maximum organizer setting) | 1856 | 0.4531 (0.0078) | 2229 | 2 | 9 | 0 |

The 4096 trials include the 256. Both are within 0.6 s.e. of 0.4491, and the
failure-code split matches the model (expected per 4096: 2242, 3.5, 10.7). No
returned pair was a full collision or repeated. A 256-trial run took under 1 s
locally (about 10^5 compressions). Only the organizer's own execution is trusted
evidence; with a holdout nonce its seeds, and so its counts, will differ.

**5.4 Distinguished-point rate of o[0] along full-width trajectories (our run).**
Events D-G depend on the rate at which points on actual trajectories have
x_0 = o[0] = 0. We iterated the full 256-bit f_s (next point = all eight digest
lanes) for 16384 walks of 2^20 steps, each with a fresh salt and start from a
splitmix64 stream, 2^34 points in total, and counted points whose low b bits of
o[0] are zero (C program in Appendix B; its compression is the one in Appendix A,
checked against verifier/blake3.py):

| b | observed | expected 2^(34-b) | deviation |
|---:|---:|---:|---:|
| 16 | 261567 | 262144 | -1.13 s.e. |
| 20 | 16293 | 16384 | -0.71 s.e. |
| 24 | 1021 | 1024 | -0.09 s.e. |
| 28 | 58 | 64 | -0.75 s.e. |
| 32 | 2 | 4 | Poisson Pr[<= 2] = 0.24 |

The largest single-bit bias of o[0] over its 32 bits was 7.6 * 10^-6 (1.99 s.e.,
the maximum of 32 comparisons). No deviation from uniform DP marking is seen. The
experiment of 5.3 additionally exercises the DP logic end to end, with theta = 1/4
on lane-0 bits. The full rate theta = 2^-32 is only probed by the b = 28 and
b = 32 rows; events D-F are about DP gaps of length g = 2^37 along one trajectory,
which no feasible experiment reaches.

**5.5 Rho measurements on truncated maps (our runs).** Point x has t bits, placed
in lanes L and L+1 (walk lanes otherwise zero). The salt is eight random lanes in
w[8..15], new per trial. f_t keeps the low t bits of o[L] + 2^32 o[L+1]. The start
is uniform per trial. rho, mu and lambda_c were found exactly with Brent's cycle
algorithm in the C program of Appendix A, whose compression output was checked
against verifier/blake3.py; 1942 returned t-bit partial-collision pairs were
rechecked with the reference. Random-mapping predictions:
E[rho]/sqrt(N_t) = sqrt(pi/2) = 1.2533 and Pr[rho <= sqrt(N_t)] = 1 - exp(-1/2) =
0.3935; sqrt(N_t) is the analogue of k' = 2^128 = sqrt(N) in event A.

Salted runs use one fresh salt and start per trial. The s.e. of the probability
column is the binomial s.e. at 0.3935. Within a batch, the L = 0 and L = 4 rows use
the same seeds, hence the same salts and starts, so they are not independent of
each other. Batch 1 had trial counts fixed in advance. Batch 2 was a follow-up,
run after batch 1's two t = 24 rows came out about 2 s.e. high in the mean; with
ten times the trials it does not reproduce that deviation.

| batch | t | L | trials | mean rho/sqrt(N_t) (s.e.) | Pr[rho <= sqrt(N_t)] (s.e.) | mu = 0 |
|---:|---:|---:|---:|---:|---:|---:|
| 1 | 24 | 0 | 20000 | 1.262 (0.005) | 0.389 (0.003) | 3 |
| 1 | 24 | 4 | 20000 | 1.263 (0.005) | 0.388 (0.003) | 9 |
| 1 | 32 | 0 | 20000 | 1.252 (0.005) | 0.393 (0.003) | 1 |
| 1 | 32 | 4 | 20000 | 1.249 (0.005) | 0.396 (0.003) | 1 |
| 1 | 40 | 0 | 4000 | 1.252 (0.010) | 0.395 (0.008) | 0 |
| 1 | 40 | 4 | 4000 | 1.249 (0.010) | 0.401 (0.008) | 0 |
| 1 | 48 | 0 | 420 | 1.246 (0.030) | 0.393 (0.024) | 0 |
| 1 | 48 | 4 | 420 | 1.222 (0.031) | 0.426 (0.024) | 0 |
| 1 | 56 | 0 | 21 | 1.313 (0.159) | 0.429 (0.107) | 0 |
| 1 | 56 | 4 | 21 | 1.174 (0.159) | 0.524 (0.107) | 0 |
| 2 | 24 | 0 | 200000 | 1.254 (0.001) | 0.393 (0.001) | 63 |
| 2 | 24 | 4 | 200000 | 1.254 (0.001) | 0.393 (0.001) | 70 |
| 2 | 28 | 0 | 100000 | 1.256 (0.002) | 0.391 (0.002) | 14 |
| 2 | 28 | 4 | 100000 | 1.253 (0.002) | 0.395 (0.002) | 5 |
| 2 | 32 | 0 | 40000 | 1.253 (0.003) | 0.392 (0.002) | 0 |
| 2 | 32 | 4 | 40000 | 1.253 (0.003) | 0.393 (0.002) | 0 |

There are 16 salted rows with two statistics each, about 32 comparisons, so one or
two excursions of about 2 s.e. are expected by chance. Batch 1's t = 24
probabilities (0.3890, 0.3882) are 0.0045 and 0.0053 below 0.3935, 1.3 and 1.5 s.e.;
an effect of that size, if real, would exceed the 0.0034 allowance of Section 4,
but batch 2 at ten times the trials gives 0.393 for both lanes. Every other salted
entry lies within about 2 s.e. of the prediction.

For comparison, here are the same maps with **no salt** (w[8..15] = 0), so each row
is one fixed function and only the start varies:

| t | L | starts | mean rho/sqrt(N_t) | Pr[rho <= sqrt(N_t)] | distinct lambda_c values |
|---:|---:|---:|---:|---:|---:|
| 24 | 0 | 20000 | 0.962 | 0.523 | 5 |
| 24 | 4 | 20000 | 1.352 | 0.409 | 7 |
| 32 | 0 | 20000 | 0.623 | 0.928 | 7 |
| 32 | 4 | 20000 | 1.212 | 0.260 | 6 |
| 40 | 0 | 5000 | 0.887 | 0.675 | 5 |
| 40 | 4 | 5000 | 0.844 | 0.674 | 6 |
| 48 | 0 | 2100 | 0.786 | 0.728 | 6 |

The unsalted values scatter between 0.26 and 0.93 depending on the function. This
motivates the salt and does not contradict H1. Each unsalted row shows only 5 to 7
distinct cycle lengths: different starts share a cycle, so those starts are not
independent trials. Each run's trial counts were fixed before it started. An
earlier unsalted run at t = 56, and at t = 48 with L = 4, was stopped unfinished
and is not reported.

**5.6 Scope, extrapolation and limitations.** The measured maps restrict the
family's input and output to at most 56 bits (16 bits in 5.3). The claim uses the
full 256-bit map, an extrapolation of about 200 bits that is not established. As
5.2 explains, no experiment here can detect permutation-like global structure of
the full map; for that mode the support is the generic premise only. Structurally,
we know of no property of 2-round BLAKE3 that makes its iteration statistics worse
for this walk. The lemma in Section 9 shows that for a fixed salt distinct points
give distinct internal states after round 1, so no trivial degeneracy appears
there; but the second round and the 512-to-256-bit output fold are not analysed for
global injectivity, and a function closer to a permutation would lower the
success probability. Only the experiment of 5.3 is organizer-executed; the
measurements of 5.4 and 5.5 were run by us, with their source in Appendices A
and B, and were not reproduced by the organizer. All counts are finite samples.
If H1 were rejected, the only effect would be on the 0.39 success bound; the time
cap and output correctness would be unchanged.

## 6. Machine model and per-operation accounting

We use the classical 256-bit word RAM of collision-frontier-v5. It has a fixed set
of 64 registers and byte-addressed memory of 256-bit words, with addresses below
2^130. The listed primitives cost 1/C = 1/430 unit each: load, store, add/sub,
AND/OR/XOR/NOT, shift/rotate, compare, conditional branch, and random word. One
selected-round compression costs 1 unit. We treat the compression as a
register-to-register operation: it takes the 16 message lanes from registers and
returns the 8 digest lanes in registers. Its fixed IV, counter, length and flag
words belong to the compression, as in the reference count that defines C. Every
load and store that feeds it or saves its outputs is charged separately as a word
operation. There is no whole-hash oracle, free sort, or uncharged lookup.

The compression is an atomic primitive; its internal state is not counted against
the 64 registers. If a reviewer instead requires it to read its input from memory
and write its output to memory, those reads and writes are exactly the 16 loads of
S1 and the 8 stores of S3 below, which are already charged, so the bound is the
same. Registers used by the program: R0..R15 (message lanes, then digest lanes),
the step index Ri, the bound Rk, the record count, D_max, the base addresses of
B and of the record arrays, and a few temporaries for the DP handler, sort and
scan, in all fewer than 32 of the 64.

**Walk step (loop body), at most 30 word operations plus 1 compression.** The
message buffer B[0..15] holds the current point in B[0..7] and the salt in
B[8..15], at constant addresses.

    S1  load R0..R15 <- B[0..15]                         16 loads
    S2  R0..R7 <- compression(R0..R15)                   1 unit
    S3  store B[0..7] <- R0..R7                          8 stores
    S4  Ri <- Ri + 1                                     1
    S5  compare R0 with 0; branch to DP handler if equal 2
    S6  compare Ri with Rk; branch to S1 if less         2

That is 29 word operations, charged as 30. The salt lanes are reloaded on every
step and charged, although a register-resident version would not need to reload
them.

**DP handler, at most 64 word operations per record** (at most D_max records,
otherwise halt): 2 to compare the count with D_max and branch; 14 shifts and ORs
to pack R0..R7; 2 for the address base + (count << 6), since records are 64 bytes;
1 add and 2 stores to store the value and the index; 1 to increment the count;
1 to branch back. That is 23 in total.

**Post-processing, at most 7080 word operations per record, plus 2^12 in total.**
With the DP handler, the per-record total is at most 64 + 7080 = 7144.

- Copy A to A1: at most 8 per record.
- Merge sort: at most 110 passes, because the count is at most 2^110. Each output
  record costs at most 64 per pass. Charged are two exhaustion tests, two key
  loads, a compare and branch, two loads and two stores of the record, cursor and
  address updates, and loop control. Run and pass setup, amortized because each
  run emits at least one record, fits within the 64. Total 7040.
- Scan for the first revisit: at most 32 per record.
- Binary searches and the checks of step 4: below 2^12 operations in total.

**Relocation.** The alignment walk takes fewer than 2^38 steps (Lemma 3, enforced
by the step-4 checks). Lockstep is capped at 2^38 iterations of 2 compressions.
So there are fewer than 2^38 + 2^39 < 2^40 compressions, each with at most 64 word
operations (loads, stores, eight lane comparisons, control). Final verification:
2 compressions and fewer than 2^10 word operations.

**Setup.** The program and public constants total at most 2^24 bytes (2^19 words).
Initializing them costs at most 2^20 word operations. Drawing and masking the
16 coin words and storing B and record 0 costs fewer than 2^7.

## 7. Total time

Compressions in the walk: exactly k, where

    k = 2^128 + 2^37 < 1.00001 * 2^128.

The walk's charged time is k * (1 + 30/430) = k * 460/430. All other work is at
most

    [2^110 * 7144 + 2^12 + 2^20 + 2^10 + 2^7] / 430      (word operations)
      + 2^40 * (1 + 64/430) + 2                          (compressions)
    < 2^110 * 16.62 + 2^41 < 2^115 = 2^-13 * 2^128.

Therefore

    T < 1.00001 * (460/430) * 2^128 + 2^-13 * 2^128
      < (1.0697782 + 0.0001221) * 2^128
      < 1.06991 * 2^128.

Since 2^0.1 = 1.0717735 > 1.06991, T < 2^128.1, and in fact
log2(1.06991) < 0.0975. This is a worst-case cap for every run. It covers the
setup, all coins, every compression, all failed or unused walk steps,
record-keeping, the sort, the scan, relocation and the final verification. There
is no restart. The submitted time_log2 = 128.1 is this bound rounded up.

## 8. Memory, preprocessing, advice and claim fields

- memory_log2_bytes = 118. A, A1 and A2 each hold at most 2^110 records of 64 bytes
  (2^116 bytes). Together with the 2^24-byte program, constants, buffer B and
  registers spilled to memory, the peak is at most 3 * 2^116 + 2^24 < 2^118 bytes.
  The expected number of records is 1 + k * theta = 2^96 + 33, so the typical
  use is about 2^102 to 2^104 bytes. The cap is the claimed figure.
- preprocessing_log2 = 12. The fixed setup is at most 2^20 word operations, i.e.
  below 2^20/430 < 2^12 units. It is included in T. There is no other
  precomputation, stored collision, or table built in advance.
- nonuniform_advice_log2_bytes = 0, meaning at most 1 byte; the actual advice is
  zero. The schema cannot express log2(0). The program and public constants are
  charged in memory and setup.
- success_probability = 0.39 is the Section 4 bound under H1, and it is about
  algorithmic success. It is not confidence in H1 or in a review.
- time_log2 = 128.1 bounds total charged v5 time (Section 7).
- data_log2 is omitted, as the schema recommends for new claims. For information,
  the number of complete-hash evaluations is at most k + 2^40 + 2 < 2^128.0001.

No certificate is supplied: no collision for 2-round BLAKE3 is known to us, and
running this search is infeasible. The certificate manifest is valid and empty.

## 9. Why no sub-birthday attack is claimed

We claim only the generic bound, for these reasons.

**Literature.** We know of no published ordinary (fixed-IV) collision attack on
BLAKE3 reduced to 2 rounds. The nearest results are below; none of them is a
2-round ordinary collision of BLAKE3.

- The BLAKE3 specification (O'Connor, Aumasson, Neves, Wilcox-O'Hearn, "BLAKE3:
  one function, fast everywhere", version 20211102173700, the version we checked),
  Table 5 ("Best differential trail probabilities for increasing round numbers of
  the compression functions of BLAKE-256, BLAKE2s, and BLAKE3 ..."), row "BLAKE3
  (hash)": 2^-0, 2^-1 and 2^-29 at 0.5, 1 and 1.5 rounds, and ">= 2^-185" at 2
  rounds, marked as found by searching rotationally symmetric differences only.
  These are trail-search results, not attacks or lower bounds.
- Li Ji and Xu Liangyu, "Attacks on Round-Reduced BLAKE" (IACR ePrint 2009/238),
  a different function (BLAKE-32). Section 3.1 and Table 5 give a 2^96 given-IV
  collision on 1.5-round BLAKE-32: message modification fixes two output words,
  and a memoryless collision search runs on the other six (3 * 32 = 96 bits). This
  is the closest technique to a sub-birthday 2-round BLAKE3 collision. For 2 and
  2.5 rounds, Table 5 gives 2^112 **free-start** collisions (out of scope here)
  and "-" for the given-IV collision. We have not analysed whether the
  output-word-fixing idea can be carried to 2-round BLAKE3; we do not claim it
  cannot.

Our search may be incomplete, and the absence of a publication is not a proof of
security.

**Our own analysis.** A natural mechanism at very low round counts is a state
difference that complements both v[i] and v[i+8]: then the folded output
v[i] XOR v[i+8] is unchanged. The lemma and remarks below show why this mechanism
does not by itself give a 2-round collision.

*Lemma (round-1 injectivity).* Fix the initial state, as here (IV, counter 0,
length 64, flags 11). Then the state after the first full round determines all
16 message words. In particular, distinct messages give distinct states after
round 1.

*Proof.* Consider G with inputs (a, b, c, d), message words (x, y), intermediate
values a1, b1, c1, d1 (after the first half) and outputs (a2, b2, c2, d2), as in
Section 1. Inverting the last updates gives

- b1 = ROL(b2, 7) XOR c2, c1 = c2 - d2 and d1 = ROL(d2, 8) XOR a2;
- then b = ROL(b1, 12) XOR c1 and c = c1 - d1.

So the outputs fix the (b, c) inputs, whatever x and y are. Conversely, when all
four inputs are fixed, (b2, c2) alone fix (x, y):

- b1 = ROL(b2, 7) XOR c2, then c1 = ROL(b1, 12) XOR b, then d2 = c2 - c1;
- d1 = c1 - c, then a1 = ROL(d1, 16) XOR d, so x = a1 - a - b;
- a2 = ROL(d2, 8) XOR d1, so y = a2 - a1 - b1.

The diagonal step's (b, c) inputs are rows 1-2 of the column-step output. Given the
state after round 1, those rows are fixed. The column G's have fixed inputs, so
their (b, c) outputs fix w[0..7] and hence the whole column-step output. The
diagonal G's then have fixed inputs and known outputs, which fix w[8..15]. QED.

Hence any 2-round collision needs a nonzero state difference after round 1 that
cancels in the folded output after a complete second round. Complement-type
differences do not pass modular additions deterministically:
NOT c + NOT d = NOT(c + d) - 1 mod 2^32. So this mechanism breaks in the
second round. We did not find any other usable characteristic. Ten Bitwuzla SMT
runs on 2-round collision instances (various sets of free message words, time
limits 1500 s or 3000 s) all ended "unknown"; that is no evidence either way.
Lacking a concrete, checkable sub-birthday method, we submit only the generic
search.

## 10. Interpretation

This is a generic baseline proposal; no improvement over the nominal reference 128
is claimed. The scalar 128.1 is above 128 because of real charged overheads: about
0.07 of a unit per step (a deliberately conservative count that reloads and
stores the lanes on every step), the 0.39 success target with its small
allowance (k' = 2^128), and the rounding. The required identifier blake3-r2-nominal-v2 is reference metadata, not
a claim of improvement. The package is a draft. No review outcome, score or
acceptance is asserted.

## Appendix A. Source of the rho measurements (Section 5.5)

The C program below (compiled with cc -O3) produced every row of the two tables in
5.5. Its `selftest` digest of the message with w[i] = i * 0x01010101 equals
verifier/blake3.py with rounds = 2:
7824581ee916d76726e08ba8d901b63c4e04009f010055a661204394337e7d2b.
Invocation: `rho_salt t trials seed L salted`, one output line per trial
(t, L, mu, lambda_c, start, the colliding pair, salt). Seeds and trials per
invocation, each run for both L = 0 and L = 4:

- unsalted (salted = 0): t = 24, 32: seeds 101-104 (t = 24) and 201-204 (t = 32),
  5000 trials each; t = 40: seeds 301-304, 1250 each; t = 48: seeds 401-407,
  300 each (L = 0 reported only, see 5.5);
- salted batch 1: t = 24, 32: seeds 1101-1104 and 1201-1204, 5000 each; t = 40:
  seeds 1301-1304, 1000 each; t = 48: seeds 1401-1407, 60 each; t = 56: seeds
  1501-1507, 3 each;
- salted batch 2: t = 24: seeds 2101-2104, 50000 each; t = 28: seeds 2801-2804,
  25000 each; t = 32: seeds 3201-3204, 10000 each.

rho = mu + lambda_c; a trial counts towards Pr[rho <= sqrt(N_t)] when
mu + lambda_c <= 2^(t/2).

```c
// Rho-length measurements for truncated 2-round BLAKE3 root-compression maps.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
static const uint32_t IV[8]={0x6A09E667,0xBB67AE85,0x3C6EF372,0xA54FF53A,0x510E527F,0x9B05688C,0x1F83D9AB,0x5BE0CD19};
static const int P[16]={2,6,3,10,7,0,4,13,1,11,12,5,9,14,15,8};
#define ROR(x,n) (((x)>>(n))|((x)<<(32-(n))))
#define G(a,b,c,d,x,y) do{v[a]=v[a]+v[b]+(x);v[d]=ROR(v[d]^v[a],16);v[c]=v[c]+v[d];v[b]=ROR(v[b]^v[c],12);\
 v[a]=v[a]+v[b]+(y);v[d]=ROR(v[d]^v[a],8);v[c]=v[c]+v[d];v[b]=ROR(v[b]^v[c],7);}while(0)
static void comp(const uint32_t w[16], uint32_t o[8]){
  uint32_t v[16],m[16],t[16];int r,i;
  for(i=0;i<8;i++)v[i]=IV[i];for(i=0;i<4;i++)v[8+i]=IV[i];v[12]=0;v[13]=0;v[14]=64;v[15]=11;
  memcpy(m,w,64);
  for(r=0;r<2;r++){G(0,4,8,12,m[0],m[1]);G(1,5,9,13,m[2],m[3]);G(2,6,10,14,m[4],m[5]);G(3,7,11,15,m[6],m[7]);
    G(0,5,10,15,m[8],m[9]);G(1,6,11,12,m[10],m[11]);G(2,7,8,13,m[12],m[13]);G(3,4,9,14,m[14],m[15]);
    for(i=0;i<16;i++)t[i]=m[P[i]];memcpy(m,t,64);}
  for(i=0;i<8;i++)o[i]=v[i]^v[i+8];
}
static int T, LANE, SALTED; static uint32_t SALT[8]; // truncation bits, starting lane (input and output)
static uint64_t MASK;
static uint64_t f(uint64_t x){ uint32_t w[16]={0},o[8];
  if(SALTED)for(int i=0;i<8;i++)w[8+i]=SALT[i];
  w[LANE]=(uint32_t)x; w[LANE+1]=(uint32_t)(x>>32);
  comp(w,o); uint64_t y=(uint64_t)o[LANE]|((uint64_t)o[LANE+1]<<32); return y&MASK; }
static uint64_t s=88172645463325252ULL; static uint64_t rnd(){s^=s<<13;s^=s>>7;s^=s<<17;return s;}
int main(int argc,char**argv){
  if(argc>1 && !strcmp(argv[1],"selftest")){ // print digest of message with lanes w[i]=i*0x01010101
    uint32_t w[16],o[8];for(int i=0;i<16;i++)w[i]=i*0x01010101u;comp(w,o);
    for(int i=0;i<8;i++)for(int b=0;b<4;b++)printf("%02x",(o[i]>>(8*b))&255);printf("\n");return 0;}
  T=atoi(argv[1]); int trials=atoi(argv[2]); s^=strtoull(argv[3],0,10)*0x9E3779B97F4A7C15ULL; LANE=atoi(argv[4]); SALTED=argc>5?atoi(argv[5]):0;
  MASK=(T==64)?~0ULL:((1ULL<<T)-1); for(int i=0;i<10;i++)rnd();
  for(int tr=0;tr<trials;tr++){
    if(SALTED)for(int i=0;i<8;i++)SALT[i]=(uint32_t)rnd();
    uint64_t x0=rnd()&MASK;
    // Brent: find lambda
    uint64_t power=1,lam=1,tort=x0,hare=f(x0);
    while(tort!=hare){ if(power==lam){tort=hare;power<<=1;lam=0;} hare=f(hare); lam++; }
    // find mu
    uint64_t a=x0,b=x0; for(uint64_t i=0;i<lam;i++)b=f(b);
    uint64_t mu=0,pa=0,pb=0; while(a!=b){pa=a;pb=b;a=f(a);b=f(b);mu++;}
    // collision pair (pa,pb) if mu>0
    printf("%d %d %llu %llu %llu %llu %llu %08x%08x%08x%08x%08x%08x%08x%08x\n",T,LANE,(unsigned long long)mu,(unsigned long long)lam,
      (unsigned long long)x0,(unsigned long long)pa,(unsigned long long)pb,SALT[0],SALT[1],SALT[2],SALT[3],SALT[4],SALT[5],SALT[6],SALT[7]);
    fflush(stdout);
  }
  return 0;
}
```

## Appendix B. Source of the distinguished-point rate measurement (Section 5.4)

Same `comp` as Appendix A (same includes, IV, P, ROR and G). Run as
`dp_traj JOB 1024 1048576` for JOB = 0..15, and the 16 output lines summed.

```c
static uint64_t sm; static uint64_t splitmix(void){uint64_t z=(sm+=0x9E3779B97F4A7C15ULL);z=(z^(z>>30))*0xBF58476D1CE4E5B9ULL;z=(z^(z>>27))*0x94D049BB133111EBULL;return z^(z>>31);}
int main(int argc,char**argv){
  if(argc>1&&!strcmp(argv[1],"selftest")){uint32_t w[16],o[8];for(int i=0;i<16;i++)w[i]=i*0x01010101u;comp(w,o);
    for(int i=0;i<8;i++)for(int b=0;b<4;b++)printf("%02x",(o[i]>>(8*b))&255);printf("\n");return 0;}
  int job=atoi(argv[1]); long salts=atol(argv[2]); long steps=atol(argv[3]);
  sm=0x5DEECE66DULL*(uint64_t)(job+1);
  uint64_t z[5]={0}, ones[32]={0}, total=0; const int bb[5]={16,20,24,28,32};
  for(long s=0;s<salts;s++){
    uint32_t w[16],o[8];
    for(int i=0;i<16;i++)w[i]=(uint32_t)splitmix();   // w[0..7] start point, w[8..15] salt
    for(long i=0;i<steps;i++){
      comp(w,o); total++;
      for(int k=0;k<5;k++){uint32_t m=bb[k]==32?0xFFFFFFFFu:((1u<<bb[k])-1); if((o[0]&m)==0)z[k]++;}
      for(int b=0;b<32;b++)ones[b]+=(o[0]>>b)&1;
      memcpy(w,o,32);                                   // next point = digest lanes
    }
  }
  printf("%llu",(unsigned long long)total); for(int k=0;k<5;k++)printf(" %llu",(unsigned long long)z[k]);
  for(int b=0;b<32;b++)printf(" %llu",(unsigned long long)ones[b]); printf("\n"); return 0;
}
```
