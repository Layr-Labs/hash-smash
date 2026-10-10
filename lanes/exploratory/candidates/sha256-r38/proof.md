# SHA-256 r38: distribution-free birthday search with wide-digit radix sorting

## 1. Claim, target, and comparison

This is an unconditional classical probabilistic 256-bit word-RAM construction for `sha256-r38-prefix-v1`. The submitted analytical upper bounds are total charged time at most `2^128.2303` target-compression equivalents, peak memory at most `2^136` bytes, and preprocessing at most `2^123` compression equivalents. Success probability is greater than 0.39, over the specified fresh independent random words for the fixed target. There is no output-distribution assumption, cryptanalytic heuristic, precomputed collision, nonuniform advice, or empirical claim. No full-scale attack or collision search has been executed.

The algorithm replaces the organizer package's 128-pass comparison merge sort with two stable counting-sort passes on 128-bit digest digits. The counter array is enormous but fits the model and the stated memory bound. Memory is a required reported metric, not a contribution to the scalar. This is an instruction-accounting improvement to a generic birthday construction, not new reduced-round differential cryptanalysis or an improvement over the nominal display exponent 128. The required `baseline_improved` identifier `sha256-r38-nominal-v2` identifies that nominal reference, not an established attack. The promoted organizer package's submitted bound is 132; the construction here improves that submitted total-computation bound without discounting target compressions.

Each complete-message evaluation uses the standard fixed SHA-256 IV, standard message schedule and original-index constants, round indices 0 through 37 inclusive, and standard wordwise feed-forward. All eight final 32-bit words are serialized big-endian in standard state order, producing the full 256-bit digest. There is no chosen chaining state, truncation, raw-compression collision substitution, changed padding, or suffix-round target.

Under `collision-frontier-v5` a selected target compression costs exactly 1; each other primitive (including a random word, load/store, shift, logical operation, comparison, and branch) costs `1/C`, with `C=2728`. This construction calls the whole selected compression and prices every such call at 1, including all schedule, rounds and feed-forward internals. It makes no use of bit-slicing or an alternative pricing of full compressions. Input and output marshaling, randomness, array initialization, sorting, scanning, failures, and final verification are additional paid work.

## 2. Messages and exact one-block encoding

Let `n=2^128`, `M=2^256`, and `D` be the set of all 48-byte messages, of size `d=2^384`. For each sample, independently draw two uniform 256-bit words `U,R` using the model's random-word primitive. Retain `V=R AND (2^128-1)`. The message is `BE32(U) || BE16(V)`, where BEk means exactly k bytes in big-endian order. This encoding is injective in `(U,V)`, and the resulting messages are iid uniform on D. R is discarded immediately. Its unused high 128 bits are not part of the message or any equality test.

The 64-byte padded block is exactly the pair of 256-bit words

```
B0 = U
B1 = (V << 128) OR (1 << 127) OR 384.
```

The first 48 bytes are the message; byte 48 is 0x80, the next seven bytes are zero, and the final eight bytes encode bit length 384 in big-endian order. Thus hashing requires exactly ONE padded block. Each invocation resets to the standard IV

```
6a09e667 bb67ae85 3c6ef372 a54ff53a
510e527f 9b05688c 1f83d9ab 5be0cd19
```

and returns the full feed-forward state after the first 38 rounds. Denote its packed 256-bit digest by `Y=f(U,V)`. The original messages have length 384 bits, satisfying the profile's strict bound of less than `2^64` bits. The returned collision consists of two unpadded 48-byte strings, not the padded blocks.

## 3. Memory layout and machine widths

A record is three 256-bit words `(Y,U,V)`; V has zero high half. Use arrays A and B of n records, and a counter array K of n single words. Assign disjoint word-address intervals

```
A: [0, 3*n)
B: [3*n, 6*n)
K: [6*n, 7*n)
```

with fixed program, constants and scalar workspace immediately above them. Retain only two random-word results at a time. Clear all 7n array words explicitly at initialization. Although B is completely overwritten on each distribution, its initial clearing is still charged.

