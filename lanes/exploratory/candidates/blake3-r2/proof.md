# Seven guarded lanes for complete BLAKE3-r2 collisions

## 1. Scope, provenance and claim

This exploratory analytical algorithm claims total charged work below
2^126.362 compression equivalents and peak memory below 2^167 bytes, with
algorithmic success probability at least 0.39 conditional on the expressly
listed table heuristic Htable. It is a generic birthday construction, not a
new differential attack, practical collision, or proof of BLAKE3 insecurity.

Prior public unpromoted research materially informs this package: jaazinn's
0a5b7ae8 introduced a sparse-set birthday search; winglock's 3022205 refined
the five-word key and table; ercumentyildirim's b2508e2 combined independent
messages with eight densely packed lanes and confined the heuristic to table
failure events. These contributions are credited as co-authors. The new
contribution here is SEVEN 32-bit fields at STRIDE 36, with four guard bits,
so ordinary addition followed by ONE packed mask replaces six-operation
carry-isolated dense addition. This is independently written code and an
explicit new resource argument, not an adoption of their unchecked counts.

No imported participant code is executed on the host. Declared Python is
executed only by the organizer's bounded networkless Docker executor.
The finite experiments test projections and do not establish the full-width
Htable premise. Independent input sampling makes the full-collision existence
bound distribution-free; only collision recovery through the partial key is
heuristic. The reference ID blake3-r2-nominal-v2 is required metadata and does
not assert superiority to an established 128-bit attack.

## 2. Exact complete-message target

Every message has exactly 64 bytes. Interpret its bytes as sixteen little
endian 32-bit words m0,...,m15. It lies in the required bit-length-below-2^64
domain. Standard unkeyed BLAKE3 on this domain has one chunk and one block,
no parents, counter zero, true block length 64 and root flags
CHUNK_START|CHUNK_END|ROOT = 11. Start with state

    v0..v7 = IV
    v8..v11 = IV0..IV3
    v12..v15 = 0,0,64,11
    IV = 6a09e667 bb67ae85 3c6ef372 a54ff53a
         510e527f 9b05688c 1f83d9ab 5be0cd19.

One G(a,b,c,d,x,y), all additions modulo 2^32, is

    a=a+b+x; d=ROR32(d XOR a,16); c=c+d; b=ROR32(b XOR c,12)
    a=a+b+y; d=ROR32(d XOR a,8);  c=c+d; b=ROR32(b XOR c,7).

The eight calls each round, in order, use

    (0,4,8,12,m0,m1)     (1,5,9,13,m2,m3)
    (2,6,10,14,m4,m5)    (3,7,11,15,m6,m7)
    (0,5,10,15,m8,m9)    (1,6,11,12,m10,m11)
    (2,7,8,13,m12,m13)   (3,4,9,14,m14,m15).

After the first round only, permute message indices by
(2,6,3,10,7,0,4,13,1,11,12,5,9,14,15,8). Execute the second
round and stop. The first eight output words are oi=vi XOR v(i+8).
Their little endian concatenation is the entire 256-bit digest. The last
eight compression output words need not be computed because root output
uses only the first 32 bytes. This retains IV, flags, feed-forward and full
output, and is an ordinary collision of the complete selected target.

## 3. Guarded arithmetic, exact for all messages

Let B=sum(j=0..6) 2^(36j), M=(2^32-1)B. Represent seven values as
X=sum xj 2^(36j), with every xj in [0,2^32). The largest occupied bit is
247, so all inputs fit a 256-bit RAM word. A two-input or three-input sum
has each unmasked field below 3*2^32 < 2^34 < 2^36. No carry reaches the
next field; the highest temporary occupied bit is at most 249. Thus

    ADD2(X,Y)=(X+Y) AND M                     (2 ordinary ops)
    ADD3(X,Y,Z)=(X+Y+Z) AND M                 (3 ordinary ops)

compute seven independent modular sums exactly, including all carry cases.
The guard bits are cleared after EVERY addition; this is not lazy reduction.
XOR acts independently in the seven fields in one ordinary operation.

For r in {7,8,12,16}, define the public constant masks

    Rr=(2^(32-r)-1)B
    Lr=((2^r-1) << (32-r))B.
    ROT(X,r)=((X >> r) AND Rr) OR ((X << (32-r)) AND Lr).

Each mask contains only bits of its own fields. The right mask discards all
incoming bits from the next field and keeps bits r..31 shifted down. The
left mask discards outgoing bits from the previous field and retains only
the low r bits of the current field shifted up. Their retained bits are
disjoint and union to a 32-bit rotation. Although the RAM left shift truncates
at bit 256, the highest retained position is bit 247 and cannot be lost.
This uses two shifts, two ANDs and one OR: FIVE operations, never four.

