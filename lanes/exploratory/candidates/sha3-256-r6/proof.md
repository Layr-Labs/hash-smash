# SHA3-256 prefix rounds 0–5: unconditional radix-sort birthday collision

The scalar below is `time_log2` under `collision-frontier-v5`. Memory is a
separately reported resource bound and does not affect the score.

Selected lane: exploratory. Target: `sha3-256-r6-prefix-v1`.
This finite classical algorithm has total charged time at most 2^129.0,
peak memory at most 2^136 bytes, and success probability at least 0.39.
The proposed scalar is **129.0**. It is a generic analytic construction
with infeasible resource use, not a claimed cryptanalytic advance over any
established attack. The required `baseline_improved` identifier
`sha3-256-r6-nominal-v2` identifies the organizer's nominal reference only.
That nominal display value 128 is not an established attack, qualified
baseline, or security bound; this package does not claim to improve it.

Relative to the organizer merge-sort package at 137.4, the only algorithmic
change is replacing comparison mergesort by LSD byte-radix sorting of the
256-bit digests (32 counting-sort passes). The hash, message domain,
probability argument, and cost model are otherwise the same family of
unconditional birthday search. No differential trail, no truncated-target
attack, and no heuristic about the six-round map is used.

## 1. Exact complete hash and legal messages

Let Q = 2^128 and N = 2^256. The input family D is all 64-byte strings,
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
or truncated output. Equality means all 256 output bits agree.
The six-round transformation costs one selected-target sponge permutation
under collision-frontier-v5; surrounding construction and serialization
operations are charged separately as ordinary word operations at 1/1626 each.

## 2. Algorithm, data structures and stopping rule

Use two arrays Src and Dst of Q records each. Each record is exactly three
RAM words (digest, u, v), or 96 bytes. No previous collision or
input-specific advice is supplied.

Also allocate a count array Cnt[0..255] of 256 words and a prefix array
Pos[0..255] of 256 words. These are O(1) relative to Q.

**Generate.** Initialize fixed code/constants/workspace and zero both
Q-record arrays (six word stores per index). For i = 0,...,Q-1 draw fresh
independent uniform 256-bit words u_i, v_i, compute d_i = H(u_i,v_i), and
store (d_i, u_i, v_i) in Src[i]. Charge all 2Q random draws and all hashes,
including unsuccessful samples. A deterministic seed expansion is not an
implementation of these ideal random-word calls.

**LSD byte-radix sort.** Digests are unsigned 256-bit words. For pass
k = 0,1,...,31, sort Src stably by byte digit

    digit(d,k) = (d >> (8*k)) AND 255

using counting sort into Dst, then swap the roles of Src and Dst (pointer
swap of the two array bases; no element copy). Explicitly:

1. Zero Cnt[0..255] (256 stores).
2. For i = 0..Q-1: let g = digit(Src[i].digest, k); Cnt[g] = Cnt[g] + 1.
3. Pos[0] = 0; for g = 0..254: Pos[g+1] = Pos[g] + Cnt[g]
   (256 additions; this is a standard exclusive prefix sum).
4. For i = 0..Q-1: let g = digit(Src[i].digest, k); let j = Pos[g];
   copy all three words of Src[i] into Dst[j]; Pos[g] = j + 1.
5. Swap the Src/Dst base pointers.

After 32 passes the final Src is sorted by full unsigned digest.
Q is a power of two only for notational neatness; radix sort does not
require it. Every pass is a complete stable counting sort, so equal-digest
classes become contiguous.

**Scan.** Scan adjacent records of the final Src. When two digest words
agree, compare both message words. If the messages are identical, continue.
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
fixed function in Section 1. For each of its N possible digest values y let

    p_y = |{m in D : H(m)=y}| / 2^512.

Some p_y may be zero, and no balance assumption is made. Independent uniform
messages produce independent outputs with this common distribution p,
because each output is a deterministic function of its respective input.
This fact asserts no independence among rounds or internal differences.

Here is the full finite-distribution bound. For q <= N let e_q(p) denote the
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
with q=Q and then 1-x <= exp(-x) to each factor:

    Pr(not E) <= Q! * binomial(N,Q) / N^Q
              = product_(j=0)^(Q-1) (1-j/N)
              <= exp(-Q*(Q-1)/(2*N)).

Here Q*(Q-1)/(2*N) = (2^128 * (2^128 - 1))/(2 * 2^256) = (1 - 2^{-128})/2
> 0.499999999, so Pr(E) > 1 - exp(-1/2) > 0.39346.

(The numerical inequality exp(-1/2) < 0.606531 uses the alternating Taylor
remainder for exp on [-1/2,0], or the elementary bound
exp(-1/2) < 1/(1+1/2+1/8) = 8/13 < 0.6154, already enough for > 0.3846;
the tighter 0.39346 follows from exp(-1/2) < 0.606531.)

