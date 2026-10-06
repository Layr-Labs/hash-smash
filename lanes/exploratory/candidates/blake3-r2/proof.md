# Fixed-a3 BLAKE3-r2 with interleaved extraction and pointer-free lookup

## 1. Target, provenance, and status

The exact target is blake3-r2-prefix-v1: ordinary collisions on distinct complete
64-byte messages, unkeyed BLAKE3 IV, counter zero, block length 64, flags 11,
prefix rounds zero and one, and all 256 digest bits. The classical 256-bit word
RAM uses collision-frontier-v5 with C=430; memory is reported, not scored.
Claimed time is 124.873, success 0.39 conditional on the explicit NEW heuristic
Hfixed, and memory_log2_bytes=262. No concrete full-width collision is supplied.

This derives the grouped partial-evaluation method and sparse-set layout from
jaazinn (0a5b7ae8) and winglock (3022205), and the seven-way guarded evaluator,
key extraction, and experimental scaffolding from tekkac (2bf40fb6, commit
 a4d78416fc5f3cc02e810dd2adf58d812d49e6d2). ercumentyildirim's independent and
grouped SWAR notes (b2508e27 and 2e96a19e) also materially informed the work.
All four are credited as coauthors. Their pending AI-qualified claims are not
human-accepted baselines, and their reported executions are not our evidence.

Our earlier submissions 200fd0ea and 5ebba6b3 use BOTH m14 and m15 to force
final round-zero a3=0. The whole fourth column of round one becomes invariant;
message construction included, the packed body costs 212 rather than 227.
This revision preserves that exact family, all key bits and processing order.
It combines winglock's public afb6e58f (commit
9bfc4542db0c737533b5c751a5f0f1ef11bc9403) interleaved extraction and descending
dense table with our fixed-a3 body. The source's own family is different; its
H1 is NOT substituted for Hfixed. The combination saves actual operations:
212 body +64 extraction +63 table +1 packed advance =340, charged344.
We keep conservative 4096-operation group and MATCH budgets. The four fresh
experiments bind the changed source, including its declined-MATCH path. Prior
AI screening is not mathematical proof, human acceptance, or successful promotion.

## 2. Exact compression and chosen message family

Let B=2^32 and M=B-1. All scalar additions below are modulo B unless stated
otherwise. A G on (a,b,c,d) with message words (x,y) performs

    a=a+b+x; d=ROR32(d XOR a,16); c=c+d; b=ROR32(b XOR c,12);
    a=a+b+y; d=ROR32(d XOR a,8);  c=c+d; b=ROR32(b XOR c,7).

The initial state is (IV[0..7],IV[0..3],0,0,64,11). Each round applies G to
(0,4,8,12),(1,5,9,13),(2,6,10,14),(3,7,11,15), then
(0,5,10,15),(1,6,11,12),(2,7,8,13),(3,4,9,14).
Round zero uses message pairs m0,m1 through m14,m15 in order. Round one uses
P=(2,6,3,10,7,0,4,13,1,11,12,5,9,14,15,8). Output o_i=v_i XOR v_(i+8).

There are G=2^96 groups. For every group independently draw two uniform
256-bit words U0,U1 and mask U1 to 192 bits. These give FOURTEEN independently
uniform words m0..m13 (448 bits). Compute the first seven G calls of round zero.
Call the resulting state v; it is independent of both remaining message words.
Put A=v3+v4, D=v14, C=v9, and E=v4. For each t in 0..B-1, define

    m14 = t-A;
    h   = ROR32(D XOR t,16);
    ch  = C+h;
    bh  = ROR32(E XOR ch,12);
    m15 = -t-bh.

These are the two missing message words. In the last G of round zero the first
a update is A+m14=t, the half-state is (t,bh,ch,h), and the second a update is
 t+bh+m15=0. Its final state is therefore

    a3=0; d14=ROR32(h,8); c9=ch+d14; b4=ROR32(bh XOR c9,7).

The other twelve state words are group constants. Because m14=t-A is a
bijection, the B messages within a group are distinct. Groups with different
448-bit prefixes cannot share any message. This family is a subset of the
ordinary 64-byte message domain; no free IV, modified padding, truncated target,
chosen chaining value, or reduced-round substitute is being claimed.

## 3. Dependency saving and fully specified evaluator