There are fewer than `2^15` words of fixed code, constants, scalar registers, hash interface/state, and output workspace; no dynamic allocator, pointer per record, PRNG state history, recursion, list of trial seeds, or second counter table is used. The finite instruction blocks and constant data described below fit in this reserve, even if stored as one 256-bit word per instruction. Fixed loops, not n unrolled instructions, implement the algorithm. Total bytes are

```
32 * (7*n + 2^15) < 256*n = 2^136.
```

The stored counts, prefix sums, insertion cursors, and loop limits must hold n itself: 129 bits suffice. A digest digit uses 128 bits. An address below `7*n+2^15` needs 131 bits in word-address units (or at most 136 bits in byte-address units). All use FULL 256-bit words. In particular, counters and pointers are not incorrectly truncated to 128 bits. All pointer/count additions below stay below `2^256`, so the model's modular arithmetic agrees with the ordinary integer arithmetic used in the proof. A record offset `3*j` is formed as `(j << 1)+j`, using a shift and addition, not unpriced multiplication.

## 4. Algorithm and bounded stopping rule

Generate exactly n samples. For each, compute its complete digest Y and append `(Y,U,V)` to A. There is no deduplication, rejection sampling, early generation stopping, or adaptive trial count. Generate every sample even when it repeats a prior message.

Then do two stable counting-sort passes: low 128-bit digit first, high 128-bit digit second. The following is INERT mathematical pseudocode specifying the RAM algorithm, not participant experiment source. Registers/variables below are full-width words. `src[p]` denotes a record pointer, with three explicitly loaded or stored fields.

```
src = A; dst = B
for shift in [0,128]:
    for t=0,...,n-1: K[t]=0
    for each src record in increasing address order:
        digit = (record.Y >> shift) AND (n-1)
        K[digit] = K[digit]+1
    s=0
    for t=0,...,n-1:
        c=K[t]; K[t]=s; s=s+c
    for each src record in increasing address order:
        digit = (record.Y >> shift) AND (n-1)
        j=K[digit]; K[digit]=j+1
        copy ALL THREE words of the record to dst[j]
    exchange(src,dst)

for each adjacent pair in src:
    if the full digests agree and the retained (U,V) pairs differ:
        serialize the two 48-byte messages
        recompute both complete hashes from the fixed IV
        check message inequality and equality of all 256 digest bits
        return the two messages if these tests pass
        otherwise return FAILURE
return FAILURE
```

Initialization precedes this code, and generation precedes the sorting passes. After two exchanges src is A again. No additional full-array copy occurs. K is cleared before EVERY pass, so offsets from a previous distribution never become counts in a new pass. The all-equal-digit case is included in every work bound. There is no expected-time bucket traversal or hash-table collision assumption. Verification happens at most once; there are at most two additional compression calls, and no restart or success amplification.

## 5. Sorting correctness and recovery of distinct messages

Fix a pass. Let `c_t` be the count of digit t and `S_t=sum_(e<t)c_e`. Counting visits every record once, so the counts are nonnegative and sum to n. The prefix loop replaces each count by its exclusive prefix S_t and ends with s=n. During distribution, the `c_t` records with digit t are assigned consecutively to exactly

```
[S_t, S_t+c_t).
```

These intervals are disjoint and partition `[0,n)`. Thus every destination record is written once, no write is out of range, and the original source is not overwritten while read. Incrementing each bucket's cursor while traversing source records in increasing order makes the pass stable, including in the extreme case `c_t=n` for one digit. The final cursor for such a bucket can be n, which is why 129-bit counts are necessary.

The first pass orders the low digit. The second orders the high digit while preserving low-digit order among equal high digits. Consequently records are sorted by the entire 256-bit digest Y. Copies preserve the whole `(Y,U,V)` record, including canonical masked V. The sorted array is a permutation of the samples, including duplicate messages.