Repeated inputs do not count as ordinary collisions. Let R be the event
that any two sampled messages are equal. Each particular pair agrees with
probability 2^{-512}; therefore the union bound gives

    Pr(R) <= binomial(Q,2)/2^512 < 2^256/(2 * 2^512) = 2^{-257} < 2^{-256}.

On E without R an equal-digest pair necessarily has distinct messages.
The scan therefore finds a valid witness. No independence between E and R
is required for

    Pr(success) >= Pr(E) - Pr(R) > 0.39346 - 2^{-256} > 0.39.

The JSON reports the weaker lower bound 0.39, above the required 0.39.
This argument works for every fixed map D to N digests, including unbalanced
ones. It uses neither a random-oracle premise nor balanced-output,
pseudorandomness, experimental extrapolation or differential independence.
This is algorithmic success, not confidence in the proof or an AI reviewer.
The heuristic list is empty.

## 4. 256-bit RAM implementation and complete charged time

Instruction budgets in this section are counts of ordinary word operations,
priced at 1/1626 each (C = reference_operation_cost for sha3-256-r6).
Permutation calls are counted separately at cost 1; their internal round
operations are not part of those instruction budgets.

All actual scalar values fit in a word: Q, indices, digit values 0..255,
Pos/Cnt entries (<= Q), 3*i, counters and byte addresses below 2^136.
The proof cardinalities N and |D| and the large total-time bounds are not
machine registers. Address record i as base + (i<<1) + i and then use
offsets 0,1,2. For byte addressing additionally shift the word address
left by five. Only listed shifts/additions are used; no multiplication
primitive is assumed. Each record is three individual loads/stores, never
a free bulk copy. There are no unbounded counters, recursion stacks or
multiword addresses.

### 4.1 Per-phase ordinary-operation envelopes

These finite envelopes deliberately overcount implementation constants.

**H wrapper (per call, excluding the permutation unit itself).**
25 zero stores, eight lane extractions from (u,v), two padding stores,
dispatch of one selected permutation, four output-lane loads, three
shifts/ORs, and call bookkeeping: at most 64 ordinary primitives.
The permutation call itself is counted separately at one
target-compression unit. Explicit copying of all 25 lanes at the
permutation interface, if charged in addition to that primitive, fits
this envelope. Every constant shift 64*j can be precomputed.

**Generate one record.** Two random-word draws, one H wrapper (64), three
record stores, loop index update and branch: at most 96 ordinary
primitives, plus one permutation unit.

**One radix pass, per record (histogram phase).** Extract digit (shift +
AND = 2), load Cnt[g], add 1, store (3), loop control (3): at most 12.
**One radix pass, per record (scatter phase).** Extract digit (2), load
Pos[g] (1), three-word record load (3), three-word record store (3),
Pos[g] += 1 (2), address arithmetic for Src/Dst (8), loop control (4):
at most 23. Combined per-record per-pass bound: 12 + 23 = 35.
Add a spare 10 for temporaries and pointer arithmetic: **45 ordinary
primitives per record per pass**.

**Per-pass O(1) work.** Zero Cnt (256 stores), prefix sum (at most 1024
operations including loads/stores/adds), pointer swap (4): at most 2^11
operations per pass, charged below as a global additive term
32 * 2^11 = 2^16, negligible beside Q-scale terms.

**Adjacent scan per inspected pair.** Two digest loads, compare, branch,
optional four message-word compares, loop control: at most 32 ordinary
primitives. Bound by 32 Q for Q-1 adjacent pairs.

**Initial zeroing.** Six word stores per index for both arrays: 6Q, well
inside a 8Q envelope.

**Fixed code load.** Straight-line/control code for generate, 32-pass
radix, scan and H wrapper needs fewer than 2^14 instructions. Five-word
encoding uses fewer than 2^17 words. Reserve a 2^24-byte fixed area.
Loading this area and clearing it costs at most 2^30 charged operations.
These are uniform data, not searched advice.

### 4.2 Totals

| Phase | Permutation calls (cost 1) | Ordinary ops (cost 1/1626) |
| --- | ---: | ---: |
| Load fixed code/constants; init fixed workspace | 0 | 2^30 |
| Zero both Q-record arrays | 0 | 8 Q |
| Draw, construct, hash and store every message | Q | 96 Q |
| 32 radix passes, per-record work | 0 | 32 * 45 Q = 1440 Q |
| 32 radix passes, O(1) count/prefix/swap | 0 | 2^16 |
| Scan all adjacent pairs | 0 | 32 Q |
| Recompute both witness hashes; verify; emit | at most 2 | 2^14 |

Summing ordinary operations:

    W <= (8 + 96 + 1440 + 32) Q + 2^30 + 2^16 + 2^14
       = 1576 Q + 1073758208 + 65536 + 16384
       = 1576 Q + 1073840128.

    H_calls <= Q + 2
    T = H_calls + W/1626
      <= Q + 2 + 1576 Q / 1626 + 1073840128/1626
       = Q (1 + 1576/1626) + 2 + 660417.05...
       = Q (3202/1626) + 660419.05...
       = Q (1601/813) + 660419.05...

