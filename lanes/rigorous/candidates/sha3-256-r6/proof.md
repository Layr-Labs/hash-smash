# SHA3-256 prefix rounds 0 through 5: unconditional generic collision package

Selected lane: rigorous. Target: `sha3-256-r6-prefix-v1`.
This finite classical algorithm has total charged time at most 2^150,
peak memory at most 2^138 bytes, and success probability at least 1/2.
The proposed scalar is 150 + 138 = 288. It is a generic analytic construction
with infeasible resource use, not a claimed cryptanalytic advance.
The required `baseline_improved` identifier `sha3-256-r6-nominal-v2`
identifies the organizer's nominal reference only. That nominal 128 is not
an established attack, qualified baseline, or security bound; this package
does not claim to improve it.

## 1. Exact complete hash and legal messages

Let Q = 2^129 and N = 2^256. The input family D is all 64-byte strings,
so |D| = 2^512. Every message has legal bit length 512 < 2^64.
Represent a message by two 256-bit words u,v and serialize it as
LE32(u) || LE32(v), where LE32 writes exactly 32 little-endian bytes,
including zero bytes. This is a bijection from pairs of words onto D.
N and |D| are mathematical cardinalities used only in the proof; the
algorithm never stores either of those out-of-word-range integers.

The selected complete hash has a 1600-bit state, rate 1088 bits (136 bytes),
capacity 512, the all-zero initial state, and full 256-bit output.
Each such message's entire padded input is exactly one 136-byte block:

    LE32(u) || LE32(v) || 06 || (00 repeated 70 times) || 80

This is the SHA3 domain suffix 01 and pad10*1, using delimited suffix 0x06.
There is exactly one absorption permutation, no extra squeezing permutation,
and no Davies-Meyer feed-forward.

The complete subroutine H(u,v) is as follows. Store the state as 25 lanes,
each in the low 64 bits of a separate RAM word; upper bits are zero.
The lane index is x+5y for 0 <= x,y < 5, in little-endian lane order.
Set all 25 lanes A to zero, then for j = 0,1,2,3 set

    A[j]   = (u >> (64*j)) AND (2^64-1)
    A[j+4] = (v >> (64*j)) AND (2^64-1).

Set A[8] = 0x06 and A[16] = 0x8000000000000000.
These are precisely the padded rate block XORed into the all-zero state.
Lanes 17 through 24 remain the zero capacity portion.

Apply exactly the first six Keccak-f[1600] rounds, indices 0 through 5.
For each round use the following stages; within a stage assignments are
simultaneous, and each stage reads the preceding one. Subscripts x,y are
modulo 5. All lane arithmetic is on 64 bits, with NOT64 and rot64 restricted
to those bits, not the entire 256-bit RAM word.

    C[x] = A[x,0] XOR A[x,1] XOR A[x,2] XOR A[x,3] XOR A[x,4]
    D[x] = C[x-1] XOR rot64(C[x+1],1)
    T[x,y] = A[x,y] XOR D[x]
    B[y,2*x+3*y] = rot64(T[x,y],rho[x,y])
    Anew[x,y] = B[x,y] XOR ((NOT64 B[x+1,y]) AND B[x+2,y])
    A = Anew
    A[0,0] = A[0,0] XOR RC[round]

The rho offsets, listed in x+5y order, are

    0, 1,62,28,27, 36,44, 6,55,20, 3,10,43,25,39,
    41,45,15,21, 8, 18, 2,61,56,14.

Use these six RC constants in this order:

    0x0000000000000001, 0x0000000000008082,
    0x800000000000808A, 0x8000000080008000,
    0x000000000000808B, 0x0000000080000001.

Return

    d = A[0] OR (A[1] << 64) OR (A[2] << 128) OR (A[3] << 192).

LE32(d) is exactly the first 32 squeeze bytes, hence the full target digest.
This is the fixed prefix-round complete hash, not Keccak-p's last-round
convention, raw permutation hashing, a free initial state, different padding,
or truncated output. Numeric ordering of d in the search changes no equality
test: equality means all 256 output bits agree.
The six-round transformation costs one selected-target sponge permutation
under collision-frontier-v3; surrounding construction and serialization
operations are charged separately.