Round one's message pairs are (m2,m6),(m3,m10),(m7,m0),(m4,m13),
(m1,m11),(m12,m5),(m9,m14),(m15,m8).
The fourth column starts with (a3=0,v7,v11,v15), all invariant, and reads
(m4,m13), also invariant. Compute that ENTIRE G once per group. The first
three columns retain the inherited partial evaluation:

- column zero starts its a update from v0+m2;
- column one precomputes a1h=v1+v5+m3, d13h=ROR32(v13 XOR a1h,16),
  and A1y=a1h+m10;
- column two precomputes a2h=v2+v6+m7 and A2y=a2h+m0.

The group constants and the exact straight-line operand schedule are
specified by setup and packed_body in experiments/fixed_a3.py. Their code is
part of this package, with no external dependency. In the counted program all
operands are fixed registers or immediates, and the four diagonal calls follow
the exact schedule above. The last b updates of diagonals one, two and three
are omitted, because only o0,o1,o2,o3,o5 form the 160-bit lookup key. The final
verification recomputes the ENTIRE digest. The experiment's full=True path
also computes the omitted outputs as evidence; it is not part of the hot count.

## 4. Seven independent arithmetic lanes, including subtraction

Pack seven 32-bit payloads at bit positions 36j, j=0..6. Four guard bits follow
each payload. For k in {7,8,12,16,20,24,25}, LOW_k is the union of the low k bits
of every payload. Using seven persistent masks, for each r in {7,8,12,16},

    PROR(z,r)=((z>>r) AND LOW_(32-r)) OR ((z AND LOW_r)<<(32-r))

takes FIVE primitives and returns the exact low32 rotation in every lane.
The masks reject all guard and neighboring-slot bits. The highest payload
ends at bit 247, so 256-bit truncation loses no retained bit.

Additions remain unreduced until rotations or extraction; they have the same
low32 result as modular additions. XOR preserves each slot. Per-slot bounds,
in units of B, prove that no carry crosses a 36-bit slot:

| stage/value | strict upper bound |
| --- | --- |
| t,h,bh,all normalized b/d,group constants | B |
| ch | 2B |
| m14=t+(-A mod B) | 2B |
| m15=2B-t-bh, ordinary nonnegative integer | at most 2B |
| c9 after round zero | 3B |
| a0 / c8 after first column | 4B / 3B |
| a1 / c9 after second column | 2B / 5B |
| a2 / c10 after third column | 2B / 3B |
| fixed fourth-column outputs | B |
| final a0,a1,a2,a3 | 8B,6B,7B,6B respectively |
| final c8,c9,c10,c11 | 5B,7B,5B,3B respectively |

The single non-strict bound m15<=2B still fits well below 16B. In the packed
program subtraction is implemented as TWO_B - T - BH, where TWO_B has value
2B in every slot. Both subtractions have no borrow across a slot: t<B and
bh<B, so every intermediate and final slot is positive. TWO_B's highest set
bit is 249, still inside the RAM word. This proves the packed subtraction
lemma, not just its low-bit congruence. The resulting m15 is congruent to
-t-bh modulo B and is safe as an unreduced addition operand.

Induction over the straight-line body now proves exact agreement of all key
bits with the scalar specified target for every prefix and seven t values.
The body contains 38 additions, 2 subtractions, 27 pre-rotation XORs, 28
five-operation rotations, and 5 output XORs: 38+2+27+140+5=212.
For comparison the inherited body is 227. The difference is the extra first
half/message construction, removal of the fourth column, and one fewer
addition in the last diagonal; it is not a change to primitive prices.

Seven keys use gapped destinations 0,36,72,108,144, an injective encoding
of the same 160 bits o0,o1,o2,o3,o5. It has bits32..35 zero and lies below2^176.
Our previous direct extraction cost97; winglock's interleaving costs64. For
key-slot set S and source-lane group J, choose delta and form

    w = OR over k in S of SHIFT(o[k] AND W_J, 36*(k-delta)).

W_J contains exactly the 32-bit payloads of lanes in J; SHIFT shifts left for
positive displacement, right for negative and is free for zero. Source lane j's
field k now starts at slot j-delta+k. SHIFT(w,36*(delta-j)) moves it to k.
If another lane's field survives, AND with M_S (the payload mask on slots S).
The selected sets have no overlapping field destinations before this cleaning:

| S | (J,delta) |
| --- | --- |
| {0,1,2} | ({0},0), ({1,4},1), ({2,5},2), ({3,6},2) |
| {3,4} | ({1,3},3), ({0,5},3), ({2,4,6},4) |