If a digest group contains at least two distinct retained pairs, its sequence must have at least one adjacent pair of different retained pairs: if every adjacent pair were equal, transitivity would make the entire group equal. The final scan therefore finds some distinct-message collision whenever one exists among the samples; identical-input pairs are merely skipped. Since hashing and sorting are exact, the two recomputations necessarily confirm digest equality. Returning unpadded serialized messages preserves distinctness because their encoding is injective. Thus the success event contains the event 'some repeated output and no repeated input' and in fact can also succeed when inputs repeat.

## 6. Distribution-free success probability

Fix the actual deterministic target function f on D. For each of M possible digests z, let `p_z=|f^-1(z)|/d`. Because input samples are independent, their outputs are independent draws from this fixed p. No independence between different collision-pair events is asserted. No uniformity of p is assumed.

For n <= M the probability that all n sampled digests differ is `n! e_n(p)`, where e_n is the elementary symmetric polynomial over the M coordinates. Here is a self-contained extremal bound. With all but two coordinates fixed, write

```
e_n = E_n + (a+b)*E_(n-1) + a*b*E_(n-2),
```

where the E terms involve the remaining coordinates and are nonnegative. Replacing a,b by their average preserves a+b and does not decrease their product, so it cannot decrease e_n. Compactness of the finite-dimensional probability simplex gives a maximizer of e_n. Choose among all maximizers one minimizing `sum_z p_z^2`, a continuous function on a compact set. If two coordinates differed, averaging them would either increase e_n, contradicting maximality, or preserve it while strictly decreasing that sum, contradicting the tie-break. Thus a maximizer is uniform. This is a theorem about the worst distribution, not a model of SHA-256.

Let E be the event of some repeated output, and F the event of some repeated input. It follows that

```
Pr(E) >= 1 - product_(i=0)^(n-1) (1-i/M)
      >= 1 - exp(-n*(n-1)/(2*M)),
Pr(F) <= n*(n-1)/(2*d).
Pr(success) >= Pr(E)-Pr(F)
            >= 1-exp(-n*(n-1)/(2*M)) - n*(n-1)/(2*d).
```

The second inequality uses `1-t <= exp(-t)` on each product factor. The input-repeat union bound uses uniform sampling of the 384-bit message, not uniformity of the hash outputs. There is no independence claim about E and F.

For n=2^128, `x=n*(n-1)/(2*M)=1/2-2^-129 > 499/1000`, and `b=n*(n-1)/(2*d)<2^-129`. The positive series for the exponential gives

```
exp(x) > 1 + 499/1000 + (499/1000)^2/2 + (499/1000)^3/6
       = 9865254499/6000000000.
exp(-x) < 6000000000/9865254499 < 609/1000.
Pr(success) > 391/1000 - 2^-129 > 39/100.
```

The submitted probability 0.39 is therefore a rigorous lower bound for a SINGLE bounded batch on the fixed selected hash. It is not a confidence score for a heuristic, not a success conditional on distinct inputs, and not an empirical extrapolation or asymptotic approximation.

## 7. Concrete ordinary-operation ledger

The algorithm uses live scalar registers in a standard word RAM; arithmetic instructions operate on word operands. A register copy, when needed, is conservatively charged as one ordinary operation. Indexed memory is not free: address addition, word load and word store are separately charged. Explicit fixed loops charge their updates, comparisons, and branches. The following generous instruction budgets cover every tape, including failures.

### Initialization

Clear all 7n words with a sequential pointer loop. The steady-state body consists of a zero store, pointer addition, comparison, and branch (four operations). Allow five per word for extra scalar traffic, hence at most 35n; use the rounded allocation 40n. Code/constants/workspace materialization, scalar initialization, constructing n/masks and array base addresses, and all fixed setup and termination over the entire program receive a further `2^20` ordinary operations. No search for a constant, characteristic or advice is omitted.

### Generation: at most 224 ordinary operations per sample

