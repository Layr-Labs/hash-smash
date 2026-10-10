# A last-chunk half-collision and a chunk-counter search for 2-round BLAKE3

The scalar below is `time_log2` under `collision-frontier-v5`. Memory is a
separately reported resource bound.

**This package against entry a402a477 (Jbenisek, 63.9522).** This package is
entry a402a477, awaiting review when this package was written, with one change
to the machine layout of an opened cluster and nothing else. In entry a402a477
an opened cluster stores seven words of its representative batch in a fixed
frame of memory before its five partner batches and reloads them after (28
units), and it keeps the opened count in a memory word (6 units for its address,
load, increment, store, comparison and branch). The partner batches use at most
31 registers and their Q paths at most 39 of the 64 (9.8), so here those seven
words and the opened count stay in eight reserved registers that no partner
batch, Q path or lane test names: an opened cluster costs 333 machine units in
place of 364. A passing lane, which may use all 64 registers in steps 2 and 3,
now stores and reloads these eight registers with its 29 words, 32 units more:
494 in place of 462 (9.8, 9.9, Section 11). The construction, the walk, every
trial and every count, the budgets, the credit, the run length, the success
argument and the three heuristics are those of entry a402a477, unchanged; the
change is in the time bound only, which charges every row at its budget as
before. The claimed bound falls from 63.9522 to **63.9016**. The program of the
declared experiment adds the new charges per event (6.4) and is otherwise
unchanged. Passages changed by this package say so ("this package"); everywhere
else "we", "our entry" and "the participant" refer to Jbenisek, the author of
entry a402a477, and to that participant's helpers.

This exploratory package targets blake3-r2-prefix-v1. It has an exact part and a
heuristic part, and it keeps them apart. It is the counter search of our entry
415e792c on the whole class of eta with the outcome set S of six outcomes of
beta*, 175020a0, 185020a0, 275020a0, 285020a0, 385020a0 and 685020a0, with the
exact filter, the s-pattern pre-check and the credit of that entry, and with
four changes. (1) *The member loop and the direct tables*, after entry e9b6649e
of the participant hecmas: the run draws one fresh word per *context*, the seven
outer words, runs the 39 lines of the outer step that do not read the member
once for that context, and walks all 2^19 members of the class in it; the two
masks of the filter are read from two tables over all 2^32 words with one load
each (9.8). (2) *The guards (G7) and (G15) and a root certificate of four
one-word tests*: (G7), of our entry 0bc5f130 (GPT Sol, answer AX 1), and (G15)
(GPT Sol, answers CF 7 and CD 10) each prescribe one more bit of the solver's
word, and the certificate (GPT Sol, answer CF 6) replaces the full test of E1 on
a root, and with the global ledger of 1,024 machine units of an outer step that
reaches the solver (GPT Sol, answer CD 11) the proved cap of the solver's work
is 17,504 machine units, at most 16/27 of the cap with (G7) alone in every outer
step; the credit of the solver is set by 16/27 times the exact model mean of the
capped work with (G7) alone, 582,173,006,981,436 / 2^47 (9.7, 10.3, Section 11).
(3) *The omega-first batch* (GPT Sol, answer CA, derived and checked by the
participant, with its charges audited in GPT Sol's answer CD): a batch of seven
members computes only the 8 member lines that lead to omega = Y3 + y + w8, and
the 17 member lines that lead only to Y9 run inside the Q path of a lane whose
test on omega passes: 66 machine units per batch on a pair of list words, 64 per
Q path, whose E count a register holds (GPT Sol, answer CD 8), 600 per context
and 462 per passing lane (494 in this package; 9.8, Section 11). (4) *The cluster gate* (GPT Sol,
answers CI 1, CJ and CK 5): the 32 members that differ only in bits 10 to 14 of
e1 form a cluster, and all of them have omega modulo 2^9 in one of two values
computed from one representative (Lemma KP); a fixed table of 2^21 words, read
once per representative, skips the cluster when neither value can pass test (2),
which loses nothing (Lemmas A9 and CL). A representative batch of seven costs 74
machine units, with no table read but the gate, and an opened cluster 364 (333
in this package), with
a budget on the opened clusters; Lemma OR proves that on average the gate opens
on at most 246,621,675 / 2^29 < 0.4593686667 of the clusters of a context, so
the budget needs no premise (9.9, Section 11). The exact filter (Section 8)
skips every outer step that cannot hold a success with an outcome of S, and the
joint solver (9.4) finds the successes of a passing outer step without
enumerating its trials. The heuristics are H1', H4' and H5', stated for the walk
by contexts, with the rate margin 11/10, the factors 1.000026 and 1.000176 on
the two count shares and 1.01 on the mean of the solver's cap (GPT Sol, answer
CK); part (ii) of H1' takes the context as the unit, a stronger clause than one
stated per outer step (10.3). Every budget and the credit carry a reserve that
bounds their overflow by exp(-20) over the independent contexts, with no further
premise (9.1, 10.3). The values that the search reads are a fixed record of
nonuniform advice, stated in full (Section 12): the success analysis uses only
properties of this record that this text verifies exactly, and the selection
procedure SEL that found it is charged in full in the time, at a cap of
8,882,224,365,081,579,520 operations that holds by construction (Section 12); no
premise is declared for it. The charges of the layout, of the solver with its
cap, the guards (G7) and (G15), the root certificate, the pre-check, the cluster
gate and the credit are proved allowances of a specified machine layout (Section
11). The search itself is the program of the declared experiment, which the
organizer runs: each organizer trial walks 32 clusters of one fresh context of
the counter instance through every step of 9.1, checks every walked member
against the full outer step, adds the charges of Section 11 per event, and
returns a pair of the root instance whose half-collision the organizer checks on
the digests (6.4, Section 13). Section 15 lists the earlier entries in one line
each, and Section 16 credits the people and models whose work is used.

**Exact part.** An explicit construction maps seven 32-bit words, a member y of
the class of eta, a set of 524,288 values, and one more word c1 to a number t
and to a 55-byte string A and a 63-byte string B. When t is not zero, F || A
and F || B, with F a string of t full chunks of 1,024 bytes, are messages of
1024 t + 55 and 1024 t + 63 bytes whose last chunks are A and B, and the
2-round compressions of these last chunks, with chunk counter t and flags 3,
give chaining values that agree on their words 0, 2, 5 and 7, that is on 128 of
their 256 bits. There is no search in this and no probability: it holds for
every choice (Sections 7 and 8). In the organizer's tree mode the digest of
such a message depends on F and on the chaining value of its last chunk alone
(Lemma TR), so a pair whose last-chunk chaining values agree in all eight words
is a collision of two complete messages. The number t is not chosen: it is the
chunk counter that the round-0 call K0 reads, solved per trial as t =
ROL(K0.d1,16) XOR K0.a1. It takes up the freedom of the message word w0, and
that is what lets the construction prescribe c1, the third value of the round-1
call E1, next to y. The search holds c1 inside the set Q* of the 2^21 words for
which the first-half b difference of E1 is beta* = 18b0e098, the difference of
the solution with which the constants were found (Section 12).

**Heuristic part.** A collision needs the other four words of the chaining value
to agree as well. The algorithm walks 640,117,155,200,996,737,024 = 2^69.117
outer steps of 2^21 trials each: 1,220,926,580,812,448 = 2^50.117 contexts drawn
at random, each with all 2^19 members of the class in 16,384 clusters of 32,
seven members to a batch. An exact filter, two carry automata on two words of
the outer step, skips every outer step that cannot hold a collision with an
outcome of S (Lemma F); it passes 2^-9.9782 of uniform pairs of words. A table
read once per cluster skips the clusters in which no member can pass the second
automaton, exactly and without loss (Lemma CL); in the other clusters the second
automaton, read from a table at omega, is tested in every lane; the member lines
that lead only to Y9, and the first automaton, run only in a lane whose omega
passes the second, 2^-4.1998 of uniform words. In a passing outer step three
bits of E1.b1 that every success shares are a function of the words of the outer
step, and they allow an outcome of S for only two of their eight values: the
pre-check skips the joint solver in the other passing outer steps, exactly and
without loss (Lemma VP). The joint solver, one depth-first traversal over the
bits of one internal word with guards that exact counts of the class prove
lossless and with the guards (G7) and (G15) (Lemmas G7 and G15), returns every
value of that word that meets the conditions of an outcome of S, and a
certificate of four one-word tests decides for each whether its trial completes
the collision (Lemma RC). Together they find exactly the trials of the outer
step that complete the collision with an outcome of S, at a cost of at most
18,062 machine units for a passing outer step whatever its words: 64 for its Q
path, 494 for its lane and 17,504 for steps 2 and 3 (Sections 9 and 11; Lemmas
V, RC, VP, G7, G15, CV). The three budgets and the credit of the solver are
halts, each charged at its bound, so the time bound contains no mean of a count;
each is a mean bound plus a reserve whose overflow probability is at most
exp(-20) over the independent contexts. Three heuristics are declared for the
success, each for the instance that the stated advice record of Section 12
fixes. H1': the valid trials (t not zero) complete the collision with an outcome
of S at a rate no lower than 125,920,632,087 * 2^-128 = 2^-91.126, ten
elevenths, rounded down, of the model's rate for this prescription and these
outcomes, and the listed good trials of one context, within one outer step and
across its members, are not clustered beyond a stated bound. H4': for uniform
words, a lane's omega passes the second automaton with probability at most
1.000026 times its exact share, and an outer step passes the filter with
probability at most 1.000176 times its exact share; then the two budgets of a
run suffice except with probability exp(-20) each. H5': averaged over the outer
steps, C(T), the proved cap with (G7) on the solver's work for the outcomes kept
by the pre-check (zero if it keeps none), is at most 1.01 times
582,173,006,981,436 / 2^47 = 4.1366, its exact mean in the counting model, which
makes the credit of the run sufficient: the run debits the cap with (G15), at
most 16/27 of C(T) in every outer step, from a credit scaled by the same 16/27.
The budget of opened clusters needs no premise: Lemma OR proves that on average
the gate opens on at most 0.4593686667 of the clusters of a context (9.9). Under
these three the search succeeds with probability at least 0.39. The search is
charged below 2^63.8999 target-compression units. The selection procedure SEL
that found the advice record is charged in full, below 2^54.198 units, at a cap
that holds by construction (Section 12). The total, 2^63.90154718..., is below
2^63.9016: the claimed scalar is 63.9016. The search needs less than 2^39 bytes
of memory, the two direct tables of the filter included; its two messages are
shorter than 2^42 bytes each, and the declared 2^44 bytes cover them, the code,
the search and every run of SEL, even all held at once (Section 12).

The rate in H1' is an assumption. Under the seven-word model of Section 13,
with Y4 uniform in the class, prescribing c1 in Q* multiplies by 2^11 the part
of beta* in the rate of the class: counting the six outcomes of S, the rate is
2^11 * 67,633,152 = 138,512,695,296 times 2^-128, which is 853.61 times the
model rate of a trial of the class (Lemma S1, proved by another AI model, GPT
Sol 6.1). The figure 67,633,152 is the sum of six exact outcome counts of the
participant's counting program, printed with its output in Section 17. Whether
the trials of the construction realise that conditional law, to at least 10/11
of its rate, is not proved, and it is declared as H1'; Lemmas S2 to S4 prove
parts of it, and Lemma S8 states how weak the dependence has to be. On real
counter trials the participant's measurements agree with the model for events
down to about 2^-31.7 per trial, and in a scaled-down end-to-end run with real
collisions of complete messages the prescription realises 0.94 +- 0.13 of its
predicted gain; a preregistered run of the same toy found 40,882 collisions
against 40,800.63 predicted, a one-sided lower bound of 0.99213 on the ratio
(Section 13). No run reaches a collision at 32 bits.

Part (ii) of H1', the dependence, is stated with the context as the unit, as
entry e9b6649e states it: the 2^19 outer steps of a context share their seven
outer words, and only the contexts are independent. This contains the per-step
clause of entry 415e792c and adds the dependence across the members of a
context. It is an assumption, which cannot be measured at full size; it fails
only if listed good trials cluster by context about 2^43.9 times more than
independent members would, while the events that every listed good trial meets
cluster by a factor between 1.14 and 1.25 at every depth measured, from the
filter to the roots of the solver; in a preregistered run of 262,144 contexts
the two halves of a listed good trial, the listed E1 outcome at 2^-32.29 per
trial and (J1) and (J2) of the E3 half at 2^-34.58, show no clustering across
members (factors 0.999 +- 0.054 and 0.90 +- 0.24), while the joint event itself
is out of reach (10.3, Section 13).

No full 2-round collision is exhibited, and the search is far beyond feasible
computation. The declared experiment runs the search itself at the scale of one
context per organizer trial: its program walks 32 clusters of a fresh context of
the counter instance through every step of 9.1, checks every walked member
against the full outer step, and returns the pair of the root instance for the
same context, single chunks of 55 and 63 bytes compressed with counter 0 and
flags 11, whose half-collision the organizer checks on the digests (6.4). It
cannot show the half-collision of the counter instance: that chunk is not the
root, and the organizer can hash only the root instance. Its halt constants are
those of the search at the rate factor 5/7, larger than those of 9.1, and no
trial reaches them; the run length, the budgets and the credit of the claim are
those of 9.1, each charged in full (Section 11).

## 1. Exact complete hash on the messages used

H is unkeyed BLAKE3-256 with only rounds 0 and 1 kept in every compression.
Every message of the root instance (Sections 4 to 6) has n = 55 or n = 63
bytes. A message of n <= 64 bytes is one chunk consisting of one block, with no
parent node, so H evaluates exactly one compression. The block is the message
followed by 64 - n zero bytes, used only for loading words. The compression has
flags CHUNK_START | CHUNK_END | ROOT = 11, true block length n, and chunk
counter and root-output counter both zero. There is no key and no derivation
flag.

Decode the zero-filled block into sixteen little-endian 32-bit words w[0..15].
The IV is

    6a09e667 bb67ae85 3c6ef372 a54ff53a
    510e527f 9b05688c 1f83d9ab 5be0cd19.

Initialize v[0..7] = IV, v[8..11] = IV[0..3] and v[12..15] = (0, 0, n, 11).
The block length n is the initial value of v[14] and enters nowhere else. All
additions and subtractions on state and message words are modulo 2^32. ROR and
ROL rotate a 32-bit word. G(a,b,c,d,x,y) is

    v[a] = v[a]+v[b]+x;  v[d] = ROR(v[d] XOR v[a],16)
    v[c] = v[c]+v[d];    v[b] = ROR(v[b] XOR v[c],12)
    v[a] = v[a]+v[b]+y;  v[d] = ROR(v[d] XOR v[a],8)
    v[c] = v[c]+v[d];    v[b] = ROR(v[b] XOR v[c],7).

A round is four column calls followed by four diagonal calls on the current
schedule s, and between rounds s is replaced by s[P[i]] with
P = (2,6,3,10,7,0,4,13,1,11,12,5,9,14,15,8). Written out for the two retained
rounds, with names used throughout:

    round 0   K0 = G(0,4,8,12, w0, w1)     K1 = G(1,5,9,13, w2, w3)
              K2 = G(2,6,10,14, w4, w5)    K3 = G(3,7,11,15, w6, w7)
              D0 = G(0,5,10,15, w8, w9)    D1 = G(1,6,11,12, w10, w11)
              D2 = G(2,7,8,13, w12, w13)   D3 = G(3,4,9,14, w14, w15)
    round 1   C0 = G(0,4,8,12, w2, w6)     C1 = G(1,5,9,13, w3, w10)
              C2 = G(2,6,10,14, w7, w0)    C3 = G(3,7,11,15, w4, w13)
              E0 = G(0,5,10,15, w1, w11)   E1 = G(1,6,11,12, w12, w5)
              E2 = G(2,7,8,13, w9, w14)    E3 = G(3,4,9,14, w15, w8)

S denotes the state after K0..K3, X the state after round 0, Y the state after
C0..C3 and Z the final state. The compression output is
o[i] = Z[i] XOR Z[i+8] and o[i+8] = Z[i+8] XOR IV[i] for i = 0..7. The digest
H(m) is the first 32 output bytes, LE4(o[0]) || ... || LE4(o[7]).

This is the complete hash of the target profile restricted to inputs of 55
and 63 bytes: standard IV, standard flags, true block length, both retained
rounds with the standard permutation, standard feed-forward and the full
256-bit digest. It is not a free-start, chosen-IV, compression-only or
truncated-output setting.

*The same compression in a last chunk.* Sections 7 to 9 use the same
compression, with the same names, as the compression of the last chunk of a
longer message: there v[12..15] = (t mod 2^32, t >> 32, n, 3), with the chunk
counter t and the flags CHUNK_START | CHUNK_END = 3, and the output words o[0],
.., o[7] are the chaining value of the chunk (Lemma TR). Nothing else changes:
the IV, the block, the two rounds and the output.

## 2. Inverting one G call

Consider one call G(a,b,c,d,x,y) with input values A, B, C, D and name its
eight assignments

    a1 = A + B + x           d1 = ROR(D XOR a1, 16)
    c1 = C + d1              b1 = ROR(B XOR c1, 12)
    a2 = a1 + b1 + y         d2 = ROR(d1 XOR a2, 8)
    c2 = c1 + d2             b2 = ROR(b1 XOR c2, 7).

Its outputs are (a2, b2, c2, d2). The values a1, d1, c1, b1 are called the
first, second, third and fourth value of the call, a2 the fifth, and so on.

**Fact 1.** Reading the assignments backwards,

    b1 = ROL(b2, 7) XOR c2       c1 = c2 - d2       d1 = ROL(d2, 8) XOR a2
    B  = ROL(b1, 12) XOR c1      C  = c1 - d1
    a1 = ROL(d1, 16) XOR D       y  = a2 - a1 - b1      x = a1 - A - B.

Each line is one assignment solved for another of its terms. A set of words
A, B, C, D, x, y, a1, d1, c1, b1, a2, d2, c2, b2 is the execution of one
call exactly when the eight assignments hold, in whatever order and for
whichever of their terms they were solved. The constructions below use
nothing else: every line of theirs is one assignment of one call, solved
for the name on its left.

## 3. Three ingredients

**3.1 The length is cancelled inside K2.** K2 is the only call of round 0 that
reads the block length n, the initial value of v[14], and it overwrites that
word; it is also the only call of round 0 that reads w4 and w5. Its inputs are
(IV[2], IV[6], IV[2], n). Put K = IV[2] + IV[6] = 5bf2cd1d. For lengths 55 and
63, whose XOR is 8, define for any w4, w5

    w4' = ((K + w4) XOR 8) - K        w5' = w5 + w4 - w4'.

**Lemma L.** K2 with block length 55 and words (w4, w5) leaves the same four
state words as K2 with block length 63 and words (w4', w5').

Proof. Let a1 = K + w4. In the second execution the first assignment gives
K + w4' = a1 XOR 8, so the second gives ROR(63 XOR a1 XOR 8, 16) =
ROR(55 XOR a1, 16) because 63 XOR 8 = 55: the same d1. The third and fourth
depend only on d1 and constants. The fifth gives
(a1 XOR 8) + b1 + w5' = a1 + b1 + w5 because
w5' - w5 = w4 - w4' = a1 - (a1 XOR 8). The last three depend only on values
already shown equal. QED.

Hence two messages of 55 and 63 bytes that share every word except w4, w5,
related as above, have the same state S after the column step and the same
state X after round 0, since no other call of round 0 reads v[14], w4 or w5
before K2 has made the states equal.

*Which words must be zero.* For both messages to be honest byte strings of
their lengths with the same words w6..w15, the bytes 55 to 63 of the block
must be zero in both. In the 55-byte message they are zero fill. In the
63-byte message bytes 55 to 62 are its last eight bytes, which are chosen
to be zero, and byte 63 is zero fill. Byte 55 is the top byte of w13, bytes
56 to 59 are w14 and bytes 60 to 63 are w15. So the family needs

    w14 = 0,   w15 = 0,   top byte of w13 = 0,

and nothing else: bytes 0 to 54 are free in both messages.

**3.2 A pinned call C3.** Fix the six constants

    X3 = 29d4fa98   X7 = bee3af28   X11 = 44036000   X15 = 40c58500
    W4 = 97475638   W13 = 0007c006

The top byte of W13 is zero. K + W4 = f33a2355 and W4' = ((K + W4) XOR 8) - K =
97475640, so W4 - W4' = fffffff8, that is -8 modulo 2^32. Evaluate C3 =
G(3,7,11,15, w4, W13) on the inputs (X3, X7, X11, X15) with w4 = W4 and with w4
= W4':

    w4 = W4    a1=7ffffff8 d1=7af83f3a c1=befb9f3a b1=01200183
               a2=8127c181 d2=bbfbdffe c2=7af77f38 b2=76f7aefd
    w4 = W4'   a1=80000000 d1=8500c0c5 c1=c90420c5 b1=fed77e78
               a2=7edf3e7e d2=bbfbdffe c2=850000c3 b2=76f7aefd

**Fact P.** The two executions give the same d output bbfbdffe and the same b
output 76f7aefd. They differ in the a output (8127c181, 7edf3e7e) and in the c
output (7af77f38, 850000c3). This is a finite computation on the displayed
constants.

**3.3 Half of the digest does not see the difference.**

**Lemma H.** Take two executions of the 2-round compression that have the same
state X after round 0 and the same message words except w4 and w5. Suppose
(X[3], X[7], X[11], X[15]) = (X3, X7, X11, X15), w13 = W13, and w4 is W4 in the
first execution and W4' in the second. Then the two digests agree on digest
words 0, 2, 5 and 7.

Proof. C0, C1, C2 read neither w4 nor w5 and act on identical states, so they
leave identical values in both executions. C3 reads state words 3, 7, 11, 15
and the words w4, w13; by Fact P it leaves the same v[7] and v[15] in both
executions and may differ only in v[3] and v[11]. So Y agrees except possibly
in Y[3] and Y[11]. E0 reads Y[0], Y[5], Y[10], Y[15] and w1, w11. E2 reads
Y[2], Y[7], Y[8], Y[13] and w9, w14. None of these is Y[3], Y[11], w4 or w5, so
E0 and E2 produce identical outputs Z[0], Z[5], Z[10], Z[15] and Z[2], Z[7],
Z[8], Z[13]. Finally o[0] = Z[0] XOR Z[8], o[2] = Z[2] XOR Z[10],
o[5] = Z[5] XOR Z[13] and o[7] = Z[7] XOR Z[15] use only those eight words.
QED.

The remaining digest words o[1] = Z[1] XOR Z[9], o[3] = Z[3] XOR Z[11],
o[4] = Z[4] XOR Z[12] and o[6] = Z[6] XOR Z[14] are computed from the outputs
of E1 and E3 only. The **residual** of a pair is the 128-bit string
R = (o[1] XOR o'[1], o[3] XOR o'[3], o[4] XOR o'[4], o[6] XOR o'[6]). The pair
is a collision exactly when R = 0.

## 4. Construction: the message from eight words, in three levels

This section, Section 5 and Section 6 build the root instance of the
construction, whose messages are single chunks compressed with counter 0 and
flags 11 (Section 1). The counter instance, which the claim uses, is built in
Section 8 from the same constants (6.4).

The construction places the six constants of 3.2 where Lemma H needs them and
gives Y4, the b output of C0, a prescribed value y. Its input is eight free
words. Six form an *outer step*: C0.c1 and C0.d1 (the third and the second
value of the round-1 call C0), D3.d1 (the second value of the round-0 call D3),
S15 and S9 (words of the state S) and the message word w5. The seventh is X2, a
word of the state X; with it the six are a *context*. The eighth is y. X3, X7,
X11, X15 are the constants, w4 = W4, w13 = W13 and w14 = w15 = 0.

*Names.* TAG.a1, TAG.d1, TAG.c1, TAG.b1 are the first to fourth value of the
call TAG (Section 2); its outputs carry the names of the state S, X or Y they
are written to; entry c66f230d writes vc, vd, vb, va for C0.c1, C0.d1, C0.b1,
C0.a1. Arithmetic is modulo 2^32. The earlier program (6.4) has steps O and M in
`outer` and `middle` ("Step S1" of entry c66f230d), step Y in `member`, step T
in `trial`.

**Step O (the outer step; 29 lines).**

    K2, forwards from w5; its first four values are constants:
        K2.a1 = IV[2] + IV[6] + W4;   K2.d1 = ROR(55 XOR K2.a1, 16)
        K2.c1 = IV[2] + K2.d1;   K2.b1 = ROR(IV[6] XOR K2.c1, 12)
        S2 = K2.a1 + K2.b1 + w5;   S14 = ROR(K2.d1 XOR S2, 8)
        S10 = K2.c1 + S14;   S6 = ROR(K2.b1 XOR S10, 7)
    D3 with w14 = w15 = 0, from D3.d1, its inputs S9, S14, its output X3:
        D3.a1 = ROL(D3.d1,16) XOR S14;   D3.c1 = S9 + D3.d1
        D3.b1 = X3 - D3.a1;   S4 = ROL(D3.b1,12) XOR D3.c1
        S3 = D3.a1 - S4;   X14 = ROR(D3.d1 XOR X3, 8)
        X9 = D3.c1 + X14;   X4 = ROR(D3.b1 XOR X9, 7)
    K3, backwards from its outputs S3, S15:
        K3.d1 = ROL(S15,8) XOR S3;   K3.c1 = IV[3] + K3.d1
        K3.b1 = ROR(IV[7] XOR K3.c1, 12);   S11 = K3.c1 + S15
        S7 = ROR(K3.b1 XOR S11, 7);   K3.a1 = ROL(K3.d1,16) XOR 11
        w6 = K3.a1 - IV[3] - IV[7];   w7 = S3 - K3.a1 - K3.b1
    C0, third assignment and fourth value; D2, backwards from X7, X8, S7:
        X8 = C0.c1 - C0.d1;   C0.b1 = ROR(X4 XOR C0.c1, 12)
        D2.b1 = ROL(X7,7) XOR X8;   D2.c1 = ROL(D2.b1,12) XOR S7
        X13 = X8 - D2.c1

**Step M (the middle step; 21 lines, from X2).**

    D2, rest:
        D2.a1 = X2 - D2.b1 - W13;   D2.d1 = ROL(X13,8) XOR X2
        S13 = ROL(D2.d1,16) XOR D2.a1;   S8 = D2.c1 - D2.d1
        w12 = D2.a1 - S2 - S7
    K1, backwards from its outputs S9, S13:
        K1.c1 = S9 - S13;   K1.d1 = K1.c1 - IV[1]
        K1.a1 = ROL(K1.d1,16);   K1.b1 = ROR(IV[5] XOR K1.c1, 12)
        S1 = ROL(S13,8) XOR K1.d1;   S5 = ROR(K1.b1 XOR S9, 7)
        w2 = K1.a1 - IV[1] - IV[5];   w3 = S1 - K1.a1 - K1.b1
    K0, backwards from its outputs S4, S8:
        K0.b1 = ROL(S4,7) XOR S8;   K0.c1 = ROL(K0.b1,12) XOR IV[4]
        K0.d1 = K0.c1 - IV[0];   K0.a1 = ROL(K0.d1,16)
        S12 = S8 - K0.c1;   S0 = ROL(S12,8) XOR K0.d1
        w0 = K0.a1 - IV[0] - IV[4];   w1 = S0 - K0.a1 - K0.b1

**Step Y (the member; 10 lines, from y and the outer step, without X2).**

    C0, backwards from its b output y:
        Y8 = ROL(y,7) XOR C0.b1;   Y12 = Y8 - C0.c1
        Y0 = ROL(Y12,8) XOR C0.d1;   C0.a1 = Y0 - C0.b1 - w6
        X12 = ROL(C0.d1,16) XOR C0.a1
    D1, backwards from its outputs X11, X12, with its inputs S6, S11:
        D1.c1 = X11 - X12;   D1.b1 = ROR(S6 XOR D1.c1, 12)
        X6 = ROR(D1.b1 XOR X11, 7);   D1.d1 = D1.c1 - S11
        X1 = ROL(X12,8) XOR D1.d1

**Step T (the four words w8..w11; 12 lines).**

    C0, its first assignment:
        X0 = C0.a1 - X4 - w2
    D0, backwards from its outputs X0, X15:
        D0.d1 = ROL(X15,8) XOR X0;   D0.c1 = S10 + D0.d1
        X10 = D0.c1 + X15;   D0.b1 = ROR(S5 XOR D0.c1, 12)
        X5 = ROR(D0.b1 XOR X10, 7);   D0.a1 = ROL(D0.d1,16) XOR S15
        w8 = D0.a1 - S0 - S5;   w9 = X0 - D0.a1 - D0.b1
    D1, rest:
        D1.a1 = ROL(D1.d1,16) XOR S12;   w10 = D1.a1 - S1 - S6
        w11 = X1 - D1.a1 - D1.b1

**Step S2.** w4' = W4' and w5' = w5 + W4 - W4', all modulo 2^32. For the
constants of 3.2 that is w5' = w5 + fffffff8, the same as w5 - 8.

**Step S3.** A is the first 55 bytes of the little-endian encoding of w0..w15;
B is the first 63 bytes of that of the same words with w4', w5' for w4, w5.

*Round 1, forwards (24 lines).* The tests of 6.3 read these values of round 1
of message A. Y3 and Y11 are the constants of Fact P for w4 = W4, and Y4 = y.

    C1, the call G(X1, X5, X9, X13; w3, w10):
        C1.a1 = X1 + X5 + w3;   C1.d1 = ROR(X13 XOR C1.a1, 16)
        C1.c1 = X9 + C1.d1;   C1.b1 = ROR(X5 XOR C1.c1, 12)
        Y1 = C1.a1 + C1.b1 + w10;   Y13 = ROR(C1.d1 XOR Y1, 8)
        Y9 = C1.c1 + Y13;   Y5 = ROR(C1.b1 XOR Y9, 7)
    C2, the call G(X2, X6, X10, X14; w7, w0):
        C2.a1 = X2 + X6 + w7;   C2.d1 = ROR(X14 XOR C2.a1, 16)
        C2.c1 = X10 + C2.d1;   C2.b1 = ROR(X6 XOR C2.c1, 12)
        Y2 = C2.a1 + C2.b1 + w0;   Y14 = ROR(C2.d1 XOR Y2, 8)
        Y10 = C2.c1 + Y14;   Y6 = ROR(C2.b1 XOR Y10, 7)
    E1 on A, with its c input Y11; third and fourth assignment in one line:
        E1.a1 = Y1 + Y6 + w12;   E1.d1 = ROR(Y12 XOR E1.a1, 16)
        E1.b1 = ROR(Y6 XOR (Y11 + E1.d1), 12);   E1.a2 = E1.a1 + E1.b1 + w5
    E3 on A, with its a input Y3 and w15 = 0; first and second in one line:
        E3.h1 = ROR(Y14 XOR (Y3 + Y4), 16);   E3.g1 = Y9 + E3.h1
        E3.f1 = ROR(Y4 XOR E3.g1, 12);   E3.e2 = (Y3 + Y4) + E3.f1 + w8

These 24 lines define nothing of the message. E3.h1, E3.g1, E3.f1, E3.e2 are
the h1, g1, f1, e2 of 6.2, and the word z of Lemma A is C2.d1 XOR Y2.

**The order and the levels.** The 29 + 21 + 10 + 12 + 24 = 96 lines above are
taken in the printed order. Lines of step O are *outer*, of step M *middle*, of
step Y *table* lines; the 12 lines of step T and the 24 of round 1 are the 36
*trial* lines. Table C gives each call's eight assignments by their left sides.

| Call | 1st | 2nd | 3rd | 4th | 5th | 6th | 7th | 8th |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| K0 | w0 | K0.a1 | K0.d1 | K0.c1 | w1 | S0 | S12 | K0.b1 |
| K1 | w2 | K1.a1 | K1.d1 | K1.b1 | w3 | S1 | K1.c1 | S5 |
| K2 | K2.a1 | K2.d1 | K2.c1 | K2.b1 | S2 | S14 | S10 | S6 |
| K3 | w6 | K3.a1 | K3.c1 | K3.b1 | w7 | K3.d1 | S11 | S7 |
| D0 | w8 | D0.a1 | D0.c1 | D0.b1 | w9 | D0.d1 | X10 | X5 |
| D1 | w10 | D1.a1 | D1.d1 | D1.b1 | w11 | X1 | D1.c1 | X6 |
| D2 | w12 | S13 | S8 | D2.c1 | D2.a1 | D2.d1 | X13 | D2.b1 |
| D3 | S3 | D3.a1 | D3.c1 | S4 | D3.b1 | X14 | X9 | X4 |
| C0 | X0 | X12 | X8 | C0.b1 | C0.a1 | Y0 | Y12 | Y8 |
| C1 | C1.a1 | C1.d1 | C1.c1 | C1.b1 | Y1 | Y13 | Y9 | Y5 |
| C2 | C2.a1 | C2.d1 | C2.c1 | C2.b1 | Y2 | Y14 | Y10 | Y6 |

The inputs, message words and outputs of the eleven calls are those of Section
1 for n = 55: Ki (i = 0..3) maps (IV[i], IV[i+4], IV[i], d) with d = 0, 0, 55,
11 to (S[i], S[i+4], S[i+8], S[i+12]); D0..D3 map (S0, S5, S10, S15), (S1, S6,
S11, S12), (S2, S7, S8, S13), (S3, S4, S9, S14), and C0..C2 map (X0, X4, X8,
X12), (X1, X5, X9, X13), (X2, X6, X10, X14), to the X and the Y words of the
same indices.

**Lemma T2.** (a) *Triangular.* In the printed order every line assigns a name
that no earlier line assigns and that is neither one of the eight words nor a
constant, and it reads only constants, the eight words (the eighth under the
name Y4 in the lines of round 1) and names of earlier lines. A line of step O
reads no word other than the six of the outer step, a line of step M reads
neither y nor a name of step Y, and a line of step Y reads neither X2 nor a
name of step M. Every line is one assignment of one call, solved for the name
on its left; the two exceptions are the lines for E1.b1 and for E3.h1, each of
which is two assignments with the first substituted into the second (c1 = Y11 +
E1.d1 and e1 = Y3 + Y4 + w15), and the line for E3.e2 uses the same e1. By
Table C the 96 lines are, each exactly once: the eight assignments of each of
the eleven calls K0..K3, D0..D3, C0..C2, with the inputs and the message words
of Section 1 for block length 55, with w4 = W4, w13 = W13, w14 = w15 = 0, and
with the constants X3, X7, X11, X15 as the a output of D3, the b output of D2,
the c output of D1 and the d output of D0; and the first five assignments of
E1 and of E3 for message A.

(b) *The calls.* For every choice of the eight words, the names of steps O, M,
Y and T are the executions of the eleven calls as listed after Table C, each
with its two message words; C0 has first, second, third and fourth value C0.a1,
C0.d1, C0.c1, C0.b1 and outputs (Y0, y, Y8, Y12); and E1.a1, E1.d1, E1.b1,
E1.a2 and E3.h1, E3.g1, E3.f1, E3.e2 are the first, second, fourth and fifth
value of E1 and the second, third, fourth and fifth value of E3 in the
compression of message A.

(c) *The levels.* An outer line is a function of the six words alone. A middle
line is a function of the six words and X2 and does not depend on y. A table
line is a function of the six words and y and does not depend on X2. In
particular the sixteen message words of two trials of one context differ at
most in w8, w9, w10, w11.

(d) *Admissible blocks.* Call a block (w0, .., w15) *admissible* if w4 = W4,
w13 = W13, w14 = w15 = 0 and round 0 on it with block length 55 ends with
(X[3], X[7], X[11], X[15]) equal to the four constants. The map of this section
from the eight words to the block of A is a bijection onto the admissible
blocks.

Proof. (a) is read off the displays, each formula compared with Section 2 and
its call's inputs, outputs and message words; Table C has one name in each of
its 88 cells, all different, and with the eight of E1 and E3 they are the 96.

(b) An assignment solved for one of its terms is an equivalent equation modulo
2^32 (Fact 1), so a line's assignment holds once it has run, and by (a) no
later line changes its names. By (a) and Table C all eight assignments of each
call hold, a constant output in its place (lines D3.b1, X14; D2.b1; D1.c1, X6;
D0.d1, X10) and y as the b output of C0 (line Y8); by Fact 1 the names are the
execution of the call. The E1 and E3 lines are those of 6.2 for message A with
Y11, Y3 of Fact P, run forwards from A's Y1, Y6, Y12, Y4, Y9, Y14.

(c) By induction over the printed order, with (a): an outer line reads only
constants, the six words and outer lines; a middle line in addition only X2
and middle lines; a table line in addition only y and table lines. w6, w7 are
outer and w0..w3, w12 middle lines, w5 is one of the six words, w4, w13, w14,
w15 are constants; only w8..w11 are trial lines.

(d) By (b), round 0 with block length 55 on an output block leaves the state X
of the names, with the constants as X[3], X[7], X[11], X[15], and the pinned
words are constants: the block is admissible. *Injective:* by (b) each of the
eight words is a value in the compression of A, so a function of the block.
*Onto:* the forward values of an admissible block (block length 55) satisfy
every equation of (a): they execute the calls, the constant outputs hold by
admissibility, and C3 has the inputs X3, X7, X11, X15, W4, W13, so Y3, Y11 are
those of Fact P. Run on the eight words taken from them, each line returns the
forward value of its name, by induction, since an assignment has exactly one
solution for any one term given the others. So the lines return the block. QED.

## 5. The half-collision

**Theorem.** For every choice of the seven words of a context (C0.c1, C0.d1,
D3.d1, S15, S9, w5, X2) and of the word y, steps O, M, Y, T, S2 and S3 output
two distinct messages A and B, of 55 and 63 bytes, whose complete 2-round
digests agree on digest words 0, 2, 5 and 7; and in both compressions the b
output of C0 is Y4 = y.

Proof. The sixteen words of steps O, M, Y and T have w14 = w15 = 0 and w13 =
W13, whose top byte is zero. So bytes 55 to 63 of their encoding are zero: A,
the first 55 bytes, is an honest 55-byte message whose zero-filled block is the
sixteen words, and B is an honest 63-byte message that ends in eight zero bytes
and whose zero-filled block is the sixteen words with w4, w5 replaced (3.1).
Run round 0 on the words of A with block length 55. By Lemma T2 (b) the column
calls leave the state S of the names and the diagonal calls, which act on
disjoint state words, leave the state X of the names. So the state after round
0 has (X[3], X[7], X[11], X[15]) equal to the four constants, and w4 = W4, w13
= W13. By Lemma L the compression of B has the same state X after round 0. The
two compressions share every word except w4, w5, so Lemma H gives the four
digest words. C0 reads X0, X4, X8, X12 and w2, w6, which are the same in both
compressions, and has b output y by Lemma T2 (b). The messages are distinct
because their lengths differ. QED.

Distinct choices of the eight words give distinct messages A: C0.c1 and C0.d1
are values inside C0, D3.d1 is a value inside D3, S15 and S9 are state words
after the column step of round 0, w5 is a message word, X2 is a state word
after round 0 and y is a state word after the column step of round 1, and all
of them are functions of the message (Lemma T2 (d)). The construction yields
2^256 different half-colliding pairs.

## 6. The root instance: trials, tests and the counted batch

**6.1 Trials.** A *context* is the six words of an outer step (C0.c1, C0.d1,
D3.d1, S15, S9, w5), a word X2, and everything that steps O and M compute from
them. The class and the sub-class defined next are sets of values of Y4. A
**trial** is a context and a member y of the sub-class; its messages A and B
are the output of steps O, M, Y, T, S2 and S3 for the context's seven words and
y. Only steps Y and T depend on y: the trials of one context differ in the four
message words w8..w11 and in nothing else of the message (Lemma T2 (c)). Step Y
does not depend on X2: for one outer step and one member its ten names are the
same for all 2^32 values of X2. The table of 6.5 rests on this.

*The class.* The first message word of E3 is w15 = 0, so the first assignment
of E3 is e1 = Y3 + Y4 for message A and e1' = Y3' + Y4 for message B, with Y3 =
8127c181 and Y3' = 7edf3e7e from Fact P. Put DY3 = Y3' - Y3 = fdb77cfd. The
second assignment is h1 = ROR(Y14 XOR e1, 16), so the XOR difference between A
and B of E3's first-half d value is

    eta = h1 XOR h1' = ROR((Y3 + Y4) XOR (Y3 + Y4 + DY3), 16),

a function of Y4 alone. Fix eta = 830303cf. The *class* is the set of all words
Y4 that give this eta.

**Lemma Q.** The class is the set of all Y4 with

    ((Y3 + Y4) AND 03cf8303) = 030c0303.

It has 524,288 members: the 19 bits of e1 = Y3 + Y4 at the positions where
03cf8303 has a zero are free, bit 31 among them, and Y4 = e1 - Y3.

Proof. Put x = ROL(eta,16) = 03cf8303, which has no bit 31. Y4 is in the class
exactly when e1 XOR (e1 + DY3) = x, that is when (e1 XOR x) - e1 = DY3 modulo
2^32. For words e and x, (e XOR x) - e is, modulo 2^32, the sum over the bits i
of x of 2^i where bit i of e is 0 and of -2^i where it is 1, which is 2 ((NOT
e) AND x) - x. So the condition is 2 ((NOT e1) AND x) = DY3 + x = 01870000
modulo 2^32. As (NOT e1) AND x has no bit 31, the doubling is exact and the
condition is ((NOT e1) AND x) = 01870000 >> 1 = 00c38000. All bits of 00c38000
lie in x, so this fixes the 13 bits of e1 on x to (e1 AND x) = (NOT 00c38000)
AND x = 030c0303 and leaves the other 19 bits free. QED.

*The sub-class.* The search uses only the members of the class whose e1 = Y3 +
Y4 has bit 21 and bit 26 equal to zero. With Lemma Q that is the set of all Y4
with

    ((Y3 + Y4) AND 07ef8303) = 030c0303.

**Lemma Q2.** The sub-class is a subset of the class and has 131,072 members:
the 17 bits of e1 at the positions 2 to 7, 10 to 14, 20 and 27 to 31, where
07ef8303 has a zero, are free, and Y4 = e1 - Y3.

Proof. 07ef8303 = 03cf8303 OR 04200000, and 04200000 has the bits 21 and 26,
which are two of the 19 positions that Lemma Q leaves free. The value 030c0303
has zeros at both. So the condition is the condition of Lemma Q together with
bit 21 = bit 26 = 0, and 17 positions stay free. QED.

Member number k of the sub-class, for 0 <= k < 131072, is the Y4 whose e1 has
the bits of k at its 17 free positions, in increasing order of position. From
here on "member" means a member of the sub-class. A part of the class is
searched and not all of it because, under the model of Section 13, the rate of
collisions differs from member to member and is higher on this part. Nothing
exact depends on that.

**Lemma T.** For every context and every member y of the class, and so for
every member of the sub-class, the messages A and B of the trial are distinct
messages of 55 and 63 bytes whose complete 2-round digests agree on digest
words 0, 2, 5 and 7; in both compressions Y4 = y; and the XOR difference
between A and B of E3's first-half d value is eta = 830303cf.

Proof. The first two statements are the theorem of Section 5. In both
compressions w15 = 0 and Y14 is the same, the a input of E3 is Y3 for A and Y3'
for B by Fact P, and Y4 = y is a member of the class, so the difference is eta
by the definition of the class. QED.

**6.2 The residual of a trial.** With Y3, Y3', Y11, Y11' the a and c outputs of
C3 from Fact P (8127c181, 7edf3e7e, 7af77f38, 850000c3), delta = W4 - W4' =
fffffff8 and the trial's words and state:

    (.., Y4, .., Y12) = C0 = G(X0, X4, X8, X12, w2, w6)
    (Y1, .., Y9, ..)  = C1 = G(X1, X5, X9, X13, w3, w10)
    (.., Y6, .., Y14) = C2 = G(X2, X6, X10, X14, w7, w0)
    E1 on A:  G(Y1, Y6, Y11,  Y12, w12, w5)
    E1 on B:  G(Y1, Y6, Y11', Y12, w12, w5 + delta)
    E3 on A:  G(Y3,  Y4, Y9, Y14, w15, w8)
    E3 on B:  G(Y3', Y4, Y9, Y14, w15, w8)

and R is formed from the eight output words of E1 and E3 as in 3.3. Y4 = y
and Y12 are known from step Y without evaluating C0 forwards. Write a1, d1,
c1, b1, a2, .. for the assignments of E1 and e1, h1, g1, f1, e2, h2, g2, f2
for those of E3 in the order a, d, c, b; a prime marks message B.

**6.3 Two tests of a trial.** The algorithm uses two tests: rule A, a condition
on one word of E3 (Lemma A), and the E1 test, a 32-bit condition on E1 alone
(Lemma N).

**Lemma N.** For a trial of 6.1 put beta = b1 XOR b1' and eps = c2 XOR c2',
both taken from E1, and

    n = eps XOR ROL(beta XOR eps, 1) XOR eta.

Let D3 and D6 be the XOR differences between A and B of digest words 3 and
6, which are the second and the fourth word of R. Then n = D3 XOR ROL(D6, 8)
for every trial. In particular R = 0 implies n = 0.

Proof. Digest word 3 is Z[3] XOR Z[11], the a output of E3 and the c output
of E1, so D3 = (e2 XOR e2') XOR eps. Digest word 6 is Z[6] XOR Z[14], the b
output of E1 and the d output of E3, so D6 = (b2 XOR b2') XOR (h2 XOR h2').
In E1, b2 = ROR(b1 XOR c2, 7), so b2 XOR b2' = ROR(beta XOR eps, 7). In E3,
h2 = ROR(h1 XOR e2, 8), and h1 XOR h1' = eta for every Y4 in the class
(Lemma T), so h2 XOR h2' = ROR(eta XOR e2 XOR e2', 8). Rotating D6 left by 8
gives ROL(D6, 8) = ROL(beta XOR eps, 1) XOR eta XOR (e2 XOR e2'). The XOR
with D3 cancels e2 XOR e2' and leaves n. QED.

A trial *passes the E1 test* when n = 0. The word n needs the first seven
assignments of E1 for both messages and nothing of E3, whose eta is the
constant of the class.

*Rule A.* Let h1 be the second value of E3 on message A, as in 6.2, and write
h[i] for bit i of h1, bit 0 being the lowest. A trial *satisfies rule A* when
all of the following hold:

    h[0] = 0;    h[1] = 1;    h[16] = 0;    h[17] = 0;
    h[2] XOR h[10] = 1;    h[3] XOR h[11] = 1;
    h[3] XOR h[12] XOR h[24] = 0;    h[6] XOR h[13] XOR h[25] = 0.

Each of the eight conditions contains a bit that no other contains (bits 0, 1,
16, 17, 10, 11, 12 and 13), so they are independent and a uniform word
satisfies rule A with probability 2^-8.

**Lemma A.** Write z[i] and e[i] for bit i of the words z and e1 defined next.

(a) For a trial of 6.1 let z = C2.d1 XOR Y2 be the XOR of the second and the
fifth value of C2, and e1 = Y3 + Y4. Then ROL(h1, 24) = z XOR ROL(e1, 8): h[i]
= z[(i + 24) mod 32] XOR e[(i + 16) mod 32].

(b) For every Y4 in the sub-class, the trial satisfies rule A exactly when

    z[24] = 0;    z[25] = 1;    z[8] = 1;    z[9] = 1;
    z[26] XOR z[2] = 0;    z[27] XOR z[3] = e[27];
    z[27] XOR z[4] XOR z[16] = e[28];   z[30] XOR z[5] XOR z[17] = 1 XOR e[29].

The bits 27, 28 and 29 of e1 are free in the sub-class, so the last three right
sides depend on the member.

(c) Let Z be a word of 36 bits or a lane of a packed word of 6.5 whose low 32
bits are z; its bits 32 to 35 and the neighbouring lanes may hold anything.
Form the word y by

    s = (Z << 12) AND 0003c000;    y = Z XOR s;
    s = s << 12;                   y = y XOR s;
    s = (y << 13) AND 40010000;    y = y XOR s,

the shifts being shifts of the whole packed word and each mask word holding the
printed value in every lane (6.5). Write y[i] for bit i of the lane. Then

    y[8] = z[8];    y[9] = z[9];    y[24] = z[24];    y[25] = z[25];
    y[26] = z[26] XOR z[2];    y[27] = z[27] XOR z[3];
    y[16] = z[16] XOR z[4] XOR z[3];    y[30] = z[30] XOR z[17] XOR z[5].

Put ALL = 4f010300, the word with the bits 8, 9, 16, 24, 25, 26, 27 and 30. For
a member of the sub-class let v be the word with

    v[8] = 0;    v[9] = 0;    v[24] = 1;    v[25] = 0;    v[26] = 1;
    v[27] = 1 XOR e[27];    v[16] = 1 XOR e[27] XOR e[28];    v[30] = e[29]

and zeros elsewhere. Then the trial satisfies rule A exactly when (y XOR v) AND
ALL = ALL.

(d) Put u = (y XOR v) AND ALL. Then u + (2^32 - ALL) is at most 2^32, and its
bit 32 is 1 exactly when the trial satisfies rule A.

Proof. (a) The sixth assignment of C2 is Y14 = ROR(C2.d1 XOR Y2, 8) = ROR(z,
8), and the second assignment of E3 is h1 = ROR(Y14 XOR e1, 16). So h1 = ROR(z,
24) XOR ROR(e1, 16), and rotating left by 24 gives the claim.

(b) By (a) the eight conditions read: z[24] XOR e[16] = 0; z[25] XOR e[17] = 1;
z[8] XOR e[0] = 0; z[9] XOR e[1] = 0; z[26] XOR e[18] XOR z[2] XOR e[26] = 1;
z[27] XOR e[19] XOR z[3] XOR e[27] = 1; z[27] XOR e[19] XOR z[4] XOR e[28] XOR
z[16] XOR e[8] = 0; z[30] XOR e[22] XOR z[5] XOR e[29] XOR z[17] XOR e[9] = 0.
The bits 0, 1, 8, 9, 16, 17, 18, 19, 22 and 26 of e1 lie in the mask 07ef8303
of Lemma Q2, so they have the same value for every member of the sub-class: in
030c0303 the bits 0, 1, 8, 9, 18 and 19 are 1 and the bits 16, 17, 22 and 26
are 0. Inserting these values gives the conditions on z. Bit 26 is fixed only
in the sub-class, not in the class.

(c) On one lane: in Z << 12, position p holds bit p - 12 of the same lane for
12 <= p <= 35, and the mask 0003c000 keeps the positions 14 to 17, so the first
s holds z[2], z[3], z[4], z[5] there and nothing else. The second s holds the
same four bits at the positions 26 to 29, still inside the lane; so y[26] =
z[26] XOR z[2], y[27] = z[27] XOR z[3], and the positions 3 and 17 hold z[3]
and z[17] XOR z[5]. In y << 13 the mask 40010000 keeps the positions 16 and 30,
which hold those two bits; after the third step y[16] = (z[16] XOR z[4]) XOR
z[3] and y[30] = z[30] XOR (z[17] XOR z[5]). The positions 8, 9, 24 and 25 never
change. Every bit that entered one of the eight positions is a bit 2, 3, 4, 5,
8, 9, 16, 17, 24, 25, 26, 27 or 30 of the lane itself: no bit above 31 and no
bit of another lane. That proves the eight equations. A position of v holds a 1
exactly where the right side that (b) requires is 0, so bit t of y XOR v is 1
exactly when y[t] has the required value. At the positions 8, 9, 24, 25, 26 and
27 these are six of the conditions of (b) as they stand, at 30 the eighth, and
at 16 it is y[16] = e[27] XOR e[28], the XOR of the sixth and the seventh
condition, because y[16] = (z[27] XOR z[3]) XOR (z[27] XOR z[4] XOR z[16]).
When the sixth holds, that one holds exactly when the seventh does. So all
eight positions of ALL hold a 1 in y XOR v exactly when all eight conditions of
(b) hold.

(d) u has no bit outside ALL, so u <= ALL, and u + (2^32 - ALL) >= 2^32 exactly
when u = ALL; the sum is at most 2^32. By (c), u = ALL exactly when the trial
satisfies rule A. QED.

*What Lemma A does not say.* Lemma A says that the word of (c) tests rule A
exactly. It does not say that a collision satisfies rule A, and that is not
true in general: there are solutions of R = 0 with Y4 in the sub-class whose h1
violates rule A. Rule A is therefore a filter that can lose solutions: a word
of seven trials in which no trial satisfies it is dropped, whether or not one
of its trials has a zero residual. How much it loses is answered in Section 13:
inside the sub-class the rule keeps all but 19,086.08 of the 185,377,197.55
counted, and for the difference beta* that the counter search uses it keeps all
of it, 67,698,688 of 67,698,688, because in every outcome of beta* every
solution satisfies rule A (10.1). On the whole class the same eight conditions
would keep less than half of the count; the rule is a rule for this sub-class
only.

**6.4 The root instance and the declared experiment.** Sections 4 to 6
build the *root instance* of the construction: its messages are single chunks of
55 and 63 bytes, and the colliding compression is the root compression, with
counter 0 and flags 11 (Section 1). The claim of this package is made for the
*counter instance* of Sections 7 to 9, whose messages have 1024 t + 55 and 1024
t + 63 bytes and whose colliding compression is that of the last chunk, with
counter t and flags 3. The two instances share the six constants, Fact P, Lemmas
L and H, the class, Lemma N and the machine of 6.5; the sub-class, rule A and
Lemma A belong to the root instance and to the 9.2 batch that our earlier
program held, not to the counter search of this package. The instances differ in
the counter and the flags that the compression reads, and in the order in which
the construction solves the assignments of rounds 0 and 1 (Sections 4 and 8).

The declared experiment `frontline-search` (experiments/frontline.py with its
manifest) runs the search of 9.1 itself, on the counter instance, at the scale
of one context per organizer trial, and returns a pair of the root instance. An
experiment of the organizer's harness returns pairs of complete messages and
tests an event on their two digests. The half-collision of the counter instance
is an agreement of four words of the chaining value of a chunk that is not the
root; the parent and root compressions above that chunk mix all eight words, so
the digests of a counter pair are not expected to agree on the masked words, and
on two counter pairs with t = 1 they do not (Section 7). This is the one thing
the experiment cannot show: the organizer can hash only the root instance, so
the half-collision of the counter instance has no organizer digest check. In the
root instance the colliding compression is the root itself, so its
half-collision is an agreement of four digest words, which the organizer
recomputes.

- *What a trial runs.* One Python 3 file, standard library only, with no BLAKE3
  library. From the seed, one context: seven fresh outer words and the 39
  context lines of Lemma Y, once. Then the walk of 9.9 on representative batches
  0 to 3 and the context's last, four-lane batch, 32 of the 16,384 clusters,
  with the five partner batches of every opened cluster. Every step of 9.1 runs
  as stated there: the packed gate key and the gate on the two borrows, with no
  T2 read on a closed gate; the opened count and its halt; test (2); the Q path
  with the E count and its halt, the packed Y9 path and T1; the passing lane
  with the pass count and its halt, the scalar rebuild, the words of (G7), the
  pre-check and the credit test against C15(T) with its halt; a second scalar
  rebuild into the bank of the global ledger; the joint solver of 9.4 with (G7)
  and (G15); the predicate of step 3 in traversal order; and, for the first
  certified root, both last-chunk compressions at counter t with flags 3 and the
  256-bit test. The entries of T1, T2 and P are computed on demand by the rules
  that fill them (Lemma DT, 9.9); the automata, VMASK, CT and the arrays of the
  solver are tabled.
- *What it charges.* The units of Section 11, added per event: 600 per context,
  74 per representative batch (56 for the four-lane one), 333 per opened
  cluster, 64 per Q path, 494 per passing lane and C15(T) per debit; the
  solver's ledger is also counted node by node and compared with C15(T). The
  program keeps the machine layout of 9.8 and 9.9 (the pair words, the
  reserved registers, the 37 caller words) in local variables, so these are the
  charges of the ledger, not counts of executed machine operations.
- *What it checks in the same run* (counted in checks; a disagreement counts as
  a mismatch): every member of every walked cluster recomputed straight-line by
  all 77 lines of step CO, with its omega mod 512 tested against the two
  prefixes of Lemma KP; every member of a closed cluster tested bit by bit for
  (2), a pass counting as a skipped pass (Lemma CL); every T2 and T1 entry used
  against a bit-serial decision of (2) and of (1); every packed sum for a carry
  across a lane (Lemma MB (d)); every passing rebuild against the packed lanes;
  every solver call repeated by the traversal without (G15), whose roots are
  certified by real compressions; on every E lane the step-CT message compressed
  at counter t with flags 3 and checked against the packed y, Y9 and omega;
  charts of step CT; and, in every 8th trial, a joint root planted from the
  equations (J1) to (J3), which both traversals must return.
- *What it returns.* For the trial's context and its first passing member
  (member 0 if none), the pair of the root instance built by steps CO and CT
  with the flags word 11 and the c1 that forces t = 0: a 55-byte and a 63-byte
  message. The hypothesis is the exact agreement of the two digests on words 0,
  2, 5 and 7, which the organizer recomputes; it follows from the proof of
  Theorem C (ii), which reads the flags only in the line for K3.d1. With it come
  16 observations, the program's own counts, which the organizer records as
  untrusted: members, e_lanes, passes, solver_calls, leaves, roots, certified,
  units, solver_units, opened, closed, skipped_pass, checks, mismatches, notes
  and halted.

A trial starts every count at zero and the credit full, and it reaches no
budget; its halt constants are those of the search at the rate factor 5/7 (9.1),
and its self-test drills each halt. A trial is not a rate measurement, does not
reach a root of the search at this scale, and is not evidence of attack cost.
The participant's runs of the program are in Section 13.

*The earlier program.* Our entries from 26ebba63 on (Section 15) filed another
program, experiments/halfsearch.py, which ran the root instance by the pieces of
6.5 and held the counter construction of Section 8 and the counter batch of 9.2.
It is not in this package. This text names its functions in backquotes
(`ctr_outer`, `CTR_TAUS` and so on) only where a participant check was made with
it; those checks are participant computations.

**6.5 Seven trials in one word.** A packed word holds seven lanes of 36 bits
at bit offsets 0, 36, .., 216. A lane represents its value modulo 2^32; bits
32..35 are carry guards. A constant is placed in all seven lanes before the
batches that use it. Additions are single 256-bit additions. A rotation of
every lane by r is the five operations

    PROR(z, r) = ((z >> r) AND A_r) OR ((z << (32-r)) AND B_r)

with A_r selecting the low 32-r bits of every lane and B_r the next r bits;
the masks discard guard bits and bits shifted in from the neighbouring lane,
so the result is reduced below 2^32. With M = 2^32 - 1 in every lane, the
complement of the low 32 bits of a lane is an XOR with M, a difference
x - y of a constant x and a lane y is (y XOR M) + (x + 1), and subtracting a
constant y is one addition of the constant -y.

*The two lists.* List word j holds the members 7j, .., 7j + 6 in the order of
their numbers; list word 18,724 holds the numbers 131,068 to 131,071, and the
last of them three times more. For list word j, U[j] holds ROL(y, 7) and V[j]
the word v of Lemma A (c), one member y per lane, member 7j + i in lane i. Each
list has 18,725 packed words, because 131072 = 18,724 * 7 + 4. Both lists are
computed once, from eta, the two bits of the sub-class, Y3 and the rule (Lemmas
Q2 and A). The build of the table reads U; stage A of a batch reads V.

*The words of an outer step.* Step O is run with every value in all seven
lanes, and 21 words are stored, each below 2^32 in every lane, in the form in
which the later pieces load them:

- loaded by the build of the table (7): C0.b1, -C0.c1, -C0.b1 - w6, -X4,
  ROL(C0.d1,16), S6, -S11;
- loaded by the middle step (8): -D2.b1 - W13, ROL(X13,8), -S2 - S7, S9 + 1,
  1 - S6, D2.c1 + 1, ROL(S4,7), w7;
- loaded by a batch (6): S10 + X15, X14, X13, X9, w5, w5 + delta.

*The table of an outer step.* Five lists of 18,725 packed words each, built
once per outer step from U, the seven words above and the word C0.d1 of the
context. For list word j and lane i, with y the member of that lane and the
names of step Y:

    Y12[j] = Y12        XA[j] = C0.a1 - X4        X6[j] = X6
    X1[j]  = X1         R[j]  = ROL(D1.d1, 16)

all modulo 2^32 and below 2^32 in every lane. The build computes, in every
lane:

- C0 backwards: Y8 = U[j] XOR C0.b1; Y12 = Y8 + (-C0.c1), reduced and stored;
  Y0 = ROL(Y12,8) XOR C0.d1; C0.a1 = Y0 + (-C0.b1 - w6); XA = C0.a1 + (-X4),
  reduced and stored; X12 = C0.a1 XOR ROL(C0.d1,16).
- D1 backwards: D1.c1 = (X12 XOR M) + (X11 + 1), which is X11 - X12; D1.b1 =
  ROR(D1.c1 XOR S6, 12); X6 = ROR(D1.b1 XOR X11, 7), stored; D1.d1 = D1.c1 +
  (-S11); X1 = ROL(X12,8) XOR D1.d1, reduced and stored; R = ROL(D1.d1,16),
  stored.

*The words of a middle step.* Step M is run in all seven lanes, and nine words
are stored: X2 itself; the seven words that a batch loads, X2 + w7, -w2, w0,
S5, w3, S12 and w12 - S1 - S6; and w1, which no batch loads (it is a word of
the message).

*What a batch computes.* The seven trials of a batch share a context and are
seven consecutive list places. Stage A computes in every lane:

- D0, as far as C2 needs it: X0 = XA[j] + (-w2); D0.d1 = X0 XOR ROL(X15,8); X10
  = D0.d1 + (S10 + X15), the third value S10 + D0.d1 plus X15 in one addition.
- C2 to z: its first value C2.a1 = X6[j] + (X2 + w7), its second, third and
  fourth value, the fifth as the first plus the fourth plus w0, and z, the XOR
  of the fifth and the second.
- Rule A: the word y of Lemma A (c) from z, u = (y XOR V[j]) AND ALL, the sum
  u + (2^32 - ALL) of Lemma A (d), and whether its bit 32 is set in some lane.

If it is set in no lane, the batch ends. Otherwise stage 2 computes:

- The entry count: the number of words that have run stage 2 is advanced and
  compared with the memory word `stage-2 budget`. In the earlier program that
  word held a constant of its counter batch (9.2); in the root instance its
  value has no influence on any output.
- C2, rest: z and the third value of C2 are formed again; Y14 = ROR(z, 8); and
  Y6 from the third value plus Y14 and the fourth value.
- D0, rest, and C1 to Y1: D0's third value as X10 + (-X15), D0.b1 with S5, and
  X5; C1's first value X5 + X1[j] + w3, its second, third and fourth value;
  D1.a1 = R[j] XOR S12; and the sum of C1's first value, its fourth value and
  D1.a1, which is Y1 + S1 + S6, since w10 = D1.a1 - S1 - S6.
- E1 on A and B: a1 as that sum plus Y6 plus the stored w12 - S1 - S6; d1 =
  ROR(a1 XOR Y12[j], 16); c1, c1', b1, b1', a2, a2', c2, c2', with Y11' and w5 +
  delta for B.
- The E1 test: eps = c2 XOR c2', beta XOR eps, the word n of Lemma N, and
  whether n is zero in some lane.

Nothing of E3 is evaluated in a batch: rule A is a condition on E3.h1, but by
Lemma A it is tested on z, a value of C2, with the bits of e1 folded into the
constants and into the list V. The words w8..w11 are never formed in a batch.

**Lemma T4 (the table).** Fix the six words of an outer step, and let the
memory hold the 21 words that step O stores for them. (a) For every list word j
the build stores the five words displayed above: in lane i, the values Y12,
C0.a1 - X4, X6, X1 and ROL(D1.d1,16) of the member of that lane, each below
2^32. (b) These five words do not depend on X2. (c) For every value of X2,
every list word j and every lane, the lines of a batch that read a table word
compute names of the trial (the six words, X2, the member of the lane):

    X0 = XA[j] - w2                          C2.a1 = X6[j] + X2 + w7
    C2.b1 = ROR(X6[j] XOR C2.c1, 12)         C1.a1 = X5 + X1[j] + w3
    D1.a1 = R[j] XOR S12                     E1.d1 = ROR(E1.a1 XOR Y12[j], 16).

Proof. (a) The ten lines of the build are the ten lines of step Y in the packed
forms of this section: U[j] is ROL(y,7), an addition of a stored word -v is the
subtraction of v, and (X12 XOR M) + (X11 + 1) is X11 - X12 modulo 2^32 in a
lane. No sum leaves its lane (below), so the low 32 bits of every lane are the
scalar value; the words stored after a sum are reduced by an AND with M, and R
and X6 are rotation outputs. XA is C0.a1 plus the stored -X4. (b) Y12, C0.a1,
X6, X1 and D1.d1 are table lines and X4 is an outer line, so by Lemma T2 (c)
none depends on X2. (c) The six equations are the lines for X0, C2.a1, C2.b1,
C1.a1, D1.a1 and E1.d1 of Section 4 with the words of (a) in place of the
names: XA[j] - w2 = C0.a1 - X4 - w2, R[j] XOR S12 = ROL(D1.d1,16) XOR S12, and
the other four contain X6, X1 and Y12 as they stand. QED.

*The machine.* The pieces run on a load/store machine with 16 registers. One
operation is charged for every addition, XOR, AND, OR and shift of 256-bit
words, for every comparison and for every branch, so PROR = 5. One load is
charged every time a word is fetched from memory, from a list or from the table
into a register, and one store every time a register is written to memory or to
the table. Shift distances are fixed in the instruction, and a register may hold
a memory word across several operations. Every sum of a batch stays below 9 *
2^32 and every sum of the build below 4 * 2^32 (bounds carried through the
lines; the self-test below reports the largest sum of each part next to its
bound), and a participant tool bounds the sums of the outer step and the middle
step below 7 * 2^32 and 8 * 2^32 by interval arithmetic: all are below 2^36, so
no carry leaves a lane and the low 32 bits of every lane equal the scalar value
modulo 2^32.

*Where these pieces ran.* The earlier program (6.4) contained the four pieces,
the counter construction and the counter batch of Sections 8 and 9, and the
machine that counts them, a packed word being one integer with seven 36-bit
lanes; for the rule with eight conditions, stage A of a batch counted 37
operations and 10 loads and stage 2 105 operations and 30 loads. Its self-test
checked every lane against the real messages of its trial, built by steps O, M,
Y, T, S2 and S3 and compressed in full with a 2-round compression written out
from Section 1: 14,000 of 14,000 lanes with N = 2,000 and seed 1, and 7,000,000
of 7,000,000 in a run filed with entry 64c075ac. These pieces belong to the root
instance; the program of this package does not run them, and they are not part
of the claim or of the charge of Section 11.

## 7. The tree lemma: the last chunk decides the digest

The claim is made for messages of more than one chunk. This section shows, from
the organizer's reference code, that for such a message the digest is a
function of the prefix and of the chaining value of the last chunk alone.

The organizer's hash, `verifier/blake3.py`, computes `blake3(data, rounds)`,
with rounds = 2 for this target, by these lines of its code:

    chunk_count = max(1, (len(data) + 1023) // 1024)
    stack = []
    for counter in range(chunk_count - 1):
        output = _chunk_output(data[counter * 1024:(counter + 1) * 1024], counter, rounds)
        cv = _compress(*output, rounds)[:8]
        total = counter + 1
        while total & 1 == 0:
            cv = _compress(*_parent_output(stack.pop(), cv), rounds)[:8]
            total >>= 1
        stack.append(cv)
    output = _chunk_output(data[(chunk_count - 1) * 1024:], chunk_count - 1, rounds)
    while stack:
        output = _parent_output(stack.pop(), _compress(*output, rounds)[:8])
    cv, words, _, block_len, flags = output
    root_words = _compress(cv, words, 0, block_len, flags | ROOT, rounds)
    return struct.pack("<8I", *root_words[:8])

There `_chunk_output(chunk, counter, rounds)` compresses every block of a chunk
but the last, starting from the chaining value IV, and returns the last block
as a descriptor (cv, words, counter, len(block), flags | CHUNK_END), where
flags is CHUNK_START = 1 when that block is the first of its chunk; its last
block starts at `last_offset = max(0, (len(chunk) - 1) // 64 * 64)`.
`_compress(cv, words, counter, block_len, flags, rounds)` is the compression of
Section 1 with v[0..7] = cv and v[12..15] = (counter mod 2^32, counter >> 32,
block_len, flags); it returns sixteen output words, of which the first eight
are the chaining value. `_parent_output(left, right)` is the descriptor (IV,
left + right, 0, 64, PARENT) of a parent node.

**Lemma TR (the last chunk decides).** Let t >= 1 and let F be any string of
1024 t bytes. For a string A of 1 to 64 bytes write words(A) for the sixteen
little-endian words of A followed by zero bytes up to 64 bytes, and CV_t(A) for
`_compress(IV, words(A), t, len(A), 3, 2)[:8]`.

(a) The last chunk of F || A is A, and the organizer's code compresses it once,
as `_compress(IV, words(A), t, len(A), 3, 2)`: the compression of Section 1
with block A, block length len(A), counter t and flags CHUNK_START |
CHUNK_END = 3. It is not the root compression.

(b) blake3(F || A, 2) is a function of F and of CV_t(A) alone.

(c) For strings A and B of 1 to 64 bytes with CV_t(A) = CV_t(B), blake3(F ||
A, 2) = blake3(F || B, 2).

Proof. (a) F || A has 1024 t + len(A) bytes with 1 <= len(A) <= 64, so
chunk_count = t + 1 and the last chunk is data[t * 1024:] = A. In
`_chunk_output(A, t, 2)`, last_offset = 0, so that function stops at its first
block, offset 0, and returns (IV, words(A), t, len(A), CHUNK_START |
CHUNK_END). The final loop of blake3 compresses this descriptor once, in its
first pass, which runs because the stack is not empty (b).

(b) The loop over counter = 0, .., t - 1 reads
data[counter*1024:(counter+1)*1024], which lies inside F, and no other byte of
the message; so the stack that it leaves depends on F alone. Each pass appends
one value and pops values only while total is even, so after t >= 1 passes the
stack holds as many values as t has one bits, at least one. The final loop
therefore runs at least once. Its first pass forms `_parent_output` of the top
of the stack and CV_t(A), and every later pass forms a parent descriptor from
the next value of the stack and the chaining value of the descriptor before it.
The root compression reads the last descriptor. So the digest is computed from
the stack, which depends on F alone, and from CV_t(A).

(c) follows from (b). QED.

The code accepts messages shorter than 2^61 bytes; the messages of this package
are shorter than 2^42 bytes (Section 8). The tree, its counters and flags and
its root output are those of the target profile. The two messages of a pair are
complete messages of the domain, and a pair with equal digests is an ordinary
collision, not a free-start or compression-only one. The converse of (c) is not
used.

*The digest does not show a partial agreement.* When CV_t(A) and CV_t(B) agree
on four words only, the parent and root compressions over them mix all eight,
and the two digests are not expected to agree on a fixed set of words. On two
counter pairs of Section 8 with t = 1, messages of 1,079 and 1,087 bytes, the
chaining values agree on words 0, 2, 5 and 7, and the two digests do not agree
on digest words 0, 2, 5 and 7 (participant computation with the organizer's
code). This is why the declared experiment returns a pair of the root instance
(6.4).

*Participant checks with the organizer's code.* In each of the following the
organizer's `verifier/blake3.py` was imported unchanged; they are participant
computations, which the organizer has not run. (1) For 2,000 trials of the
counter construction of Section 8 in 40 outer steps, 8 of them with outer words
0 or ffffffff, `_chunk_output` of the last chunk returned (IV, the block words,
t, 55 or 63, 3) for A and for B, and `_compress` returned the chaining value
that the earlier program computes, in 2,000 of 2,000; words 0, 2, 5 and 7 of the
two chaining values were equal in all 2,000 and all eight words in none; and
204,000 internal words of the construction were equal to a separately written
forward computation of the compression. (2) For five counter trials with t = 1,
3, 3, 4 and 16,383, the complete messages F || A and F || B, with F a string of
t chunks of pseudorandom bytes, were hashed by `blake3(m, 2)`. In each, the
messages have 1024 t + 55 and 1024 t + 63 bytes; the code makes exactly one
compression with block length 55 or 63, and its inputs are (IV, the block words,
t, 55 or 63, 3); its chaining values agree on words 0, 2, 5 and 7 and not on all
eight; the two digests differ; and when the output of that compression of F || B
is replaced by the output of the one of F || A, blake3 returns the digest of F
|| A, and the other way round. (3) Before the program was written a helper agent
checked (b) in the same way for 25 values of t from 1 to 1,025, on 150 messages
and 75 pairs with a replaced output, all as the lemma says.

## 8. The counter construction

*Words and constants.* The construction has nine free words: the seven *outer
words* C0.d1, D2.a1, D2.b1, S11, S4, X9 and w6 (`CTR_BASIS` of the earlier
program); a member y of the class of 6.1 (Lemma Q), which becomes the value of
Y4; and the *inner word* c1, which becomes the third value of E1 on message A.
The constants are those of Section 4: X3, X7, X11 and X15, w4 = W4, w13 = W13,
w14 = w15 = 0, the four constant first values K2.a1, K2.d1, K2.c1 and K2.b1 of
K2 given in step O, and Y3, Y11 of Fact P. The compression reads three more
values besides the message and the IV. K3 reads the flags, here 3 (the line for
K3.d1); K1 reads v[13], here 0 (the line for K1.a1); and K0 reads the counter
v[12], which is not fixed in advance: the line for t solves K0's second
assignment for it. The names are those of Section 4.

*The cube Q*.* Q* is the set of the 2^21 words c with (c AND 0e09818b) =
02008000; the earlier program names the mask and the value `CTR_MASK` and
`CTR_VALUE`. Member number j of Q*, for 0 <= j < 2^21, is the word whose bits at
the 21 positions where 0e09818b has a zero are the bits of j, in increasing
order of position (`ctr_c1` of the earlier program).

*Members.* In Sections 8 to 12 a *member* is a member of the class of Lemma Q,
not of the sub-class of 6.1. Member number k of the class, for 0 <= k < 2^19,
is the Y4 whose e1 = Y3 + Y4 has the bits of k at the 19 positions where
03cf8303 has a zero, in increasing order of position, and Y4 = e1 - Y3. The
search of this package uses every member; it has no sub-class and no rule A.

**Step CO (the outer step; 77 lines, from the seven outer words and y).**

    X2 = D2.a1 + D2.b1 + W13;   X8 = ROL(X7,7) XOR D2.b1
    C0.c1 = X8 + C0.d1;   K3.a1 = IV[3] + IV[7] + w6
    K3.d1 = ROR(K3.a1 XOR 3,16);   K3.c1 = IV[3] + K3.d1
    S15 = S11 - K3.c1;   S3 = ROL(S15,8) XOR K3.d1
    K3.b1 = ROR(IV[7] XOR K3.c1,12);   D3.a1 = S3 + S4
    S7 = ROR(K3.b1 XOR S11,7);   D3.b1 = X3 - D3.a1
    D2.c1 = ROL(D2.b1,12) XOR S7;   D3.c1 = ROL(D3.b1,12) XOR S4
    X4 = ROR(D3.b1 XOR X9,7);   X13 = X8 - D2.c1
    X14 = X9 - D3.c1;   C0.b1 = ROR(X4 XOR C0.c1,12)
    D2.d1 = ROL(X13,8) XOR X2;   D3.d1 = ROL(X14,8) XOR X3
    Y8 = ROL(Y4,7) XOR C0.b1;   S13 = ROL(D2.d1,16) XOR D2.a1
    S9 = D3.c1 - D3.d1;   Y12 = Y8 - C0.c1
    K1.c1 = S9 - S13;   Y0 = ROL(Y12,8) XOR C0.d1
    K1.d1 = K1.c1 - IV[1];   C0.a1 = Y0 - C0.b1 - w6
    K1.a1 = ROL(K1.d1,16);   w2 = K1.a1 - IV[1] - IV[5]
    X0 = C0.a1 - X4 - w2;   S14 = ROL(D3.d1,16) XOR D3.a1
    K1.b1 = ROR(IV[5] XOR K1.c1,12);   S10 = K2.c1 + S14
    D0.d1 = ROL(X15,8) XOR X0;   S5 = ROR(K1.b1 XOR S9,7)
    D0.c1 = S10 + D0.d1;   D0.b1 = ROR(S5 XOR D0.c1,12)
    X10 = D0.c1 + X15;   X5 = ROR(D0.b1 XOR X10,7)
    S1 = ROL(S13,8) XOR K1.d1;   w3 = S1 - K1.a1 - K1.b1
    X12 = ROL(C0.d1,16) XOR C0.a1;   D1.c1 = X11 - X12
    D1.d1 = D1.c1 - S11;   S8 = D2.c1 - D2.d1
    K0.b1 = ROL(S4,7) XOR S8;   S2 = ROL(S14,8) XOR K2.d1
    S6 = ROR(K2.b1 XOR S10,7);   X1 = ROL(X12,8) XOR D1.d1
    K0.c1 = ROL(K0.b1,12) XOR IV[4];   D1.b1 = ROR(S6 XOR D1.c1,12)
    C1.a1 = X1 + X5 + w3;   S12 = S8 - K0.c1
    w7 = S3 - K3.a1 - K3.b1;   X6 = ROR(D1.b1 XOR X11,7)
    C1.d1 = ROR(X13 XOR C1.a1,16);   D1.a1 = ROL(D1.d1,16) XOR S12
    C1.c1 = X9 + C1.d1;   C2.a1 = X2 + X6 + w7
    w10 = D1.a1 - S1 - S6;   C1.b1 = ROR(X5 XOR C1.c1,12)
    C2.d1 = ROR(X14 XOR C2.a1,16);   w12 = D2.a1 - S2 - S7
    Y1 = C1.a1 + C1.b1 + w10;   C2.c1 = X10 + C2.d1
    Y13 = ROR(C1.d1 XOR Y1,8);   C2.b1 = ROR(X6 XOR C2.c1,12)
    K0.d1 = K0.c1 - IV[0];   Y9 = C1.c1 + Y13
    S0 = ROL(S12,8) XOR K0.d1;   D0.a1 = ROL(D0.d1,16) XOR S15
    w8 = D0.a1 - S0 - S5;   w5 = S2 - K2.a1 - K2.b1
    w9 = X0 - D0.a1 - D0.b1;   w11 = X1 - D1.a1 - D1.b1
    Y5 = ROR(C1.b1 XOR Y9,7)

**Step CT (the trial; 16 lines, from c1 and the names of step CO).**

    E1.d1 = c1 - Y11;   E1.a1 = ROL(E1.d1,16) XOR Y12
    Y6 = E1.a1 - Y1 - w12;   Y10 = ROL(Y6,7) XOR C2.b1
    Y14 = Y10 - C2.c1;   E1.b1 = ROR(Y6 XOR c1,12)
    Y2 = ROL(Y14,8) XOR C2.d1;   E3.h1 = ROR(Y14 XOR (Y3 + Y4),16)
    w0 = Y2 - C2.a1 - C2.b1;   E3.g1 = Y9 + E3.h1
    K0.a1 = IV[0] + IV[4] + w0;   E3.f1 = ROR(Y4 XOR E3.g1,12)
    t = ROL(K0.d1,16) XOR K0.a1;   w1 = S0 - K0.a1 - K0.b1
    E1.a2 = E1.a1 + E1.b1 + w5;   E3.e2 = Y3 + Y4 + E3.f1 + w8

**Step CS (the messages).** If t = 0 the trial is invalid and is dropped: a
message with no full chunk before its last chunk has that chunk as its root,
compressed with counter 0 and flags 11 and not with the flags 3 that the line
for K3.d1 used. Otherwise the words w0 to w12 of the lines, with w4 = W4 and w13
= W13, and w14 = w15 = 0 form the block of A; A is the first 55 bytes of its
little-endian encoding, and B the first 63 bytes of that of the same words with
w4' = W4' and w5' = w5 + fffffff8 in place of w4 and w5, as in steps S2 and S3
of Section 4. F is the string of 1024 t zero bytes, and the two messages are F
|| A, of 1024 t + 55 bytes, and F || B, of 1024 t + 63 bytes. In the earlier
program step CO is `ctr_outer`, step CT and the two blocks of step CS are
`ctr_trial`, which returns nothing for t = 0, and the flags are the constant
`CTR_FLAGS` = 3.

*The order and the calls.* Table CT gives each call's eight assignments by the
name that the line for that assignment assigns; the cells K2.a1, K2.d1, K2.c1
and K2.b1 are the four constant values. E1's first five assignments are the
lines for Y6, E1.a1, E1.d1, E1.b1 and E1.a2, in the order of the assignments;
E3's first two assignments are the line for E3.h1, and its third to fifth the
lines for E3.g1, E3.f1 and E3.e2.

| Call | 1st | 2nd | 3rd | 4th | 5th | 6th | 7th | 8th |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| K0 | K0.a1 | t | K0.d1 | K0.c1 | w1 | S0 | S12 | K0.b1 |
| K1 | w2 | K1.a1 | K1.d1 | K1.b1 | w3 | S1 | K1.c1 | S5 |
| K2 | K2.a1 | K2.d1 | K2.c1 | K2.b1 | w5 | S2 | S10 | S6 |
| K3 | K3.a1 | K3.d1 | K3.c1 | K3.b1 | w7 | S3 | S15 | S7 |
| D0 | w8 | D0.a1 | D0.c1 | D0.b1 | w9 | D0.d1 | X10 | X5 |
| D1 | w10 | D1.a1 | D1.d1 | D1.b1 | w11 | X1 | D1.c1 | X6 |
| D2 | w12 | S13 | S8 | D2.c1 | X2 | D2.d1 | X13 | X8 |
| D3 | D3.a1 | S14 | S9 | D3.c1 | D3.b1 | D3.d1 | X14 | X4 |
| C0 | X0 | X12 | C0.c1 | C0.b1 | C0.a1 | Y0 | Y12 | Y8 |
| C1 | C1.a1 | C1.d1 | C1.c1 | C1.b1 | Y1 | Y13 | Y9 | Y5 |
| C2 | C2.a1 | C2.d1 | C2.c1 | C2.b1 | w0 | Y2 | Y14 | Y10 |

The order was found by a solver search of the participant's helper agents for
an order in which Y4 and E1.d1 are both free words.

**Lemma CT (the counter order).** (a) *Triangular.* In the printed order, step
CO and then step CT, every line assigns a name that no earlier line assigns and
that is neither one of the nine free words nor a constant, and it reads only
constants, the nine words and names of earlier lines; a line of step CO reads
neither c1 nor a name of step CT. Every line is one assignment of one call
solved for the name on its left; the exceptions are the line for E3.h1, which
is the first two assignments of E3 with the first substituted into the second
(e1 = Y3 + Y4 + w15, w15 = 0), and the line for E3.e2, which uses the same e1.
By Table CT the 93 lines and the four constant values of K2 are, each exactly
once, the eight assignments of each of the eleven calls K0..K3, D0..D3, C0..C2,
with the inputs and the message words of Section 1 for block length 55, counter
v[12] = t, v[13] = 0 and flags v[15] = 3, with w4 = W4, w13 = W13, w14 = w15 =
0, and with the constants X3, X7, X11, X15 as the a output of D3, the b output
of D2, the c output of D1 and the d output of D0; and the first five
assignments of E1 and of E3 for message A, E1 with c input Y11 and E3 with a
input Y3.

(b) *The calls.* For every choice of the nine words, the names of the lines are
the executions of these calls. In particular round 0 on the block of A, with
block length 55, counter t, v[13] = 0 and flags 3, leaves the state X of the
names, with the four constants as X[3], X[7], X[11] and X[15]; C0 has outputs
(Y0, y, Y8, Y12); and in the compression of A, E1.c1 = c1, since E1's third
assignment is E1.c1 = Y11 + E1.d1.

(c) *The levels.* A line of step CO is a function of the seven outer words and
y. Of the message words only w0 and w1 are lines of step CT, and so is the
counter t; every other message word is a line of step CO or a constant. So the
trials of one outer step differ in w0, w1 and t and in nothing else of their
two messages.

Proof. (a) is read off the displays, each formula compared with Section 2 and
with its call's inputs, outputs and message words (Section 1, with v[12] = t,
v[13] = 0 and v[15] = 3); Table CT has one name in each of its 88 cells, all
different, the four constant values of K2 among them, and with the five names
of E1 and the four lines of E3 they are the 93 lines and the four constants.
(b) As in Lemma T2 (b): an assignment solved for one of its terms is an
equivalent equation modulo 2^32 (Fact 1), so a line's assignment holds once it
has run, and by (a) no later line changes its names. By (a) and Table CT all
eight assignments of each call hold, a constant output in its place (the lines
for D3.b1 and D3.d1; X8; D1.c1 and X6; D0.d1 and X10) and y as the b output of
C0 (the line for Y8); by Fact 1 the names are the execution of the call. (c) By
induction over the printed order, with (a): a line of step CO reads only
constants, the seven outer words, y and lines of step CO; w2, w3, w5 and w7 to
w12 are lines of step CO, w6 is an outer word, w4, w13, w14 and w15 are
constants, and w0, w1 and t are lines of step CT. QED.

**Theorem C (the last-chunk half-collision).** For every choice of the seven
outer words, of a member y of the class and of a word c1, steps CO and CT
give a counter t. If t is not zero, step CS outputs two distinct messages F ||
A and F || B of 1024 t + 55 and 1024 t + 63 bytes, with 1 <= t < 2^32, such
that

(i) their last chunks are A and B, compressed with counter t, v[13] = 0 and
flags 3 (Lemma TR (a));

(ii) the chaining values CV_t(A) and CV_t(B) agree on words 0, 2, 5 and 7;

(iii) in both last-chunk compressions Y4 = y, and the XOR difference between A
and B of E3's first-half d value is eta = 830303cf;

(iv) in the compression of A, E1.c1 = c1; and if c1 is in Q*, the XOR
difference between A and B of E1's first-half b value is beta* = 18b0e098.

Proof. t is the XOR of two 32-bit words, so t < 2^32 and t >> 32 = 0, the value
v[13] = 0 that the line for K1.a1 used. The sixteen words have w14 = w15 = 0
and w13 = W13, whose top byte is zero, so A and B are honest strings of 55 and
63 bytes whose zero-filled blocks are the sixteen words and the same words with
w4 and w5 replaced, as in Section 5. By Lemma TR (a) the last chunks are
compressed with counter t, v[13] = 0, flags 3 and block lengths 55 and 63. By
Lemma CT (b) round 0 on the block of A leaves the state X of the names, with
the four constants as X[3], X[7], X[11] and X[15]. The counter, v[13] and the
flags are the same in both compressions, and K2 is the only call of round 0
that reads the block length, w4 or w5; Lemma L, whose proof concerns K2 alone,
therefore gives the same state X for B. Lemma H gives (ii): its proof uses only
round 1 and o[i] = Z[i] XOR Z[i + 8] for i = 0, 2, 5 and 7, and the chaining
value is (o[0], .., o[7]). (iii) As in the proof of Lemma T: C0 reads the same
words of X and w2, w6 in both compressions and has b output y by Lemma CT (b);
w15 = 0, Y14 is the same in both, the a input of E3 is Y3 for A and Y3' for B
by Fact P, and y is in the class, so the difference is eta by the definition of
the class (6.1). (iv) E1.c1 = c1 is Lemma CT (b). E1 has inputs (Y1, Y6, Y11,
Y12) and message words (w12, w5) for A, and (Y1, Y6, Y11', Y12) and (w12, w5 +
delta) for B. Its first and second values are the same for both, so its third
values are c1 and c1 + DY11, with DY11 = Y11' - Y11 = 0a08818b, and its fourth
values are ROR(Y6 XOR c1, 12) and ROR(Y6 XOR (c1 + DY11), 12). Their XOR is
ROR(c1 XOR (c1 + DY11), 12), which is beta* exactly when c1 XOR (c1 + DY11) =
ROL(beta*, 12) = 0e09818b. For words c and x, (c XOR x) - c = x - 2 (c AND x)
modulo 2^32, which is the identity of the proof of Lemma Q; with x = 0e09818b
this holds exactly when 2 (c1 AND 0e09818b) = 0e09818b - DY11 = 04010000. As
0e09818b has no bit 31 the doubling is exact, and it holds exactly when (c1 AND
0e09818b) = 02008000, that is when c1 is in Q*. The messages are distinct
because their lengths differ. QED.

*The counter is the free word.* In the root instance the second assignment of
K0 reads the counter 0, so K0.a1 = ROL(K0.d1,16) follows from the context, and
with it the message word w0. Here that assignment is solved for the counter
instead, which leaves K0.a1, and with it w0, free. The word w0 enters round 1
only in the fifth assignment of C2, and the lines for Y2, Y14, Y10, Y6, E1.a1
and E1.d1 of step CT map their running word one to one, so every value of
E1.d1, and so of c1, can be prescribed in one outer step. With the counter
fixed, no order of the assignments has both Y4 and E1.d1 among its free words,
and with the counter free no order has Y4, E1.d1 and E3.h1 all free: the
counter buys one prescribed word. These two statements are results of a
participant search over the orders, decided by an exact peeling test that was
checked against brute force; nothing below uses them.

**Lemma IP (the inner permutations and the member with t = 0; GPT Sol 6.1).**
Fix the seven outer words and y. (a) The maps c1 -> E3.h1 and c1 -> t given by
step CT are permutations of the 32-bit words. (b) So the 2^21 members of Q*
give 2^21 different values of E3.h1 and of t, and at most one member of Q* has
t = 0.

Proof. With the names of step CO fixed, the lines for E1.d1, E1.a1, Y6, Y10,
Y14 and E3.h1, with e1 = Y3 + y, each map their running word one to one. Read
backwards: Y14 = ROL(E3.h1,16) XOR e1, Y6 = ROR((Y14 + C2.c1) XOR C2.b1, 7),
E1.a1 = Y6 + Y1 + w12 and c1 = Y11 + ROR(E1.a1 XOR Y12, 16). For the counter,
Y2 = ROL(Y14,8) XOR C2.d1 = ROL(E3.h1,24) XOR ROL(e1,8) XOR C2.d1, and the
lines for w0, K0.a1 and t give t = ROL(K0.d1,16) XOR (Y2 + IV[0] + IV[4] -
C2.a1 - C2.b1), where K0.d1, C2.a1, C2.b1, C2.d1 and e1 are names of step CO.
That is a composition of permutations of E3.h1. Its only zero is at E3.h1 =
ROR((ROL(K0.d1,16) - IV[0] - IV[4] + C2.a1 + C2.b1) XOR ROL(e1,8) XOR C2.d1,
24), and the inverse above gives its one value of c1, which may or may not lie
in Q*. QED.

So an outer step has 2^21 or 2^21 - 1 valid trials. Lemma IP bounds the number
of trials that the rule t != 0 drops, one in 2^21 at most; it does not bound the
share of the collision mass that the dropped trial carries (10.3). In the
participant's checks the member with t = 0 was constructed by the inverse above
in 40 outer steps and rejected by the earlier program in 40 of 40; over 8,192
further outer steps it lay in Q* 4 times, against 4.0 expected, and was rejected
4 times out of 4.

*The length of the messages.* Within one outer step the 2^21 members of Q* give
2^21 different values of t below 2^32 (Lemma IP); over 2,000 trials of the
participant's check t ran from 891,836 to 4,291,586,422 with a mean of log2 t
of 30.56. A pair found by the search has messages of 1024 t + 55 and 1024 t +
63 bytes, shorter than 2^42 bytes and about 2^41 on average. A small t cannot
be chosen: it is the value of a permutation of c1 at the member that the search
finds.

**The outer filter.** Number the seven outcomes of beta* whose tau ends in
5020a0 (10.1) j = 1 to 7 in the order of the table of 10.1: 175020a0, 185020a0,
275020a0, 285020a0, 385020a0, 675020a0 and 685020a0, the seven of entry 26ebba63
and of the earlier program's `CTR_TAUS`. This search lists six of them, the set
S = {1, 2, 3, 4, 5, 7}: all but 675020a0 (j = 6). In the hexadecimal masks
below, with bit j - 1 for outcome j, S is 5f. Beta* has seven more outcomes on
the class, the same seven with bit 14 of tau set (j = 8 to 14 of 10.1); this
search does not list them either. Let tau_j be the tau of outcome j, sigma_j =
tau_j XOR ROR(tau_j, 1) and theta_j = ROL(sigma_j, 12); all seven have eps =
6e21be55. For an outer step put omega = Y3 + y + w8, with Y3 of Fact P, y the
member of the outer step and w8 the name of step CO; DY3 = Y3' - Y3 = fdb77cfd
is that of Section 6. For a word x:

- condition (1)_j holds for x when some word h gives
  (x + h) XOR (x + (h XOR eta)) = theta_j;
- condition (2)_j holds for x when some word f gives
  (x + f) XOR ((x + DY3) + (f XOR sigma_j)) = eps.

An outer step *passes* the filter when for some j in S both (1)_j holds for its Y9
and (2)_j holds for its omega. Y9 and w8 are names of step CO and y is drawn with
the outer words, so whether an outer step passes depends on the outer step alone
and on no c1.

**Lemma F (the outer filter; GPT Sol 6.1, answers AC and AN).** Fix an outer
step that does not pass the filter. Then no trial of the outer step, for any
word c1, has R = 0 with an E1 outcome in S. (A trial with R = 0 whose E1 outcome
is another outcome of beta* on the class may lie in a rejected outer step; the
search does not count it.)

Proof. Take a trial with R = 0 whose E1 outcome is outcome j. Write h, g, f and
e2 for E3.h1, E3.g1, E3.f1 and E3.e2 in the compression of A, and h', g', f' and
e2' for the same values in that of B. Y9 and w8 are the same in both
compressions: w8 is a line of step CO and a word of both blocks, and Y9 is an
output of C1, which reads words of the state X, the same for A and B (proof of
Theorem C), and the message words w3 and w10, which the two blocks share. Both
compressions have Y4 = y and h' = h XOR eta (Theorem C (iii)), and the a input
of E3 is Y3 for A and Y3' for B (Fact P). The conditions of R = 0 (Section 13,
how r is counted) give that the XOR difference of E3's first-half b values is
psi = tau_j XOR ROR(tau_j, 1) = sigma_j, and that of its a outputs is eps' =
eps. Now g = Y9 + h and g' = Y9 + (h XOR eta); f = ROR(y XOR g, 12) and f' =
ROR(y XOR g', 12), so f XOR f' = ROR(g XOR g', 12) = sigma_j gives g XOR g' =
theta_j, and h witnesses (1)_j for Y9. With w15 = 0, e2 = Y3 + y + f + w8 =
omega + f and e2' = Y3' + y + f' + w8 = (omega + DY3) + (f XOR sigma_j), and e2
XOR e2' = eps, so f witnesses (2)_j for omega. So the outer step passes, against
the hypothesis. QED.

The lemma uses no law of the words: no uniformity, no independence and no
relation between h and f besides the two equations. It does not use the rule t
!= 0, and it holds for any list of outcomes (GPT Sol, answer AN 2), S among them.
The filter can pass outer steps that hold no success, since (1)_j and (2)_j are
solved with separate witnesses; it cannot reject an outer step that holds a
success with an outcome of S.

**The exact share (GPT Sol, answers AC, AN and AW; recounted by the
participant).** Let pi be the share of the 2^64 pairs (x1, x2) of words such
that for some j in S condition (1)_j holds for x1 and (2)_j for x2. Then

    pi = 18,289,159,183,466,496 / 2^64 = 279,070,422,111 / 2^48,

about 0.00099145731 = 2^-9.978162. With all seven outcomes j = 1 to 7 in place
of S the share is 20,504,986,129,465,344 / 2^64 = 312,881,258,079 / 2^48 =
2^-9.813176, the share of the filter of entry 26ebba63 and the earlier program's
`CTR_SHARE`; this search does not use it. Let pi_E be the share of the 2^32
words x for which (2)_j holds for some j in S: pi_E = 233,715,456 / 2^32, about
0.054416120 = 2^-4.199822.

*Method.* Whether (1)_j holds for x is decided bit by bit from bit 0 upwards.
At bit i the XOR of the two sum bits prescribes the XOR of the two incoming
carries; the state is the set of incoming carry pairs that some choice of the
lower bits of the witness reaches with the lower bits of x, and the next state
is the set of carry pairs out of bit i that some witness bit gives from a pair
of the set that meets the prescription. The condition holds when the set is
still nonempty after bit 31, which has no outgoing carry to prescribe because
the arithmetic is modulo 2^32. For (2)_j the carry of x + DY3 is carried as
well. The seven sets for the seven outcomes are carried together over the same
bits of x, each with its own witness (a subset construction), so one pass over
the bits of x gives its *mask*, the set of j for which the condition holds;
equal states add their counts of prefixes of x, and witnesses are never
counted. A pair passes exactly when the mask of x1 under (1) and the mask of x2
under (2) intersect, so the number of passing pairs is the sum, over pairs of
intersecting masks a and b, of the number of words with mask a under (1) times
the number of words with mask b under (2).

*Certificate.* Masks are written in hexadecimal with bit j - 1 for outcome j
(bit 0 for 175020a0, bit 6 for 685020a0). The numbers of words with each
nonzero seven-bit mask m are 7,936 a_m under (1), a_m the second column, and
1,082,016 b_m under (2), b_m the fourth and the sixth columns:

| mask, (1) | words / 7,936 | mask, (2) | words / 1,082,016 | mask, (2) | words / 1,082,016 |
| --- | ---: | --- | ---: | --- | ---: |
| 01 | 266 | 01 | 10 | 36 | 30 |
| 02 | 2,044 | 02 | 18 | 41 | 10 |
| 04 | 1,778 | 03 | 5 | 43 | 1 |
| 08 | 254 | 09 | 10 | 49 | 10 |
| 10 | 2,032 | 12 | 22 | 53 | 1 |
| 12 | 2,044 | 13 | 5 | 5b | 2 |
| 18 | 1,524 | 16 | 30 | 62 | 1 |
| 20 | 2,016 | 1b | 2 | 63 | 4 |
| 21 | 1,512 | 1e | 2 | 72 | 1 |
| 40 | 504 | 1f | 8 | 73 | 4 |
| 42 | 1,512 | 22 | 15 | 7e | 2 |
| 52 | 1,512 | 32 | 15 | 7f | 8 |

No other nonzero seven-bit mask occurs; 134,896,128 words satisfy some (1)_j and
233,715,456 some (2)_j. Every mask of (2) in the table meets 5f, so the same
233,715,456 words satisfy (2)_j for some j in S. The sum of a_m b_n over the
pairs of masks m and n with m AND n AND 5f not zero is 2,129,896, and over all
pairs of intersecting masks it is 2,387,944. So the number of pairs that pass
for S is 7,936 * 1,082,016 * 2,129,896 = 18,289,159,183,466,496, and for all
seven 7,936 * 1,082,016 * 2,387,944 = 20,504,986,129,465,344 (the participant's
arithmetic on the table; GPT Sol's answer AW 3 gives the same 279,070,422,111
and 233,715,456). With the seven other outcomes of beta* on the class added, GPT
Sol's certificate of the fourteen-outcome filter (answer AN 2) gives
99,669,577,442,459,648 passing pairs, 2^-7.531997; that filter is not used here.

*The automata.* The earlier program's `ctr_automaton` builds the subset
construction above as four byte tables: a state is the carry of x + DY3 (zero
for (1)) and, per outcome, the set of reachable carry pairs, four bits; the
table of byte p maps a state and byte p of x to the next state, and the table of
the last byte maps to the mask. `ctr_tables` builds the two automata once per
run from `CTR_TAUS` and `CTR_EPS`, which in that program hold the seven outcomes
of entry 26ebba63. The search of this package builds the same two automata (step
0 of 9.1) and ANDs every entry of their last tables with 5f once, so that every
mask it reads is restricted to S; the states and the number of table loads do
not change. Its construction has 1, 18, 43, 37 and 1, 3, 7, 7 states at the four
byte boundaries and tables of 25,344 and 4,608 entries (a participant run of its
own functions). `ctr_look` runs an automaton on a word with one table load per
byte, and `ctr_filter` returns the AND of the mask of Y9 under (1) and the mask
of omega under (2); its outer step passes when it is not zero. Its count of
passing pairs from its own tables is `CTR_SHARE` = 20,504,986,129,465,344, for
the seven outcomes, which its self-test recounted, and it checked those automata
against brute force. The program of 6.4 builds the same two automata restricted
to S and checks them against brute force at 8 bits.

## 9. The counter search

**9.1 The algorithm.** The search uses these constants. FACTOR = floor(10 *
138,512,695,296 / 11) = 125,920,632,087 is the factor of H1' (10.3): ten
elevenths, rounded down, of the count in 10.1 of the six outcomes of S.
RUN_STEPS_MIN = ceil(0.49676 * 2^128 / (FACTOR * (2^21 - 1))) =
640,117,155,200,996,249,977 is the least number of outer steps that yields
0.49676 = 12419 / 25000 expected listed good trials at the rate of H1' (10.4).
RUN_CONTEXTS = ceil(RUN_STEPS_MIN / 2^19) = 1,220,926,580,812,448, about
2^50.117, counts the contexts of a run (9.8), and RUN_STEPS = 2^19 *
RUN_CONTEXTS = 640,117,155,200,996,737,024, about 2^69.117, its outer steps,
487,047 more than RUN_STEPS_MIN. A context has 16,384 clusters of 32 members in
2,341 = ceil(16,384 / 7) representative batches (9.9), so a run has 2,341 *
RUN_CONTEXTS representative batches, about 2^61.310. Every count with a budget
is a sum over the independent contexts, and its budget is an upper bound on its
mean plus a reserve of s times its range in one context, s = ceil(sqrt(10 *
RUN_CONTEXTS)) = 110,495,547, so that Hoeffding's inequality bounds its overflow
by exp(-20) (GPT Sol, answers CJ 1.2 and CK 2 and 9). The opened clusters have
the budget A_BUDGET = ceil(246,621,675 * RUN_CONTEXTS / 2^15) + 16,384 * s =
9,189,056,937,678,035,781, about 2^62.995, on the mean bound of Lemma OR (9.9).
SHARE = 18,289,159,183,466,496 is the number of pairs that pass the filter for S
(Section 8), whose share pi is therefore SHARE / 2^64, and E_COUNT = 233,715,456
the number of words that pass the automaton of (2) for S (Section 8). The two
count budgets rest on the means that H4' declares, alpha_E = 1.000026 and
alpha_P = 1.000176 times the nominal shares (10.3):

    E_BUDGET    = 34,833,655,546,458,722,911   (about 2^64.918)
                = ceil(1.000026 * RUN_STEPS * E_COUNT / 2^32) + 2^19 * s,
    PASS_BUDGET = 634,818,459,892,147,173      (about 2^59.140)
                = ceil(1.000176 * RUN_STEPS * SHARE / 2^64) + 2^19 * s.

Further, the table CT of 9.7 holds, for every subset T of S, the proved cap
C15(T) (Section 11) of steps 2 and 3 with the guards (G7) and (G15) and the
certificate of step 3 on the outcomes of T, and C15(T) = 0 when T is empty. CBAR
= 582,173,006,981,436 defines cbar = CBAR / 2^47 = 4.13658801066..., the mean
over all outer steps, in the counting model of H5', of C(T), the larger cap with
(G7) alone of 9.7 (10.3). Since C15(T) <= 16/27 C(T) for every T that occurs
(Section 11), the debits of a run have a mean of at most m_C under H5' (1.01
times cbar), and the credit adds a reserve for L_C = 17,504 * 2^19 =
9,177,137,152, the most that the debits of one context can total (GPT Sol,
answers AW 5, CD 11 and CK 2):

    m_C         = 1,584,817,753,552,722,787,165
                = ceil(101 * 16 * RUN_STEPS * CBAR / (100 * 27 * 2^47)),
    CREDIT      = 1,584,841,873,457,225,944,219   (about 2^70.425)
                = m_C + ceil(sqrt(40 * L_C * m_C)) + 14 * L_C.

0. Once, before the first context: the two automata of the outer filter for the
   seven outcomes are built, with the entries of their last tables ANDed with S
   (Section 8), and the direct tables T2 and T1 are filled from them with the
   masks of (2) and of (1), restricted to S, of every 32-bit word (Lemma DT);
   the member lists in cluster order and the gate table P are written (9.9); so
   are the table VMASK of the pre-check and the table CT of the credit (9.7),
   the credit counter, which starts at CREDIT, and the three transition arrays,
   the static row descriptors of the six outcomes of S and the statically
   written traversal of the joint solver with the guards (G7) and (G15) (9.4,
   9.7, Section 11). Nothing built here depends on an outer word.
1. Walk the contexts one after another, RUN_CONTEXTS of them. A context takes
   one fresh uniform 256-bit word: its 32-bit words 0 to 6 are the outer words
   C0.d1, D2.a1, D2.b1, S11, S4, X9 and w6, and word 7 is unused. The 39
   context lines of step CO (Lemma Y) run once, and the words of the context
   are prepared (9.8). The context then runs its 2,341 representative batches
   one after another; lane i of representative batch b carries the
   representative of cluster 7 b + i. *Gate (9.9):* the omega side of a
   representative batch also gives the key of every lane, and each used lane
   reads the gate table P at its key. On 0 the whole cluster of the lane is
   skipped, the representative included (Lemma CL). Otherwise the opened count
   is incremented, and the run halts with failure if it now exceeds A_BUDGET;
   then the representative and the 31 partners of the cluster, in five partner
   batches, are walked as below, before the gate test of the next lane. The
   outer step of a lane is the context together with the member of the lane.
   *Test (2):* the 8 member-dependent lines of step CO on which omega depends,
   and omega = Y3 + y + w8, are computed for all lanes at once on packed words;
   each used lane of a partner batch, lane 0 first, and the representative of
   an opened cluster then read from T2 the mask of (2) of their omega,
   restricted to S (9.8, 9.9). When that mask is zero the outer step of the
   lane is finished. *Q path:* a lane with a nonzero mask of (2) first
   increments the count of such lanes, the *E count*, held in a register (9.8),
   and the run halts with failure if it now exceeds E_BUDGET. Otherwise the 17
   member-dependent lines on which only Y9 depends are computed on packed
   words, two of them in one line (9.8), the Y9 of the lane is taken out, its
   mask of (1), restricted to S, is read from T1, and the AND of the two masks
   is the mask X of the outer step. When X is zero the outer step is finished.
   Otherwise the outer step *passes* (Section 8): the count of passing outer
   steps is incremented, and the run halts with failure if it now exceeds
   PASS_BUDGET; otherwise the names of step CO that steps 2 and 3 read are
   rebuilt on scalar words from the seven outer words of the context and the
   member of the lane. *Pre-check:* compute the word nu of 9.7 from Y9, y,
   C2.c1 and C2.b1 and T = X AND VMASK[nu]. If T is zero the outer step ends
   there (it holds no listed good trial, Lemma VP). Otherwise read C15(T) from
   the table CT; halt with failure when it exceeds the remaining credit, and
   else subtract it from the credit and run steps 2 and 3 for this outer step.
2. *Roots:* run the joint solver of 9.4 with the guards (G7) and (G15) of 9.7 on
   Y9, y and omega for every outcome j whose bit is set in T. It returns the
   joint roots of these outcomes that satisfy (G7) and (G15), each a word h with
   the outcome of which it is a root, at most 16 per outer step (9.4).
3. *Certificate (Lemma RC, 10.2; GPT Sol, answer CF 6):* for each returned root
   h, with its outcome j, in turn, at its leaf: compute from h, with the names
   of step CO and all sums modulo 2^32, the lines of step CT backwards (Lemma
   IP), Y14 = ROL(h,16) XOR (Y3 + y), Z = (Y14 + C2.c1) XOR C2.b1, Y6 = ROR(Z,
   7), E1.a1 = Y6 + Y1 + w12, E1.d1 = ROR(E1.a1 XOR Y12, 16), c1 = Y11 + E1.d1,
   E1.b1 = ROR(Y6 XOR c1, 12) and E1.a2 = E1.a1 + E1.b1 + w5, and t by the
   lines Y2, w0, K0.a1 and t of step CT; put s = E1.b1 AND beta*, p = ((tau_j -
   beta* + 8 + 2 s) mod 2^32) >> 1 and z = ROR(E1.d1 XOR E1.a2, 8). The root is
   *certified* when

       (Q)  c1 AND 0e09818b = 02008000,
       (A)  E1.a2 AND tau_j = p,
       (C)  (c1 + z) XOR ((c1 + DY11) + (z XOR ROR(tau_j, 8))) = eps,
       (T)  t != 0,

   with DY11 = Y11' - Y11 = 0a08818b and eps = 6e21be55. For the first certified
   root, form F || A and F || B by steps CT and CS for its c1, evaluate blake3
   of both in full, check that the two digests agree, output the pair and halt.
4. If no pair has been output when the last context ends, halt with failure.

There are exactly five ways for the run to halt with failure, each a test on a
count kept by the algorithm: the opened count exceeds A_BUDGET, the E count
exceeds E_BUDGET, the count of passing outer steps exceeds PASS_BUDGET, the cap
C15(T) of an outer step that reaches the solver exceeds the remaining credit, or
the contexts run out. Hence at most A_BUDGET clusters are opened, at most
E_BUDGET lanes run the Q path, at most PASS_BUDGET passing outer steps are
rebuilt and pre-checked, and the caps C15(T) of the outer steps that run steps 2
and 3 add up to at most CREDIT. Steps 2 and 3 need no budget of their own, since
the joint solver returns at most 16 roots and, whatever the words of an outer
step, their work in it is at most its C15(T) (9.4, 9.7, Section 11). The work of
every run is therefore bounded by the counts of Section 11, and a pair of
messages is formed and hashed at most once, for a certified root.

A trial is *valid* when its t is not zero; a valid trial with R = 0 is *good*; a
good trial is *listed* when its E1 outcome is in S (Section 8, 10.1). A listed
good trial is found unless the run ends before its outer step is reached, by one
of the three budgets, by the credit or by the output of another pair: its outer
step passes the filter by Lemma F, its cluster is opened by Lemma CL, its lane
is taken as passing by Lemmas MB and DT, the pre-check keeps its outcome by
Lemma VP, the joint solver returns its E3.h1 as a root of its outcome by Lemmas
G7, G15 and CV, and step 3 certifies it (Lemmas RC and CV, 10.2). Every
certified root is the E3.h1 of a listed good trial (Lemma CV). A good trial that
is not listed is not found, and Section 10 does not count it; by the count of
10.1 beta* has eight more outcomes on the class, 675020a0 and the seven with bit
14 of tau set, which carry 4,065,280 of its 71,698,432 (5.7 per cent) and are
not listed. When the run outputs a pair, the pair is a collision of two complete
messages: the certified trial has R = 0 (Lemma V, 10.2), step 3 has checked both
digests, and Lemma TR (c) says that R = 0 with the half-collision of Theorem C
gives equal digests.

*What the submitted program holds.* The program of the declared experiment,
experiments/frontline.py (6.4), holds this search in the layout of 9.8 and 9.9:
steps CO and CT, the two automata restricted to S, the walk by clusters with the
gate, test (2), the Q path, the passing lane with the pre-check and the credit
test, the joint solver of 9.4 with (G7) and (G15), step 3 and the five halts,
and it adds the charges of Section 11 per event. An organizer trial walks one
context under a member budget (6.4). The halt constants of the program are those
of this search at the rate factor 5/7 with the margins 17/16 and 1.06 (its
RUN_CONTEXTS, A_BUDGET, E_BUDGET, PASS_BUDGET and CREDIT_G), each larger than
the constant above; a trial starts every count at zero and reaches none of them
(Section 13), so on the members it walks it takes the decisions of this search.
The budgets and the credit of this section bound the claimed run; the program's
halts are exercised only by its self-test.

**9.2 Seven trials in one word.** The earlier program (6.4) also held the
counter batch of entry e7b17fd1 (`ctr_batch`), which runs on the machine of 6.5
over packed words of seven members of Q* of a passing outer step and computes
for each lane rule A and the word n of Lemma N, so that R = 0 implies n = 0
(Lemma CB of that entry). The search of this package does not run it: in a
passing outer step the joint solver of 9.4 takes the place of that enumeration,
and the walk is that of 9.8. Its count of this batch, 41 units for stage A and
72 for stage 2 on 16 registers (`CTR_TABLE`), is not part of the charge of
Section 11.

**9.3 The counter part of the self-test.** The self-test of the earlier program
also ran N cases of the counter batch (`ctr_selftest`), each one outer step, one
table word and the counted batch, and checked every lane against its trial: it
built the two last-chunk blocks by steps CO, CT and CS and compressed each in
full with counter t and flags 3, and a lane was right when its words, its rule-A
flag and its word n agreed with that compression. With N = 2,000 and seed 1 it
reported 14,000 of 14,000 lanes right and 2,000 of 2,000 cases with right end
tests. Its compression with counter t and flags 3 was compared with the
organizer's `_compress` on 2,000 trials (Section 7). The program of this package
checks the counter instance in its own run (6.4).

*The filter part of the self-test.* The same self-test also checked the filter
of the earlier program (`ctr_filter_selftest`): (a) the automata built for words
of 10 bits, with real and random targets, against brute force over all 1,024
witnesses in 64 cases; (b) the count of passing pairs from the program's own
tables of 32 bits against CTR_SHARE; (c) 2^16 real outer steps walked by
`ctr_run`, with a second walk at pass budget 2 that must halt at the third
passing outer step; and (d) the counted outer step and filter (`ctr_count`)
against the plain ones. With seed 1 it reported 128 of 128 masks right, the
count of passing pairs equal to CTR_SHARE (2^-9.8132), 74 of the 65,536 real
outer steps passing (2^-9.791, z = +0.14 against pi), the halt right and 8 of 8
counted outer steps right.

**9.4 The joint solver (GPT Sol, answers AE, AF, AI, AL, AO and AR).** Fix a
passing outer step and write Q = Y9, y for its member, E = omega = Y3 + y + w8
and E' = E + DY3; x[i] is bit i of a word x, bit 0 the lowest, and maj is the
majority of three bits. Put e1 = Y3 + y and b = e1[2], u = e1[21] and v =
e1[26], three bits that are free in the class (in the sub-class of entry
26ebba63, u = v = 0). For an outcome j of beta* (10.1) put sigma = sigma_j and
theta = theta_j (Section 8), eps = 6e21be55, gamma = eta XOR theta, D = (sigma
XOR eps) AND 7fffffff, kappa = sigma XOR eps XOR E XOR E' and mu = ROR(eta XOR
eps, 8) = 9aed22bd. For a word h put g = Q + h, f = ROR(y XOR g, 12), e2 = E +
f and h2 = ROR(h XOR e2, 8): for E3.h1 = h these are E3.g1, E3.f1 and E3.e2 of
step CT and the d output of E3 on message A (6.2). The *static descriptor* of
outcome j holds sigma, theta, gamma, D and the positions of its constants and
guards; the static descriptors of the six outcomes of S depend on no outer word
and are formed once per run.

*Joint roots.* A word h is a *joint root* of outcome j when

    (J1)  (Q + h) XOR (Q + (h XOR eta)) = theta,
    (J2)  (E + f) XOR (E' + (f XOR sigma)) = eps,
    (J3)  (g + h2) XOR ((g XOR theta) + (h2 XOR mu)) = tau_j.

(J1) and (J2) are the conditions (1)_j and (2)_j of Section 8, with the two
witnesses tied by f = ROR(y XOR (Q + h), 12). By (J1) theta is a function of h,
and then so is the left side of (J3); the seven values of tau are different,
so no word is a joint root of two outcomes. There is no rule A: a joint root is
any word that satisfies (J1) to (J3).

*Carries.* Write u[i] and u'[i] for the carries into bit i of Q + h and of Q +
(h XOR eta), and a[k] and a'[k] for those into bit k of E + f and of E' + (f
XOR sigma), all 0 into bit 0. Bit by bit, (J1) holds exactly when u'[i] = u[i]
XOR gamma[i] for every i, and (J2) exactly when a'[k] = a[k] XOR kappa[k] for
every k. Bit i of h gives g[i] = Q[i] XOR h[i] XOR u[i] and bit k = (i + 20)
mod 32 of f, f[k] = y[i] XOR g[i]. So the solver chooses h from bit 0 to bit 31
and runs both pairs of additions along it: those of (J1) on bits 0 to 31, and
those of (J2) on bits 20 to 31 and then 0 to 19. The carry a[20] is not known
at the start; it is guessed for the constants of (a) below, and the check of
(J2) as a word at each leaf enforces that bits 0 to 19 give the right carry
into bit 20 (one traversal, below). At a bit k < 31 with D[k] = 1, the
*prescription* of f[k] is f[k] = E[k] XOR sigma[k] XOR kappa[k+1] if a[k] =
E[k], and f[k] = E'[k] XOR kappa[k+1] otherwise: from carries a[k] and a[k] XOR
kappa[k], it is the only value of f[k] that gives the carries into bit k + 1
the difference kappa[k+1] (Lemma S5).

*The phase equations (GPT Sol, answer AO 5 and 6.1).* The participant's
counter, run on the class with its E3 count split by the pattern of h on the
sixteen bits 0 to 3, 6 to 13, 16, 17, 24 and 25 and by (b, u, v), records for
each of the eight values of (b, u, v) every pattern that occurs in a solution
of E3 with an outcome of beta* (records of the participant, not in the
package). GPT Sol checked every recorded pattern against

    h[0] = 0,  h[1] = 1,  h[2] = 1 XOR b,  h[10] = b,  h[16] = h[17] = 0,
    h[11] = 1 XOR h[3],  h[24] = h[3] XOR h[12] XOR u                   (PHASE)

and found no violation in any of the eight cells, whose sets have 88, 88, 108,
132, 108, 132, 88 and 88 patterns in the order b + 2u + 4v. Each of the fourteen
outcomes of beta* on the class has an E1 count L_j > 0 that depends neither on y
nor on h, so a zero count outside (PHASE) means that no joint root of any of
them, the six of S among them, violates (PHASE). The equations are
consequences of the count, which the solver uses as guards; they are not a rule
that drops members or solutions.

*The parity certificate (GPT Sol, answer AR 1).* Call the outcomes j = 1 to 7,
whose tau ends in 20a0, the *old rows*, and j = 8 to 14, whose tau ends in 60a0
and has bit 14 set, the *new rows*; a row is also named by the first three
hexadecimal digits of its tau. Every joint root h of outcome j, for y in the
class, satisfies

    h[6] XOR h[13] XOR h[25] = u XOR tau_j[14],                        (P*)

that is h[6] XOR h[13] XOR h[25] = u on the old rows and u XOR 1 on the new
rows. This search lists only the old rows, on which (P*) reads h[6] XOR h[13]
XOR h[25] = u; the certificate is stated for all fourteen rows as it was
proved. The proof is an exact finite count. The count N3_j of 10.1 counts the
quadruples (Y4, E3.h1, Y9, w8), Y4 in the class, that meet the E3 conditions of
outcome j, and by the proof of Lemma V (10.2) these are exactly the quadruples
whose E3.h1 is a joint root of outcome j for Q = Y9, y = Y4 and E = Y3 + Y4 +
w8. GPT Sol split every N3_j by the phase (b, u, v) of Y4 and by the parity pi
= h[6] XOR h[13] XOR h[25] of the root. The split is a sum of nonnegative
integers over an exact enumeration of submasks, through the identity (z XOR
m) - z = m - 2 (z AND m) modulo 2^32 and a carry recurrence with two states in
integers, in coordinates of E3 that are a bijection of the counted quadruples;
nothing is sampled. With a = 24, 16, 4, 24, 32, 1 and 6 for the rows 175, 185,
275, 285, 385, 675 and 685:

| rows | phases (b, u, v) with a nonzero count | count in each such phase | pi | count with the other pi |
| --- | --- | ---: | --- | ---: |
| old, all seven | all eight | a * 2^49 | u | 0 |
| new 185, 285, 385, 685 | u XOR v = 1 | a * 2^47 | u XOR 1 | 0 |
| new 175, 275, 675 | u XOR v = 1 and b = 1 | a * 2^47 | u XOR 1 | 0 |

Every other cell has count 0. Every joint root adds at least 1 to the cell of
its phase and its parity, so a cell of count 0 holds no root at all: (P*) holds
for every joint root of the fourteen outcomes on the whole class, pointwise and
not on average, and it drops no member and no root. The cells add up to the
fourteen N3_j of 10.1 exactly: 8 * a * 2^49 = a * 2^52 on the old rows, 4 * a *
2^47 on the new rows 185, 285, 385 and 685, and 2 * a * 2^47 on the new rows
175, 275 and 675 (checked by a helper agent of the participant). In the phase b
= 1, u = 0, v = 1, the 2^16 members of the class with e1 AND 07ef8307 =
070c0307, a separate exact count of a helper agent of the participant, with the
function N3_count of the counting program of Section 17 and the parity as one
more condition, gives all fourteen counts with pi = 0 on the old rows, pi = 1
on the new rows and the count 0 with the other pi, as the table says. The cells
of the other seven phases are GPT Sol's evaluation and were not re-run by the
participant. The count shows as well that a new row has no joint root when u =
v, and a new row 175, 275 or 675 none when b = 0; the search of this package
lists no new row.

*The guard on the third addition (GPT Sol, answer AR 6.1).*

**Lemma J0.** Every joint root h of every one of the seven outcomes has
h2[0] = 0, that is h[8] = e2[8].

Proof. For all seven outcomes tau_j[0] = tau_j[1] = 0, theta_j[0] =
theta_j[1] = 1 and gamma[1] = gamma[2] = 0, and mu[0] = 1, mu[1] = 0. By
(PHASE) h[0] = 0 and h[1] = 1. In (J1) both carries into bit 0 are 0. Since
eta[0] = eta[1] = 1 and gamma[1] = 0, the carry Q[0] AND (h[0] XOR 1) = Q[0] of
the second addition into bit 1 must equal the carry Q[0] AND h[0] = 0 of the
first, so Q[0] = 0 and g[0] = 0; since gamma[2] = 0, the carry maj(Q[1], 0, 0)
= 0 of the second addition into bit 2 must equal the carry maj(Q[1], 1, 0) =
Q[1] of the first, so Q[1] = 0 and g[1] = 1. Both additions of (J3) have carry
0 into bit 0. At bit 0, g + h2 adds 0 and h2[0], with sum bit h2[0] and carry 0
out; (g XOR theta) + (h2 XOR mu) adds 1 and h2[0] XOR 1, with sum bit h2[0] and
carry 1 XOR h2[0] out. At bit 1, g + h2 adds 1, h2[1] and 0, with sum bit 1 XOR
h2[1]; the other adds g[1] XOR theta[1] = 0, h2[1] XOR mu[1] = h2[1] and 1 XOR
h2[0], with sum bit h2[1] XOR 1 XOR h2[0]. (J3) at bit 1 requires the XOR of
the two sum bits, which is h2[0], to be tau_j[1] = 0. So h2[0] = 0, and h2[0]
is bit 8 of h XOR e2. QED. The zero carries into bit 0 are those of addition
modulo 2^32; nothing is guessed. The participant checked the bits that the
proof reads for all fourteen outcomes of beta* on the class, the six of S among
them.

e2[8] is produced at position i = 20 of the traversal (k = 8): e2[8] = E[8] XOR
f[8] XOR a[8] with f[8] = y[20] XOR Q[20] XOR h[20] XOR u[20], and every term
but h[20] is known when position 20 is reached, h[8] among them. So Lemma J0 is
a forward guard that sets h[20] = h[8] XOR E[8] XOR a[8] XOR y[20] XOR Q[20]
XOR u[20]. It holds for every joint root, so no root is lost, and position 20,
which no constant and no carry prescribes on any row, is no longer free.

*The constants and guards of an outcome.* For y in the class, every joint root
of outcome j has the following values, which the solver computes from Q, y, E
and the outcome before it branches, or checks during the traversal (GPT Sol,
answers AE 2.1, AF 1.2, AN 6, AO 6.1 and AR 2 and 6.1). Every member of the
class has y[0] = 0, y[1] = 1 and bits 16 to 19 of y equal to 0, 0, 1, 0, so
f[20] = f[21] = 0, bits 4 to 7 of f are the constant 2, the carry u[20] is
Q[19], and the first addition is reset as in the sub-class.

(a) *The carry into bit 22.* For each guess a[20] = 0 and a[20] = 1, with
a'[20] = a[20] XOR kappa[20], run bits 20 and 21 of both additions of (J2) with
f[20] = f[21] = 0, and keep the guess only if a'[21] = a[21] XOR kappa[21] and
a'[22] = a[22] XOR kappa[22]. If no guess is kept, the outcome has no joint
root. Two kept guesses have the same carries into bit 21, and so into bit 22:
all seven outcomes have sigma[20] = sigma[21] = 1, eps[20] = 0 and eps[21] = 1,
and the cases E[20] = E'[20], E[20] = 0 with E'[20] = 1, and E[20] = 1 with
E'[20] = 0 give, in turn, at most one guess that passes bit 21, equal carries
into bit 21 for both guesses, and at most one guess that passes bit 22. Write
a[22] for the common carry.

(b) f[22] is its prescription (D[22] = 1). If gamma[3] = 0, then D[23] = 1 and
f[23] is its prescription; if gamma[3] = 1, f[23] = 1 XOR Q[3] XOR y[3]. Run
bits 22 and 23 of (J2); if a'[23] is not a[23] XOR kappa[23] or a'[24] is not
a[24] XOR kappa[24], the outcome has no joint root. This gives a[24].

(c) h[0] = 0, h[1] = 1 and u[2] = 0; h[2] = y[2] XOR f[22] XOR Q[2], and the
outcome has no joint root unless h[2] = 1 XOR b; u[3] = maj(h[2], Q[2], 0);
h[3] = y[3] XOR f[23] XOR Q[3] XOR u[3] and u[4] = maj(h[3], Q[3], u[3]); h[10]
= b and h[11] = 1 XOR h[3]; u[11] = maj(h[10], Q[10], Q[9]) if gamma[10] = 0
and u[11] = Q[10] if gamma[10] = 1; u[12] = maj(h[11], Q[11], u[11]).

(d) f[0] is its prescription with a[0] = 0 (D[0] = 1), and a[1] = maj(E[0],
f[0], 0); h[12] = y[12] XOR f[0] XOR Q[12] XOR u[12], u[13] = maj(h[12], Q[12],
u[12]) and h[24] = h[3] XOR h[12] XOR u.

(e) Bit 16 of h2 is 0, so f[24] = h[24] XOR E[24] XOR a[24]; h[4] = y[4] XOR
f[24] XOR Q[4] XOR u[4] and u[5] = maj(h[4], Q[4], u[4]). Run bit 24 of (J2);
if a'[25] is not a[25] XOR kappa[25], the outcome has no joint root. f[25] is
its prescription (D[25] = 1), a[26] = maj(E[25], f[25], a[25]) and h[5] = y[5]
XOR f[25] XOR Q[5] XOR u[5].

(f) Bits 6, 13, 25 and 26 depend on the kind of the outcome; (P*) is used on
every row. The outcomes of S are old rows of two kinds (675020a0, an old row that
this search does not list, is described with them).

- *Low old rows, 175020a0, 275020a0 and 675020a0:* if E[1] = a[1], the carry
  into bit 2 is E[1], f[2] is its prescription (D[2] = 1) and e2[2] = E[2] XOR
  f[2] XOR E[1]; otherwise the outcome has no joint root if kappa[2] = 1, and
  e2[2] = E[2] XOR kappa[3] if kappa[2] = 0. Then h[26] = 1 XOR h[2] XOR e2[2]
  XOR Q[26] XOR Q[25], f[26] = h[26] XOR E[26] XOR a[26] and h[6] = f[26] XOR
  y[6] XOR gamma[7]. By (P*), h[25] = h[6] XOR h[13] XOR u: a forward guard,
  set once bit 13 of h is chosen.
- *High old rows, 185020a0, 285020a0, 385020a0 and 685020a0:* h[25] = e2[1]
  (answer AE 2.1), where e2[1] = E[1] XOR f[1] XOR a[1] and f[1] = y[13] XOR
  Q[13] XOR h[13] XOR u[13]. With (P*), h[6] = h[13] XOR h[25] XOR u = y[13]
  XOR Q[13] XOR u[13] XOR E[1] XOR a[1] XOR u, in which h[13] cancels: h[6] is
  fixed by (c) and (d), which give u[13] and a[1]. The guard of position 25 is
  then h[25] = h[6] XOR h[13] XOR u, the same as h[25] = e2[1]. h[26] = e2[26]
  (bit 18 of h2 is 0), and e2[26] is given by position 6, whose value is now
  fixed, so h[26] is a constant of the row.

(g) h[16] = h[17] = 0, h[18] = 1 XOR Q[18], h[19] = Q[19], and, if gamma[7] =
1, h[7] = 1 XOR gamma[8] XOR h[6], now a constant on every row.

On every row h[29] = 1 XOR e2[29] (bit 21 of h2 is 1), where e2[29] is known
once bit 9 of h is chosen, and h[20] is set by Lemma J0. These are the
*constants and guards* of the outcome. On every row h[0] to h[6] are fixed
before the traversal; the guards that read bits chosen during the traversal are
those of position 20 (every row), position 25 (the old rows) and position 29
(every row). In entry 26ebba63 the parity h[25] = h[6] XOR h[13] was a
condition of rule A on the sub-class; here (P*) is not a rule but a consequence
of the count of the class, true of every joint root.

*One traversal.* Every carry guess a[20] that (a) keeps reaches, after the
constants h[0] to h[6], the same state: the same bits h[0] to h[6], the same
carries u[7] and a[27], and the same e2[26]; the values e2[20] and e2[21],
which depend on the guess, are not used by any guard. So the solver walks bits
0 to 6 under both kept guesses with the tests of (a), (b) and (e), then drops
the guesses and starts one depth-first traversal for each searched outcome at
depth 7 from that state, and checks (J1), (J2) and (J3) as words at each leaf,
which enforces the closure of the carries that the guess stood for (GPT Sol,
answers AO 2 and 6.1 and AR 2). Every joint root survives a guess and reaches
this common state, and a single traversal over the bits of h reaches every h at
most once.

*Transitions.* For each position i = 7, .., 31, with k = (i + 20) mod 32, each
pair (u[i], a[k]) of incoming carries and each value v of h[i], put g[i] = Q[i]
XOR v XOR u[i], u[i+1] = maj(Q[i], v, u[i]) and u'[i+1] = maj(Q[i], v XOR
eta[i], u[i] XOR gamma[i]), and require u'[i+1] = u[i+1] XOR gamma[i+1] if i <
31; put f[k] = y[i] XOR g[i], e2[k] = E[k] XOR f[k] XOR a[k], a[k+1] =
maj(E[k], f[k], a[k]) and a'[k+1] = maj(E'[k], f[k] XOR sigma[k], a[k] XOR
kappa[k]), and require a'[k+1] = a[k+1] XOR kappa[k+1] if k < 31. A value that
passes is an arc to the pair (u[i+1], a[k+1]), or to (u[i+1], 0) if k = 31,
since both carries into bit 0 of (J2) are 0 (kappa[0] = 0: E'[0] differs from
E[0], eps[0] = 1 and sigma[0] = 0 for all seven outcomes); the arc records v
and e2[k]. The *descriptor* of a position is 14 bits: Q[i], y[i], E[k], E'[k],
eta[i], gamma[i], sigma[k], kappa[k], gamma[i+1], kappa[k+1], whether the
position has a constant and its value, and whether i = 31 and k = 31 (GPT Sol,
answer AI 1). The solver reads the arcs from three arrays built once per run
(answer AR 6.2), each entry computed by the relation above, which is the same
relation and not an approximation; an arc is five bits, the next carry pair,
h[i], e2[k] and a validity bit:

| array | key | words | entry |
| --- | --- | ---: | --- |
| forced | descriptor and carry pair | 2^16 | the one passing arc, or invalid |
| dual | descriptor and carry pair | 2^16 | both arcs, packed in one word |
| selected | descriptor, carry pair and a desired bit | 2^17 | the passing arc whose e2[k] is the desired bit, or invalid |

A position with a constant reads the forced array with the constant in its
descriptor. A position i < 31 with gamma[i] = 1, or with k < 31 and D[k] = 1,
has at most one passing value by Lemma S5 and reads the forced array as well. A
position with a guard on bits chosen during the traversal, 25 on the old rows
and 29 on every row, reads the forced array with the value of the guard written
into the constant field of its key: 1 XOR e2[29], from the saved bit e2[29],
and h[6] XOR h[13] XOR u, from bit 13 of the prefix of h. Position 20 reads the
selected array with the desired bit h[8] (Lemma J0); as e2[8] changes with
h[20], at most one arc has it. A free position (below) reads the dual array. So
a position that is not free has at most one child.

*The search.* From the common state at depth 7, search depth first over the
positions 7 to 31: a node at depth d has a child at depth d + 1 for each arc of
position d from its carry pair that meets the guards of the position. A node at
depth 32 is a *leaf*; it gives a root when its h satisfies (J1), (J2) and (J3)
as words. The root is returned with the outcome j.

*Counts.* Call a position i >= 7 *free* when it has no constant and no guard,
gamma[i] = 0 or i = 31, and D[(i + 20) mod 32] = 0, and *prescribed* otherwise.
For a row with the set F of free positions put n_i = 2^(the number of free
positions p with 7 <= p < i), for i = 7, .., 32. A traversal of the row has at
most n_i nodes at depth i: at most the sum of n_i over the prescribed positions
*forced* nodes, the sum over the free positions *free* nodes, n_20 *selected*
nodes among the forced ones (position 20 is prescribed on every row, by Lemma
J0), and n_32 = 2^|F| leaves (GPT Sol, answer AR 6.5; recomputed by the
participant from the free positions):

| tau | free positions | forced nodes | free nodes | selected nodes | leaves |
| --- | --- | ---: | ---: | ---: | ---: |
| 175020a0 | 7, 13, 15, 30 | 142 | 15 | 8 | 16 |
| 185020a0 | 13, 15, 30 | 72 | 7 | 4 | 8 |
| 275020a0 | 9, 13, 15, 30 | 140 | 15 | 8 | 16 |
| 285020a0 | 7, 9, 13, 15, 30 | 278 | 31 | 16 | 32 |
| 385020a0 | 9, 13, 15, 30 | 140 | 15 | 8 | 16 |
| 675020a0 | 13, 15, 30 | 72 | 7 | 4 | 8 |
| 685020a0 | 7, 13, 15, 30 | 142 | 15 | 8 | 16 |

These are counts of the static trees: an arc that fails a carry test or a guard only
removes nodes, and the trees that occur may be smaller. The row 675020a0 is not
in S: its line is kept as proved, and this search does not build its tree.

*The trees with the guard (G7).* The guard (G7) of 9.7 fixes position 7 on every
row before the traversal (GPT Sol, answer AX 1.1), so with it position 7 is free
on no row. The rows 175020a0, 285020a0 and 685020a0 lose the free position 7
that the table gives them: with (G7) they have 72, 140 and 72 forced nodes, 7,
15 and 7 free nodes, 4, 8 and 4 selected nodes and 8, 16 and 8 leaves, and the
other rows of S are unchanged. These trees with (G7) are those of our entry
0bc5f130 and of the cap C(T) of 9.7; the table above is that of the solver
without (G7).

*The trees with the guards (G7) and (G15).* The guard (G15) of 9.7 prescribes
position 15, which is free on every row of S with (G7) (GPT Sol, answer CF 7.2).
With both guards the rows 175020a0, 185020a0 and 685020a0 have the free
positions 13 and 30, 42 forced nodes, 3 free nodes, 2 selected nodes, 2 nodes at
position 15 and 4 leaves, and the rows 275020a0, 285020a0 and 385020a0 the free
positions 9, 13 and 30, 80 forced nodes, 7 free nodes, 4 selected nodes, 4 nodes
at position 15 and 8 leaves (the counts of the table's rule; a node at position
15 is a forced node). These trees with (G7) and (G15) are the trees of the
solver of this package.

The outcomes searched in an outer step that reaches the solver have their bits
set in T, a subset of the mask of Y9 under (1) and of S. By the certificate of
Section 8 every nonzero mask under (1) is one of the twelve nonzero seven-bit
masks of its table, and each of these is a subset of {275020a0}, {175020a0,
675020a0}, {285020a0, 385020a0} or {185020a0, 385020a0, 685020a0}. So the
searched outcomes are among the rows of one of these four sets restricted to S:
{275020a0}, {175020a0}, {285020a0, 385020a0} and {185020a0, 385020a0, 685020a0}.
Without (G7) these have 1, 1, 2 and 3 rows; (140, 15, 8), (142, 15, 8), (418,
46, 24) and (354, 37, 20) forced, free and selected nodes; and 16, 16, 48 and 40
leaves. With (G7) alone they have (140, 15, 8), (72,
7, 4), (280, 30, 16) and (284, 29, 16) forced, free and selected nodes and 16,
8, 32 and 32 leaves. With (G7) and (G15), in the solver of this package, they
have (80, 7, 4), (42, 3, 2), (160, 14, 8) and (164, 13, 8) forced, free and
selected nodes, 4, 2, 8 and 8 nodes at position 15, and 8, 4, 16 and 16 leaves.
A leaf gives at most one root. So an outer step has at most 3 searched
outcomes, 16 leaves and 16 roots, whatever its words (GPT Sol, answers AT 1,
AW 2, AX 1.1 and CF 7.2).

*Families.* Within one of the four sets the rows fall into *families* by two
marks: low row (175, 275, 675) or high row (185, 285, 385, 685), and the bit
gamma[10] (on the class the new rows, which this search does not list, would
form families of their own). gamma[3] is 0 on the low rows and 1 on the high
rows, gamma[10] is 1 on the rows 675 and 685 and 0 on the others, and sigma[20]
to sigma[26] and sigma[0] to sigma[3] are the same on all low rows and on all
high rows; gamma[10] fixes the reset of u[11] in (c). So the formulas of (a) to
(e) and the walks of bits 0 to 5 under both guesses are the same for the rows of
a family and are evaluated once per family (GPT Sol, answer AR 6.4). Restricted
to S the four sets have 1, 1, 1 and 2 families, and at most two rows of a set
share a family. gamma[7] can differ within a family, so bit 6 and its outgoing
carries, h[6], h[7] and h[26] are computed for each row: no prefix of seven bits
is shared.

*What is proved and by whom.* The phase equations, the guards of (c), (d) and
(e), the single traversal and the common state are GPT Sol's (answers AO 5, 6.1
and 6.2 and AR 2), on the constants of answers AE 2.1, AF 1.2 to 1.4 and AN 6
and the transition relation of answer AI 1; the parity certificate (P*), Lemma
J0, the guards of (f) with (P*), the three arrays, the families and the counts
of the static trees are GPT Sol's answer AR (1, 2 and 6.1 to 6.5); the
restriction of the solver to the outcomes of S, with the four sets above, is its
answer AW 2, the same solver visiting only the outcomes of T, with the same
proofs; the guard (G7), with its trees above, is its answer AX 1; and the guard
(G15), with its trees above, is its answer CF 7, with the row-set caps 8,544,
6,656, 13,760 and 17,504 of Section 11 (answers CF 7.2 and CD 11). The
participant recomputed the free positions, the node, leaf and selected counts of
the table and of the four sets, the families, the bits that Lemma J0 reads, and
the sums of the parity certificate against the counts of 10.1; the other
constants and guards were not re-derived by the participant. At positions 25 and
29 the guard selects the candidate before the table read (GPT Sol's corrected
answer AR 6.3): these positions are not prescribed by the carries, so the value
of the guard is written into the key before the read, within the same allowance
and the same proved cap (Section 11). Lemma CV (10.2) states what the solver
returns. The layout is specified and charged by this text; it is not an
implementation (9.5).

**9.5 Checks of the joint solver.** The solver of 9.4 for the class, with the
guards (G7) and (G15) and the certificate of step 3, the pre-check and the
credit of 9.7 are run by the program of the declared experiment (6.4) on every
passing outer step that a trial walks, and every solver call is repeated by the
traversal without (G15), whose roots are certified by real compressions (Section
13). At that scale no root occurs: the solver is checked on the synthetic roots
that every 8th trial plants, and the predicate of the certificate against real
compressions on the charts of step CT (6.4). The completeness of the solver
rests on the proofs cited in 9.4, on Lemmas G7, G15 and RC, on the count of the
class and on the parity certificate; its cap of 17,504 machine units rests on
the schedule of Section 11, an upper allowance written out block by block, which
the program compares with its count of nodes but does not execute as machine
operations; and the pre-check rests on Lemma VP, whose bit identity was checked
on real trials (9.7).

**9.6 Seven outer steps in one word (GPT Sol, answer AQ).** *This package walks
the outer steps by contexts (9.8). This subsection keeps the conventions of the
packed lanes and the rebuild of a passing lane, which 9.8 and Section 11 use,
and summarizes the batch of entry 415e792c, which 9.8 replaces.* Packed words
have the seven 36-bit lanes of 6.5: lane i is bits 36 i to 36 i + 35 of a word,
and it holds a 32-bit value in its low 32 bits with four guard bits above them.
The conventions are those of 6.5. The low 32 bits of a lane are the scalar value
modulo 2^32, and every lane of every sum stays below 2^36, so that no carry
leaves its lane; where an interval bound of a sum could reach 2^36, an AND with
the word M that has the low 32 bits of every lane set is made first, and
charged. x - z is formed as x + (z XOR M) + 1, never by a packed subtraction,
whose borrows could cross lanes. A rotation by r is PROR: ((x >> r) AND A_r) OR
((x << (32 - r)) AND B_r), five operations, with A_r and B_r the masks of its
two parts in every lane; since A_r and B_r keep only bits that come from the low
32 bits of the same lane, PROR gives in the low 32 bits of each lane the
rotation of the low 32 bits of that lane, whatever its guard bits. On packed
words an XOR, an OR and an AND with a constant act on each bit, and an addition
acts on each lane separately while no lane reaches 2^36. The addition of a
constant is kept pending until the value is read by an XOR, an OR, a shift, a
rotation or a table index, and the one addition that then forms it is charged.
All interval bounds depend on the lines and the constants only, not on the
words.

*The batch of entry 415e792c*, which drew seven outer steps at once, each from
its own random word, is replaced by the walk of 9.8: Lemma CX takes the place of
its Lemma PL, Lemma MB that of its Lemma PB, and the charges of 9.8 and Section
11 those of that entry.

*The rebuild of a passing lane.* After the pass count and its test, step CO runs
on scalar words for the member of the lane and gives all the names that steps 2
and 3 read: at most 295 units, the participant's count for entry 415e792c, whose
implementation of that batch rebuilt the names of 4,452 of 4,452 passing lanes
as the earlier program's `ctr_outer` gives them. The pass count and the credit
live in fixed memory words and are reloaded, never restored from a stale copy,
and the E count is kept as 9.8 says. The passing lane of this package, with this
rebuild, is that of 9.8.

**9.7 The s-pattern pre-check with the guards (G7) and (G15), and the credit of
the solver (GPT Sol, answers AW 1, 2 and 5, AX 1, CF 7 and CD 10; a helper
agent of the participant found the pre-check).** Fix a passing outer
step, with mask X, and write Q = Y9, e1 = Y3 + y and, for a trial of it, s =
E1.b1 AND beta*. By the lines of step CT read backwards, Y14 = ROL(E3.h1, 16)
XOR e1, Y10 = Y14 + C2.c1, Y6 = ROR(Y10 XOR C2.b1, 7) and E1.b1 = ROR(Y6 XOR c1,
12), so for each bit p of beta*

    s[p] = Z[(p + 19) mod 32] XOR c1[(p + 12) mod 32],   Z = (Y14 + C2.c1) XOR C2.b1.

At p = 13, 14 and 15 the bits of c1 are fixed by Q* (c1 AND 0e09818b =
02008000), with the values 1, 0 and 0, and the bits of Z are 0, 1 and 2. Every
joint root h has h[16] = h[17] = 0 and h[18] = 1 XOR Q[18] ((PHASE) and (g) of
9.4), and every member of the class has e1[0] = e1[1] = 1. So when E3.h1 is a
joint root the low three bits of Y14 are 1, 1 and 1 XOR Q[18] XOR e1[2], and the
number nu = s[13] + 2 s[14] + 4 s[15] is a function of the outer step:

    r  = (((Q >> 16) XOR e1) AND 4) XOR 7,
    nu = (((r + C2.c1) XOR C2.b1) XOR 1) AND 7.                          (V)

r is exactly the low three bits of Y14 at a joint root. The identity is used
only at joint roots; it says nothing of the other trials of the outer step.

*The allowed values (GPT Sol, answer AW 1).* For an outcome j of beta*, a
pattern s is compatible when E1 can give the differences beta*, tau_j and eps
with that s. With Delta(s) = beta* - 2 s - 8 modulo 2^32, the relation a XOR
(a + Delta) = tau has a solution exactly when d = (tau - Delta) mod 2^32 is even
and d / 2 has no bit outside tau, since a XOR tau - a = tau - 2 (a AND tau)
modulo 2^32 and tau[31] = 0. GPT Sol enumerated the 2,048 submasks of beta* with
this exact criterion for the fourteen outcomes:

| rows | compatible s, rows 175, 185, 275, 285, 385, 675, 685 | allowed nu |
| --- | --- | --- |
| old, tau ending in 20a0 | 16, 32, 8, 16, 32, 8, 16 | 3, 4 |
| new, tau ending in 60a0 | 32, 64, 16, 32, 64, 16, 32 | 2, 3, 4, 5 |

Every compatible s has s[3] = s[4] = 1. In the order (s[13], s[14], s[15]), nu =
3 is 110 and nu = 4 is 001. As a table over the fourteen outcomes, bit j - 1 for
outcome j, VMASK = [0, 0, 3f80, 3fff, 3fff, 3f80, 0, 0] for nu = 0 to 7. Every
outcome of S is an old row, so for this search T = X AND VMASK[nu] is X when nu
is 3 or 4 and empty otherwise. A helper agent of the participant found the same
allowed values from the exact E1 counts L_j split by s (the function L_count of
the counting program of Section 17): 16, 32, 8, 16, 32, 8 and 16 patterns with a
nonzero count on the old rows, each with nu = 3 or nu = 4, half of the count of
the row on each, and every row sum equal to its L_j of 10.1.

**Lemma VP (the pre-check is lossless).** Fix a passing outer step with mask X
and let nu be given by (V). Every listed good trial of the outer step has its
outcome in T = X AND VMASK[nu]. So an outer step or an outcome that the
pre-check skips holds no listed good trial, and the count N_o of H1' of every
outer step is the same, pointwise, as without the pre-check.

Proof. Let a listed good trial have outcome j in S and E3.h1 = h. By the proof
of Lemma F, bit j - 1 is set in both masks, so j is in X; by Lemma V, h is a
joint root of outcome j. By (PHASE) and (g) of 9.4, h[16] = h[17] = 0 and h[18]
= 1 XOR Q[18], and e1[0] = e1[1] = 1 for every member, so by the identity above
the bits s[13], s[14] and s[15] of the trial are those of nu. The trial's E1
gives beta*, tau_j and eps, so its s is compatible with outcome j, and by the
enumeration above nu is allowed for j: VMASK[nu] has bit j - 1. So j is in T.
QED. The lemma uses no law of the words. It says which outcomes a passing outer
step can hold; it does not say how often nu takes a value, which enters only the
credit (H5').

*Checks (participant computations, not part of the package).* On 30,000,000 real
outer steps of the whole class (seed 7, the lines of step CO of a participant
program with the class member), 324,098 real trials with c1 in Q* whose E3.h1
had h[16] = h[17] = 0 and h[18] = 1 XOR Q[18] gave s[13] to s[15] equal to nu by
(V) in 324,098 of 324,098. Planted joint roots with y in the class (seed 11,
every root re-tested against the E3 conditions) had h[16] = h[17] = 0 and h[18]
= 1 XOR Q[18] in 2,944 of 2,944, with all fourteen outcomes covered (82 to 477
roots each). These are checks, not proofs; Lemma VP rests on (PHASE), on (g) of
9.4 and on the exact enumeration.

*The charge (GPT Sol, answer AW 2).* On a passing lane, after the rebuild of
step CO on scalar words, Y9, e1, C2.c1 and C2.b1 are names of the rebuild. (V)
takes 8 operations (a shift, an XOR, an AND, an XOR, an addition, an XOR, an XOR
and an AND); the address and load of VMASK[nu], the AND with X, the comparison
and the branch take 5, and the branch on a nonempty T leads straight to the
credit test: 13 units, inside the 494 of the lane (9.8, Section 11; GPT Sol,
answers CD 3 and CI 1.5), paid by every passing
lane, also when T is empty. The pre-check never enlarges T, so the cap of 9.4
holds for every T. VMASK is built once from the enumeration above, below 2^23
operations, inside the once-only allowance of Section 11.

*Guard (G7), GPT Sol's answer AX 1, as used in our entry 0bc5f130.* Every
compatible s has s[3] = s[4] = 1 (above). At p = 3 and p = 4 the bits of c1 that
Q* fixes are 1 and 0 and the bits of Z are 22 and 23, so s[3] = Z[22] XOR 1 and
s[4] = Z[23]: every listed good trial has Z[22] = 0 and Z[23] = 1. Write C =
C2.c1, B = C2.b1, and a22 and a23 for the carries into bits 22 and 23 of Y14 +
C. Bit 22 of Y14 = ROL(h, 16) XOR e1 is x = h[6] XOR e1[22], and bit 23 is h[7]
XOR e1[23]. The two required sum bits give

    a22  = x XOR C[22] XOR B[22],
    a23  = maj(x, C[22], a22),
    h[7] = e1[23] XOR 1 XOR C[23] XOR B[23] XOR a23.                     (G7)

**Lemma G7.** Let a listed good trial of an outer step have outcome j and E3.h1
= h. Then h[7] is the value that (G7) gives from h[6], e1, C2.c1 and C2.b1.

Proof. The trial's E1 gives beta*, tau_j and eps, so its s is compatible with
outcome j and s[3] = s[4] = 1 by the enumeration above; that is, Z[22] = 0 and
Z[23] = 1 with Z = (Y14 + C) XOR B. Bit 22 of Y14 + C is x XOR C[22] XOR a22,
and it equals Z[22] XOR B[22] = B[22]; this gives a22. The carry out of bit 22
is a23 = maj(x, C[22], a22). Bit 23 of Y14 + C is h[7] XOR e1[23] XOR C[23] XOR
a23, and it equals Z[23] XOR B[23] = 1 XOR B[23]; this gives h[7]. QED. The
unknown carry a22 is fixed by the required bit 22 and need not be computed from
the lower 22 bits; a trial whose true carry differs is not a success, and the E1
test of step 3 would reject it. The lemma uses no law of the words.

*Use in the solver.* h[6] is fixed on every row before the traversal (9.4), so
after it the solver computes h[7] by (G7) for each searched row. On a row on
which position 7 is otherwise free, it becomes prescribed with that value; on a
row on which h[7] is already a constant ((g) of 9.4), the row is dropped for
this outer step when the two values differ. By Lemma G7 no listed good trial is
lost; joint roots that would fail the E1 test of step 3 may be dropped early, so
the solver returns the joint roots of the outcomes of T that satisfy (G7), and
these contain the root of every listed good trial (Lemma CV). Position 7 is then
free on no row (the trees with (G7) of 9.4). h[7] is computed after the row's
own patch of h[6] and is never shared across a family.

*The charge of (G7) (GPT Sol, answer AX 1.1).* 128 more units for each searched
row: the six source bits e1[22], e1[23], C[22], C[23], B[22] and B[23], the
loads and addresses of the three source words, x, the carry a22, the majority,
h[7], the comparison with an existing constant and its branch, and the insertion
of the value into the descriptor of position 7, fewer than 16 blocks of at most
8 units; the scratch words are released before the 32 descriptors are resident,
so the traversal uses no more registers. The caller stores C2.c1, C2.b1 and e1
in three fixed memory words, at most 6 more units, counted in the 494 of the
lane. The extra prescribed bit of the written-out rows is inside the once-only
allowance. (G7) adds no budget and no premise of its own: the credit is debited
with the cap C15(T) before steps 2 and 3 run, and so before (G7) runs (9.1); the
mean of the cap C(T) with (G7) alone, below, is the premise H5' (10.3).

*Guard (G15), GPT Sol's answers CF 7 and CD 10.* Write C = C2.c1, B = C2.b1, V =
Y12 and A = (Y1 + w12) mod 2^32, so that Z = (Y14 + C) XOR B, Y6 = ROR(Z, 7),
E1.a1 = Y6 + A, E1.d1 = ROR(E1.a1 XOR V, 16) and c1 = Y11 + E1.d1 (step CT),
with Y11 = 7af77f38, whose bit 0 is 0. Let a22 be the carry into bit 22 of Y14 +
C, as in (G7), and v16 the carry into bit 16 of Y6 + A, and put

    a22 = h[6] XOR e1[22] XOR C[22] XOR B[22],
    v16 = V[16] XOR 1 XOR A[16].

For the prefix H of the bits h[0] to h[14] of a node at position 15 (its higher
bits zero), with all words of 32 bits:

    L     = (H >> 6) XOR (e1 >> 22),
    zeta  = (((L + (C >> 22) + a22) XOR (B >> 22)) >> 1) AND 1ff,
    p15   = (zeta + ((A >> 16) AND 1ff) + v16) AND 1ff,
    cstar = (Y11 AND 1ff) + (p15 XOR ((V >> 16) AND 1ff)),

    (G15)  cstar AND 08b = 0  and  h[15] = bit 8 of cstar.

**Lemma G15.** Let a listed good trial of an outer step have outcome j and E3.h1
= h. Then h satisfies (G15).

Proof. The trial has Z[22] = 0 and Z[23] = 1 (proof of Lemma G7) and c1 in Q*,
so c1[0] = c1[1] = c1[3] = c1[7] = c1[8] = 0 (the mask 0e09818b and the value
02008000). Bit 22 of Y14 + C is h[6] XOR e1[22] XOR C[22] XOR a22 and equals
Z[22] XOR B[22] = B[22], which gives a22. c1[0] = 0 and Y11[0] = 0 give E1.d1[0]
= 0, that is E1.a1[16] = V[16]; Y6[16] = Z[23] = 1; and bit 16 of Y6 + A is 1
XOR A[16] XOR v16 = V[16], which gives v16. Bits 22 to 31 of Y14 = ROL(h, 16)
XOR e1 are h[6] to h[15] XOR e1[22] to e1[31], which are L when h[15] = 0.
Adding C[22..31] with the carry a22 and XORing B[22..31] gives Z[22..31], and
the shift drops Z[22]: zeta is Z[23..31] = Y6[16..24]. Adding A[16..24] with the
carry v16 gives E1.a1[16..24], so p15 XOR V[16..24] is E1.d1[0..8], and adding
Y11[0..8] with no carry into bit 0 gives c1[0..8]. So the low nine bits of cstar
are c1[0..8] of the trial with h[15] set to 0. Changing h[15] alone flips
Y14[31], hence Z[31], Y6[24], E1.a1[24], E1.d1[8] and c1[8], and no lower bit of
these words. As c1[0] = c1[1] = c1[3] = c1[7] = 0, cstar AND 08b = 0; as c1[8] =
0, h[15] = bit 8 of cstar. QED. The carries a22 and v16 are those of a listed
good trial: a word whose true carries differ is not a success, and step 3 still
tests every root in full (Lemma RC). The lemma uses no law of the words.

*Use in the solver.* For each searched row, after (G7), the solver stores five
words in fixed memory: e1 >> 22, (C >> 22) + a22, B >> 22, ((A >> 16) AND 1ff) +
v16 and (V >> 16) AND 1ff; a22 needs h[6], fixed on the row. At each node of
position 15 it computes cstar from the prefix of the node, drops the prefix when
cstar AND 08b is not 0, and otherwise prescribes h[15] = bit 8 of cstar in a
temporary copy of the descriptor of position 15, which the forced transition
array then reads; the stored descriptor is not changed, since another prefix may
need the other value. Position 15 is then free on no row (the trees with (G15)
of 9.4). By Lemma G15 no listed good trial is lost; the solver returns the joint
roots of the outcomes of T that satisfy (G7) and (G15) (Lemma CV).

*The charge of (G15) (GPT Sol, answer CF 7.2).* 128 more units for each searched
row, for its five words: the loads and addresses of their sources, at most 24;
the additions, masks, shifts and the two carries, at most 24; five stores with
their addresses, 10; row control and addresses, 16: 74. 64 more units at each
node of position 15, besides its 20 as a forced node: five loads with their
addresses, 10; the shift, XOR, addition, XOR, shift and AND of zeta, 6; the
addition, AND, XOR and addition of p15 and cstar, 4; the test of cstar AND 08b
and its branch, 3; bit 8 taken out and the temporary key patched, at most 6;
copies and control, at most 16: 45. It uses the ten temporaries of the traversal
and spills nothing (Section 11). Its code, the layout of the five words and the
updated CT are inside one more once-only allowance of 2^20 (Section 11).

*The credit (GPT Sol, answers AW 5, CD 10 and CD 11).* For a subset T of S,
C(T) denotes the cap with the guard (G7) alone, the ledger of our entry
0bc5f130 on the rows of T, C(T) = 4,096 + 2,304 F + 1,280 A + 20 N_f + 48 N_r +
4 N_s + 368 Lf, where A is the number of rows of T, F the number of their
families (9.4; 175020a0 and 275020a0 never occur together and count as two),
and N_f, N_r, N_s and Lf are the sums, over the rows of T, of the forced, free
and selected nodes and of the leaves of their trees with (G7) in 9.4; and
C15(T) the cap of this package, C15(T) = 1,024 + 2,304 F + 1,408 A + 20 N_f +
48 N_r + 4 N_s + 64 N_15 + 200 Lf over their trees with (G7) and (G15), N_15
their nodes at position 15, with the global ledger of 1,024 of Section 11; both
are 0 for T empty. Section 11 shows that in every outer step whose pre-check
gives T, whatever its words, steps 2 and 3 cost no more than C15(T) machine
units, that C15(T) <= 17,504 for every T that occurs, and that C15(T) <= 16/27
C(T) for every T that occurs. The table CT stores C15(T) in 128 words indexed
by the seven-bit mask T, of which the 64 subsets of S are used; it is built
once, inside the once-only allowance of Section 11.

When T is not zero the lane forms the address of CT[T] and loads it, forms the
address of the remaining credit and loads it, compares them, branches to the
halt when C15(T) exceeds the credit, and else subtracts C15(T) and stores the
credit at the address already formed: 8 units, inside the 494 of the lane (9.8,
Section 11; GPT Sol, answers CD 3 and CI 1.5). The whole cap C15(T) is debited before steps
2 and 3 run, so
the work of steps 2 and 3 over a run is at most CREDIT, whatever the words; no
meter is placed inside the solver, and the debit is the proved cap, not the work
done. An outer step whose C15(T) exceeds the remaining credit halts the run with
failure before steps 2 and 3; a final failed test is charged once more, 16
(Section 11). The credit is a halt like the budgets of 9.1, so the time bound
depends on no mean; whether the credit suffices is the premise H5' (10.3),
which bears on the success probability alone.

**9.8 The member loop, the direct tables and the omega-first batch.** This
subsection defines the walk of step 1 of 9.1. The member loop and the direct
tables are those of entry e9b6649e of the participant hecmas, described here in
our own words and checked by a separate reimplementation of the participant; the
omega-first order of the batch is GPT Sol's answer CA, whose partition,
listings, registers and charge the participant derived from the printed lines of
step CO and checked by programs (below); the fused line of the Y9 path, the
allowance of a context and the layout of a passing lane are GPT Sol's audit of
that charge, answer CD (sections 1 and 3), and the E count held in a register,
with the frame of a passing lane, is its answer CD (sections 6 and 8.1). The
walk takes the place of the batch of 9.6 of entry 415e792c; it uses the packed
words, lanes, guard bits and masked rotation PROR of 6.5 and 9.6 and the machine
of Section 11.

*Contexts.* The seven outer words C0.d1, D2.a1, D2.b1, S11, S4, X9 and w6 of
step CO together are called a *context*. Fixing a context and a member y of the
class fixes an outer step, whose trials are its 2^21 values of c1 in Q* (Section
8). The member loop changes only the order and the grouping in which outer steps
are visited; each outer step, with its filter, pre-check, guards (G7) and (G15),
solver and certificate, is that of Sections 8 and 9.

**Lemma Y (the lines that read the member).** Call a line of step CO *needed*
when Y9 or w8 depends on it, directly or through other lines; 64 of the 77 lines
are needed. Call a needed line *member-dependent* when one of its operands is y
= Y4 or a member-dependent line. Exactly 25 needed lines are member-dependent;
in the order in which step CO prints them, numbered here, they are

     1 to  5:   Y8     Y12    Y0     C0.a1  X0
     6 to 10:   D0.d1  D0.c1  D0.b1  X10    X5
    11 to 15:   X12    D1.c1  D1.d1  X1     C1.a1
    16 to 20:   C1.d1  D1.a1  C1.c1  w10    C1.b1
    21 to 25:   Y1     Y13    Y9     D0.a1  w8

The remaining 39 needed lines, in the same printed order,

     1 to  8:   X2     X8     C0.c1  K3.a1  K3.d1  K3.c1  S15    S3
     9 to 16:   K3.b1  D3.a1  S7     D3.b1  D2.c1  D3.c1  X4     X13
    17 to 24:   X14    C0.b1  D2.d1  D3.d1  S13    S9     K1.c1  K1.d1
    25 to 32:   K1.a1  w2     S14    K1.b1  S10    S5     S1     w3
    33 to 39:   S8     K0.b1  S6     K0.c1  S12    K0.d1  S0

depend on the seven outer words and on constants only. Besides these, omega =
Y3 + y + w8 depends on the member.

*Proof.* Both statements are finite checks on the printed text of step CO.
Walking the lines in printed order and marking a line when an operand is y or a
marked line gives the first list; Y8 is the first line marked. Each line of the
second list has as operands only outer words, constants (IV, the six constants
of 3.2 and the four constant values of K2) and earlier unmarked lines.
Collecting the lines on which Y9 and w8 depend gives the 64. QED. A participant
program that parsed step CO from its printed lines and computed both sets
reproduces the two lists in this order; it checks the lists and is not part of
the proof (Section 13).

Hence, within one context, the 39 context lines can run once; per member, only
the 25 member-dependent lines and omega remain.

**Lemma CX (contexts and the class).** Let a run draw its contexts as in step 1
of 9.1. (a) Different contexts read different fresh words, so the contexts are
independent, and within a context the seven outer words are independent and
uniform. (b) The member lists of 9.9 hold every member of the class in exactly
one lane, so a context walks every member once, except the members of the
clusters that its gate skips, whose outer steps have a zero mask of (2) (Lemma
CL). (c) For any function g of an outer step with a finite mean, let G be its
sum over the 2^19 outer steps of one context. Then E[G] = 2^19 E[g(U)], with U
an outer step whose seven outer words are uniform and whose member is uniform on
the class and independent of them: the outer step that step 1 of entry 415e792c
draws. The values of G for the contexts of a run are independent and identically
distributed. (d) If 0 <= g <= c on every outer step, then 0 <= G <= 2^19 c.

*Proof.* (a) holds by the construction of step 1. (b) The representative lists
hold the 16,384 representatives once each and the partner lists the 31 partners
of every cluster once each (9.9); the clusters partition the class. (c) G is the
sum over all members y of g at the outer step (context, y). For each fixed y the
outer words of the context are uniform and do not depend on y, so the mean of
that term is E[g(W, y)] with W uniform; summing over the 2^19 values of y gives
2^19 E[g(U)]. G is a function of the fresh word of its context only, so (a)
gives the independence and the equal laws. (d) is immediate. QED. By Lemma CL,
each quantity whose totals 10.3 and 10.4 use, the indicators of the E count and
of the pass count, V and N_o, is zero on the outer steps that the gate skips, so
its total over the outer steps that a context walks is its G.

What the member loop does to the law of the run is therefore limited to
dependence. The means that the heuristics use, the rate of H1', the shares of
H4' and the mean of H5', are those of a uniform outer step, exactly as in entry
415e792c; but the 2^19 outer steps that share a context also share its seven
words, so independence holds between contexts and not between outer steps. 10.3
states the dependence part of H1' for contexts and proves the tails of H4' and
H5' over contexts.

**Lemma DT (the direct tables).** The tables T2 and T1 have one entry for each
32-bit word x: T2[x] = (mask of (2) on x) AND 5f and T1[x] = (mask of (1) on x)
AND 5f. A lane therefore reads, with one load each, the same masks restricted to
S that the two automata of Section 8 give.

*Proof.* Step 0 of 9.1 computes each entry by running the corresponding
automaton of Section 8, with its last table ANDed with S, on x, one byte table
per byte, as `ctr_look` of the earlier program does and as the program of 6.4
does for every entry that it reads. QED. Cost of the build: for each of the 2^32
words and each of the two tables, the four bytes of the word are separated (a
shift and an AND each), the state is advanced with four table loads and three
additions, the mask is ANDed with S and stored at its address, and the loop
advances; fewer than 32 units, so fewer than 2^32 * 2 * 32 = 2^38 units in all,
and Section 11 charges 2^39. The two tables have 2^33 entries, 2^38 bytes as
words of 256 bits (Section 12). Since every entry is the automaton's mask, the
share of passing pairs read through the tables is SHARE / 2^64, as in Section 8.

*The member lists.* Step 0 of 9.1 writes the member lists of 9.9. In a word U[b]
of a list, lane i is ROL(y, 7) for the member y of the lane, the word that the
line Y8 reads, and in the word E[b] it is e1 = Y3 + y, the word that omega
needs; the unused lanes of a last word hold copies of its last member and are
never tested.

*The words of a context.* Once the 39 context lines have run on scalar words, a
context prepares the sixteen operands that the member-dependent lines take from
it, C0.b1, -C0.c1, C0.d1, -C0.b1 - w6, ROL(C0.d1, 16), K = X11 + 1 - S11, S12,
-X4 - w2, -S1 - S6, S15, S10, S5, w3, X13, X9 and -S0 - S5 (subtractions modulo
2^32), and copies each into all seven lanes. These sixteen packed words occupy
sixteen registers while the batches of the context run. Every other operand of
those lines is fixed for the whole search: ROL(X15, 8), X15, the lane mask M
(the low 32 bits of every lane) and the masks of PROR are written into the
instructions. The context also stores, once, the scalar names that a passing
lane needs for its rebuild.

*The omega-first batch.* The 25 member lines split in two. The 8 lines Y8, Y12,
Y0, C0.a1, X0, D0.d1, D0.a1 and w8, with omega, are those that omega needs: the
*omega side*. The other 17, D0.c1, D0.b1, X10, X5, X12, D1.c1, D1.d1, X1, C1.a1,
C1.d1, D1.a1, C1.c1, w10, C1.b1, Y1, Y13 and Y9, are needed by Y9 alone: the *Y9
path*. Every member line is in exactly one of the two, and the Y9 path reads of
the omega side only C0.a1 (in X12) and D0.d1 (in D0.c1). For batch b of a
context, on packed words, with the units of each line (one for each operation
and load, five for PROR, where PROR(x, r) rotates the low 32 bits of every lane
right by r):

    U    = load U[b]                       1   (at the pair pointer p)
    Y8   = U XOR C0.b1                     1
    Y12  = Y8 + (-C0.c1)                   1
    Y0   = PROR(Y12, 24) XOR C0.d1         6
    C0a1 = Y0 + (-C0.b1 - w6)              1
    X0   = C0a1 + (-X4 - w2)               1
    D0d1 = X0 XOR ROL(X15, 8)              1
    D0a1 = PROR(D0d1, 16) XOR S15          6
    w8   = D0a1 + (-S0 - S5)               1
    E    = load E[b]                       1   (and its address p + 1, 1)
    om   = E + w8                          1   (omega = Y3 + y + w8)

The eight lines and omega cost 19 units; the two list loads cost 2 and the
address p + 1 of the second 1 more, since the two list words of a batch are
adjacent (9.9). Next come seven *lane tests*, for i = 0 to 6. Lane i shifts om
right by 36 i (lane 0 needs no shift) and keeps the low 32 bits with an AND,
adds that omega to the base address of T2 and loads the mask of (2), then
compares the mask with zero and branches: 6 units per lane and 5 for lane 0, 41
in all. Finally the batch cursor is incremented, compared and branched on, 3
units. Every partner batch of seven lanes therefore executes *66 units*; a
representative batch tests the gate in place of T2 (9.9). C0a1, D0d1 and om stay
in registers through the lane tests.

A lane whose mask of (2) is not zero runs its *Q path* right after its lane
test. The Q path first updates the E count and tests it (GPT Sol, answers CD 1,
6 and 8.1). The count n_E lives in one register of the batch for the whole run:
the Q path increments it, compares it with E_BUDGET, an immediate, and branches
to the halt when it is larger, 3 units. Only the Q path writes n_E; the context
does not reset it, and a passing lane saves it with the other words of the batch
and reloads it unchanged (below), so at every Q path it is the exact count so
far, and the test precedes the Y9 path as before. It then builds the Y9 path on
packed words from C0a1 and D0d1 of the batch and the words of the context; the
second column gives the units of a line and the third their running sum:

    X12  = C0a1 XOR ROL(C0.d1, 16)        1    1
    D1d1 = (X12 XOR M) + K                2    3   (= X11 - X12 - S11)
    X1   = PROR(X12, 24) XOR D1d1         6    9
    D1a1 = PROR(D1d1, 16) XOR S12         6   15
    w10  = D1a1 + (-S1 - S6)              1   16
    D0c1 = D0d1 + S10                     1   17
    D0b1 = PROR(S5 XOR D0c1, 12)          6   23
    X10  = D0c1 + X15                     1   24
    X5   = PROR(D0b1 XOR X10, 7)          6   30
    C1a1 = X1 + X5 + w3                   2   32
    C1d1 = PROR(X13 XOR C1a1, 16)         6   38
    C1c1 = X9 + C1d1                      1   39
    C1b1 = PROR(X5 XOR C1c1, 12)          6   45
    Y1   = C1a1 + C1b1 + w10              2   47
    Y13  = PROR(C1d1 XOR Y1, 8)           6   53
    Y9   = C1c1 + Y13                     1   54

Step CO forms D1.c1 = X11 - X12 and then D1.d1 = D1.c1 - S11; D1.c1 has no other
use among the 25 lines of Lemma Y (D1.b1, which also reads it, is not needed),
so the line D1d1 forms D1.d1 at once from K = (X11 + 1 - S11) mod 2^32, which
the context prepares in place of -S11 (GPT Sol, answer CD 1). The 17 lines of
the Y9 path, D1.c1 and D1.d1 in one line, cost 54 units. Lane i of Y9 is then
isolated (shift and AND, 2), used as an index into T1 (base addition and load,
2), and the mask of (1) found there is ANDed with the mask of (2), compared with
zero and branched on (3). A Q path therefore costs *64 units*: 3 + 54 + 7. The
Y9 path runs after the test of the E count, so it runs in at most E_BUDGET lanes
of a run, and the lane that halts the run on that test does not reach it. When a
batch has two or more lanes with a nonzero mask of (2), each of their Q paths
computes the Y9 path again from the same C0a1, D0d1 and words of the context,
which no Q path changes, and gets the same packed values: each Q path does
exactly the work charged, and no flag and no budget per batch is needed.

*The code of a batch.* It is written out for the seven lanes in order: the lane
test of lane i, whose branch skips the Q path of lane i when its mask of (2) is
zero; then the Q path of lane i, whose last branch goes to the passing lane when
X is not zero and otherwise falls through to the lane test of lane i + 1. A
passing lane returns to the lane test of lane i + 1, inside its own units
(Section 11). The fifth partner word of a cluster has three used lanes, and its
code has the lane tests and Q paths of lanes 0 to 2 only: the two list loads
with the address p + 1, 3, the omega side, 19, three lane tests, 5 + 6 + 6 = 17,
and the cursor, 3, so it costs at most *42 units* (GPT Sol, answers CI 1.5 and
CJ 3). So every dispatch of a batch is inside its 66 units, or 42, and those of
its Q paths.

*Registers.* The bases of T1, T2, U and E are immediate operands, written into
the instructions with the code (GPT Sol, answer CD 3). Live through a batch: the
29 words that a passing lane saves (below), that is the sixteen words of the
context, C0a1, D0d1, om, the packed E[b], the batch cursor, the context count,
the lane, its return link, the mask of (2) of the current lane and the E count
n_E, with the two operands of the gate and the key of 9.9, and two temporaries
of the lane tests: 31 words. A Q path adds at most six packed values of the Y9
path live at once (a liveness count on the listing above) and the two
temporaries of PROR: at most 39 of the 64 registers are live, and nothing is
spilled.

**Lemma MB (the packed batch is exact).** Take any used lane i of any batch, and
let (context, y) be its outer step. (a) The low 32 bits of lane i of om equal
omega = Y3 + y + w8 as step CO computes it for that outer step, and the lane
test reads T2 at that value. (b) If the lane runs a Q path, the low 32 bits of
lane i of the packed Y9 built in that Q path equal the Y9 of step CO for the
same outer step, and the Q path reads T1 at that value. (c) The lane is taken as
passing exactly when its outer step passes the filter of Section 8. (d) No lane
of any packed value reaches 2^36.

*Proof.* The two listings contain the member-dependent lines of Lemma Y and
omega, D1.c1 and D1.d1 in one line, each written with packed operands: a word
of the context appears as the packed word that repeats its scalar value in
every lane, subtracting such a word is adding its negation modulo 2^32, and
the one subtraction of a member-dependent value, in D1.d1 = (X11 - X12) - S11,
is written (X12 XOR M) + K with K = (X11 + 1 - S11) mod 2^32; X12 XOR M flips
the low 32 bits of each lane and keeps its guard bits, and (2^32 - 1 - x) +
X11 + 1 - S11 = X11 - x - S11 modulo 2^32, so the low 32 bits of the result
are the D1.d1 of step CO. An XOR acts on each bit; an addition acts on each
lane separately while no lane reaches 2^36, and then the low 32 bits of a lane
are the sum modulo 2^32; PROR gives in the low 32 bits of each lane the
rotation of the low 32 bits of that lane, whatever its guard bits (9.6). Lane
i of U[b] and of E[b] holds ROL(y, 7) and Y3 + y for the member of the lane.
By induction over the printed order the low 32 bits of each lane of each line
are its scalar value. The Y9 path reads the values C0a1 and D0d1 of the omega
side of the same batch, which the lane tests and the Q paths do not change, so
the order of the two parts changes no value. The lane test and the Q path take
the low 32 bits of lane i, and Lemma DT gives the masks. When the mask of (2)
is zero the AND of the two masks is zero whatever the mask of (1), so leaving
out the Y9 path and the mask of (1) in such a lane changes no decision; in any
other lane the decision is that AND, as in Section 8. *Bounds.* Every loaded
word and every word of the context is below 2^32 in every lane, and so is the
output of PROR. Carry an exclusive upper bound through the lines: an addition
of values below A and B is below A + B - 1, and an XOR of values below A and B
is below the least power of two that is at least the larger of A and B. These
bounds are functions of the lines alone, not of the words. Among the sums, Y1
has the largest bound, 9 * 2^32 - 5 < 2^35.17; among the XORs, the input of
the PROR of Y13 has the largest, 2^36; om and Y9 stay below 3 * 2^32. So no
lane reaches 2^36, and no AND with M is needed before a sum. QED. The bounds
are those of the member loop of entry e9b6649e, whose lines are the same; the
participant recomputed them for this order and for the fused line, whose
bound, 3 * 2^32 - 1, is below the 4 * 2^32 - 2 of the two lines it replaces,
and a participant simulation of the order with the two lines apart asserted
every value of every operation below 2^36 (below).

*A context.* Drawing the fresh word, the 39 context lines on scalar words,
forming and copying the sixteen packed operands, storing the names for rebuilds
and the context loop come to at most 507 units, and to at most 547 with the two
operands of the gate of 9.9, itemized in Section 11 and charged as 600 per
context (GPT Sol, answers CD 1 and CI 1.5).

*A passing lane.* A lane that passes first advances the pass count, which lives
in a fixed memory word, and tests it (step 1 of 9.1): its address, load,
increment, store, comparison with the immediate PASS_BUDGET and branch, six
operations. It then reloads the seven outer words from the names stored for its
context and the word E[b], and takes y out of lane i of E[b] (a shift, an AND
and the subtraction of Y3); runs step CO on scalar words for all the names that
steps 2 and 3 read; stores C2.c1, C2.b1 and e1 in three fixed words for the
guards (G7) and (G15); runs the pre-check of 9.7; and, when T is not zero, runs
the credit test of 9.7 and, when the credit covers C15(T), steps 2 and 3, which
may use all 64 registers. Before steps 2 and 3 the lane stores the 29 words that
the batch still needs, and the eight reserved registers of an opened cluster
(9.9), and reloads them afterwards, the words live through a batch listed above; the return link among them brings the lane back to the lane
test of the next lane. The packed Y9 is not among them: the next lane with a
nonzero mask of (2) rebuilds its Y9 path from C0a1, D0d1 and the words of the
context. No callee writes n_E, so its reloaded copy is current; the pass count
and the credit live in fixed memory words and are reloaded, never restored from
a stale copy. Section 11 itemizes the lane at 494 units (GPT Sol, answers CD 3
and CI 1.5; 462 in entry a402a477, and 32 more for the eight reserved registers
of 9.9).

*The participant checks.* Three participant programs, which are not part of the
package and which the organizer does not run. (1) A reimplementation of the
member loop of entry e9b6649e (research/impl/memberloop of the participant)
parsed the lines of step CO, found the two lists of Lemma Y in the printed
order, and on 100,000 random pairs of a context and a member compared Y9, omega,
both masks, the pass decision and all 25 member-dependent lines with the full
step CO, with 0 differences; a graphics-card version, with the two direct
tables, agreed with the full step CO on 100,000 vectors. (2) A Python program
(research/frontline/ca of the participant) derived the omega side and the Y9
path from the same parsed lines and ran, on 1,000,006 pairs of a context and a
member (142,858 batches of seven consecutive members in 1,429 contexts), the
omega-first batch on scalar words and as a packed simulation with seven 36-bit
lanes that executes and counts every operation, load and PROR and asserts every
lane value below 2^36, against the full member loop: the pass decisions differed
in 0 cases, scalar and packed, and the mask of (2) and Y9 differed in 0 of the
54,067 lanes with a nonzero mask of (2); 1,044 lanes passed; the simulation
executed 67 units in every batch and 78 in every Q path, the Q path of answer
CA, with 16 for the E count and the lines D1.c1 and D1.d1 apart (the E count in
a register and the fused line above are written out, not simulated); the largest
lane value was 2^35.02. (3) A graphics-card version of the omega-first batch
(RTX 3090) agreed with Python's full member loop on 1,000,000 vectors (0
differences, 53,034 lanes with a nonzero mask of (2), 971 passes), and walked
2,048 contexts (2^30 outer steps, seed 1) and 120,000 contexts (62,914,560,000
outer steps, seed 2), every member of every context, with the omega-first batch
and the full member loop on every outer step: 0 different pass decisions, 0
different masks of (2) and 0 different values of Y9 in the 3,418,392,488 lanes
of the larger run with a nonzero mask of (2), and 62,294,500 passes. Lanes with
a nonzero mask of (2) were 0.054334 of the outer steps, against the exact share
0.054416 and the share 0.054418 that E_BUDGET allows, and 11.8 per cent of the
batches had at least one. These programs check the walk up to the pass decision;
they do not run the pre-check, the guards (G7) and (G15), the solver, the
certificate of step 3 or the credit.

**9.9 The cluster gate (GPT Sol, answers CI 1, CJ and CK 5; Lemma OR, GPT-6
Luna, sharpened in answer CK 5).** This subsection fixes the order in which a
context walks its members and lets it skip, with one table read, a group of 32
members that is proved to fail test (2). Every outer step that is walked is that
of 9.8, with the same batch, lane test, Q path and passing lane.

*Clusters.* Write e = Y3 + y for the word e1 of a member y. The class fixes the
13 bits of e in 03cf8303 and leaves the other 19 free (Lemma Q); bits 10 to 14
are free and bit 15 is fixed at 0. Let g run over the 2^14 settings of the 14
free bits other than 10 to 14, and let e_g have these bits and bits 10 to 14
zero. The *cluster* of g is the 32 members with e = e_g + j * 2^10, 0 <= j < 32;
its *representative* is the member with j = 0, and the other 31 are its
*partners*. The 16,384 clusters partition the class.

In one context put b = C0.b1, c = C0.c1, d = C0.d1, A = C0.b1 + w6 + X4 + w2, L
= ROL(X15, 24) XOR S15 and C = e - S0 - S5, all modulo 2^32. With r = ROL(y, 7)
XOR b, v = r - c (the line Y12), p = ROL(v, 8) XOR d (the line Y0) and x = p - A
(the line X0), the omega side of 9.8 gives

    omega = (ROL(x, 16) XOR L) + C,

since D0.a1 = ROL(X0 XOR ROL(X15, 8), 16) XOR S15 and omega = e + D0.a1 - S0 -
S5. The term ROL(X15, 24) of L is part of the identity.

**Lemma KP (two prefixes per cluster).** Fix a context and a cluster. Let p_0 be
the p of its representative, u = (((p_0 >> 16) AND 1ff) - ((A >> 16) AND 1ff))
mod 512, and W_l = (C + (((u - l) mod 512) XOR (L AND 1ff))) mod 512 for l = 0
and 1. Then every member of the cluster has omega mod 512 in {W_0, W_1}.

*Proof.* The members of a cluster differ only in bits 10 to 14 of e, so C mod
512 is the same for all of them. Bit 15 of e is 0, so e mod 2^16 < 32,768,
while Y3 mod 2^16 = c181 = 49,537: the subtraction y = e - Y3 borrows into bit
16 in every member, and bits 16 to 31 of y, like bits 0 to 9, are the same for
all members; only bits 10 to 15 differ. Then r differs only in bits 17 to 22,
so bits 0 to 16 of v = r - c are the same for all members, and its bits 24 to
31 take at most two values, which differ by the borrow into bit 24. Hence bits
8 to 24 of p = ROL(v, 8) XOR d are the same for all members and only its low
byte varies. Bits 16 to 24 of x = p - A are ((p >> 16) AND 1ff) - ((A >> 16)
AND 1ff) - l modulo 512, where l in {0, 1} is the borrow of (p mod 2^16) - (A
mod 2^16) into bit 16; the first term is that of the representative, so these
bits are (u - l) mod 512. Bits 0 to 8 of ROL(x, 16) are bits 16 to 24 of x, and
bits 0 to 8 of a sum depend only on bits 0 to 8 of its terms, so omega mod 512
= W_l. QED. The two values may be equal, and one of them may not occur: the
lemma is a cover, not a rate.

**Lemma A9 (dead residues of test (2)).** Let S7 be the 52 residues 25 to 3e and
45 to 5e (hexadecimal) modulo 128. If omega mod 128 is not in S7, then (2)_j
fails for omega for every j in S, and T2[omega] = 0.

*Proof.* A word f with (omega + f) XOR ((omega + DY3) + (f XOR sigma_j)) = eps
(Section 8) satisfies the equation modulo 2^9, whose bits depend only on omega
and f modulo 2^9. For the six outcomes of S, sigma_j mod 2^9 = f0 (the low
twelve bits of every tau_j are 0a0), DY3 mod 2^9 = fd and eps mod 2^9 = 55. The
finite check

    [r for r in range(512)
     if any((((r + f) ^ (r + 0xfd + (f ^ 0xf0))) & 511) == 0x55 for f in range(512))]

lists the residues r of omega modulo 2^9 for which the equation modulo 2^9 has a
solution: 208 residues, exactly those whose value modulo 128 lies in S7. For any
other omega no j in S satisfies (2)_j, and by Lemma DT the mask of (2),
restricted to S, is zero. QED.

*The gate table.* For 0 <= a, q, c < 128 let P[a + 128 c + 16,384 q] = 1 when
((a XOR q) + c) mod 128 or ((((a - 1) mod 128) XOR q) + c) mod 128 lies in S7,
and 0 otherwise: 2^21 entries of one word, 2^26 bytes, fixed for the whole
search. For every fixed (q, c) at most 63 of the 128 values of a give 1 (each
set T = {a : ((a XOR q) + c) mod 128 in S7} gives |T union (T + 1)| <= 63), and
940,000 of the 2^21 keys give 1; both are finite checks.

**Lemma CL (the gate is lossless).** Fix a context and a cluster, and let a = u
mod 128, q = L mod 128 and c = C mod 128, with u of Lemma KP. If P[a + 128 c +
16,384 q] = 0, then every member of the cluster has T2[omega] = 0; none of its
outer steps runs a Q path or passes the filter, and none holds a listed good
trial.

*Proof.* By Lemma KP the omega of a member is, modulo 128, (c + (((u - l) mod
128) XOR q)) mod 128 for some l in {0, 1}, and (u - l) mod 128 is a or (a - 1)
mod 128. P = 0 says that neither value lies in S7, so Lemma A9 gives T2[omega]
= 0. A lane with a zero mask of (2) runs no Q path and does not pass (Lemma MB
(c)), and by Lemma F an outer step that does not pass holds no listed good
trial. QED.

Hence skipping a cluster whose gate entry is 0 loses nothing: the E count, the
pass count, the work of passing lanes and of steps 2 and 3, the debits of the
credit and the number N_o of 10.3 are zero on every outer step that the gate
skips, so their totals over the outer steps that a context walks equal their
totals over all 2^19 outer steps of the context, outer step by outer step. The
gate needs no law of the words.

*The walk of a context.* Step 0 of 9.1 writes the member lists in cluster order
as pairs of adjacent words (U, E) (GPT Sol, answer CJ 3): 2,341 representative
pairs, lane i of pair b holding the representative of cluster 7 b + i (lanes 0
to 3 in the last pair), and five partner pairs per cluster, holding its partners
j = 1 to 31 in order, seven to a pair and three in the fifth; 168,522 words,
5,392,704 bytes, every member in exactly one lane. A batch loads U at its
pointer p, forms p + 1 and loads E, 3 units (9.8), so a partner batch costs 66
and the fifth of a cluster, with three lanes, 42. Besides the sixteen operands
of 9.8 a context prepares -(A >> 16) mod 128, copied into the lanes, and the
scalar base P_q = P + 16,384 q of the block of P for its q = L mod 128 (answer
CJ 4). For each representative pair it runs a *representative batch*:

- the omega side of 9.8, whose line Y0 gives p in every lane;
- the key of every lane, on packed words with the mask R7 of the low seven bits
  of each lane: a = (((p >> 16) AND R7) + (-(A >> 16) mod 128)) AND R7, c = (E +
  (-S0 - S5)) AND R7 and key = a OR (c << 7), 8 operations; every field stays
  below 2^14 in its lane;
- for each used lane in order, the *gate test*: the key of the lane taken out by
  a shift and an AND (lane 0 needs no shift), P_q added and the entry loaded,
  compared with zero and branched on, 6 units, 5 for lane 0. On 0 the cluster is
  skipped, and the representative's T2 is not read: its mask of (2) is zero by
  Lemma CL (answer CJ 2). Otherwise the cluster is *opened*: the opened count,
  which a register holds for the whole run (this package), is incremented and
  compared with the immediate
  A_BUDGET, and the run halts with failure when it exceeds A_BUDGET; then the
  representative reads T2 at its omega and tests the mask, 6 units, with its Q
  path and passing lane those of 9.8, and the five partner pairs of the cluster
  run as five batches of 9.8, each with its lane tests, Q paths and passing
  lanes, whether or not the representative's mask is zero, before the gate test
  of the next lane.

*Registers of an opened cluster (this package).* The seven words of the
representative batch that the partner batches would overwrite and that are read
again, the packed E word, om, C0a1, D0d1, the representative pair pointer, the
lane and its return link, were stored in a fixed frame of seven memory words in
entry a402a477 and reloaded after the fifth partner batch (answer CJ 5), at 28
units. Here the representative batch writes these seven values into seven
registers, R_F1 to R_F7, that the code of a partner batch, of a Q path and of a
lane test never names, and the opened count lives in one more such register,
R_A, for the whole run; the code is written out statically with every register
named (Section 11), so this is a choice of names, not a move. Register budget:
through a partner batch at most 31 registers are live and at most 39 in a Q path
(9.8); with the eight reserved registers that is at most 39 and 47 of the 64. A
passing lane, which may use all 64 registers in steps 2 and 3, stores these
eight words with the 29 of 9.8 before steps 2 and 3 and reloads them after:
37 words, 32 units more than in entry a402a477, charged to every passing lane
(Section 11). So when the fifth partner batch returns, R_F1 to R_F7 hold the
values that the representative batch wrote, unchanged, and the gate test of the
next lane reads them as it read the frame. The packed key and the context
cursor are not written during the partner loop: they sit in two of the 29
registers that every passing lane saves and reloads. The representative's mask
of (2) is not saved: after its Q path no step reads it, a closed next gate reads
none and an opened one loads a fresh one. The E count, the pass count, the
credit and the opened count are never restored from a stale copy: the pass count
and the credit live in fixed memory words, and n_E and the opened count are in
registers that only their own increments write, saved and reloaded together by a
passing lane, whose callees write neither. Every label is fixed in the code, and the
return goes to the gate test of the next lane.

*Charges (Section 11).* A representative batch costs 74: 3 for its pair of
list words, 19 for the omega side, 8 for the key, 41 for the seven gate
tests and 3 for the cursor; it reads no T2 (answers CJ 2 and 4). The last
representative pair has four used lanes and costs 56, its four gate tests
costing 5 + 3 * 6 = 23. An opened cluster costs 333 (364 in entry a402a477):
its five partner batches, 4 * 66 + 42 = 306, where the batch of three lanes
costs 3 for the pair loads, 19 for the omega side, 5 + 6 + 6 = 17 for its lane
tests and 3 for the cursor; 21 for 4 for the base of its partner pairs (((g <<
2) + g) << 1 plus the base), 2 for the cursor, 3 for the opened count in its
register and its test, 4 for the jump in and the return and 8 for control, the
5 units of the cluster index g = 7 I + lane with I = (p - base) >> 1 among them,
with no frame (above); and 6 for the representative's T2 and its test (answers
CJ 2 to 5). The opened count is paid before the
partner batches, so the run charges A_BUDGET + 1 opened clusters, the one
that halts included. A passing lane saves and reloads the 29 words of 9.8,
the operand -(A >> 16) mod 128, P_q and the key among them, and the eight
reserved registers above, at 4 units each with the addresses, and is charged
494 in a representative or a partner batch. Through a batch at most 31 registers are live, and at most 39 in a Q
path. The table P is built once: for each of its 2^21 keys, at most 64 units
to take the key apart, form both sums, compare them with the ends of the two
intervals of S7, store the entry at its index and loop, 2^27 in all; and
2^20 more covers the labels of the gate, the frame and its initialisation,
and four more 2^20 the changes of answers CJ 2 to 5.

*The rows of the table.* For 0 <= q, c < 128 let T_qc be the set of a with P[a +
128 c + 16,384 q] = 1, G(q, c) = |T_qc| / 128, h_qc(z) = |T_qc intersected with
{z, z + 1, .., z + 15}| (residues modulo 128) and B(q, c) the largest value of
the sum over j = 0 to 7 of max(h_qc(o + 16 j), h_qc(o + 16 j + d)), over 0 <= o
< 16 and the odd d modulo 128, divided by 128. The exhaustive check

    S7 = set(range(0x25, 0x3f)) | set(range(0x45, 0x5f))
    G, B = [], []
    for q in range(128):
        for c in range(128):
            T = [((a ^ q) + c) % 128 in S7
                 or ((((a - 1) % 128) ^ q) + c) % 128 in S7
                 for a in range(128)]
            h = [sum(T[(z + k) % 128] for k in range(16))
                 for z in range(128)]
            G.append(sum(T))
            B.append(max(sum(max(h[o + 16 * j], h[(o + 16 * j + d) % 128])
                             for j in range(8))
                         for o in range(16) for d in range(1, 128, 2)))
    print(sum(G), sum(B), min(2 * b - g for g, b in zip(G, B)))

prints 940000 1791200 140 (GPT Sol, answer CK 5.2; the participant reproduced
the sums and the whole histogram of B, from 98 to 120 over the 16,384 rows). So
for (q, c) uniform on its 16,384 values E[G] = 940,000 / 2^21 = 29,375 / 65,536
and E[B - G] = 851,200 / 2^21 = 3,325 / 8,192, and 2B - G >= 140 / 128 > 1 in
every row.

**Lemma OR (the opening rate of the gate).** Let the seven outer words of a
context be independent and uniform, as in a run (Lemma CX (a)), and fix a
representative, its word e = e1 with bits 10 to 14 zero. Then the gate entry
P[a + 128 c + 16,384 q] of its cluster (Lemma CL) is 1 with probability at most

    p* = 246,621,675 / 2^29 = 0.45936866663... < 0.4593686667.

Hence the number A(C) of clusters of a context whose gate entry is 1 has E[A(C)]
<= 16,384 p* = 246,621,675 / 2^15 = 7,526.29623...; no independence between the
clusters of a context is used.

*Proof.* Write b = C0.b1, H = w6 + w2 and Z = S0 + S5; X3, X7, X15, W13 and the
IV are constants.

(a) *A chart.* The lines of step CO (Section 8) recover the seven outer words
from (b, H, D2.b1, S15, w6, S4, D2.a1): w6 gives K3.a1, K3.d1, K3.c1 and K3.b1,
and S11 = S15 + K3.c1; then S3, D3.a1 = S3 + S4, D3.b1 and D3.c1; with D2.a1
and D2.b1 also X2, X8, S7, D2.c1, X13, D2.d1, S13 and S8; w2 = H - w6, K1.a1 =
w2 + IV[1] + IV[5], K1.d1 = ROR(K1.a1, 16), K1.c1 = K1.d1 + IV[1] and S9 =
K1.c1 + S13; then D3.d1 = D3.c1 - S9, X14 = ROR(D3.d1 XOR X3, 8), X9 = X14 +
D3.c1 and X4 = ROR(D3.b1 XOR X9, 7); last C0.c1 = X4 XOR ROL(b, 12) and C0.d1 =
C0.c1 - X8. So the map from the seven outer words to these seven words is
one-to-one on 2^224 values, a bijection, and the seven new words are
independent and uniform. The same lines give X4, X8 = ROL(X7, 7) XOR D2.b1,
S15, H, S5 = ROR(K1.b1 XOR S9, 7) and S0 (from S8, S4 and the lines of K0)
without b. So b is uniform and independent of (X4, X8, H, S15, Z), and C0.c1 =
X4 XOR ROL(b, 12), C0.d1 = C0.c1 - X8 and A = b + X4 + H.

(b) *The law of the key.* By Lemma CL, q = (ROL(X15, 24) XOR S15) mod 128 and c
= (e - Z) mod 128. Fix (H, D2.b1, S15, w6, D2.a1); by (a) S8 and S5 are fixed.
Put z = K0.c1 = ROL(ROL(S4, 7) XOR S8, 12) XOR IV[4], a bijective function of
S4; the lines of K0 give S0 = ROL(S8 - z, 8) XOR (z - IV[0]), so S0 mod 128 is
bits 24 to 30 of S8 - z XOR the low seven bits of z - IV[0]. Write z - IV[0] =
z_0 + 128 m with z_0 < 128: for fixed z_0, as m runs over its 2^25 values, S8 -
z = (S8 - IV[0] - z_0) - 128 m runs over the 2^25 words with fixed low seven
bits, whose bits 24 to 30 take each value 2^18 times. So S0 mod 128, and with it
Z mod 128, is uniform given the five fixed words, and (S15 mod 128, D2.b1 mod 8,
Z mod 128) is uniform on its 2^17 values. Hence (q, c, X8 mod 8) is uniform.

(c) *The window.* Fix (X4, X8, H, S15, Z), which fixes q and c, and write b =
b_0 + 2^16 t with 0 <= t < 128 and bits 16 to 22 of b_0 zero; by (a) the 25
bits of b_0 and the 7 of t are independent and uniform. With y = e - Y3 and r
= ROL(y, 7) XOR b, the lines Y8, Y12 and Y0 give p = ROL(r - C0.c1, 8) XOR
C0.d1, so the window w = (p >> 16) mod 128 is bits 8 to 14 of r - C0.c1 XOR
bits 16 to 22 of C0.d1 = C0.c1 - X8. Bit i of b is bit i + 12 mod 32 of C0.c1:
t sets bits 16 to 22 of r and bits 28 to 31 and 0 to 2 of C0.c1, and C0.c1 mod
8 runs over its 8 values as t does. So t changes w only through two borrows:
into bit 8 of r - C0.c1, the comparison of r mod 2^8 with C0.c1 mod 2^8, and
into bit 16 of C0.c1 - X8, the comparison of C0.c1 mod 2^16 with X8 mod 2^16.
As the low three bits of C0.c1 run over 0 to 7 with its other bits fixed, the
first is not constant exactly on E1: bits 3 to 7 of r and of C0.c1 agree and r
mod 8 < 7; the second exactly on E2: bits 3 to 15 of C0.c1 and of X8 agree and
X8 mod 8 != 0. E1 reads bits 0 to 7 of b (in r) and 23 to 27 (bits 3 to 7 of
C0.c1), so Pr(E1) = (1/32)(7/8) = 7/256; E2 reads the 13 bits 23 to 31 and 0
to 3 of b, so Pr(E2) = [X8 mod 8 != 0] / 8,192. Both are events on b_0.

(d) *The count over t.* A = A_0 + 2^16 t with A_0 = b_0 + X4 + H, so a = (w -
(A_0 >> 16) - t) mod 128. Write t = 16 j + i with 0 <= j < 8 and 0 <= i < 16.
The four bits of i are bits 16 to 19 of b; they set bits 16 to 19 of r and bits
28 to 31 of C0.c1, which neither borrow of (c) reads and which do not enter bits
8 to 14 of r - C0.c1 or bits 16 to 22 of C0.d1, so w depends on t only through
j, on E1 and E2 as well (answer CK 5.1). Let w be the window when neither borrow
occurs, and n_0 = w - (A_0 >> 16). For block j, as i runs over 0 to 15, n_0 - t
runs over the 16 consecutive residues z_j to z_j + 15 with z_j = n_0 - 16 j - 15
mod 128, and these eight blocks partition the residues: z_j = o + 16 j' for one
alignment o < 16 and j' running over 0 to 7. Without E1 and E2, a = n_0 - t
takes each value once, and the gate opens for exactly |T_qc| values of t. With
exactly one of them, the window of block j is w or w + d, with d odd and the
same for all j (the two values n XOR f and ((n - 1) mod 128) XOR f for fixed n
and f, which differ in bit 0), and it is the same for the 16 values of i; so
block j opens for h_qc(z_j) or h_qc(z_j + d) values of t, and the gate opens for
at most the sum over j of max(h_qc(o + 16 j), h_qc(o + 16 j + d)) <= 128 B(q, c)
values of t. With both, it opens for at most 128. Since 2B - G >= 1, in every
case the share of t that open is at most G + (B - G)([E1] + [E2]).

(e) *The mean.* Averaging (d) over b_0 with (c), the gate opens, given (X4, X8,
H, S15, Z), with probability at most G(q, c) + (B - G)(q, c) (7/256 + [X8 mod 8
!= 0] / 8,192), a function of (q, c, X8 mod 8). By (b) this triple is uniform,
so the probability is at most E[G] + E[B - G] (7/256 + (7/8) / 8,192) = 29,375 /
65,536 + (3,325 / 8,192)(1,799 / 65,536) = (1,925,120,000 + 47,853,400) / 2^32 =
p*. This holds for each of the 16,384 representatives, and E[A(C)] is the sum of
their probabilities. QED. As a check, not used here, a participant sample of
2^32 clusters, each on a fresh context, found the gate open on 0.448220 of them,
and the program of 6.4 opened 0.4435 of 131,072 clusters (Section 13). The
finite verification of B, 2^24 candidates (q, c, o, d) of eight interval maxima
each, is charged 2^34 once (Section 11).

*The budget (GPT Sol, answers CJ 1.2 and CK 9).* With s = ceil(sqrt(10 *
RUN_CONTEXTS)) = 110,495,547, the run halts with failure when the opened count
exceeds

    A_BUDGET = ceil(246,621,675 * RUN_CONTEXTS / 2^15) + 16,384 * s
             = 9,189,055,127,318,993,733 + 1,810,359,042,048
             = 9,189,056,937,678,035,781.

The A(C) of the contexts of a run are independent and identically distributed,
each between 0 and 16,384 (Lemma CX (a)); by Lemma OR their total has mean at
most 246,621,675 * RUN_CONTEXTS / 2^15, and it bounds the opened count of the
run. Hoeffding's inequality puts the probability that the opened count exceeds
A_BUDGET at most exp(-2 (16,384 s)^2 / (RUN_CONTEXTS * 16,384^2)) = exp(-2 s^2 /
RUN_CONTEXTS) <= exp(-20) < 2.1 * 10^-9. No premise enters: the budget bears on
the success probability alone (10.4), and the time bound charges A_BUDGET + 1
opened clusters whatever the words.

## 10. The rate of a counter trial and the success probability

**10.1 The model rate.** The seven-word model M of Section 13 treats the
residual of a trial as a function of seven words, E1.d1, E1.b1 and E1.a2 of
message A and Y4, Y9, w8 and E3.h1. In this package Y4 is uniform in the class
of eta, not in the sub-class, and the other six are independent uniform words,
so M has 2^192 * 2^19 = 2^211 inputs. Under M the rate of the class is
85074516985129 / 524288 = 162,266,763.66 (Section 13): a trial has R = 0 with
probability that number times 2^-128. The part of a value beta of E1's
first-half b difference in it is written r(beta); the part of beta* is
71,698,432, and the part of the six outcomes of S that this search lists (below)
is 67,633,152. A trial of Section 8 has c1 in Q* and so the difference beta*
(Theorem C (iv)); under M the event that c1 = Y11 + E1.d1 lies in Q* has
probability 2^-11 and is the event that the difference is beta* (Lemma S1). The
rate at which a trial that M conditions on c1 in Q* has R = 0 with an outcome of
S is therefore

    p = 2^11 * 67,633,152 * 2^-128 = 138,512,695,296 * 2^-128 = 1,032 * 2^-101,

about 2^-90.989. It is 853.61 = 2^9.738 times the model rate of a trial of the
class.

*The outcomes of beta*.* In the count of Section 13 an outcome of beta
is a pair (tau, eps) of the differences of E1's a and c outputs. For an outcome
j of beta*, L_j is the number of triples (E1.c1, E1.b1, E1.a2) of words for
which E1 on A and on B (6.2) gives the differences beta*, tau_j and eps_j; and
N3_j is the number N3 of step 3 of the count for that outcome: the number of
quadruples (Y4, E3.h1, Y9, w8), Y4 in the class, for which E3 on A and on B
gives the differences eta and tau_j XOR ROR(tau_j, 1) of its first-half d and b
values and tau_j and eps_j of its c and a outputs. Every input of the 2^211 of
the model falls into one outcome, so r(beta*) = sum over j of L_j N3_j / 2^83.
Beta* has fourteen outcomes on the class, all with eps = 6e21be55; this search
lists the six of S, j = 1 to 5 and 7:

| j | tau | L_j | N3_j | L_j * N3_j / 2^83 |
| ---: | --- | ---: | ---: | ---: |
| 1 | 175020a0 | 562,949,953,421,312 | 108,086,391,056,891,904 | 6,291,456 |
| 2 | 185020a0 | 2,251,799,813,685,248 | 72,057,594,037,927,936 | 16,777,216 |
| 3 | 275020a0 | 562,949,953,421,312 | 18,014,398,509,481,984 | 1,048,576 |
| 4 | 285020a0 | 2,251,799,813,685,248 | 108,086,391,056,891,904 | 25,165,824 |
| 5 | 385020a0 | 1,125,899,906,842,624 | 144,115,188,075,855,872 | 16,777,216 |
| 6 | 675020a0 | 140,737,488,355,328 | 4,503,599,627,370,496 | 65,536 |
| 7 | 685020a0 | 562,949,953,421,312 | 27,021,597,764,222,976 | 1,572,864 |
| 8 | 175060a0 | 281,474,976,710,656 | 6,755,399,441,055,744 | 196,608 |
| 9 | 185060a0 | 1,125,899,906,842,624 | 9,007,199,254,740,992 | 1,048,576 |
| 10 | 275060a0 | 281,474,976,710,656 | 1,125,899,906,842,624 | 32,768 |
| 11 | 285060a0 | 1,125,899,906,842,624 | 13,510,798,882,111,488 | 1,572,864 |
| 12 | 385060a0 | 562,949,953,421,312 | 18,014,398,509,481,984 | 1,048,576 |
| 13 | 675060a0 | 70,368,744,177,664 | 281,474,976,710,656 | 2,048 |
| 14 | 685060a0 | 281,474,976,710,656 | 3,377,699,720,527,872 | 98,304 |
| sum, S: j = 1 to 5 and 7 (listed) | | | | 67,633,152 |
| sum, j = 1 to 7 (the seven of the program) | | | | 67,698,688 |
| sum, all fourteen | | | | 71,698,432 |

The rows j = 1 to 7 have the L_j of the sub-class of entry 26ebba63 and four
times its N3_j, so on this scale they carry exactly its 67,698,688 = 1,033 *
2^16. S leaves out row 6, 675020a0, with 65,536 = 2^16, and carries 67,633,152 =
1,032 * 2^16, so p = 1,032 * 2^-101 exactly; the rows j = 8 to 14, with bit 14
of tau set, add 3,999,744, 5.6 per cent of the part of beta*, and are not listed
either. The integers L_j and N3_j are those of the participant's counting
program, printed in Section 17 with the six rows of its output that this search
lists; it prints L_j N3_j / 2^81, four times the last column, and the six listed
rows sum to 270,532,608 = 4 * 67,633,152 there, and the scale 2^83 is that of a
trial with Y4 uniform in the 2^19 members of the class (GPT Sol, answer AQ 3).
Of the 52 values of tau that pass the screens of the count, 30 have N3_j > 0 and
14 have L_j N3_j > 0. The count uses no rule on h1.

*Why S.* S = 5f is part of the stated advice record of Section 12, and what the
analysis uses of it is verified here: its count, 67,633,152 = 1,032 * 2^16 (the
table above, Section 17), its certificate with SHARE and E_COUNT (Section 8) and
its charge (Section 11). It is not claimed to be least under Section 11; step 3
of SEL (Section 12) chose it under the ledger of entry 415e792c (GPT Sol, answer
AW 4).

*Why beta*.* Beta* = 18b0e098 is a value of the stated advice record, and what
the analysis uses of it is verified here: its cube of c1, k = 11 fixed bits,
mask 0e09818b and value 02008000 (Theorem C (iii) and (iv)), and its fourteen
outcomes on the class with their counts (the table above). It is the beta of the
solution with which the solver found the six constants. The program of 6.4
stores beta* and the mask and value of its cube.

**10.2 Lemmas on the counter sampler (GPT Sol 6.1).** The following lemmas were
proved by GPT Sol 6.1 for this construction, Lemma S9 by GPT Sol in its answer
AC, and are given with their hypotheses; each is exact mathematics under the
hypotheses stated. The
participant compared Lemmas S1 to S4 and Lemma IP with the construction line by
line; the carry Lemmas S5 to S7 were not re-derived by the participant. They do
not prove the rate of H1' or the success probability; 10.3 states what remains
a premise. The proofs of Lemmas S1 and S9 hold for any fixed set of members
(GPT Sol, answer AN 1); here the set is the class.

**Lemma S1 (conditioning the model).** *Hypotheses:* under M the six words
E1.d1, E1.b1, E1.a2, Y9, w8 and E3.h1 are independent uniform words, independent
of Y4, which is uniform in the class; c1 = Y11 + E1.d1. *Statement:* c1 lies in
Q* with probability 2^-11, and that is the event that E1's first-half b
difference is beta*. Conditional on it, E1.d1 is uniform on Q* - Y11, E1.b1 and
E1.a2 keep their independent uniform laws, and (Y4, Y9, w8, E3.h1) keeps its law
and stays independent of (E1.d1, E1.b1, E1.a2). Hence, with G_S the event that R
= 0 with an outcome of S, Pr_M(G_S | c1 in Q*) = 2^11 Pr_M(G_S and c1 in Q*) =
2^11 * 67,633,152 * 2^-128 = p, the last step by the count of 10.1.

*Proof.* Translation by Y11 makes c1 uniform and independent of every other
coordinate. By the identity of the proof of Theorem C (iv), c1 lies in Q*
exactly when the difference is beta*, and Q* fixes 11 bits of c1, so the
probability is 2^-11. The event depends on E1.d1 alone, so for every event G1
of the words of E1 and G3 of the words of E3, Pr_M(G1 and G3 | c1 in Q*) =
Pr_M(G1 | c1 in Q*) Pr_M(G3). No independence of the output differences inside
E1 or inside E3 is used. QED. The finite counts behind 67,633,152 are those of
the counting program of Section 17 and are not proved by this lemma.

**Lemma S2 (the outer chart).** *Hypotheses:* y and c1 are fixed; the seven
outer words are independent uniform words; the names obey the assignments of
step CO, with flags 3 and v[13] = 0. *Statement:* the seven outer words are in
bijection with the seven context words (C0.c1, C0.d1, D3.d1, S15, S9, w5, X2)
of Section 4. These are therefore independent uniform words, and their law does
not depend on c1 or y.

*Proof.* Given the context words, these assignments, which are lines of steps O
and M of Section 4 with flags 3 in place of 11, return the outer words: S2 =
K2.a1 + K2.b1 + w5; S14 = ROR(K2.d1 XOR S2, 8); D3.a1 = ROL(D3.d1,16) XOR S14;
D3.b1 = X3 - D3.a1; D3.c1 = S9 + D3.d1; S4 = ROL(D3.b1,12) XOR D3.c1; S3 =
D3.a1 - S4; X14 = ROR(D3.d1 XOR X3, 8); X9 = D3.c1 + X14; K3.d1 = ROL(S15,8)
XOR S3; w6 = (ROL(K3.d1,16) XOR 3) - IV[3] - IV[7]; S11 = IV[3] + K3.d1 + S15;
X8 = C0.c1 - C0.d1; D2.b1 = ROL(X7,7) XOR X8; D2.a1 = X2 - D2.b1 - W13.
Substituted into K2, D3, K3 and D2 they return w5, D3.d1, S9, S15, X2, C0.c1
and C0.d1, and the lines of step CO, run on the outer words they return, give
the context words back. Both maps are inverse bijections between two sets of
2^224 elements, and the uniform law is carried to the uniform law. QED.

**Lemma S3 (two independent offsets).** *Hypotheses:* those of Lemma S2.
*Statement:* (w5, D3.a1, Y12, S15, X2, X8, C0.d1) is another chart of the outer
words, so these seven are independent uniform words; in particular Y12 and w5,
which E1 reads, are independent uniform words.

*Proof.* The chart is reached by replacements of coordinates, each a bijection
with the other coordinates held fixed: (w6, S11) by (S3, S15), with inverse
K3.d1 = ROL(S15,8) XOR S3, w6 = (ROL(K3.d1,16) XOR 3) - IV[3] - IV[7], S11 =
IV[3] + K3.d1 + S15; (D2.a1, D2.b1) by (X2, X8), with D2.b1 = ROL(X7,7) XOR X8
and D2.a1 = X2 - D2.b1 - W13; (S3, S4, X9) by (D3.a1, S4, S14), with inverse
D3.b1 = X3 - D3.a1, D3.d1 = ROR(S14 XOR D3.a1, 16), X14 = ROR(D3.d1 XOR X3, 8),
D3.c1 = ROL(D3.b1,12) XOR S4, X9 = D3.c1 + X14, S3 = D3.a1 - S4; S14 by w5,
with S2 = K2.a1 + K2.b1 + w5 and S14 = ROR(K2.d1 XOR S2, 8); at fixed D3.a1 and
S14, S4 by X4, with inverse X9 = ROL(X4,7) XOR D3.b1, D3.c1 = X9 - X14, S4 =
ROL(D3.b1,12) XOR D3.c1; and last, with C0.c1 = X8 + C0.d1, X4 by Y12, with
C0.b1 = (Y12 + C0.c1) XOR ROL(y,7) and X4 = ROL(C0.b1,12) XOR C0.c1. The
composition proves the chart and the uniform law. It says nothing about the
independence of Y12 and w5 from functions that also depend on them, such as the
residual. QED.

**Lemma S4 (a marginal and the physical conditioning).** *Hypotheses:* those of
Lemmas S2 and S3, and c1 independent of the outer words. *Statement:* (a) At
each fixed c1 and y, E1.a1 and E1.a2 - E1.b1 are independent uniform words. (b)
For two members c1 and c1' of Q* in one outer step, put m4 = ROL((c1 - Y11) XOR
(c1' - Y11), 16); then the difference of their values of E1.a2 - E1.b1 is m4 -
2 (E1.a1 AND m4), E1.a1 being that of c1, and conditional only on the value of
E1.a2 - E1.b1 at c1 it is uniform on the values m4 - 2 s, s a submask of m4 AND
7fffffff, which are all different. (c) Let a baseline sampler draw t as a
uniform 32-bit word, t = 0 included as an algebraic trace, with flags 3, the
same constants and the same outer words, and solve c1 from it; then c1 is
uniform and independent of the outer words and y, and the sampler of Section 8,
c1 uniform in Q*, is exactly the baseline conditioned on c1 in Q*: for every
event of the trace, its probability under the sampler of Section 8 is 2^11
times the probability under the baseline that it happens and c1 lies in Q*.

*Proof.* (a) By Lemma S3, Y12 and w5 are independent uniform, so E1.a1 =
ROL(E1.d1,16) XOR Y12 and w5 are, and E1.a2 - E1.b1 = E1.a1 + w5 by E1's fifth
assignment; replacing (E1.a1, w5) by (E1.a1, E1.a1 + w5) is a bijection. (b)
The same outer words give c1' the first value E1.a1 XOR m4 and the same w5, and
(X XOR m4) - X = m4 - 2 (X AND m4) modulo 2^32. Conditional on the first value,
E1.a1 stays uniform, its bits under m4 AND 7fffffff give the uniform law
stated, and different submasks below 2^31 have different doubles. (c) By Lemma
IP, c1 -> t is a permutation for every outer step and y, so a uniform t makes
c1 uniform and independent of them; conditioning on c1 in Q*, an event of
probability 2^-11, leaves the outer words and y unchanged, and step CT run
forwards from c1 is the same trace. QED. Statement (c) is about the
construction's own sampler and does not identify it with M; it lets an event
include t != 0 but does not say how much of the rare success mass the rule t !=
0 removes.

**Lemma S5 (a carry prescription).** *Statement:* let x, s, s', a and d be
words of w bits with (x + s) XOR ((x XOR a) + s') = d. Every bit i < w - 1 at
which a and d differ is determined by the lower bits of x and by the constants;
so at most 2^(w - n1) words x solve the equation, n1 being the number of bits
of (a XOR d) AND (2^(w - 1) - 1).

*Proof.* Write u_i and u'_i for the carries into bit i of the two additions.
Equality at bit i gives a_i XOR d_i = s_i XOR s'_i XOR u_i XOR u'_i. If its
left side is 1, exactly one of the pairs (s_i, u_i) and (s'_i, u'_i) has
unequal bits; the carry out of that addition is its variable input bit, x_i or
x_i XOR a_i, and the carry out of the other addition is its fixed common bit.
Equality at bit i + 1 prescribes the XOR of the two carries out, which fixes
x_i. Counting the choices from the low bits to the high bits gives the bound;
bit w - 1 has no next bit, which is why it is left out. QED.

**Lemmas S6 and S7 of entry 26ebba63**, an E3 prescription and a cap of 3,072
complete successes in one outer step, are stated for the sub-class with rule A
and its seven outcomes, and this package does not use them. Its cap on the
successes of one outer step is that of 9.4 with Lemmas G7, G15 and CV: at most
16 listed good trials (10.3).

**Lemma S8 (success from a mean and a factorial moment).** *Statement:* let N_o
be a count with values in {0, 1, ..}, mu = E[N_o] > 0 and rho = E[N_o (N_o -
1)] / mu. Then Pr(N_o > 0) >= mu b(rho), where b(rho) = (2 r_o - rho) / (r_o
(r_o + 1)) and r_o = floor(rho) + 1; for 0 <= rho <= 1 this is 1 - rho / 2, and
b decreases with rho. If the outer steps of a run are independent and each has
mean at least mu and ratio at most rho, the probability that some outer step
has N_o > 0 is at least 1 - exp(-mu b(rho) times the number of outer steps).

*Proof.* For integers r_o >= 1 and z >= 0, the indicator of z > 0 is at least
(2 r_o z - z (z - 1)) / (r_o (r_o + 1)): with equality at z = 0, and for z >= 1
the inequality is (z - r_o)(z - r_o - 1) >= 0, which holds for integers. Taking
expectations gives the first statement. For independent outer steps, the
probability that none has N_o > 0 is the product of the values 1 - Pr(N_o > 0)
of the outer steps, at most exp(-mu b(rho) times their number). QED. The proof
uses only that the units are independent and that each count takes values in
{0, 1, ..}; it holds as well for the contexts of 9.8, with the count N_c of a
context in place of N_o (10.3).

**Lemma S9 (the success mass lies on passing outer steps; GPT Sol, answer AC).**
(a) *No hypothesis.* In every outer step that does not pass the filter, the
count N_o of H1' (10.3) is zero. Let pi_o be the probability that an outer step
of step 1 of 9.1 passes the filter, the share of the 2^256 values of its random
word whose outer step passes. If pi_o > 0, then E[N_o | the outer step passes] =
E[N_o] / pi_o. (b) *Hypotheses:* those of Lemma S1. Under M, also conditional on
c1 in Q*, Y9 and omega = Y3 + Y4 + w8 are independent uniform words, and the
filter passes with probability pi. G_S, the event that R = 0 and the E1 outcome
is in S, has probability p under M given c1 in Q* (Lemma S1 and the count of
10.1), and it lies inside the event that the filter passes. So Pr_M(G_S | c1 in
Q* and the filter passes) = p / pi = 1,032 / (279,070,422,111 * 2^53), about
2^-81.011, and Pr_M(the filter passes | c1 in Q*) times this conditional rate is
p: conditioning on the pass loses no part of p.

*Proof.* (a) A listed good trial has R = 0 with an outcome of S, so by Lemma F
its outer step passes; N_o is a count that is zero off the event that the outer
step passes, and E[N_o] = pi_o E[N_o | the outer step passes]. (b) Under M, Y9
and w8 are independent uniform words, independent of Y4; for fixed Y4, w8 ->
omega is a translation, so (Y9, omega) is uniform on all 2^64 pairs and
independent of Y4, and Lemma S1 leaves the law of (Y4, Y9, w8, E3.h1) unchanged
under c1 in Q*. The proof of Lemma F uses only the assignments of E3 and the
conditions of R = 0, which hold for the model words, so it gives the inclusion;
by 10.1 p is the part of the outcomes of S. Dividing by the probability pi of
the pass gives the conditional rate. QED. Statement (a) uses the pass
probability pi_o of the sampler itself; that pi_o equals pi is not proved (H4').
Statement (b) is about M and says nothing about the sampler.

*The search lists exactly the listed good trials.* The two lemmas below concern
the search of 9.1. Lemma V follows from 3.3 and is the participant's; Lemma CV
rests on the constants and guards of 9.4, proved by GPT Sol (answers AE 4 and
7, AF 1.3, AO 6.1 and AR 1, 2 and 6.1), among them the parity certificate (P*)
and Lemma J0, which hold for every joint root on the class.

**Lemma V (the certificate of a root).** Fix an outer step, a word c1 in Q* and
an outcome j of beta*, and let h be E3.h1 of the trial. The trial has R = 0
with E1 outcome j exactly when E1 on A and on B gives the XOR differences tau_j
and eps = 6e21be55 of its a and c outputs and h satisfies the joint conditions
(J1), (J2) and (J3) of outcome j (9.4).

*Proof.* Write tau, eps and beta for the XOR differences between A and B of
E1's a output, c output and first-half b value, and eta, psi, tau' and eps'
for those of E3's first-half d and b values and its c and a outputs, as in
Section 13. beta = beta* because c1 is in Q* (Theorem C (iv)), and eta =
830303cf (Theorem C (iii)). By 3.3, R is formed from o[1] = Z[1] XOR Z[9],
o[3] = Z[3] XOR Z[11], o[4] = Z[4] XOR Z[12] and o[6] = Z[6] XOR Z[14],
where Z[1], Z[6], Z[11] and Z[12] are the a, b, c and d outputs of E1 and
Z[3], Z[4], Z[9] and Z[14] those of E3. The first two values of E1 are the
same for A and B (proof of Theorem C (iv)), so the d and b outputs of E1
differ by ROR(tau, 8) and ROR(beta XOR eps, 7); by the last three
assignments of E3, its b and d outputs differ by ROR(psi XOR tau', 7) and
ROR(eta XOR eps', 8). So R = 0 exactly when tau' = tau, eps' = eps, psi =
tau XOR ROR(tau, 1) and eta = eps XOR ROL(beta XOR eps, 1), the conditions
of Section 13. For E1 outcome j, tau = tau_j and eps = 6e21be55, and the
last condition holds: 6e21be55 XOR ROL(18b0e098 XOR 6e21be55, 1) = 830303cf.
As in the proof of Lemma F, with h' = h XOR eta, g' = Y9 + h' and f' = ROR(y
XOR g', 12), psi = f XOR f' = ROR(g XOR g', 12), so psi = sigma_j exactly
when (J1) holds. Then f' = f XOR sigma_j and the a output of E3 on B is
(omega + DY3) + f', so eps' = eps exactly when (J2) holds. Then the d output
of E3 on B is ROR(h XOR eta XOR e2 XOR eps, 8) = h2 XOR mu and g' = g XOR
theta_j, so tau' = tau_j exactly when (J3) holds. QED.

**Lemma RC (the root certificate; GPT Sol, answers CF 6 and 6.1).** Fix an outer
step, an outcome j of S and a word h, and let c1 be the word that step 3 of 9.1
computes from h, that of the trial with E3.h1 = h (Lemma IP). The four tests
(Q), (A), (C) and (T) of step 3 hold exactly when c1 is in Q*, t is not zero,
and E1 on A and on B (6.2) gives the XOR differences tau_j and eps = 6e21be55 of
its a and c outputs.

*Proof.* The lines of step 3 are those of step CT read backwards from E3.h1 = h,
so they give the trial's Y14, Y6, E1.a1, E1.d1, c1, E1.b1, E1.a2 and t. (Q) is
the definition of Q*, and (T) is t != 0. Suppose (Q), and write a1, d1, c1, b1,
a2, d2, c2 for the assignments of E1 on A and primes for B (6.2). E1 on B has
the same a, b and d inputs and the same first message word, so a1' = a1 and d1'
= d1; its c input is Y11' = Y11 + DY11, so c1' = c1 + DY11; and b1' = b1 XOR
beta* (Theorem C (iv)), which is b1 + beta* - 2 s with s = b1 AND beta*. With
its second message word w5 + fffffff8, a2' = a2 + Delta(s), Delta(s) = beta* - 2
s - 8 (as in 9.7). Now a2 XOR a2' = tau_j exactly when a2 + Delta(s) = a2 XOR
tau_j, that is when Delta(s) = (a2 XOR tau_j) - a2 = tau_j - 2 (a2 AND tau_j)
modulo 2^32, that is when 2 (a2 AND tau_j) = (tau_j - Delta(s)) mod 2^32. Since
tau_j[31] = 0, 2 (a2 AND tau_j) is below 2^32, and tau_j - Delta(s) = tau_j -
beta* + 8 + 2 s is even, as tau_j and beta* are; so this is (A). Given (A), a2'
= a2 XOR tau_j, so d2 = ROR(d1 XOR a2, 8) = z and d2' = ROR(d1 XOR a2', 8) = z
XOR ROR(tau_j, 8); with c2 = c1 + d2 and c2' = c1' + d2', c2 XOR c2' = eps is
(C). The same identities give (A) and (C) back from the two differences when c1
is in Q*. QED. The lemma uses no law of the words; with Lemma V it says that a
root is certified exactly when it is the E3.h1 of a listed good trial of outcome
j.

**Lemma CV (coverage of the search).** Fix an outer step that passes the filter,
with T = X AND VMASK[nu] of 9.7. (a) When T is not empty, step 2 of 9.1 returns
every joint root that satisfies (G7) and (G15) of every outcome whose bit is set
in T, each once, and nothing else. (b) Run over the whole list, step 3 certifies
exactly the roots that are the E3.h1 of a listed good trial of the outer step,
and the E3.h1 of every listed good trial of the outer step is among the roots;
when T is empty the outer step holds no listed good trial (Lemma VP). Hence a
passing outer step has as many certified roots as its count N_o of H1' (10.3),
the number of its listed good valid trials over all of Q* (none when T is
empty), and N_o <= 16.

*Proof.* (a) A leaf yields a root only if (J1), (J2) and (J3) hold as words, so
each returned word is a joint root of the outcome with which it is returned.
Conversely, take a joint root h of a searched outcome, with h satisfying (G7)
and (G15). By (PHASE), (P*), Lemma J0, the guards (G7) and (G15) and the
constants and guards of 9.4 its bits take those values, and its carries pass
every test of (a), (b) and (e) there: its own carry into bit 20 is a kept guess,
every kept guess reaches the common state at depth 7, and the single traversal
follows the arcs of its bits from the carry pairs that its own carries give,
each read from the array of its position with the guard values that its own bits
give (at position 15 its prefix passes the test of (G15) and the prescribed bit
is its h[15]), and reaches its leaf, where the three conditions hold. A
depth-first traversal reaches each node once, so h is returned once. No word is
a joint root of two outcomes (9.4). (b) Let c1 in Q* give a listed good trial
with outcome j, and let h be its E3.h1. By the proof of Lemma F, h witnesses
(1)_j for Y9 and the trial's f witnesses (2)_j for omega, so bit j - 1 is set in
both masks, and by Lemma VP it is set in T; in particular T is not empty. By
Lemma V, h satisfies (J1) to (J3) of outcome j, so it is a joint root; Lemmas G7
and G15 give (G7) and (G15) for it, and by (a) step 2 returns it. Step 3 maps it
to c1, since it computes the inverse of the permutation c1 -> E3.h1 of Lemma IP;
c1 is in Q*, its t is not zero and its E1 outcome is j, so the root is certified
(Lemma RC). Conversely, by Lemma RC a certified root h of outcome j gives a c1
in Q* with t not zero whose E1 differences are tau_j and eps, and h satisfies
(J1) to (J3), so by Lemma V the trial of c1 has R = 0 with outcome j: it is a
listed good trial. Different roots give different c1 (Lemma IP), and no outer
step has more than 16 roots (9.4). QED.

So in every passing outer step that it reaches, the search of 9.1 certifies
precisely the listed good valid trials that an enumeration of all of Q* in that
outer step finds, with the same outer steps, the same members y and the same
filter. The count N_o of every outer step is the same, and with it the joint law
of the counts of the outer steps of a run: H1' is about these counts, H4' about
two counts of the outer steps and H5' about the caps C(T) of the outcomes that
the pre-check keeps, and none of them changes (GPT Sol, answers AE 7 and AW 1
and 5). No law of the words is used by Lemmas V, RC, VP, G7, G15 and CV. The
guards of the solver are lossless: (PHASE) and (P*) are consequences of exact
counts of the class, (P*) with a count of 0 for the other parity in every phase
and every outcome (9.4), and Lemma J0 is algebra; none drops a member or a joint
root. The pre-check and the guards (G7) and (G15) lose no listed good trial
(Lemmas VP, G7 and G15), and walking the outer steps by contexts changes no
outer step (Lemmas CX and MB).

**10.3 Heuristics.**

The three premises H1', H4' and H5' below concern the instance that the stated
advice record of Section 12 fixes: the six constants of 3.2, eta = 830303cf,
beta* = 18b0e098 with its cube, the outcomes of beta* with the filter's values
of tau and eps, and S = 5f. Each is a statement about the run for this record
and for no other, and none concerns how the record was found. No premise
concerns how the record was found: the selection procedure SEL that found it is
charged in full as preprocessing, with a cap that holds by construction (Section
12).

**Heuristic H1' (score-critical).** The coins of the run are its RUN_CONTEXTS
independent fresh words (step 1 of 9.1); each gives the seven outer words of one
context, and every context walks all 2^19 members of the class, except those of
clusters that hold no listed good trial (9.8, 9.9, Lemmas CX and CL). Let N_o be
the number of listed good valid trials (9.1) of one outer step, counted over all
of Q* whether or not the outer step passes the filter or the pre-check, and let
N_c be the sum of N_o over the 2^19 outer steps of a context. (i) *Rate:* for a
uniform outer step U, whose seven outer words are uniform and whose member is
uniform on the class, independently (the outer step of entry 415e792c),
E[N_o(U)] >= (2^21 - 1) q, with q = FACTOR * 2^-128, just under 10p / 11, about
2^-91.126; by Lemma CX (c), E[N_c] = 2^19 E[N_o(U)]. (ii) *Dependence, with the
context as the unit:* the probability that no valid trial of the run is a listed
good trial is at most exp(-0.49676) + 0.001; that is, listed good trials are not
clustered, neither among the trials of one outer step nor among the outer steps
(members) of one context, beyond what this bound allows.

This is the premise of entry 415e792c, rate and dependence, restated for the
walk by contexts as entry e9b6649e restates it: part (i) is the same statement
as there, since N_c is a sum over the whole class (Lemma CX (c)), and part (ii)
is stated for the contexts, the independent units of this run. The clause of
entry 26ebba63 concerned the sub-class with rule A and its seven outcomes and
does not by itself imply the law of these trials (GPT Sol, answer AT 2), so the
premise is declared anew for these trials, this walk and S. Neither the filter,
nor the pre-check, nor the guards (G7) and (G15) change it: they skip only outer
steps, outcomes and words that hold no listed good trial (Lemmas F, VP, G7 and
G15), so N_o is the same count, pointwise (GPT Sol, answer AW 1).

In the terms of Lemmas S1 to S4 the premise is this: the construction's
pushforward of the uniform outer words and members, with c1 running over all of
Q*, onto the seven model words (E1.d1, E1.b1, E1.a2, Y4, Y9, w8, E3.h1) carries
at least the share FACTOR / 138,512,695,296, just under 10/11, of the
complete-success integral p of the conditional law of Lemma S1; that stays true
after the member with t = 0 is dropped (Lemma IP); and the dependence between
trials that share a context, in one outer step or in two outer steps of it, is
weak enough for the stated success at the declared run length. The two parts are
separate: neither follows from the other, and neither follows from the model or
from Lemmas S1 to S9. The factor FACTOR = 125,920,632,087 is assumed; 10.1 gives
what it is set against, the count 138,512,695,296 of the six outcomes of S, of
which it is ten elevenths rounded down. The margin 11/10 is a declared numerical
clause, open and not proved (GPT Sol, answer CK 9); it is stronger than the
factor 5/7 of entry 415e792c, which does not imply it. The participant's
preregistered toy run of the counter arrangement supports it (Section 13):
40,882 collisions of complete messages found against 40,800.63 predicted, with a
one-sided 97.7 per cent lower bound of 0.99213 on the ratio, above 10/11; that
is evidence at 8-bit words, not a transfer to 32 bits. The filter does not
change it.

*The rate on passing outer steps.* By Lemma S9 (a), N_o is zero on every outer
step that the filter rejects, so (i) says E[N_o | the outer step passes] >=
(2^21 - 1) q / pi_o, with pi_o of Lemma S9. Per member of Q* of a passing outer
step the rate is then at least about q / pi_o; for pi_o = pi it is q / pi =
125,920,632,087 / (279,070,422,111 * 2^80), about 2^-81.148: the rate of H1'
divided by the pass share, with no part of the counted mass lost (Lemma S9). The
success argument below uses (i) per context and needs no value of pi_o; pi_o
enters only the pass budget (H4').

*What is proved and what is not.* Proved (Lemmas S2 to S4): the outer words of a
step are uniform in the chart of the seven context words of Section 4; Y12 and
w5 are independent uniform words; E1.a1 and E1.a2 - E1.b1 are independent
uniform words at every fixed c1; and the sampler of Section 8 is exactly the
uniform-counter sampler conditioned on c1 in Q*. Proved as well (Lemmas V, RC,
G7, G15 and CV, 10.2 and 9.7): in every passing outer step that it reaches, the
search of 9.1 certifies exactly the listed good valid trials of the outer step,
so N_o is the same count for it as for an enumeration of all of Q*. Not proved:
that E1.b1, E1.a2, E3.h1, Y9 and w8 have the model's joint law with the rest;
GPT Sol 6.1 reduces part (i) to one success-weighted density of seven words that
the outer step fixes, Y12, Y1 + w12, C2.b1, C2.c1, w5, Y9 and w8, and that
density has not been counted. Not proved either: how much of the success mass
the member with t = 0 carries (Lemma IP bounds the number of dropped trials, one
in 2^21, not their mass), and the dependence inside an outer step and across the
members of a context.

*Part (ii) for contexts.* The contexts of a run are independent and identically
distributed (Lemma CX), and by part (i) the run has RUN_CONTEXTS * E[N_c] =
RUN_STEPS * E[N_o(U)] >= RUN_STEPS * (2^21 - 1) * FACTOR * 2^-128 =
0.4967600000... >= 0.49676. Lemma S8, applied to the contexts with N_c in place
of N_o, therefore gives part (ii) as soon as rho_c = E[N_c (N_c - 1)] / E[N_c]
is at most 0.0065: in that case b(rho_c) >= 0.99675, Lemma S8's exponent is no
less than 0.4951455, and exp(-0.4951455) < 0.609483 < exp(-0.49676) + 0.001.
Write N_c as the sum of the counts N_o(m) of the members m of the context. Then

    rho_c = rho_w + rho_x,  rho_w = E[sum over m of N_o(m) (N_o(m) - 1)] / E[N_c],
                            rho_x = E[sum over m != m' of N_o(m) N_o(m')] / E[N_c],

where, by Lemma CX (c), rho_w equals E[N_o(U) (N_o(U) - 1)] / E[N_o(U)], the
factorial ratio of a uniform outer step that the clause of entry 415e792c
bounds, and rho_x is the part that pairs of different members of one context
add. Both are at least zero, so rho_c <= 0.0065 implies rho_w <= 0.0065: *the
clause of this package is stronger than the per-step clause of entry 415e792c*.
It contains that clause and adds the dependence across the members of a context,
which the member loop creates by letting 2^19 outer steps share their seven
words.

*Part (ii) is an assumption.* That rho_c <= 0.0065 is assumed. It is not
measured, and it cannot be measured at full size: a context holds a listed good
trial with probability at most E[N_c] = 2^19 E[N_o(U)], about 2^19 * 2^21 *
2^-91.126 = 2^-51.126, so no run of feasible length sees one in a context, let
alone two. The margin is wide. Write v for the clustering ratio of listed good
trials by context, rho_x = v * (2^19 - 1) E[N_o(U)], so that v = 1 when the
listed good trials of different members of a context are independent; then rho_x
is about v * 2^-51.126, and the clause fails only if v exceeds about 2^43.86, or
if one listed good trial makes another in the same context, at the same member
or at another, far more likely than its rate.

*What is known of it.* For rho_w: an outer step has N_o <= 16 (Lemmas CV, G7
and G15), so rho_w <= 15, which does not help at this run length. GPT Sol 6.1
proves the bound 2^-13 for rho_w in a model in which E1.b1, E1.a2 and E3.h1 are
drawn afresh for every member of Q*, and proves as well that the construction's
own pair law is not of that kind: for two members of one outer step the second
member's three words take at most 2^62 values given the first's, not 2^96. So
that bound does not transfer. On the whole class, the error of the E1 rate of
the seven outcomes of entry 59f8915e, which contain S, clustered by outer step
equals its Poisson value (Section 13), which bears on the E1 side only. For v,
the participant measured the same ratio on the counter instance for events that
every listed good trial meets and that are frequent enough to count per
context: (E[n(n-1)]/E[n]) / ((2^19 - 1) p) for the count n of the event in a
context and its share p per member, which is 1 for independent members, each
run with a control arm of independent outer steps grouped in blocks of 2^19
(Section 13). At every depth from the filter to the roots of the solver it
stays near 1: the filter pass 1.151, the pass with the pre-check 1.157 and an
outer step whose solver reaches a leaf 1.153, over 120,000 contexts (control
1.000, 1.000 and 0.998); and an outer step whose solver returns a root, the
deepest event frequent enough to count, 1.249 +- 0.081 over 46,104,576
contexts, against 1.037 +- 0.072 for the control. The factor comes from
condition (2), whose omega = Y3 + y + w8 has w8 fixed by the context (condition
(1) alone gives 1.000175), and it does not grow with depth: from the pass to
the root no step adds more than the factor 1.005 of the pre-check, within the
errors. So wherever the ratio can be measured it is within a factor 1.25 of 1,
against a margin of about 2^43.9 for v. A preregistered run went deeper, to the
two halves of a listed good trial, over 262,144 contexts and 2^46 trials per
arm, with two generators and a control arm (Section 13): the cross-member
factor Rx, the part of the ratio that pairs of different members add, is 0.999
+- 0.054 (upper limit 1.162) for the listed E1 outcome at 2^-32.29 per trial
and 0.90 +- 0.24 (upper limit 1.94) for (J1) and (J2) of the E3 half at
2^-34.58, and R24, the low 24 bits of the difference of chaining-value word 1
zero at 2^-23.76, gives 1.0002; only the filter events cluster (1.144 for test
(2), 1.152 for the pass), and every upper limit lies at least 42 bits below the
2^43.86 that the clause allows at this run length (2^44.21 at the run length
for which the run was preregistered). A root of the solver is not yet a listed
good trial, which must also pass the certificate of step 3; the joint event,
about 2^-91 per trial, is not reachable, so carrying Rx near 1 to it remains
the premise, and v itself is not measured.

*No budget for steps 2 and 3.* Whenever an outer step reaches them, whatever its
words, the joint solver returns no more than 16 roots and steps 2 and 3 cost no
more than C15(T) <= 17,504 machine units (9.4, 9.7, Section 11), which the outer
step debits from the credit before they run (9.7); the final pair is formed and
hashed at most once, for a certified root (Lemma V). The run halts with failure
only when one of the two counts of 9.1 exceeds its budget, which H4' with
Hoeffding's inequality covers, when the opened count exceeds A_BUDGET, which
Lemma OR bounds with no premise (9.9), when the credit does not cover the C15(T)
of an outer step, which H5' covers, or after the last context, which H1' covers.

**Heuristic H4' (supporting).** For an outer step of the run, before any halt,
let I_E be 1 when the mask of (2) of its omega meets S and I_2 be 1 when its
mask X is not zero (it passes the filter, Section 8); let N_E and N_2 be the
sums of I_E and I_2 over the RUN_STEPS outer steps. H4' is two declared
numerical clauses on the means, open and not proved (GPT Sol, answer CK 2.1),
for a uniform outer step U, the outer step of entry 415e792c:

- *the test-(2) clause*, Pr(I_E(U) = 1) <= alpha_E p_E with alpha_E = 1.000026,
  where p_E = 233,715,456 / 2^32 = 2^-4.199822 is the exact share of words omega
  that pass the automaton of (2) for S (Section 8);

- *the pass clause*, Pr(I_2(U) = 1) <= alpha_P pi with alpha_P = 1.000176, where
  pi = 279,070,422,111 / 2^48 = 2^-9.978162 is the exact share of Section 8 for
  uniform independent pairs (Y9, omega).

*Use (proved).* The contexts of a run are independent and identically
distributed (Lemma CX), and N_E and N_2 are sums over the contexts of
per-context counts between 0 and 2^19; by Lemma CX (c) the mean of each
per-context count is 2^19 times the probability of its indicator for U, and the
two indicators of one outer step may depend on each other in any way. Each
budget of 9.1 is ceil(alpha RUN_STEPS p) + 2^19 s for its clause, so it exceeds
the mean of its count by at least 2^19 s, and Hoeffding's inequality over the
contexts, with range 2^19, puts the probability that the count exceeds its
budget at most exp(-2 (2^19 s)^2 / (RUN_CONTEXTS * 2^38)) = exp(-2 s^2 /
RUN_CONTEXTS) <= exp(-20) (GPT Sol, answer CK 2.2). The two clauses are stronger
than the factor 1.06 of entry 415e792c and do not follow from it. The reserve
2^19 s is 1.7 parts per million of E_BUDGET and 91 parts per million of
PASS_BUDGET: if a physical share exceeded its declared factor by more than about
that, its budget would be reached and the run would halt with failure, which
lowers the success probability and not the time bound. That the two
probabilities are at most alpha_E and alpha_P times their nominal shares is not
proved: Y9 and omega of a uniform outer step are not proved independent and
uniform. The number of outer steps that reach the solver has no budget and no
clause here: the solver is paid from the credit, which H5' covers (GPT Sol,
answer AW 5).

*Evidence.* The participant's preregistered sample of H5' (Section 13) counted
both indicators exactly on 2^39 = 549,755,813,888 real outer steps of the whole
class: 29,915,698,553 lanes with a nonzero mask of (2) against the nominal 2^39
p_E = 29,915,578,368, and 545,067,537 passing outer steps against 2^39 pi =
545,059,418.2. For a proposed share p_0 = alpha p and m = 2^39 p_0, the
one-sided Chernoff bound exp(-(m - k)^2 / (2 m)) on a count of k or fewer is at
most exp(-7) when (m - k)^2 >= 14 m; on the grid of one part per million,
1.000026 and 1.000176 are the least factors that pass this test for the two
counts, and 1.000025 and 1.000175 fail it (exact rational arithmetic, GPT Sol,
answer CK 2.1, recomputed by the participant). This reads the sample as ideal
independent draws; its words come from a pseudorandom generator (Philox4x32-10),
so it is evidence for the declared factors, not a proof of the physical means.
Also measured (Section 13): the preregistered run of 262,144 contexts per arm
gave the test-(2) and pass counts at 1.0000 +- 0.0008 and 1.0002 +- 0.0008 of
their nominal values; with the member loop, over 120,000 contexts with all 2^19
members each, the share of passing outer steps was 0.99847 of pi and the share
of lanes with a nonzero mask of (2) 0.99868 of p_E; and on 60,000,000 real outer
steps without the member loop, N_E is 1.0004 +- 0.0005 and N_2 0.9980 +- 0.0041
of their nominal values. If a budget is reached the run halts with failure; the
time bound charges each budget plus one and is not affected.

**Heuristic H5' (supporting; GPT Sol, answers AW 5 and AX 1).** For an outer
step U of the run, before any halt, V(U) denotes C(T(U)): the proved cap with
the guard (G7) alone of 9.7 and Section 11, for the outcomes T = X AND VMASK[nu]
kept by its pre-check, which is at least 27/16 times the debited cap C15(T(U))
(Section 11); V(U) = 0 when T is empty, in particular when the outer step fails
the filter. The premise: for a uniform outer step U (that of entry 415e792c),
and hence for the mean over the outer steps of one context (Lemma CX (c)), the
mean E[V(U)] is at most 1.01 * cbar, where cbar = CBAR / 2^47 =
582,173,006,981,436 / 2^47 = 4.13658801066... is a mean over all outer steps,
passing or not, with the zeros counted. This is a declared numerical clause,
open and not proved; it is stronger than the factor 1.06 of entry 415e792c,
which does not imply it (GPT Sol, answer CK 2.1).

In the counting model M_v, cbar is the exact mean of V; M_v takes the masks of
uniform independent (Y9, omega), as the nominal shares of H4' do, and a
three-bit nu, uniform and independent of them. If n_A pairs (Y9, omega) out of
2^48 have the mask A, then cbar is the sum, over A and over the eight values of
nu, of n_A C(A AND S AND VMASK[nu]), divided by 2^51 (GPT Sol, answers AW 5 and
AX 1). For S, T is X when nu is 3 or 4 and empty otherwise, so in M_v cbar is a
quarter of the mean of C(X), and CBAR is an eighth of the sum of n_X C(X) over
the masks X in S. By the certificate of Section 8 ten masks X occur; with their
counts n_X over 2^48, the caps C(X) of Section 11 with (G7) alone and without
(G7), and the debited cap C15(X):

| X | n_X | C(X) with (G7) | C(X) without (G7) | C15(X) |
| --- | ---: | ---: | ---: | ---: |
| 01 | 18,637,049,340 | 12,416 | 17,032 | 6,656 |
| 02 | 96,560,460,360 | 12,416 | 12,288 | 6,656 |
| 04 | 18,637,049,340 | 17,120 | 16,992 | 8,544 |
| 08 | 5,457,993,021 | 17,120 | 26,440 | 8,544 |
| 10 | 56,709,878,706 | 17,120 | 16,992 | 8,544 |
| 12 | 57,936,276,216 | 23,136 | 22,880 | 11,872 |
| 18 | 4,792,384,116 | 27,840 | 37,032 | 13,760 |
| 40 | 10,830,033,396 | 12,416 | 17,032 | 6,656 |
| 42 | 5,943,311,010 | 20,736 | 25,224 | 12,288 |
| 52 | 3,565,986,606 | 31,456 | 35,816 | 17,504 |

The n_X sum to 279,070,422,111 = SHARE / 2^16. The sum of n_X C(X) with (G7) is
4,657,384,055,851,488, and an eighth of it is CBAR = 582,173,006,981,436,
exactly, as the participant recounted it in integers from the certificate of
Section 8 and the trees of 9.4. Without (G7) the same sum gives
611,713,706,062,329, the CBAR of entry 415e792c. The sampler's nu is a function
of the outer step (9.7) and is not proved uniform or independent of the masks:
H5' is a physical statement about one weighted mean, the law of (X, nu) under
the sampler weighted by C, and it is not a consequence of H4' or of the shares
of the pre-check. It is not a mean of executed work: V is a proved upper bound
of the work of steps 2 and 3, outer step by outer step, so H5' assumes nothing
about the solver beyond the proved ledger.

*Use (proved).* The run debits C15(T(U)) <= 16/27 V(U) (Section 11). Let W be
the sum of C15(T(U)) over the RUN_STEPS outer steps; the run debits only in
outer steps that reach the solver, in order, and stops at the first halt, so
its debits are at most W. Under H5', E[W] <= 16/27 * 1.01 * cbar * RUN_STEPS
<= m_C (9.1). The sums of C15(T) over the 2^19 outer steps of the contexts of
a run are independent (Lemma CX), each between 0 and L_C = 17,504 * 2^19, so
their variances add up to at most L_C m_C, and Bernstein's inequality puts
Pr(W > m_C + t) at most exp(-t^2 / (2 L_C m_C + (2/3) L_C t)). With t =
CREDIT - m_C = ceil(sqrt(40 L_C m_C)) + 14 L_C = 24,119,904,503,157,054, t^2
>= 40 L_C m_C + (40/3) L_C t, so the exponent is at least 20 (GPT Sol, answer
CK 2.2). The credit is exhausted only when W exceeds CREDIT, with probability
at most exp(-20). The premise is used scaled by the pointwise ratio 16/27
(GPT Sol, answer CD 11.3). That E[V(U)] is at most 1.01 times cbar is not
proved.

*Evidence.* (a) The participant's preregistered sample of Section 13 measured V
with (G7) on 2^39 = 549,755,813,888 real outer steps of the whole class: mean
4.136407 against cbar = 4.136588, ratio 0.999956 +- 0.000089, with one-sided
upper bounds of 1.000297 (empirical Bernstein, delta 0.00135, range 31,456) and
1.000384 (bounded Kullback-Leibler) on the ratio, both below 1.01: by the rule
fixed in advance, SUPPORTED at eps when the upper bound is at most 1 + eps, it
supports H5' at eps = 0.01. (b) The earlier preregistered sample of 2^28 real
outer steps of Section 13, of V without (G7), gives a weaker bound from another
generator: on every mask C(X) with (G7) is at most 723/715 = 1.01119 times C(X)
without it (on 12, 23,136 against 22,880), so V with (G7) is at most 723/715
times V without it, outer step by outer step, and that sample bounds E[V] with
(G7) by 1.0151 * 4.346487 * 723/715 < 4.4617, 1.0786 times cbar, which does not
reach the 1.01 of H5'. Both samples are evidence from pseudorandom generators on
real outer steps, not proofs, and neither tests H1' or H4'. This premise takes
the place of the third count budget of our entry 0bc5f130.

**10.4 Success probability.** The probability space is the RUN_CONTEXTS fresh
words of step 1 of 9.1, independent uniform 256-bit words, for the fixed target
and the stated advice record of Section 12; the algorithm is otherwise
deterministic. Under H1', H4' and H5' it outputs a collision with probability at
least 1 - (exp(-0.49676) + 0.001) - 4 exp(-20) >= 1 - (exp(-0.49676) + 0.001) -
0.0005 = 0.390000993950... > 0.39 (GPT Sol, answers AW 3 and 5, CJ 1.2 and CK
2.2, with the tails of 10.3 and 9.9 over contexts). This is the union bound over
the five events "no valid trial is a listed good trial", "the E count exceeds
E_BUDGET", "the pass count exceeds PASS_BUDGET", "the credit does not cover an
outer step" and "the opened count exceeds A_BUDGET", which need not be
independent: H1' bounds the first; H4' with Hoeffding's inequality the second
and the third, exp(-20) each; H5' with Bernstein's inequality the fourth,
exp(-20); and Lemma OR with Hoeffding's inequality the fifth, exp(-20), with no
premise (9.9). A listed good trial lies in a passing outer step (Lemma F), in a
cluster whose gate opens (Lemma CL), which its lane takes as passing (Lemmas MB
and DT), whose pre-check keeps its outcome (Lemma VP) and whose solver with (G7)
and (G15) returns its root (Lemmas G7, G15 and CV); the search certifies it
unless the run ends before its outer step is reached, by a budget, by the credit
or by the output of another pair (9.1, Lemma CV). When the algorithm outputs a
pair, the pair is a genuine collision: its trial is certified, so R = 0 (Lemmas
RC and V), step 3 checks both complete digests, and the messages have different
lengths. The run is the shortest of this form that gives 0.39: RUN_STEPS_MIN is
the fewest outer steps that give 0.49676 expected listed good trials, 0.49676 is
the smallest number of five decimals for which the bound, with the allowance
0.0005 for the four tails, reaches 0.39 (with 0.49675 in its place it is below
0.389995), and RUN_CONTEXTS rounds RUN_STEPS_MIN up to whole contexts.

The heuristics are not proved; Section 13 gives the evidence for H1', H4' and
H5'.

## 11. Charged time

One 2-round target compression costs one unit, and every other primitive word
operation, every load and every store included, costs 1/430 of a unit. The rows
below are in operations, loads and stores, called machine units here; 430 of
them make one unit of time.

*The machine.* The search is charged on the load/store machine of 6.5, and the
selection procedure SEL of Section 12 counts operations of the same cost model,
with its 256-bit words, its packed lanes, its masked rotation and its charge of
one unit for every operation, load and store, with two changes: it has 64
registers in place of 16, and every constant is an immediate operand, written in
its instruction and not loaded. The cost model of the track charges primitive
word operations and sets no register count; this text charges as well a load for
every other word fetched from memory into a register and a store for every word
written to memory, spills included. The batches of seven members and their Q
paths run on packed words (9.8); the context, the rebuild of a passing lane, the
joint solver and step 3 run on scalar words of the same machine, one 32-bit
value to a word. The pieces of 6.5 and the counts of the earlier program on 16
registers (9.2) are not part of the charge. The schedules of this section are
upper bounds written out by blocks, after GPT Sol's answers AL 2, AQ 2, AR 3 and
6.2 to 6.6, AT 1 and 4, AW 2, 4 and 5, AX 1, CA, CD (sections 1, 3, 6, 8, 10 and
11), CF (sections 6 and 7), CI (section 1), CJ and CK (sections 2 and 9), and
not counts of an executed program, with two exceptions: the batch, whose 67
units with two list addresses participant programs executed with a count of
every operation and load (9.8; the pair words of 9.9 save one address), and the
295 of the rebuild of a passing lane, which a participant implementation counted
for entry 415e792c (9.6). The program of the declared experiment adds these
charges per event; it does not count machine operations (6.4). The Q path of 64
is the executed Q path of answer CA, 78 units, with its E count written out in 3
operations on a register in place of an allowance of 16 and two of its lines
fused into one (9.8).

**The cost, with every term.** Every row is machine units times an upper bound
on how often a run executes it; a row with a budget runs at most that many
times, plus the one that halts, because the algorithm halts with failure when a
count passes its budget (9.1). Exponents of counts and products are rounded up.

| Row | How often over a run, at most | Units | log2 of the product |
| --- | --- | ---: | ---: |
| context (9.8): drawing the fresh word, the 39 context lines on scalar words, preparing the sixteen packed operands, K included, storing the names for rebuilds, the context loop (bound in words, 507) | RUN_CONTEXTS + 1 = 2^50.117 | 600 | 59.346 |
| representative batch (9.9): its pair of list words (3), the omega side (19), the gate key of every lane (8), seven gate tests that each load P once (41) and the cursor (3), 74, with no T2; the last of a context, with four lanes, 56 | 2,341 * RUN_CONTEXTS = 2^61.310, RUN_CONTEXTS of them last | 74 or 56 | 67.520 |
| opened cluster (9.9): the opened count in its register and its test, the seven words of the representative batch kept in registers (no frame), the representative's T2 (6) and five partner batches of 9.8 on pair words, four of seven lanes (66 each) and one of three (42) | A_BUDGET + 1 = 2^62.995 | 333 | 71.375 |
| Q path of a lane whose mask of (2) meets S (9.8): the E count in three operations on a register, the 17 Y9-path lines in 16 packed lines (54), isolating Y9, loading T1, combining the two masks and branching (7) | E_BUDGET + 1 = 2^64.918 | 64 | 70.918 |
| passing lane: the pass count, the rebuild of its outer step on scalar words, the 37 words of the batch around steps 2 and 3 (the 29 of entry a402a477, the seven words of the representative batch and the opened count), the three words of (G7), the pre-check of 9.7 and, when T is not zero, the credit test (written out, 494) | PASS_BUDGET + 1 = 2^59.140 | 494 | 68.088 |
| outer step that reaches the solver: joint solver of 9.4 with (G7) and (G15), then the certificate of step 3 on each root; its cap C15(T) (bound in words) is debited from the credit first | total debits at most CREDIT = 2^70.425 | C15(T) <= 17,504 | 70.425 |
| one-time work: the direct tables T1, T2 (2^39) of 9.8, the member lists (2^27) and the gate table P (2^27) of 9.9; static rows with their descriptors (2^20); four allowances of 2^26, for the filter's automata, the three transition arrays, the written-out search code, and row metadata with VMASK, CT, array bases and initialisation; the reserve of 2^50 for exact histograms, cbar and CT; 40 for resident constants and the final halt test; 16 for a last failed budget or credit test; twelve allowances of 2^20, for the E count in a register, the root certificate, (G15), the global ledger of steps 2 and 3, the labels and frame of the gate, the four layout changes of 9.9 and the three new budget and credit constants; two more allowances of 2^20 for the register layout of the opened cluster and the opened count in a register (this package); 2^34 for the finite verification of B in Lemma OR | once | 1,126,467,395,125,304 | 50.001 |
| **total** | | | **72.649** |

In exact integers the sum of the rows is 600 * (RUN_CONTEXTS + 1) + 173,216 *
RUN_CONTEXTS + 333 * (A_BUDGET + 1) + 64 * (E_BUDGET + 1) + 494 *
(PASS_BUDGET + 1) + CREDIT + 2^39 + 2^27 + 2^20 + 4 * 2^26 + 2^50 + 40 + 16 +
14 * 2^20 + 2^27 + 2^34 = 732,555,948,487,469,400 +
211,484,018,622,008,992,768 + 3,059,955,960,246,785,915,406 +
2,229,353,954,973,358,266,368 + 313,600,319,186,720,703,956 +
1,584,841,873,457,225,944,219 + 1,126,467,395,125,304 =
7,399,969,808,901,982,417,421 machine units, where 173,216 = 74 * 2,340 + 56.

*Why every budget is charged plus one, and the credit once.* No more than
A_BUDGET clusters are opened, no more than E_BUDGET lanes run a Q path, and no
more than PASS_BUDGET passing lanes are rebuilt and pre-checked: in either case
the next lane pushes its count past the budget and halts the run before the work
of its stage. Each such row therefore charges its full allowance for the budget
plus one, which covers those lanes and the one that halts (GPT Sol, answer AW
4). An outer step that runs steps 2 and 3 has first debited its C15(T) from the
credit, so over the run their work is at most CREDIT; an outer step whose C15(T)
is larger than the credit left halts the run before steps 2 and 3, and that test
sits inside the 494 of its lane (GPT Sol, answer AW 5). Contexts and
representative batches have no budget: a run has at most RUN_CONTEXTS contexts,
each with 2,340 full representative batches and one of four lanes, and the
context row charges one more context. An opened cluster pays its count before
its partner batches, so the cluster that halts the run is inside the A_BUDGET +
1 charged. A context that halts before its last batch costs no more than a
complete one (GPT Sol, answer CD 3).

*A context, 600* (9.8), bound in words. Allowances: 16 to draw the fresh word
and split off the seven outer words; 195 for the 39 context lines on scalar
words, which need at most 158 (20 lines contain a rotation at five units and at
most one more operation, the other 19 at most two operations); 24 to form the
sixteen packed operands, K = X11 + 1 - S11 among them, which need at most 21;
128 to copy them into seven lanes, at most 8 per operand; 128 to save up to 64
scalar names for rebuilds; 16 for the context loop and the reset of the batch
cursor; and 40 for the two operands of the gate of 9.9, -(A >> 16) mod 128 with
its mask and its copies into seven lanes, and the base P_q, with their stored
metadata (answer CJ 4). These add up to 547, and the context is charged 600 (GPT
Sol, answers CD 1 and CI 1.5). The context leaves the register of the E count as
it is: the count runs over the whole run.

*The partner batch, 66* (9.8; GPT Sol, answers CA, CD 1 and CJ 3), identical in
every partner batch of seven lanes: 3 for loading the pair U[b], E[b] with the
address p + 1; 19 for the eight omega-side lines and omega (two rotations at
five units, each followed by an XOR, 12, and 7 single operations); 41 for the
seven lane tests (6 per lane, 5 for lane 0, which needs no shift); and 3 for the
batch cursor: 66. The fifth partner batch of a cluster has three used lanes: 3 +
19 + 17 + 3 = 42 (answers CI 1.5 and CJ 3). The participant's simulation of 9.8
executed and counted 67 units, with two list addresses, in every one of its
142,858 batches. No slack is added, and none is needed: the dispatch to a Q path
is the branch of its lane test, the jump to the fifth partner batch is the
branch of the cursor, and a passing lane returns inside its own units (9.8). At
most 36 registers are live and nothing is spilled (9.8).

*A representative batch, 74, and an opened cluster, 333* (9.9; GPT Sol, answers
CI 1.5 and CJ 2 to 5). A representative batch loads its pair of list words, 3;
runs the omega side, 19; forms the gate key of its lanes, eight packed
operations (a shift, two ANDs and an addition for a; an addition and an AND for
c; a shift and an OR for the key); runs seven gate tests, each the key of its
lane taken out by a shift and an AND, P_q added and the entry loaded, compared
and branched on, 6 units, 5 for lane 0: 41; and advances the cursor, 3. In all
74; it reads no T2. The last representative batch of a context has four used
lanes: 3 + 19 + 8 + 23 + 3 = 56. A run has 2,341 representative batches per
context, so this row is (74 * 2,340 + 56) * RUN_CONTEXTS = 173,216 *
RUN_CONTEXTS. An opened cluster costs its five partner batches, 4 * 66 + 42 =
306; 21 for its nesting (this package; 52 in entry a402a477): 4 for the base of
its partner pairs, 2 to set the cursor, 3 for the opened count, which a register
holds (the increment, the comparison with the immediate A_BUDGET and the
branch), 4 for the jump into the partner batches and the return to the next
gate test, and 8 for control and bookkeeping, the cluster index included; the
seven words of the representative batch stay in registers that no partner
batch, Q path or lane test names (9.9, *Registers of an opened cluster*), so
the 28 units of their frame in entry a402a477 are not spent; and 6 for the
representative's T2, its omega taken out, the load, the comparison and the
branch: 333. The opened count
is tested before the partner batches run. Q paths and passing lanes of the
representative and of the partners are charged in their own rows.

*A Q path, 64* (9.8; GPT Sol, answers CA and CD 1, 6 and 8.1), paid only by a
lane whose mask of (2) is not zero: 3 for the E count, which a register of the
batch holds (the increment, the comparison with the immediate E_BUDGET and the
branch); 54 for the 17 Y9-path lines in 16 packed lines (seven rotations at five
units, each next to an XOR, 42, and 12 single operations, two of them for the
fused line (X12 XOR M) + K); 2 to isolate the Y9 of the lane; 2 to index and
load T1; 3 to combine the masks, compare and branch: 64. The simulation of 9.8
executed 78 units in every one of its 54,067 Q paths in the form of answer CA,
with an allowance of 16 for the E count and 55 for the lines. A lane whose mask
of (2) is zero cannot pass and does not pay it (Lemma MB).

*A passing lane, 494 outside steps 2 and 3* (GPT Sol, answers AQ 2, AT 4, AW 2
and 5, AX 1.1, CD 3 and 8.1 and CI 1.5; the words of the batch for the walk of
9.8): the member y taken out of lane i of E[b] by a shift, an AND and the
subtraction of Y3, and step CO on scalar words with all the names that steps 2
and 3 read, at most 295, the participant's count for entry 415e792c, which took
eight words out of packed lanes at 2 units each where this lane takes one at 3;
16 for reloading the seven outer words of the context and E[b] with their
addresses; 116 for storing and reloading the 29 words of the batch of 9.8 and
9.9 around steps 2 and 3, the E count among them, which may use all 64
registers, 4 units a word with the addresses; 6 for storing C2.c1, C2.b1 and e1
in three fixed words for the guards; 8 for the pass count, held in memory, in
six operations (its address, its load, the increment, the store, the comparison
with the immediate PASS_BUDGET and the branch), the return link and the return
jump to the lane test of the next lane; 13 for the pre-check of 9.7; and 8 for
the credit test of 9.7, the address and load of CT[T], the address and load of
the credit, the comparison, the branch, the debit and its store: 462; and, in
this package, 32 for storing and reloading eight more words, the seven words of
the representative batch and the opened count, which registers now hold through
an opened cluster (9.9): 494. It is paid
by every passing lane, also when T is empty. The four bases of the tables and
lists are immediate operands, written with the code. The pass count and the
credit live in fixed memory words and are reloaded, never restored from a stale
copy. Only the Q path writes the E count, so the copy that the lane reloads is
current.

*Steps 2 and 3: C15(T), at most 17,504.* Each outer step that reaches the solver
is charged block by block, every block an upper bound on its operations, loads
and stores, with addresses, branches, spills and the restoration of registers
included (GPT Sol, answers AL 2, AR 3, AR 6.3 to 6.5, AT 1, AW 2, AX 1.1, CF 6.5
and 7.2 and CD 11.2):

- 1,024 once for an outer step whose T is not zero, the global ledger below;
  none when T is zero, since then no part of steps 2 and 3 runs.
- 2,304 for each family (9.4): at most 128 blocks of the formulas of (a) to (e)
  of 9.4, the phase checks, (P*) and their preparation, at 12 units each, 1,536
  (the 112 blocks of the formulas of answer AI 2 and 16 more; a block is the
  extraction of one source bit, a majority of four operations, an XOR of at most
  five inputs, the comparison or choice of a carry prescription, or a carry
  update, with its branch and assignment); the walks of bits 0 to 5 under the
  two guesses, at most 32 units a bit, 384; and 384 for the record of the
  family, which at most two rows of a set share (64 to store a record of 32
  words and 128 to load it twice), the packing of the guard planes and the
  dispatch.
- 1,408 for each searched row. Its 32 descriptors are built in 32 registers at
  32 units each, 1,024 (seven fields vary with the outer step, Q[i], y[i], E[k],
  E'[k], kappa[k], kappa[k+1] and the value of a constant, at 4 operations each,
  and 4 for the static base, the shift of the key and the assignment); 128 for
  the walks of bit 6 under the two guesses (64), the patches of h[6], h[7],
  h[13] and h[26] (24), kappa and the consistency of bit 6 (8), and the dispatch
  of the row (32); the guard (G7) of 9.7 adds 128 (answer AX 1.1), and the guard
  (G15) of 9.7 128 more for its five words (answer CF 7.2).
- 20 for each forced node: the key from the carry pair, the descriptor and the
  base of the array, and the read, 3; the validity, its comparison and the
  branch, 3; the next carry pair and the saved bit e2[29] (at position 9 the new
  bit is put in its place), 3; the chosen bit of h, shifted to its place and
  ORed into the prefix, 3; the guard of position 25 or 29 written into the key,
  at most 7 (at 25, bit 13 of the prefix shifted and masked, XORed with h[6] XOR
  u, which is held, shifted and ORed into the key, 5; at 29, the saved bit
  e2[29] masked, shifted and XORed into the key, 3); and the continuation, 1.
- 4 more for each selected node, at position 20: bit 8 of the prefix as the
  desired bit of the key of the selected array.
- 64 more for each node at position 15: the test of (G15) and the prescription
  of h[15] in a temporary copy of the descriptor (9.7).
- 48 for each free node: the parent saved in one register, 2; the key and the
  read of the dual array, 3; the two arcs taken apart, 2; 11 for each of the two
  children, for the validity, the carry pair and the saved bit, the prefix and
  the control; the parent restored before the second child, 2; and 5 for
  dispatch and return: 36, charged 48. No guard reads a free position.
- 80 for each leaf: g, f, e2 and h2 of its h and (J1), (J2) and (J3) as words, a
  rotation at five operations, 64; and 16 to reload the context words.
- 120 for each root: the certificate of step 3 (Lemma RC), run at the leaf of
  the root: Y14, Z, Y6, E1.a1, E1.d1 and c1, 22; the test (Q), 3; E1.b1, s,
  E1.a2, p and the test (A), 16; z and the test (C), 15; Y2, w0, K0.a1, t and
  the test (T), 17; twelve addressed loads, h, e1, C2.c1, C2.b1 twice, Y1,
  w12, Y12, w5, K0.d1, C2.a1 and C2.d1, 24; dispatch, return and control, 16:
  113, charged 120. A rotation on scalar words takes four units (two shifts,
  an OR and a mask), every sum is masked to 32 bits, and Y11, beta*, DY11,
  eps, IV[0] + IV[4] and the constants tau_j - beta* + 8 and ROR(tau_j, 8) of
  each row are immediates of the written code (answers CF 6.2 and 6.5).

*The global ledger, 1,024 (GPT Sol, answer CD 11.2).* This is a specified
layout, not a count of a program. The lane of 9.8 has finished its paid
pre-check and credit test when it calls steps 2 and 3, and it calls them only
when T is not zero. So that a lane with T = 0 stores nothing for the solver,
steps 2 and 3 repeat the scalar rebuild of step CO and store the names that they
read as these become available, in a fixed bank of 32 memory words, disjoint
from the 29 words of the batch, the family records and the words of (G15). The
names are the seven outer words of the context, Q, y, E, e1, C2.a1, C2.b1,
C2.c1, C2.d1, Y1, Y12, w5, w12, K0.d1, E' and E XOR E', and the two phase bits:
24 words, each stored before its register is reused. Every word of the bank that
is read later was written in this outer step, and no other word of it is read,
so the bank needs no clearing. Every address is a fixed offset from an immediate
base, and every name of a word, register and row is written in the code; nothing
is looked up by value. Once for a nonempty T:

| item | units, at most |
| --- | ---: |
| the scalar rebuild of step CO, repeated (295), and the addressed reloads of the seven outer words and E[b] (16) | 311 |
| up to 32 addressed stores of names into the bank, 2 each | 64 |
| E' = E + DY3, E XOR E', the phase fields, their normalisation and stores | 16 |
| loading sources at the boundaries of families and rows | 128 |
| the choice of outcomes and families from the fixed mask, and the top-level dispatch | 128 |
| entry into the frame, bookkeeping of bank slots and control, and the final return | 128 |
| unused reserve | 249 |
| total | 1,024 |

The loads cover five source words for each family, at most three families, 30,
and six context words for each row, at most three rows, 36, with 62 to spare;
the reloads of a leaf and the loads of (G7) and (G15) keep their own allowances
above. The choice runs a fixed decision tree over the six bits of T: six bit
tests at 6 units each, three family entries and three row entries and exits at 8
units each, and 16 for entry and exit, 100 in all. The last 128 pay the call and
return edges, the preparation of the bank base and offsets, and up to 32 further
addressed accesses. Each root is certified at its leaf and a rejected root
returns straight into the traversal (step 3), so no list of roots is kept,
allocated or sorted. Forming the first certified pair is in the once-only
allowance of the root certificate.

Summing the blocks: when an outer step reaches the solver with searched outcomes
T, steps 2 and 3 cost at most C15(T) = 1,024 + 2,304 F + 1,408 A + 20 N_f + 48
N_r + 4 N_s + 64 N_15 + (80 + 120) Lf machine units, where A counts the rows of
T, F their families, N_f, N_r, N_s and N_15 their forced, free and selected
nodes and their nodes at position 15, and Lf the leaves of their trees with (G7)
and (G15) in 9.4; roots are at most leaves, and this C15(T) is the entry CT[T]
of 9.7. The four sets of rows of 9.4, restricted to the outcomes of S, contain
every T that occurs:

| rows searched, among | A | F | N_f | N_r | N_s | N_15 | Lf | cap of steps 2 and 3 |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 275 | 1 | 1 | 80 | 7 | 4 | 4 | 8 | 8,544 |
| 175 | 1 | 1 | 42 | 3 | 2 | 2 | 4 | 6,656 |
| 285, 385 | 2 | 1 | 160 | 14 | 8 | 8 | 16 | 13,760 |
| 185, 385, 685 | 3 | 2 | 164 | 13 | 8 | 8 | 16 | 17,504 |

So steps 2 and 3 cost at most 17,504 machine units in every outer step that
reaches them, whatever its words and whatever its T, which the pre-check never
enlarges: 1,024 + 2 * 2,304 + 3 * 1,408 + 20 * 164 + 48 * 13 + 4 * 8 + 64 * 8 +
200 * 16 = 17,504 on the rows 185, 385 and 685 (GPT Sol, answers CF 7.2, CD 10
and CD 11.3; the trees and the arithmetic recomputed by the participant). The
cap C15(X) of each of the ten masks X of S that occur is in 10.3. The counts are
those of the static trees, and the blocks are added whether or not they occur
together, so this is an upper bound; it is not claimed to be attained or to be
the least such bound.

*The ratio 16/27 (GPT Sol, answer CD 11.3).* C(T) of 9.7 is the ledger of our
entry 0bc5f130 with (G7) alone: 4,096 once, 1,280 per row, 368 per leaf (80
and 288 for the full test of E1 on A and on B), no (G15), and the trees with
(G7) of 9.4; it is at most 31,456. Let n_s and n_l count the rows of a
nonempty T with eight and with sixteen leaves with (G7), those of 175, 185 and
685 and those of 275, 285 and 385. Summing each row's units over its trees,
1,280 + 20 * 72 + 48 * 7 + 4 * 4 + 368 * 8 = 6,016 and 1,280 + 20 * 140 + 48 *
15 + 4 * 8 + 368 * 16 = 10,720 with (G7) alone, 1,408 + 20 * 42 + 48 * 3 + 4 *
2 + 64 * 2 + 200 * 4 = 3,328 and 1,408 + 20 * 80 + 48 * 7 + 4 * 4 + 64 * 4 +
200 * 8 = 5,216 with (G15), so C(T) = 4,096 + 2,304 F + 6,016 n_s + 10,720 n_l
and C15(T) = 1,024 + 2,304 F + 3,328 n_s + 5,216 n_l. Every T that occurs lies
inside a mask X of Section 8 (T = X AND VMASK[nu]), and each of the ten masks
X lies inside one of the four sets of rows of 9.4, {275}, {175}, {285, 385}
and {185, 385, 685}. The table lists every nonempty subset of these four sets,
so every nonempty T that occurs:

| T | F | C(T) | C15(T) | 16 C(T) - 27 C15(T) |
| --- | ---: | ---: | ---: | ---: |
| 275 | 1 | 17,120 | 8,544 | 43,232 |
| 175 | 1 | 12,416 | 6,656 | 18,944 |
| 285 | 1 | 17,120 | 8,544 | 43,232 |
| 385 | 1 | 17,120 | 8,544 | 43,232 |
| 285, 385 | 1 | 27,840 | 13,760 | 73,920 |
| 185 | 1 | 12,416 | 6,656 | 18,944 |
| 185, 385 | 1 | 23,136 | 11,872 | 49,632 |
| 685 | 1 | 12,416 | 6,656 | 18,944 |
| 185, 685 | 2 | 20,736 | 12,288 | 0 |
| 385, 685 | 2 | 25,440 | 14,176 | 24,288 |
| 185, 385, 685 | 2 | 31,456 | 17,504 | 30,688 |

The last column is nonnegative on every row, so C15(T) <= 16/27 C(T) in every
outer step; for T = 0 both are 0. Equality holds for {185, 685}. The ratio is
claimed only for these T: on sets that never occur, such as 175, 185 and 685
together (three families), it fails. The participant recomputed the table in
integers from the trees of 9.4. The ratio needs no premise: it compares two
proved caps outer step by outer step, and the bound of H5' (10.3) on the mean of
C(T) bounds the mean of C15(T) by 16/27 of the same value.

*Registers of steps 2 and 3* (GPT Sol, answers AL 2, AR 3 and 6.3, CF 6.5 and
7.2). The search of 9.4 is written out statically for each row and each prefix
of free choices: a node at a prescribed position has at most one child, whose
code follows that of its parent, and a leaf label jumps to the leaf check; a
node at a free position, at most five on a path, saves its parent in one
register, the prefix of h and, above bit 32, the two carries and the bit
e2[29], the only earlier output bit that a later guard reads (the guard of
position 25 reads bit 13 of the prefix). The registers of the traversal are the
32 descriptors, five saved parents, six context words, eight constants, array
bases and control words, two words of the current state and ten temporaries: 63
of the 64. A leaf keeps the descriptors and the saved parents and uses the
others for its check, after which the context words are reloaded (the 16
above). The certificate of a root and the test of (G15) use only the ten
temporaries. For the certificate, t is formed first; then the live values fit
seven temporaries in each phase: Y14 with at most four loaded words; Y6, E1.a1,
E1.d1, c1, E1.b1, s and a loaded word; E1.a2, E1.d1, c1, s, p and a test word;
z, c1, two sums and z XOR ROR(tau_j, 8). One more temporary takes the shifted
part of a rotation, which is formed first so that a rotation may overwrite a
source that dies, one holds an address and one a comparison. The prefix h is
read without overwriting the protected word of the current state. For (G15):
the five words, an accumulator, the temporary descriptor, a test word, an
address and a prefix temporary. On both outcomes every other register of the
traversal is kept as it was, with no spill. The formulas of a family run before
the descriptors are built, in at most 58 registers: at most 35 bits and
carries, five source and context words, eight table, literal and control words
and ten temporaries. The repeated rebuild and the stores into the bank of the
global ledger run before that, with the 29 words of the batch already saved, so
all 64 registers are free for them; the bank is memory, and only the five
source words of a family are live when its formulas run (answer CD 11.2). No
register is addressed by a value: every position and register is named in the
code.

*Once.* The direct tables T1 and T2 (Lemma DT) are charged 2^39. The member
lists of 9.9, in cluster order, are charged 2^27: for each of the 2^19 members,
the deposit of its 19 bits at the free positions of e1, at most 3 units a bit,
57; the subtraction of Y3 and the rotation by 7, at most 6; and for each of the
two lists the shift of the value to its lane and the OR into the packed word, 2,
with the store of each packed word and its address, below 2 per member; and the
loop, 3: below 2^7 units per member, below 2^26 for the lists; and at most 64
units per cluster, 2^20 in all, to place its representative and its five partner
words. The six static rows of the outcomes of S, with the static fields of their
descriptors at the 32 positions and the metadata of the batches, are charged
2^20. 2^26 for the two automata of the filter for the seven outcomes, built and
composed into eight byte tables whose entries hold the base address of the next
table, with the entries of the last tables ANDed with S (GPT Sol, answers AN 2
and AQ 2): their states at each of the 32 bits are images of those of the
fourteen-outcome automata, at most 146, so the allowance of answer AN 2 covers
them. 2^26 for the three transition arrays of 9.4: their 2^18 entries at most
256 operations each, the enumeration of the keys, both candidate arcs, the test
for an invalid or a second arc, the selection and the store included (answer AR
6.2). 2^26 for writing the code of the search, the immediate bases of the tables
and lists of 9.8 included: 432 static nodes over the six rows of S, with the
prescribed bits of (G7) and (G15) at positions 7 and 15, fewer than 2^14 labels,
at most 256 operations each with their set-up (answer AL 2). And 2^26 for the
row metadata, the absolute bases of the arrays and their initialisation, a
fourth allowance that GPT Sol keeps for safety (answer AR 6.2), which also
covers the enumeration of the compatible patterns of 9.7, the eight words of
VMASK and the 128 words of CT, below 2^23 operations (answers AW 2 and 5). 2^50,
the once-only reserve of GPT Sol's answer AW 5 for the exact mask histograms,
the mean cbar and the table CT, charged in full whether or not it is used. 32
for loading the resident constants and array bases into their registers, 8 for
the test of the final halt, and 16 for a final failed budget or credit test,
kept conservatively (answer AW 4). And 2^20 for each of four parts of this
layout (answers CD 6, 8 and 11.2, CF 6.2 and 7.2): the E count in a register,
with its code, the frame of the batch and its initialisation; the root
certificate, with the immediates of the rows, its code, the updated CT and at
most 1,024 units to form the last blocks of the first returned pair; (G15), with
its unrolled code, the layout of the five words of a row and the updated CT; and
the global ledger, with the layout of the bank of 32 words, its labels and the
updated CT. 2^27 for the gate table P of 9.9: for each of its 2^21 keys at most
64 units, to take the key apart, form the two sums, compare them with the ends
of the two intervals of S7 and branch, store the entry and loop. And a fifth
2^20 for the labels of the gate, the frame and the opened count, with their
initialisation (answer CI 1.5); four more for the code and constants of the four
layout changes of 9.9, the T2 read only in opened clusters, the pair words, the
q blocks of P and the seven-word frame (answers CJ 2 to 5); three more for the
immediates of the new run length, the E and pass budgets, the credit and the
opening budget (answers CK 2, 5 and 9); and 2^34 for the finite verification of
B in Lemma OR, 2^24 candidates at 512 units each below 2^33 and the supports,
windows and histograms below 2^33 more (answer CK 5.2).

*One-time items.* The items above are in the last row. The final step, once:
steps CT and CS for the trial found, writing the two messages, shorter than 2^42
bytes each, and two complete evaluations of blake3; each message has at most
2^32 chunks of 16 compressions each and fewer than 2^32 parent compressions,
below 2^37.1 compressions for both, and writing them is below 2^38 machine
units: below 2^38 units of time in all. Preprocessing: the selection procedure
SEL of Section 12, charged in full at its cap by construction, S_old =
8,882,224,365,081,579,520 machine units, below 2^54.198 units of time.

Total:

    T <= (sum of the rows) / 430 + 2^38 + S_old / 430
      <  2^63.9016.

In exact arithmetic the numerator is 7,399,969,808,901,982,417,421 + S_old =
7,399,969,808,901,982,417,421 + 8,882,224,365,081,579,520 =
7,408,852,033,267,063,996,941 machine units, T = 7,408,852,033,267,063,996,941
/ 430 + 2^38 = 17,229,888,724,336,195,308.98 units, and log2 T =
63.90154718710604...; in integers, with 430 T = 7,408,852,151,464,563,982,861 a
whole number, (430 T)^10000 < 2^639016 * 430^10000 and (430 T)^10000 >=
2^639015 * 430^10000. The claimed time_log2 is 63.9016, this total rounded up
at the fourth decimal. The search part alone, that is the rows and the final
step without SEL, is 2^63.89981655079854...; S_old / 430 is 2^-9.702 times the
search part and adds 0.00173 to log2 T. The bound holds in the worst case for
the algorithm as stated: every run halts within its three budgets, its credit
and its RUN_CONTEXTS contexts, steps 2 and 3 are bounded in every outer step
that reaches them, and SEL is bounded by its caps. No mean of a count of work
enters it, since CREDIT is a fixed number enforced by a halt; H1', H4', H5',
Lemma OR and the four overflow tails bear on the success probability only. The
claim rests on this 64-register schedule: no figure for 16 registers is
claimed, and this schedule is not claimed to be the cheapest.

*Where the search part goes.* The opened clusters are 41.35 per cent of the sum
of the rows, the Q paths 30.13 per cent, the credit of the solver 21.42 per
cent, the passing lanes 4.24 per cent, the representative batches 2.86 per cent,
the contexts 0.010 per cent and the one-time items, the reserve of 2^50
included, about 10^-5 per cent. Per walked trial, RUN_STEPS * 2^21 of them, the
sum is 0.0000055124 machine units (2^-17.469); per walked outer step it is 11.56
machine units, of which 8.59 are the batches, the opened clusters and the Q
paths and 2.4759 the credit.

*The one formula.* In the form that the entries of this track use, time_log2 =
log2(lambda) + 128 - log2(C / m) + log2(ops / 430) + c, where lambda = 0.49676
is the expected number of listed good trials, C = 138,512,695,296 is the count
of the six outcomes of S (10.1), m = 1.1 is the margin and ops = 0.0000055124
machine units per walked trial from the sum above, gives 63.8999 for the search
(63.89981... before rounding up). The one-time items and the final step are far
below the allowance c; SEL adds 0.00173 (above).

Nothing is sorted and nothing is looked up by value: each root is tested against
the conditions of its own outcome, and no certified trial is compared with
another. The reads at positions that words give are: per batch, the words U[b]
and E[b]; per used lane of a partner batch and per opened representative, the
entry of T2 at its omega, and per lane of a representative batch the entry of P
at its key; per Q path, the entry of T1 at its Y9; per passing outer step, the
names saved for its context, the words saved for its batch, VMASK[nu] and, when
T is not zero, CT[T] and the credit; in an outer step that reaches the solver,
the transition arrays at the keys of the searched rows, the five words of (G15)
of each searched row, the family records and the static rows of the outcomes.
Every such read is charged as one load: a partner batch counts its 2 list loads
and 7 loads of T2 inside its 66 units, a representative batch its 2 list loads
and 7 loads of P inside its 74, an opened cluster the representative's load of
T2 inside its 333, a Q path its load of T1 inside its 64, and the loads of a
context, of a passing lane, of the pre-check, of the joint solver and of step 3
are inside the allowances above. No table grows with the trials.

## 12. Memory, preprocessing and advice

The program of the search is the lines of steps CO, CT and CS, the outer
filter, the walk of 9.8 and 9.9, the joint solver of 9.4 with its statically
written traversal and the guards (G7) and (G15), and a compression routine for
step 3 and the final check: below 2^28 bytes of code and metadata (Section 11).
Data, one word of 256 bits each unless said otherwise: the two direct tables T1
and T2 of 9.8, 2^33 words, 2^38 bytes; the two member lists, 168,522 words,
5,392,704 bytes, below 2^23 bytes; the gate table P of 9.9, 2^21 words, 2^26
bytes; the 29,952 entries of the tables of the filter's two automata, from
which the direct tables are built; the three transition arrays of 9.4, 2^18
words of 32 bits, 2^20 bytes; fewer than 4,096 words for the joint solver (the
descriptors of the positions of a row, the six static descriptors of S, the
records of the families, the bank of 32 words of Section 11 and scratch); and
fewer than 1,024 words for the names of step CO, the stored names of a context,
the stored words of a batch, the five words of (G15) of each row, the constants
and masks, VMASK, the 128 words of CT, the two counts, the credit and the cells
of step 3. The memory of the search is therefore below 2^38 + 2^28 + 2^26 +
2^23 + 2^21 + 2^20 + 2^18 < 2^39 bytes. Nothing grows with the number of
trials. The two messages of a found pair have 1024 t + 55 and 1024 t + 63 bytes
with t < 2^32, each shorter than 2^42 bytes; the output, the two messages with
their digests, takes less than 2^43 bytes.

**The advice record.** The search reads a fixed record, stated here in full,
which this package treats as nonuniform advice: the six constants X3 = 29d4fa98,
X7 = bee3af28, X11 = 44036000, X15 = 40c58500, W4 = 97475638 and W13 = 0007c006
of 3.2, 24 bytes; eta = 830303cf, 4 bytes; beta* = 18b0e098 with the mask
0e09818b and the value 02008000 of its cube, 12 bytes; the seven values of tau
of the filter's automata, 175020a0, 185020a0, 275020a0, 285020a0, 385020a0,
675020a0 and 685020a0, and eps = 6e21be55, 32 bytes; and the mask 5f of S, 1
byte: 73 bytes, so nonuniform_advice_log2_bytes = 7. The submitted program (6.4)
stores these values and no other advice: its other constants are the IV, values
derived from the record, and run constants and charges (9.1, Section 11); it has
no sub-class.

The success analysis of 10.3 and 10.4 uses only properties of this stated
record, and this text verifies each of them exactly, whatever the way the record
was found: Fact P, the equal d and b outputs of C3 for W4 and W4' (3.2); Lemma
Q, the class of eta with exactly 524,288 members; Theorem C (iii) and (iv), by
which c1 gives the difference beta* exactly when c1 AND 0e09818b = 02008000; the
fourteen outcomes of beta* on the class, all with eps = 6e21be55, and the count
67,633,152 = 1,032 * 2^16 of the six of S (10.1, with the program of Section
17); the certificate of the filter for S, with SHARE and E_COUNT (Section 8);
and, for the search itself, the allowed patterns of the pre-check (9.7) and the
guards, trees and caps of the joint solver for this class and S (9.4, Lemmas J0,
G7 and G15, Section 11). H1', H4' and H5' are stated for this record (10.3).
Nothing in the success analysis depends on how the record was found, on a
selection returning it, or on any record of the runs that found it.

**The selection procedure SEL.** The advice record was found by a solver search
and one count per model, which the submitted program does not contain. This
section writes that search as a procedure, SEL, and charges its whole cost as
preprocessing, included in T (Section 11). The cost model charges any search
omitted from the submitted program; SEL is that search, and its whole capped
cost is charged. The charge is a bound by construction: every search of SEL runs
over a range stated here, and every run of a program in SEL halts as soon as it
has executed a stated number of primitive word operations, its cap, or holds
2^34 bytes; a run that halts so returns nothing, and SEL goes on. Operations are
counted as in Section 11, 430 to the unit. SEL runs two programs of the
participant that are not in the package: the solver kissat, on instances made by
a generator of the participant, and the counter of Section 13, which computes in
integer arithmetic the part of one beta in the rate of the class of a given eta,
with no rule on h1; a run of the counter whose part would be 2^192 or more
counts as one that reaches its cap.

*Step 1, the pinned call (solver runs).* For each of the 116 runs of the
participant's solver log for this search (51 runs for the lengths 55 and 63, the
other 65 for nine other variants of the instance; bounds 97 to 118; logged
seeds), build the instance of the run and run kissat on it with the logged seed,
the two together with a cap of 2^56 operations. For the lengths 55 and 63 the
instance is that of entry c66f230d (its Section 10): the call C3 for both
messages with equal b and d outputs, the two words w4 related as the length
cancellation prescribes for the XOR 8 of the lengths, the top byte of word 13
zero, E1 and E3 for both messages, a zero residual, and a bound on the number of
bit positions, bit 31 excepted, at which a difference is active in six additions
of E1 and E3. A run that finds a model returns six constants X3, X7, X11, X15,
W4, W13 and the values of a solution, among them its Y4 and its beta. Cost: at
most 116 * 2^56 < 2^62.86 operations.

*Step 2, the constants, the class and beta* (a count for each model).* For each
model of step 1, compute Y3 and Y3' by C3 from its constants, its class eta =
ROR((Y3 + Y4) XOR (Y3' + Y4), 16) from the Y4 of its solution and its beta from
the c1 of its solution, and with the counter the part of that beta in the rate
of the class of that eta, with a cap of 2^52. Output the six constants, the eta
and the beta of the model with the largest part, the first in the order of the
log if parts are equal. Cost: at most 116 * (2^52 + 2^10) < 2^58.86 operations.

*Step 3, the cube, the outcomes and S.* With DY11 = Y11' - Y11 for the output of
step 2, form the mask ROL(beta, 12) AND 7fffffff and the value (ROL(beta, 12) -
DY11) / 2 of the cube of the words c1 that give beta (proof of Theorem C (iv)),
and the outcomes (tau, eps) of beta whose product L * N3 is not zero, which the
count of step 2 lists; for beta* these are the fourteen of 10.1. Then, for each
of the 16,383 nonempty sets S of these outcomes, compute in integers the
numerator O(S) of the ledger under which S was chosen, that of entry 415e792c:
O(S) = 424 * RUN_BATCHES + 35 * (E_BUDGET + 1) + 512 * (PASS_BUDGET + 1) +
CREDIT + 1,125,900,176,326,712, with its count from the rows of step 2, its
FACTOR, RUN_STEPS and RUN_BATCHES = ceil(RUN_STEPS / 7), its E_COUNT and SHARE
from the mask certificates of the two automata of the outcomes, its two budgets,
its table CT of the caps without (G7), 4,096 + 2,304 F + 1,152 A + 20 N_f + 48
N_r + 4 N_s + 368 Lf over the trees without (G7) of 9.4, their mean cbar_S over
the masks of these certificates and the eight values of nu (10.3), and its
credit at 1.06 times cbar_S. Output the S with the least O(S), the first in
increasing order of its mask if two are equal, and the outcomes whose tau has
bit 14 equal to 0, from which the outer filter's automata are built. Step 3 and
the bookkeeping of SEL run under a cap of 2^50 operations.

**The bound.** Steps 1 to 3 cost at most

    S_old = 116 * 2^56 + 116 * (2^52 + 2^10) + 2^50 = 8,882,224,365,081,579,520

operations, below 2^62.946 (in integers S_old^1000 < 2^62946), and so below
2^(62.946 - 8.748) < 2^54.198 units (S_old^1000 < 430^1000 * 2^54198).
preprocessing_log2 = 55 is this bound rounded up to a whole number, and the
whole of S_old is in T (Section 11). It bounds SEL as defined, whatever the two
programs do inside and whatever they return, because every run halts at its cap
and every loop has the range stated. SEL is not a premise of this package, and
no heuristic is declared for it.

*What rests on records.* The bound rests on no record. That SEL returns exactly
the six constants of 3.2, eta = 830303cf, beta* = 18b0e098 and S = 5f rests on
the participant's records: for S, on GPT Sol's exact comparison of the 16,383
sets (answers AW 4 and 5); for the rest, on the participant's solver log, by
which the run for the lengths 55 and 63 with bound 104 and seed 506 found these
constants after 4,770 seconds, with a solution of class 830303cf and beta
18b0e098, and on an exact integer recount, by the participant's counter on the
whole class of each instance, of all 65 distinct instances that the runs of the
log returned with a model, in which these constants have the part 71,698,432,
the largest, and the next is 13,107,200 (a strict maximum, 5.47 times the next).
Every run of the log stopped within 9,010.5 seconds on one processor core and
every recount within 320 seconds; at 2^42 operations a second for a core, a rate
the participant states and does not prove, every run stayed below 2^55.14
operations and every recount below 2^50.33, inside the caps. The log does not
fix every instance: some runs excluded pairs that runs finished before them had
found, and 32 runs were stopped from outside without a record of the cause. So
the records certify a historical run of the solver, not a replay with operation
caps, and the generator of the instances, the solver log and the counter are not
in the package. If a record were wrong, SEL could return other constants or
none; its cost would stay within the bound.

*Memory of SEL.* Every program run of SEL halts when it holds 2^34 bytes, and
SEL runs one program at a time; its own data stay below 2^20 bytes, the parts of
step 2 and the outputs. SEL therefore holds fewer than 2^34 + 2^20 bytes at any
time; the search fewer than 2^39 bytes, its direct tables included; the output
fewer than 2^43 bytes. Held at once, these total below 2^43 + 2^39 + 2^35 <
2^44: memory_log2_bytes = 44 bounds all. The measurements of Section 13 are not
part of SEL: they test the heuristics and select nothing. The cost model does
not score memory.

The direct tables and the member lists, like the tables of the filter's
automata, VMASK, CT, the three transition arrays, the descriptors and the
traversal, are not advice: they are computed from the record. SHARE and E_COUNT
are counts from the certificate of Section 8, CBAR is computed from that
certificate, VMASK and CT, and the budgets and the credit of 9.1 are computed
from them, from the factors of H4' and H5' and from the other constants of 9.1.
The flags 3 and the counter rule are part of the algorithm. There is no other
stored data and no stored collision.

## 13. Evidence, scope and field meanings

Throughout this text costs and bounds are rounded up, and margins, rooms and the
whole numbers of the count that the claim uses are rounded down. Counts printed
with decimals are rounded to the nearest.

**What is exact.** Sections 2 to 5, 7 and 8; Lemmas L, H, Q, Q2, T, T2, T4, N,
A, TR, CT, IP, F, J0, V, RC, VP, G7, G15, CV, Y, CX, DT, MB, KP, A9 and CL and
Theorem C; the count of passing pairs of Section 8 and the allowed patterns of
the pre-check and the table CT of the credit (9.7); the parity certificate (P*),
an exact count, and the constants and caps of the joint solver (9.4) with its
schedule (Section 11), as upper bounds, with the ratio 16/27 of its caps; and
Lemmas S1 to S9 under their stated hypotheses. Lemma A says what stage A tests,
not that a collision passes it. The declared experiment returns, per organizer
seed, a pair of the root instance built by steps CO and CT with the flags word
11 and t = 0 for the context of the trial, and the organizer recomputes both
digests; the proof of Theorem C (ii), which reads the flags only in the line for
K3.d1, predicts the agreement on the 128 masked digest bits. The counter
instance has no organizer digest check (6.4).

*How it was checked.* The participant's checks are computations, not proofs: the
counter construction against the organizer's own functions on 2,000 trials, with
204,000 internal words compared with a separately written forward computation,
and complete messages hashed by the organizer's code (Section 7); every lane of
the counter batch against the earlier program's compression of the real last
chunks (9.3); all 2^21 members of Q*, each giving the difference beta*; the rule
t != 0 (Section 8); the earlier program's automata against brute force at 10
bits (9.3); the free positions, static trees, families and caps of the solver,
and the sums of the cells of (P*) against the counts of 10.1, with a separate
count of (P*) in one phase of 2^16 members (9.4); the word nu of the pre-check
against the bits s[13] to s[15] of 324,098 real trials (9.7); and the two lists
of Lemma Y, the member lines and the pass decisions of the member loop and of
the omega-first batch against the full outer step, with every operation of the
batch counted (9.8); and the finite checks of Lemma A9 and of the gate table,
with Lemma KP and the gate against the word equations of 9.9 on 20,000 random
clusters and context words (9.9); and, in the program of 6.4, every walked
member of every trial against the full outer step, every closed cluster against
a bit-serial test (2) and every E lane against a real compression (Section 13).
For Sections 1 to 6, three independent reruns found no wrong value in the
displays, Table C and Lemmas Q, Q2, L, A, T2 and T4, and Lemma A was checked by
complete enumeration of the 2^16 patterns that it reads. No person has read any
part of this text.

**The seven-word model.** By 6.2 the residual of a trial, of the root instance
or of the counter instance, is a function of the constants and of seven 32-bit
words: for E1 its first-half values d1 and b1 and its a output a2 on message A,
and for E3 the words Y4, Y9, w8 and its first-half value h1 on A. The model M
says that over the trials the six words other than Y4 behave like independent
uniform words, independent of Y4, which is uniform in the sub-class. Under M a
trial has R = 0 with probability r * 2^-128, where r * 2^81 is the number of
solutions of R = 0 among the 2^209 values of the seven words with Y4 in the
sub-class. Call r the *rate of the sub-class*. Rule A is a condition on h1, so
under M the trials with R = 0 that satisfy rule A have a rate of the same kind,
r_A, counting only the solutions that satisfy rule A; r_A is at most r. The
counter search prescribes c1 = Y11 + d1 in Q*, and under M that is a
conditioning on d1 (Lemma S1); its rate p is formed from the part of beta* in r
(10.1). On the outer steps that pass the filter of Section 8 the rate under M is
p / pi, and no part of p lies on the others (Lemma S9). M and the count give the
rate of a single trial. They do not give the
probability that a run has a good trial, which also depends on how the good
trials of a run cluster; a model of the single trial says nothing about that.

Given M, the rates are properties of the constants, the sub-class and beta*
alone and can be counted without sampling; the count says nothing about whether
M holds. The six words are not free in a trial. In the counter search Y4, Y9
and w8 are fixed for the 2^21 trials of an outer step, and so are Y12 and w5,
which E1 reads; the trials of an outer step differ in d1 and in what follows
from it (Lemma CT (c)), and E1.b1, E1.a2 and E3.h1 move with d1. M is a
statement about averages over the outer steps of a run. Lemmas S2 to S4 show
which parts of it hold exactly for the construction, and H1' declares the rest.
The measurements below show where M fails inside one context and inside one
outer step.

**How r is counted (participant computation, not organizer-verified).** Write
tau, eps, beta for the XOR differences between A and B of E1's a output, c
output and first-half b, and eta, psi, tau', eps' for those of E3's first-half d
and b and its c and a outputs. Because E1's a1 and d1 are the same for A and B,
R = 0 holds exactly when tau' = tau, eps' = eps, psi = tau XOR ROR(tau, 1) and
eta = eps XOR ROL(beta XOR eps, 1); for Y4 in the class the left side of the
last equation is the constant 830303cf. The counter works in integers (128-bit
unsigned integers; exact fractions for the products and sums), has no sampling
branch, and needed no fallback on any outcome of the count below; no
floating-point number is on the path of a figure printed below as a fraction.

1. *The betas.* beta is a function of d1 alone: with c1 = Y11 + d1 and DY11 =
   Y11' - Y11 = 0a08818b, beta = ROR(c1 XOR (c1 + DY11), 12). As in Lemma Q, the
   d1 with a given beta are a share 2^-k of all d1, k being the number of bits
   of the mask ROL(beta,12) AND 7fffffff.
2. *The outcomes of one beta.* An outcome is a pair (tau, eps); the admissible
   tau are enumerated with a carry automaton, with no bound on the weight of
   tau. A beta for which beta XOR ROR(eta, 1) has odd weight contributes
   nothing; every other has two candidates for eps.
3. *The E3 side.* N3 is the number of quadruples (Y4, h1, Y9, w8) for which E3
   produces eta, psi, eps and tau; all of them have Y4 in the class.
4. *The E1 side.* P1 is the probability that E1 produces tau and eps when d1 is
   uniform among the values with this beta and b1 and a2 are uniform.
5. *The sum.* For the sub-class, N3 counts only the quadruples with Y4 in the
   sub-class, and the part of a beta in r is 2^(15 - k) times the sum over its
   outcomes of P1 * N3, where 15 is the number of bits that Lemma Q2 fixes, so
   that the sub-class is a share 2^-15 of all Y4: the sum of N3 over all 2^96
   values of (d1, b1, a2) is r * 2^81, and 2^96 / 2^81 = 2^15. r is the sum of
   the parts over all betas. Parts are not negative, so the sum over any set of
   betas is a lower bound for r. For r_A, N3 counts only the quadruples whose h1
   satisfies rule A.

**The count of the class and of the sub-class (participant computation).** The
count runs over the 60 words beta that have a part in the rate of the whole
class, the list of entry c66f230d: of the 133,742 words that occur as beta, the
4,550 with k at most 14 were enumerated, and for the 129,192 others a SAT solver
was asked whether the whole system has a solution with that beta and answered no
for 129,147, without certificates. The integer enumeration of GPT Sol 6.1 over
every beta finds the same 60. For the whole class the rate is
85074516985129/524288 = 162,266,763.66, from 60 betas and 453 outcomes with a
nonzero product. For the sub-class of the root instance it is r =
194382080300609/1048576 = 185,377,197.55, about 2^27.47, so that under M a trial
of the root instance has R = 0 with probability about 2^-100.53. A few betas
carry most of the count (beta* = 18b0e098 alone 36.5% of r, the four heaviest
98.8%), so the count rests on few paths; the claim of this package uses only the
part of beta* on the class (10.1).

**Checks of the counter (participant computations).** (1) Complete enumeration
with 8-bit words of every quadruple (Y4, h1, Y9, w8) through both executions of
E3 and every triple of the E1 side, over random constants, classes, sub-classes
with up to three more fixed bits of e1 and rules with parities of three bits:
five runs, 1,472,040 and 5,332,992 integers, none different from the counter.
(2) At 32 bits two functions compute the E3 side with its split by the rule and
agree on all 687 outcomes both counted; the other 285 (16 with a nonzero
product) were counted by one alone. The E1 count agrees with the earlier
calculator on 972 of 972 outcomes. (3) For the whole class, a helper agent that audited entry
c66f230d counted both factors of all 453 outcomes with two programs written from
the definitions of 6.2 and 6.3 alone: the same total, 85074516985129/524288, and
the same parts for 60 of 60 betas.

**Real messages in the counter arrangement.** This and the next paragraph
report participant measurements of the counter arrangement; the organizer's
harness does not run them, and they are untrusted evidence for it. On a
graphics card a helper agent ran the counter construction on real 32-bit
messages, with random outer words and 2^12 consecutive members of Q* per outer
step: 2^45 trials with Y4 in the sub-class and 2^44 with Y4 in the whole class,
and the same counters on the seven-word model with c1 in Q* (2^44 and 2^43
model trials); on a processor, four runs of 2^20 outer steps with 2^16 members
each. Every real trial had the difference beta* (2^45 of 2^45). Against the
exact figures of the model:

| Event | Model, exact | Real counter trials |
| --- | --- | --- |
| tau listed for beta* | 2^-10.696 per trial | 2^-10.696 per trial |
| listed E1 outcome (beta*, tau, eps), sub-class | 10,176.0 | 10,129, that is 2^-31.694 per trial |
| listed E1 outcome, both classes together | 15,264 | 15,139 (-0.8% +- 0.8%) |
| rule A | 2^-8 | 2^-8.000 |
| listed E1 outcome and rule A, both classes | 59.6 | 55 |
| listed partial E3 event, whole class | 3,569 | 3,626 |
| E1 test of Lemma N passed (n = 0) | | 2^-26.02 per trial |

The ratios of the real to the model runs, in the sub-class with Poisson errors:
listed E1 outcome 1.009 +- 0.017; listed tau 1.0001; rule A 1.0000; E1 test
0.9998 +- 0.0024; listed tau and rule A 0.9999 +- 0.0002; listed E1 outcome and
rule A 0.90 +- 0.25; listed partial E3 event 1.057 +- 0.020, where the true
error is larger because these events cluster by outer step (whole class
0.971 +- 0.028); each of the four residual words zero 1.019, 1.009, 0.984 and
0.990, each +- 0.006 to 0.021. In the arrangement of entry 64c075ac the same
events of beta* are rarer by the factor of the prescription: c1 lies in Q* with
probability 2^-11 there, and the listed E1 outcome of beta* has 2^-42.69 per
trial, against 1 and 2^-31.69 here. So the E1 side of a counter trial carries
the factor 2^11 that the count predicts, and the E3 side is unchanged. On the
processor the number of trials of one outer step that satisfy rule A has a
variance 572 times its mean, and that of the listed tau 247 times: single outer
steps differ strongly, and only averages over outer steps agree with M. No
event here is deeper than about 2^-40, the listed E1 outcome with rule A; none
is the joint event of H1', at about 2^-91.

**A scaled-down end-to-end run of the counter arrangement.** The whole counter
search was run on an eight-bit version of the hash: 2-round BLAKE3 with 8-bit
words, 2-bit toy bytes, 64-byte blocks and 1,024-byte chunks, with eight sets
of toy constants fixed before any counted run and the class of each. The
messages are F || A and F || B of 1024 t + 55 and 1024 t + 63 toy bytes with
t = 1 to 255, F being t chunks of zero bytes; the last chunk is compressed with
counter t and flags 3, and t = 0 is dropped (79.3 million of 20.3 billion
trials, one in 256, as expected). The inner word d1 runs over the values of the
heaviest beta of each set, the toy form of c1 in Q*. Both last-chunk
compressions of every trial were evaluated in full and all eight words
compared, with no rule and no filter; every collision was rebuilt as two
complete messages and confirmed by two independent toy tree hashes, one of them
written after the organizer's code. The predictions are exact model counts for
each set. Over the eight sets:

| Arrangement | Collisions found | Predicted | Trials per collision |
| --- | ---: | ---: | ---: |
| root instance (counter 0, flags 11) | 67 | 64.0 | 8.8 * 10^8 |
| counter, d1 in the set of the heaviest beta | 251 | 255.0 | 8.1 * 10^7 |
| counter, d1 not restricted (control) | 54 | 47.8 | 8.2 * 10^8 |

All 372 collisions are collisions of complete messages, and no trial failed a
check. The realised fraction of the predicted gain of the prescription is (251
/ 255.0) / (67 / 64.0) = 0.94 +- 0.13, that is -0.09 +- 0.20 bit: no loss is
detected. The control shows that the counter alone, without the prescription,
changes nothing. This tests the mechanism with real collisions. It does not
test the size of the factor at 32 bits, which the toy cannot reach (its factors
are 3.9 to 31.8 on the eight sets, against 853.61 here), and it has no rule A,
no sub-class and no packed batch.

**Real messages in passing outer steps.** A participant measurement made for an
earlier entry of this search, untrusted evidence like the two paragraphs before
it, which the organizer's harness does not run. On a graphics card a helper
agent ran the counter construction on real 32-bit messages with Y4 in the
sub-class. Uniform random outer steps, drawn by the measuring program, were
filtered by conditions (1) and (2) with tables generated as the earlier program
generates them, and every passing outer step enumerated the whole of Q*, all
2^21 values of c1 in the earlier program's member order, as 299,594 packed words
of seven lanes: 2^22.00 passing outer steps, 2^43.00 trials. A control with the
filter off ran 2^18 outer steps, 2^39 trials. On 330 records a check against the
earlier program (step CO, the filter, the member order, rule A and the word n of
the E1 test from its compression of the real last chunks) found no difference.
Errors are taken per outer step, because the trials of one outer step cluster.

| Event | Over all outer steps | In passing outer steps | Ratio |
| --- | --- | --- | --- |
| outer step passes the filter | 2^-9.8132 (pi, exact) | 2^-9.8127 | z = +0.7 |
| rule A, per lane | 2^-8 | 2^-8.000 | 1.0003 +- 0.0006 |
| E1 test of Lemma N passed, per trial | 2^-26.02 | 2^-26.023 | 0.9945 +- 0.0031 |
| listed E1 outcome, per trial | 2^-31.694 | 2^-31.724 | 0.979 +- 0.022 |
| listed partial E3 event, per trial | about 2^-32.4 (control, 98 events) | 2^-24.17 | about 2^8 |

So inside passing outer steps rule A and the E1 test keep their values over all
outer steps, and the listed E1 outcome keeps its value within its error. Per
outer step the count of trials that satisfy rule A has standard deviation 9,785
against a mean of 8,195: the trials that satisfy it cluster. Over the 12
patterns of the filter's masks with at least 40,000 passing outer steps each,
rule A lies between 2^-8.006 and 2^-7.996 and the E1 test between 2^-26.08 and
2^-26.00. The partial E3 event, a condition on E3 like (1) and (2), is
concentrated by the filter, as expected. Trials with t = 0 were not dropped, at
most one per outer step. These measurements bear on H4' and on the rate of H1'
inside passing outer steps; they reach no event deeper than about 2^-31.7 and
no collision.

**Real counter trials on the whole class.** A participant measurement made for
the class, untrusted evidence like the paragraphs before it, which the
organizer's harness does not run. On a graphics card a helper agent ran the
counter construction on real 32-bit messages in two classes of one build: the
whole class of eta (all 2^19 members, no rule, the filter of the fourteen
outcomes of beta*), and as a control the sub-class of entry 26ebba63 with rule A
and the seven-outcome filter. Each run walked 2^35 uniform random outer steps
and enumerated all of Q* in 2^25 of its passing outer steps, 2^46 trials per
class; the passing steps kept are the first in the order of the card's atomic
counter, which does not depend on their content, and the pass share uses every
walked step. Before the runs, the filter tables were compared with the earlier
program's construction, 1,000 members of each class with the member lists, and a
sweep of all 2^32 values of tau and of eps at beta* showed that the counters
list exactly the fourteen and the seven outcomes of 10.1; no trial lacked the
difference beta*. The counters are the E1 outcome and the filter; errors are
clustered by outer step. The model per trial is the sum of L_j over the listed
outcomes times 2^-85 (2^-96 for the triples times 2^11 for c1 in Q*).

| Event | Exact model | Measured | z |
| --- | --- | --- | --- |
| E1 outcome among the seven of entry 59f8915e, whole class | 53 * 2^-38 = 2^-32.2721 per trial | 2^-32.2692 (13,595 events), 1.0020 +- 0.0086 of the model | +0.23 |
| the same, sub-class control | 2^-32.2721 | 2^-32.2540 (13,739 events), 1.0126 +- 0.0086 | +1.46 |
| ratio whole class / sub-class, the seven | 1 | 0.9895 +- 0.0120 | -0.87 |
| E1 outcome among all fourteen, whole class | 79.5 * 2^-38 = 2^-31.6871 | 2^-31.6888 (20,328 events), 0.9988 +- 0.0070 | -0.17 |
| share of the seven new outcomes among the fourteen, whole class | 1/3 | 0.3312 +- 0.0033 | -0.64 |
| fourteen-outcome filter passes, whole class | 2^-7.5320 (exact) | 2^-7.5321, 0.99990 +- 0.00007 | -1.38 |
| seven-outcome filter passes, sub-class control | 2^-9.8132 (exact) | 2^-9.8130, 1.00012 +- 0.00016 | +0.74 |

Every measured quantity matches the exact model within 1.5 clustered standard
errors, and the clustered error of each E1 rate equals its Poisson value: no
excess clustering of E1 outcomes by outer step. For this package the first row
is the one that bears on the rate: the E1 rate of the seven outcomes of entry
59f8915e, with members drawn from the whole class and no rule, in trials of
passing outer steps of the fourteen-outcome filter, which contain every passing
outer step of the filter for S (Lemma F); it equals the rate of the same seven
outcomes on the sub-class with rule A, as the model says. The counter covered
the seven outcomes together: the E1 event of S, six of them, is a sub-event of
the measured event, with model rate 52 * 2^-38 per trial, 52/53 of it, and it
was not counted on its own. The run has no counter of the E3 side and none of
the joint event: the E3 count of these outcomes on the class (N3_j four times
that of the sub-class, 10.1) and the joint event of H1', about 2^-91 per trial,
are not measured, and the seven-outcome filter was run only in the sub-class
control. These measurements bear on H1' and H4'; they reach no collision.

**Real outer steps for the pre-check and the budgets.** Participant measurements
made for our entry 415e792c, untrusted evidence like the paragraphs before it, which
the organizer's harness does not run. Helper agents walked real outer steps of
the counter construction on the whole class (all 2^19 members, no rule), drawn
from Python's generator, with the participant's program of the class measurement
(step CO and the automata of the fourteen outcomes, their masks restricted to
S), and computed nu by (V) on every outer step whose X is not zero. Errors are
binomial over outer steps, which are independent.

| Event per outer step | Nominal share | Count | Ratio to nominal | z |
| --- | --- | ---: | --- | ---: |
| I_E, mask of (2) meets S; 60,000,000 steps | 2^-4.199822 | 3,266,224 | 1.0004 +- 0.0005 | +0.72 |
| I_2, X not zero; the same steps | 2^-9.978162 | 59,367 | 0.9980 +- 0.0041 | -0.49 |
| I_3, T not zero; the same steps | 2^-11.978162 | 15,055 | 1.0123 +- 0.0082 | +1.50 |
| I_2; 30,000,000 other steps (seed 7) | 2^-9.978162 | 29,688 | 0.9981 +- 0.0058 | -0.32 |
| I_3 among those passing steps | 1/4 | 7,452 (0.25101) | 1.0040 +- 0.0101 | +0.40 |

On the 60,000,000 steps the share of passing outer steps that survive the
pre-check is 0.2536 +- 0.0018 (z = +2.0); over both runs it is 22,507 of 89,055,
0.2527 +- 0.0015 (z = +1.9), and the count of I_3 is 1.0089 +- 0.0067 of its
nominal value. On the 30,000,000 steps, among the outer steps that pass the
fourteen-outcome filter, nu has chi-square 9.99 on 7 degrees of freedom against
the uniform law, and 16.04 on 14 against the group of the mask. Every measured
share is within its errors of its nominal share (the clauses of H4' rest on the
preregistered sample below); I_3 has no budget in this package, and it bears on
H5' only through the mean of C(T), measured below. These are two runs of one
generator, made after the design; they are not a proof that the sampler's nu is
uniform or independent of its masks. The program of the 60,000,000 steps is
research/pkg21/work/E/lean_share.py of the participant, not part of the package.

**Real outer steps walked by contexts (the member loop).** A participant
measurement made for this package, untrusted evidence like the paragraphs before
it, which the organizer's harness does not run. The participant's
reimplementation of the member loop of entry e9b6649e (9.8;
research/impl/memberloop of the participant, its own SplitMix64 generator, one
run made after the design) walked 120,000 contexts, each with all 2^19 members
of the class, 62,914,560,000 outer steps, on a graphics card, and counted per
context the passing outer steps and the lanes whose mask of (2) is not zero.
With m = 2^19 and p the exact share:

| per context | passing outer steps | lanes with a nonzero mask of (2) |
| --- | ---: | ---: |
| mean count, against m p | 519.013 against 519.809 (0.99847) | 28,491.98 against 28,529.72 (0.99868) |
| z, with the standard error of the 120,000 counts | -1.36 | -1.21 |
| ratio (E[n(n-1)]/E[n]) / ((m - 1) p_hat), p_hat the observed share | 1.152 | 1.144 |

Both shares agree with their exact values within the error of the clustered
counts, as Lemma CX (c) says the means must. The same reimplementation checked
the two lists of Lemma Y and compared the 25 member lines and the masks with the
full step CO on 100,000 pairs, and the omega-first batch was compared with the
full member loop on every outer step of a run of 62,914,560,000 outer steps
(9.8).

**Clustering by context at every depth (participant measurements).** Untrusted
evidence for part (ii) of H1' (10.3), made after the design and not
preregistered. For each event below, every listed good trial meets it; n is its
count in one context of m = 2^19 members, p_hat its observed share per member,
and the ratio (E[n(n-1)]/E[n]) / ((m - 1) p_hat) is 1 when the members of a
context are independent. Each run has a control arm: as many blocks of 2^19
independent outer steps (eight fresh words each), with the same statistic. All
arithmetic is exact on 32-bit words, on a graphics card. Before the runs, 23,000
vectors were compared with the participant's Python code on Y9, omega, C2.c1,
C2.b1, both masks, nu and the pre-check, with no difference; every outer step
that the pre-check kept (15.6 million per arm) was rebuilt on the processor and
passed to the Python solver with (G7) and the pre-check, and every root to the
certificate; in the root runs the recorded steps reproduced the counts of every
block, and a re-run of the first 32,768 blocks was byte-identical.

| event of an outer step, per context | contexts | ratio, contexts | ratio, control |
| --- | ---: | ---: | ---: |
| condition (1) alone | 120,000 | 1.000175 | 1.0000 |
| condition (2) alone | 120,000 | 1.1433 +- 0.0008 | 1.0000 |
| passes the filter | 120,000 | 1.1513 +- 0.0009 | 1.0000 |
| passes and the pre-check keeps an outcome | 120,000 | 1.1572 +- 0.0010 | 1.0000 |
| the solver reaches a leaf | 120,000 | 1.153 +- 0.003 | 0.998 +- 0.002 |
| the solver returns a root | 46,104,576 | 1.2486 +- 0.0806 | 1.0367 +- 0.0718 |

The errors are over groups of contexts (12 groups of 10,000; for the root a
jackknife over 100 groups). Relative to the event above it, the pre-check adds a
factor 1.00518 +- 0.0002 and the leaf 0.996 +- 0.002, and at the cuts of the
solver between the leaf and the root the ratio stays between 1.14 and 1.25 with
no step beyond its error. Contexts with two outer steps that return a root: 252
against 201.4 for independent members and about 248 at a ratio of 1.233; in the
control 208 against 200.3; none with three in either arm. The clustering comes
from condition (2): omega = Y3 + y + w8, and w8 depends on the context only. No
root of these runs passed the certificate of step 3 (0 of the 763 roots of the
120,000-context runs): no listed good trial is observed, and the ratio of listed
good trials themselves is not measured. The runs are
research/impl/memberloop/deep and research/impl/memberloop/roots of the
participant (seeds 1001 and 3003 for the contexts, 2002 and 4004 for the
controls), not part of the package.

**Clustering of the deepest events across members: a preregistered run.**
Untrusted participant evidence for part (ii) of H1' (10.3). Before any step ran,
a protocol file, PREREG.txt of the participant (SHA-256
248838947f505b89c3927b7da829548acef92a540e474a9eefe3bd04c06cb92e, rechecked
after the run), fixed the events, the arms, the statistics, the decision rule,
the size rule and the seeds. Each arm has 262,144 contexts, each walking all
2^19 members with 512 values of c1 per outer step, a random affine subspace of
Q*, so 2^46 trials per arm, from two generators (Philox4x32-10 and SHA-256 in
counter mode); the control arm draws fresh outer words for every outer step. For
the count n of an event in a context, the ratio (E[n(n-1)]/E[n]) / ((m - 1) p)
splits into a part from pairs within one outer step and the cross-member factor
Rx from pairs of different members, which is 1 for independent members. The
graphics-card code matched a Python reference on 1,179,648 trials with no
difference, and all 32,199 recorded hits of the two deepest events were
recomputed with real compressions.

| event, per trial | share | Rx, contexts | upper limit U | Rx, control |
| --- | ---: | ---: | ---: | ---: |
| listed E1 outcome: tau in S, eps = eps*, beta = beta* | 2^-32.29 | 0.999 +- 0.054 | 1.162 | 1.068 +- 0.064 |
| (J1) and (J2) of the E3 half, for an outcome of S | 2^-34.58 | 0.90 +- 0.24 | 1.94 | 1.12 +- 0.27 |
| R24: low 24 bits of the difference of chaining-value word 1 zero | 2^-23.76 | 1.0002 +- 0.0001 | 1.0006 | 1.0001 +- 0.0001 |

U is Rx plus three standard errors (a jackknife over 128 groups of contexts), or
the 99.865 per cent Poisson limit when fewer than 30 cross-member pairs occur
(13 for the E3 event). Only the filter events cluster by context: test (2)
1.1439 +- 0.0004 and the pass 1.1522 +- 0.0005, against 1.0000 in the control.
Every upper limit lies at least 42 bits below the factor 2^43.86 that part (ii)
allows at this run length (2^44.21 at the run length for which the run was
preregistered). Limits: the joint event, about 2^-91 per trial, is not reachable
and the two halves are measured separately, so carrying Rx near 1 to it remains
the premise. The run is research/impl/memberloop/prereg8 of the participant, not
part of the package.

**The mean of H5' with the guard (G7): a preregistered sample.** A participant
measurement made for this package, untrusted evidence, which the organizer's
harness does not run. Before any outer step of the main sample was drawn, a
protocol file, PREREG.txt of the participant (SHA-256
92d16cda1cd13aacb287470b968ff2d914362b12fefb680c94960280a7471131), fixed the
statistic, V = C(T) with (G7) for every outer step, with nu by (V) and T = X
AND VMASK[nu], zero when T is empty (the ledger of 10.3 with the trees with
(G7), 1,280 per row); the model mean cbar = 582,173,006,981,436 / 2^47, rebuilt
in integers with every line of the table of 10.3 and the sum
4,657,384,055,851,488 asserted; the cap 31,456; the seeds; the decision rule;
and a timing rule for the sample size. The rule: SUPPORTED at eps when the
one-sided upper bound on the ratio of the mean of V to cbar, by the empirical
Bernstein bound at delta = 0.00135 with range 31,456 and by a bounded
Kullback-Leibler bound, is at most 1 + eps. The sampler is the earlier
program's outer step of the whole class (all 2^19 members, no rule), translated
line by line into a graphics-card kernel, with the words from Philox4x32-10
keyed by seeds derived by SHA-256, none of which a scan of the participant's
36,311 files found elsewhere. On separate seeds the kernel matched the
unchanged Python code on every field of 65,536 outer steps, and in the main run
on the first 4,096 outer steps of each of its eight streams. The sample ran
once, with no interim look, and the eight streams were pooled.

| Quantity | Value |
| --- | --- |
| outer steps | 549,755,813,888 (2^39) |
| sum of V | 2,274,013,943,520 |
| mean of V | 4.136407 (model 4.136588) |
| ratio to cbar | 0.999956 +- 0.000089 (z = -0.49) |
| upper bound of the ratio, empirical Bernstein | 1.000297 |
| upper bound of the ratio, bounded KL | 1.000384 |
| largest V | 31,456, the cap |
| passing outer steps kept by the pre-check | 136,255,727 of 545,067,537, 0.249980 (z = -1.10) |

Both upper bounds are below 1.01: by the rule fixed in advance the sample
supports H5' at eps = 0.01. Its exact counts of the two indicators of H4',
29,915,698,553 lanes with a nonzero mask of (2) and 545,067,537 passing outer
steps, give the factors of H4' (10.3). Checks fixed in the protocol: nu by (V)
against a separate computation of it in every outer step, with no difference; no
mask pair outside the support of the model; and, after the run, the protocol
file and the 22 files it lists with their recorded hashes. Diagnostics:
545,067,537 outer steps passed the filter for S against 545,059,418 expected (z
= +0.35); the 10 cells of T with positive weight give chi-square 9.84 on 9
degrees of freedom; the means of the eight streams lie between 4.13515 and
4.13819. This is statistical evidence from one pseudorandom generator for the
single moment of H5', not a proof of it, and it does not test H1' or H4'; V is
the proved cap C(T), and the solver itself was not run. The sampler, the
analysis and the protocol are research/pkg19/as_subset/prereg7 of the
participant, not part of the package.

**Real outer steps for H5' (a preregistered sample).** A participant measurement
made for our entry 415e792c, untrusted evidence, of the mean of V without the
guard (G7). A protocol file, PREREG.txt of the participant (SHA-256
c862bfb1082e5236b0d9d81d6daef38e5f1135b27b25ad5c0093a1bf76455872), written
before the main sample, fixed V = C(T) without (G7) for every outer step, the
model mean cbar = 611,713,706,062,329 / 2^47, the cap 37,032, the seeds, a
timing rule for the sample size and the decision rule of the sample above. The
sampler drew 2^28 = 268,435,456 real outer steps of the whole class with
Python's generator (MT19937) from 32 seeds derived by SHA-256, once, with no
interim look. The mean of V was 4.322858 against 4.346487, ratio 0.99456 +-
0.00405 (z = -1.34), with one-sided upper bounds 1.01059 (empirical Bernstein,
delta 0.00135, range 37,032) and 1.01513 (bounded KL); the largest V was 37,032,
the cap; nu by (V) agreed with a separate computation in every outer step; and
the pre-check kept 66,047 of 265,543 passing outer steps, 0.24872 (z = -1.52).
Through the ratio 723/715 of 10.3 it bounds the mean with (G7) by 1.0786 times
cbar, a weaker bound, from another generator, than the sample above. The
sampler, the analysis and the protocol are research/pkg19/as_subset/prereg6 of
the participant, not part of the package.


**A preregistered toy run of the rate margin.** Untrusted participant evidence
for the margin 11/10 of H1' (i), made for this package. Before any step of the
main run, a protocol file, PREREG.txt of the participant (SHA-256
c5895dd64b07710f9fb386b0f9d4f6b5cb38b14b502a4cc80e51c60584432a4e, rechecked
after the run), fixed the code of the scaled-down counter arrangement of the
end-to-end run above (8-bit words, its program unchanged and a graphics-card
port of its outer step), eight constant sets with their heaviest beta, the exact
model prediction per counted trial, the seeds, a timing rule for the sample size
and the decision rule: SUPPORTED when the one-sided 97.7 per cent exact Poisson
lower bound on found / predicted is at least 1/1.1. Before the protocol was
fixed, the port reproduced all 251 collisions of the earlier run line for line.
The main run, 40,960 runs and 3,235,715,578,385 counted trials, ran once with no
interim look and found 40,882 collisions of complete messages against 40,800.63
predicted: ratio 1.00199 +- 0.00496 (z = +0.40), lower bound 0.99213 >= 1/1.1 =
0.909091, SUPPORTED. An independent Python tree hash confirmed 40,882 of 40,882.
Limits: this is 8-bit evidence for the realised-to-model ratio of the counter
arrangement; it does not test the 32-bit factor, the filter or the joint event,
and its words come from a pseudorandom generator. The run is
research/impl/toy8_prereg of the participant, not part of the package.

**The declared experiment, run by the participant.** Untrusted participant runs
of experiments/frontline.py (6.4), outside the organizer's harness. Size: 61,222
bytes of program and 3,720 of manifest, 64,942 of the 65,536 allowed; ASCII;
imports hashlib, json, math, struct and sys only. In the organizer's image
python:3.12.12-slim-bookworm with the runner's limits (1 CPU, 128 MB, read-only,
no network), four seed sets of 256 trials, twice each, took 5.4 to 5.9 seconds,
container start included; the largest memory seen was 29 MB; the output replays
byte for byte. On the public request: 3,690 of 8,192 clusters opened (0.450),
122,582 members walked, 13,481 lanes with a nonzero mask of (2), 225 passes, 64
solver calls and no root; 428,544 checks, 0 mismatches and 0 skipped passes; all
256 returned pairs agree on digest words 0, 2, 5 and 7 under the organizer's
verifier/blake3.py, and all 256 are distinct. On 4,096 trials: 58,136 of 131,072
clusters opened (0.4435, below the bound 0.4594 of Lemma OR), 229,018 lanes with
a nonzero mask of (2) among 4,194,304 cluster members (0.0546), 3,998 passes,
1,031 solver calls, 0 skipped passes and 0 mismatches. The self-test checks the
program's constants against its formulas, both automata against brute force at 8
bits, T1 and T2 against bit-serial decisions on 8,000 random words, Lemma A9,
the cluster map and each of the four halts at its threshold; an always-open gate
gives the same lanes and passes as the table. A gate on one borrow only, or with
one key bit flipped, gives 339 or 252 skipped passes. In a separate test, 6,000
of 6,000 planted roots were returned by both traversals. Not exercised: no root
of the search occurs at this scale, so the 256-bit test of a certified pair
never runs; the solver is checked on the planted roots and the predicate of step
3 against real compressions on the charts of step CT; a trial walks 32 of the
16,384 clusters of its context; the budgets and the credit are never reached;
the machine layout of 9.9 is not modeled, and the units are added per event.

**What does not exist.**

- No organizer digest check of the counter instance (6.4): the organizer can
  hash only the root instance. The program checks the counter instance in its
  own run against its own compression (6.4), and Section 7 adds participant
  computations with the organizer's functions imported.
- No measurement of the joint event of H1', at about 2^-91 per trial; the
  deepest counter events measured are the listed E1 outcome at 2^-31.7 and that
  outcome together with rule A, 55 events at about 2^-39.8. No separate count of
  the E1 rate of the six outcomes of S: it is a sub-event of the measured seven.
- No proof of the open parts that H1' declares (10.3), of the shares of the two
  counts of H4' or of the mean of C(T) of H5'; these are measured (above), the
  mean with (G7) on a preregistered sample of 2^39 real outer steps.
- No measurement of rho_x or of the clustering ratio v of listed good trials by
  context (10.3), which no run of feasible size can observe; the ratio was
  measured for the events that every listed good trial meets, from the filter to
  the roots of the solver, and its cross-member part, preregistered, for the two
  halves of a listed good trial (above).
- No root of the search at the scale of a trial, and no complete message of a
  found pair: the program's 256-bit test never runs on a root of the search, its
  solver is checked on planted roots and the predicate of step 3 on charts of
  step CT (Section 13), and the complete messages hashed (Section 7) are trials,
  with t from 1 to 16,383.
- No count of machine operations of the search: the program of 6.4 adds the
  charges of Section 11 per event, and every row of Section 11 is bounded in
  words, except the batch, whose 67 units with two list addresses participant
  programs executed and counted (9.8), and the counted 295 of the rebuild of a
  passing lane (9.6); the machine layout of 9.9 (the pair words, the eight
  reserved registers, the 37 caller words) is specified, not run. The program's halt
  constants are those of the search at the rate factor 5/7 (9.1), and no trial
  reaches a budget or the credit.

**Limits of the evidence.** H1' is an assumption (10.3); beyond it:

- M fails inside one context and one outer step: the count of rule A per outer
  step has a variance 572 times its mean. Where it was measured it holds on
  averages over outer steps. The counter search fixes Y4, Y9, w8, Y12 and w5 for
  the 2^21 trials of an outer step; a context, in turn, holds its seven outer
  words fixed for all its 2^19 outer steps. Success therefore comes from many
  independent contexts, 2^50.117 of them, with 2^69.117 outer steps walked,
  about 2^59.14 of them passing and 2^57.14 reaching the solver, and it rests on
  the premise that a context rarely holds more than one listed good trial.
- The shares of H4' and the mean of H5' are measured on pseudorandom generators,
  and the quarter share of the pre-check and cbar are exact only in a model with
  nu uniform; none of them is proved for the sampler. Lemmas F and VP need no
  law of the words, and the time bound needs none either: a reached budget or an
  exhausted credit halts the run, which lowers the success probability and not
  the time bound.
- The model is checked on real messages to about 2^-40, not at 2^-91; the
  scaled-down whole-collision run of the counter arrangement is level (0.94 +-
  0.13 of the predicted gain).
- The constants and the class were chosen by the count, and beta* with them, so
  they favour any choice that the model overrates; S was chosen by the charge.
  The six outcomes of S carry 41.7 per cent of the count of the class, with one
  value of eps. Most measurements of this section are on the sub-class and the
  seven outcomes of entry 26ebba63; on the whole class the E1 side of those
  seven outcomes, which contain S, was measured (2^46 trials), and their E3 side
  was not.
- The count rests on programs that are not in the package and on a list of
  values of beta that is complete only by uncertified solver answers and the
  other model's enumeration.
- Helper agents of the participant wrote and checked the counter construction,
  the filter and this text, and another AI model proved Lemmas IP, F and S1 to
  S9 and derived the count of passing pairs; no person has read it.

**Scope and limitations.**

- No full collision is exhibited; this is an analytical cost claim, and the
  search tests each trial against zero, needing no memory that grows with the
  trials.
- The messages have 1024 t + 55 and 1024 t + 63 bytes, with 1 <= t < 2^32 the
  solved chunk counter, about 2^41 bytes on average and fewer than 2^42;
  computing their digests costs about 2^37 compressions, which is charged. They
  rely on the chunk counter and the true block length being inputs of the
  compression, as the target profile specifies; the colliding compression is
  that of the last chunk, which is not the root, and Lemma TR carries the
  collision to the complete digests in the profile's own tree mode.
- The gain over a birthday search comes from matching half the chaining value by
  construction, the prescription of c1 in the cube of beta* that the solved
  counter makes possible, assumed at 125,920,632,087 times the uniform rate,
  work shared per context and per outer step, the cluster gate, which skips only
  clusters whose every member fails test (2), the outer filter, which passes
  about one outer step in 2^9.98 without losing any success with an outcome of
  S, the pre-check and the joint solver: 2^90.117 trials walked, at most
  2^80.140 of them in passing outer steps and, at the nominal shares, about
  2^78.14 in outer steps that reach the solver.
- A brief literature search found free-start collisions and near-collisions of
  reduced BLAKE compression functions and no collision attack on 2-round BLAKE3.
  No priority or novelty claim is made.
- The time bound charges every operation, load and store of the machine of
  Section 11, every row at the budget or the credit at which the run halts: an
  upper bound under that convention, not a measured time; the program of 6.4
  adds the same charges per event, and the organizer does not recompute them.
  Its largest term is the search part; the selection procedure SEL of Section
  12, charged in full, is 2^-9.702 times it.

**Field meanings.**

- time_log2 = 63.9016 bounds total charged time by 2^63.9016 units (Section 11):
  log2 T = 63.90154718710604..., the search below 2^63.8999 units and the
  selection procedure SEL, charged in full, below 2^54.198 (Section 12).
- memory_log2_bytes = 44 bounds the storage of the selection procedure (below
  2^35 bytes), the search, its code and direct tables included (below 2^39
  bytes), and the output (below 2^43 bytes), even all held at once: 2^43 + 2^39 +
  2^35 < 2^44 (Section 12).
- preprocessing_log2 = 55 bounds the selection procedure SEL of Section 12 by
  2^55 target-compression units (fewer than 2^62.946 primitive operations).
  Every search of SEL runs over a stated range and every program run in it
  halts at a stated cap, so this is a bound by construction, with no premise;
  that SEL returns exactly the stored values rests on the participant's logs
  (Section 12).
- nonuniform_advice_log2_bytes = 7 bounds the stated advice record of Section
  12, the constants, eta, beta* with its cube, the seven values of tau with eps
  of the outer filter's automata and the mask of S, 73 bytes, by 128 bytes.
- success_probability = 0.39 holds under H1', H4' and H5', stated for the
  advice record, as shown in 10.4; it uses only properties of the record that
  this text verifies exactly (Section 12).

The required baseline_improved identifier blake3-r2-nominal-v2 names the
organizer's nominal display reference 128, not an established attack, qualified
baseline or security bound; the claimed 63.9016 lies below it. Whether a
qualified result improves the Yukon incumbent is decided separately; no Pareto
dominance claim follows.

## 14. Corrections to our entry c66f230d

Twenty-four points raised after entry c66f230d (97.6) was filed change none of
its lemmas, its count or its claim; this text applies the corrections wherever a
passage recurs.

## 15. Earlier entries

One line each: the entry of the participant, its time_log2, its ruling or status
when this text was written, and what this text keeps from it. New here against
entry 415e792c are the member loop over contexts with the direct tables (after
entry e9b6649e of hecmas, 65.3643), the guard (G7) with the credit at its exact
mean, the omega-first batch, the E count in a register, the root certificate of
four one-word tests, the guard (G15) and the global ledger of 1,024 with the
credit scaled by 16/27, the selection procedure SEL charged as preprocessing at
its cap (Section 12), the cluster gate (9.9), the reserves of the budgets and
the credit with the margins of GPT Sol's answer CK (9.1, 10.3), and a program
that runs the search in the organizer's sandbox (6.4).

| entry | time_log2 | ruling | kept in this text |
| --- | ---: | --- | --- |
| c66f230d | 97.6 | in review | the constants, eta, Fact P, Lemmas L, H, Q, T and N (Section 14) |
| 64c075ac | 92.53 | not evaluable | the root instance of Sections 4 to 6 and the machine of 6.5 |
| e7b17fd1 | 84.98 | in review | the counter construction, Lemmas TR, CT, IP, S1 to S5 and S8 |
| 26ebba63 | 71.39 | in review | the filter, the joint solver, H1', H4' |
| 59f8915e | 67.8004 | in review | the whole class, (P*), Lemma J0, the families of the solver |
| 415e792c | 66.8050 | in review | S, the pre-check, the credit with H5' |
| 0bc5f130 | 66.8751 | in review | the guard (G7) with its trees, ledger and caps |
| 11ccf5a7 | 70.21 | not evaluable | nothing |
| e85fffe8 | 75.4217 | not evaluable | nothing; the advice record of Section 12 |
| 78ac164c | 71.7481 | not evaluable | nothing; the advice record of Section 12 |

## 16. Credit

*For this package.* Everything in this package is entry a402a477 (Jbenisek and
the people and models credited below), except the register layout of an opened
cluster of 9.9 and its charges in Section 11 and 6.4: keeping the seven words of
the representative batch and the opened count in reserved registers instead of a
memory frame and a memory word, with the passing lane saving them. That change,
its register count, the recomputed ledger and the edits of this text are the
work of **Claude Opus 5.5 (Anthropic), run in Devin** by the submitter of this
package (0xshikhar). Holding a count in a register in place of memory follows
the E count of GPT Sol's answer CD 8 in entry a402a477. Jbenisek and the others
credited below have not reviewed this package. Dependency declared: a402a477.


One line per contributor. Apart from the helper agents of the participant,
nobody named here has reviewed this package, and a credit is not an endorsement.

- **hecmas**, entry e9b6649e: the member loop over contexts, the two direct
  tables of the filter and the restatement of the premises for contexts (9.8,
  10.3, described in the participant's words).
- **Th0rgal**, entry 77818485: the credit of the solver at the exact model mean
  of the capped work with (G7), 582,173,006,981,436 / 2^47 (9.1, 10.3); earlier,
  the member values built once per outer step (entry df8bd46d) and three coding
  steps of 6.5 (entry 8c81a219).
- **GPT Sol 6.1 (OpenAI)**, an AI model run by the participant: the cluster gate
  with Lemmas KP, A9 and CL, its table, layout and charges (answer CI 1), its
  opened-cluster budget on the bound of Lemma OR and the layout cuts of 9.9
  (answer CJ), the sharper opening bound by blocks of sixteen, the reserves of
  the budgets and the credit and the margins of H1', H4' and H5' (answer CK),
  the omega-first batch and its audit, the E count in a register with the frame
  of a passing lane, the global ledger of 1,024 and the credit scaled by 16/27
  (answers CA and CD), the root certificate with Lemma RC and the guard (G15)
  with Lemma G15 (CF 6 and 7), the guard (G7) with Lemma G7 (AX 1), the
  pre-check, the budgets and the credit with H5' (AW), the joint solver with its
  certificates, guards and caps (AE to AT), Lemmas F and S9 (AC), Lemmas IP and
  S1 to S8, and the sub-class and rule A of the root instance.
- **Jbenisek**, the participant who files this package: the half-collision, the
  class search and the counter construction of the participant's entries from
  17bba2ae on (Section 15), among them the guard (G7) in this solver (0bc5f130).
- **The participant who filed entry dd91b2f6**: dropping the sub-class and rule
  A in the solver design, and the fourteen outcomes of beta* on the class;
  nothing of that entry is used.
- **winglock**: searching only a sub-class of members chosen by an exact count
  (entry 18a7fc52), which the sub-class of the root instance follows.
- **5kyguy**: keeping masks in registers across the loop over the members (entry
  404d14df).
- **tekkac**: the lane layout of 6.5, seven 36-bit lanes with a masked rotation
  (public ticket 2bf40fb).
- **Grok 4.7 (xAI)**, run by the participant: the hostile review of entry
  c66f230d (Section 14).
- **GPT-6 Luna**, on the owner's server: the proof of Lemma OR, the bound on the
  opening rate of the cluster gate (9.9), restated here in the participant's
  words; earlier, a search for better pinned constants, which found none.
- **A model reached through the service Venice**: a statement on prior art,
  unverified and used in no proof or figure.
- **Helper agents of the participant**, instances of the AI model that wrote
  this text: the program of the declared experiment (6.4), the reimplementation
  of the member loop and its measurements, the omega-first batch with its
  op-counting simulation, the integer recounts, the price with its integer test,
  the count of Section 17, the measurements of Section 13, and this text.

## 17. The counting program for 67,633,152

The program below computes the part of beta* = 18b0e098 in the rate of the
class of eta (Section 10.1), outcome by outcome, in exact integer arithmetic,
with the standard
library only: every tau (taus), both roots eps (eps_roots), the E1 count L_j
(L_count) and the E3 count N3_j (N3_count), each as an exact carry count over
all bit positions, with Y4 over all 524,288 members of the class (Lemma Q) and
no rule on h1. Nothing is sampled, capped or delegated to a solver. It is the
program printed by entry 26ebba63 with these changes only: the header comment,
the member list (the class in place of the sub-class) with its size check, the
empty rule, and the final check. Run as `python3 -B count.py`, it printed the
outcome table below in about 2.5 minutes (Python 3.14). Its column L*N3/2^81
is four times the last column of the table of 10.1; its column "rule A" is the
count with the empty rule and equals N3 in every row. Its self-test, a brute
force at width 6 that follows the listing in the file, ran 12 seeds with no
mismatch. The program prints all fourteen outcomes of beta* on the class and
their sum; this package lists the six outcomes of S, and only their rows are
shown below, in the program's order. They sum to 270,532,608 = 4 * 67,633,152 on
the program's scale 2^81, that is 67,633,152 on the scale 2^83 of a trial with
Y4 uniform in the class (10.1). The eight rows that are left out, 675020a0 and
the seven with tau ending in 5060a0, sum to 16,261,120 = 4 * 4,065,280 and are
listed, with their L_j and N3_j, in the table of 10.1; the sum and check lines
of the program, which follow the rows, are those of all fourteen.

```python
#!/usr/bin/env python3
# Exact count of the part of beta* in the rate of the WHOLE class of eta, no rule filter.
# (pkg17 copy of research\pkg12c\draft\count.py: only the member list, the rule and the checks changed.)
# Integer arithmetic only on the count; no sampling, no cap, no solver; standard library only.
# Run: python3 -B count.py [--beta HEX]   (--selftest: brute force at width 6, below the listing)
import sys, time
from collections import Counter
from functools import lru_cache
from itertools import product

class Inst:                                     # word width, rotations of G, constants
    def __init__(s, n, r16, r12, r8, r7, Y3, Y3B, Y11, Y11B, delta, eta, Y4s, rule):
        s.n, s.m, s.r16, s.r12, s.r8, s.sh = n, (1 << n) - 1, r16, r12, r8, r8 - r7
        s.Y3, s.Y11, s.delta, s.eta, s.Y4s, s.rule = Y3, Y11, delta, eta, Y4s, rule
        s.DY3, s.DY11 = (Y3B - Y3) & s.m, (Y11B - Y11) & s.m

def ror(c, x, r): r %= c.n; return ((x >> r) | (x << (c.n - r))) & c.m
def rol(c, x, r): return ror(c, x, c.n - r % c.n)
def wt(x): return bin(x).count('1')
def subs(X):                                    # every p with p AND NOT X = 0
    p = X
    while True:
        yield p
        if p == 0: return
        p = (p - 1) & X
def sgn(c, p, X): return (X - 2 * p) & c.m      # (v XOR X) - v for every v with v AND X = p
def pats(c, X, d):                              # every p in subs(X) with sgn(p, X) = d
    w = (X - d) & c.m
    if w & 1 or (w >> 1) & ~X: return []
    top = 1 << (c.n - 1)
    return [w >> 1, (w >> 1) | top] if X & top else [w >> 1]
def bit(x, i): return (x >> i) & 1
def adv(S, base, plus_ok, minus_ok):            # one digit of a sum checked to be 0 mod 2^n
    return {(base + cy + x - y) >> 1 for cy in S for x in range(plus_ok + 1)
            for y in range(minus_ok + 1) if (base + cy + x - y) % 2 == 0}

def eps_roots(c, beta):                         # eps XOR ror(eps, sh) = ror(eta, sh) XOR beta
    y = ror(c, c.eta, c.sh) ^ beta
    return [e for e in (solve(c, y, 0), solve(c, y, 1)) if e is not None]
def solve(c, y, x0):                            # needs gcd(sh, n) = 1
    x, i = x0, 0
    for _ in range(c.n):
        j = (i + c.sh) % c.n
        b = bit(x, i) ^ bit(y, i)
        if j == 0: return x if b == x0 else None
        x |= b << j; i = j

def taus(c, beta, eps):                         # every tau with N1 and N2 (a superset of L > 0)
    n, r8 = c.n, c.r8
    K1, K2, out = (beta + c.delta) & c.m, (eps - c.DY11) & c.m, []
    def rec(t, tau, S1, S2):
        if t == n:
            for j in range(n - r8, n):          # N2 positions that need tau bits 0..r8-1
                S2 = adv(S2, bit(K2, j) - bit(tau, (j + r8) % n),
                         bit(tau, (j - 1 + r8) % n), bit(eps, j - 1))
                if not S2: return
            out.append(tau); return
        for b in (0, 1):
            tau2 = tau | (b << t)
            T1 = adv(S1, b - bit(K1, t), bit(beta, t - 1) if t else 0, bit(tau, t - 1) if t else 0)
            if not T1: continue
            T2, j = S2, t - r8
            if j >= 0:
                T2 = adv(S2, bit(K2, j) - b, bit(tau, t - 1) if j else 0, bit(eps, j - 1) if j else 0)
                if not T2: continue
            rec(t + 1, tau2, T1, T2)
    rec(0, 0, {0}, {0})
    return out

def L_count(c, beta, tau, eps):                 # triples (c1, b1, a2) with differences beta, tau, eps
    Bc, R8 = rol(c, beta, c.r12), ror(c, tau, c.r8)
    mult = Counter(pa for q in subs(beta) for pa in pats(c, tau, (sgn(c, q, beta) + c.delta) & c.m))
    tot = 0
    for qc in pats(c, Bc, c.DY11):              # c1 AND Bc = qc: the cube of beta
        for pa, w in mult.items():
            for pd in subs(R8):
                for pc in pats(c, eps, (c.DY11 + sgn(c, pd, R8)) & c.m):
                    tot += w * e1_dp(c, Bc, qc, tau, rol(c, pd, c.r8) ^ pa, R8, pd, eps, pc)
    return tot << (c.n - wt(beta))              # b1 is free off beta
def e1_dp(c, Bc, qc, tau, need, R8, pd, eps, pc):
    S = {(0, 0): 1}                             # (borrow of c1 - Y11, carry of c1 + d2)
    for i in range(c.n):
        T = Counter()
        for (bo, ca), w in S.items():
            for x in ((bit(qc, i),) if bit(Bc, i) else (0, 1)):
                v = x - bit(c.Y11, i) - bo
                if bit(tau, i) and (v & 1) != bit(need, i): continue
                for z in ((bit(pd, i),) if bit(R8, i) else (0, 1)):
                    s = x + z + ca
                    if bit(eps, i) and (s & 1) != bit(pc, i): continue
                    T[(1 if v < 0 else 0, s >> 1)] += w
        S = T
    return sum(S.values())

def N3_count(c, tau, eps):                      # quadruples (Y4, h1, Y9, w8); and those with rule A
    A, E, T = c.eta, eps, tau
    psi = tau ^ ror(c, tau, c.sh); Psi = rol(c, psi, c.r12)
    B = A ^ E; B8 = ror(c, B, c.r8); AE = A | E
    D1 = {}
    for ph in subs(A):
        pg = pats(c, Psi, sgn(c, ph, A))
        if pg: D1.setdefault(sgn(c, ph, A), ([], pg))[0].append(ph)
    D2 = [(pf, pe) for pf in subs(psi) for pe in pats(c, E, (c.DY3 + sgn(c, pf, psi)) & c.m)]
    if not D1 or not D2: return 0, 0
    RB = 0
    for mk, _ in c.rule: RB |= mk
    X = (A & E) | (E & ~A & RB)                 # the bits of pe that G and the rule read
    Yc = Counter(y & Psi for y in c.Y4s)
    W = {pg: Counter() for _, pgs in D1.values() for pg in pgs}
    for pg, Wg in W.items():                    # W[pg][x]: sum of Y over (pf, pe) with pe AND X = x
        for pf, pe in D2:
            Wg[pe & X] += Yc[rol(c, pf, c.r12) ^ pg]
    tot = totA = 0
    for d1, (phs, pgs) in D1.items():
        D3 = [(pb, pt) for pt in subs(T) for pb in pats(c, B8, (sgn(c, pt, T) - d1) & c.m)]
        for ph in phs:
            for pg in pgs:
                for x, y in W[pg].items():
                    if not y: continue
                    for pb, pt in D3:
                        kb = rol(c, pb, c.r8)
                        g = g_dp(c, pg, Psi, kb | ((ph ^ x) & A & E), AE, pt, T)
                        tot += y * g
                        totA += y * g * rule_count(c, ph | ((x ^ kb) & E & ~A), AE)
    return tot << (c.n - wt(AE)), totA
@lru_cache(maxsize=None)
def g_dp(c, pg, Psi, kfix, AE, pt, T):          # (g1, k): g1 AND Psi = pg, k AND AE = kfix
    S = [1, 0]                                  # carry of g2 = g1 + ror(k, r8)
    for i in range(c.n):
        j = (i + c.r8) % c.n
        nxt = [0, 0]
        for ca in (0, 1):
            for x in ((bit(pg, i),) if bit(Psi, i) else (0, 1)):
                for z in ((bit(kfix, j),) if bit(AE, j) else (0, 1)):
                    s = x + z + ca
                    if bit(T, i) and (s & 1) != bit(pt, i): continue
                    nxt[s >> 1] += S[ca]
        S = nxt
    return S[0] + S[1]
@lru_cache(maxsize=None)
def rule_count(c, hfix, AE):                    # h1 with h1 AND AE = hfix that satisfy the rule
    F = 0
    for mk, _ in c.rule: F |= mk & ~AE
    ok = sum(all(wt((hfix | f) & mk) % 2 == v for mk, v in c.rule) for f in subs(F))
    return ok << (c.n - wt(AE) - wt(F))

def solvable(c, eqs, masks):                    # do patterns p_v of masks[v] make every
    S = {(0,) * len(eqs)}                       # sum(s*word) + sum(2*s*p_v) zero mod 2^n?
    for i in range(c.n):
        nS = set()
        for ch in product(*[(0, 1) if i and bit(mk, i - 1) else (0,) for mk in masks]):
            for st in S:
                nxt = []
                for (consts, coefs), cy in zip(eqs, st):
                    d = cy + sum(s * bit(w, i) for s, w in consts) + sum(s * ch[v] for v, s in coefs)
                    if d % 2: break
                    nxt.append(d >> 1)
                else: nS.add(tuple(nxt))
        S = nS
        if not S: return False
    return True
def e3_screen(c, tau, eps):                     # (a) with (c), and (b): necessary for N3 > 0
    A, psi = c.eta, tau ^ ror(c, tau, c.sh)
    Psi, B8 = rol(c, psi, c.r12), ror(c, c.eta ^ eps, c.r8)
    ac = [([(1, Psi), (-1, A)], [(0, 1), (1, -1)]),                  # vars 0 ph, 1 pg, 2 pt, 3 pb
          ([(1, tau), (-1, A), (-1, B8)], [(0, 1), (3, 1), (2, -1)])]   # (var, sign of 2 p_var)
    b = [([(1, eps), (-1, c.DY3), (-1, psi)], [(0, -1), (1, 1)])]     # vars 0 pe, 1 pf
    return solvable(c, ac, [A, Psi, tau, B8]) and solvable(c, b, [eps, psi])

def beta_part(c, beta, show=print):
    tot = totA = 0; rows = []
    for eps in eps_roots(c, beta):
        ts = taus(c, beta, eps)
        ts3 = [tau for tau in ts if e3_screen(c, tau, eps)]
        show(f"eps {eps:08x}: {len(ts)} tau pass N1 and N2, {len(ts3)} also the E3 screen")
        for tau in ts3:
            n3, n3a = N3_count(c, tau, eps)
            if n3 == 0: continue
            L = L_count(c, beta, tau, eps)
            show(f"  tau {tau:08x}  L {L}  N3 {n3}  N3_ruleA {n3a}")
            if L: rows.append((tau, eps, L, n3, n3a))
            tot += L * n3; totA += L * n3a
    return rows, tot, totA

def inst32():
    Y3, Y3B, Y11, Y11B = 0x8127c181, 0x7edf3e7e, 0x7af77f38, 0x850000c3   # Fact P
    W4, W4B = 0x97475638, 0x97475640
    Y4s = [((0x030c0303 | f) - Y3) & 0xffffffff for f in subs(~0x03cf8303 & 0xffffffff)]   # whole class (Lemma Q)
    rule = []                                                                            # no rule filter
    c = Inst(32, 16, 12, 8, 7, Y3, Y3B, Y11, Y11B, (W4 - W4B) & 0xffffffff, 0x830303cf, Y4s, rule)
    assert len(Y4s) == 524288 and all(ror(c, ((Y3 + y) ^ (Y3B + y)) & c.m, 16) == c.eta for y in Y4s)
    return c

def main32(beta):
    t0 = time.perf_counter()
    c = inst32()
    rows, tot, totA = beta_part(c, beta)
    print(f"beta {beta:08x}: {len(rows)} outcomes with L * N3 > 0")
    print("tau       eps       L                  N3                 L*N3/2^81  rule A")
    for tau, eps, L, n3, n3a in sorted(rows):
        q, rem = divmod(L * n3, 2**81)
        print(f"{tau:08x}  {eps:08x}  {L:<17}  {n3:<17}  {q:<9}{'' if rem == 0 else ' +rem'}  "
              f"{'all' if n3a == n3 else n3a}")
    q, rem = divmod(tot, 2**81); qA, remA = divmod(totA, 2**81)
    print(f"part = sum / 2^81 = {q} remainder {rem}; with rule A {qA} remainder {remA}")
    print(f"seconds {time.perf_counter() - t0:.1f}")
    return tot, totA

if __name__ == "__main__" and "--selftest" not in sys.argv:
    beta = int(sys.argv[sys.argv.index("--beta") + 1], 16) if "--beta" in sys.argv else 0x18b0e098
    tot, totA = main32(beta)
    if beta == 0x18b0e098:
        q83, r83 = divmod(tot, 2**83)           # 2^19 members = 4 * 2^17: per-member scale of the sub-class
        print(f"sum / 2^83 = {q83} remainder {r83}  (= sum / 2^81 divided by 2^19 / 2^17 = 4)")
        assert tot == 286793728 << 81 and tot == 71698432 << 83 and totA == tot
        print("CHECK whole class, no rule: sum / 2^81 = 286,793,728; sum / 2^83 = 71,698,432 (rival dd91b2f6)")
```

Output of that run, the outcome table restricted to the six rows of this
package (the program's other lines are unchanged):

```text
beta 18b0e098: 14 outcomes with L * N3 > 0
tau       eps       L                  N3                 L*N3/2^81  rule A
175020a0  6e21be55  562949953421312    108086391056891904  25165824   all
185020a0  6e21be55  2251799813685248   72057594037927936  67108864   all
275020a0  6e21be55  562949953421312    18014398509481984  4194304    all
285020a0  6e21be55  2251799813685248   108086391056891904  100663296  all
385020a0  6e21be55  1125899906842624   144115188075855872  67108864   all
685020a0  6e21be55  562949953421312    27021597764222976  6291456    all
part = sum / 2^81 = 286793728 remainder 0; with rule A 286793728 remainder 0
seconds 141.6
sum / 2^83 = 71698432 remainder 0  (= sum / 2^81 divided by 2^19 / 2^17 = 4)
CHECK whole class, no rule: sum / 2^81 = 286,793,728; sum / 2^83 = 71,698,432 (rival dd91b2f6)
exit 0
```

**End of Section 17.**