Every desired field survives 256-bit truncation: for each pair (j,k), its
intermediate slot j-delta+k lies between0 and6. Neighbouring lanes' fields are
disjoint and discarded by the final mask when necessary. The two cleaned
pieces for each lane are ORed. Word construction costs40, per-lane shifts9,
cleaning ANDs8, and final ORs7:64 operations. Nine W/M masks are constants.
This changes no key equality or probability event.

The source embeds RAM_FIXED and RAM_PROGRAM, a fully specified straight-line
schedule obtained by static AST lowering, without executing participant code.
There are276 ALU instructions (212+64), followed by seven TABLE sites. Instruction
operands are explicit register numbers, except shift amounts embedded in the
instruction. Program destinations lie in0..61 of a64-register file. Constants
occupy46 registers: the25 used group constants, seven rotation masks, nine
extraction masks, T,CC,BC7,ONE,TWO_B. A last-use allocation needs at most16
temporaries including two lookup scratch registers. Source ram_keys interprets
that exact allocation and cross-checks it against the readable counted source.
The seven TABLE markers consume keys in lane order; the production expansion is
Section5. No hot-loop memory is used for the evaluator or constant reloading.
Python interpreter dispatch/setup is evidence machinery, not the claimed RAM
implementation. Every executed RAM primitive itself is charged.

## 5. Pointer-free sparse set, loop and memory

This section adopts winglock's afb6e58f layout, with our own message replay.
Let TOP=2^256-1. CC starts at TOP and is the next dense WORD address. Key K
itself is the sparse address. Table step (scratch w,q, a comparison flag):

    w=LOAD(K)                          1
    if CC<w:                           compare+branch 2
        q=LOAD(w)                      1
        if q==K: go to MATCH           compare+branch 2
    STORE(K,CC)                        1
    STORE(CC,K)                        1
    CC=CC-ONE                          1

Worst nonmatch:9 operations; early insertion6; MATCH entry6. On a declined
MATCH, the separately charged handler MUST execute STORE(CC,K); CC=CC-ONE.
This dummy entry is essential: CC counts every message, not just unique keys.
The sparse pointer is unchanged on MATCH, retaining the first representative.

Invariant after j messages: CC=TOP-j, dense[TOP-i]=key_i for every i<j,
and sparse[K]=TOP-i for the FIRST occurrence i of each key. If an unseen key's
garbage pointer w is <=CC it inserts. Otherwise w lies in the contiguous
already-written dense region (CC,TOP]. That dense word cannot equal an unseen
key, so it also inserts. No initialization, false MATCH or unwritten dense
read is assumed. A seen key always MATCHes its first dense entry. Dummy entries
repeat keys previously inserted and preserve this argument.

Messages are processed by group g, then t=0..2^32-1. Thus i=g*2^32+t;
NOT w recovers the prior i and NOT CC the current i. A shift32 and AND with
M decode g,t. Each group retains the original two prefix words U0,U1.

Disjoint memory regions, all word addressed:

| region | address |
| --- | --- |
| dense | TOP-i, 0<=i<2^128 |
| sparse | K<2^176, with bits32..35 zero |
| prefix records | (g<<36) OR 2^32 OR k, k=1,2 |
| scalars, spills, outputs | 2^32+[16,2^14) |
| code and constants | 2^33+[0,2^22) |

Every non-dense address is below2^177. Record/scalar/code addresses have bit32
or33 set, unlike keys; the two record offsets are disjoint from scalars and
from each other. Code has bit32 clear; records and scalars have bit32 set.
Dense addresses exceed2^255. Full address-space span is2^256 words, or2^261
bytes. Report memory_log2_bytes=262 to include registers beyond that complete
span and conservative bookkeeping. At most2^128 dense and
2^128 sparse entries are written, but the smaller populated size is NOT our
reported span. There is no unbounded or larger-than256-bit production address.

Pack t..t+6 in T and advance by BC7=broadcast(7), one operation each batch.
There are q=floor(2^32/7)=613566756 full batches and a final four-message batch.
Before that tail, mask T with the payload mask to normalize inactive overflow
lanes; pay a complete344-operation batch though only lanes0..3 are tabled.
Unroll eight full batches; loop control costs at most4 primitives per block
(load group end, compare, branch, plus explicit constant/address allowance).
The spare four per batch more than covers this. Remaining full batches at group
end use straight-line copies. Tail, dispatch, group-loop work and loading end
addresses lie in the4096 group budget. Each TABLE site has a fixed MATCH
continuation; no indirect dispatch is free. Code and masks fit below2^20 words
and their initialization is charged2^20 operations.