| Portion | Bound |
| --- | ---: |
| Two random-word draws, mask V, form B0/B1, associated scalar copies | 16 |
| Split B0/B1 into 16 ordinary 32-bit input words | 96 |
| Load/store eight standard IV words for the compression interface | 16 |
| Pack eight output words into Y, masking and loading every word | 64 |
| Store the three fields, advance pointers, update/test/branch the trial loop, extra bookkeeping | 32 |
| Total, in addition to the one compression | 224 |

Splitting can be done with at most six operations per field: source load/copy, right shift, mask, destination store and two spare operations. Packing can use at most eight per output field: load, mask, shift, OR and four spare operations. The selected compression includes the schedule and feed-forward, not these marshaling operations. Record stores use precomputed constant field offsets, and p advances by 3 with one addition. There is no library encoder, multiplication, uncharged random generator, or byte-buffer allocator. The 224 allocation includes compressions' call/return bookkeeping via the spare operations. For the low digit pass a shift by zero may be omitted, but it remains covered by the budgets below.

### Each radix pass: at most 88n ordinary operations

All loops keep base, pointer, end, shift and mask in scalar registers. The explicit instruction blocks below demonstrate the per-iteration upper allocations, with each semicolon-separated assignment/load/store/test/branch charged individually. `load(p)` and `store(p,x)` are one word operation each; source and destination field addresses are formed explicitly.

1. Clear K: budget 8 per counter. A zero store, p+=1, p<end and branch use four, leaving four for scalar traffic. Total <=8n.
2. Count: budget 16 per source record. A body is

```
y=load(p); d=y>>shift; d=d AND mask; a=Kbase+d;
c=load(a); c=c+1; store(a,c);
p=p+3; test(p<end); branch;
```

There are ten primitive operations, leaving six for extra scalar copies/control. Total <=16n.
3. Exclusive prefixes: budget 16 per counter. A body is

```
c=load(p); store(p,s); s=s+c;
p=p+1; test(p<end); branch;
```

There are six primitives, leaving ten spare. The old c is retained before the replacement store. Total <=16n.
4. Stable distribution: budget 48 per source record. A body is

```
y=load(p); d=y>>shift; d=d AND mask; a=Kbase+d;
j=load(a); c=j+1; store(a,c);
o=j<<1; o=o+j; q=dstbase+o;
store(q,y);
a=p+1; u=load(a); a=q+1; store(a,u);
a=p+2; v=load(a); a=q+2; store(a,v);
p=p+3; test(p<end); branch;
```

There are 22 primitive operations, leaving 26 spare for scalar moves, instruction/call bookkeeping and any loop/end/base traffic. Total <=48n. Source record pointers are advanced directly, not multiplied by 3. Every one of the three destination word stores and each address calculation is charged. No bulk-copy primitive is presumed.

Thus a pass costs <=(8+16+16+48)n=88n, and both cost <=176n. Pass setup, prefix-loop s initialization, exchanges, bounds, and fixed loop entry/exit work are in the `2^20` fixed allocation. There are exactly two passes and no expected-time loop.

### Adjacent scan: at most 32n ordinary operations

With p denoting the left record and q=p+3 the right, a mismatch costs one q addition, two digest loads, comparison and conditional branch, then pointer addition, loop comparison and branch. When digests agree, also load the two U and two V fields with four constant-offset address additions, compare both pairs, combine the Boolean results and branch. Both paths fit within 32 primitives per adjacent pair including spare scalar copies. Identical pairs are skipped without rehashing. Scan at most n-1 pairs, bounded by n. No scan-time bucket walks or hidden sorted-data reconstruction occurs.

### Final verification and fixed overhead