## 2. Algorithm, data structures and stopping rule

Use two arrays A and B of Q records each, unrelated to H's small local lane
array. Each record is exactly three RAM words (digest,u,v), or 96 bytes.
No previous collision or input-specific advice is supplied.

Initialize fixed code/constants/workspace and zero all 6Q table words.
For i = 0,...,Q-1 draw fresh independent uniform 256-bit words u_i,v_i,
compute d_i=H(u_i,v_i), and store (d_i,u_i,v_i) in A[i].
Charge all 2Q random draws and all hashes, including unsuccessful samples.
A deterministic seed expansion is not an implementation of these ideal
random-word calls.

Sort all records by unsigned full-digest word using iterative bottom-up
mergesort. Initially source=A, destination=B and width=1.
For each width<Q merge consecutive pairs of width-record runs, copy every
three-word record to destination, swap source/destination and double width.
Q is a power of two, so all pairs are complete and there are exactly 129
passes, with widths 1,2,...,2^128. For each start s=0,2*width,...,Q-2*width,
perform this merge:

    left=s; left_end=s+width; right=left_end; right_end=s+2*width; out=s
    while out<right_end:
        if left==left_end: chosen=right; right=right+1
        else if right==right_end: chosen=left; left=left+1
        else if source[left].digest <= source[right].digest:
            chosen=left; left=left+1
        else: chosen=right; right=right+1
        destination[out] = all three words of source[chosen]
        out=out+1

The chosen index is saved before incrementing its left/right counter.
Taking from the left on ties is deterministic. No recursion, hashed lookup,
expected sorting bound, integer multiplication primitive, or variable-size
integer representation is needed.

Scan adjacent records of the final source. When two digest words agree,
compare both message words. If the messages are identical, continue.
If they differ, recompute H for both from fresh all-zero states, check full
digest equality, and output the two 64-byte messages.
On verification failure output failure; this branch is unreachable under
exact RAM semantics. If the scan ends without a witness, output failure.
There is one complete batch and no restart or amplification.

Sorting preserves every record and makes each equal-digest class contiguous.
If a class contains distinct messages, some adjacent messages differ:
otherwise transitivity of equality would make the whole class one message.
Thus the algorithm succeeds exactly when its sample contains distinct
messages with equal target digests. Every output satisfies the exact
ordinary-collision relation by distinctness and complete-hash recomputation.

## 3. Unconditional success for this fixed function

The only randomness is the 2Q independent uniform RAM words. H remains the
fixed function in section 1. For each of its N possible digest values y let

    p_y = |{m in D : H(m)=y}| / 2^512.

Some p_y may be zero, and no balance assumption is made. Independent uniform
messages produce independent outputs with this common distribution p,
because each output is a deterministic function of its respective input.
This fact asserts no independence among rounds or internal differences.

Here is the full finite-distribution bound. For q<=N let e_q(p) denote the
sum of products of probabilities over all q-element subsets of coordinates.
The probability of all q sampled outputs being distinct is q! e_q(p).
Hold all coordinates except a,b fixed, and keep a+b fixed. Then

    e_q(p) = a*b*e_(q-2)(rest) + (a+b)*e_(q-1)(rest) + e_q(rest),

where e_0=1 and impossible-size coefficients are zero.
All coefficients are nonnegative, so replacing a,b by their mean cannot
decrease e_q: their product increases at fixed sum.
To obtain a global maximum rigorously, e_q attains one on the compact
probability simplex. Among maximizers choose one minimizing sum p_i^2.
If two of its coordinates differ, averaging them does not decrease e_q
and strictly decreases the sum of squares, a contradiction.
Therefore the uniform vector maximizes e_q, including over distributions
with zero coordinates. No limiting repeated-averaging step is assumed.

Let E be the event that some two sampled digests agree. Apply this inequality
with q=Q and then 1-x<=exp(-x) to each factor:

    Pr(not E) <= Q! * binomial(N,Q) / N^Q
              = product_(j=0)^(Q-1) (1-j/N)
              <= exp(-Q*(Q-1)/(2*N)).