## 6. Bounded collision confirmation and total work

Stop with failure when the (2^110+1)-th MATCH would be entered. Incrementing,
loading, storing and testing its cap counter costs at most 10 primitives for
the final aborted entry. At each allowed MATCH:

- decode earlier i=NOT w and current i=NOT CC; recover t,g by AND/shift;
  load the two retained prefix words for each message;
- unpack fourteen words and recompute the first seven G calls and A,D,C,E;
  reconstruct both m14,m15 by Section 2; do this for both messages;
- reject identical messages; hash each with a COMPLETE selected two-round root
  compression; test all 256 bits; return the distinct pair only on equality;
- on a failed full comparison, write the dummy dense entry and decrement CC;
  restore spilled live registers and resume, keeping the first representative.

For each message reconstruction, seven scalar G cost at most 7*30=210 primitive
operations (two ternary adds, two binary adds, four XORs and four four-operation
scalar rotations per G), plus <100 unpack/construction/address operations.
Even a more literal masked implementation with seven G at 36 each is below
400 per reconstruction. Two reconstructions, comparisons, output, bookkeeping,
and at most 64 spills/restores with explicit address updates are below 2048;
we charge 4096 ordinary operations PLUS two whole selected compressions per
allowed MATCH. All failed comparisons and cap failure are included.

Per group, at most 4096 ordinary operations cover two random words, masking,
storage/address arithmetic, fourteen-word unpacking, the seven prefix G, the
fixed fourth column, other constants, 26 broadcasts (<8 operations each),
constant-register initialization, group/loop setup and the final tail. Group
setup is performed online, but included in preprocessing_log2=100 if all group
preparation is classified as preprocessing. Fixed code/mask initialization is
charged 2^20 ordinary operations. No target-dependent advice is supplied.

Per seven-message batch,212 body +64 extraction +7*9 table +1 T advance=340.
Charge344, leaving four primitives per batch for loop control and spare margin. This spare is not needed for the separately charged
MATCH handler. The final four-message batch is charged a full344.
Therefore, for EVERY run, success or failure,

    T <= [2^96*(q+1)*344 + 2^96*4096 + 2^20 + 10]/430
         + 2^110*(2+4096/430)
      < 0.115 * 2^128
      < 2^124.871272
      < 2^124.873.

The submitted bound is rounded UP. Preprocessing is below 2^100 target units
including all group preparations and fixed setup; it is already in T, not an
extra uncharged phase. memory_log2_bytes=262; nonuniform_advice_log2_bytes=0
means no supplied advice (zero cap convention), not a stored collision.

## 7. Success analysis and the new heuristic Hfixed

Failure events are Fprefix (duplicate 448-bit prefixes), Fnone (no complete
collision among the N=2^128 generated messages), Fhide (a full-colliding pair
is hidden by an earlier different-digest message with the same 160-bit key),
and Fcap (more than 2^110 confirmations). Except Fprefix, their bounds below
are HEURISTIC about this newly constrained family, not theorems about BLAKE3.
Every RETURNED pair is valid independently of any heuristic.

Fprefix is bounded unconditionally by choose(2^96,2)/2^448 <2^-257.
In a comparison model of independent uniform 256-bit digests:

    Pr[Fnone] <= exp(-N(N-1)/2^257) <0.6065307;
    Pr[Fhide] <N^3 *2^-256 *2^-160 =2^-32;
    E[equal-key pairs] <N^2/2^161=2^95;
    Pr[Fcap] <=2^95/2^110=2^-15.

The loose ORDERED-triple bound avoids any convention about a factor of two.
Each actual confirmation corresponds to an equal-key pair, so Markov applies.
If no failure event occurs, the sparse-set invariant and final check recover
a full collision. The model success is therefore >0.3934387.

Hfixed asserts that for the fixed selected hash and the exact fresh-random
prefix construction in Section 2, the SUM of the probabilities of Fnone,Fhide,
and Fcap exceeds the model upper bounds by at most 0.003. Then success is
>0.3934387-0.003-2^-257 >0.3904387 >0.39. This is an explicitly quantified
heuristic allowance, NOT a confidence interval and NOT measured at full scale.