Induction over all G assignments proves bit-for-bit agreement in every lane
with the target in Section 2, for every possible seven-message batch. State
initialization repeats each public constant using B; actual production code
precomputes those constants. The message permutation changes statically
selected register operands in straight-line code; it is not a runtime
copy or a Python list operation in the counted RAM program.

Per G, the two triple additions cost 6, the two double additions cost 4,
the four XORs cost 4, and the four rotations cost 20. Total 34, hence sixteen
G calls cost 544. Eight output XORs cost 8. FULL digest cost is 552 per
seven independent messages. This differs from tightly packed eight-field
addition, which needs extra carry suppression for each addition.

## 4. Sampling, retained state and recovery

Set N=2^128 and batches b=0,...,ceil(N/7)-1. In each batch draw sixteen
fresh independent uniform 256-bit random words Ui. Set Wi=Ui AND M and
store the sixteen Wi words in a retained message array at base A+16b+i.
Their 112 used 32-bit fields are independent uniform words, since disjoint
bits of independent uniform words are independent. Thus all seven messages
of every batch are independent uniform 512-bit messages. Use only the first
N messages; at most six excess hashes in the last batch are still charged.
There is no PRNG or assumption of independently random hash rounds in the
production probability space. Seeded SHAKE expansion belongs to experiments
only and does not implement the ideal random-word primitive.

Read the sixteen Wi into fixed working registers, initialize the sixteen
state registers using public packed constants, and evaluate Section 3.
For lane j form K from words o0..o4, a 160-bit key. For j>0, extraction is
one shift and one mask for each of five words (10 operations), followed by
four shifts and four ORs to concatenate them (8). Lane zero costs less.
Charge 18 operations per lane. Every full-digest collision has equal K.
The integer message ID is z=7b+j in generation order; a single increment
maintains z, including when a message is discarded after key recovery.

For any stored ID z, recover b=floor(z/7), j=z mod 7 without an unavailable
unit-cost division. Binary long division of a 128-bit integer by the fixed
constant 7 takes 128 rounds; each round costs at most 7 word operations
(shift/mask bit extraction, shift/add remainder, compare, conditional subtract,
quotient bit update). Fewer than 1024 ordinary operations suffices per ID.
Use <=4096 operations for TWO IDs, message loads, unpacking, distinctness,
full digest comparisons and all handler control. Two complete root hashes
are additionally charged as two whole target compressions per confirmation.
No successful collision is accepted without these checks.

## 5. Sparse-set collision table, including arbitrary initial memory

The table uses a separate sparse segment S=2^160 + K, one word per key.
Dense record j occupies addresses 2j and 2j+1: (K, message ID). Maintain
record count c starting at zero. All dense records are written before c
is incremented. Dense addresses are less than 2N. The sparse segment lies
above all other arrays. No sparse segment initialization is assumed free;
instead its arbitrary preexisting contents are permitted and validated.

At each key K, perform the following RAM program. Every listed load, store,
comparison, branch, arithmetic and logical operation is charged:

    s = (2^160) OR K                         1
    p = LOAD(s)                             1
    if p < c:                               compare + branch = 2
        q = p << 1                          1
        h = LOAD(q)                         1
        if h == K:                          compare + branch = 2
            old = LOAD(q+1)                 add + load = 2
            run bounded confirmation; continue
    q = c << 1                              1
    STORE(q,K)                              1
    STORE(q+1,z)                            add + store = 2
    STORE(s,c)                              1
    c = c + 1                               1

The worst inserting path is 14 operations, not counting the MATCH handler
which is charged separately. Allow 18 ordinary operations per message to
include an explicit jump/continuation and bounded table-control overhead.
No word combines 160 key bits with a 128-bit ID in 256 bits: TWO dense
words are deliberately used. Only valid dense indices are dereferenced.

If K was inserted, its sparse pointer refers to a written dense entry with
that exact K. If its sparse word is garbage, either its pointer fails p<c,
or its pointed-to WRITTEN key differs from K, or a written record actually
has K. The last case is a legitimate earlier candidate, never a false
positive due to uninitialized memory. Keys never move, and insertion only
occurs if that exact key has no existing dense record. There is no displacement
or overwrite by a different key because sparse indexing is the FULL key.
Distinct messages with an equal partial key are confirmed independently;
keep the first representative of the key after an unsuccessful confirmation.
Stop with failure when more than L=2^110 confirmations would be needed.
Stop with a collision on the first valid full match; otherwise halt after N
messages. Every run has the same deterministic work cap.

## 6. Distribution-free full-collision existence