Here Q*(Q-1)/(2*N)=2-2^-128>1, so Pr(E)>1-exp(-1).
Since exp(1)>1+1+1/2+1/6=8/3, we have exp(-1)<3/8 and Pr(E)>5/8.

Repeated inputs do not count as ordinary collisions. Let R be the event
that any two sampled messages are equal. Each particular pair agrees with
probability 2^-512; therefore the union bound gives

    Pr(R) <= binomial(Q,2)/2^512 < 2^258/(2*2^512) = 2^-255 < 1/8.

On E without R an equal-digest pair necessarily has distinct messages.
The scan therefore finds a valid witness. No independence between E and R
is required for

    Pr(success) >= Pr(E)-Pr(R) > 5/8-1/8 = 1/2.

The JSON reports the weaker lower bound 0.5, above the required 0.39.
This argument works for every fixed map D to N digests, including unbalanced
ones. It uses neither a random-oracle premise nor balanced-output,
pseudorandomness, experimental extrapolation or differential independence.
This is algorithmic success, not confidence in the proof or an AI reviewer.

## 4. 256-bit RAM implementation and complete charged time

All actual scalar values fit in a word: Q, widths, indices, endpoint Q,
3*i, 6*Q, counters and byte addresses below 2^138. The proof cardinalities
N and |D| and the large total-time bounds are not machine registers.
Address record i as base+(i<<1)+i and then use offsets 0,1,2.
For byte addressing additionally shift the word address left by five.
Only the listed shifts/additions are used; no multiplication is assumed.
Each record is three individual loads/stores, never a free bulk copy.
There are no unbounded counters, recursion stacks or multiword addresses.

The following finite envelopes deliberately overcount implementation
constants. For one merge output, source/destination addressing uses fewer
than 20 additions/shifts. Two digest loads, three record loads, three
record stores, eight comparisons/branches and eight counter operations
suffice. Setup/end control is fewer than 32 additional operations per
nonempty run pair, chargeable to its first output. These total below 128.
Including loads/stores for every scalar temporary and pointer swap gives
a conservative bound of 512 primitives per output before fetch allowance.
The adjacent scan likewise fits in 512 primitives per inspected pair.

For H, 25 zero stores, eight lane extractions, two padding stores, one
selected permutation, four output-lane loads, three shifts/ORs and call
bookkeeping total below 512 primitives. The two random draws and three
record stores also fit within 512 per generated record. Explicit copying
of all 25 lanes at the permutation interface, if charged in addition to
that primitive, fits this envelope. Every constant shift 64*j can be
precomputed; no variable integer multiplication is needed.

An elementary instruction and literal operands can be encoded in at most
five RAM words: opcode and at most four operands. Allow five additional
charged instruction-fetch loads for each instruction. The 512-operation
bound becomes 3072; round upward to 4096=2^12 per record below.
These fetches are conservatively charged even if the model would not
separately charge them. No operating system, Python objects, allocator
metadata or library sorting implementation is being assumed.

The uniform program has the fixed loop bodies specified above. Its
elementary straight-line/control code needs fewer than 2^14 instructions.
Even if the selected primitive's code storage is included, six rounds of
25 lanes require fewer than this number: fixed lane coordinates eliminate
modulo/index computations, and each round uses fewer than 1024 elementary
instructions for the displayed XOR, rotation, chi, loads and stores.
All six rounds plus the generation, merge, scan and loop bodies remain
below 2^14 instructions. Five-word encoding uses 81920 words.
Constants, counters, temporary records, output and working lanes together
use fewer than 4096 further words, totaling less than 2^17 words.
Reserve the larger 2^24-byte fixed area for all of them.
Loading this code/constants and clearing the fixed area costs at most
2^30 charged operations. These are uniform data, not searched advice.

