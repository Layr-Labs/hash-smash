# Fixed intermediate word in a seven-way BLAKE3-r2 birthday search

## 1. Target, provenance, and status

The exact target is blake3-r2-prefix-v1: ordinary collisions on distinct complete
64-byte messages, unkeyed BLAKE3 IV, counter zero, block length 64, flags 11,
prefix rounds zero and one, and all 256 digest bits. The classical 256-bit word
RAM uses collision-frontier-v5 with C=430; memory is reported, not scored.
Claimed time is 125.160, success 0.39 conditional on the explicit NEW heuristic
Hfixed, and memory_log2_bytes=167. No concrete full-width collision is supplied.

This derives the grouped partial-evaluation method and sparse-set layout from
jaazinn (0a5b7ae8) and winglock (3022205), and the seven-way guarded evaluator,
key extraction, and experimental scaffolding from tekkac (2bf40fb6, commit
 a4d78416fc5f3cc02e810dd2adf58d812d49e6d2). ercumentyildirim's independent and
grouped SWAR notes (b2508e27 and 2e96a19e) also materially informed the work.
All four are credited as coauthors. Their pending AI-qualified claims are not
human-accepted baselines, and their reported executions are not our evidence.

Our change uses BOTH m14 and m15 to force the final a3 word of the last G in
round zero to ZERO. The whole fourth column of round one is then invariant
within a group. Extra message-construction work is included: the seven-message
body falls from the source's 227 to 212 word operations. Total counted batch
work falls from 420 to 405; we charge 420, with explicit loop and tail budgets.
This changes the message family, so the source's heuristic is not inherited as
established evidence. The three declared experiments use the new family.

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

The 26 group constants and the exact straight-line operand schedule are
specified by setup and packed_body in experiments/fixed_a3.py. Their code is
part of this package, with no external dependency. In the counted program all
operands are fixed registers or immediates, and the four diagonal calls follow
the exact schedule above. The last b updates of diagonals one, two and three
are omitted, because only o0,o1,o2,o3,o5 form the 160-bit lookup key. The final
verification recomputes the ENTIRE digest. The experiment's full=True path
also computes the omitted outputs as evidence; it is not part of the hot count.

## 4. Seven independent arithmetic lanes, including subtraction

Pack seven 32-bit payloads at bit positions 36j, j=0..6. Four guard bits follow
each payload. For each r in {7,8,12,16}, define A_r as the union of low 32-r
bits of each payload and B_r as the union of high r payload positions. Then

    PROR(z,r)=((z>>r) AND A_r) OR ((z<<(32-r)) AND B_r)

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

Seven keys are extracted directly at destinations 0,32,64,96,128. Lane zero
requires 13 operations; each of lanes one through six requires 14. Four shifts
derive key masks, giving 13+6*14+4=101. The source's extract_keys is the exact
transcript. Registers containing state values that are no longer used can be
reused for masks and table work after all output words have been formed.

Register budget: 26 group constants, at most 16 variable state/intermediate
values, 2 temporaries, 8 rotation masks, T,R,CC,M,MC,SB,INC,loop, and TWO_B:
61 registers. The initial h,bh,m14,m15 reuse slots before the column/diagonal
variables become live. Shift amounts are immediates. There is no register
array load or uncharged arbitrary indexing in the counted straight-line RAM.
MATCH spills and restores live registers within its separate conservative cap.

## 5. Loop, sparse set, and memory

Use the inherited table layout. Define MC=(2^128-1)<<32, SB=2^160 and INC=2^32.
CC starts at zero and is the next dense WORD address. The record descriptor
is R=t+(g<<160). Its low32 t and high96 group fields leave bits32..159 free
for the dense pointer. The packed T starts with t values 0..6 and is advanced
by broadcast(7) in one add per batch. Scalar R advances once per active lane.
There are q=floor(B/7)=613566756 full batches and a last four-message batch per
group. Mask T with the payload mask before that last batch to normalize the
three ignored overflow lanes; charge the full batch even though only four keys
are used. Partial group tails and loop setup are expressly charged below.

At key K=o0|(o1<<32)|(o2<<64)|(o3<<96)|(o5<<128), perform:

    sa=K OR SB                          1
    w=LOAD(sa)                         1
    p=w AND MC                         1
    if p<CC:                           compare+branch 2
        x=LOAD(p)                      1
        if x==K: go to MATCH           compare+branch 2
    STORE(sa,R OR CC)                  OR+store 2
    STORE(CC,K)                        1
    CC=CC+INC                          1