Let D have size 2^512, Q=2^256. For iid uniform messages, digest distribution
p_y=|H^-1(y)|/|D| need not be uniform. Independence of the digest samples
follows from independent messages and a fixed deterministic H. The probability
that all N outputs are distinct is N! e_N(p), the elementary symmetric
polynomial. Uniform p maximizes it: averaging two unequal coordinates changes
the polynomial by increasing their product times a nonnegative coefficient,
while preserving their sum. Among maxima choose one minimizing sum p_y^2;
any unequal coordinates then contradict minimality. Hence

    Pr[no output collision]
      <= product(j=0..N-1)(1-j/Q)
      <= exp(-N(N-1)/(2Q))
       = exp(-(1-2^-128)/2) < 0.606530660.

The last numerical slack is strict at this N; the difference from exp(-1/2)
is below 2^-128, far smaller than the displayed 2.8e-10 slack.
The union bound for repeated INPUTS is

    Pr[any identical inputs] <= N(N-1)/(2*2^512) < 2^-257.

Thus a distinct-message complete-hash collision exists with probability
at least 0.393469340 - 2^-257 for every fixed target function. This is an
unconditional finite counting bound, not a random-oracle premise. Identical
inputs are never returned because final confirmation tests distinctness.

## 7. Table failure events and declared heuristic

Existence does not guarantee recovery using one representative per PARTIAL
key. Two potential losses are explicitly distinguished:
Finterference: an earlier different-digest member squats the key of a later
full-colliding pair; Fcap: more than L key confirmations are needed.

In the iid uniform DIGEST model (only here a heuristic about the fixed H),
for three distinct sample indices, event Dx=Dz and Ky=Kx has probability
2^-256 * 2^-160 = 2^-416. At most N^3 ordered triples give

    Pr[Finterference] <= N^3/2^416 = 2^-32.

Using this deliberately looser ordered-triple bound avoids needing a factor
one-half convention. Expected equal-key PAIRS is less than N^2/2^161=2^95.
The number of actual confirmations is no larger than the number of equal-key
pairs; Markov gives

    Pr[Fcap] <= 2^95/2^110 = 2^-15.

Under these model values, success is at least
0.393469340 - 2^-257 - 2^-32 - 2^-15 > 0.3934388.
Htable permits an additional TOTAL 0.003 failure-probability deviation in
the two table events for the fixed selected target. Therefore success remains
above 0.3904388 > 0.39. This allowance is part of the HEURISTIC, not a
statistically certified margin. The claim object states the scope and limitation;
its use of a 2^-33 illustrative model bound should be read conservatively as
the explicit 2^-32 ordered bound here. We do not claim an unconditional
success theorem for the sparse table or a mathematically established Htable.

## 8. Relevant finite experiment support and its limits

Two declared experiments use 1024 deterministic seed-expanded messages, seven
packed lanes, the actual two-round target and 20-bit output events:
spread four bits over each of o0..o4, or concentrate all 20 bits in o0.
The source also compares each lane of the first batch of every trial against a separately written
scalar compression and reports mismatches as UNTRUSTED observations. Organizer
trusted hashing independently checks every returned projected-collision pair.
A projected collision is NOT a full-width collision. The random-model collision
probability at this scale is approximately 1-exp(-1024*1023/2^21)=0.39317.

These experiments are relevant to concentration and cross-lane artifacts in
selected key projections; they do not measure rare 160/256-bit triple events
at N=2^128, prove iid uniform digests, or certify the 0.003 heuristic allowance.
The logical field arithmetic proof in Section 3, rather than sampled outputs,
supports evaluator correctness. The organizer's experiment report is fresh
bound evidence; no participant-generated report or fabricated result is supplied.

## 9. Total work: every instruction category counted

The RAM is classical with 256-bit words. One target compression costs 1;
every other primitive costs 1/430. The production evaluator is an explicit
straight-line sequence for each of the sixteen G calls, with statically fixed
round-two operand names and fixed public masks. There is no unit-cost library
hash, packing, sorting, division or unspecified lookup. No target compression
is charged in addition to its explicitly evaluated ordinary operations.

Per batch (at most seven messages):

| Item | ordinary operations |
|---|---:|
| Draw sixteen uniform random words, mask, retain (16 each) | 48 |
| Address arithmetic for sixteen retained stores (unrolled, base+i) | 16 |
| Load sixteen message words and set sixteen initial-state registers | 48 |
| Sixteen G calls, 34 each | 544 |
| Eight output XORs | 8 |
| Batch base advancement and batch control | 12 |
| Total independent of individual lane table handling | 676 |