| Phase | Worst-case charged units including addressing, loops and fetches |
| --- | ---: |
| Load fixed code/constants and initialize fixed workspace | 2^30 |
| Zero both Q-record arrays, six word stores per record index | 2^12 Q |
| Draw, construct, hash and store every message | 2^12 Q |
| Every copy in all 129 bottom-up merge passes | 129 * 2^12 Q |
| Scan all adjacent pairs, including repeated-message checks | 2^12 Q |
| Recompute both witness hashes, verify and emit output or failure | 2^14 |

Explicit table zeroing is easily within 512 primitives per index before
fetch allowance, so allocation assumes no free zero-fill.
The table charges all samples, failed comparisons, merge passes and
verification regardless of success. There is no hidden restart cost.
These are worst-case bounds for one run, hence also bound expected time.

    T <= 132 * 2^12 Q + 2^30 + 2^14 < 2^21 Q = 2^150.

The organizer unit is named `target-compressions`: one selected six-round
sponge permutation costs one unit and each other listed primitive word
operation costs one unit. T is not merely the number of hashes.
Preprocessing is the fixed initialization and array zeroing, already
included in T:

    P <= 2^12 Q + 2^30 < 2^142.

No earlier search chooses messages, favorable coins, collisions, parameters
or advice. No failed trials or preparation steps are left outside T.

## 5. Memory, data and interpretation of the claim

Each array occupies 3Q words = 96Q bytes, including every retained 64-byte
message and 32-byte full digest. Both arrays total 6Q words = 192Q bytes.
Retained random words are the stored message words, not another allocation.
Uniform code/constants, copying temporaries, state, counters, output and
other fixed data all fit in the 2^24-byte area justified above.
There are no additional table copies, external storage, recursive stacks,
compressed messages or retained randomness outside those areas.

    M <= 192Q + 2^24 = 192 * 2^129 + 2^24 < 2^138 bytes.

This is within 256-bit byte or word addressing. It is not constant memory
or a statement of physical practicality.

The JSON fields have these explicit units and meanings:

* `time_log2: 150` means T <= 2^150 total charged operations.
* `memory_log2_bytes: 138` means M <= 2^138 peak bytes, including code.
* `data_log2: 130` means at most Q+2 < 2^130 complete-message hash
  evaluations including both final verification evaluations.
  All messages are generated internally; external input data is zero.
  Their 64-byte input traffic is at most 64(Q+2) < 2^136 bytes.
  Repeated table traffic is accounted for in time and memory above.
* `preprocessing_log2: 142` means P < 2^142 charged setup operations,
  already included in T, not an extra omitted phase.
* `success_probability: 0.5` is a proved one-batch lower bound.
* `nonuniform_advice_log2_bytes: 0` bounds advice by 2^0 bytes.
  Actual nonuniform advice is zero bytes. The schema cannot encode log2(0),
  so the nonnegative value 0 is a conservative upper bound, not a hidden
  precomputed collision. Uniform program/constants are charged above.

Resource logarithms describe conservative upper bounds; success describes
a lower bound. The proposed scalar is 288. No scalar improvement or Pareto
dominance over an established attack is claimed.

## 6. Evidence, heuristic disclosures and limitations

All needed evidence is the self-contained analytic argument in sections
1 through 5. The heuristic list is empty: every material probability and
resource premise is discharged for the fixed target and stipulated RAM.
Fresh independent uniform random words are an explicit model primitive,
not an empirical assumption about a device or deterministic PRNG.
No smaller-round experiment or sibling package is needed for this proof.
There are no toy-to-full-size extrapolations or unexplained cryptanalytic
premises, and no external link must be fetched to assess the argument.

The certificate manifest is valid and empty. No computed collision or
certificate is claimed. No experiment is declared, and no candidate
program has been executed. Finite sampling would not establish the costs
or success of this infeasible run and is not used as evidence.
This is an analytic upper bound in the abstract model, not a measured
practical attack.

`ready` means complete and available for review. Qualification and score
emission require organizer review of this exact package.
Exploratory qualification is `plausible_not_refuted`; rigorous qualification
is `ai_rigor_qualified`. Neither is mathematical proof or human acceptance.
This candidate does not assert a review outcome, trusted score or successful
Yukon baseline import.