At most two additional selected compressions are charged. Formation, marshaling and serialization of two messages, resetting IV, packing results, checking full digest equality and message inequality, and writing outputs take fewer than `2^16` ordinary operations: even an explicit per-byte loop with 64 operations per byte for two 48-byte inputs, plus two generation-style hash interfaces and comparisons, fits that bound. Add this and ALL other fixed overhead (including program setup above, loop setup, pass exchanges, constants, scalar/output clearing, termination, and no-advice bookkeeping) under a single conservative allocation `2^20` ordinary operations. There are only a fixed number of instruction blocks, fewer than `2^15` fixed words to initialize, and only two passes. Explicit code/workspace copying and clearing with eight-operation loops twice is at most `2^19`; the remaining `2^19` easily covers the stated fixed verification and loop setup. Program instruction fetch is part of RAM instruction execution, not a separate unbounded process; any explicit data load/store and scalar copy described here is included.

Overall the per-n coefficient is

```
W <= (40+224+176+32)*n + 2^20 = 472*n + 2^20,
H <= n+2,
T = H+W/2728 <= n*(1+472/2728) + 2 + 2^20/2728.
```

This is total serial work summed over the single specified computation, not latency or amortized expected work. It includes every unsuccessful sample and batch failure. No time/memory tradeoff hides paid operations.

## 8. Scalar arithmetic, preprocessing and advice

`1+472/2728=3200/2728=400/341`. Therefore

```
log2(n*400/341) = 128 + log2(400/341)
               = 128.23022826075055... .
```

For a rigorous rounding comparison without reliance on floating point, put `r=400/341`. The convergent positive series

```
ln(r)=2*sum_(k>=0) [(59/741)^(2*k+1)/(2*k+1)]
ln(2)=2*sum_(k>=0) [(1/3)^(2*k+1)/(2*k+1)]
```

follows by integrating the geometric series for `1/(1-t^2)`. Bound the first sum from above after k=4 by adding remainder `2*(59/741)^11/[11*(1-(59/741)^2)]`. Bound ln(2) from below using its first ten positive terms (k=0,...,9). Exact rational arithmetic then gives `ln(r)/ln(2) < 230229/1000000 < 2303/10000`. These statements are elementary rational comparisons; no target experiment is needed. For example their ratio is less than 0.230228261, already below the claimed exponent.

The additive fixed allowance `F=2+2^20/2728` is less than 2^10. Its relative value to `n*r` is less than 2^-118. Using `ln(1+t)<=t` and `ln(2)>1/2`, its contribution to log2 T is less than 2^-117, much smaller than the rounding margin `0.2303-0.230229=0.000071`. Thus `T < 2^128.2303`, including fixed work and final compressions. The claim is an upper bound with a visible rounding margin, not an official measured score.

Preprocessing is explicit array/code/workspace initialization, not message generation or online counting. It is at most `(40*n+2^20)/2728`. This is less than `n/32=2^123`, since `2728/32=85.25` and `40+2^20/n<85.25`. Its work is already INCLUDED in T, not charged a second time or omitted. No advice exists; `nonuniform_advice_log2_bytes=0` is the schema's representation of an empty advice budget (at most one byte), not a free stored collision. Literal public IV, masks and loop limits belong to fixed code/constants and their initialization is paid.

## 9. Evidence and limitations

All support is analytical and self-contained in this proof. The certificate manifest is valid and empty. No experiment manifest is declared, and no participant source is to be executed to justify this claim. Mechanical package checks cannot establish this argument or emit an official score; `ready` requests remote review only. A fresh-context advisory critique is not official qualification.

The memory allocation and n=2^128 batch are physically infeasible on available machines. This limitation does not change the ideal model's bounded algorithm or permit omission of memory initialization. There is no inference from a small experiment to a large birthday regime, no PRG replacing the stipulated ideal random words, and no empirical claim about SHA-256 fibers. The success proof works for every fixed function on the specified finite domain.

The comparison is to the promoted organizer package's conservative 132 upper bound. Many unrelated cryptanalytic and generic submissions are awaiting review, including lower scalar claims; beating this promoted score does not establish that this construction is the best pending claim, nor a new security frontier. The improvement here is deterministic wide-digit sorting under unscored but fully reported memory and preserves the full-compression price of 1. The nominal reference 128 is not improved. Any changed target, probability space, advice policy, or operation pricing needs a new analysis and fresh review.