Registers hold sixteen message words, sixteen evolving state words, eight
outputs (they reuse dead state registers), constant masks and table variables.
Fewer than 64 live registers suffice, including shift counts and fixed bases.
Ordinary assignments that simply choose register destinations are instructions
already represented by the primitive producing that register. Initial-state
copies are expressly charged above; no uncharged arbitrary register array is
used. Constants including rotation masks and IV occupy fixed storage and are
preloaded into fixed registers; no amortized per-message operand decoding or
instruction-fetch charge is part of this RAM's published primitive model.

Per message, key extraction <=18, table <=18, ID increment 1, and lane/last-batch
control <=4: <=41. A seven-way straight-line unroll therefore costs at most
676+7*41=963 per full batch, or 137.572 per message. Charge 138 per message,
leaving 0.428 operations of margin. The last partial batch costs at most another
963 ordinary operations; all unused samples and hashes are included. No average
hardware latency or vector throughput is substituted for summed total work.

The confirmation handler costs <=4096 ordinary operations and two whole
compressions per key match, with at most L=2^110 matches. Fixed code,
constants, storage setup, counters and all public-mask construction are charged
<=2^20 ordinary operations. Random masks can be built in seven unrolled
shift/OR steps; no large precomputed table or target advice is involved.
No sparse-array zeroing is needed by Section 5, and retained message/dense
arrays are written before use. Their writes are in the ledger above.

Consequently every execution has

    T <= (138*N + 963 + 2^20)/430
         + 2^110*(2+4096/430)
      < (138/430 + (2+4096/430)/2^18 + 2^-100) * 2^128
      < 0.320975 * 2^128
      < 2^126.362.

This gives the submitted rounded-up scalar. Preprocessing <=2^20/430
is included already and preprocessing_log2=20 is a loose standalone bound.
No restart, success amplification or uncharged failed trial is omitted.
No supplied collision or nonuniform advice is used; advice is zero and the
schema field 0 denotes an allowed cap of one byte rather than log2(0).

## 10. Memory, boundaries and recovery layout

Dense records start at word address 0 and use <2^129 words. Retained batches
start at A=2^130 and use 16*ceil(N/7)<3N words, ending below 2^131.
Code, constants, working spills, output and counters are placed at 2^132
with fewer than 2^20 words, below 2^133. Sparse words occupy
[2^160,2^161); all segments are disjoint. Every address and counter is a
256-bit representable integer. Byte addresses stay below 2^166; the reported
2^167 cap includes the entire sparse address span, not merely touched memory.
Byte-addressed implementations multiply word indices by 32 via one shift;
that is a constant interpretation of the word-addressed RAM. If every memory
reference instead requires an extra runtime byte-address shift, charge up to
seven more ordinary operations per message; this alternate conservative
reading gives <2^126.44 and still improves the 126.67 candidate benchmark.
Our claimed program uses WORD addresses as in the prior sparse-set RAM work.
Memory is infeasible physically and unscored, and no Pareto dominance is claimed.

## 11. Research context and honest status

Official BLAKE3 specifications define the hash and root semantics; old BLAKE
collision, invertibility and near-collision papers do not automatically transfer
to this target. A search of recent dedicated BLAKE3 cryptanalysis did not yield
an applicable full fixed-IV two-round collision construction. In particular,
Aumasson et al., Differential and Invertibility Properties of BLAKE (FSE2010,
eprint 2010/043), analyzes a different primitive; no exponent is imported from
it. Our practical lever is exact RAM amortization of independent evaluations.

The package is ready only after mechanical validation and fresh declared
experiments. Qualification, candidate ranking, human acceptance and promotion
are distinct. The algorithm and counts are analytical; no 2^128-message run,
full-width collision, measured hardware speedup, or prior AI result is asserted
as mathematical proof. Changed package bytes require fresh remote judging.

## 12. Local organizer-executor reproduction

The unmodified organizer run_experiments function was invoked using its pinned
Python3.12.12 Linux amd64 Docker image and default256-trial,20-second budgets,
network none, read-only root, non-root UID65534,128MiB and one CPU. Each source
request was repeated in fresh containers and byte-identical stdout was required.
The organizer independently recomputed every returned message-pair event.
Both guarded-spread and guarded-lowbits completed with107 successes of256
trials. The first seven packed messages of each trial were compared against the
source's independent scalar evaluator: zero reported mismatches, untrusted
observations. Trusted projected-pair checks are stronger than this internal
observation but still cover projections only. Full report hash:
ffdae90fa561dd5123b654fa29254e8872b1feb168d8a694953fff90eac151bf.
This is local execution of the organizer sandbox, not remote AI qualification.

Setup:283 deterministic tests passed,5 skipped. Mechanical candidate check
returned mechanically_valid. No local live AI review or generated score was
used. Remote Yukon submission must run fresh qualification.