The forced intermediate zero is a real restriction; it could introduce digest
correlations absent from ordinary grouped searches. Cross-group inputs retain
448 random bits, but entropy alone does not prove the output premise. Within
group behavior is especially structured. We therefore declare fresh tests for
both many-group and single-group layouts, including all output words. Prior AI
screening of another message family does not establish Hfixed. If Hfixed is
refuted or judged unsupported, this candidate has no justified 0.39 claim and
must not receive an exploratory score merely because its time count is sound.

## 8. Declared experiments, checks, and limitations

Four experiments use 1024 messages from the NEW family, in seven-way batches,
under organizer-provided seeds. The fixed source expands each group's fourteen
prefix words with SHAKE256, for reproducibility ONLY. The production algorithm
uses independent uniform RAM random words; deterministic seed expansion is not
proof that those random coins have been implemented in an astronomical search.

- fixed-a3-pf-spread: 32 prefixes, 32 consecutive t each, twenty output bits spread
  across the five key words.
- fixed-a3-pf-single: one prefix, 1024 t, a different twenty-bit key projection.
- fixed-a3-pf-fullword: 32 prefixes, 32 t, twenty bits spanning all eight digest
  words; the evidence-only full packed evaluator computes omitted outputs too.

- fixed-a3-pf-keysub:32 prefixes,32 t, a16-bit lookup key projected from a20-bit
  event. Four extra event bits are in omitted words o4,o6,o7, so declined MATCHes
  and their dummy dense entries are exercised. This is a scaled hiding test.

All use the actual pointer-free sparse-set lookup under seeded stale-pointer garbage. The first three
scaled tests use the event mask itself as the key, so they test projected
birthday behavior and sparse-set semantics; they DO NOT measure the full-width
key-hiding or verification-cap probabilities. The fullword experiment uses a
Python namespace above2^257 to separate its evidence-only full key; that is
not an instruction or memory requirement of the claimed production RAM program.

Before searching each trial, source code compares fourteen lane instances
(including zero, maximum32, near-maximum32 and high-bit boundary t values) with
an independently structured scalar compression and checks all eight output
words. It raises on a discrepancy. A counting wrapper checks (212,64) for body
and extraction. The lowered64-register path must return the same seven keys, and dense-address
decoding is checked after every processed message. Those observations/counts are participant-controlled and are
not a trusted certification; the arithmetic proof and full source support the
claim. Organizer hashing independently validates every returned projected pair.
Trials with no match return two nulls. For the first three experiments, the predicted independent model frequency
is 1-product(i=0..1023)(1-i/2^20), approximately 0.39327.

The organizer must execute and bind these experiments before review. No local
participant code was executed, because the required organizer Docker executor
was unavailable. Local work was static source inspection, AST syntax/counting,
Decimal arithmetic of the closed-form cost, and organizer mechanical intake.
No fabricated local frequency, source author's run, full-scale collision,
mathematical proof of Hfixed, or statistically certified 0.003 margin is claimed.
The 20-bit experiments cannot resolve arbitrary full256 structure or extrapolate
rare triple events at N=2^128. They supply relevant finite evidence for reviewers
to assess, including the risk caused by fixing a3. AI qualification, manual
acceptance and successful promotion remain separate stages.

## 9. Revision audit and qualifications

This revision combines our5ebba6b3 fixed-a3 family/body with winglock's afb6e58f
interleaving and pointer-free lookup, retaining jaazinn, winglock, tekkac and
ercumentyildirim as coauthors. No public author's reported execution is passed
as our evidence. Hfixed's full-scale extrapolation remains unresolved. The
new table is provably the same first-representative algorithm for the same key
and message order, so no new success premise is introduced by this optimization.
The additional224-bit-prefix family considered in research is NOT used here.

Static lowering/counting finds212 body+64 extraction primitives and at most62
live/fixed registers including lookup scratch; shift immediates cost no extra
operation, consistent with the reference operation model. All loads, stores,
comparisons and branches are charged. The production64-register machine and
fixed program contain no Python lists/dictionaries or arbitrary-index operations.
The source interpreter and counting wrapper are untrusted independent evidence
checks; actual returned message pairs are checked by organizer hashing.

Exact arithmetic of the full bound gives log2(T)=
124.87127192132815880788783692072667795267607086821121935024545302.
The claim124.873 rounds upward, and the full address span261 plus register overhead is reported conservatively as262.
Our125.097 and winglock124.937 are pending AI-qualified claims, not accepted
baselines. Neither comparison establishes mathematical truth or publication.
No local participant program was executed. Fresh organizer isolated experiments
must run on this exact source before its empirical support can be assessed.