Worst nonmatch path: 12 primitives, early insertion 9, match entry 8. No
initialization of the sparse region is assumed. After j insertions,
dense[i*2^32]=key_i for i<j, and sparse[SB+key_i]=R_i|(i<<32).
An arbitrary sparse word either fails p<CC or points to a previously WRITTEN
dense cell. Equality of that cell to K then means an actual earlier insertion
of K. A nonexistent key cannot create a false MATCH through garbage. Once
inserted, a key and its first descriptor never move or change. Every full
collision has the same K, although an earlier different digest with that K
can hide it; that probability is explicitly covered by Hfixed, not ignored.

Memory regions (word addresses): dense i<<32, i<2^128; group records U0,U1
at 4g+1,4g+2; scalars/output at odd addresses between 2^99 and 2^100; code,
constants and spill region at odd addresses starting 2^100 with fewer than
2^22 reserved words; sparse at [2^160,2^161). Dense multiples of 2^32 are
excluded from the other regions, which use odd or 2 mod4 addresses. These
regions are disjoint, every address is below 2^161, and the whole span is below
2^166 bytes. Report 167 to include all code, tables, registers and outputs.
The machine is word addressed; no unit-cost arbitrary precision address is used.

The eight-batch unroll uses at most 3 operations for loop control per 8 batches.
Group-end remainder/control, packed initialization, register loads and broadcasts
fit inside the separately charged group setup. MATCH has one copy per table
site and returns to its own R increment; no indirect branch is assumed. Fewer
than 2^20 instruction/constant words suffice even with conservative duplication.

## 6. Bounded collision confirmation and total work

Stop with failure when the (2^110+1)-th MATCH would be entered. Incrementing,
loading, storing and testing its cap counter costs at most 10 primitives for
the final aborted entry. At each allowed MATCH:

- recover earlier t and g by AND/shift; load two retained prefix words;
- unpack fourteen words and recompute the first seven G calls and A,D,C,E;
  reconstruct both m14,m15 by Section 2; do this for both messages;
- reject identical messages; hash each with a COMPLETE selected two-round root
  compression; test all 256 bits; return the distinct pair only on equality;
- restore spilled live registers and resume, keeping the first representative.

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

Per seven-message batch, 212 body +101 extraction +7*12 table +7 R increments
+1 T advance =405. Charge 420, leaving 15 primitives to cover 3/8 amortized loop
control and unused margin. This spare is not needed for the separately charged
MATCH handler. The final four-message batch is charged a full 420.
Therefore, for EVERY run, success or failure,

    T <= [2^96*(q+1)*420 + 2^96*4096 + 2^20 + 10]/430
         + 2^110*(2+4096/430)
      < 0.139578853 * 2^128
      < 2^125.159153
      < 2^125.160.

The submitted bound is rounded UP. Preprocessing is below 2^100 target units
including all group preparations and fixed setup; it is already in T, not an
extra uncharged phase. memory_log2_bytes=167; nonuniform_advice_log2_bytes=0
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

Three experiments use 1024 messages from the NEW family, in seven-way batches,
under organizer-provided seeds. The fixed source expands each group's fourteen
prefix words with SHAKE256, for reproducibility ONLY. The production algorithm
uses independent uniform RAM random words; deterministic seed expansion is not
proof that those random coins have been implemented in an astronomical search.

- fixed-a3-spread: 32 prefixes, 32 consecutive t each, twenty output bits spread
  across the five key words.
- fixed-a3-single: one prefix, 1024 t, a different twenty-bit key projection.
- fixed-a3-fullword: 32 prefixes, 32 t, twenty bits spanning all eight digest
  words; the evidence-only full packed evaluator computes omitted outputs too.

All use the actual sparse-set lookup under seeded stale-pointer garbage. These
scaled tests use the event mask itself as the key, so they test projected
birthday behavior and sparse-set semantics; they DO NOT measure the full-width
key-hiding or verification-cap probabilities. The fullword experiment uses a
Python namespace above 2^256 to separate its evidence-only full key; that is
not an instruction or memory requirement of the claimed production RAM program.

Before searching each trial, source code compares fourteen lane instances
(including zero, maximum32, near-maximum32 and high-bit boundary t values) with
an independently structured scalar compression and checks all eight output
words. It raises on a discrepancy. A counting wrapper checks (212,101) for body
and extraction. Those observations/counts are participant-controlled and are
not a trusted certification; the arithmetic proof and full source support the
claim. Organizer hashing independently validates every returned projected pair.
Trials with no match return two nulls. The predicted independent model frequency
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