Now 1601/813 < 1.96925, and for Q = 2^128:

    T < 1.96925 * 2^128 + 660420
      < 1.96925 * 2^128 + 2^20
      < 1.9693 * 2^128
      < 2^129.0,

because 1.9693 < 2 and log2(1.9693) < 0.978 < 1, so
1.9693 * 2^128 < 2^129. More tightly,
log2(1.96925) < 0.9778, hence T < 2^{128.978} < 2^{129.0}.

The integer check 1601/813 * 2^128 + 660420 < 2^129 is equivalent to
1601/813 * 2^128 + 660420 < 2^129, i.e.
1601 * 2^128 + 660420 * 813 < 813 * 2^129,
i.e. 1601 * 2^128 + 536921460 < 813 * 2^129.
Since 813 * 2 = 1626 > 1601, the leading terms alone give a gap of
25 * 2^128, far larger than 536921460.

Thus T < 2^{129.0}. The claimed scalar is 129.0.

Preprocessing is fixed initialization plus array zeroing, already in T:

    P <= (8 Q + 2^30)/1626 < 2^{128} * 8/1626 + 2^{30}/1626
       < 2^{119} + 2^{20} < 2^{131}.

The retained `preprocessing_log2: 131` is a loose independent upper bound.
Actual preprocessing is included in T; the metadata does not assert that
setup alone takes 2^131 units.

No earlier search chooses messages, favorable coins, collisions, parameters
or advice. No failed trials or preparation steps are left outside T.
These are worst-case bounds for one run, hence also bound expected time.

## 5. Memory, data and interpretation of the claim

Each array occupies 3Q words = 96Q bytes, including every retained 64-byte
message and 32-byte full digest. Both arrays total 6Q words = 192Q bytes.
Cnt and Pos use 512 words = 2^{14} bytes. Retained random words are the
stored message words, not another allocation. Uniform code/constants,
copying temporaries, state, counters, output and other fixed data all fit
in the 2^{24}-byte area justified above.

    M <= 192 Q + 2^{14} + 2^{24}
       = 192 * 2^{128} + 2^{14} + 2^{24}
       < 2^8 * 2^{128} = 2^{136} bytes.

(192 < 256 = 2^8.) This is within 256-bit byte or word addressing. It is
not constant memory or a statement of physical practicality.

The JSON fields have these explicit units and meanings:

* `time_log2: 129.0` means T <= 2^{129.0} target-compression units of total work.
* `memory_log2_bytes: 136` means M <= 2^{136} peak bytes, including code.
* `data_log2: 129` means at most Q+2 < 2^{129} complete-message hash
  evaluations including both final verification evaluations.
  All messages are generated internally; external input data is zero.
* `preprocessing_log2: 131` means P < 2^{131} target-compression units of
  setup, already included in T, not an extra omitted phase.
* `success_probability: 0.39` is a proved one-batch lower bound.
* `nonuniform_advice_log2_bytes: 0` bounds advice by 2^0 bytes.
  Actual nonuniform advice is zero bytes. The schema cannot encode log2(0),
  so the nonnegative value 0 is a conservative upper bound, not a hidden
  precomputed collision. Uniform program/constants are charged above.

Resource logarithms describe conservative upper bounds; success describes
a lower bound. The proposed scalar is 129.0. No scalar improvement or Pareto
dominance over an established attack is claimed. Compared with the prior
organizer merge-sort package (137.4), this package reduces sort work from
128 comparison-merge passes of three-word records to 32 byte-radix
counting-sort passes, which is why the charged total drops by about eight
bits while remaining fully unconditional.

## 6. Evidence, heuristic disclosures and limitations

All needed evidence is the self-contained analytic argument in Sections
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

Literature context (not used as a numeric premise): to our knowledge no
classical ordinary-collision attack on six-round SHA3-256 below the
birthday bound is published. Known six-round collision results in the
Keccak/SHA3 line are quantum (out of scope) or apply to other digests /
near-collisions. This package stays at the generic birthday cost with
tightened sorting accounting.

`ready` means complete and available for review. Qualification and score
emission require organizer review of this exact package.
Exploratory qualification is `plausible_not_refuted`; rigorous qualification
is `ai_rigor_qualified`. Neither is mathematical proof or human acceptance.
This candidate does not assert a review outcome, trusted score or successful
Yukon baseline import.

## 7. Provenance

This package replaces the local organizer-style merge-sort birthday claim
at time_log2 137.4 in the same editable path. The complete hash, 64-byte
message encoding, three-word records, unconditional Schur-style birthday
probability proof, and collision-frontier-v5 pricing (C = 1626) are
retained. The sorting subroutine is new (LSD byte radix). The success
threshold is set to the required 0.39 with Q = 2^{128} rather than the
previous Q = 2^{129} margin for probability 1/2. This new package requires
fresh ordinary review and asserts neither an inherited qualification nor
a structural cryptanalytic algorithm.
