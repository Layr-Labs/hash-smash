# A last-chunk half-collision and a chunk-counter search for 2-round BLAKE3

The scalar below is `time_log2` under `collision-frontier-v5`. Memory is a separately reported resource bound.

This exploratory package targets blake3-r2-prefix-v1. It has an exact part and a heuristic part, and it keeps them apart. It is
the counter search of our entry 415e792c on the whole class of eta with the outcome set S of six outcomes of beta*, 175020a0,
185020a0, 275020a0, 285020a0, 385020a0 and 685020a0, with the exact filter and the s-pattern pre-check of that entry, and with
eight changes. (1) *The member loop and the direct tables*, after entry e9b6649e of the participant hecmas: the run draws one
fresh word per *context*, the seven outer words, runs the 39 lines of the outer step that do not read the member once for that
context, and walks all 2^19 members of the class in it; the two masks of the filter are read from two tables over all 2^32 words
with one load each (9.8). (2) *The guards (G7) and (G15) and a root certificate of four one-word tests*: (G7), of our entry
0bc5f130 (GPT Sol, answer AX 1), and (G15) (GPT Sol, answers CF 7 and CD 10) each prescribe one more bit of the solver's word, and
the certificate (GPT Sol, answer CF 6) replaces the full test of E1 on a root; with the global ledger of 736 machine units of an
outer step that reaches the solver, which takes the solver's source bank from words that the walk already holds (GPT Sol, answers
CD 11 and D13), and with at most one row of each family left at depth 7 (GPT-6 Astra, Batch 17), the proved cap of the solver's
work is 15,296 machine units (9.7, Section 11). (3) *The omega-first batch* (GPT Sol, answer CA, derived and checked by the
participant, with its charges audited in GPT Sol's answer CD): a batch of seven members computes only the member lines that lead
to omega = Y3 + y + w8, folded into 17 machine units (GPT Sol, answer D9), and the 17 member lines that lead only to Y9 run only
for a batch with a lane whose test on omega passes: 50 machine units per partner batch of seven, 112,519 per context and 53 per
passing lane (9.8, Section 11). (4) *The straddle cluster gate* (GPT Sol, answers CI 1, CJ 1 to 5, D14 and D16): the 32 members
that differ only in bits 10 to 14 of e1 form a cluster; one fixed table of 2^30 words, read once per representative at a key
formed in six operations from its omega, its Y0 and its e1, skips the cluster, with no read of T2, when no member can pass test
(2), which loses nothing (Lemmas A9 and CL); Lemma OR proves that on average the gate opens on at most 0.40633153915... of the
clusters of a context, so the budget of opened clusters needs no premise (9.9). (5) *The masked partner walk* (GPT Sol, answer
D14, from a combination sweep of the participant): four carries of the representative's omega side fix bits 0 to 13 of the omega
of every partner, and a table of 128 descriptors built per context lists, in at most two chunks of seven, the partners whose omega
survives test (2) on its low 16 bits; the other partners are proved to fail (2) and are not walked, and a byte guard sends the
clusters in which the carries could vary to the earlier walk of five partner batches (Lemma XF). A representative batch of seven
costs 59 machine units and an opened cluster 144, its two chunks priced together (GPT Sol, answer D18, after Grok, job 58; 9.9,
Section 11). (6) *The cached Y9* (GPT Sol, answer CM 5A): the packed Y9 lines of a batch run once, at its first lane whose test on
omega passes, and the seven lanes of Y9 stay in a register for its later lanes: 56 machine units per such batch, the *fill*, and 7
per lane that passes, the *E lane*, with a budget on the fills (9.8). (7) *The metered credit* (GPT Sol, answer CK3): the credit
of the solver is debited, block by block, with exactly the work that a call executes, after a test that the remaining credit
covers the whole cap of the call, at most 15,296; the credit is set by the exact bound of GPT-6 Astra on the mean of the solver's
ledger in an explicit model, carried to the shorter ledger of this row by a factor 478/487 that holds in every call (GPT Sol,
answer D13; 9.7, 10.3, Section 11). (8) *One work register and the layout of this row*: the four counted events add their charges
to one register W, which a context tests once against a fixed bound WB (9.1); the frame words of the walk stay in registers, after
entry 73d5265f of the participant 0xshikhar; a passing lane takes the guard words of the pre-check and the source bank of the
solver from the words of its batch (GPT Sol, answers D9 and D13), and the pre-check needs no table; T2, T1 and the gate table sit
at fixed word addresses that the lanes index directly; and the representative loop, its partner chunks and the passing lanes are
written out (9.6 to 9.9, Section 11). The exact filter (Section 8) skips every outer step that cannot hold a success with an
outcome of S, and the joint solver (9.4) finds the successes of a passing outer step without enumerating its trials. The
heuristics are H1', H4', H5_exec and H_G_cluster, stated for the walk by contexts; part (ii) of H1' takes the context as the unit,
a stronger clause than one stated per outer step (10.3). The values that the search reads are a fixed record of nonuniform advice,
stated in full (Section 12): the success analysis uses only properties of this record that this text verifies exactly, and the
selection procedure SEL that found it is charged in full in the time, at a cap of 5,486,510,246,044,225,536 operations that holds
by construction (Section 12); no premise is declared for it. The layout of the solver, its cap, the guards (G7) and (G15), the
root certificate, the pre-check, the cluster gate, the masked partner walk, the cache and the meter are proved allowances, charged
in machine units; the declared experiment `frontline-search` executes this search in the organizer's sandbox, one context per
trial with 32 of its clusters, the work register, the cache and the metered credit of this row included, and checks it in the same
run against a straight-line recomputation (9.2). Section 15 lists the earlier entries in one line each, and Section 16 credits the
people and models whose work is used.

**Exact part.** An explicit construction maps seven 32-bit words, a member y of the class of eta, a set of 524,288 values, and one
more word c1 to a number t and to a 55-byte string A and a 63-byte string B. When t is not zero, F || A and F || B, with F a
string of t full chunks of 1,024 bytes, are messages of 1024 t + 55 and 1024 t + 63 bytes whose last chunks are A and B, and the
2-round compressions of these last chunks, with chunk counter t and flags 3, give chaining values that agree on their words 0, 2,
5 and 7, that is on 128 of their 256 bits. There is no search in this and no probability: it holds for every choice (Sections 7
and 8). In the organizer's tree mode the digest of such a message depends on F and on the chaining value of its last chunk alone
(Lemma TR), so a pair whose last-chunk chaining values agree in all eight words is a collision of two complete messages. The
number t is not chosen: it is the chunk counter that the round-0 call K0 reads, solved per trial as t = ROL(K0.d1,16) XOR K0.a1.
It takes up the freedom of the message word w0, and that is what lets the construction prescribe c1, the third value of the
round-1 call E1, next to y. The search holds c1 inside the set Q* of the 2^21 words for which the first-half b difference of E1 is
beta* = 18b0e098, the difference of the solution with which the constants were found (Section 12).

**Heuristic part.** A collision needs the other four words of the chaining value to agree as well. The algorithm walks
639,060,516,044,734,464,000 = 2^69.115 outer steps of 2^21 trials each: 1,218,911,201,562,375 = 2^50.115 contexts drawn at random,
each with all 2^19 members of the class in 16,384 clusters of 32, seven members to a batch. An exact filter, two carry automata on
two words of the outer step, skips every outer step that cannot hold a collision with an outcome of S (Lemma F); it passes
2^-9.9782 of uniform pairs of words. A table read once per cluster skips the clusters in which no member can pass the second
automaton, exactly and without loss (Lemma CL); in the other clusters a table of the context skips the partners that provably fail
it (Lemma XF), and the second automaton, read from a table at omega, is tested in every other lane; the member lines that lead
only to Y9, and the first automaton, run only in a lane whose omega passes the second, 2^-4.1998 of uniform words. In a passing
outer step three bits of E1.b1 that every success shares are a function of the words of the outer step, and they allow an outcome
of S for only two of their eight values: the pre-check skips the joint solver in the other passing outer steps, exactly and
without loss (Lemma VP). The joint solver, one depth-first traversal over the bits of one internal word with guards that exact
counts of the class prove lossless and with the guards (G7) and (G15) (Lemmas G7 and G15), returns every value of that word that
meets the conditions of an outcome of S, and a certificate of four one-word tests decides for each whether its trial completes the
collision (Lemma RC). Together they find exactly the trials of the outer step that complete the collision with an outcome of S, at
a cost of at most 15,412 machine units for a passing outer step whatever its words: 7 for its E lane, 56 for the fill of its
batch, 53 for its lane and 15,296 for steps 2 and 3 with the meter (Sections 9 and 11; Lemmas V, RC, VP, G7, G15, CV, FX, ME). The
four budgets, through one work register, and the credit of the solver are halts, charged at their bounds, so the time bound
contains no mean of a count. Four heuristics are declared for the success, each for the instance that the stated advice record of
Section 12 fixes. H1': the valid trials (t not zero) complete the collision with an outcome of S at a rate no lower than
125,920,632,087 * 2^-128 = 2^-91.126, ten elevenths, rounded down, of the model's rate for this prescription and these outcomes,
and the listed good trials of one context, within one outer step and across its members, are not clustered beyond a stated bound.
H4': for a uniform outer step, a lane whose omega passes the second automaton and a passing outer step occur with probability at
most 1.000026 and 1.000176 times their exact shares; each budget adds to that mean a reserve over the independent contexts that
Hoeffding's inequality proves sufficient. H5_exec: averaged over the outer steps, the ledger U0 of the work that steps 2 and 3
execute for the outcomes kept by the pre-check (zero if it keeps none), with the global part of 1,024 machine units of the earlier
layout, is at most 1.01 times 92,113,900,425,963 / 2^46 = 1.3090, the exact bound on its mean in model M, which makes the credit
sufficient: the meter debits the ledger U of this row, at most 478/487 of U0 in every call (Lemmas ME and CP), and the credit adds
a reserve that Bernstein's inequality proves sufficient and a preflight reserve of one whole call. H_G_cluster: a context has on
average at most 12,466 batches with an E lane, so at most that many fills; the fill budget adds a Hoeffding reserve over the
contexts. The budget of opened clusters needs no premise: Lemma OR proves that on average the gate opens on at most
0.40633153915... of the clusters of a context (9.9). Under these four the search succeeds with probability at least 0.39. The
search is charged below 2^62.7911 target-compression units. The selection procedure SEL that found the advice record is charged in
full, below 2^53.503 units, at a cap that holds by construction (Section 12). The total, 2^62.79333893..., is below 2^62.7934: the
claimed scalar is 62.7934. The search needs less than 2^42 bytes of memory, its tables and its written-out code included; its two
messages are shorter than 2^42 bytes each, and the declared 2^44 bytes cover them, the code, the search and every run of SEL, even
all held at once (Section 12).

The rate in H1' is an assumption. Under the seven-word model of Section 13, with Y4 uniform in the class, prescribing c1 in Q*
multiplies by 2^11 the part of beta* in the rate of the class: counting the six outcomes of S, the rate is 2^11 * 67,633,152 =
138,512,695,296 times 2^-128, which is 853.61 times the model rate of a trial of the class (Lemma S1, proved by another AI model,
GPT Sol 6.1). The figure 67,633,152 is the sum of six exact outcome counts of the participant's counting program, printed with its
output in Section 17. Whether the trials of the construction realise that conditional law, to at least 10/11 of its rate, is not
proved, and it is declared as H1'; Lemmas S2 to S4 prove parts of it, and Lemma S8 states how weak the dependence has to be. On
real counter trials the participant's measurements agree with the model for events down to about 2^-31.7 per trial, and in a
preregistered scaled-down end-to-end run with 40,882 real collisions of complete messages the counter arrangement realises 1.00199
+- 0.00496 of the predicted count, with a one-sided 97.7 per cent lower bound of 0.99213, above 10/11 (Section 13). No run reaches
a collision at 32 bits.

Part (ii) of H1', the dependence, is stated with the context as the unit, as entry e9b6649e states it: the 2^19 outer steps of a
context share their seven outer words, and only the contexts are independent. It is an assumption, which cannot be measured at
full size; it fails only if listed good trials cluster by context about 2^44 times more than independent members would, while the
events that every listed good trial meets cluster by a factor between 1.14 and 1.25 at every depth measured, and the two halves of
a listed good trial show no clustering across members in a preregistered run (10.3, Section 13).

No full 2-round collision is exhibited, and the search is far beyond feasible computation. The declared experiment executes the
search of 9.1 on organizer seeds, one context per trial, and returns for each trial the root-instance pair of the same
construction, single chunks of 55 and 63 bytes compressed with counter 0 and flags 11, whose half-collision the organizer's runner
checks on the digests; no digest experiment can show the half-collision of the counter instance, whose colliding chunk is not the
root (6.4). Its observations, the program's own counts, are untrusted (9.2).

## 1. Exact complete hash on the messages used

H is unkeyed BLAKE3-256 with only rounds 0 and 1 kept in every compression. Every message of the root instance (Sections 4 to 6)
has n = 55 or n = 63 bytes. A message of n <= 64 bytes is one chunk consisting of one block, with no parent node, so H evaluates
exactly one compression. The block is the message followed by 64 - n zero bytes, used only for loading words. The compression has
flags CHUNK_START | CHUNK_END | ROOT = 11, true block length n, and chunk counter and root-output counter both zero. There is no
key and no derivation flag.

Decode the zero-filled block into sixteen little-endian 32-bit words w[0..15]. The IV is

    6a09e667 bb67ae85 3c6ef372 a54ff53a
    510e527f 9b05688c 1f83d9ab 5be0cd19.

Initialize v[0..7] = IV, v[8..11] = IV[0..3] and v[12..15] = (0, 0, n, 11). The block length n is the initial value of v[14] and
enters nowhere else. All additions and subtractions on state and message words are modulo 2^32. ROR and ROL rotate a 32-bit word.
G(a,b,c,d,x,y) is

    v[a] = v[a]+v[b]+x;  v[d] = ROR(v[d] XOR v[a],16)
    v[c] = v[c]+v[d];    v[b] = ROR(v[b] XOR v[c],12)
    v[a] = v[a]+v[b]+y;  v[d] = ROR(v[d] XOR v[a],8)
    v[c] = v[c]+v[d];    v[b] = ROR(v[b] XOR v[c],7).

A round is four column calls followed by four diagonal calls on the current schedule s, and between rounds s is replaced by
s[P[i]] with P = (2,6,3,10,7,0,4,13,1,11,12,5,9,14,15,8). Written out for the two retained rounds, with names used throughout:

    round 0   K0 = G(0,4,8,12, w0, w1)     K1 = G(1,5,9,13, w2, w3)
              K2 = G(2,6,10,14, w4, w5)    K3 = G(3,7,11,15, w6, w7)
              D0 = G(0,5,10,15, w8, w9)    D1 = G(1,6,11,12, w10, w11)
              D2 = G(2,7,8,13, w12, w13)   D3 = G(3,4,9,14, w14, w15)
    round 1   C0 = G(0,4,8,12, w2, w6)     C1 = G(1,5,9,13, w3, w10)
              C2 = G(2,6,10,14, w7, w0)    C3 = G(3,7,11,15, w4, w13)
              E0 = G(0,5,10,15, w1, w11)   E1 = G(1,6,11,12, w12, w5)
              E2 = G(2,7,8,13, w9, w14)    E3 = G(3,4,9,14, w15, w8)

S denotes the state after K0..K3, X the state after round 0, Y the state after C0..C3 and Z the final state. The compression
output is o[i] = Z[i] XOR Z[i+8] and o[i+8] = Z[i+8] XOR IV[i] for i = 0..7. The digest H(m) is the first 32 output bytes,
LE4(o[0]) || ... || LE4(o[7]).

This is the complete hash of the target profile restricted to inputs of 55 and 63 bytes: standard IV, standard flags, true block
length, both retained rounds with the standard permutation, standard feed-forward and the full 256-bit digest. It is not a
free-start, chosen-IV, compression-only or truncated-output setting.

*The same compression in a last chunk.* Sections 7 to 9 use the same compression, with the same names, as the compression of the
last chunk of a longer message: there v[12..15] = (t mod 2^32, t >> 32, n, 3), with the chunk counter t and the flags
CHUNK_START | CHUNK_END = 3, and the output words o[0], .., o[7] are the chaining value of the chunk (Lemma TR). Nothing else
changes: the IV, the block, the two rounds and the output.

## 2. Inverting one G call

Consider one call G(a,b,c,d,x,y) with input values A, B, C, D and name its eight assignments

    a1 = A + B + x           d1 = ROR(D XOR a1, 16)
    c1 = C + d1              b1 = ROR(B XOR c1, 12)
    a2 = a1 + b1 + y         d2 = ROR(d1 XOR a2, 8)
    c2 = c1 + d2             b2 = ROR(b1 XOR c2, 7).

Its outputs are (a2, b2, c2, d2). The values a1, d1, c1, b1 are called the first, second, third and fourth value of the call, a2
the fifth, and so on.

**Fact 1.** Reading the assignments backwards,

    b1 = ROL(b2, 7) XOR c2       c1 = c2 - d2       d1 = ROL(d2, 8) XOR a2
    B  = ROL(b1, 12) XOR c1      C  = c1 - d1
    a1 = ROL(d1, 16) XOR D       y  = a2 - a1 - b1      x = a1 - A - B.

Each line is one assignment solved for another of its terms. A set of words A, B, C, D, x, y, a1, d1, c1, b1, a2, d2, c2, b2 is
the execution of one call exactly when the eight assignments hold, in whatever order and for whichever of their terms they were
solved. The constructions below use nothing else: every line of theirs is one assignment of one call, solved for the name on its
left.

## 3. Three ingredients

**3.1 The length is cancelled inside K2.** K2 is the only call of round 0 that reads the block length n, the initial value of
v[14], and it overwrites that word; it is also the only call of round 0 that reads w4 and w5. Its inputs are (IV[2], IV[6], IV[2],
n). Put K = IV[2] + IV[6] = 5bf2cd1d. For lengths 55 and 63, whose XOR is 8, define for any w4, w5

    w4' = ((K + w4) XOR 8) - K        w5' = w5 + w4 - w4'.

**Lemma L.** K2 with block length 55 and words (w4, w5) leaves the same four state words as K2 with block length 63 and words
(w4', w5').

Proof. Let a1 = K + w4. In the second execution the first assignment gives K + w4' = a1 XOR 8, so the second gives ROR(63 XOR a1
XOR 8, 16) = ROR(55 XOR a1, 16) because 63 XOR 8 = 55: the same d1. The third and fourth depend only on d1 and constants. The
fifth gives (a1 XOR 8) + b1 + w5' = a1 + b1 + w5 because w5' - w5 = w4 - w4' = a1 - (a1 XOR 8). The last three depend only on
values already shown equal. QED.

Hence two messages of 55 and 63 bytes that share every word except w4, w5, related as above, have the same state S after the
column step and the same state X after round 0, since no other call of round 0 reads v[14], w4 or w5 before K2 has made the states
equal.

*Which words must be zero.* For both messages to be honest byte strings of their lengths with the same words w6..w15, the bytes 55
to 63 of the block must be zero in both. In the 55-byte message they are zero fill. In the 63-byte message bytes 55 to 62 are its
last eight bytes, which are chosen to be zero, and byte 63 is zero fill. Byte 55 is the top byte of w13, bytes 56 to 59 are w14
and bytes 60 to 63 are w15. So the family needs

    w14 = 0,   w15 = 0,   top byte of w13 = 0,

and nothing else: bytes 0 to 54 are free in both messages.

**3.2 A pinned call C3.** Fix the six constants

    X3 = 29d4fa98   X7 = bee3af28   X11 = 44036000   X15 = 40c58500
    W4 = 97475638   W13 = 0007c006

The top byte of W13 is zero. K + W4 = f33a2355 and W4' = ((K + W4) XOR 8) - K = 97475640, so W4 - W4' = fffffff8, that is -8
modulo 2^32. Evaluate C3 = G(3,7,11,15, w4, W13) on the inputs (X3, X7, X11, X15) with w4 = W4 and with w4 = W4':

    w4 = W4    a1=7ffffff8 d1=7af83f3a c1=befb9f3a b1=01200183
               a2=8127c181 d2=bbfbdffe c2=7af77f38 b2=76f7aefd
    w4 = W4'   a1=80000000 d1=8500c0c5 c1=c90420c5 b1=fed77e78
               a2=7edf3e7e d2=bbfbdffe c2=850000c3 b2=76f7aefd

**Fact P.** The two executions give the same d output bbfbdffe and the same b output 76f7aefd. They differ in the a output
(8127c181, 7edf3e7e) and in the c output (7af77f38, 850000c3). This is a finite computation on the displayed constants.

**3.3 Half of the digest does not see the difference.**

**Lemma H.** Take two executions of the 2-round compression that have the same state X after round 0 and the same message words
except w4 and w5. Suppose (X[3], X[7], X[11], X[15]) = (X3, X7, X11, X15), w13 = W13, and w4 is W4 in the first execution and W4'
in the second. Then the two digests agree on digest words 0, 2, 5 and 7.

Proof. C0, C1, C2 read neither w4 nor w5 and act on identical states, so they leave identical values in both executions. C3 reads
state words 3, 7, 11, 15 and the words w4, w13; by Fact P it leaves the same v[7] and v[15] in both executions and may differ only
in v[3] and v[11]. So Y agrees except possibly in Y[3] and Y[11]. E0 reads Y[0], Y[5], Y[10], Y[15] and w1, w11. E2 reads Y[2],
Y[7], Y[8], Y[13] and w9, w14. None of these is Y[3], Y[11], w4 or w5, so E0 and E2 produce identical outputs Z[0], Z[5], Z[10],
Z[15] and Z[2], Z[7], Z[8], Z[13]. Finally o[0] = Z[0] XOR Z[8], o[2] = Z[2] XOR Z[10], o[5] = Z[5] XOR Z[13] and o[7] = Z[7] XOR
Z[15] use only those eight words. QED.

The remaining digest words o[1] = Z[1] XOR Z[9], o[3] = Z[3] XOR Z[11], o[4] = Z[4] XOR Z[12] and o[6] = Z[6] XOR Z[14] are
computed from the outputs of E1 and E3 only. The **residual** of a pair is the 128-bit string R = (o[1] XOR o'[1], o[3] XOR o'[3],
o[4] XOR o'[4], o[6] XOR o'[6]). The pair is a collision exactly when R = 0.

## 4. Construction: the message from eight words, in three levels

This section, Section 5 and Section 6 build the root instance of the construction, whose messages are single chunks compressed
with counter 0 and flags 11 (Section 1). The counter instance, which the claim uses, is built in Section 8 from the same constants
(6.4).

The construction places the six constants of 3.2 where Lemma H needs them and gives Y4, the b output of C0, a prescribed value y.
Its input is eight free words. Six form an *outer step*: C0.c1 and C0.d1 (the third and the second value of the round-1 call C0),
D3.d1 (the second value of the round-0 call D3), S15 and S9 (words of the state S) and the message word w5. The seventh is X2, a
word of the state X; with it the six are a *context*. The eighth is y. X3, X7, X11, X15 are the constants, w4 = W4, w13 = W13 and
w14 = w15 = 0.

*Names.* TAG.a1, TAG.d1, TAG.c1, TAG.b1 are the first to fourth value of the call TAG (Section 2); its outputs carry the names of
the state S, X or Y they are written to. Arithmetic is modulo 2^32.

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

**Step S2.** w4' = W4' and w5' = w5 + W4 - W4', all modulo 2^32. For the constants of 3.2 that is w5' = w5 + fffffff8, the same as
w5 - 8.

**Step S3.** A is the first 55 bytes of the little-endian encoding of w0..w15; B is the first 63 bytes of that of the same words
with w4', w5' for w4, w5.

*Round 1, forwards (24 lines).* The tests of 6.3 read these values of round 1 of message A. Y3 and Y11 are the constants of Fact P
for w4 = W4, and Y4 = y.

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

These 24 lines define nothing of the message. E3.h1, E3.g1, E3.f1, E3.e2 are the h1, g1, f1, e2 of 6.2.

**The order and the levels.** The 29 + 21 + 10 + 12 + 24 = 96 lines above are taken in the printed order. Lines of step O are
*outer*, of step M *middle*, of step Y *table* lines; the 12 lines of step T and the 24 of round 1 are the 36 *trial* lines. Table
C gives each call's eight assignments by their left sides.

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

The inputs, message words and outputs of the eleven calls are those of Section 1 for n = 55: Ki (i = 0..3) maps (IV[i], IV[i+4],
IV[i], d) with d = 0, 0, 55, 11 to (S[i], S[i+4], S[i+8], S[i+12]); D0..D3 map (S0, S5, S10, S15), (S1, S6, S11, S12), (S2, S7,
S8, S13), (S3, S4, S9, S14), and C0..C2 map (X0, X4, X8, X12), (X1, X5, X9, X13), (X2, X6, X10, X14), to the X and the Y words of
the same indices.

**Lemma T2.** (a) *Triangular.* In the printed order every line assigns a name that no earlier line assigns and that is neither
one of the eight words nor a constant, and it reads only constants, the eight words (the eighth under the name Y4 in the lines of
round 1) and names of earlier lines. A line of step O reads no word other than the six of the outer step, a line of step M reads
neither y nor a name of step Y, and a line of step Y reads neither X2 nor a name of step M. Every line is one assignment of one
call, solved for the name on its left; the two exceptions are the lines for E1.b1 and for E3.h1, each of which is two assignments
with the first substituted into the second (c1 = Y11 + E1.d1 and e1 = Y3 + Y4 + w15), and the line for E3.e2 uses the same e1. By
Table C the 96 lines are, each exactly once: the eight assignments of each of the eleven calls K0..K3, D0..D3, C0..C2, with the
inputs and the message words of Section 1 for block length 55, with w4 = W4, w13 = W13, w14 = w15 = 0, and with the constants X3,
X7, X11, X15 as the a output of D3, the b output of D2, the c output of D1 and the d output of D0; and the first five assignments
of E1 and of E3 for message A.

(b) *The calls.* For every choice of the eight words, the names of steps O, M, Y and T are the executions of the eleven calls as
listed after Table C, each with its two message words; C0 has first, second, third and fourth value C0.a1, C0.d1, C0.c1, C0.b1 and
outputs (Y0, y, Y8, Y12); and E1.a1, E1.d1, E1.b1, E1.a2 and E3.h1, E3.g1, E3.f1, E3.e2 are the first, second, fourth and fifth
value of E1 and the second, third, fourth and fifth value of E3 in the compression of message A.

(c) *The levels.* An outer line is a function of the six words alone. A middle line is a function of the six words and X2 and does
not depend on y. A table line is a function of the six words and y and does not depend on X2. In particular the sixteen message
words of two trials of one context differ at most in w8, w9, w10, w11.

(d) *Admissible blocks.* Call a block (w0, .., w15) *admissible* if w4 = W4, w13 = W13, w14 = w15 = 0 and round 0 on it with block
length 55 ends with (X[3], X[7], X[11], X[15]) equal to the four constants. The map of this section from the eight words to the
block of A is a bijection onto the admissible blocks.

Proof. (a) is read off the displays, each formula compared with Section 2 and its call's inputs, outputs and message words; Table
C has one name in each of its 88 cells, all different, and with the eight of E1 and E3 they are the 96.

(b) An assignment solved for one of its terms is an equivalent equation modulo 2^32 (Fact 1), so a line's assignment holds once it
has run, and by (a) no later line changes its names. By (a) and Table C all eight assignments of each call hold, a constant output
in its place (lines D3.b1, X14; D2.b1; D1.c1, X6; D0.d1, X10) and y as the b output of C0 (line Y8); by Fact 1 the names are the
execution of the call. The E1 and E3 lines are those of 6.2 for message A with Y11, Y3 of Fact P, run forwards from A's Y1, Y6,
Y12, Y4, Y9, Y14.

(c) By induction over the printed order, with (a): an outer line reads only constants, the six words and outer lines; a middle
line in addition only X2 and middle lines; a table line in addition only y and table lines. w6, w7 are outer and w0..w3, w12
middle lines, w5 is one of the six words, w4, w13, w14, w15 are constants; only w8..w11 are trial lines.

(d) By (b), round 0 with block length 55 on an output block leaves the state X of the names, with the constants as X[3], X[7],
X[11], X[15], and the pinned words are constants: the block is admissible. *Injective:* by (b) each of the eight words is a value
in the compression of A, so a function of the block. *Onto:* the forward values of an admissible block (block length 55) satisfy
every equation of (a): they execute the calls, the constant outputs hold by admissibility, and C3 has the inputs X3, X7, X11, X15,
W4, W13, so Y3, Y11 are those of Fact P. Run on the eight words taken from them, each line returns the forward value of its name,
by induction, since an assignment has exactly one solution for any one term given the others. So the lines return the block. QED.

## 5. The half-collision

**Theorem.** For every choice of the seven words of a context (C0.c1, C0.d1, D3.d1, S15, S9, w5, X2) and of the word y, steps O,
M, Y, T, S2 and S3 output two distinct messages A and B, of 55 and 63 bytes, whose complete 2-round digests agree on digest words
0, 2, 5 and 7; and in both compressions the b output of C0 is Y4 = y.

Proof. The sixteen words of steps O, M, Y and T have w14 = w15 = 0 and w13 = W13, whose top byte is zero. So bytes 55 to 63 of
their encoding are zero: A, the first 55 bytes, is an honest 55-byte message whose zero-filled block is the sixteen words, and B
is an honest 63-byte message that ends in eight zero bytes and whose zero-filled block is the sixteen words with w4, w5 replaced
(3.1). Run round 0 on the words of A with block length 55. By Lemma T2 (b) the column calls leave the state S of the names and the
diagonal calls, which act on disjoint state words, leave the state X of the names. So the state after round 0 has (X[3], X[7],
X[11], X[15]) equal to the four constants, and w4 = W4, w13 = W13. By Lemma L the compression of B has the same state X after
round 0. The two compressions share every word except w4, w5, so Lemma H gives the four digest words. C0 reads X0, X4, X8, X12 and
w2, w6, which are the same in both compressions, and has b output y by Lemma T2 (b). The messages are distinct because their
lengths differ. QED.

Distinct choices of the eight words give distinct messages A: C0.c1 and C0.d1 are values inside C0, D3.d1 is a value inside D3,
S15 and S9 are state words after the column step of round 0, w5 is a message word, X2 is a state word after round 0 and y is a
state word after the column step of round 1, and all of them are functions of the message (Lemma T2 (d)). The construction yields
2^256 different half-colliding pairs.

## 6. The root instance: trials, tests and the packed machine

**6.1 Trials.** A *context* is the six words of an outer step (C0.c1, C0.d1, D3.d1, S15, S9, w5), a word X2, and everything that
steps O and M compute from them. The class and the sub-class defined next are sets of values of Y4. A **trial** is a context and a
member y of the sub-class; its messages A and B are the output of steps O, M, Y, T, S2 and S3 for the context's seven words and y.
Only steps Y and T depend on y: the trials of one context differ in the four message words w8..w11 and in nothing else of the
message (Lemma T2 (c)). Step Y does not read X2: its ten names depend on the outer step and the member only.

*The class.* The first message word of E3 is w15 = 0, so the first assignment of E3 is e1 = Y3 + Y4 for message A and e1' = Y3' +
Y4 for message B, with Y3 = 8127c181 and Y3' = 7edf3e7e from Fact P. Put DY3 = Y3' - Y3 = fdb77cfd. The second assignment is h1 =
ROR(Y14 XOR e1, 16), so the XOR difference between A and B of E3's first-half d value is

    eta = h1 XOR h1' = ROR((Y3 + Y4) XOR (Y3 + Y4 + DY3), 16),

a function of Y4 alone. Fix eta = 830303cf. The *class* is the set of all words Y4 that give this eta.

**Lemma Q.** The class is the set of all Y4 with

    ((Y3 + Y4) AND 03cf8303) = 030c0303.

It has 524,288 members: the 19 bits of e1 = Y3 + Y4 at the positions where 03cf8303 has a zero are free, bit 31 among them, and Y4
= e1 - Y3.

Proof. Put x = ROL(eta,16) = 03cf8303, which has no bit 31. Y4 is in the class exactly when e1 XOR (e1 + DY3) = x, that is when
(e1 XOR x) - e1 = DY3 modulo 2^32. For words e and x, (e XOR x) - e is, modulo 2^32, the sum over the bits i of x of 2^i where bit
i of e is 0 and of -2^i where it is 1, which is 2 ((NOT e) AND x) - x. So the condition is 2 ((NOT e1) AND x) = DY3 + x = 01870000
modulo 2^32. As (NOT e1) AND x has no bit 31, the doubling is exact and the condition is ((NOT e1) AND x) = 01870000 >> 1 =
00c38000. All bits of 00c38000 lie in x, so this fixes the 13 bits of e1 on x to (e1 AND x) = (NOT 00c38000) AND x = 030c0303 and
leaves the other 19 bits free. QED.

*The sub-class.* The search uses only the members of the class whose e1 = Y3 + Y4 has bit 21 and bit 26 equal to zero. With Lemma
Q that is the set of all Y4 with

    ((Y3 + Y4) AND 07ef8303) = 030c0303.

**Lemma Q2.** The sub-class is a subset of the class and has 131,072 members: the 17 bits of e1 at the positions 2 to 7, 10 to 14,
20 and 27 to 31, where 07ef8303 has a zero, are free, and Y4 = e1 - Y3.

Proof. 07ef8303 = 03cf8303 OR 04200000, and 04200000 has the bits 21 and 26, which are two of the 19 positions that Lemma Q leaves
free. The value 030c0303 has zeros at both. So the condition is the condition of Lemma Q together with bit 21 = bit 26 = 0, and 17
positions stay free. QED.

Member number k of the sub-class, for 0 <= k < 131072, is the Y4 whose e1 has the bits of k at its 17 free positions, in
increasing order of position. From here on "member" means a member of the sub-class. A part of the class is searched and not all
of it because, under the model of Section 13, the rate of collisions differs from member to member and is higher on this part.
Nothing exact depends on that.

**Lemma T.** For every context and every member y of the class, and so for every member of the sub-class, the messages A and B of
the trial are distinct messages of 55 and 63 bytes whose complete 2-round digests agree on digest words 0, 2, 5 and 7; in both
compressions Y4 = y; and the XOR difference between A and B of E3's first-half d value is eta = 830303cf.

Proof. The first two statements are the theorem of Section 5. In both compressions w15 = 0 and Y14 is the same, the a input of E3
is Y3 for A and Y3' for B by Fact P, and Y4 = y is a member of the class, so the difference is eta by the definition of the class.
QED.

**6.2 The residual of a trial.** With Y3, Y3', Y11, Y11' the a and c outputs of C3 from Fact P (8127c181, 7edf3e7e, 7af77f38,
850000c3), delta = W4 - W4' = fffffff8 and the trial's words and state:

    (.., Y4, .., Y12) = C0 = G(X0, X4, X8, X12, w2, w6)
    (Y1, .., Y9, ..)  = C1 = G(X1, X5, X9, X13, w3, w10)
    (.., Y6, .., Y14) = C2 = G(X2, X6, X10, X14, w7, w0)
    E1 on A:  G(Y1, Y6, Y11,  Y12, w12, w5)
    E1 on B:  G(Y1, Y6, Y11', Y12, w12, w5 + delta)
    E3 on A:  G(Y3,  Y4, Y9, Y14, w15, w8)
    E3 on B:  G(Y3', Y4, Y9, Y14, w15, w8)

and R is formed from the eight output words of E1 and E3 as in 3.3. Y4 = y and Y12 are known from step Y without evaluating C0
forwards. Write a1, d1, c1, b1, a2, .. for the assignments of E1 and e1, h1, g1, f1, e2, h2, g2, f2 for those of E3 in the order
a, d, c, b; a prime marks message B.

**6.3 Two tests of a trial.** Two tests of a trial of the root instance are used by the measurements of Section 13: rule A, a
condition on one word of E3, and the E1 test, a 32-bit condition on E1 alone (Lemma N).

**Lemma N.** For a trial of 6.1 put beta = b1 XOR b1' and eps = c2 XOR c2', both taken from E1, and

    n = eps XOR ROL(beta XOR eps, 1) XOR eta.

Let D3 and D6 be the XOR differences between A and B of digest words 3 and 6, which are the second and the fourth word of R. Then
n = D3 XOR ROL(D6, 8) for every trial. In particular R = 0 implies n = 0.

Proof. Digest word 3 is Z[3] XOR Z[11], the a output of E3 and the c output of E1, so D3 = (e2 XOR e2') XOR eps. Digest word 6 is
Z[6] XOR Z[14], the b output of E1 and the d output of E3, so D6 = (b2 XOR b2') XOR (h2 XOR h2'). In E1, b2 = ROR(b1 XOR c2, 7),
so b2 XOR b2' = ROR(beta XOR eps, 7). In E3, h2 = ROR(h1 XOR e2, 8), and h1 XOR h1' = eta for every Y4 in the class (Lemma T), so
h2 XOR h2' = ROR(eta XOR e2 XOR e2', 8). Rotating D6 left by 8 gives ROL(D6, 8) = ROL(beta XOR eps, 1) XOR eta XOR (e2 XOR e2').
The XOR with D3 cancels e2 XOR e2' and leaves n. QED.

A trial *passes the E1 test* when n = 0. The word n needs the first seven assignments of E1 for both messages and nothing of E3,
whose eta is the constant of the class.

*Rule A.* Let h1 be the second value of E3 on message A, as in 6.2, and write h[i] for bit i of h1, bit 0 being the lowest. A
trial *satisfies rule A* when all of the following hold:

    h[0] = 0;    h[1] = 1;    h[16] = 0;    h[17] = 0;
    h[2] XOR h[10] = 1;    h[3] XOR h[11] = 1;
    h[3] XOR h[12] XOR h[24] = 0;    h[6] XOR h[13] XOR h[25] = 0.

Each of the eight conditions contains a bit that no other contains (bits 0, 1, 16, 17, 10, 11, 12 and 13), so they are independent
and a uniform word satisfies rule A with probability 2^-8.

Rule A can lose solutions: there are solutions of R = 0 with Y4 in the sub-class that violate it. The counter search of this
package does not use rule A.

**6.4 The root instance and the declared experiment.** Sections 4 to 6 build the *root instance* of the construction: its messages
are single chunks of 55 and 63 bytes, and the colliding compression is the root compression, with counter 0 and flags 11 (Section
1). The claim of this package is made for the *counter instance* of Sections 7 to 9, whose messages have 1024 t + 55 and 1024 t +
63 bytes and whose colliding compression is that of the last chunk, with counter t and flags 3. The two instances share the six
constants, Fact P, Lemmas L and H, the class, Lemma N and the machine of 6.5; the sub-class and rule A belong to the root
instance, not to the counter search of this package. The instances differ in the counter and the flags that the compression reads,
and in the order in which the construction solves the assignments of rounds 0 and 1 (Sections 4 and 8).

An experiment of the organizer's harness returns pairs of complete messages and tests an event on their two digests, while the
half-collision of the counter instance is an agreement of four words of the chaining value of a chunk that is not the root. The
parent and root compressions above that chunk mix all eight words, so the digests of a counter pair are not expected to agree on
the masked words, and on two counter pairs with t = 1 they do not (Section 7). No digest experiment can show a half-collision of a
non-root chunk's chaining value. The declared experiment `frontline-search` (9.2) therefore executes the counter search of 9.1 on
each trial and returns a pair of the root instance of the same lines: for the trial's context and its first passing member (member
0 if none), steps CO and CT of Section 8 with the flags 11 of the root in the line for K3.d1 and the c1 for which t = 0 (Lemma IP)
give single chunks of 55 and 63 bytes, compressed as the root with counter 0 and flags 11. Theorem C, read with 11 in place of 3
in that line, as Lemma S2 reads steps O and M, predicts that every pair agrees on digest words 0, 2, 5 and 7, which the organizer
recomputes.

**6.5 Seven trials in one word.** A packed word holds seven lanes of 36 bits at bit offsets 0, 36, .., 216. A lane represents its
value modulo 2^32; bits 32..35 are carry guards. A constant is placed in all seven lanes before the batches that use it. Additions
are single 256-bit additions. A rotation of every lane by r is the five operations

    PROR(z, r) = ((z >> r) AND A_r) OR ((z << (32-r)) AND B_r)

with A_r selecting the low 32-r bits of every lane and B_r the next r bits; the masks discard guard bits and bits shifted in from
the neighbouring lane, so the result is reduced below 2^32. With M = 2^32 - 1 in every lane, the complement of the low 32 bits of
a lane is an XOR with M, a difference x - y of a constant x and a lane y is (y XOR M) + (x + 1), and subtracting a constant y is
one addition of the constant -y.

*The machine.* A load/store machine with 16 registers. One operation is charged for every addition, XOR, AND, OR and shift of
256-bit words, for every comparison and for every branch, so PROR = 5. One load is charged every time a word is fetched from
memory, from a list or from a table into a register, and one store every time a register is written to memory or to a table. Shift
distances are fixed in the instruction, and a register may hold a memory word across several operations. While no lane reaches
2^36 no carry leaves a lane and the low 32 bits of every lane equal the scalar value modulo 2^32; Lemma MB bounds the values of
the batches of 9.8 below 2^36.

## 7. The tree lemma: the last chunk decides the digest

The claim is made for messages of more than one chunk. This section shows, from the organizer's reference code, that for such a
message the digest is a function of the prefix and of the chaining value of the last chunk alone.

The organizer's hash, `verifier/blake3.py`, computes `blake3(data, rounds)`, with rounds = 2 for this target, by these lines of
its code:

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

There `_chunk_output(chunk, counter, rounds)` compresses every block of a chunk but the last, starting from the chaining value IV,
and returns the last block as a descriptor (cv, words, counter, len(block), flags | CHUNK_END), where flags is CHUNK_START = 1
when that block is the first of its chunk; its last block starts at `last_offset = max(0, (len(chunk) - 1) // 64 * 64)`.
`_compress(cv, words, counter, block_len, flags, rounds)` is the compression of Section 1 with v[0..7] = cv and v[12..15] =
(counter mod 2^32, counter >> 32, block_len, flags); it returns sixteen output words, of which the first eight are the chaining
value. `_parent_output(left, right)` is the descriptor (IV, left + right, 0, 64, PARENT) of a parent node.

**Lemma TR (the last chunk decides).** Let t >= 1 and let F be any string of 1024 t bytes. For a string A of 1 to 64 bytes write
words(A) for the sixteen little-endian words of A followed by zero bytes up to 64 bytes, and CV_t(A) for `_compress(IV, words(A),
t, len(A), 3, 2)[:8]`.

(a) The last chunk of F || A is A, and the organizer's code compresses it once, as `_compress(IV, words(A), t, len(A), 3, 2)`: the
compression of Section 1 with block A, block length len(A), counter t and flags CHUNK_START | CHUNK_END = 3. It is not the root
compression.

(b) blake3(F || A, 2) is a function of F and of CV_t(A) alone.

(c) For strings A and B of 1 to 64 bytes with CV_t(A) = CV_t(B), blake3(F || A, 2) = blake3(F || B, 2).

Proof. (a) F || A has 1024 t + len(A) bytes with 1 <= len(A) <= 64, so chunk_count = t + 1 and the last chunk is data[t * 1024:] =
A. In `_chunk_output(A, t, 2)`, last_offset = 0, so that function stops at its first block, offset 0, and returns (IV, words(A),
t, len(A), CHUNK_START | CHUNK_END). The final loop of blake3 compresses this descriptor once, in its first pass, which runs
because the stack is not empty (b).

(b) The loop over counter = 0, .., t - 1 reads data[counter*1024:(counter+1)*1024], which lies inside F, and no other byte of the
message; so the stack that it leaves depends on F alone. Each pass appends one value and pops values only while total is even, so
after t >= 1 passes the stack holds as many values as t has one bits, at least one. The final loop therefore runs at least once.
Its first pass forms `_parent_output` of the top of the stack and CV_t(A), and every later pass forms a parent descriptor from the
next value of the stack and the chaining value of the descriptor before it. The root compression reads the last descriptor. So the
digest is computed from the stack, which depends on F alone, and from CV_t(A).

(c) follows from (b). QED.

The code accepts messages shorter than 2^61 bytes; the messages of this package are shorter than 2^42 bytes (Section 8). The tree,
its counters and flags and its root output are those of the target profile. The two messages of a pair are complete messages of
the domain, and a pair with equal digests is an ordinary collision, not a free-start or compression-only one. The converse of (c)
is not used.

*The digest does not show a partial agreement.* When CV_t(A) and CV_t(B) agree on four words only, the parent and root
compressions over them mix all eight, and the two digests are not expected to agree on a fixed set of words. On two counter pairs
of Section 8 with t = 1, messages of 1,079 and 1,087 bytes, the chaining values agree on words 0, 2, 5 and 7, and the two digests
do not agree on digest words 0, 2, 5 and 7 (participant computation with the organizer's code). This is why the declared
experiment returns pairs of the root instance (6.4).

*Participant checks with the organizer's code.* In each of the following the organizer's `verifier/blake3.py` was imported
unchanged; they are participant computations, which the organizer has not run. (1) For 2,000 trials of the counter construction of
Section 8 in 40 outer steps, 8 of them with outer words 0 or ffffffff, `_chunk_output` of the last chunk returned (IV, the block
words, t, 55 or 63, 3) for A and for B, and `_compress` returned the chaining value that entry 26ebba63's program computes, in
2,000 of 2,000; words 0, 2, 5 and 7 of the two chaining values were equal in all 2,000 and all eight words in none; and 204,000
internal words of the construction were equal to a separately written forward computation of the compression. (2) For five counter
trials with t = 1, 3, 3, 4 and 16,383, the complete messages F || A and F || B, with F a string of t chunks of pseudorandom bytes,
were hashed by `blake3(m, 2)`. In each, the messages have 1024 t + 55 and 1024 t + 63 bytes; the code makes exactly one
compression with block length 55 or 63, and its inputs are (IV, the block words, t, 55 or 63, 3); its chaining values agree on
words 0, 2, 5 and 7 and not on all eight; the two digests differ; and when the output of that compression of F || B is replaced by
the output of the one of F || A, blake3 returns the digest of F || A, and the other way round.

## 8. The counter construction

*Words and constants.* The construction has nine free words: the seven *outer words* C0.d1, D2.a1, D2.b1, S11, S4, X9 and w6; a
member y of the class of 6.1 (Lemma Q), which becomes the value of Y4; and the *inner word* c1, which becomes the third value of
E1 on message A. The constants are those of Section 4: X3, X7, X11 and X15, w4 = W4, w13 = W13, w14 = w15 = 0, the four constant
first values K2.a1, K2.d1, K2.c1 and K2.b1 of K2 given in step O, and Y3, Y11 of Fact P. The compression reads three more values
besides the message and the IV. K3 reads the flags, here 3 (the line for K3.d1); K1 reads v[13], here 0 (the line for K1.a1); and
K0 reads the counter v[12], which is not fixed in advance: the line for t solves K0's second assignment for it. The names are
those of Section 4.

*The cube Q*.* Q* is the set of the 2^21 words c with (c AND 0e09818b) = 02008000. Member number j of Q*, for 0 <= j < 2^21, is
the word whose bits at the 21 positions where 0e09818b has a zero are the bits of j, in increasing order of position.

*Members.* In Sections 8 to 12 a *member* is a member of the class of Lemma Q, not of the sub-class of 6.1. Member number k of the
class, for 0 <= k < 2^19, is the Y4 whose e1 = Y3 + Y4 has the bits of k at the 19 positions where 03cf8303 has a zero, in
increasing order of position, and Y4 = e1 - Y3. The search of this package uses every member; it has no sub-class and no rule A.

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

**Step CS (the messages).** If t = 0 the trial is invalid and is dropped: a message with no full chunk before its last chunk has
that chunk as its root, compressed with counter 0 and flags 11 and not with the flags 3 that the line for K3.d1 used. Otherwise
the words w0 to w12 of the lines, with w4 = W4 and w13 = W13, and w14 = w15 = 0 form the block of A; A is the first 55 bytes of
its little-endian encoding, and B the first 63 bytes of that of the same words with w4' = W4' and w5' = w5 + fffffff8 in place of
w4 and w5, as in steps S2 and S3 of Section 4. F is the string of 1024 t zero bytes, and the two messages are F || A, of 1024 t +
55 bytes, and F || B, of 1024 t + 63 bytes.

*The order and the calls.* Table CT gives each call's eight assignments by the name that the line for that assignment assigns; the
cells K2.a1, K2.d1, K2.c1 and K2.b1 are the four constant values. E1's first five assignments are the lines for Y6, E1.a1, E1.d1,
E1.b1 and E1.a2, in the order of the assignments; E3's first two assignments are the line for E3.h1, and its third to fifth the
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

The order was found by a solver search of the participant's helper agents for an order in which Y4 and E1.d1 are both free words.

**Lemma CT (the counter order).** (a) *Triangular.* In the printed order, step CO and then step CT, every line assigns a name that
no earlier line assigns and that is neither one of the nine free words nor a constant, and it reads only constants, the nine words
and names of earlier lines; a line of step CO reads neither c1 nor a name of step CT. Every line is one assignment of one call
solved for the name on its left; the exceptions are the line for E3.h1, which is the first two assignments of E3 with the first
substituted into the second (e1 = Y3 + Y4 + w15, w15 = 0), and the line for E3.e2, which uses the same e1. By Table CT the 93
lines and the four constant values of K2 are, each exactly once, the eight assignments of each of the eleven calls K0..K3, D0..D3,
C0..C2, with the inputs and the message words of Section 1 for block length 55, counter v[12] = t, v[13] = 0 and flags v[15] = 3,
with w4 = W4, w13 = W13, w14 = w15 = 0, and with the constants X3, X7, X11, X15 as the a output of D3, the b output of D2, the c
output of D1 and the d output of D0; and the first five assignments of E1 and of E3 for message A, E1 with c input Y11 and E3 with
a input Y3.

(b) *The calls.* For every choice of the nine words, the names of the lines are the executions of these calls. In particular round
0 on the block of A, with block length 55, counter t, v[13] = 0 and flags 3, leaves the state X of the names, with the four
constants as X[3], X[7], X[11] and X[15]; C0 has outputs (Y0, y, Y8, Y12); and in the compression of A, E1.c1 = c1, since E1's
third assignment is E1.c1 = Y11 + E1.d1.

(c) *The levels.* A line of step CO is a function of the seven outer words and y. Of the message words only w0 and w1 are lines of
step CT, and so is the counter t; every other message word is a line of step CO or a constant. So the trials of one outer step
differ in w0, w1 and t and in nothing else of their two messages.

Proof. (a) is read off the displays, each formula compared with Section 2 and with its call's inputs, outputs and message words
(Section 1, with v[12] = t, v[13] = 0 and v[15] = 3); Table CT has one name in each of its 88 cells, all different, the four
constant values of K2 among them, and with the five names of E1 and the four lines of E3 they are the 93 lines and the four
constants. (b) As in Lemma T2 (b): an assignment solved for one of its terms is an equivalent equation modulo 2^32 (Fact 1), so a
line's assignment holds once it has run, and by (a) no later line changes its names. By (a) and Table CT all eight assignments of
each call hold, a constant output in its place (the lines for D3.b1 and D3.d1; X8; D1.c1 and X6; D0.d1 and X10) and y as the b
output of C0 (the line for Y8); by Fact 1 the names are the execution of the call. (c) By induction over the printed order, with
(a): a line of step CO reads only constants, the seven outer words, y and lines of step CO; w2, w3, w5 and w7 to w12 are lines of
step CO, w6 is an outer word, w4, w13, w14 and w15 are constants, and w0, w1 and t are lines of step CT. QED.

**Theorem C (the last-chunk half-collision).** For every choice of the seven outer words, of a member y of the class and of a word
c1, steps CO and CT give a counter t. If t is not zero, step CS outputs two distinct messages F || A and F || B of 1024 t + 55 and
1024 t + 63 bytes, with 1 <= t < 2^32, such that

(i) their last chunks are A and B, compressed with counter t, v[13] = 0 and flags 3 (Lemma TR (a));

(ii) the chaining values CV_t(A) and CV_t(B) agree on words 0, 2, 5 and 7;

(iii) in both last-chunk compressions Y4 = y, and the XOR difference between A and B of E3's first-half d value is eta = 830303cf;

(iv) in the compression of A, E1.c1 = c1; and if c1 is in Q*, the XOR difference between A and B of E1's first-half b value is
beta* = 18b0e098.

Proof. t is the XOR of two 32-bit words, so t < 2^32 and t >> 32 = 0, the value v[13] = 0 that the line for K1.a1 used. The
sixteen words have w14 = w15 = 0 and w13 = W13, whose top byte is zero, so A and B are honest strings of 55 and 63 bytes whose
zero-filled blocks are the sixteen words and the same words with w4 and w5 replaced, as in Section 5. By Lemma TR (a) the last
chunks are compressed with counter t, v[13] = 0, flags 3 and block lengths 55 and 63. By Lemma CT (b) round 0 on the block of A
leaves the state X of the names, with the four constants as X[3], X[7], X[11] and X[15]. The counter, v[13] and the flags are the
same in both compressions, and K2 is the only call of round 0 that reads the block length, w4 or w5; Lemma L, whose proof concerns
K2 alone, therefore gives the same state X for B. Lemma H gives (ii): its proof uses only round 1 and o[i] = Z[i] XOR Z[i + 8] for
i = 0, 2, 5 and 7, and the chaining value is (o[0], .., o[7]). (iii) As in the proof of Lemma T: C0 reads the same words of X and
w2, w6 in both compressions and has b output y by Lemma CT (b); w15 = 0, Y14 is the same in both, the a input of E3 is Y3 for A
and Y3' for B by Fact P, and y is in the class, so the difference is eta by the definition of the class (6.1). (iv) E1.c1 = c1 is
Lemma CT (b). E1 has inputs (Y1, Y6, Y11, Y12) and message words (w12, w5) for A, and (Y1, Y6, Y11', Y12) and (w12, w5 + delta)
for B. Its first and second values are the same for both, so its third values are c1 and c1 + DY11, with DY11 = Y11' - Y11 =
0a08818b, and its fourth values are ROR(Y6 XOR c1, 12) and ROR(Y6 XOR (c1 + DY11), 12). Their XOR is ROR(c1 XOR (c1 + DY11), 12),
which is beta* exactly when c1 XOR (c1 + DY11) = ROL(beta*, 12) = 0e09818b. For words c and x, (c XOR x) - c = x - 2 (c AND x)
modulo 2^32, which is the identity of the proof of Lemma Q; with x = 0e09818b this holds exactly when 2 (c1 AND 0e09818b) =
0e09818b - DY11 = 04010000. As 0e09818b has no bit 31 the doubling is exact, and it holds exactly when (c1 AND 0e09818b) =
02008000, that is when c1 is in Q*. The messages are distinct because their lengths differ. QED.

*The counter is the free word.* In the root instance the second assignment of K0 reads the counter 0, so K0.a1 = ROL(K0.d1,16)
follows from the context, and with it the message word w0. Here that assignment is solved for the counter instead, which leaves
K0.a1, and with it w0, free. The word w0 enters round 1 only in the fifth assignment of C2, and the lines for Y2, Y14, Y10, Y6,
E1.a1 and E1.d1 of step CT map their running word one to one, so every value of E1.d1, and so of c1, can be prescribed in one
outer step. With the counter fixed, no order of the assignments has both Y4 and E1.d1 among its free words, and with the counter
free no order has Y4, E1.d1 and E3.h1 all free: the counter buys one prescribed word. These two statements are results of a
participant search over the orders, decided by an exact peeling test that was checked against brute force; nothing below uses
them.

**Lemma IP (the inner permutations and the member with t = 0; GPT Sol 6.1).** Fix the seven outer words and y. (a) The maps c1 ->
E3.h1 and c1 -> t given by step CT are permutations of the 32-bit words. (b) So the 2^21 members of Q* give 2^21 different values
of E3.h1 and of t, and at most one member of Q* has t = 0.

Proof. With the names of step CO fixed, the lines for E1.d1, E1.a1, Y6, Y10, Y14 and E3.h1, with e1 = Y3 + y, each map their
running word one to one. Read backwards: Y14 = ROL(E3.h1,16) XOR e1, Y6 = ROR((Y14 + C2.c1) XOR C2.b1, 7), E1.a1 = Y6 + Y1 + w12
and c1 = Y11 + ROR(E1.a1 XOR Y12, 16). For the counter, Y2 = ROL(Y14,8) XOR C2.d1 = ROL(E3.h1,24) XOR ROL(e1,8) XOR C2.d1, and the
lines for w0, K0.a1 and t give t = ROL(K0.d1,16) XOR (Y2 + IV[0] + IV[4] - C2.a1 - C2.b1), where K0.d1, C2.a1, C2.b1, C2.d1 and e1
are names of step CO. That is a composition of permutations of E3.h1. Its only zero is at E3.h1 = ROR((ROL(K0.d1,16) - IV[0] -
IV[4] + C2.a1 + C2.b1) XOR ROL(e1,8) XOR C2.d1, 24), and the inverse above gives its one value of c1, which may or may not lie in
Q*. QED.

So an outer step has 2^21 or 2^21 - 1 valid trials. Lemma IP bounds the number of trials that the rule t != 0 drops, one in 2^21
at most; it does not bound the share of the collision mass that the dropped trial carries (10.3). In the participant's checks the
member with t = 0 was constructed by the inverse above in 40 outer steps and rejected by the program of entry 26ebba63 in 40 of
40; over 8,192 further outer steps it lay in Q* 4 times, against 4.0 expected, and was rejected 4 times out of 4.

*The length of the messages.* Within one outer step the 2^21 members of Q* give 2^21 different values of t below 2^32 (Lemma IP);
over 2,000 trials of the participant's check t ran from 891,836 to 4,291,586,422 with a mean of log2 t of 30.56. A pair found by
the search has messages of 1024 t + 55 and 1024 t + 63 bytes, shorter than 2^42 bytes and about 2^41 on average. A small t cannot
be chosen: it is the value of a permutation of c1 at the member that the search finds.

**The outer filter.** Number the seven outcomes of beta* whose tau ends in 5020a0 (10.1) j = 1 to 7 in the order of the table of
10.1: 175020a0, 185020a0, 275020a0, 285020a0, 385020a0, 675020a0 and 685020a0, the seven of entry 26ebba63. This search lists six
of them, the set S = {1, 2, 3, 4, 5, 7}: all but 675020a0 (j = 6). In the hexadecimal masks below, with bit j - 1 for outcome j, S
is 5f. Beta* has seven more outcomes on the class, the same seven with bit 14 of tau set (j = 8 to 14 of 10.1); this search does
not list them either. Let tau_j be the tau of outcome j, sigma_j = tau_j XOR ROR(tau_j, 1) and theta_j = ROL(sigma_j, 12); all
seven have eps = 6e21be55. For an outer step put omega = Y3 + y + w8, with Y3 of Fact P, y the member of the outer step and w8 the
name of step CO; DY3 = Y3' - Y3 = fdb77cfd is that of Section 6. For a word x:

- condition (1)_j holds for x when some word h gives (x + h) XOR (x + (h XOR eta)) = theta_j;
- condition (2)_j holds for x when some word f gives (x + f) XOR ((x + DY3) + (f XOR sigma_j)) = eps.

An outer step *passes* the filter when for some j in S both (1)_j holds for its Y9 and (2)_j holds for its omega. Y9 and w8 are
names of step CO and y is drawn with the outer words, so whether an outer step passes depends on the outer step alone and on no
c1.

**Lemma F (the outer filter; GPT Sol 6.1, answers AC and AN).** Fix an outer step that does not pass the filter. Then no trial of
the outer step, for any word c1, has R = 0 with an E1 outcome in S. (A trial with R = 0 whose E1 outcome is another outcome of
beta* on the class may lie in a rejected outer step; the search does not count it.)

Proof. Take a trial with R = 0 whose E1 outcome is outcome j. Write h, g, f and e2 for E3.h1, E3.g1, E3.f1 and E3.e2 in the
compression of A, and h', g', f' and e2' for the same values in that of B. Y9 and w8 are the same in both compressions: w8 is a
line of step CO and a word of both blocks, and Y9 is an output of C1, which reads words of the state X, the same for A and B
(proof of Theorem C), and the message words w3 and w10, which the two blocks share. Both compressions have Y4 = y and h' = h XOR
eta (Theorem C (iii)), and the a input of E3 is Y3 for A and Y3' for B (Fact P). The conditions of R = 0 (Section 13, how r is
counted) give that the XOR difference of E3's first-half b values is psi = tau_j XOR ROR(tau_j, 1) = sigma_j, and that of its a
outputs is eps' = eps. Now g = Y9 + h and g' = Y9 + (h XOR eta); f = ROR(y XOR g, 12) and f' = ROR(y XOR g', 12), so f XOR f' =
ROR(g XOR g', 12) = sigma_j gives g XOR g' = theta_j, and h witnesses (1)_j for Y9. With w15 = 0, e2 = Y3 + y + f + w8 = omega + f
and e2' = Y3' + y + f' + w8 = (omega + DY3) + (f XOR sigma_j), and e2 XOR e2' = eps, so f witnesses (2)_j for omega. So the outer
step passes, against the hypothesis. QED.

The lemma uses no law of the words: no uniformity, no independence and no relation between h and f besides the two equations. It
does not use the rule t != 0, and it holds for any list of outcomes (GPT Sol, answer AN 2), S among them. The filter can pass
outer steps that hold no success, since (1)_j and (2)_j are solved with separate witnesses; it cannot reject an outer step that
holds a success with an outcome of S.

**The exact share (GPT Sol, answers AC, AN and AW; recounted by the participant).** Let pi be the share of the 2^64 pairs (x1, x2)
of words such that for some j in S condition (1)_j holds for x1 and (2)_j for x2. Then

    pi = 18,289,159,183,466,496 / 2^64 = 279,070,422,111 / 2^48,

about 0.00099145731 = 2^-9.978162. With all seven outcomes j = 1 to 7 in place of S the share is 20,504,986,129,465,344 / 2^64 =
312,881,258,079 / 2^48 = 2^-9.813176, which is the share of the seven-outcome filter of entry 26ebba63 and is not used here. Let
pi_E be the share of the 2^32 words x for which (2)_j holds for some j in S: pi_E = 233,715,456 / 2^32, about 0.054416120 =
2^-4.199822.

*Method.* Whether (1)_j holds for x is decided bit by bit from bit 0 upwards. At bit i the XOR of the two sum bits prescribes the
XOR of the two incoming carries; the state is the set of incoming carry pairs that some choice of the lower bits of the witness
reaches with the lower bits of x, and the next state is the set of carry pairs out of bit i that some witness bit gives from a
pair of the set that meets the prescription. The condition holds when the set is still nonempty after bit 31, which has no
outgoing carry to prescribe because the arithmetic is modulo 2^32. For (2)_j the carry of x + DY3 is carried as well. The seven
sets for the seven outcomes are carried together over the same bits of x, each with its own witness (a subset construction), so
one pass over the bits of x gives its *mask*, the set of j for which the condition holds; equal states add their counts of
prefixes of x, and witnesses are never counted. A pair passes exactly when the mask of x1 under (1) and the mask of x2 under (2)
intersect, so the number of passing pairs is the sum, over pairs of intersecting masks a and b, of the number of words with mask a
under (1) times the number of words with mask b under (2).

*Certificate.* Masks are written in hexadecimal with bit j - 1 for outcome j (bit 0 for 175020a0, bit 6 for 685020a0). The numbers
of words with each nonzero seven-bit mask m are 7,936 a_m under (1), a_m the second column, and 1,082,016 b_m under (2), b_m the
fourth and the sixth columns:

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

No other nonzero seven-bit mask occurs; 134,896,128 words satisfy some (1)_j and 233,715,456 some (2)_j. Every mask of (2) in the
table meets 5f, so the same 233,715,456 words satisfy (2)_j for some j in S. The sum of a_m b_n over the pairs of masks m and n
with m AND n AND 5f not zero is 2,129,896, and over all pairs of intersecting masks it is 2,387,944. So the number of pairs that
pass for S is 7,936 * 1,082,016 * 2,129,896 = 18,289,159,183,466,496, and for all seven 7,936 * 1,082,016 * 2,387,944 =
20,504,986,129,465,344 (the participant's arithmetic on the table; GPT Sol's answer AW 3 gives the same 279,070,422,111 and
233,715,456). With the seven other outcomes of beta* on the class added, GPT Sol's certificate of the fourteen-outcome filter
(answer AN 2) gives 99,669,577,442,459,648 passing pairs, 2^-7.531997; that filter is not used here.

*The automata.* The subset construction above is built as four byte tables: a state is the carry of x + DY3 (zero for (1)) and,
per outcome, the set of reachable carry pairs, four bits; the table of byte p maps a state and byte p of x to the next state, and
the table of the last byte maps to the mask. The search builds the two automata for the seven outcomes of entry 26ebba63 once
(step 0 of 9.1) and ANDs every entry of their last tables with 5f, so that every mask it reads is restricted to S; the states and
the number of table loads do not change. The construction has 1, 18, 43, 37 and 1, 3, 7, 7 states at the four byte boundaries and
tables of 25,344 and 4,608 entries (a participant run of the program of entry 26ebba63). Its count of passing pairs for the seven
outcomes is 20,504,986,129,465,344.

## 9. The counter search

**9.1 The algorithm.** The search uses these constants. FACTOR = floor(10 * 138,512,695,296 / 11) = 125,920,632,087 is the factor
of H1' (10.3): ten elevenths, rounded down, of the count in 10.1 of the six outcomes of S. RUN_STEPS_MIN = ceil(0.49594 * 2^128 /
(FACTOR * (2^21 - 1))) = 639,060,516,044,734,036,987 is the least number of outer steps that yields 0.49594 = 24797 / 50000
expected listed good trials at the rate of H1' (10.4). RUN_CONTEXTS = ceil(RUN_STEPS_MIN / 2^19) = 1,218,911,201,562,375, about
2^50.115, counts the contexts of a run (9.8), and RUN_STEPS = 2^19 * RUN_CONTEXTS = 639,060,516,044,734,464,000, about 2^69.115,
its outer steps, 427,013 more than RUN_STEPS_MIN, with 2^90.115 trials in all. A context has 16,384 clusters of 32 members in
2,341 = ceil(16,384 / 7) representative batches (9.9), so a run has 2,341 * RUN_CONTEXTS representative batches, about 2^61.307,
and its opened clusters have the budget A_BUDGET = ceil(852,139 * RUN_CONTEXTS / 2^7) + 16,384 * ceil(sqrt(10 * RUN_CONTEXTS)) =
8,114,703,155,646,753,044, about 2^62.816 (9.9). SHARE = 18,289,159,183,466,496 is the number of pairs that pass the filter for S
(Section 8), whose share pi is therefore SHARE / 2^64, and E_COUNT = 233,715,456 the number of words that pass the automaton of
(2) for S (Section 8). Each of the two budgets is the bound of H4' on the expected number of its outer steps in a run, rounded up,
plus the reserve 2^19 s with the same s = ceil(sqrt(10 * RUN_CONTEXTS)) = 110,404,312 (GPT Sol, answer CK 2.2; 10.3):

    E_BUDGET    = 34,776,155,800,492,855,966   (about 2^64.915)
                = ceil(1000026 * RUN_STEPS * E_COUNT / (1000000 * 2^32)) + 2^19 s = 34,776,097,916,836,926,110 + 57,883,655,929,856,
    PASS_BUDGET = 633,770,615,067,648,623      (about 2^59.137)
                = ceil(1000176 * RUN_STEPS * SHARE / (1000000 * 2^64)) + 2^19 s = 633,712,731,411,718,767 + 57,883,655,929,856.

The batches of a context that can hold a lane with a nonzero mask of (2) are its 2,341 representative batches and, for each of its
16,384 clusters, its two partner chunks or, on a fallback, its five partner batches (9.9), at most 84,261 in all; a batch is
*filled* at its first such lane (9.8). The fills have the budget G_BUDGET, the bound 12,466 of H_G_cluster on the mean number of
filled batches of a context in the walk with five partner batches per opened cluster, which bounds the fills of this walk context
by context (Lemma XF (d)), times RUN_CONTEXTS, plus the reserve 84,261 s with the same s (GPT Sol, answers CM 5 and D14; 10.3):

    G_BUDGET    = 15,194,956,341,454,300,182   (about 2^63.721)
                = ceil(12,466 * RUN_CONTEXTS) + 84,261 s = 15,194,947,038,676,566,750 + 9,302,777,733,432.

Further, the table CT of 9.7 holds, for every subset T of S, the metered cap CM(T) of the call in bits 0 to 15 of its word, with
A(T) of 9.7 above them: CM(T) is the proved cap (Section 11) of steps 2 and 3 with the guards (G7) and (G15) and the certificate
of step 3 on the outcomes of T, with one tree per family (Lemma FX), and CM(T) = 0 when T is empty; CM(T) <= 15,296 for every T
that occurs (Lemma ME). u_M = 92,113,900,425,963 / 2^46 = 1.3090172562... is GPT-6 Astra's exact bound on the mean, over all outer
steps, of the ledger U0 of the work that steps 2 and 3 execute with the global part of 1,024 of the earlier layout, in the model M
of 10.3. The meter debits exactly the ledger U of this row in every call, and U <= (478/487) U0 in every call (Lemmas ME and CP),
so the credit of the solver is m_C = ceil(478 m_0 / 487), m_0 the bound of H5_exec on the expected sum of U0 over a run, at 1.01
times u_M, rounded up, plus a reserve in L_C = 15,296 * 2^19 = 8,019,509,248, the most that one context can debit, plus the
preflight reserve 15,296, the largest metered cap (GPT Sol, answers CK3 4 and D13; 10.3):

    m_0         = ceil(101 * RUN_STEPS * 92113900425963 / (100 * 2^46)) = 844,906,655,693,766,489,106,
    m_C         = ceil(478 * m_0 / 487) = 829,292,364,315,442,262,408,
    CREDIT      = 829,308,674,569,081,960,042   (about 2^69.491)
                = m_C + ceil(sqrt(40 L_C m_C)) + 14 L_C + 15,296 = 829,292,364,315,442,262,408 + 16,310,253,639,682,338 + 15,296.

The four counted events of a run, opened clusters, E lanes, fills and passing lanes, add their units of Section 11, u_O = 144, u_E
= 7, u_G = 56 and u_P = 53, to one register W, the *work register*, which starts at 0. A context tests W once, at its start,
against

    WB    = u_O A_BUDGET + u_E E_BUDGET + u_G G_BUDGET + u_P PASS_BUDGET = 2,296,457,742,736,608,617,309,

and one context adds at most W_CTX = 16,384 u_O + 2^19 u_E + 84,261 u_G + 2^19 u_P = 38,535,192 to W, for its 16,384 clusters,
2^19 members and 84,261 batches. The program of the declared experiment computes these constants by the same formulas and asserts
the budgets, the credit and N against the figures of this text (9.2).

0. Once, before the first context: the two automata of the outer filter for the seven outcomes are built, with the entries of
   their last tables ANDed with S (Section 8); the direct table T2' at word address 0 is filled with the mask of (2), restricted
   to S, of every 32-bit word, three times (T2'[x] = T2[x mod 2^32] for x < 3 * 2^32), and the direct table T1 at word address
   2^34 with the mask of (1) (Lemma DT); the member lists in cluster order, the gate table at word address 2^35 and the table PX
   are written (9.9); so are the table CT of the metered caps (9.7), the three transition arrays, the static row descriptors of
   the six outcomes of S and the written-out code of the walk and of the joint solver with the guards (G7) and (G15) (9.4, 9.7,
   9.8, 9.9, Section 11). The credit register starts at CREDIT and W at 0. Nothing built here depends on an outer word.
1. Walk the contexts one after another, RUN_CONTEXTS of them. A context first compares W with WB and halts the run with failure
   when W > WB. It takes one fresh uniform 256-bit word: its 32-bit words 0 to 6 are the outer words C0.d1, D2.a1, D2.b1, S11, S4,
   X9 and w6, and word 7 is unused. The 39 context lines of step CO (Lemma Y) run once, and the words of the context are prepared
   (9.8), with the four flags and the base of the gate (9.9). The context then runs its 2,341 representative batches one after
   another; lane i of representative batch b carries the representative of cluster 7 b + i. The context also builds the descriptor
   table of its masked partner walk (9.9). *Gate (9.9):* the omega side of a representative batch also gives the key of every lane
   and the carry word IX, and each used lane reads the gate table at its key. On 0 the whole cluster of the lane is skipped, with
   no read of T2' (Lemma CL). Otherwise u_O is added to W, and the representative is walked with the omega of its batch, as below.
   Then its byte guard is tested: on a fire the 31 partners of the cluster are walked in the five partner batches of the earlier
   layout; otherwise the descriptor of the context's table at the carries and the omega prefix of the representative gives at most
   two chunks of at most seven partners, which are walked as batches, and the other partners, which fail test (2) (Lemma XF), are
   not. All this comes before the gate test of the next lane. The outer step of a lane is the context together with the member of
   the lane. *Test (2):* the 8 member-dependent lines of step CO on which omega depends, and omega = Y3 + y + w8, are computed for
   all lanes at once on packed words; each used lane, lane 0 first, then reads from T2' the mask of (2) of its omega, restricted
   to S (9.8). When that mask is zero the outer step of the lane is finished. *E lane:* a lane with a nonzero mask of (2) adds u_E
   to W. *Fill:* the first such lane of its batch adds u_E + u_G instead, in one addition, C0.a1 and D0.d1 of the batch are
   rebuilt, and the 17 member-dependent lines on which only Y9 depends are computed on packed words for all lanes of the batch,
   two of them in one line, and kept in a register as the batch's *cached Y9* (9.8). Then the Y9 of the lane is taken out of the
   cached Y9, its mask of (1), restricted to S, is read from T1, and the AND of the two masks is the mask X of the outer step.
   When X is zero the outer step is finished. Otherwise the outer step *passes* (Section 8): u_P is added to W, and C2.a1, C2.d1,
   C2.c1 and C2.b1 are computed from the words of the batch (9.6). *Pre-check:* compute the word nu of 9.7 from Y9, e1, C2.c1 and
   C2.b1; T = X when nu is 3 or 4, and T = 0 otherwise. If T is zero the outer step ends there (it holds no listed good trial,
   Lemma VP). Otherwise read CM(T) from the table CT; halt with failure when it exceeds the remaining credit (the *preflight*),
   and else run steps 2 and 3 for this outer step under the meter of 9.7, which subtracts from the credit A(T) at the start of the
   call and the unit cost of each block as the block runs.
2. *Roots:* run the joint solver of 9.4 with the guards (G7) and (G15) of 9.7 on Y9, y and omega for every outcome j whose bit is
   set in T. It returns the joint roots of these outcomes that satisfy (G7) and (G15), each a word h with the outcome of which it
   is a root, at most 16 per outer step (9.4).
3. *Certificate (Lemma RC, 10.2; GPT Sol, answer CF 6):* for each returned root h, with its outcome j, in turn, at its leaf:
   compute from h, with the names of step CO and all sums modulo 2^32, the lines of step CT backwards (Lemma IP), Y14 = ROL(h,16)
   XOR (Y3 + y), Z = (Y14 + C2.c1) XOR C2.b1, Y6 = ROR(Z, 7), E1.a1 = Y6 + Y1 + w12, E1.d1 = ROR(E1.a1 XOR Y12, 16), c1 = Y11 +
   E1.d1, E1.b1 = ROR(Y6 XOR c1, 12) and E1.a2 = E1.a1 + E1.b1 + w5, and t by the lines Y2, w0, K0.a1 and t of step CT; put s =
   E1.b1 AND beta*, p = ((tau_j - beta* + 8 + 2 s) mod 2^32) >> 1 and z = ROR(E1.d1 XOR E1.a2, 8). The root is *certified* when

       (Q)  c1 AND 0e09818b = 02008000,
       (A)  E1.a2 AND tau_j = p,
       (C)  (c1 + z) XOR ((c1 + DY11) + (z XOR ROR(tau_j, 8))) = eps,
       (T)  t != 0,

   with DY11 = Y11' - Y11 = 0a08818b and eps = 6e21be55. For the first certified root, form F || A and F || B by steps CT and CS
   for its c1, evaluate blake3 of both in full, check that the two digests agree, output the pair and halt.
4. If no pair has been output when the last context ends, halt with failure.

There are exactly three ways for the run to halt with failure, each a test on a value kept by the algorithm: W exceeds WB at the
start of a context, the metered cap CM(T) of an outer step that reaches the solver exceeds the remaining credit, or the contexts
run out. W is the sum of u_O, u_E, u_G and u_P times the counts of opened clusters, E lanes, fills and passing lanes so far. A
context starts only when W <= WB and adds at most W_CTX, so W <= WB + W_CTX at every moment of a run: the units of these four
events add up to at most WB + W_CTX (Section 11). If none of the four counts exceeds its budget, A_BUDGET, E_BUDGET, G_BUDGET or
PASS_BUDGET, then W <= WB; so W halts the run only on the union of the four overflow events of 10.4. The metered debits of the
outer steps that run steps 2 and 3 add up to at most CREDIT: a call starts only when the credit left covers CM(T), and it debits
at most CM(T) (Lemma ME), so the credit never goes below zero. Steps 2 and 3 need no budget of their own, since the joint solver
returns at most 16 roots and, whatever the words of an outer step, their work in it is at most its CM(T) and its debit is that
work (9.4, 9.7, Section 11). The work of every run is therefore bounded by the counts of Section 11, and a pair of messages is
formed and hashed at most once, for a certified root.

A trial is *valid* when its t is not zero; a valid trial with R = 0 is *good*; a good trial is *listed* when its E1 outcome is in
S (Section 8, 10.1). A listed good trial is found unless the run ends before its outer step is reached, by the work register W, by
the credit or by the output of another pair: its outer step passes the filter by Lemma F, its cluster is opened by Lemma CL, its
member is walked by Lemma XF, its lane is taken as passing by Lemmas MB and DT, the pre-check keeps its outcome by Lemma VP, the
joint solver returns its E3.h1 as a root of its outcome by Lemmas G7, G15 and CV, and step 3 certifies it (Lemmas RC and CV,
10.2). Every certified root is the E3.h1 of a listed good trial (Lemma CV). A good trial that is not listed is not found, and
Section 10 does not count it; by the count of 10.1 beta* has eight more outcomes on the class, 675020a0 and the seven with bit 14
of tau set, which carry 4,065,280 of its 71,698,432 (5.7 per cent) and are not listed. When the run outputs a pair, the pair is a
collision of two complete messages: the certified trial has R = 0 (Lemma V, 10.2), step 3 has checked both digests, and Lemma TR
(c) says that R = 0 with the half-collision of Theorem C gives equal digests.

**9.2 The declared experiment.** The program `experiments/frontline.py` (Python 3, standard library only, no BLAKE3 library) holds
this search: steps CO, CT and CS from the printed lines, with the flags word as an input; the two automata of the filter,
restricted to S; the walk of 9.8 and 9.9 with the straddle gate, the byte guard and the masked partner walk with its descriptor
table, test (2), the E lane, the fill and the cached Y9 of each batch, the passing lane, the pre-check, the preflight against
CT[T] = CM(T) and the meter; the joint solver of 9.4 with (G7) and (G15); the certificate of step 3; the three halts above; and
the constants of this section, computed by the formulas above and asserted equal to the figures of this text. Entries of T1, T2'
and the gate table are computed on demand by the rules that fill those tables (Lemma DT, 9.9), and the units of Section 11 are
added per event: 112,519 per context, 59 per representative batch (45 for the last), 144 per opened cluster, 7 per E lane, 56 per
fill, 53 per passing lane and the metered debit of each call. The meter is kept in the traversal itself: A(T) when the call
starts, and at every forced, free, leaf and root block its unit cost of Section 11. W is a variable of the walk.

One organizer trial is one context: seven fresh outer words from the trial's seed, the 39 context lines once, and representative
batches 0 to 3 and the context's last batch, 32 clusters, with the partners of every opened cluster. A trial starts with W = 0 and
the full CREDIT, so at this scale neither WB nor the credit is reached. In the same run every member of every walked cluster is
recomputed straight-line (all 77 lines of step CO, no packing) and its omega modulo 512 tested against the two prefixes of Lemma
KP; every member of a closed cluster is tested bit by bit for (2) and against S7, a pass being counted as a skipped pass and a
mismatch; the key of the gate is compared with the one formed from the scalar omega, Y0 and e1 and the flags of the context, and
its entry with S7 at omega and the straddle rule read from the two exact prefixes of Lemma KP, and every index of T2', T1 and the
gate table with the range of its table; every partner of a cluster walked by its descriptor is compared with it: its omega modulo
2^14 with the window arithmetic of Lemma XF, its survival with the rule alive16, and every partner not walked is tested bit by bit
for (2); every T1 and T2' entry used is compared with a bit-serial decision of (1) or (2); at every passing lane C2.a1, C2.d1,
C2.c1, C2.b1 and the pre-check are compared with a scalar rebuild of step CO and with VMASK[nu] of 9.7, and the source bank of the
solver with the rebuild; at every E lane the cached Y9 of the batch is compared with a fresh fill, and the step-CT message is
compressed and its Y4, Y9 and omega compared with the packed lanes; the metered debit of every call is compared with the ledger U
of the same call, from its node counts, and must equal U and be at most CM(T); every solver call is repeated by the traversal
without (G15), whose roots are certified by real compressions; and every eighth trial plants a joint root, built from (J1) to
(J3), that both traversals must return, with the same meter test. The returned pair is that of 6.4, and the 16 observations are
the program's own counts, which the organizer records as untrusted. In the participant's run of the public request (256 trials):
3,349 of 8,192 clusters opened (0.409), 35,772 members walked, 13,481 E lanes in 3,378 filled batches, 225 passes, 64 solver
calls, no root, 379,131 checks, 0 skipped passes and 0 mismatches; the 256 pairs are those of entry 50d28015 on the same request.
Over 4,096 trials of our own seeds, 52,748 of 131,072 clusters opened (0.4024, below the bound of Lemma OR), 229,018 E lanes among
the 4,194,304 members of these clusters (0.0546) in 57,642 filled batches, 569,568 members walked, 3,998 passes and 1,031 solver
calls, with 0 skipped passes and 0 mismatches. 256 of 256 pairs met the event, recomputed with the organizer's
`verifier/blake3.py`; the run took 6.8 to 7.0 s, container start included, in the organizer's image with one processor and 128 MB.
Not exercised at this scale: a root of the search itself and a halt; the machine layout of 9.8 and 9.9 (pair loads, registers, the
written-out code) is kept in variables with the same decisions; the units of the walk's events (the omega side, key, carry word,
gate and lane tests, byte guard, descriptor selection, broadcasts, chunk addressing, E lane, fill, shortcut, pre-check and
preflight) were counted in this program as it ran, statement by statement (Section 11).

**9.3 The self-test.** `python3 experiments/frontline.py --selftest`, which the organizer does not run, checks the constants of
9.1 against this text; both automata against brute force at width 8 (256 of 256); SHARE and E_COUNT recounted from the tables; T1
and T2 against the bit-serial decisions on 8,000 random words, and on those words T2(x) = 0 whenever x mod 128 is not in S7; the
208 residues of Lemma A9, four copies of S7; the cluster map as a bijection of the 2^19 member numbers; the pre-check of 9.7
against nu and VMASK on 3,997 quadruples of random words; on 16 random contexts, y[16..24] = 2 T_i for 272 representatives and,
for each of them at all 256 values of A[0..7] with A[8..15] = p[8..15], the straddle rule of the flags hbad_i against the two
exact prefixes of Lemma KP (69,632 cases, 1,944 of them straddling); the gate entry against an independent form of S7 and of the
straddle rule on 8,000 indices, half of them with mid = a, at both values of bit 7; the omega side of F1 and the fill against step
CO on 224 lanes of 32 contexts; halt drills: a context that starts with W = WB + 1 halts before its first member, one that starts
with W = WB runs to its end with WB < W <= WB + W_CTX, and the credit halts; a drill in which a credit of exactly the preflight
reserve 15,296 admits the first call; and on 8 seeds that the gate table and an always-open gate give the same E lanes (436),
fills (106) and passes (10), that an always-closed gate gives 436 skipped passes (the 436 E lanes), and that the walk without the
mask, all partners in five batches, gives the same E lanes and passes with 195 fills and 3,976 members walked against 1,238. The
program asserts CM(T) <= 15,296 for every T of a call, the exact row of Section 11 and that every leaf's parent is a forced node,
at position 31.

**9.4 The joint solver (GPT Sol, answers AE, AF, AI, AL, AO and AR).** Fix a passing outer step and write Q = Y9, y for its
member, E = omega = Y3 + y + w8 and E' = E + DY3; x[i] is bit i of a word x, bit 0 the lowest, and maj is the majority of three
bits. Put e1 = Y3 + y and b = e1[2], u = e1[21] and v = e1[26], three bits that are free in the class (in the sub-class of entry
26ebba63, u = v = 0). For an outcome j of beta* (10.1) put sigma = sigma_j and theta = theta_j (Section 8), eps = 6e21be55, gamma
= eta XOR theta, D = (sigma XOR eps) AND 7fffffff, kappa = sigma XOR eps XOR E XOR E' and mu = ROR(eta XOR eps, 8) = 9aed22bd. For
a word h put g = Q + h, f = ROR(y XOR g, 12), e2 = E + f and h2 = ROR(h XOR e2, 8): for E3.h1 = h these are E3.g1, E3.f1 and E3.e2
of step CT and the d output of E3 on message A (6.2). The *static descriptor* of outcome j holds sigma, theta, gamma, D and the
positions of its constants and guards; the static descriptors of the six outcomes of S depend on no outer word and are formed once
per run.

*Joint roots.* A word h is a *joint root* of outcome j when

    (J1)  (Q + h) XOR (Q + (h XOR eta)) = theta,
    (J2)  (E + f) XOR (E' + (f XOR sigma)) = eps,
    (J3)  (g + h2) XOR ((g XOR theta) + (h2 XOR mu)) = tau_j.

(J1) and (J2) are the conditions (1)_j and (2)_j of Section 8, with the two witnesses tied by f = ROR(y XOR (Q + h), 12). By (J1)
theta is a function of h, and then so is the left side of (J3); the seven values of tau are different, so no word is a joint root
of two outcomes. There is no rule A: a joint root is any word that satisfies (J1) to (J3).

*Carries.* Write u[i] and u'[i] for the carries into bit i of Q + h and of Q + (h XOR eta), and a[k] and a'[k] for those into bit
k of E + f and of E' + (f XOR sigma), all 0 into bit 0. Bit by bit, (J1) holds exactly when u'[i] = u[i] XOR gamma[i] for every i,
and (J2) exactly when a'[k] = a[k] XOR kappa[k] for every k. Bit i of h gives g[i] = Q[i] XOR h[i] XOR u[i] and bit k = (i + 20)
mod 32 of f, f[k] = y[i] XOR g[i]. So the solver chooses h from bit 0 to bit 31 and runs both pairs of additions along it: those
of (J1) on bits 0 to 31, and those of (J2) on bits 20 to 31 and then 0 to 19. The carry a[20] is not known at the start; it is
guessed for the constants of (a) below, and the check of (J2) as a word at each leaf enforces that bits 0 to 19 give the right
carry into bit 20 (one traversal, below). At a bit k < 31 with D[k] = 1, the *prescription* of f[k] is f[k] = E[k] XOR sigma[k]
XOR kappa[k+1] if a[k] = E[k], and f[k] = E'[k] XOR kappa[k+1] otherwise: from carries a[k] and a[k] XOR kappa[k], it is the only
value of f[k] that gives the carries into bit k + 1 the difference kappa[k+1] (Lemma S5).

*The phase equations (GPT Sol, answer AO 5 and 6.1).* The participant's counter, run on the class with its E3 count split by the
pattern of h on the sixteen bits 0 to 3, 6 to 13, 16, 17, 24 and 25 and by (b, u, v), records for each of the eight values of (b,
u, v) every pattern that occurs in a solution of E3 with an outcome of beta* (records of the participant, not in the package). GPT
Sol checked every recorded pattern against

    h[0] = 0,  h[1] = 1,  h[2] = 1 XOR b,  h[10] = b,  h[16] = h[17] = 0,
    h[11] = 1 XOR h[3],  h[24] = h[3] XOR h[12] XOR u                   (PHASE)

and found no violation in any of the eight cells, whose sets have 88, 88, 108, 132, 108, 132, 88 and 88 patterns in the order b +
2u + 4v. Each of the fourteen outcomes of beta* on the class has an E1 count L_j > 0 that depends neither on y nor on h, so a zero
count outside (PHASE) means that no joint root of any of them, the six of S among them, violates (PHASE). The equations are
consequences of the count, which the solver uses as guards; they are not a rule that drops members or solutions.

*The parity certificate (GPT Sol, answer AR 1).* Call the outcomes j = 1 to 7, whose tau ends in 20a0, the *old rows*, and j = 8
to 14, whose tau ends in 60a0 and has bit 14 set, the *new rows*; a row is also named by the first three hexadecimal digits of its
tau. Every joint root h of outcome j, for y in the class, satisfies

    h[6] XOR h[13] XOR h[25] = u XOR tau_j[14],                        (P*)

that is h[6] XOR h[13] XOR h[25] = u on the old rows and u XOR 1 on the new rows. This search lists only the old rows, on which
(P*) reads h[6] XOR h[13] XOR h[25] = u; the certificate is stated for all fourteen rows as it was proved. The proof is an exact
finite count. The count N3_j of 10.1 counts the quadruples (Y4, E3.h1, Y9, w8), Y4 in the class, that meet the E3 conditions of
outcome j, and by the proof of Lemma V (10.2) these are exactly the quadruples whose E3.h1 is a joint root of outcome j for Q =
Y9, y = Y4 and E = Y3 + Y4 + w8. GPT Sol split every N3_j by the phase (b, u, v) of Y4 and by the parity pi = h[6] XOR h[13] XOR
h[25] of the root. The split is a sum of nonnegative integers over an exact enumeration of submasks, through the identity (z XOR
m) - z = m - 2 (z AND m) modulo 2^32 and a carry recurrence with two states in integers, in coordinates of E3 that are a bijection
of the counted quadruples; nothing is sampled. With a = 24, 16, 4, 24, 32, 1 and 6 for the rows 175, 185, 275, 285, 385, 675 and
685:

| rows | phases (b, u, v) with a nonzero count | count in each such phase | pi | count with the other pi |
| --- | --- | ---: | --- | ---: |
| old, all seven | all eight | a * 2^49 | u | 0 |
| new 185, 285, 385, 685 | u XOR v = 1 | a * 2^47 | u XOR 1 | 0 |
| new 175, 275, 675 | u XOR v = 1 and b = 1 | a * 2^47 | u XOR 1 | 0 |

Every other cell has count 0. Every joint root adds at least 1 to the cell of its phase and its parity, so a cell of count 0
holds no root at all: (P*) holds for every joint root of the fourteen outcomes on the whole class, pointwise and not on average,
and it drops no member and no root. The cells add up to the fourteen N3_j of 10.1 exactly: 8 * a * 2^49 = a * 2^52 on the old
rows, 4 * a * 2^47 on the new rows 185, 285, 385 and 685, and 2 * a * 2^47 on the new rows 175, 275 and 675 (checked by a helper
agent of the participant). In the phase b = 1, u = 0, v = 1, the 2^16 members of the class with e1 AND 07ef8307 = 070c0307, a
separate exact count of a helper agent of the participant, with the function N3_count of the counting program of Section 17 and
the parity as one more condition, gives all fourteen counts with pi = 0 on the old rows, pi = 1 on the new rows and the count 0
with the other pi, as the table says. The cells of the other seven phases are GPT Sol's evaluation and were not re-run by the
participant. The count shows as well that a new row has no joint root when u = v, and a new row 175, 275 or 675 none when b = 0;
the search of this package lists no new row.

*The guard on the third addition (GPT Sol, answer AR 6.1).*

**Lemma J0.** Every joint root h of every one of the seven outcomes has h2[0] = 0, that is h[8] = e2[8].

Proof. For all seven outcomes tau_j[0] = tau_j[1] = 0, theta_j[0] = theta_j[1] = 1 and gamma[1] = gamma[2] = 0, and mu[0] = 1,
mu[1] = 0. By (PHASE) h[0] = 0 and h[1] = 1. In (J1) both carries into bit 0 are 0. Since eta[0] = eta[1] = 1 and gamma[1] = 0,
the carry Q[0] AND (h[0] XOR 1) = Q[0] of the second addition into bit 1 must equal the carry Q[0] AND h[0] = 0 of the first, so
Q[0] = 0 and g[0] = 0; since gamma[2] = 0, the carry maj(Q[1], 0, 0) = 0 of the second addition into bit 2 must equal the carry
maj(Q[1], 1, 0) = Q[1] of the first, so Q[1] = 0 and g[1] = 1. Both additions of (J3) have carry 0 into bit 0. At bit 0, g + h2
adds 0 and h2[0], with sum bit h2[0] and carry 0 out; (g XOR theta) + (h2 XOR mu) adds 1 and h2[0] XOR 1, with sum bit h2[0] and
carry 1 XOR h2[0] out. At bit 1, g + h2 adds 1, h2[1] and 0, with sum bit 1 XOR h2[1]; the other adds g[1] XOR theta[1] = 0, h2[1]
XOR mu[1] = h2[1] and 1 XOR h2[0], with sum bit h2[1] XOR 1 XOR h2[0]. (J3) at bit 1 requires the XOR of the two sum bits, which
is h2[0], to be tau_j[1] = 0. So h2[0] = 0, and h2[0] is bit 8 of h XOR e2. QED. The zero carries into bit 0 are those of addition
modulo 2^32; nothing is guessed. The participant checked the bits that the proof reads for all fourteen outcomes of beta* on the
class, the six of S among them.

e2[8] is produced at position i = 20 of the traversal (k = 8): e2[8] = E[8] XOR f[8] XOR a[8] with f[8] = y[20] XOR Q[20] XOR
h[20] XOR u[20], and every term but h[20] is known when position 20 is reached, h[8] among them. So Lemma J0 is a forward guard
that sets h[20] = h[8] XOR E[8] XOR a[8] XOR y[20] XOR Q[20] XOR u[20]. It holds for every joint root, so no root is lost, and
position 20, which no constant and no carry prescribes on any row, is no longer free.

*The constants and guards of an outcome.* For y in the class, every joint root of outcome j has the following values, which the
solver computes from Q, y, E and the outcome before it branches, or checks during the traversal (GPT Sol, answers AE 2.1, AF 1.2,
AN 6, AO 6.1 and AR 2 and 6.1). Every member of the class has y[0] = 0, y[1] = 1 and bits 16 to 19 of y equal to 0, 0, 1, 0, so
f[20] = f[21] = 0, bits 4 to 7 of f are the constant 2, the carry u[20] is Q[19], and the first addition is reset as in the
sub-class.

(a) *The carry into bit 22.* For each guess a[20] = 0 and a[20] = 1, with a'[20] = a[20] XOR kappa[20], run bits 20 and 21 of both
additions of (J2) with f[20] = f[21] = 0, and keep the guess only if a'[21] = a[21] XOR kappa[21] and a'[22] = a[22] XOR
kappa[22]. If no guess is kept, the outcome has no joint root. Two kept guesses have the same carries into bit 21, and so into bit
22: all seven outcomes have sigma[20] = sigma[21] = 1, eps[20] = 0 and eps[21] = 1, and the cases E[20] = E'[20], E[20] = 0 with
E'[20] = 1, and E[20] = 1 with E'[20] = 0 give, in turn, at most one guess that passes bit 21, equal carries into bit 21 for both
guesses, and at most one guess that passes bit 22. Write a[22] for the common carry.

(b) f[22] is its prescription (D[22] = 1). If gamma[3] = 0, then D[23] = 1 and f[23] is its prescription; if gamma[3] = 1, f[23] =
1 XOR Q[3] XOR y[3]. Run bits 22 and 23 of (J2); if a'[23] is not a[23] XOR kappa[23] or a'[24] is not a[24] XOR kappa[24], the
outcome has no joint root. This gives a[24].

(c) h[0] = 0, h[1] = 1 and u[2] = 0; h[2] = y[2] XOR f[22] XOR Q[2], and the outcome has no joint root unless h[2] = 1 XOR b; u[3]
= maj(h[2], Q[2], 0); h[3] = y[3] XOR f[23] XOR Q[3] XOR u[3] and u[4] = maj(h[3], Q[3], u[3]); h[10] = b and h[11] = 1 XOR h[3];
u[11] = maj(h[10], Q[10], Q[9]) if gamma[10] = 0 and u[11] = Q[10] if gamma[10] = 1; u[12] = maj(h[11], Q[11], u[11]).

(d) f[0] is its prescription with a[0] = 0 (D[0] = 1), and a[1] = maj(E[0], f[0], 0); h[12] = y[12] XOR f[0] XOR Q[12] XOR u[12],
u[13] = maj(h[12], Q[12], u[12]) and h[24] = h[3] XOR h[12] XOR u.

(e) Bit 16 of h2 is 0, so f[24] = h[24] XOR E[24] XOR a[24]; h[4] = y[4] XOR f[24] XOR Q[4] XOR u[4] and u[5] = maj(h[4], Q[4],
u[4]). Run bit 24 of (J2); if a'[25] is not a[25] XOR kappa[25], the outcome has no joint root. f[25] is its prescription (D[25] =
1), a[26] = maj(E[25], f[25], a[25]) and h[5] = y[5] XOR f[25] XOR Q[5] XOR u[5].

(f) Bits 6, 13, 25 and 26 depend on the kind of the outcome; (P*) is used on every row. The outcomes of S are old rows of two
kinds (675020a0, an old row that this search does not list, is described with them).

- *Low old rows, 175020a0, 275020a0 and 675020a0:* if E[1] = a[1], the carry into bit 2 is E[1], f[2] is its prescription (D[2]
  = 1) and e2[2] = E[2] XOR f[2] XOR E[1]; otherwise the outcome has no joint root if kappa[2] = 1, and e2[2] = E[2] XOR
  kappa[3] if kappa[2] = 0. Then h[26] = 1 XOR h[2] XOR e2[2] XOR Q[26] XOR Q[25], f[26] = h[26] XOR E[26] XOR a[26] and h[6] =
  f[26] XOR y[6] XOR gamma[7]. By (P*), h[25] = h[6] XOR h[13] XOR u: a forward guard, set once bit 13 of h is chosen.
- *High old rows, 185020a0, 285020a0, 385020a0 and 685020a0:* h[25] = e2[1] (answer AE 2.1), where e2[1] = E[1] XOR f[1] XOR a[1]
  and f[1] = y[13] XOR Q[13] XOR h[13] XOR u[13]. With (P*), h[6] = h[13] XOR h[25] XOR u = y[13] XOR Q[13] XOR u[13] XOR E[1] XOR
  a[1] XOR u, in which h[13] cancels: h[6] is fixed by (c) and (d), which give u[13] and a[1]. The guard of position 25 is then
  h[25] = h[6] XOR h[13] XOR u, the same as h[25] = e2[1]. h[26] = e2[26] (bit 18 of h2 is 0), and e2[26] is given by position 6,
  whose value is now fixed, so h[26] is a constant of the row.

(g) h[16] = h[17] = 0, h[18] = 1 XOR Q[18], h[19] = Q[19], and, if gamma[7] = 1, h[7] = 1 XOR gamma[8] XOR h[6], now a constant on
every row.

On every row h[29] = 1 XOR e2[29] (bit 21 of h2 is 1), where e2[29] is known once bit 9 of h is chosen, and h[20] is set by Lemma
J0. These are the *constants and guards* of the outcome. On every row h[0] to h[6] are fixed before the traversal; the guards that
read bits chosen during the traversal are those of position 20 (every row), position 25 (the old rows) and position 29 (every
row). In entry 26ebba63 the parity h[25] = h[6] XOR h[13] was a condition of rule A on the sub-class; here (P*) is not a rule but
a consequence of the count of the class, true of every joint root.

*One traversal.* Every carry guess a[20] that (a) keeps reaches, after the constants h[0] to h[6], the same state: the same bits
h[0] to h[6], the same carries u[7] and a[27], and the same e2[26]; the values e2[20] and e2[21], which depend on the guess, are
not used by any guard. So the solver walks bits 0 to 6 under both kept guesses with the tests of (a), (b) and (e), then drops the
guesses and starts one depth-first traversal for each searched outcome at depth 7 from that state, and checks (J1), (J2) and (J3)
as words at each leaf, which enforces the closure of the carries that the guess stood for (GPT Sol, answers AO 2 and 6.1 and AR
2). Every joint root survives a guess and reaches this common state, and a single traversal over the bits of h reaches every h at
most once.

*Transitions.* For each position i = 7, .., 31, with k = (i + 20) mod 32, each pair (u[i], a[k]) of incoming carries and each
value v of h[i], put g[i] = Q[i] XOR v XOR u[i], u[i+1] = maj(Q[i], v, u[i]) and u'[i+1] = maj(Q[i], v XOR eta[i], u[i] XOR
gamma[i]), and require u'[i+1] = u[i+1] XOR gamma[i+1] if i < 31; put f[k] = y[i] XOR g[i], e2[k] = E[k] XOR f[k] XOR a[k], a[k+1]
= maj(E[k], f[k], a[k]) and a'[k+1] = maj(E'[k], f[k] XOR sigma[k], a[k] XOR kappa[k]), and require a'[k+1] = a[k+1] XOR
kappa[k+1] if k < 31. A value that passes is an arc to the pair (u[i+1], a[k+1]), or to (u[i+1], 0) if k = 31, since both carries
into bit 0 of (J2) are 0 (kappa[0] = 0: E'[0] differs from E[0], eps[0] = 1 and sigma[0] = 0 for all seven outcomes); the arc
records v and e2[k]. The *descriptor* of a position is 14 bits: Q[i], y[i], E[k], E'[k], eta[i], gamma[i], sigma[k], kappa[k],
gamma[i+1], kappa[k+1], whether the position has a constant and its value, and whether i = 31 and k = 31 (GPT Sol, answer AI 1).
The solver reads the arcs from three arrays built once per run (answer AR 6.2), each entry computed by the relation above, which
is the same relation and not an approximation; an arc is five bits, the next carry pair, h[i], e2[k] and a validity bit:

| array | key | words | entry |
| --- | --- | ---: | --- |
| forced | descriptor and carry pair | 2^16 | the one passing arc, or invalid |
| dual | descriptor and carry pair | 2^16 | both arcs, packed in one word |
| selected | descriptor, carry pair and a desired bit | 2^17 | the passing arc whose e2[k] is the desired bit, or invalid |

A position with a constant reads the forced array with the constant in its descriptor. A position i < 31 with gamma[i] = 1, or
with k < 31 and D[k] = 1, has at most one passing value by Lemma S5 and reads the forced array as well. A position with a guard on
bits chosen during the traversal, 25 on the old rows and 29 on every row, reads the forced array with the value of the guard
written into the constant field of its key: 1 XOR e2[29], from the saved bit e2[29], and h[6] XOR h[13] XOR u, from bit 13 of the
prefix of h. Position 20 reads the selected array with the desired bit h[8] (Lemma J0); as e2[8] changes with h[20], at most one
arc has it. A free position (below) reads the dual array. So a position that is not free has at most one child.

*The search.* From the common state at depth 7, search depth first over the positions 7 to 31: a node at depth d has a child at
depth d + 1 for each arc of position d from its carry pair that meets the guards of the position. A node at depth 32 is a *leaf*;
it gives a root when its h satisfies (J1), (J2) and (J3) as words. The root is returned with the outcome j.

*Counts.* Call a position i >= 7 *free* when it has no constant and no guard, gamma[i] = 0 or i = 31, and D[(i + 20) mod 32] = 0,
and *prescribed* otherwise. For a row with the set F of free positions put n_i = 2^(the number of free positions p with 7 <= p <
i), for i = 7, .., 32. A traversal of the row has at most n_i nodes at depth i: at most the sum of n_i over the prescribed
positions *forced* nodes, the sum over the free positions *free* nodes, n_20 *selected* nodes among the forced ones (position 20
is prescribed on every row, by Lemma J0), and n_32 = 2^|F| leaves (GPT Sol, answer AR 6.5; recomputed by the participant from the
free positions):

| tau | free positions | forced nodes | free nodes | selected nodes | leaves |
| --- | --- | ---: | ---: | ---: | ---: |
| 175020a0 | 7, 13, 15, 30 | 142 | 15 | 8 | 16 |
| 185020a0 | 13, 15, 30 | 72 | 7 | 4 | 8 |
| 275020a0 | 9, 13, 15, 30 | 140 | 15 | 8 | 16 |
| 285020a0 | 7, 9, 13, 15, 30 | 278 | 31 | 16 | 32 |
| 385020a0 | 9, 13, 15, 30 | 140 | 15 | 8 | 16 |
| 675020a0 | 13, 15, 30 | 72 | 7 | 4 | 8 |
| 685020a0 | 7, 13, 15, 30 | 142 | 15 | 8 | 16 |

These are counts of the static trees: an arc that fails a carry test or a guard only removes nodes, and the trees that occur may
be smaller. The row 675020a0 is not in S: its line is kept as proved, and this search does not build its tree.

*The trees with the guard (G7).* The guard (G7) of 9.7 fixes position 7 on every row before the traversal (GPT Sol, answer AX
1.1), so with it position 7 is free on no row. The rows 175020a0, 285020a0 and 685020a0 lose the free position 7 that the table
gives them: with (G7) they have 72, 140 and 72 forced nodes, 7, 15 and 7 free nodes, 4, 8 and 4 selected nodes and 8, 16 and 8
leaves, and the other rows of S are unchanged. These trees with (G7) are those of our entry 0bc5f130; the table above is that of
the solver without (G7).

*The trees with the guards (G7) and (G15).* The guard (G15) of 9.7 prescribes position 15, which is free on every row of S with
(G7) (GPT Sol, answer CF 7.2). With both guards the rows 175020a0, 185020a0 and 685020a0 have the free positions 13 and 30, 42
forced nodes, 3 free nodes, 2 selected nodes, 2 nodes at position 15 and 4 leaves, and the rows 275020a0, 285020a0 and 385020a0
the free positions 9, 13 and 30, 80 forced nodes, 7 free nodes, 4 selected nodes, 4 nodes at position 15 and 8 leaves (the counts
of the table's rule; a node at position 15 is a forced node). These trees with (G7) and (G15) are the trees of the solver of this
package.

The outcomes searched in an outer step that reaches the solver have their bits set in T, a subset of the mask of Y9 under (1) and
of S. By the certificate of Section 8 every nonzero mask under (1) is one of the twelve nonzero seven-bit masks of its table, and
each of these is a subset of {275020a0}, {175020a0, 675020a0}, {285020a0, 385020a0} or {185020a0, 385020a0, 685020a0}. So the
searched outcomes are among the rows of one of these four sets restricted to S: {275020a0}, {175020a0}, {285020a0, 385020a0} and
{185020a0, 385020a0, 685020a0}. With (G7) alone they have (140, 15, 8), (72, 7, 4), (280, 30, 16) and (284, 29, 16) forced, free
and selected nodes and 16, 8, 32 and 32 leaves. With (G7) and (G15), in the solver of this package, they have (80, 7, 4), (42, 3,
2), (160, 14, 8) and (164, 13, 8) forced, free and selected nodes, 4, 2, 8 and 8 nodes at position 15, and 8, 4, 16 and 16 leaves.
A leaf gives at most one root. So an outer step has at most 3 searched outcomes, 16 leaves and 16 roots, whatever its words (GPT
Sol, answers AT 1, AW 2, AX 1.1 and CF 7.2).

*Families.* Within one of the four sets the rows fall into *families* by two marks: low row (175, 275, 675) or high row (185, 285,
385, 685), and the bit gamma[10] (on the class the new rows, which this search does not list, would form families of their own).
gamma[3] is 0 on the low rows and 1 on the high rows, gamma[10] is 1 on the rows 675 and 685 and 0 on the others, and sigma[20] to
sigma[26] and sigma[0] to sigma[3] are the same on all low rows and on all high rows; gamma[10] fixes the reset of u[11] in (c).
So the formulas of (a) to (e) and the walks of bits 0 to 5 under both guesses are the same for the rows of a family and are
evaluated once per family (GPT Sol, answer AR 6.4). Restricted to S the four sets have 1, 1, 1 and 2 families, and at most two
rows of a set share a family. gamma[7] can differ within a family, so bit 6 and its outgoing carries, h[6], h[7] and h[26] are
computed for each row: no prefix of seven bits is shared.

*What is proved and by whom.* The phase equations, the guards of (c), (d) and (e), the single traversal and the common state are
GPT Sol's (answers AO 5, 6.1 and 6.2 and AR 2), on the constants of answers AE 2.1, AF 1.2 to 1.4 and AN 6 and the transition
relation of answer AI 1; the parity certificate (P*), Lemma J0, the guards of (f) with (P*), the three arrays, the families and
the counts of the static trees are GPT Sol's answer AR (1, 2 and 6.1 to 6.5); the restriction of the solver to the outcomes of S,
with the four sets above, is its answer AW 2, the same solver visiting only the outcomes of T, with the same proofs; the guard
(G7), with its trees above, is its answer AX 1; and the guard (G15), with its trees above, is its answer CF 7, with the row-set
caps of Section 11, which Lemma FX of 9.7 lowers (answers CF 7.2 and CD 11). The participant recomputed the free positions, the
node, leaf and selected counts of the table and of the four sets, the families, the bits that Lemma J0 reads, and the sums of the
parity certificate against the counts of 10.1; the other constants and guards were not re-derived by the participant. At positions
25 and 29 the guard selects the candidate before the table read (GPT Sol's corrected answer AR 6.3): these positions are not
prescribed by the carries, so the value of the guard is written into the key before the read, within the same allowance and the
same proved cap (Section 11). Lemma CV (10.2) states what the solver returns. The layout is specified and charged by this text; it
is not an implementation (9.5).

**9.5 Checks of the joint solver.** The solver of 9.4 with the guards (G7) and (G15), the certificate of step 3, and the
pre-check, the preflight and the meter of 9.7 are executed by the declared program (9.2) on every passing outer step of its
trials, with each solver call repeated by the traversal without (G15) and planted joint roots returned by both; no root of the
search itself occurs at that scale. The completeness of the solver rests on the proofs cited in 9.4, on Lemmas G7, G15 and RC, on
the count of the class and on the parity certificate; its cap of 15,296 machine units rests on the schedule of Section 11 and on
Lemma FX, an upper allowance written out block by block, which the program checks against its own count of nodes on every call, as
it checks the metered debit against Lemma ME; and the pre-check rests on Lemma VP, whose bit identity was checked on real trials
(9.7).

**9.6 Packed words and the shortcut of a passing lane (GPT Sol, answer AQ; our audit).** The walk of 9.8 and Section 11 use the
packed words of 6.5, lane i being bits 36 i to 36 i + 35 of a word. The low 32 bits of a lane are the scalar value modulo 2^32,
and every lane of every sum stays below 2^36, so that no carry leaves its lane; where an interval bound of a sum could reach 2^36,
an AND with the word M that has the low 32 bits of every lane set is made first, and charged. x - z is formed as x + (z XOR M) +
1, never by a packed subtraction, whose borrows could cross lanes. A rotation by r is PROR: ((x >> r) AND A_r) OR ((x << (32 - r))
AND B_r), five operations, with A_r and B_r the masks of its two parts in every lane; since A_r and B_r keep only bits that come
from the low 32 bits of the same lane, PROR gives in the low 32 bits of each lane the rotation of the low 32 bits of that lane,
whatever its guard bits. On packed words an XOR, an OR and an AND with a constant act on each bit, and an addition acts on each
lane separately while no lane reaches 2^36. The addition of a constant is kept pending until the value is read by an XOR, an OR, a
shift, a rotation or a table index, and the one addition that then forms it is charged. All interval bounds depend on the lines
and the constants only, not on the words.

*The shortcut of a passing lane (GPT Sol, answer D9 2; our audit).* A passing lane needs, for the pre-check of 9.7, only bit 18
of Q = Y9, e1, C2.c1 and C2.b1, and the source bank of steps 2 and 3 needs C2.a1 and C2.d1 as well (Section 11). The lines X12 =
ROL(C0.d1, 16) XOR C0.a1, D1.c1 = X11 - X12, D1.b1 = ROR(S6 XOR D1.c1, 12), X6 = ROR(D1.b1 XOR X11, 7), C2.a1 = X2 + X6 + w7,
C2.d1 = ROR(X14 XOR C2.a1, 16), D0.c1 = S10 + D0.d1, X10 = D0.c1 + X15, C2.c1 = X10 + C2.d1 and C2.b1 = ROR(X6 XOR C2.c1, 12) of
step CO read, besides constants, only C0.a1 and D0.d1, which the cache of the batch holds packed (9.8), the packed operands
ROL(C0.d1, 16) and S10, and the names S6, X14 and X2 + w7, which the context holds in three registers. On the machine of Section
11, with a scalar rotation at 4 units: X12, the XOR of the packed words and the shift of lane i out, 2; D1.c1 = (X12 XOR M) +
(X11 + 1), masked, 3, since X11 - x = (2^32 - 1 - x) + X11 + 1 modulo 2^32 and the bits of X12 above its low 32 do not reach
them; D1.b1, 5; X6, 5; C2.a1, 2; C2.d1, 5; X10 = (lane i of D0d1 + S10) + X15, masked, 4; C2.c1, 2; C2.b1, 5; e1 out of lane i of
E[b], 2; and r' = (((Y9' >> (36 i + 16)) XOR e1) AND 4) XOR 3, the word of the pre-check (9.7), 4: 39 units, 36 for lane 0, which
needs three shifts fewer. Every value is the scalar value of step CO for the outer step of the lane: the low 32 bits of each lane
of C0a1 and D0d1 are C0.a1 and D0.d1 (Lemma MB), and every line is evaluated modulo 2^32. The lane uses at most six temporaries.
W and the credit live in registers for the whole run, and the lane neither stores nor reloads them (9.8).

**9.7 The s-pattern pre-check with the guards (G7) and (G15), and the credit of the solver (GPT Sol, answers AW 1, 2 and 5, AX 1,
CF 7 and CD 10; a helper agent of the participant found the pre-check).** Fix a passing outer step, with mask X, and write Q = Y9,
e1 = Y3 + y and, for a trial of it, s = E1.b1 AND beta*. By the lines of step CT read backwards, Y14 = ROL(E3.h1, 16) XOR e1, Y10
= Y14 + C2.c1, Y6 = ROR(Y10 XOR C2.b1, 7) and E1.b1 = ROR(Y6 XOR c1, 12), so for each bit p of beta*

    s[p] = Z[(p + 19) mod 32] XOR c1[(p + 12) mod 32],   Z = (Y14 + C2.c1) XOR C2.b1.

At p = 13, 14 and 15 the bits of c1 are fixed by Q* (c1 AND 0e09818b = 02008000), with the values 1, 0 and 0, and the bits of Z
are 0, 1 and 2. Every joint root h has h[16] = h[17] = 0 and h[18] = 1 XOR Q[18] ((PHASE) and (g) of 9.4), and every member of the
class has e1[0] = e1[1] = 1. So when E3.h1 is a joint root the low three bits of Y14 are 1, 1 and 1 XOR Q[18] XOR e1[2], and the
number nu = s[13] + 2 s[14] + 4 s[15] is a function of the outer step:

    r  = (((Q >> 16) XOR e1) AND 4) XOR 7,
    nu = (((r + C2.c1) XOR C2.b1) XOR 1) AND 7.                          (V)

r is exactly the low three bits of Y14 at a joint root. The identity is used only at joint roots; it says nothing of the other
trials of the outer step.

*The allowed values (GPT Sol, answer AW 1).* For an outcome j of beta*, a pattern s is compatible when E1 can give the differences
beta*, tau_j and eps with that s. With Delta(s) = beta* - 2 s - 8 modulo 2^32, the relation a XOR (a + Delta) = tau has a solution
exactly when d = (tau - Delta) mod 2^32 is even and d / 2 has no bit outside tau, since a XOR tau - a = tau - 2 (a AND tau) modulo
2^32 and tau[31] = 0. GPT Sol enumerated the 2,048 submasks of beta* with this exact criterion for the fourteen outcomes:

| rows | compatible s, rows 175, 185, 275, 285, 385, 675, 685 | allowed nu |
| --- | --- | --- |
| old, tau ending in 20a0 | 16, 32, 8, 16, 32, 8, 16 | 3, 4 |
| new, tau ending in 60a0 | 32, 64, 16, 32, 64, 16, 32 | 2, 3, 4, 5 |

Every compatible s has s[3] = s[4] = 1. In the order (s[13], s[14], s[15]), nu = 3 is 110 and nu = 4 is 001. As a table over the
fourteen outcomes, bit j - 1 for outcome j, VMASK = [0, 0, 3f80, 3fff, 3fff, 3f80, 0, 0] for nu = 0 to 7. Every outcome of S is an
old row, so for this search T = X AND VMASK[nu] is X when nu is 3 or 4 and empty otherwise. A helper agent of the participant
found the same allowed values from the exact E1 counts L_j split by s (the function L_count of the counting program of Section
17): 16, 32, 8, 16, 32, 8 and 16 patterns with a nonzero count on the old rows, each with nu = 3 or nu = 4, half of the count of
the row on each, and every row sum equal to its L_j of 10.1.

**Lemma VP (the pre-check is lossless).** Fix a passing outer step with mask X and let nu be given by (V). Every listed good trial
of the outer step has its outcome in T = X AND VMASK[nu]. So an outer step or an outcome that the pre-check skips holds no listed
good trial, and the count N_o of H1' of every outer step is the same, pointwise, as without the pre-check.

Proof. Let a listed good trial have outcome j in S and E3.h1 = h. By the proof of Lemma F, bit j - 1 is set in both masks, so j is
in X; by Lemma V, h is a joint root of outcome j. By (PHASE) and (g) of 9.4, h[16] = h[17] = 0 and h[18] = 1 XOR Q[18], and e1[0]
= e1[1] = 1 for every member, so by the identity above the bits s[13], s[14] and s[15] of the trial are those of nu. The trial's
E1 gives beta*, tau_j and eps, so its s is compatible with outcome j, and by the enumeration above nu is allowed for j: VMASK[nu]
has bit j - 1. So j is in T. QED. The lemma uses no law of the words. It says which outcomes a passing outer step can hold; it
does not say how often nu takes a value, which enters only the credit (H5_exec).

*Checks (participant computations, not part of the package).* On 30,000,000 real outer steps of the whole class (seed 7, the lines
of step CO of a participant program with the class member), 324,098 real trials with c1 in Q* whose E3.h1 had h[16] = h[17] = 0
and h[18] = 1 XOR Q[18] gave s[13] to s[15] equal to nu by (V) in 324,098 of 324,098. Planted joint roots with y in the class
(seed 11, every root re-tested against the E3 conditions) had h[16] = h[17] = 0 and h[18] = 1 XOR Q[18] in 2,944 of 2,944, with
all fourteen outcomes covered (82 to 477 roots each). These are checks, not proofs; Lemma VP rests on (PHASE), on (g) of 9.4 and
on the exact enumeration.

*The charge (GPT Sol, answers AW 2 and D9; our audit).* On a passing lane, e1, C2.c1 and C2.b1 come from the shortcut of 9.6, and
bit 18 of Q from the cached Y9. Every outcome of S is an old row, so VMASK[nu] AND S is S for nu = 3 and 4 and 0 otherwise, and T
is X or 0 with no table. For u = (Y9' >> (36 i + 16)) XOR e1 the bit 2 is Q[18] XOR e1[2], since the bit 2^34 of Y9' and the lanes
above do not reach it; r' = (u AND 4) XOR 3 is r + 4 modulo 8, with r of (V), and an addition of 4 modulo 8 changes bit 2 only,
which commutes with the XORs; so with w = (r' + C2.c1) XOR C2.b1, nu = (w XOR 5) AND 7, and ((w XOR 5) + 5) AND 6 = 0 exactly when
nu is 3 or 4 (a check over the eight values of w modulo 8). The four operations of r' are in the shortcut; the pre-check is the
addition of C2.c1, the XOR of C2.b1, the XOR with 5, the addition of 5, the AND with 6, the comparison with zero and the branch: 7
units, inside the 53 of the lane (Section 11), paid by every passing lane, also when T is empty; a nonzero result ends the outer
step and a zero one falls through to the preflight. The pre-check never enlarges T, so the cap of 9.4 holds for every T.

*Guard (G7), GPT Sol's answer AX 1, as used in our entry 0bc5f130.* Every compatible s has s[3] = s[4] = 1 (above). At p = 3 and p
= 4 the bits of c1 that Q* fixes are 1 and 0 and the bits of Z are 22 and 23, so s[3] = Z[22] XOR 1 and s[4] = Z[23]: every listed
good trial has Z[22] = 0 and Z[23] = 1. Write C = C2.c1, B = C2.b1, and a22 and a23 for the carries into bits 22 and 23 of Y14 +
C. Bit 22 of Y14 = ROL(h, 16) XOR e1 is x = h[6] XOR e1[22], and bit 23 is h[7] XOR e1[23]. The two required sum bits give

    a22  = x XOR C[22] XOR B[22],
    a23  = maj(x, C[22], a22),
    h[7] = e1[23] XOR 1 XOR C[23] XOR B[23] XOR a23.                     (G7)

**Lemma G7.** Let a listed good trial of an outer step have outcome j and E3.h1 = h. Then h[7] is the value that (G7) gives from
h[6], e1, C2.c1 and C2.b1.

Proof. The trial's E1 gives beta*, tau_j and eps, so its s is compatible with outcome j and s[3] = s[4] = 1 by the enumeration
above; that is, Z[22] = 0 and Z[23] = 1 with Z = (Y14 + C) XOR B. Bit 22 of Y14 + C is x XOR C[22] XOR a22, and it equals Z[22]
XOR B[22] = B[22]; this gives a22. The carry out of bit 22 is a23 = maj(x, C[22], a22). Bit 23 of Y14 + C is h[7] XOR e1[23] XOR
C[23] XOR a23, and it equals Z[23] XOR B[23] = 1 XOR B[23]; this gives h[7]. QED. The unknown carry a22 is fixed by the required
bit 22 and need not be computed from the lower 22 bits; a trial whose true carry differs is not a success, and the E1 test of step
3 would reject it. The lemma uses no law of the words.

*Use in the solver.* h[6] is fixed on every row before the traversal (9.4), so after it the solver computes h[7] by (G7) for each
searched row. On a row on which position 7 is otherwise free, it becomes prescribed with that value; on a row on which h[7] is
already a constant ((g) of 9.4), the row is dropped for this outer step when the two values differ. By Lemma G7 no listed good
trial is lost; joint roots that would fail the E1 test of step 3 may be dropped early, so the solver returns the joint roots of
the outcomes of T that satisfy (G7), and these contain the root of every listed good trial (Lemma CV). Position 7 is then free on
no row (the trees with (G7) of 9.4). h[7] is computed after the row's own patch of h[6] and is never shared across a family.

*The charge of (G7) (GPT Sol, answer AX 1.1).* 128 more units for each searched row: the six source bits e1[22], e1[23], C[22],
C[23], B[22] and B[23], the loads and addresses of the three source words, x, the carry a22, the majority, h[7], the comparison
with an existing constant and its branch, and the insertion of the value into the descriptor of position 7, fewer than 16 blocks
of at most 8 units; the scratch words are released before the 32 descriptors are resident, so the traversal uses no more
registers. (G7) and (G15) load e1, C2.b1 and C2.c1 from the bank of the global ledger, which stores them before any row (Section
11); the caller stores nothing. The extra prescribed bit of the written-out rows is inside the once-only allowance. (G7) adds no
budget and no premise of its own: its work is inside the 1,408 of each row, which the meter debits with A(T) before (G7) runs.

*Guard (G15), GPT Sol's answers CF 7 and CD 10.* Write C = C2.c1, B = C2.b1, V = Y12 and A = (Y1 + w12) mod 2^32, so that Z =
(Y14 + C) XOR B, Y6 = ROR(Z, 7), E1.a1 = Y6 + A, E1.d1 = ROR(E1.a1 XOR V, 16) and c1 = Y11 + E1.d1 (step CT), with Y11 =
7af77f38, whose bit 0 is 0. Let a22 be the carry into bit 22 of Y14 + C, as in (G7), and v16 the carry into bit 16 of Y6 + A, and
put

    a22 = h[6] XOR e1[22] XOR C[22] XOR B[22],
    v16 = V[16] XOR 1 XOR A[16].

For the prefix H of the bits h[0] to h[14] of a node at position 15 (its higher bits zero), with all words of 32 bits:

    L     = (H >> 6) XOR (e1 >> 22),
    zeta  = (((L + (C >> 22) + a22) XOR (B >> 22)) >> 1) AND 1ff,
    p15   = (zeta + ((A >> 16) AND 1ff) + v16) AND 1ff,
    cstar = (Y11 AND 1ff) + (p15 XOR ((V >> 16) AND 1ff)),

    (G15)  cstar AND 08b = 0  and  h[15] = bit 8 of cstar.

**Lemma G15.** Let a listed good trial of an outer step have outcome j and E3.h1 = h. Then h satisfies (G15).

Proof. The trial has Z[22] = 0 and Z[23] = 1 (proof of Lemma G7) and c1 in Q*, so c1[0] = c1[1] = c1[3] = c1[7] = c1[8] = 0 (the
mask 0e09818b and the value 02008000). Bit 22 of Y14 + C is h[6] XOR e1[22] XOR C[22] XOR a22 and equals Z[22] XOR B[22] = B[22],
which gives a22. c1[0] = 0 and Y11[0] = 0 give E1.d1[0] = 0, that is E1.a1[16] = V[16]; Y6[16] = Z[23] = 1; and bit 16 of Y6 + A
is 1 XOR A[16] XOR v16 = V[16], which gives v16. Bits 22 to 31 of Y14 = ROL(h, 16) XOR e1 are h[6] to h[15] XOR e1[22] to e1[31],
which are L when h[15] = 0. Adding C[22..31] with the carry a22 and XORing B[22..31] gives Z[22..31], and the shift drops Z[22]:
zeta is Z[23..31] = Y6[16..24]. Adding A[16..24] with the carry v16 gives E1.a1[16..24], so p15 XOR V[16..24] is E1.d1[0..8], and
adding Y11[0..8] with no carry into bit 0 gives c1[0..8]. So the low nine bits of cstar are c1[0..8] of the trial with h[15] set
to 0. Changing h[15] alone flips Y14[31], hence Z[31], Y6[24], E1.a1[24], E1.d1[8] and c1[8], and no lower bit of these words. As
c1[0] = c1[1] = c1[3] = c1[7] = 0, cstar AND 08b = 0; as c1[8] = 0, h[15] = bit 8 of cstar. QED. The carries a22 and v16 are those
of a listed good trial: a word whose true carries differ is not a success, and step 3 still tests every root in full (Lemma RC).
The lemma uses no law of the words.

*Use in the solver.* For each searched row, after (G7), the solver stores five words in fixed memory: e1 >> 22, (C >> 22) + a22, B
>> 22, ((A >> 16) AND 1ff) + v16 and (V >> 16) AND 1ff; a22 needs h[6], fixed on the row. At each node of position 15 it computes
cstar from the prefix of the node, drops the prefix when cstar AND 08b is not 0, and otherwise prescribes h[15] = bit 8 of cstar
in a temporary copy of the descriptor of position 15, which the forced transition array then reads; the stored descriptor is not
changed, since another prefix may need the other value. Position 15 is then free on no row (the trees with (G15) of 9.4). By Lemma
G15 no listed good trial is lost; the solver returns the joint roots of the outcomes of T that satisfy (G7) and (G15) (Lemma CV).

*The charge of (G15) (GPT Sol, answer CF 7.2).* 128 more units for each searched row, for its five words: the loads and addresses
of their sources, at most 24; the additions, masks, shifts and the two carries, at most 24; five stores with their addresses, 10;
row control and addresses, 16: 74. 64 more units at each node of position 15, besides its 20 as a forced node: five loads with
their addresses, 10; the shift, XOR, addition, XOR, shift and AND of zeta, 6; the addition, AND, XOR and addition of p15 and
cstar, 4; the test of cstar AND 08b and its branch, 3; bit 8 taken out and the temporary key patched, at most 6; copies and
control, at most 16: 45. It uses the ten temporaries of the traversal and spills nothing (Section 11). Its code, the layout of the
five words and the updated CT are inside one more once-only allowance of 2^20 (Section 11).

*The metered credit (GPT Sol, answers CD 10 and 11, CK3 2 to 4 and D13).* For a nonempty subset T of S, with r rows and F families
(9.4; 175020a0 and 275020a0 never occur together and count as two), A(T) = 736 + 2,304 F + 1,408 r is the part of steps 2 and 3
paid once per call and per row, 736 the global ledger of Section 11. For one call, the *ledger* U is A(T) + 20 n_f + 48 n_d + 4
n_20 + 64 n_15 + 80 n_l + 120 n_o, with n_f, n_d, n_20, n_15, n_l and n_o the forced, free, selected and position-15 nodes, leaves
and roots that the call executes, each at its unit cost of Section 11; U = 0 when T is empty. The ledger with the global part of
1,024 of the earlier layout, U0 = U + 288 when T is not empty and 0 otherwise, is the ledger of H5_exec (10.3).

**Lemma FX (one row per family; GPT-6 Astra, Batch 17).** In every call at most one row of each family of T reaches depth 7: the
setup of 9.4 with (G7) drops every other row of the family.

Proof. Restricted to S, a family with two rows of one of the four sets of 9.4 is {185, 385} or {285, 385}; 685 is in the other
high family and each low family has one row. For the high rows 185, 285 and 385, gamma[10] = 0 and the bits of sigma that (a) to
(e) read agree, so (a) to (e) give them the same h[4], h[5] and u[6], and the high-row formula of (f) gives them the same h[6]. At
bit 6 the transition of 9.4 with h[0] to h[6] fixed requires u[6] = Q[6] XOR gamma[7]. For 185 and 385 gamma[7] = 1 for both, and
(g) gives h[7] = 1 XOR h[6] on 185 (gamma[8] = 0) and h[7] = h[6] on 385 (gamma[8] = 1); (G7) gives one value of h[7] from their
common h[6] and the words of the outer step, so it drops one of the two. For 285 and 385 gamma[7] is 0 and 1, and their common
u[6] meets the condition of at most one. QED. The rows of A(T) are still paid for every row of T; only the trees below depth 7 are
excluded.

So, with a tree of 1,920 units for a row with four leaves (20 * 42 + 48 * 3 + 4 * 2 + 64 * 2 + 200 * 4) and 3,808 for a row with
eight (20 * 80 + 48 * 7 + 4 * 4 + 64 * 4 + 200 * 8), U <= CM(T) = A(T) plus, for each family of T, the largest tree of its rows,
in every call: since every executed count is at most the static one of the surviving row and roots are at most leaves. CM(T) = 0
when T is empty. The table CT holds, for each of the 128 values of the seven-bit mask T, the word CM(T) OR (A(T) << 16), both
fields below 2^16; it is built once, inside the once-only allowance of Section 11. In the same way U0 <= CM(T) + 288 <= 15,584.

**Lemma CP (the cap transfer; GPT Sol, answer D13).** In every outer step, U <= (478/487) U0.

Proof. If T is empty, U = U0 = 0. Otherwise U = U0 - 288 and U0 <= 15,584 (above), so 288 = (9/487) 15,584 >= (9/487) U0 and U =
U0 - 288 <= (478/487) U0. QED. The inequality holds pointwise, before any mean is taken, and uses no law of the words and no rate
of calls.

The remaining credit lives in the 64th register for the whole run: no code of the walk names it (9.8), the traversal uses 63
(Section 11), the credit register is in no saved parent, and the helpers of the leaf, the root and (G15) use only their ten
temporaries. *Preflight:* when T is not zero the lane forms the address of CT[T] and loads it (2), takes out A(T) (1), which one
subtraction in the global ledger debits (Section 11), takes out CM(T) (1), and compares it with the credit register and branches
to the halt when CM(T) exceeds the credit (2): 6 units, inside the 53 of the lane. *Meter (our audit):* every forced, free and
root block that the call executes subtracts from the credit register its unit cost in one operation with an immediate operand, the
4 of a selected node and the 64 of a node at position 15 added to the immediate of their forced block, and a forced block at
position 31 subtracts, in a second operation, the 80 of the leaf below it when its arc is valid. Every leaf is the child of a node
at position 31, and position 31 is forced on every row of S (the trees of 9.4). Each such operation lies inside the unit cost of
its block, whose itemized work leaves room for it (Section 11: a forced block does at most 18 units of work of its 20, 13 at
position 31, a free block 36 of its 48, a root 113 of its 120); a free block pays for its own two-child control, not for its
children; and a leaf block spends its 80 on its work and subtracts nothing. The call therefore debits

    V = A(T) + 20 n_f + 48 n_d + 4 n_20 + 64 n_15 + 80 n_l + 120 n_o = U.

**Lemma ME (the meter).** In every call, whatever its words: (a) V = U <= CM(T) <= 15,296; (b) if the credit before the call is at
least CM(T), the credit stays nonnegative throughout the call.

Proof. (a) V = U by the display: every block that the call executes is debited exactly its unit cost, once, by itself or, for a
leaf, by its parent at position 31. U <= CM(T) by Lemma FX and the counts above; the largest CM(T) over the T that occur is
15,296, for 185, 385 and 685 (Section 11). (b) The debits of the call are subtractions of positive amounts that add up to V <=
CM(T). QED. The lemma uses no law of the words.

An outer step whose CM(T) exceeds the remaining credit halts the run with failure before steps 2 and 3; the failed test is part of
the preflight of its lane (Section 11). The credit is a halt like the work register of 9.1, so the time bound depends on no mean:
the debits of the run add up to at most CREDIT. Whether the credit suffices is the premise H5_exec (10.3), which bears on the
success probability alone. The preflight reserve of 15,296 in CREDIT is needed because the preflight tests the whole metered cap:
on the event that the unhalted sum of the debits is at most m_C + t (10.3), the credit left before every call is at least 15,296
>= CM(T), so no preflight fails and the meter loses no trial (GPT Sol, answer CK3 4).

**9.8 The member loop, the direct tables and the omega-first batch.** This subsection defines the walk of step 1 of 9.1. The
member loop and the direct tables are those of entry e9b6649e of the participant hecmas, described here in our own words and
checked by a separate reimplementation of the participant; the omega-first order of the batch is GPT Sol's answer CA, whose
partition, listings, registers and charge the participant derived from the printed lines of step CO and checked by programs
(below); the fused line of the Y9 path, the allowance of a context and the layout of a passing lane are GPT Sol's audit of that
charge, answer CD (sections 1 and 3), and the E count held in a register, with the frame of a passing lane, is its answer CD
(sections 6 and 8.1). The walk uses the packed words, lanes, guard bits and masked rotation PROR of 6.5 and 9.6 and the machine of
Section 11. The layout of this row, with the work register W, T2' and T1 at fixed word addresses, the frame in registers and the
written-out code, is our audit; keeping the frame words in registers follows entry 73d5265f of the participant 0xshikhar.

*Contexts.* The seven outer words C0.d1, D2.a1, D2.b1, S11, S4, X9 and w6 of step CO together are called a *context*. Fixing a
context and a member y of the class fixes an outer step, whose trials are its 2^21 values of c1 in Q* (Section 8). The member loop
changes only the order and the grouping in which outer steps are visited; each outer step, with its filter, pre-check, guards (G7)
and (G15), solver and certificate, is that of Sections 8 and 9.

**Lemma Y (the lines that read the member).** Call a line of step CO *needed* when Y9 or w8 depends on it, directly or through
other lines; 64 of the 77 lines are needed. Call a needed line *member-dependent* when one of its operands is y = Y4 or a
member-dependent line. Exactly 25 needed lines are member-dependent; in the order in which step CO prints them, numbered here,
they are

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

depend on the seven outer words and on constants only. Besides these, omega = Y3 + y + w8 depends on the member.

*Proof.* Both statements are finite checks on the printed text of step CO. Walking the lines in printed order and marking a line
when an operand is y or a marked line gives the first list; Y8 is the first line marked. Each line of the second list has as
operands only outer words, constants (IV, the six constants of 3.2 and the four constant values of K2) and earlier unmarked lines.
Collecting the lines on which Y9 and w8 depend gives the 64. QED. A participant program that parsed step CO from its printed lines
and computed both sets reproduces the two lists in this order; it checks the lists and is not part of the proof (Section 13).

Hence, within one context, the 39 context lines can run once; per member, only the 25 member-dependent lines and omega remain.

**Lemma CX (contexts and the class).** Let a run draw its contexts as in step 1 of 9.1. (a) Different contexts read different
fresh words, so the contexts are independent, and within a context the seven outer words are independent and uniform. (b) The
member lists of 9.9 hold every member of the class in exactly one lane, so a context walks every member once, except the members
of the clusters that its gate skips and the partners that its descriptor table leaves out, whose outer steps have a zero mask of
(2) (Lemmas CL and XF). (c) For any function g of an outer step with a finite mean, let G be its sum over the 2^19 outer steps of
one context. Then E[G] = 2^19 E[g(U)], with U an outer step whose seven outer words are uniform and whose member is uniform on the
class and independent of them: the outer step that step 1 of entry 415e792c draws. The values of G for the contexts of a run are
independent and identically distributed. (d) If 0 <= g <= c on every outer step, then 0 <= G <= 2^19 c.

*Proof.* (a) holds by the construction of step 1. (b) The representative lists hold the 16,384 representatives once each and the
partner lists the 31 partners of every cluster once each (9.9); the clusters partition the class. (c) G is the sum over all
members y of g at the outer step (context, y). For each fixed y the outer words of the context are uniform and do not depend on y,
so the mean of that term is E[g(W, y)] with W uniform; summing over the 2^19 values of y gives 2^19 E[g(U)]. G is a function of
the fresh word of its context only, so (a) gives the independence and the equal laws. (d) is immediate. QED. By Lemmas CL and XF,
each quantity whose totals 10.3 and 10.4 use, the indicators of the E count and of the pass count, the ledger U and N_o, is zero
on the outer steps that the gate and the descriptor table skip (Lemma XF), so its total over the outer steps that a context walks
is its G.

What the member loop does to the law of the run is therefore limited to dependence. The means that the heuristics use, the rate of
H1', the shares of H4' and the mean of H5_exec, are those of a uniform outer step, exactly as in entry 415e792c; but the 2^19
outer steps that share a context also share its seven words, so independence holds between contexts and not between outer steps.
10.3 states the dependence part of H1' for contexts, states H_G_cluster for contexts, and proves the tails of H4', H5_exec and
H_G_cluster over contexts.

**Lemma DT (the direct tables).** The tables T2 and T1 have one entry for each 32-bit word x: T2[x] = (mask of (2) on x) AND 5f
and T1[x] = (mask of (1) on x) AND 5f. They are stored as T2' at word address 0, with 3 * 2^32 entries T2'[x] = T2[x mod 2^32],
and T1 at word address 2^34, so that a lane's index, or 2^34 plus it, is the address of its entry. A lane therefore reads, with
one load each, the same masks restricted to S that the two automata of Section 8 give.

*Proof.* Step 0 of 9.1 computes each entry by running the corresponding automaton of Section 8, with its last table ANDed with S,
on x, one byte table per byte. QED. Cost of the build: for each of the 2^32 words and each of the two tables, the four bytes of
the word are separated (a shift and an AND each), the state is advanced with four table loads and three additions, the mask is
ANDed with S and stored at its address, and the loop advances; fewer than 32 units, so fewer than 2^32 * 2 * 32 = 2^38 units in
all, and Section 11 charges 2^38; the two further copies of T2 in T2', 2^33 entries at a load, a store, their addresses and the
loop, below 8 units each, are charged 2^36. T2' and T1 have 2^34 entries, 2^39 bytes as words of 256 bits (Section 12). Since
every entry is the automaton's mask, the share of passing pairs read through the tables is SHARE / 2^64, as in Section 8.

*The member lists.* Step 0 of 9.1 writes the member lists of 9.9 as pairs of adjacent words (U[b], E[b]) (GPT Sol, answer CJ 3).
In U[b], lane i is ROL(y, 7) for the member y of the lane, the word that the line Y8 reads, and in E[b] it is e1 = Y3 + y, the
word that omega needs; the unused lanes of a last word hold copies of its last member and are never tested.

*The words of a context.* Once the 39 context lines have run on scalar words, a context prepares the sixteen operands that the
member-dependent lines take from it, C0.b1, -C0.c1, C0.d1, -C0.b1 - w6, ROL(C0.d1, 16), K = X11 + 1 - S11, S12, K' = -C0.b1 - w6
- X4 - w2, -S1 - S6, S15' = S15 XOR ROR(X15, 8), S10, S5, w3, X13, X9 and -S0 - S5 (subtractions modulo 2^32), and copies each
  into all seven lanes. These sixteen packed words occupy sixteen registers while the batches of the context run. Every other
  operand of those lines is fixed for the whole search: ROL(X15, 8), X15, the lane mask M (the low 32 bits of every lane) and the
  masks of PROR are written into the instructions. The context also loads S6, X14 and X2 + w7, which the shortcut of a passing
  lane reads (9.6), into three registers, forms S2 = ROL(S14, 8) XOR K2D, w5 = S2 - K2A - K2B and w12 = D2.a1 - S2 - S7 and stores
  them with the names that steps 2 and 3 reload (GPT Sol, answer D13), and its packed copy of X9 is X9' = X9 + 2^34 in every lane,
  which only the Y9 path reads (below).

*The omega-first batch.* The 25 member lines split in two. The 8 lines Y8, Y12, Y0, C0.a1, X0, D0.d1, D0.a1 and w8, with omega,
are those that omega needs: the *omega side*. The other 17, D0.c1, D0.b1, X10, X5, X12, D1.c1, D1.d1, X1, C1.a1, C1.d1, D1.a1,
C1.c1, w10, C1.b1, Y1, Y13 and Y9, are needed by Y9 alone: the *Y9 path*. Every member line is in exactly one of the two, and the
Y9 path reads of the omega side only C0.a1 (in X12) and D0.d1 (in D0.c1). On packed words the omega side is folded (F1, GPT Sol,
answer D9 1): X0 = C0.a1 - X4 - w2 = Y0 + K' and, since D0.d1 = X0 XOR ROL(X15, 8), ROR(D0.d1, 16) = ROR(X0, 16) XOR ROR(X15, 8),
so D0.a1 = ROR(X0, 16) XOR S15'; C0.a1 and D0.d1 are not formed, and omega = e1 + D0.a1 + (-S0 - S5) is summed as D0.a1 + (e1 +
(-S0 - S5)), the same integer in every lane. For batch b of a context, on packed words, with the units of each line (one for each
operation and load, five for PROR, where PROR(x, r) rotates the low 32 bits of every lane right by r):

    U    = load [p]                        1   (p: an immediate address)
    Y8   = U XOR C0.b1                     1
    Y12  = Y8 + (-C0.c1)                   1
    Y0   = PROR(Y12, 24) XOR C0.d1         6
    X0   = Y0 + K'                         1
    D0a1 = PROR(X0, 16) XOR S15'           6
    E    = load [p + 1]                    1   (and p + 1, 1)
    cg   = E + (-S0 - S5)                  1
    om   = D0a1 + cg                       1   (omega = Y3 + y + w8)

The six lines and omega cost 17 units; the pair costs 3, two loads and p + 1, which the opening of a cluster pays for its old
partner batches (9.9). Next come seven *lane tests*, for i = 0 to 6. Lane i shifts om right by 36 i (lane 0 needs no shift) and,
except lane 6, keeps the low 36 bits with an AND; the result, the lane's omega with its guard bits, is below 3 * 2^32 (Lemma MB)
and is the word address of the entry of T2' at that omega, so the lane loads the mask of (2) with no base, compares it with zero
and branches: 5 units per lane, 4 for lanes 0 and 6, 33 in all. Lane 6 needs no AND, since bits 252 to 255 of om are zero (Lemma
MB). A partner batch of seven lanes therefore executes *50 units*, its omega side and its lane tests, a batch of n < 7 lanes 17 +
4 + 5 (n - 1), and the fifth old partner batch of a cluster, with three lanes, 17 + 14 = 31 (our audit). X0, Y0, Y12 and om stay
in registers through the lane tests.

A lane whose mask of (2) is not zero is an *E lane* and runs its E handler right after its lane test. The handler adds u_E = 7 to
W, one addition with an immediate. *The fill (GPT Sol, answer CM 5A).* At the first E lane of a batch the handler adds u_E + u_G =
7 + 56 in that one addition instead (our audit), rebuilds C0a1 = Y0 + (-C0.b1 - w6) and D0d1 = X0 XOR ROL(X15, 8), 2 units (GPT
Sol, answer D9 1), builds the Y9 path on packed words for all seven lanes at once from them and the words of the context, and
keeps the result, with C0a1, D0d1 and the packed Y1, in registers: the batch's *cached Y9*. The second column gives the units of a
line of the Y9 path and the third their running sum:

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

Step CO forms D1.c1 = X11 - X12 and then D1.d1 = D1.c1 - S11; D1.c1 has no other use among the 25 lines of Lemma Y (D1.b1, which
also reads it, is not needed), so the line D1d1 forms D1.d1 at once from K = (X11 + 1 - S11) mod 2^32, which the context
prepares in place of -S11 (GPT Sol, answer CD 1). The 17 lines of the Y9 path, D1.c1 and D1.d1 in one line, cost 54 units and
the two rebuilt words 2, so a fill costs *56 units*. With X9' = X9 + 2^34 of the context in place of X9, the line C1c1 gives
C1.c1 + 2^34 in every lane and the line Y9 gives Y9 + 2^34; C1.c1 is read only by Y9 and by the PROR of C1b1, which drops the
guard bits, so no other value changes (Lemma MB). Every E lane, the first included, then isolates its lane i of the cached Y9
with a shift and an AND with 2^34 + M (2), which gives the word address 2^34 + Y9 of the entry of T1 at its Y9, loads that entry
(1), and ANDs the mask of (1) found there with the mask of (2), compares with zero and branches (3). An E lane therefore costs
*7 units*: 1 + 2 + 1 + 3, 6 for lane 0, and its batch's fill 56 more once. The fill computes the same packed values that a Y9
path built at any later lane of the batch would compute: they depend only on X0, Y0 and the words of the context, which no lane
test, E handler or passing lane changes.

*The code of a batch (our audit).* It is written out lane by lane as a *not-ready chain*, run until the batch's first E lane,
whose E handlers contain the fill, and, after the E handler of each lane i of that chain, a *ready tail* for the lanes i + 1 to 6,
whose E handlers read the cached Y9 only; a passing lane is written inline after each E handler. In the chain and in every tail,
the lane test of lane i branches past its E handler when its mask of (2) is zero and otherwise falls through into it; an E handler
falls through into its passing lane when X is not zero and otherwise branches to the lane test of the next lane; a passing lane
falls through, or returns from steps 2 and 3, to the lane test of the next lane; and a not-ready E handler with its passing lane
continues in the ready tail that follows it. The exits of the last lane are the branches of its lane test, its E handler and its
pre-check and the return of steps 2 and 3, all aimed at the code that follows the batch. So whether the cache is ready is a
position in the code, held by no flag and tested by no instruction, and every transfer is a fall-through or a branch that is
charged in its lane (Section 11). The fifth old partner batch of a cluster has three used lanes, the last representative batch
four and a chunk the n lanes of its dispatch leaf (9.9), and their code has those lanes only. The written-out code is paid in the
once-only allowances of Section 11.

*Registers (our audit; the frame in registers after entry 73d5265f; GPT Sol, answer D14 3).* The tables T2', T1 and the gate
table are read at their word addresses, and the list addresses are immediate operands, written into the instructions with the
code (GPT Sol, answers CD 3 and D13). Live through a partner batch or chunk: at most 18 words of the context (its sixteen packed
operands, X9' among them, the gate base BG6 of 9.9 and the context count), the three registers S6, X14 and X2 + w7, 11 of the
representative batch (its key, E[b], om, Y0, X0, its list address, its cached Y9 with C0a1, D0d1 and Y1, and Y12), 11 of the
partner batch (its address, E[b], om, C0a1, D0d1, its cached Y9, Y1, Y12, the mask of the current lane and two temporaries of the
lane tests; a partner's Y0 and X0 give way to its C0a1 and D0d1), W and the credit: 45; and nine words of the masked walk of 9.9,
IX, the representative's U, A[8..15] and six reusable words (the carries, the broadcast U and E, the descriptor address, JU, JE
and the metadata): 54 of the 64 registers. A fill adds at most six packed values of the Y9 path live at once (a liveness count on
the listing above) and the two temporaries of PROR, 62; a passing lane adds at most six temporaries of the shortcut and its mask
X, 61. So nothing is spilled; the frame of the representative batch stays in its registers through the partner batches, the
counts of 9.1 are the one register W, and no code of the walk names the credit register.

**Lemma MB (the packed batch is exact).** Take any used lane i of any batch, and let (context, y) be its outer step. (a) The low
32 bits of lane i of om equal omega = Y3 + y + w8 as step CO computes it for that outer step, and the lane test reads T2' at that
value plus 2^32 times its guard bits, which is T2 at omega. (b) If the lane is an E lane, the low 32 bits of lane i of the cached
Y9 of its batch equal the Y9 of step CO for the same outer step, bit 34 of the lane is 1 and bit 35 is 0, and the E handler reads
T1 at that Y9. (c) The lane is taken as passing exactly when its outer step passes the filter of Section 8. (d) No lane of any
packed value reaches 2^36, so bits 252 to 255 of every packed word are zero; om is below 3 * 2^32 in every lane.

*Proof.* The two listings contain the member-dependent lines of Lemma Y and omega, D1.c1 and D1.d1 in one line, C0.a1, X0, D0.d1
and D0.a1 of the omega side by the identities of F1 above and C0a1 and D0d1 rebuilt by the fill, each written with packed
operands: a word of the context appears as the packed word that repeats its scalar value in every lane, subtracting such a word
is adding its negation modulo 2^32, and the one subtraction of a member-dependent value, in D1.d1 = (X11 - X12) - S11, is written
(X12 XOR M) + K with K = (X11 + 1 - S11) mod 2^32; X12 XOR M flips the low 32 bits of each lane and keeps its guard bits, and
(2^32 - 1 - x) + X11 + 1 - S11 = X11 - x - S11 modulo 2^32, so the low 32 bits of the result are the D1.d1 of step CO. An XOR
acts on each bit; an addition acts on each lane separately while no lane reaches 2^36, and then the low 32 bits of a lane are the
sum modulo 2^32; PROR gives in the low 32 bits of each lane the rotation of the low 32 bits of that lane, whatever its guard bits
(9.6). Lane i of U[b] and of E[b] holds ROL(y, 7) and Y3 + y for the member of the lane. By induction over the printed order the
low 32 bits of each lane of each line are its scalar value. The Y9 path reads the values C0a1 and D0d1 of the omega side of the
same batch, which the lane tests, the E handlers and the passing lanes do not change, so the order of the two parts changes no
value, and the cached Y9 read by a later E lane of the batch is the value that a Y9 path built at that lane would give. The
cached Y9 is the batch's own: it is filled only at the batch's first E lane, read only by E lanes of the same batch, kept across
the steps 2 and 3 of a passing lane in the saved words of the batch and across the partner batches of an opened cluster in the
frame of 9.9, and a new batch starts in the not-ready copy. The lane test and the E handler take the low 32 bits of lane i, and
Lemma DT gives the masks. When the mask of (2) is zero the AND of the two masks is zero whatever the mask of (1), so leaving out
the Y9 path and the mask of (1) in such a lane changes no decision; in any other lane the decision is that AND, as in Section 8.
*Bounds.* Every loaded word and every word of the context is below 2^32 in every lane, and so is the output of PROR. Carry an
exclusive upper bound through the lines: an addition of values below A and B is below A + B - 1, and an XOR of values below A and
B is below the least power of two that is at least the larger of A and B. These bounds are functions of the lines alone, not of
the words. Among the sums, Y1 has the largest bound, below 9 * 2^32 < 2^35.17; among the XORs, the input of the PROR of Y13 has
the largest, at most 2^36; om = D0a1 + cg and Y9 stay below 3 * 2^32. The chunks of 9.9 form their U and E as the broadcast words
of the representative plus offsets 2^17 j and 2^10 j with j < 32 in each lane, which are the U and E of the partners: ROL(y_j, 7)
= ROL(y_0, 7) + 2^17 j and e_j = e_0 + 2^10 j with no carry out of bit 22 or 14 (Lemma XF), all below 2^32. With X9' < 2^34 +
2^32 in place of X9, C1c1 stays below 2^34 + 2^33, the input of the PROR of C1b1 below 2^35, and Y9 below 2^34 + 3 * 2^32 = 7 *
2^32 with its bit 34 set and bit 35 clear, since Y9 - 2^34 is the value of the original line, below 3 * 2^32 < 2^34. So no lane
reaches 2^36, and no AND with M is needed before a sum. QED. The bounds are those of the member loop of entry e9b6649e, whose
lines are the same; the participant recomputed them for this order and for the fused line, whose bound, 3 * 2^32 - 1, is below
the 4 * 2^32 - 2 of the two lines it replaces, and a participant simulation of the order with the two lines apart asserted every
value of every operation below 2^36 (below).

*A context.* Drawing the fresh word, the 39 context lines on scalar words, forming and copying the sixteen packed operands,
storing the names for steps 2 and 3, the gate base of 9.9, X9', X2 + w7, the three registers of the shortcut, S2, w5 and w12 and
the test of W come to at most 541 units, charged 547; with the four flags of the gate (160), the descriptor table of 9.9, the
carry word of every representative batch and the fallback premiums, itemized in Section 11, a context is charged 112,519 (GPT Sol,
answers CD 1, CI 1.5, D13, D14 and D16; our audit).

*A passing lane.* A lane that passes adds u_P = 53 to W, one addition; computes e1, C2.a1, C2.d1, C2.c1, C2.b1 and the word r' of
the pre-check by the shortcut of 9.6 (39); runs the pre-check of 9.7 (7); and, when T is not zero, runs the preflight of 9.7 (6)
and, when the credit covers CM(T), calls steps 2 and 3 under the meter, which may use all 64 registers: the global ledger saves
the live words of the batch, W among them, at its entry and reloads them before its return (Section 11). The lane is written
inline after its E handler, so it keeps no return link and makes no jump of its own; the credit stays in its register and is never
restored from a copy. Section 11 itemizes the lane at 53 units, 1 + 39 + 7 + 6 (GPT Sol, answers CD 3, CI 1.5, CK3 2, CM 5A and
D9; our audit).

*The participant checks.* Three participant programs, not part of the package. (1) A reimplementation of the member loop of entry
e9b6649e (research/impl/memberloop) found the two lists of Lemma Y from the printed lines and, on 100,000 random pairs of a
context and a member, compared Y9, omega, both masks, the pass decision and all 25 member-dependent lines with the full step CO: 0
differences. (2) A Python program (research/frontline/ca) ran 142,858 batches of seven consecutive members in 1,429 contexts on
scalar words and as a packed simulation with seven 36-bit lanes that executes and counts every operation, load and PROR and
asserts every lane value below 2^36, against the full member loop: 0 different pass decisions, 0 different masks of (2) or Y9 in
the 54,067 lanes with a nonzero mask of (2); the simulation executed 67 units in every batch, with the two list words loaded apart
(the pair saves one address), and 78 in every Q path, the Q path of answer CA, with 16 for the E count and D1.c1 and D1.d1 apart;
the largest lane value was 2^35.02. (3) A graphics-card version (RTX 3090) walked 120,000 contexts (62,914,560,000 outer steps),
every member, with the omega-first batch and the full member loop on every outer step: 0 different pass decisions, masks of (2) or
values of Y9 in the 3,418,392,488 lanes with a nonzero mask of (2), and 62,294,500 passes. Lanes with a nonzero mask of (2) were
0.054334 of the outer steps, against the exact share 0.054416 and the share 0.054418 that E_BUDGET allows.

**9.9 The cluster gate and the masked partner walk (GPT Sol, answers CI 1, CJ 1 to 5, D12, D14, D16 and D18; the layout, our
audit).** This subsection fixes the order in which a context walks its members, lets it skip, with one table read, a group of 32
members that is proved to fail test (2), and, in a group that it opens, skips the members that a table of the context proves to
fail it. Every outer step that is walked is that of 9.8, with the same batch, lane test, E handler and passing lane.

*Clusters.* Write e = Y3 + y for the word e1 of a member y. The class fixes the 13 bits of e in 03cf8303 and leaves the other 19
free (Lemma Q); bits 10 to 14 are free and bit 15 is fixed at 0. Let g run over the 2^14 settings of the 14 free bits other than
10 to 14, and let e_g have these bits and bits 10 to 14 zero. The *cluster* of g is the 32 members with e = e_g + j * 2^10, 0 <= j
< 32; its *representative* is the member with j = 0, and the other 31 are its *partners*. The 16,384 clusters partition the class.

In one context put b = C0.b1, c = C0.c1, d = C0.d1, A = C0.b1 + w6 + X4 + w2, L = ROL(X15, 24) XOR S15 and C = e - S0 - S5, all
modulo 2^32. With r = ROL(y, 7) XOR b, v = r - c (the line Y12), p = ROL(v, 8) XOR d (the line Y0) and x = p - A (the line X0),
the omega side of 9.8 gives

    omega = (ROL(x, 16) XOR L) + C,

since D0.a1 = ROL(X0 XOR ROL(X15, 8), 16) XOR S15 and omega = e + D0.a1 - S0 - S5. The term ROL(X15, 24) of L is part of the
identity.

**Lemma KP (two prefixes per cluster).** Fix a context and a cluster. Let p_0 be the p of its representative, u = (((p_0 >> 16)
AND 1ff) - ((A >> 16) AND 1ff)) mod 512, and W_l = (C + (((u - l) mod 512) XOR (L AND 1ff))) mod 512 for l = 0 and 1. Then every
member of the cluster has omega mod 512 in {W_0, W_1}.

*Proof.* The members of a cluster differ only in bits 10 to 14 of e, so C mod 512 is the same for all of them. Bit 15 of e is 0,
so e mod 2^16 < 32,768, while Y3 mod 2^16 = c181 = 49,537: the subtraction y = e - Y3 borrows into bit 16 in every member, and
bits 16 to 31 of y, like bits 0 to 9, are the same for all members; only bits 10 to 15 differ. Then r differs only in bits 17 to
22, so bits 0 to 16 of v = r - c are the same for all members, and its bits 24 to 31 take at most two values, which differ by
the borrow into bit 24. Hence bits 8 to 24 of p = ROL(v, 8) XOR d are the same for all members and only its low byte varies.
Bits 16 to 24 of x = p - A are ((p >> 16) AND 1ff) - ((A >> 16) AND 1ff) - l modulo 512, where l in {0, 1} is the borrow of (p
mod 2^16) - (A mod 2^16) into bit 16; the first term is that of the representative, so these bits are (u - l) mod 512. Bits 0 to
8 of ROL(x, 16) are bits 16 to 24 of x, and bits 0 to 8 of a sum depend only on bits 0 to 8 of its terms, so omega mod 512 =
W_l. QED. The two values may be equal, and one of them may not occur: the lemma is a cover, not a rate.

**Lemma A9 (dead residues of test (2)).** Let S7 be the 52 residues 25 to 3e and 45 to 5e (hexadecimal) modulo 128. If omega mod
128 is not in S7, then (2)_j fails for omega for every j in S, and T2[omega] = 0.

*Proof.* A word f with (omega + f) XOR ((omega + DY3) + (f XOR sigma_j)) = eps (Section 8) satisfies the equation modulo 2^9,
whose bits depend only on omega and f modulo 2^9. For the six outcomes of S, sigma_j mod 2^9 = f0 (the low twelve bits of every
tau_j are 0a0), DY3 mod 2^9 = fd and eps mod 2^9 = 55. The finite check

    [r for r in range(512)
     if any((((r + f) ^ (r + 0xfd + (f ^ 0xf0))) & 511) == 0x55 for f in range(512))]

lists the residues r of omega modulo 2^9 for which the equation modulo 2^9 has a solution: 208 residues, exactly those whose value
modulo 128 lies in S7. For any other omega no j in S satisfies (2)_j, and by Lemma DT the mask of (2), restricted to S, is zero.
QED.

*The straddle gate (GPT Sol, answers D14 and D16).* Write w[k..l] for bits k to l of a word w as a number. For i = 0 to 3 let T_i
= f2, fa, 02 and 0a (hexadecimal), that is (8 i - 14) mod 256, and put

    H_i = ((T_i XOR b[24..31]) - c[24..31]) mod 256,   lo0_i = H_i XOR d[0..7],   lo1_i = ((H_i - 1) mod 256) XOR d[0..7],
    hbad_i = [min(lo0_i, lo1_i) < A[0..7] <= max(lo0_i, lo1_i)],   Hbad = hbad_0 + 2 hbad_1 + 4 hbad_2 + 8 hbad_3.

These depend on the context alone. The cluster of a representative with word e and line Y0 = p *straddles* when p[8..15] =
A[8..15] and hbad_i = 1 for i = e[20..21]. The *gate table* holds, at word address 2^35 + w + 2^8 m + 2^16 h + 2^20 i + 2^22 a,
for 0 <= w < 128, 0 <= m, a < 256, 0 <= h < 16 and 0 <= i < 4, the entry 1 when w lies in S7 or when m = a and bit i of h is 1,
and 0 otherwise; bit 7 of the index is not used, and both of its values hold the same entry. These are 2^30 entries of one word at
word addresses 2^35 to 2^35 + 2^30 - 1, built once (Section 11), inside the band 2^35 to 2^36 - 1, which holds no other table,
code or descriptor. A representative reads it at w = omega mod 128, m = p[8..15], h = Hbad, i = e[20..21] and a = A[8..15], so its
entry is 1 exactly when its omega mod 128 lies in S7 or its cluster straddles.

**Lemma CL (the gate is lossless).** Fix a context and a cluster. If the cluster does not straddle, every member has the omega mod
512 of the representative. If the gate entry of the representative is 0, then every member of the cluster has T2[omega] = 0; none
of its outer steps runs a Q path or passes the filter, and none holds a listed good trial.

*Proof.* Member j has e = e_0 + 2^10 j. Since e mod 2^10 >= 303 > 181 = Y3 mod 2^10 (hexadecimal) and e[10..15] = j < 48 =
Y3[10..15], y = e - Y3 has y[10..15] = 16 + j. Bits 15 and 16 of e are 0, so e[0..16] < 2^15 and y[0..16] = e[0..16] + 2^17 -
1c181 < 2^16: y[16] = 0, and the subtraction borrows into bit 17. With e[17..24] = 134 + 8 i (the class fixes e[17..19], e[22..24]
and leaves e[20..21] = i) and Y3[17..24] = 147, y[17..24] = (134 + 8 i - 147 - 1) mod 256 = T_i for every member. So r = ROL(y, 7)
XOR b has r[24..31] = T_i XOR b[24..31], the same for all members, and the high byte of v = r - c is H_i or (H_i - 1) mod 256, by
the borrow out of its low 24 bits; p = ROL(v, 8) XOR d has p[8..24] common to the cluster (Lemma KP) and the low byte lo0_i or
lo1_i. The borrow of x = p - A into bit 16 is [p mod 2^16 < A mod 2^16]: when p[8..15] differs from A[8..15] it does not depend on
the low byte, and when they are equal it differs between the low bytes lo0_i and lo1_i exactly when hbad_i = 1. So when the
cluster does not straddle, every member has the borrow of the representative, x[16..24] is common, and by omega = (ROL(x, 16) XOR
L) + C, with C mod 2^10 common, omega mod 512 is the representative's. When the entry is 0 the cluster does not straddle and the
representative's omega mod 128 is not in S7, so no member's is, and Lemma A9 gives T2[omega] = 0. A lane with a zero mask of (2)
is no E lane and does not pass (Lemma MB (c)), and by Lemma F an outer step that does not pass holds no listed good trial. QED.
The lemma uses no law of the words. The participant's arithmetic program checks y[10..24] and the borrow into bit 17 on all 2^19
members, and on 20,000 random clusters, half of them with A[8..15] = p[8..15], the straddle rule against the borrows of the two
low bytes, the common omega mod 512 and the gate against the word equations of every member; the declared program compares the
entry of every representative it walks with S7 and the two exact prefixes of Lemma KP (9.2).

Hence skipping a cluster whose gate entry is 0 loses nothing: the E count, the pass count, the work of passing lanes and of steps
2 and 3, the debits of the credit and the number N_o of 10.3 are zero on every outer step that the gate skips, so their totals
over the outer steps that a context walks equal their totals over all 2^19 outer steps of the context, outer step by outer step.
In the same way the fills of a context in the walk with the five partner batches of every opened cluster, before any halt, are
exactly those of its 84,261 batches (its representative batches and the five partner batches of each cluster) that hold a member
with a nonzero mask of (2): a skipped cluster holds none, so its partner batches and its representative's lane would not be
filled. This count, G(C), is a function of the context alone; Lemma XF (d) bounds the fills of the masked walk below by it.

*The carries of a cluster.* Fix a context and a cluster, with members e_j = e_0 + 2^10 j and y_j, j = 0 the representative. For a
member let c17, c25, c9a and c9b be the carries into bit 17 of Y8 + (-C0.c1), into bit 25 of Y0 + K', into bit 9 of D0.a1 + (-S0 -
S5) and into bit 9 of e1 + w8, and IX = c17 + 2 c25 + 4 c9a + 8 c9b. The *byte guard* of the cluster fires when bits 8 to 15 of
the representative's Y0 equal those of A = -K'. With five-bit windows, all modulo 32, put

    o(IX, j) = (((((((16 + j) XOR (C0.b1 >> 17)) + ((-C0.c1) >> 17) + c17) XOR (C0.d1 >> 25)) + (K' >> 25) + c25)
               XOR (S15' >> 9)) + ((-S0 - S5) >> 9) + c9a) + 1 + 2 (j mod 16) + c9b,

and let alive16(w), for w < 2^16, be 1 when w mod 128 is in S7 and bit (w >> 9) mod 32 of LW[(w >> 8) mod 2] is 1, with LW =
(e000001f, f000001f), whose words have 8 and 9 bits set.

**Lemma XF (the masked partner walk).** Fix a context and a cluster whose byte guard does not fire, and let W and b8 be omega mod
512 and its bit 8 for the representative. (a) Every member has the same IX and the same omega mod 512, and bits 9 to 13 of the
omega of member j are o(IX, j); for each IX, j -> o(IX, j) is a bijection of the 32 values of j. (b) If T2[omega] is not 0, then
alive16(omega mod 2^16) = 1. (c) So the partners j with T2[omega_j] not 0 are among the *survivors*, the j from 1 to 31 with W mod
128 in S7 and bit o(IX, j) of LW[b8] set, and there are at most 9 survivors. (d) Let chunk A be the survivors in the partner batch
of the earlier walk (j from 1 to 7, 8 to 14, 15 to 21, 22 to 28 or 29 to 31) that holds the most of them, the first such batch,
and chunk B the other survivors: each has at most 7 members, and walking the representative and then the two chunks, each a batch
of 9.8 with its own cache, fills at most as many batches as walking the five partner batches, outer step by outer step. (e) The
byte guard fires on at most 128 of the 16,384 clusters of a context.

*Proof.* (a) Bits 0 to 9 of e_j are those of e_0, and e_0 mod 2^10 = 303 + 4 m (hexadecimal, m < 64) is at least 303 > 181 =
Y3 mod 2^10, so y_j = y_0 + 2^10 j with bits 10 to 15 of y_j equal to 16 + j and bit 16 equal to 0 (as in Lemma KP), and
ROL(y_j, 7) = ROL(y_0, 7) + 2^17 j, with bits 17 to 22 equal to 16 + j and every other bit that of the representative. So
bits 0 to 16 of Y8 = ROL(y, 7) XOR C0.b1 are common and c17 is common; bits 0 to 16 of Y12 are common, so bits 8 to 24 of Y0
= ROL(Y12, 8) XOR C0.d1 are common, and only its low byte varies. When bits 8 to 15 of Y0 differ from those of A, the carry
into bit 16 of Y0 + K' = Y0 - A does not depend on that byte, so bits 16 to 24 of X0 and c25 are common; then bits 0 to 8 of
D0.a1 = ROR(X0, 16) XOR S15', of w8 and of e1 are common, and so are omega mod 512, c9a and c9b. Following the windows, bits
17 to 21 of Y8 are ((16 + j) XOR (C0.b1 >> 17)) mod 32; adding (-C0.c1) >> 17 and c17 gives bits 17 to 21 of Y12; the XOR
with C0.d1 >> 25 gives bits 25 to 29 of Y0; adding K' >> 25 and c25 gives those of X0; the XOR with S15' >> 9 gives bits 9
to 13 of D0.a1; adding (-S0 - S5) >> 9 and c9a gives those of w8; and adding bits 9 to 13 of e1, 1 + 2 (j mod 16), and c9b
gives those of omega: o(IX, j). In every step but the last, bit i of the result is bit i of j XOR a function of the bits of
j below i; the last adds 2 (j mod 16), whose bit i is bit i - 1 of j, which keeps that form; so j -> o(IX, j) is triangular
with unit diagonal, a bijection. (b) The bits 0 to 15 of the equation (2) depend only on omega and f modulo 2^16, so a
solution of (2) is one modulo 2^16; the w < 2^16 for which (2) has a solution modulo 2^16 for some row of S were listed
exhaustively by a carry-pair walk over the 65,536 values (the participant's arithmetic program): 7,072 of them, exactly
those with alive16(w) = 1. (c) follows from (a) and (b); LW[b8] has at most 9 bits set and j -> o(IX, j) is a bijection, so
at most 9 values of j survive. (d) If chunk A holds m survivors and there are at most 9 in five batches, then m >= 2 or
there are at most 5, so chunk B has at most 7; chunk A, inside one batch, has at most 7. A chunk is filled only when it
holds a member with T2[omega] not 0; chunk A's members are in its old batch and chunk B's in old batches other than A's, so
a filled chunk A maps to its filled old batch and a filled chunk B to a different filled old batch; the representative batch
is the same in both walks. (e) Bits 8 to 15 of Y0 are bits 0 to 7 of Y8 + (-C0.c1) XOR bits 8 to 15 of C0.d1, a bijection of
bits 0 to 7 of Y8 = ROL(y, 7) XOR C0.b1, which carry y[25..31] and y[0] = 0. The class fixes e1[22..25] = 0011 (from bit 22
up) and leaves e1[26..31] and e1[20], e1[21] free, and y[25..31] = (e1[25..31] - Y3[25..31] - [e1[21] = 0]) mod 128: for a
fixed e1[21] the 64 values of e1[26..31] give 64 different values, all of one parity, and the two values of e1[21] give
opposite parities. So the byte of the guard is hit by at most one value of (e1[26..31], e1[21]), and with the 2^7 values of
e1[2..7] and e1[20] by at most 128 clusters. QED. The lemma uses no law of the words; the participant's arithmetic program
also checks (a) on 3,000 random clusters and the bijection for every IX, the chunk sizes, and (e) on 24 random contexts, and
the declared program compares every partner of every walked descriptor with (a) and (c) (9.2).

So the masked walk loses nothing: every partner with a nonzero mask of (2) is in a chunk, so the E lanes, passing lanes, solver
calls, debits and listed good trials of a context are those of the walk with five partner batches, outer step by outer step, and
only their order inside a cluster can differ, when its two chunks both hold passing lanes.

*The walk of a context (GPT Sol, answers CJ 2 to 5, D12 and D14; our audit).* Step 0 of 9.1 writes the member lists in cluster
order (9.8), interleaved: for each representative batch b, the pair (U[b], E[b]) of its representatives, lane i holding the
representative of cluster 7 b + i (lanes 0 to 3 in the last pair), followed by the five partner pairs of each of its clusters in
lane order, holding its partners j = 1 to 31 in order, seven to a pair and three in the fifth: 72 words for a full batch, 42 for
the last; 168,522 words, 5,392,704 bytes, every member in exactly one lane. Besides the sixteen operands of 9.8 a context prepares
A = -K', its four flags hbad_i, the *gate base* BG6 = 2^35 + 2^16 Hbad + 2^22 A[8..15] in every lane, A[8..15] in a register, and
the *descriptor table* of its masked walk: for each of the 16 values of IX and each b8 with W mod 128 in S7, the survivors of
Lemma XF (c) in two chunks as in (d), the chunk that holds the least survivor first, at word address DB + 8 (2 IX + 32 b8 + 64)
with DB = 2^36 + 2^24 - 2^13: n_0, JU_0 and JE_0 in its words 0 to 2 and n_1, JU_1 and JE_1 in its words 4 to 6, n the size of the
chunk, JU the sum of 2^(36 t + 17) j_t and JE that of 2^(36 t + 10) j_t over its members j_t in increasing order. The other 96
descriptors have n_0 = n_1 = 0, and the table PX of 512 words at DB + 4,096, PX[w] = 32 (bit 8 of w) + 64 [w mod 128 in S7], is
built once. The representative loop is written out for the 2,341 representative batches of a context, each a *representative
batch*, with the list addresses as immediates (GPT Sol, answer D13):

- the pair and the omega side of 9.8, which give X0, Y0, Y12, Y8, D0a1, cg and om in every lane;
- the key of every lane, key = (om AND R7) OR (Y0 AND R8) OR (E AND R20) OR BG6, three ANDs and three ORs, 6 operations and no
  shift (GPT Sol, answer D16), with R7, R8 and R20 the masks of bits 0 to 6, 8 to 15 and 20 to 21 of each lane: in lane i it is
  2^35 + omega mod 128 + 2^8 p[8..15] + 2^16 Hbad + 2^20 e[20..21] + 2^22 A[8..15], the word address of the representative's gate
  entry, every field in its own bits, so no carry crosses a field or a lane, and every lane below 2^35 + 2^30;
- the carry word IX = (((Y12 XOR Y8 XOR (-C0.c1)) >> 17) AND N1) OR (((X0 XOR Y0 XOR K') >> 24) AND N2) OR (((w8 XOR D0a1 XOR
  (-S0 - S5)) >> 7) AND N4) OR (((om XOR E XOR w8) >> 6) AND N8), with w8 = D0a1 + (-S0 - S5) and N1, N2, N4 and N8 the words
  with bit 0, 1, 2 or 3 of every lane: the four carries of Lemma XF in bits 0 to 3 of every lane, 20 operations, which the
  context pays;
- for each used lane in order, the *gate test*: the key of the lane taken out by a shift and an AND (lane 0 needs no shift and
  lane 6 no AND, bits 252 to 255 being zero), the entry loaded at that address, compared with zero and branched on, 5 units, 4 for
  lanes 0 and 6. On 0 the cluster is skipped: T2' is not read (Lemma CL). Otherwise the cluster is *opened*: u_O is added to W;
  the representative's lane test reads T2' at its om, with its E handler and passing lane as in 9.8; then the *byte guard*
  compares bits 8 to 15 of lane i of Y0 with A[8..15], 4 units. On a fire, the *fallback*: the five partner pairs at p + 2 + 10 i
  to p + 11 + 10 i run as five batches of 9.8, each with its lane tests, E handlers, fill and cached Y9 and passing lanes.
  Otherwise the *descriptor selection*: bits 0 to 3 of lane i of IX and bits 0 to 8 of lane i of om are taken out, PX is loaded at
  the latter, the index 2 IX OR PX and the descriptor address DB + 8 (index) are formed, and n_0 is loaded, compared with zero and
  branched on; on 0 no partner survives and the cluster ends. Otherwise the representative's U and E are taken out of lane i and
  *broadcast* to the seven lanes by three shifts and ORs each (w OR (w << 36), then the same with 72 and 108; lane 3 receives
  equal bits twice); then each chunk in turn: its n (n_0, still in its register, for the first chunk; n_1, loaded at the
  descriptor address plus 4, for the second) is decoded by a depth-three tree of comparisons whose leaves are the code for n
  lanes, JU and JE are loaded and added to the broadcast U and E, which gives the U and E of a batch whose lane t holds the
  partner j_t (Lemma MB), and the chunk runs as a batch of 9.8 with n used lanes and its own cache; the leaf 0 of the second chunk
  ends the cluster. All this precedes the gate test of the next lane. The representative batch is one batch of 9.8 for the cache:
  it is filled at most once, at its first representative E lane.

The code of an opened cluster, its fallback and its chunks included, is written out at each representative lane site, so the
branch of the gate test skips it; the code of a chunk at each leaf of a dispatch tree ends with one jump to the code that follows
the chunk, and the end of the cluster falls through to the gate test of the next lane. The words of the representative batch, its
key, E[b], om, Y0, X0, Y12 and its cached Y9, stay in their registers through the partner batches and chunks, which use other
registers (9.8), so nothing is stored or reloaded around them and no count is restored from a copy.

*Charges (Section 11).* A representative batch costs 59: 3 for the pair, 17 for the omega side, 6 for the key and 33 for the
seven gate tests; its list addresses are immediates, so it has no cursor (GPT Sol, answer D13), and it has no lane test on T2'.
The last representative pair has four used lanes and costs 45, its gate tests being 4 + 3 * 5 = 19. The carry word, 20 units per
representative batch, is paid by the context. An opened cluster costs 144 (GPT Sol, answer D18, after Grok, job 58): at most 5
for the representative's T2' load and test; 3 for the addition of u_O to W and the jumps at the ends of the two chunks; 13 for
the descriptor selection (the lane extraction and mask of IX, 2; those of the omega prefix, 2; PX, its address and load, 2; the
shift of IX and the OR of the index, 2; its shift and the addition of DB, 2; the load of n_0 at that address, 1; its comparison
and branch, 2), 11 in lane 0, which needs no shifts; 4 for the byte guard; 16 for the broadcasts (two lane extractions, 2 each,
and two broadcasts, 6 each); at most 77 for the omega sides and lane tests of the two chunks; and 12 + 14 for their addressing
(for each chunk the dispatch, three comparisons and branches, 6, and JU and JE, each an addition of its offset to the descriptor
address, a load and an addition to the broadcast word, 6; the second chunk also loads n_1, 2, and costs 8 when it is empty): 5 +
3 + 13 + 4 + 16 + 77 + 12 + 14 = 144. A chunk of n lanes runs its omega side, 17, and its lane tests, 4 + 5 (n - 1) for n < 7
and 33 for n = 7, so it costs c(n) = 16 + 5 n for n < 7 and c(7) = 50; by Lemma XF (c) and (d) the two chunks have n_A, n_B <= 7
and n_A + n_B <= 9, so c(n_A) + c(n_B) = 32 + 5 (n_A + n_B) - [n_A = 7] - [n_B = 7] <= 77 when both are used, with equality when
n_A + n_B = 9 and neither is 7, and c(n_A) <= 50 when the second is empty. The parts do not overlap: the 77 prices only the
omega sides and lane tests, the 12 + 14 the operands and the dispatch of the chunks, the 13 the descriptor address and the first
load and test of n_0, which the first chunk reuses, and the 3 the addition to W and the two end jumps; a cluster with no
surviving partner ends at the test of n_0, and an empty second chunk at its dispatch. A fallback cluster costs the 257 of the
earlier walk, 5 + 21 + 4 * 50 + 31, and the guard, 261: u_O = 144 is added to W and the other 117 are paid by the context, which
allows 128 of them (Lemma XF (e)). E lanes, fills and passing lanes of the representative and of the partners are charged in
their own rows. The descriptor table of a context costs at most 48,896, charged 50,000: 16 * 32 * 50 for the masks of the 16
carry indices at the 32 values of j (21 for the window arithmetic, 12 for the two tests of LW and 17 for decoding, the store and
control), 32 * (32 * 10 + 5 * 8 + 9 * 32 + 16) for the 32 descriptors with W mod 128 in S7 (the 31 positions at 10, five steps
of the largest batch at 8, at most 9 survivors placed at 32 and the stores at 16), and 2,048 for its setup, the reset of n_0 and
n_1 of the 96 other descriptors (672) and the save and reload of 64 words around it (256) (GPT Sol, answer D14 5). The flags and
the base of the gate cost a context at most 132 units, charged 160 (GPT Sol, answer D14): at each of the four sites H_i (an XOR,
a subtraction and an AND, 3), lo0_i (1) and lo1_i (3), the minimum and maximum with a branch and two assignments (4), the two
range comparisons and their AND (3) and the shift and OR into Hbad (2), 16 a site; 10 for the cuts of b, c, d and A and for A;
10 for BG6 and its copy into seven lanes by three shifts and ORs; 32 for addressed loads and stores of context words; and 16 for
staging and control. The gate table is built once (GPT Sol, answer D16): over its 2^22 prefixes (a, m, h and the four sites i),
with the straddle bit and the address prefix formed outside the 256 entries of w and bit 7, at most 32 units per prefix; for
each entry at most 8 (the flag F[q] = [q mod 128 in S7], its address and load, 2; an OR, 1; the address and the store, 2; the
loop, 3); and 4,096 for the 256 flags and the constants: 8 * 2^30 + 32 * 2^22 + 4,096 = 8,724,156,416 units, below 2^34.

**Lemma OR (the opening rate of the gate).** Let the seven outer words of a context be independent and uniform, as in a run (Lemma
CX (a)). Then the number A(C) of clusters of the context whose gate entry is 1 has

    E[A(C)] <= 6,656 + (38/64) * 16,384 * 9/65,536 = 852,139 / 2^7 = 6657.3359375,

so the mean share of opened clusters is at most p* = 852,139 / 2^21 = 0.40633153915...; no independence between the clusters of a
context is used.

*Proof (GPT Sol, answer D14).* (a) *Blocks.* The free bits of a representative's e other than 10 to 14 are e[2..7], e[20..21] and
e[26..31]. Fix e[20..21] and e[26..31] and let u = e[2..7] run over its 64 values: a *block* of 64 representatives, 256 blocks to
a context. Since e mod 2^10 = 303 + 4 u > 181 = Y3 mod 2^10 (hexadecimal), u changes no bit of y = e - Y3 from bit 10 up, and y[0]
= 0. So on a block i = e[20..21] is fixed, and so is p[8..15] = v[0..7] XOR d[8..15], since v[0..7] depends only on r[0..7] =
(y[25..31] and y[0]) XOR b[0..7]: the straddle flag is constant on a block.

(b) *A block that does not straddle opens on exactly 26.* Put z = y[1..7]. As u runs over its 64 values, y mod 256 = (4 u - 126)
mod 256 and z = (2 u - 63) mod 128 run through the 64 odd residues, with e mod 128 = (1 + 2 z) mod 128. Every representative of
the block has r[24..31] = T_i XOR b[24..31], so its p has the low byte lo0_i or lo1_i and the block's p[8..15]; off straddle the
borrow into bit 16 of x = p - A is therefore the same for all of them, as in the proof of Lemma CL, and so is the borrow into bit
8 of v = r - c, which depends on r[0..7] alone. With b8, c8, d16, A16, L7 and SS7 the seven-bit slices b[8..14], c[8..14],
d[16..22], A[16..22], L[0..6] and (S0 + S5)[0..6], and br8 and br16 the two borrows, the identity omega = (ROL(x, 16) XOR L) + e -
S0 - S5 gives

    omega mod 128 = (1 + 2 z + P(z)) mod 128,   P(z) = ((((((z XOR b8) - c8 - br8) XOR d16) - A16 - br16) XOR L7) - SS7) mod 128.

An XOR with a constant and a subtraction of a constant change bit k of their input by a function of the bits below k alone, and so
does the addition of 2 z, whose bit k is bit k - 1 of z; so z -> (1 + 2 z + P(z)) mod 128 is triangular with a unit diagonal, a
bijection of the 128 residues, and its bit 0 is z[0] plus a constant, so the 64 odd z go onto the 64 residues of one parity. S7
holds 26 residues of each parity, so exactly 26 representatives of the block have omega mod 128 in S7, and these are the ones
whose gate opens.

(c) *Per context.* With B(C) the number of straddling blocks of the context and G(C) = 64 B(C), pointwise

    A(C) <= 26 (256 - B(C)) + 64 B(C) = 6,656 + (38/64) G(C).

(d) *The straddle probability.* Condition on w6, S11 and S4. The lines of step CO give c = C0.c1 = X8 + C0.d1 with X8 = ROL(X7, 7)
XOR D2.b1, and b = C0.b1 = ROR(X4 XOR c, 12) with X4 = ROR(D3.b1 XOR X9, 7), where D3.b1 depends only on w6, S11 and S4; so
(C0.d1, D2.b1, X9) -> (d, c, b) is a bijection, b, c and d are independent and uniform, and the outer word x = D2.a1 is uniform
and independent of them. Given b, c and d, the word p of the representative, the flags hbad_i and K = b + w6 + X4 are fixed, and A
= K + w2. With B = D2.b1 + W13, the context's X13 and R = S9 - IV[1], also fixed, the lines X2, D2.d1, S13, K1.c1, K1.d1, K1.a1
and w2 give

    s13 = ROL(ROL(X13, 8) XOR (x + B), 16) XOR x,   w2 = ROL(R - s13, 16) - IV[1] - IV[5].

For a fixed low half of x the high half of s13 is a constant XOR the high half of x, a bijection, and the high half of R - s13 is
R[16..31] - s13[16..31] - br with br in {0, 1}, so one value of it comes from at most two values of s13[16..31], whatever br does.
So each value of w2 mod 2^16, and of A mod 2^16 = (K + w2) mod 2^16, comes from at most 2 * 2^16 of the 2^32 values of x:
probability at most 2 / 2^16. The cluster straddles exactly when A mod 2^16 = 2^8 p[8..15] + a with min(lo0_i, lo1_i) < a <=
max(lo0_i, lo1_i), which are gap = |lo0_i - lo1_i| values, so given b, c and d it straddles with probability at most 2 gap / 2^16.
H_i is uniform, b[24..31] being uniform and independent of c, and d[0..7] is uniform and independent of H_i. For H_i not 0 with t
trailing zero bits, H_i XOR d[0..7] and (H_i - 1) XOR d[0..7] differ exactly in bits 0 to t, where they are complements, and the
mean of their distance is 2^t; 2^(7 - t) values of H_i have t trailing zeros, for t = 0 to 7; for H_i = 0 the two bytes are
complements, mean 128. So

    E[gap] = (sum over t = 0 to 7 of 2^(7 - t) 2^t + 128) / 256 = 9/2,   Pr(straddle) <= 2 E[gap] / 2^16 = 9/65,536.

(e) Summing over the 16,384 representatives, E[G(C)] <= 16,384 * 9/65,536, and (c) gives E[A(C)] <= 6,656 + (38/64) * 16,384 *
9/65,536 = 852,139/128. QED. The law of the outer words enters only in (d), as the independent uniform outer words of Lemma CX
(a). The participant's arithmetic program checks (a) and (b) on 3,000 random blocks (each that does not straddle opens on exactly
26 of its 64), the bijection of (b) for 2,000 random settings of the slices, E[gap] exactly over the 65,536 pairs (H_i, d[0..7]),
294,912 / 65,536 = 9/2, the two-preimage bound of (d) for 6 random settings over all 2^16 high halves, and the bound and the
budget below in exact fractions. As a check, not used here: in the declared program's run of 4,096 trials (9.2) the gate opened on
0.4024 of 131,072 clusters.

*The budget (GPT Sol, answer CJ 1.2).* With s = ceil(sqrt(10 * RUN_CONTEXTS)) = 110,404,312, the opened clusters enter WB (9.1)
with the budget

    A_BUDGET = ceil(852,139 * RUN_CONTEXTS / 2^7) + 16,384 * s
             = 8,114,701,346,782,505,236 + 1,808,864,247,808
             = 8,114,703,155,646,753,044.

The A(C) of the contexts of a run are independent and identically distributed, each between 0 and 16,384 (Lemma CX (a)); by Lemma
OR their total has mean at most 852,139 * RUN_CONTEXTS / 2^7, and it bounds the opened count of the run. Hoeffding's inequality
puts the probability that the opened count exceeds A_BUDGET at most exp(-2 (16,384 s)^2 / (RUN_CONTEXTS * 16,384^2)) = exp(-2 s^2
/ RUN_CONTEXTS) <= exp(-20) < 2.1 * 10^-9. No premise enters: the budget bears on the success probability alone (10.4), and the
time bound charges u_O A_BUDGET in WB, with W_CTX, whatever the words.

## 10. The rate of a counter trial and the success probability

**10.1 The model rate.** The seven-word model M of Section 13 treats the residual of a trial as a function of seven words, E1.d1,
E1.b1 and E1.a2 of message A and Y4, Y9, w8 and E3.h1. In this package Y4 is uniform in the class of eta, not in the sub-class,
and the other six are independent uniform words, so M has 2^192 * 2^19 = 2^211 inputs. Under M the rate of the class is
85074516985129 / 524288 = 162,266,763.66 (Section 13): a trial has R = 0 with probability that number times 2^-128. The part of a
value beta of E1's first-half b difference in it is written r(beta); the part of beta* is 71,698,432, and the part of the six
outcomes of S that this search lists (below) is 67,633,152. A trial of Section 8 has c1 in Q* and so the difference beta* (Theorem
C (iv)); under M the event that c1 = Y11 + E1.d1 lies in Q* has probability 2^-11 and is the event that the difference is beta*
(Lemma S1). The rate at which a trial that M conditions on c1 in Q* has R = 0 with an outcome of S is therefore

    p = 2^11 * 67,633,152 * 2^-128 = 138,512,695,296 * 2^-128 = 1,032 * 2^-101,

about 2^-90.989. It is 853.61 = 2^9.738 times the model rate of a trial of the class.

*The outcomes of beta*.* In the count of Section 13 an outcome of beta is a pair (tau, eps) of the differences of E1's a and c
outputs. For an outcome j of beta*, L_j is the number of triples (E1.c1, E1.b1, E1.a2) of words for which E1 on A and on B (6.2)
gives the differences beta*, tau_j and eps_j; and N3_j is the number N3 of step 3 of the count for that outcome: the number of
quadruples (Y4, E3.h1, Y9, w8), Y4 in the class, for which E3 on A and on B gives the differences eta and tau_j XOR ROR(tau_j, 1)
of its first-half d and b values and tau_j and eps_j of its c and a outputs. Every input of the 2^211 of the model falls into one
outcome, so r(beta*) = sum over j of L_j N3_j / 2^83. Beta* has fourteen outcomes on the class, all with eps = 6e21be55; this
search lists the six of S, j = 1 to 5 and 7:

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

The rows j = 1 to 7 have the L_j of the sub-class of entry 26ebba63 and four times its N3_j, so on this scale they carry exactly
its 67,698,688 = 1,033 * 2^16. S leaves out row 6, 675020a0, with 65,536 = 2^16, and carries 67,633,152 = 1,032 * 2^16, so p =
1,032 * 2^-101 exactly; the rows j = 8 to 14, with bit 14 of tau set, add 3,999,744, 5.6 per cent of the part of beta*, and are
not listed either. The integers L_j and N3_j are those of the participant's counting program, printed in Section 17 with the six
rows of its output that this search lists; it prints L_j N3_j / 2^81, four times the last column, and the six listed rows sum to
270,532,608 = 4 * 67,633,152 there, and the scale 2^83 is that of a trial with Y4 uniform in the 2^19 members of the class (GPT
Sol, answer AQ 3). Of the 52 values of tau that pass the screens of the count, 30 have N3_j > 0 and 14 have L_j N3_j > 0. The
count uses no rule on h1.

*Why S.* S = 5f is part of the stated advice record of Section 12, and what the analysis uses of it is verified here: its count,
67,633,152 = 1,032 * 2^16 (the table above, Section 17), its certificate with SHARE and E_COUNT (Section 8) and its charge
(Section 11). It is not claimed to be least under Section 11; step 3 of SEL (Section 12) chose it under the ledger of entry
415e792c (GPT Sol, answer AW 4).

*Why beta*.* Beta* = 18b0e098 is a value of the stated advice record, and what the analysis uses of it is verified here: its cube
of c1, k = 11 fixed bits, mask 0e09818b and value 02008000 (Theorem C (iii) and (iv)), and its fourteen outcomes on the class with
their counts (the table above). It is the beta of the solution with which the solver found the six constants.

**10.2 Lemmas on the counter sampler (GPT Sol 6.1).** The following lemmas were proved by GPT Sol 6.1 for this construction, Lemma
S9 by GPT Sol in its answer AC, and are given with their hypotheses; each is exact mathematics under the hypotheses stated. The
participant compared Lemmas S1 to S4 and Lemma IP with the construction line by line; the carry Lemma S5 was not re-derived by the
participant. They do not prove the rate of H1' or the success probability; 10.3 states what remains a premise. The proofs of
Lemmas S1 and S9 hold for any fixed set of members (GPT Sol, answer AN 1); here the set is the class.

**Lemma S1 (conditioning the model).** *Hypotheses:* under M the six words E1.d1, E1.b1, E1.a2, Y9, w8 and E3.h1 are independent
uniform words, independent of Y4, which is uniform in the class; c1 = Y11 + E1.d1. *Statement:* c1 lies in Q* with probability
2^-11, and that is the event that E1's first-half b difference is beta*. Conditional on it, E1.d1 is uniform on Q* - Y11, E1.b1
and E1.a2 keep their independent uniform laws, and (Y4, Y9, w8, E3.h1) keeps its law and stays independent of (E1.d1, E1.b1,
E1.a2). Hence, with G_S the event that R = 0 with an outcome of S, Pr_M(G_S | c1 in Q*) = 2^11 Pr_M(G_S and c1 in Q*) = 2^11 *
67,633,152 * 2^-128 = p, the last step by the count of 10.1.

*Proof.* Translation by Y11 makes c1 uniform and independent of every other coordinate. By the identity of the proof of Theorem C
(iv), c1 lies in Q* exactly when the difference is beta*, and Q* fixes 11 bits of c1, so the probability is 2^-11. The event
depends on E1.d1 alone, so for every event G1 of the words of E1 and G3 of the words of E3, Pr_M(G1 and G3 | c1 in Q*) = Pr_M(G1 |
c1 in Q*) Pr_M(G3). No independence of the output differences inside E1 or inside E3 is used. QED. The finite counts behind
67,633,152 are those of the counting program of Section 17 and are not proved by this lemma.

**Lemma S2 (the outer chart).** *Hypotheses:* y and c1 are fixed; the seven outer words are independent uniform words; the names
obey the assignments of step CO, with flags 3 and v[13] = 0. *Statement:* the seven outer words are in bijection with the seven
context words (C0.c1, C0.d1, D3.d1, S15, S9, w5, X2) of Section 4. These are therefore independent uniform words, and their law
does not depend on c1 or y.

*Proof.* Given the context words, these assignments, which are lines of steps O and M of Section 4 with flags 3 in place of 11,
return the outer words: S2 = K2.a1 + K2.b1 + w5; S14 = ROR(K2.d1 XOR S2, 8); D3.a1 = ROL(D3.d1,16) XOR S14; D3.b1 = X3 - D3.a1;
D3.c1 = S9 + D3.d1; S4 = ROL(D3.b1,12) XOR D3.c1; S3 = D3.a1 - S4; X14 = ROR(D3.d1 XOR X3, 8); X9 = D3.c1 + X14; K3.d1 =
ROL(S15,8) XOR S3; w6 = (ROL(K3.d1,16) XOR 3) - IV[3] - IV[7]; S11 = IV[3] + K3.d1 + S15; X8 = C0.c1 - C0.d1; D2.b1 = ROL(X7,7)
XOR X8; D2.a1 = X2 - D2.b1 - W13. Substituted into K2, D3, K3 and D2 they return w5, D3.d1, S9, S15, X2, C0.c1 and C0.d1, and the
lines of step CO, run on the outer words they return, give the context words back. Both maps are inverse bijections between two
sets of 2^224 elements, and the uniform law is carried to the uniform law. QED.

**Lemma S3 (two independent offsets).** *Hypotheses:* those of Lemma S2. *Statement:* (w5, D3.a1, Y12, S15, X2, X8, C0.d1) is
another chart of the outer words, so these seven are independent uniform words; in particular Y12 and w5, which E1 reads, are
independent uniform words.

*Proof.* The chart is reached by replacements of coordinates, each a bijection with the other coordinates held fixed: (w6, S11) by
(S3, S15), with inverse K3.d1 = ROL(S15,8) XOR S3, w6 = (ROL(K3.d1,16) XOR 3) - IV[3] - IV[7], S11 = IV[3] + K3.d1 + S15; (D2.a1,
D2.b1) by (X2, X8), with D2.b1 = ROL(X7,7) XOR X8 and D2.a1 = X2 - D2.b1 - W13; (S3, S4, X9) by (D3.a1, S4, S14), with inverse
D3.b1 = X3 - D3.a1, D3.d1 = ROR(S14 XOR D3.a1, 16), X14 = ROR(D3.d1 XOR X3, 8), D3.c1 = ROL(D3.b1,12) XOR S4, X9 = D3.c1 + X14, S3
= D3.a1 - S4; S14 by w5, with S2 = K2.a1 + K2.b1 + w5 and S14 = ROR(K2.d1 XOR S2, 8); at fixed D3.a1 and S14, S4 by X4, with
inverse X9 = ROL(X4,7) XOR D3.b1, D3.c1 = X9 - X14, S4 = ROL(D3.b1,12) XOR D3.c1; and last, with C0.c1 = X8 + C0.d1, X4 by Y12,
with C0.b1 = (Y12 + C0.c1) XOR ROL(y,7) and X4 = ROL(C0.b1,12) XOR C0.c1. The composition proves the chart and the uniform law. It
says nothing about the independence of Y12 and w5 from functions that also depend on them, such as the residual. QED.

**Lemma S4 (a marginal and the physical conditioning).** *Hypotheses:* those of Lemmas S2 and S3, and c1 independent of the outer
words. *Statement:* (a) At each fixed c1 and y, E1.a1 and E1.a2 - E1.b1 are independent uniform words. (b) For two members c1 and
c1' of Q* in one outer step, put m4 = ROL((c1 - Y11) XOR (c1' - Y11), 16); then the difference of their values of E1.a2 - E1.b1 is
m4 - 2 (E1.a1 AND m4), E1.a1 being that of c1, and conditional only on the value of E1.a2 - E1.b1 at c1 it is uniform on the
values m4 - 2 s, s a submask of m4 AND 7fffffff, which are all different. (c) Let a baseline sampler draw t as a uniform 32-bit
word, t = 0 included as an algebraic trace, with flags 3, the same constants and the same outer words, and solve c1 from it; then
c1 is uniform and independent of the outer words and y, and the sampler of Section 8, c1 uniform in Q*, is exactly the baseline
conditioned on c1 in Q*: for every event of the trace, its probability under the sampler of Section 8 is 2^11 times the
probability under the baseline that it happens and c1 lies in Q*.

*Proof.* (a) By Lemma S3, Y12 and w5 are independent uniform, so E1.a1 = ROL(E1.d1,16) XOR Y12 and w5 are, and E1.a2 - E1.b1 =
E1.a1 + w5 by E1's fifth assignment; replacing (E1.a1, w5) by (E1.a1, E1.a1 + w5) is a bijection. (b) The same outer words give
c1' the first value E1.a1 XOR m4 and the same w5, and (X XOR m4) - X = m4 - 2 (X AND m4) modulo 2^32. Conditional on the first
value, E1.a1 stays uniform, its bits under m4 AND 7fffffff give the uniform law stated, and different submasks below 2^31 have
different doubles. (c) By Lemma IP, c1 -> t is a permutation for every outer step and y, so a uniform t makes c1 uniform and
independent of them; conditioning on c1 in Q*, an event of probability 2^-11, leaves the outer words and y unchanged, and step CT
run forwards from c1 is the same trace. QED. Statement (c) is about the construction's own sampler and does not identify it with
M; it lets an event include t != 0 but does not say how much of the rare success mass the rule t != 0 removes.

**Lemma S5 (a carry prescription).** *Statement:* let x, s, s', a and d be words of w bits with (x + s) XOR ((x XOR a) + s') = d.
Every bit i < w - 1 at which a and d differ is determined by the lower bits of x and by the constants; so at most 2^(w - n1) words
x solve the equation, n1 being the number of bits of (a XOR d) AND (2^(w - 1) - 1).

*Proof.* Write u_i and u'_i for the carries into bit i of the two additions. Equality at bit i gives a_i XOR d_i = s_i XOR s'_i
XOR u_i XOR u'_i. If its left side is 1, exactly one of the pairs (s_i, u_i) and (s'_i, u'_i) has unequal bits; the carry out of
that addition is its variable input bit, x_i or x_i XOR a_i, and the carry out of the other addition is its fixed common bit.
Equality at bit i + 1 prescribes the XOR of the two carries out, which fixes x_i. Counting the choices from the low bits to the
high bits gives the bound; bit w - 1 has no next bit, which is why it is left out. QED.

**Lemma S8 (success from a mean and a factorial moment).** *Statement:* let N_o be a count with values in {0, 1, ..}, mu =
E[N_o] > 0 and rho = E[N_o (N_o - 1)] / mu. Then Pr(N_o > 0) >= mu b(rho), where b(rho) = (2 r_o - rho) / (r_o (r_o + 1)) and
r_o = floor(rho) + 1; for 0 <= rho <= 1 this is 1 - rho / 2, and b decreases with rho. If the outer steps of a run are
independent and each has mean at least mu and ratio at most rho, the probability that some outer step has N_o > 0 is at least
1 - exp(-mu b(rho) times the number of outer steps).

*Proof.* For integers r_o >= 1 and z >= 0, the indicator of z > 0 is at least (2 r_o z - z (z - 1)) / (r_o (r_o + 1)): with
equality at z = 0, and for z >= 1 the inequality is (z - r_o)(z - r_o - 1) >= 0, which holds for integers. Taking expectations
gives the first statement. For independent outer steps, the probability that none has N_o > 0 is the product of the values 1 -
Pr(N_o > 0) of the outer steps, at most exp(-mu b(rho) times their number). QED. The proof uses only that the units are
independent and that each count takes values in {0, 1, ..}; it holds as well for the contexts of 9.8, with the count N_c of a
context in place of N_o (10.3).

**Lemma S9 (the success mass lies on passing outer steps; GPT Sol, answer AC).** (a) *No hypothesis.* In every outer step that
does not pass the filter, the count N_o of H1' (10.3) is zero. Let pi_o be the probability that an outer step of step 1 of 9.1
passes the filter, the share of the 2^256 values of its random word whose outer step passes. If pi_o > 0, then E[N_o | the outer
step passes] = E[N_o] / pi_o. (b) *Hypotheses:* those of Lemma S1. Under M, also conditional on c1 in Q*, Y9 and omega = Y3 + Y4 +
w8 are independent uniform words, and the filter passes with probability pi. G_S, the event that R = 0 and the E1 outcome is in S,
has probability p under M given c1 in Q* (Lemma S1 and the count of 10.1), and it lies inside the event that the filter passes. So
Pr_M(G_S | c1 in Q* and the filter passes) = p / pi = 1,032 / (279,070,422,111 * 2^53), about 2^-81.011, and Pr_M(the filter
passes | c1 in Q*) times this conditional rate is p: conditioning on the pass loses no part of p.

*Proof.* (a) A listed good trial has R = 0 with an outcome of S, so by Lemma F its outer step passes; N_o is a count that is zero
off the event that the outer step passes, and E[N_o] = pi_o E[N_o | the outer step passes]. (b) Under M, Y9 and w8 are independent
uniform words, independent of Y4; for fixed Y4, w8 -> omega is a translation, so (Y9, omega) is uniform on all 2^64 pairs and
independent of Y4, and Lemma S1 leaves the law of (Y4, Y9, w8, E3.h1) unchanged under c1 in Q*. The proof of Lemma F uses only the
assignments of E3 and the conditions of R = 0, which hold for the model words, so it gives the inclusion; by 10.1 p is the part of
the outcomes of S. Dividing by the probability pi of the pass gives the conditional rate. QED. Statement (a) uses the pass
probability pi_o of the sampler itself; that pi_o equals pi is not proved (H4'). Statement (b) is about M and says nothing about
the sampler.

*The search lists exactly the listed good trials.* The two lemmas below concern the search of 9.1. Lemma V follows from 3.3 and is
the participant's; Lemma CV rests on the constants and guards of 9.4, proved by GPT Sol (answers AE 4 and 7, AF 1.3, AO 6.1 and AR
1, 2 and 6.1), among them the parity certificate (P*) and Lemma J0, which hold for every joint root on the class.

**Lemma V (the certificate of a root).** Fix an outer step, a word c1 in Q* and an outcome j of beta*, and let h be E3.h1 of the
trial. The trial has R = 0 with E1 outcome j exactly when E1 on A and on B gives the XOR differences tau_j and eps = 6e21be55 of
its a and c outputs and h satisfies the joint conditions (J1), (J2) and (J3) of outcome j (9.4).

*Proof.* Write tau, eps and beta for the XOR differences between A and B of E1's a output, c output and first-half b value, and
eta, psi, tau' and eps' for those of E3's first-half d and b values and its c and a outputs, as in Section 13. beta = beta*
because c1 is in Q* (Theorem C (iv)), and eta = 830303cf (Theorem C (iii)). By 3.3, R is formed from o[1] = Z[1] XOR Z[9], o[3] =
Z[3] XOR Z[11], o[4] = Z[4] XOR Z[12] and o[6] = Z[6] XOR Z[14], where Z[1], Z[6], Z[11] and Z[12] are the a, b, c and d outputs
of E1 and Z[3], Z[4], Z[9] and Z[14] those of E3. The first two values of E1 are the same for A and B (proof of Theorem C (iv)),
so the d and b outputs of E1 differ by ROR(tau, 8) and ROR(beta XOR eps, 7); by the last three assignments of E3, its b and d
outputs differ by ROR(psi XOR tau', 7) and ROR(eta XOR eps', 8). So R = 0 exactly when tau' = tau, eps' = eps, psi = tau XOR
ROR(tau, 1) and eta = eps XOR ROL(beta XOR eps, 1), the conditions of Section 13. For E1 outcome j, tau = tau_j and eps =
6e21be55, and the last condition holds: 6e21be55 XOR ROL(18b0e098 XOR 6e21be55, 1) = 830303cf. As in the proof of Lemma F, with h'
= h XOR eta, g' = Y9 + h' and f' = ROR(y XOR g', 12), psi = f XOR f' = ROR(g XOR g', 12), so psi = sigma_j exactly when (J1)
holds. Then f' = f XOR sigma_j and the a output of E3 on B is (omega + DY3) + f', so eps' = eps exactly when (J2) holds. Then the
d output of E3 on B is ROR(h XOR eta XOR e2 XOR eps, 8) = h2 XOR mu and g' = g XOR theta_j, so tau' = tau_j exactly when (J3)
holds. QED.

**Lemma RC (the root certificate; GPT Sol, answers CF 6 and 6.1).** Fix an outer step, an outcome j of S and a word h, and let c1
be the word that step 3 of 9.1 computes from h, that of the trial with E3.h1 = h (Lemma IP). The four tests (Q), (A), (C) and (T)
of step 3 hold exactly when c1 is in Q*, t is not zero, and E1 on A and on B (6.2) gives the XOR differences tau_j and eps =
6e21be55 of its a and c outputs.

*Proof.* The lines of step 3 are those of step CT read backwards from E3.h1 = h, so they give the trial's Y14, Y6, E1.a1, E1.d1,
c1, E1.b1, E1.a2 and t. (Q) is the definition of Q*, and (T) is t != 0. Suppose (Q), and write a1, d1, c1, b1, a2, d2, c2 for the
assignments of E1 on A and primes for B (6.2). E1 on B has the same a, b and d inputs and the same first message word, so a1' = a1
and d1' = d1; its c input is Y11' = Y11 + DY11, so c1' = c1 + DY11; and b1' = b1 XOR beta* (Theorem C (iv)), which is b1 + beta* -
2 s with s = b1 AND beta*. With its second message word w5 + fffffff8, a2' = a2 + Delta(s), Delta(s) = beta* - 2 s - 8 (as in
9.7). Now a2 XOR a2' = tau_j exactly when a2 + Delta(s) = a2 XOR tau_j, that is when Delta(s) = (a2 XOR tau_j) - a2 = tau_j - 2
(a2 AND tau_j) modulo 2^32, that is when 2 (a2 AND tau_j) = (tau_j - Delta(s)) mod 2^32. Since tau_j[31] = 0, 2 (a2 AND tau_j) is
below 2^32, and tau_j - Delta(s) = tau_j - beta* + 8 + 2 s is even, as tau_j and beta* are; so this is (A). Given (A), a2' = a2
XOR tau_j, so d2 = ROR(d1 XOR a2, 8) = z and d2' = ROR(d1 XOR a2', 8) = z XOR ROR(tau_j, 8); with c2 = c1 + d2 and c2' = c1' +
d2', c2 XOR c2' = eps is (C). The same identities give (A) and (C) back from the two differences when c1 is in Q*. QED. The lemma
uses no law of the words; with Lemma V it says that a root is certified exactly when it is the E3.h1 of a listed good trial of
outcome j.

**Lemma CV (coverage of the search).** Fix an outer step that passes the filter, with T = X AND VMASK[nu] of 9.7. (a) When T is
not empty, step 2 of 9.1 returns every joint root that satisfies (G7) and (G15) of every outcome whose bit is set in T, each once,
and nothing else. (b) Run over the whole list, step 3 certifies exactly the roots that are the E3.h1 of a listed good trial of the
outer step, and the E3.h1 of every listed good trial of the outer step is among the roots; when T is empty the outer step holds no
listed good trial (Lemma VP). Hence a passing outer step has as many certified roots as its count N_o of H1' (10.3), the number of
its listed good valid trials over all of Q* (none when T is empty), and N_o <= 16.

*Proof.* (a) A leaf yields a root only if (J1), (J2) and (J3) hold as words, so each returned word is a joint root of the outcome
with which it is returned. Conversely, take a joint root h of a searched outcome, with h satisfying (G7) and (G15). By (PHASE),
(P*), Lemma J0, the guards (G7) and (G15) and the constants and guards of 9.4 its bits take those values, and its carries pass
every test of (a), (b) and (e) there: its own carry into bit 20 is a kept guess, every kept guess reaches the common state at
depth 7, and the single traversal follows the arcs of its bits from the carry pairs that its own carries give, each read from the
array of its position with the guard values that its own bits give (at position 15 its prefix passes the test of (G15) and the
prescribed bit is its h[15]), and reaches its leaf, where the three conditions hold. A depth-first traversal reaches each node
once, so h is returned once. No word is a joint root of two outcomes (9.4). (b) Let c1 in Q* give a listed good trial with
outcome j, and let h be its E3.h1. By the proof of Lemma F, h witnesses (1)_j for Y9 and the trial's f witnesses (2)_j for omega,
so bit j - 1 is set in both masks, and by Lemma VP it is set in T; in particular T is not empty. By Lemma V, h satisfies (J1) to
(J3) of outcome j, so it is a joint root; Lemmas G7 and G15 give (G7) and (G15) for it, and by (a) step 2 returns it. Step 3 maps
it to c1, since it computes the inverse of the permutation c1 -> E3.h1 of Lemma IP; c1 is in Q*, its t is not zero and its E1
outcome is j, so the root is certified (Lemma RC). Conversely, by Lemma RC a certified root h of outcome j gives a c1 in Q* with
t not zero whose E1 differences are tau_j and eps, and h satisfies (J1) to (J3), so by Lemma V the trial of c1 has R = 0 with
outcome j: it is a listed good trial. Different roots give different c1 (Lemma IP), and no outer step has more than 16 roots
(9.4). QED.

So in every passing outer step that it reaches, the search of 9.1 certifies precisely the listed good valid trials that an
enumeration of all of Q* in that outer step finds, with the same outer steps, the same members y and the same filter. The count
N_o of every outer step is the same, and with it the joint law of the counts of the outer steps of a run: H1' is about these
counts, H4' about two counts of the outer steps, H5_exec about the ledger of the calls that the pre-check keeps and H_G_cluster
about the batches with an E lane, and none of them changes (GPT Sol, answers AE 7 and AW 1 and 5). No law of the words is used by
Lemmas V, RC, VP, G7, G15 and CV. The guards of the solver are lossless: (PHASE) and (P*) are consequences of exact counts of the
class, (P*) with a count of 0 for the other parity in every phase and every outcome (9.4), and Lemma J0 is algebra; none drops a
member or a joint root. The pre-check and the guards (G7) and (G15) lose no listed good trial (Lemmas VP, G7 and G15), and walking
the outer steps by contexts changes no outer step (Lemmas CX and MB).

**10.3 Heuristics.**

The four premises H1', H4', H5_exec and H_G_cluster below concern the instance that the stated advice record of Section 12 fixes:
the six constants of 3.2, eta = 830303cf, beta* = 18b0e098 with its cube, the outcomes of beta* with the filter's values of tau
and eps, and S = 5f. Each is a statement about the run for this record and for no other, and none concerns how the record was
found. No premise concerns how the record was found: the selection procedure SEL that found it is charged in full as
preprocessing, with a cap that holds by construction (Section 12).

**Heuristic H1' (score-critical).** The coins of the run are its RUN_CONTEXTS independent fresh words (step 1 of 9.1); each gives
the seven outer words of one context, and every context walks all 2^19 members of the class, except those of clusters that hold no
listed good trial (9.8, 9.9, Lemmas CX and CL). Let N_o be the number of listed good valid trials (9.1) of one outer step, counted
over all of Q* whether or not the outer step passes the filter or the pre-check, and let N_c be the sum of N_o over the 2^19 outer
steps of a context. (i) *Rate:* for a uniform outer step U, whose seven outer words are uniform and whose member is uniform on the
class, independently (the outer step of entry 415e792c), E[N_o(U)] >= (2^21 - 1) q, with q = FACTOR * 2^-128, just under 10p / 11,
about 2^-91.126; by Lemma CX (c), E[N_c] = 2^19 E[N_o(U)]. (ii) *Dependence, with the context as the unit:* the probability that
no valid trial of the run is a listed good trial is at most exp(-0.49594) + 0.001; that is, listed good trials are not clustered,
neither among the trials of one outer step nor among the outer steps (members) of one context, beyond what this bound allows.

This is the premise of entry 415e792c, rate and dependence, restated for the walk by contexts as entry e9b6649e restates it: part
(i) is the same statement, since N_c is a sum over the whole class (Lemma CX (c)), and part (ii) is stated for the contexts, the
independent units of this run. Neither the filter, nor the pre-check, nor the guards (G7) and (G15) change it: they skip only
outer steps, outcomes and words that hold no listed good trial (Lemmas F, VP, G7 and G15), so N_o is the same count, pointwise
(GPT Sol, answer AW 1).

In the terms of Lemmas S1 to S4 the premise is this: the construction's pushforward of the uniform outer words and members, with
c1 running over all of Q*, onto the seven model words (E1.d1, E1.b1, E1.a2, Y4, Y9, w8, E3.h1) carries at least the share FACTOR /
138,512,695,296, just under 10/11, of the complete-success integral p of the conditional law of Lemma S1; that stays true after
the member with t = 0 is dropped (Lemma IP); and the dependence between trials that share a context, in one outer step or in two
outer steps of it, is weak enough for the stated success at the declared run length. The two parts are separate: neither follows
from the other, and neither follows from the model or from Lemmas S1 to S5, S8 and S9. The factor FACTOR = 125,920,632,087 is
assumed; 10.1 gives what it is set against, the count 138,512,695,296 of the six outcomes of S, of which it is ten elevenths
rounded down. The filter does not change it. The evidence for this margin is the preregistered scaled-down run of Section 13,
whose one-sided 97.7 per cent lower bound on the realised share of the predicted collisions is 0.99213, above 10/11; it is
evidence at 8 bits, not a proof at 32.

*The rate on passing outer steps.* By Lemma S9 (a), N_o is zero on every outer step that the filter rejects, so (i) says E[N_o |
the outer step passes] >= (2^21 - 1) q / pi_o, with pi_o of Lemma S9. Per member of Q* of a passing outer step the rate is then at
least about q / pi_o; for pi_o = pi it is q / pi = 125,920,632,087 / (279,070,422,111 * 2^80), about 2^-81.148: the rate of H1'
divided by the pass share, with no part of the counted mass lost (Lemma S9). The success argument below uses (i) per context and
needs no value of pi_o; pi_o enters only the pass budget (H4').

*What is proved and what is not.* Proved (Lemmas S2 to S4): the outer words of a step are uniform in the chart of the seven
context words of Section 4; Y12 and w5 are independent uniform words; E1.a1 and E1.a2 - E1.b1 are independent uniform words at
every fixed c1; and the sampler of Section 8 is exactly the uniform-counter sampler conditioned on c1 in Q*. Proved as well
(Lemmas V, RC, G7, G15 and CV, 10.2 and 9.7): in every passing outer step that it reaches, the search of 9.1 certifies exactly the
listed good valid trials of the outer step, so N_o is the same count for it as for an enumeration of all of Q*. Not proved: that
E1.b1, E1.a2, E3.h1, Y9 and w8 have the model's joint law with the rest; GPT Sol 6.1 reduces part (i) to one success-weighted
density of seven words that the outer step fixes, Y12, Y1 + w12, C2.b1, C2.c1, w5, Y9 and w8, and that density has not been
counted. Not proved either: how much of the success mass the member with t = 0 carries (Lemma IP bounds the number of dropped
trials, one in 2^21, not their mass), and the dependence inside an outer step and across the members of a context.

*Part (ii) for contexts.* The contexts of a run are independent and identically distributed (Lemma CX), and by part (i) the run
has RUN_CONTEXTS * E[N_c] = RUN_STEPS * E[N_o(U)] >= RUN_STEPS * (2^21 - 1) * FACTOR * 2^-128 = 0.4959400000... >= 0.49594. Lemma
S8, applied to the contexts with N_c in place of N_o, therefore gives part (ii) as soon as rho_c = E[N_c (N_c - 1)] / E[N_c] is at
most 0.0065: in that case b(rho_c) >= 0.99675, Lemma S8's exponent is no less than 0.4943281, and exp(-0.4943281) < 0.609981 <
exp(-0.49594) + 0.001. Write N_c as the sum of the counts N_o(m) of the members m of the context. Then

    rho_c = rho_w + rho_x,  rho_w = E[sum over m of N_o(m) (N_o(m) - 1)] / E[N_c],
                            rho_x = E[sum over m != m' of N_o(m) N_o(m')] / E[N_c],

where, by Lemma CX (c), rho_w equals E[N_o(U) (N_o(U) - 1)] / E[N_o(U)], the factorial ratio of a uniform outer step that the
clause of entry 415e792c bounds, and rho_x is the part that pairs of different members of one context add. Both are at least zero,
so rho_c <= 0.0065 implies rho_w <= 0.0065: *the clause of this package is stronger than the per-step clause of entry 415e792c*.
It contains that clause and adds the dependence across the members of a context, which the member loop creates by letting 2^19
outer steps share their seven words.

*Part (ii) is an assumption.* That rho_c <= 0.0065 is assumed. It is not measured, and it cannot be measured at full size: a
context holds a listed good trial with probability at most E[N_c] = 2^19 E[N_o(U)], about 2^19 * 2^21 * 2^-91.126 = 2^-51.126, so
no run of feasible length sees one in a context, let alone two. The margin is wide. Write v for the clustering ratio of listed
good trials by context, rho_x = v * (2^19 - 1) E[N_o(U)], so that v = 1 when the listed good trials of different members of a
context are independent; then rho_x is about v * 2^-51.126, and the clause fails only if v exceeds about 2^44, or if one listed
good trial makes another in the same context, at the same member or at another, far more likely than its rate.

*What is known of it.* An outer step has N_o <= 16 (Lemmas CV, G7 and G15), so rho_w <= 15, which does not help at this run
length. GPT Sol 6.1 proves the bound 2^-13 for rho_w in a model in which E1.b1, E1.a2 and E3.h1 are drawn afresh for every member
of Q*, and proves as well that the construction's own pair law is not of that kind (for two members of one outer step the second
member's three words take at most 2^62 values given the first's, not 2^96), so that bound does not transfer. For v, the
participant measured the same ratio, (E[n(n-1)]/E[n]) / ((2^19 - 1) p) for the count n of an event in a context and its share p
per member, for every event that a listed good trial meets and that is frequent enough to count, each run with a control arm of
independent outer steps (Section 13). From the filter to the roots of the solver it stays between 1.14 and 1.25 (the controls near
1), and it does not grow with depth; the factor comes from condition (2), whose omega = Y3 + y + w8 has w8 fixed by the context. A
preregistered run went deeper, to the two halves of a listed good trial, over 262,144 contexts and 2^46 trials per arm: the
cross-member factor Rx is 0.999 +- 0.054 (upper limit 1.162) for the listed E1 outcome at 2^-32.29 per trial and 0.90 +- 0.24
(upper limit 1.94) for (J1) and (J2) of the E3 half at 2^-34.58, and every upper limit lies at least 43 bits below the 2^43.86
that the clause allows. The joint event, about 2^-91 per trial, is not reachable, so carrying Rx near 1 to it remains the premise,
and v itself is not measured.

*No budget for steps 2 and 3.* Whenever an outer step reaches them, whatever its words, the joint solver returns no more than 16
roots and steps 2 and 3 cost no more than CM(T) <= 15,296 machine units (9.4, 9.7, Section 11), which the meter debits from the
credit as they run, exactly that work, after a preflight against CM(T) (Lemma ME); the final pair is formed and hashed at most
once, for a certified root (Lemma V). The run halts with failure only when W exceeds WB, which needs one of the four counts of 9.1
above its budget: the E count or the pass count, which H4' covers, the fill count, which H_G_cluster covers, or the opened count,
which Lemma OR bounds with no premise (9.9); when the credit does not cover the CM(T) of an outer step, which H5_exec covers, or
after the last context, which H1' covers.

**Heuristic H4' (supporting; GPT Sol, answers AW 3 and 5 and CK 2).** For an outer step of the run, before any halt, let I_E be 1
when the mask of (2) of its omega meets S and I_2 be 1 when its mask X is not zero (it passes the filter, Section 8); let N_E and
N_2 be the sums of I_E and I_2 over the RUN_STEPS outer steps. H4' says: for a uniform outer step U (that of entry 415e792c), and
hence for the mean over the outer steps of one context (Lemma CX (c)), Pr(I_E(U) = 1) <= 1.000026 p_E and Pr(I_2(U) = 1) <=
1.000176 pi, where p_E = 233,715,456 / 2^32 = 2^-4.199822 is the exact share of words omega that pass the automaton of (2) for S
and pi = 279,070,422,111 / 2^48 = 2^-9.978162 the exact share of pairs (Y9, omega) that pass the filter (Section 8), both for
uniform independent words. The two indicators of one outer step may depend on each other in any way. The factors are not proved:
Y9 and omega of a uniform outer step are not proved independent and uniform.

*Use (proved, given H4').* The contexts of a run are independent and identically distributed (Lemma CX), and N_E and N_2 are sums
over the RUN_CONTEXTS contexts of per-context counts between 0 and 2^19. Under H4' their means are at most 1.000026 RUN_STEPS p_E
and 1.000176 RUN_STEPS pi, and the budgets of 9.1 exceed these means by 2^19 s, s = ceil(sqrt(10 * RUN_CONTEXTS)). Hoeffding's
inequality over the contexts, with range 2^19, puts the probability that a count exceeds its budget at most exp(-2 (2^19 s)^2 /
(RUN_CONTEXTS * 2^38)) = exp(-2 s^2 / RUN_CONTEXTS) <= exp(-20) for each. No law of the members inside a context is used. The
number of outer steps that reach the solver has no budget and no clause here: the solver is paid from the credit, which H5_exec
covers (GPT Sol, answer AW 5). A count above its budget can make W exceed WB and halt the run with failure; the time bound charges
WB + W_CTX and is not affected.

*Evidence and the choice of the factors.* Our preregistered sample of Section 13 (prereg7, 2^39 real outer steps of the whole
class) counted 29,915,698,553 lanes with a nonzero mask of (2), against 29,915,578,368 at p_E, and 545,067,537 passing outer
steps, against 545,059,418.18 at pi. For a proposed mean p0 = alpha p and m = 2^39 p0, the lower-tail Chernoff bound for k events,
Pr(N <= k) <= exp(-(m - k)^2 / (2 m)), is at most exp(-7) when (m - k)^2 >= 14 m. On the grid of one part per million, alpha_E =
1,000,026 / 1,000,000 and alpha_P = 1,000,176 / 1,000,000 are the least factors that pass this test: in exact rational arithmetic
each passes and the factor one part per million lower fails. Under independent draws a true share above the declared bound would
have produced counts this low with probability below exp(-7) for each. The sample's words come from a pseudorandom generator
(Philox4x32-10), so this is evidence for the declared factors, not a proof; every other measured share of the two counts, with and
without the member loop, lies between 0.998 and 1.001 times its nominal value (Section 13).

**Heuristic H5_exec (supporting; GPT Sol, answer CK3; GPT-6 Astra, Batch 11).** For an outer step of the run, before any halt, its
*ledger* U0 is that of 9.7 for its call of steps 2 and 3 with the global part of 1,024 of the earlier layout: A(T) + 288 plus the
unit cost of every block that the joint solver with (G7) and (G15) and the certificate execute on the words of the outer step, for
the outcomes T = X AND VMASK[nu] that its pre-check keeps; U0 = 0 when T is empty, in particular when the outer step fails the
filter. The premise, unchanged from entry 50d28015: for a uniform outer step (that of entry 415e792c), and hence for the mean over
the outer steps of one context (Lemma CX (c)), the mean E[U0] is at most 1.01 * u_M, where u_M = 92,113,900,425,963 / 2^46 =
1.3090172562... bounds, in model M below, the mean of U over all outer steps, passing or not, with the zeros counted. It is a
statement about the joint law of all the words that the solver reads, not about T alone, and it is not a consequence of H4'.

*The model value (GPT-6 Astra, Batch 11; GPT Sol, answer CK3 1).* Model M draws Q = Y9, E = omega, C2.c1, C2.b1, Y1 + w12 and Y12
as independent uniform words and the member uniformly from the class, independently, and computes nu, the pre-check, the guards
and every other word from them as the search does. In M a call happens when the filter passes and nu is 3 or 4, with probability
p_call = 279,070,422,111 / 2^50, a quarter of pi (9.7), and then T is the mask X with probability n_X / 279,070,422,111, n_X the
counts of the certificate of Section 8. The part of U0 paid per call and per row, A(T) + 288, has the exact mean

| X | n_X | A(X) |
| --- | ---: | ---: |
| 01 | 18,637,049,340 | 4,736 |
| 02 | 96,560,460,360 | 4,736 |
| 04 | 18,637,049,340 | 4,736 |
| 08 | 5,457,993,021 | 4,736 |
| 10 | 56,709,878,706 | 4,736 |
| 12 | 57,936,276,216 | 6,144 |
| 18 | 4,792,384,116 | 6,144 |
| 40 | 10,830,033,396 | 4,736 |
| 42 | 5,943,311,010 | 8,448 |
| 52 | 3,565,986,606 | 9,856 |

E_M[A(T) | call] = 1,450,318,894,756,992 / 279,070,422,111 = 1383624064/266237 = 5196.96..., as the participant recounted it in
integers from the certificate. GPT-6 Astra proves in M, from exact counts of the rows that survive the setup of 9.4 and bounds on
the nodes and leaves that use only coordinates that are fresh at each node, that the blocks of the trees add at most
22422672/266237 = 84.22... per call; that proof is cited, not reproduced here. Hence E_M[U] <= p_call (1383624064/266237 +
22422672/266237) = u_M, exactly. Model M is a model: it is not proved that the sampler gives its words that law, and H5_exec
states the bound, with the factor 1.01, for the sampler.

*Use (proved, given H5_exec; GPT Sol, answers CK3 3 and 4 and D13).* In every call the meter debits V = U, 0 <= V <= CM(T) <=
15,296 (Lemma ME), and U <= (478/487) U0 in every outer step (Lemma CP), so the mean of U is at most 478/487 of that of U0 with no
law of calls. Let D_C be the sum of the debits over the 2^19 outer steps of a context, taken without halts: the D_C of the
contexts of a run are independent and identically distributed (Lemma CX), each between 0 and L_C = 15,296 * 2^19 = 8,019,509,248.
Under H5_exec their total has mean at most (478/487) m_0 <= m_C = 829,292,364,315,442,262,408, with m_0 =
844,906,655,693,766,489,106 >= 1.01 * RUN_STEPS * u_M, and, since D_C^2 <= L_C D_C, a variance of at most L_C m_C. With t =
ceil(sqrt(40 L_C m_C)) + 14 L_C = 16,310,253,639,682,338, expansion gives t^2 >= 40 L_C m_C + (40/3) L_C t, and Bernstein's
inequality bounds the probability that the total exceeds m_C + t = 829,308,674,569,081,944,746 by exp(-t^2 / (2 L_C m_C + (2/3)
L_C t)) <= exp(-20); the exponent is 20.00. The run debits in order and stops at the first halt, so outside that event the credit
left before any call is at least CREDIT - (m_C + t) = 15,296 >= CM(T), every preflight passes, and the credit never halts the run.
V = U holds pointwise (Lemma ME), so no second premise enters; no law of the members inside a context is used. That E[U] is at
most 1.01 u_M is not proved.

*Evidence.* A participant measurement (Section 13): on 2^32 real outer steps with the lines of the searched instance and as many
with flags 11, with fresh words for every step, the ledger U of a reimplementation of this solver averaged at most 1.300375 per
outer step, against the bound 1.01 u_M = 1.322107. It is evidence from a pseudorandom generator, not a proof.

**Heuristic H_G_cluster (supporting; GPT Sol, answer CM 5).** For a context C of the run let G(C) be the number of its 84,261
batches, its representative batches and the five partner batches of every cluster, that hold a member with a nonzero mask of (2),
counted without halts: the fills of the context in the walk of entry 50d28015, which this premise was stated for (9.8, 9.9). The
premise: for a context with uniform outer words, E[G(C)] <= 12,466. G(C) is a function of the seven outer words alone (9.9); the
premise says nothing about the members, lanes or batches of a context beyond this mean, and it is not a consequence of H4', which
bounds the mean number of E lanes, not how they share batches.

*Use (proved, given H_G_cluster; GPT Sol, answers CM 5 and D14).* The masked walk fills at most G(C) batches in every context,
outer step by outer step (Lemma XF (d)), with at most 84,261 batches that can be filled. The G(C) of the contexts of a run are
independent and identically distributed (Lemma CX), each between 0 and 84,261, and under H_G_cluster their total has mean at most
12,466 * RUN_CONTEXTS, which G_BUDGET exceeds by 84,261 s. Hoeffding's inequality over the contexts puts the probability that the
total exceeds G_BUDGET at most exp(-2 (84,261 s)^2 / (RUN_CONTEXTS * 84,261^2)) = exp(-2 s^2 / RUN_CONTEXTS) <= exp(-20). A halt
only stops fills, so the fills of a run are at most that total. No law of the batches, lanes or members inside a context is used.
If the fills exceed G_BUDGET, W can exceed WB and halt the run with failure; the time bound charges WB + W_CTX and is not
affected.

*Evidence.* Our sample of Section 13: 16,777,216 = 2^24 contexts with fresh outer words, G counted exactly in the batch order of
9.9, sum 208,495,306,067, mean 12,427.289 (standard error 1.276), largest 31,214. For independent contexts with G between 0 and
84,261, Hoeffding's inequality bounds the mean, at confidence 1 - exp(-7), by the sample mean plus 84,261 sqrt(7 / (2 n)),
12,465.77...; in exact integers, 2 (n g - sum)^2 >= 7 * 84,261^2 * n holds at g = 12,466 (843,618,896,195,301,842 >=
833,817,784,407,293,952) and fails at 12,465 (800,596,746,937,250,258), so 12,466 is the least integer that this bound supports.
The outer words come from SHAKE256 in place of uniform words, so this is evidence, not a proof.

**10.4 Success probability.** The probability space is the RUN_CONTEXTS fresh words of step 1 of 9.1, independent uniform 256-bit
words, for the fixed target and the stated advice record of Section 12; the algorithm is otherwise deterministic. Under H1', H4',
H5_exec and H_G_cluster it outputs a collision with probability at least 1 - (exp(-0.49594) + 0.001) - 2 * 10^-8 =
0.390001800132... > 0.39 (GPT Sol, answers AW 3 and 5, CJ 1.2, CK 2.2, CK3 4 and CM 6, with the tails of 10.3 and 9.9 over
contexts). This is the union bound over the events "no valid trial is a listed good trial", "the E count exceeds E_BUDGET", "the
pass count exceeds PASS_BUDGET", "the fills exceed G_BUDGET", "a preflight fails" and "the opened count exceeds A_BUDGET", which
need not be independent; a halt by W needs one of the four counts above its budget (9.1): H1' bounds the first by exp(-0.49594) +
0.001; given the means of H4', H_G_cluster and H5_exec and, for the last, with no premise (Lemma OR), Hoeffding's and Bernstein's
inequalities over the independent contexts bound each of the other five by exp(-20), and 5 exp(-20) < 1.04 * 10^-8 is below the
allowance 2 * 10^-8 kept for them. A listed good trial lies in a passing outer step (Lemma F), in a cluster whose gate opens
(Lemma CL), in a chunk of its cluster (Lemma XF), which its lane takes as passing (Lemmas MB and DT), whose pre-check keeps its
outcome (Lemma VP) and whose solver with (G7) and (G15) returns its root (Lemmas G7, G15 and CV); the search certifies it unless
the run ends before its outer step is reached, by the work register, by the credit or by the output of another pair (9.1, Lemma
CV). When the algorithm outputs a pair, the pair is a genuine collision: its trial is certified, so R = 0 (Lemmas RC and V), step
3 checks both complete digests, and the messages have different lengths. The run is the shortest of this form that gives 0.39:
RUN_STEPS_MIN is the fewest outer steps that give 0.49594 expected listed good trials, 0.49594 is the smallest number of five
decimals for which the bound reaches 0.39 (with 0.49593 in its place the bound is below 0.389996), and RUN_CONTEXTS rounds
RUN_STEPS_MIN up to whole contexts.

The heuristics are not proved; Section 13 gives the evidence for H1', H4', H5_exec and H_G_cluster.

## 11. Charged time

One 2-round target compression costs one unit, and every other primitive word operation, every load and every store included,
costs 1/430 of a unit. The rows below are in operations, loads and stores, called machine units here; 430 of them make one unit of
time.

*The machine.* The search is charged on the load/store machine of 6.5, and the selection procedure SEL of Section 12 counts
operations of the same cost model, with its 256-bit words, its packed lanes, its masked rotation and its charge of one unit for
every operation, load and store, with two changes: it has 64 registers in place of 16, and every constant is an immediate operand,
written in its instruction and not loaded. The cost model of the track charges primitive word operations and sets no register
count; this text charges as well a load for every other word fetched from memory into a register and a store for every word
written to memory, spills included. The batches of seven members, their E handlers and fills run on packed words (9.8); the
context, the shortcut of a passing lane, the joint solver and step 3 run on scalar words of the same machine, one 32-bit value to
a word. Every schedule of this section is an upper bound written out by blocks, after GPT Sol's answers AL 2, AQ 2, AR 3 and 6.2
to 6.6, AT 1 and 4, AW 2, 4 and 5, AX 1, CA, CD (sections 1, 3, 6, 8, 10 and 11), CF (sections 6 and 7), CI (section 1) and CJ
(sections 2 to 5), and not counts of an executed program, with these exceptions: the 67 units of a batch, which participant
programs executed with a count of every operation and load (9.8); and the omega side (17), PROR (5), the key (6), the carry word
(20), the gate tests (33, and 19 for four lanes), the byte guard (4), the descriptor selection (13, 11 for lane 0), the broadcasts
(16, 14 for lane 0), the chunk addressing (12 for the first chunk, which reuses n_0, and 14, or 8 when it is empty, for the
second), the lane tests (33 for seven lanes and 4 + 5 (n - 1) for n < 7), the omega sides and lane tests of the two chunks of a
cluster together (c(n_A) + c(n_B), at most 77, 9.9), the E lane (7, 6 for lane 0), the fill (56), the shortcut (39, 36 for lane
0), the pre-check (7), the preflight (6) and the additions to W (1) of this row, which a participant tool counted in the declared
program itself as it ran the public request and its self-test: every data word wrapped so that each operation, comparison, branch,
load and address that the program executes on it is counted, and the counts attributed to the program's own statements; every
occurrence equalled the declared count (our audit). The end jump of a chunk (9.9), a transfer of the written-out code, has no
statement in the program, whose chunks are a loop; it is charged in the 3 of an opened cluster and is not part of that count. The
54 of the Y9 path in a fill are the Y9 part of the executed Q path of answer CA, two of its lines fused into one (9.8).

**The cost, with every term.** Every row is machine units times an upper bound on how often a run executes it, except the four
rows of the counted events, which are charged together through the work register: their units add up to W <= WB + W_CTX (9.1), and
the table writes WB + W_CTX as the four products u_k (B_k + c_k), with c_k the most that one context adds to the count k (16,384
clusters, 2^19 lanes, 84,261 batches, 2^19 lanes). Each of these four products is a share of the joint bound, not a bound on its
own count. Exponents of counts and products are rounded up.

| Row | Charged count over a run | Units | log2 of the product |
| --- | --- | ---: | ---: |
| context (9.8, 9.9): drawing the fresh word, the 39 context lines on scalar words, preparing the sixteen packed operands, K, K', S15' and X9' included, storing the names for steps 2 and 3, S2, w5 and w12, the three registers of the shortcut, the gate base, the test of W, the context loop (bound in words, 541, charged 547); the four flags of the gate (160); the descriptor table of the masked walk (50,000), the carry word of every representative batch (20 * 2,341), its setup (16) and 128 fallback premiums of 117 | RUN_CONTEXTS + 1 = 2^50.115 | 112,519 | 66.895 |
| representative batch (9.9): the pair (3), the omega side (17), the key of every lane (6) and seven gate tests that each load the gate table once (33), 59; the last of a context, with four lanes, 45 | 2,341 * RUN_CONTEXTS = 2^61.307, RUN_CONTEXTS of them last | 59 or 45 | 67.190 |
| opened cluster (9.9): the representative's T2' test (5), W and the end jumps of the two chunks (3), the descriptor selection (13), the byte guard (4), the broadcasts (16), the omega sides and lane tests of the two chunks (at most 77) and their addressing (12 + 14); a fallback cluster 257 + 4, of which the context pays 117 | A_BUDGET + 16,384, through W | 144 | 69.986 |
| E lane, a lane whose mask of (2) meets S (9.8): W (1), isolating 2^34 + Y9 from the cached Y9 (2), loading T1 (1), combining the two masks and branching (3) | E_BUDGET + 2^19, through W | 7 | 67.723 |
| fill, once per batch with an E lane (9.8): C0.a1 and D0.d1 rebuilt (2) and the 17 Y9-path lines in 16 packed lines (54); its W addition is that of its E lane | G_BUDGET + 84,261, through W | 56 | 69.528 |
| passing lane: W (1), the shortcut of 9.6 (39), the pre-check of 9.7 (7) and, when T is not zero, the preflight (6) (written out, 53) | PASS_BUDGET + 2^19, through W | 53 | 64.865 |
| outer step that reaches the solver: joint solver of 9.4 with (G7) and (G15), then the certificate of step 3 on each root, under the meter of 9.7; its metered debit V = U <= CM(T) (Lemma ME) | total debits at most CREDIT = 2^69.491 | V <= 15,296 | 69.491 |
| one-time work: the direct tables T1, T2 (2^38) and the replicas of T2 in T2' (2^36) of 9.8, the member lists (2^26 + 2^20), the table P (2^27) and the allowance of 2^41 of the earlier two-borrow gate, kept, the gate table (2^34) and the masked walk's certificate, constant tables and layout generator (2^28 + 2^20) of 9.9; static rows with their descriptors (2^20); four allowances of 2^26, for the filter's automata, the three transition arrays, the code of the search, and row metadata with CT, array bases and initialisation; the reserve of 2^50 for exact histograms, model means and CT; 40 for resident constants and the final halt test; twelve allowances of 2^20 of the earlier layout (the E count in a register, the root certificate, (G15), the global ledger, the labels and frame of the gate, the representative's T2 on opening, the list pairs, the block of P, the frame of 9.9, the constants of the budgets, the credit, the run and the opening bound); three of 2^20 for the credit bound, the meter with CT and the cache; fourteen of 2^20 for the layout of the earlier row; two of 2^22 for the inline partner blocks and passing lanes; 2^38 for writing out the representative loop; and 2^34 for the certificate of Lemma OR | once | 1,128,752,545,267,752 | 50.004 |
| **total** | | | **71.540** |

In exact integers the sum of the rows is 112,519 * (RUN_CONTEXTS + 1) + 138,105 * RUN_CONTEXTS + 144 * (A_BUDGET + 16,384) + 7 *
(E_BUDGET + 2^19) + 56 * (G_BUDGET + 84,261) + 53 * (PASS_BUDGET + 2^19) + CREDIT + 2^38 + 2^26 + 2^20 + 2^20 + 4 * 2^26 + 2^50 +
40 + 12 * 2^20 + 2^27 + 2^34 + 3 * 2^20 + 14 * 2^20 + 2^36 + 2 * 2^22 + 2^38 + 2^41 + 2^34 + 2^28 + 2^20 =
137,150,669,488,596,985,144 + 168,337,731,491,771,799,375 + 1,168,517,254,413,134,797,632 + 243,433,090,603,453,661,778 +
850,917,555,121,445,528,808 + 33,589,842,598,613,164,283 + 829,308,674,569,081,960,042 + 1,128,752,545,267,752 =
3,431,255,947,038,643,164,814 machine units, where 138,105 = 59 * 2,341 - 14 and the four counted rows add up to WB + W_CTX =
2,296,457,742,736,608,617,309 + 38,535,192.

*Why the four counted rows are charged WB + W_CTX, and the credit once (our audit).* W is the sum of the units of the opened
clusters, E lanes, fills and passing lanes so far, each added by one instruction at the start of its stage. A context starts only
when W <= WB, and a context has at most 16,384 clusters, 2^19 lanes that can be E lanes or pass and 84,261 batches that can be
filled, so W <= WB + W_CTX whenever the run halts or ends (9.1). An outer step that runs steps 2 and 3 is metered: it starts only
when the credit left covers its CM(T), and its debit V is the work U that it executes, at most CM(T) (Lemma ME), so over the run
their work is at most CREDIT and the credit never goes below zero; an outer step whose CM(T) is larger than the credit left halts
the run before steps 2 and 3, and that test sits inside the 53 of its lane (GPT Sol, answer CK3 2). Contexts and representative
batches have no budget: a run has at most RUN_CONTEXTS contexts, each with 2,340 full representative batches and one of four
lanes, and the context row charges one more context, the one whose test of W halts the run. A context that halts before its last
batch costs no more than a complete one (GPT Sol, answer CD 3).

*A context, 112,519* (9.8, 9.9; GPT Sol, answers CD 1, CI 1.5, D13, D14 and D18; our audit), bound in words. Allowances: 16 to
draw the fresh word and split off the seven outer words; 158 for the 39 context lines on scalar words (20 lines contain a rotation
at five units and at most one more operation, the other 19 at most two operations; a direct schedule needs 139); 24 to form the
sixteen packed operands, K, K' and S15' among them, which need at most 24; 128 to copy them into seven lanes, at most 8 per
operand; 128 to save up to 64 scalar names for steps 2 and 3; 16 for the context loop; 40 for the gate base of 9.9 with its masks,
its copy into seven lanes, A[8..15] and its stored metadata; 1 for X9' = X9 + 2^34 in the packed copy of X9; 6 to form X2 + w7 and
store it with its address; 2 for the test of W against the immediate WB and its branch; 16 for S2, w5 and w12 (5 + 2 + 3) and
their stores with addresses; and 6 to load S6, X14 and X2 + w7 into their registers. These add up to 541, charged 547. The gate
adds 160 for its four flags hbad_i, Hbad and BG6 (at most 132, 9.9), and the masked walk 50,000 for the descriptor table (9.9), 20
for the carry word of each of the 2,341 representative batches, 16 for its setup and 128 * (261 - 144) for the premiums of at most
128 fallback clusters (Lemma XF (e)): 547 + 111,972 = 112,519. The context leaves W as it is: W runs over the whole run.

*A partner batch or chunk, 50* (9.8; GPT Sol, answers CA, CD 1, CJ 3 and D9; our audit), identical in every batch of seven lanes:
17 for the omega side, the six folded lines and omega (two rotations at five units, each followed by an XOR, 12, and 5 single
operations); 33 for the seven lane tests (5 per lane: the shift, the AND with 2^36 - 1, the load at the address that the result
is, the comparison and the branch; 4 for lane 0, which needs no shift, and for lane 6, which needs no AND): 50. Its pair, two
loads and the increments of the address, is paid by the opening of its cluster, and a chunk forms its U and E from the descriptor
(9.9). The fifth old partner batch of a cluster has three used lanes: 17 + 14 = 31, and a chunk of n < 7 lanes 17 + 4 + 5 (n - 1)
< 50. The participant's simulation of 9.8 executed and counted 67 units in every one of its 142,858 batches, with the two list
words loaded apart and the lane tests and omega side of the earlier layout. No slack is added, and none is needed: the dispatch to
an E handler is the fall-through of its lane test, every other transfer is a branch of a lane test, an E handler or a pre-check,
the return of steps 2 and 3 or the jump at the end of a chunk (9.9), and the code is written out. At most 62 registers are live
and nothing is spilled (9.8).

*A representative batch, 59, and an opened cluster, 144* (9.9; GPT Sol, answers CI 1.5, CJ 2 to 5, D13, D14, D16 and D18;
Grok, job 58; our audit). A representative batch has no lane test on T2': 3 for the pair; 17 for the omega side; the key of
its lanes, six packed operations (the ANDs of om, Y0 and E with their masks and three ORs, the last with the gate base BG6,
no shift); and seven gate tests, each the key of its lane taken out by a shift and an AND, the entry loaded at that address,
compared and branched on, 5 units, 4 for lane 0, which needs no shift, and for lane 6, which needs no AND: 33; its list
addresses are immediates of the written-out loop. In all 59. The last representative batch of a context has four used lanes:
3 + 17 + 6 + 19 = 45. A run has 2,341 representative batches per context, so this row is (59 * 2,341 - 14) * RUN_CONTEXTS =
138,105 * RUN_CONTEXTS. An opened cluster costs at most 5 for the representative's T2' load and test; 3 for W and the jumps
at the ends of its two chunks; 13 for the descriptor selection, 4 for the byte guard and 16 for the broadcasts; at most 77
for the omega sides and lane tests of its two chunks, c(n_A) + c(n_B) with c(n) = 16 + 5 n for n < 7 and c(7) = 50, n_A, n_B
<= 7 and n_A + n_B <= 9 (Lemma XF); and 12 + 14 for their addressing (9.9): 5 + 3 + 13 + 4 + 16 + 77 + 12 + 14 = 144. A
fallback cluster costs 5 + 21 + 4 * 50 + 31 + 4 = 261, 21 for W, the address and the ten loads and nine increments of the old
partner pairs, of which W pays 144 and the context 117. Nothing else is needed, since its code is written out at the
representative's lane site, the branch of the gate test skips it and its end falls through to the next gate test. E lanes,
fills and passing lanes of the representative and of the partners are charged in their own rows.

*An E lane, 7, and a fill, 56* (9.8; GPT Sol, answers CA, CD 1, 6 and 8.1 and CM 5A; our audit). An E lane, a lane whose mask of
(2) is not zero, pays 1 to add u_E to W, an addition with an immediate; 2 to isolate 2^34 + Y9 from the cached Y9 (a shift and an
AND with 2^34 + M; lane 0 needs no shift); 1 to load T1 at that address; and 3 to combine the masks, compare and branch: 7. The
first E lane of a batch adds u_E + u_G in that one addition instead and pays 2 to rebuild C0a1 and D0d1 and 54 for the 17 Y9-path
lines in 16 packed lines (seven rotations at five units, each next to an XOR, 42, and 12 single operations, two of them for the
fused line (X12 XOR M) + K): 56. The not-ready chain of the code of a batch (9.8) makes the choice between the fill and the cached
Y9 a position in the code, with no test. The simulation of 9.8 executed 78 units in every one of its 54,067 Q paths in the form of
answer CA, with an allowance of 16 for the E count and 55 for the lines. A lane whose mask of (2) is zero cannot pass and pays
neither (Lemma MB).

*A passing lane, 53 outside steps 2 and 3* (GPT Sol, answers AQ 2, AW 2 and 5, CD 3, CI 1.5 and D9; our audit): 1 to add u_P to W;
39 for e1, C2.a1, C2.d1, C2.c1, C2.b1 and the word r' by the shortcut of 9.6 (36 for lane 0); 7 for the pre-check of 9.7; and 6
for the preflight of 9.7, the address and load of CT[T], A(T) and CM(T) taken out, the comparison with the credit register and the
branch: 53, paid by every passing lane, also when T is empty. The lane is written inline after its E handler and keeps no return
link; the call and return edges of steps 2 and 3 are inside the global ledger (below). W and the credit stay in their registers,
and the global ledger saves the live words of the batch around steps 2 and 3.

*Steps 2 and 3: CM(T), at most 15,296.* Each outer step that reaches the solver is charged block by block, every block an upper
bound on its operations, loads and stores, with addresses, branches, spills and the restoration of registers included (GPT Sol,
answers AL 2, AR 3, AR 6.3 to 6.5, AT 1, AW 2, AX 1.1, CF 6.5 and 7.2 and CD 11.2):

- 736 once for an outer step whose T is not zero, the global ledger below; none when T is zero, since then no part of steps 2 and
  3 runs.
- 2,304 for each family (9.4): at most 128 blocks of the formulas of (a) to (e) of 9.4, the phase checks, (P*) and their
  preparation, at 12 units each, 1,536 (the 112 blocks of the formulas of answer AI 2 and 16 more; a block is the extraction of
  one source bit, a majority of four operations, an XOR of at most five inputs, the comparison or choice of a carry prescription,
  or a carry update, with its branch and assignment); the walks of bits 0 to 5 under the two guesses, at most 32 units a bit, 384;
  and 384 for the record of the family, which at most two rows of a set share (64 to store a record of 32 words and 128 to load it
  twice), the packing of the guard planes and the dispatch.
- 1,408 for each searched row. Its 32 descriptors are built in 32 registers at 32 units each, 1,024 (seven fields vary with the
  outer step, Q[i], y[i], E[k], E'[k], kappa[k], kappa[k+1] and the value of a constant, at 4 operations each, and 4 for the
  static base, the shift of the key and the assignment); 128 for the walks of bit 6 under the two guesses (64), the patches of
  h[6], h[7], h[13] and h[26] (24), kappa and the consistency of bit 6 (8), and the dispatch of the row (32); the guard (G7) of
  9.7 adds 128 (answer AX 1.1), and the guard (G15) of 9.7 128 more for its five words (answer CF 7.2).
- 20 for each forced node: the key from the carry pair, the descriptor and the base of the array, and the read, 3; the validity,
  its comparison and the branch, 3; the next carry pair and the saved bit e2[29] (at position 9 the new bit is put in its place),
  3; the chosen bit of h, shifted to its place and ORed into the prefix, 3; the guard of position 25 or 29 written into the key,
  at most 5 (at 25, bit 13 of the prefix shifted and masked, XORed with h[6] XOR u, which is held, shifted and ORed into the key,
  5; at 29, the saved bit e2[29] masked, shifted and XORed into the key, 3; none at 31); and the continuation, 1: at most 18, 13
  at position 31. Its debit of the meter (9.7) is one more operation, and at position 31 the debit of its leaf one more.
- 4 more for each selected node, at position 20: bit 8 of the prefix as the desired bit of the key of the selected array.
- 64 more for each node at position 15: the test of (G15) and the prescription of h[15] in a temporary copy of the descriptor
  (9.7).
- 48 for each free node: the parent saved in one register, 2; the key and the read of the dual array, 3; the two arcs taken apart,
  2; 11 for each of the two children, for the validity, the carry pair and the saved bit, the prefix and the control; the parent
  restored before the second child, 2; and 5 for dispatch and return: 36, charged 48, and its debit of the meter one more
  operation. No guard reads a free position.
- 80 for each leaf: g, f, e2 and h2 of its h and (J1), (J2) and (J3) as words, a rotation at five operations, 64; and 16 to reload
  the context words: 80; its debit of the meter is made by its parent at position 31.
- 120 for each root: the certificate of step 3 (Lemma RC), run at the leaf of the root: Y14, Z, Y6, E1.a1, E1.d1 and c1, 22; the
  test (Q), 3; E1.b1, s, E1.a2, p and the test (A), 16; z and the test (C), 15; Y2, w0, K0.a1, t and the test (T), 17; twelve
  addressed loads, h, e1, C2.c1, C2.b1 twice, Y1, w12, Y12, w5, K0.d1, C2.a1 and C2.d1, 24; dispatch, return and control, 16: 113,
  charged 120, and its debit of the meter one more operation. A rotation on scalar words takes four units (two shifts, an OR and a
  mask), every sum is masked to 32 bits, and Y11, beta*, DY11, eps, IV[0] + IV[4] and the constants tau_j - beta* + 8 and
  ROR(tau_j, 8) of each row are immediates of the written code (answers CF 6.2 and 6.5).

*The global ledger, 736 (GPT Sol, answers CD 11.2 and D13).* This is a specified layout, not a count of a program. The lane of 9.8
has finished its paid pre-check and preflight when it calls steps 2 and 3, and it calls them only when T is not zero. So that a
lane with T = 0 stores nothing for the solver, steps 2 and 3 store the names that they read, as these become available, in a fixed
bank of 32 memory words, disjoint from the saved words of the batch, the family records and the words of (G15). The names are the
seven outer words of the context, reloaded; Q = Y9, the T1 address of the lane with the bit 2^34 removed (an AND); y = e1 - Y3; E
and e1 of the lane; C2.a1, C2.b1, C2.c1 and C2.d1 of the shortcut of 9.6; Y1 and Y12 taken out of their packed words of the batch
(a shift and an AND each); w5, w12 and K0.d1 of the context (9.8); E' and E XOR E'; and the two phase bits: 24 words, each stored
before its register is reused. No scalar rebuild of step CO runs for a call; the one rebuild of the found trial is inside the
once-only allowance of the root certificate (GPT Sol, answer D13). Every word of the bank that is read later was written in this
outer step, and no other word of it is read, so the bank needs no clearing. Every address is a fixed offset from an immediate
base, and every name of a word, register and row is written in the code; nothing is looked up by value. Once for a nonempty T:

| item | units, at most |
| --- | ---: |
| the source bank: Y1, Y12, y and Q from the words of the batch (7), and the addressed reloads of the seven outer words and E[b] (16) | 23 |
| up to 32 addressed stores of names into the bank, 2 each | 64 |
| E' = E + DY3, E XOR E', the phase fields, their normalisation and stores | 16 |
| loading sources at the boundaries of families and rows | 128 |
| the choice of outcomes and families from the fixed mask, and the top-level dispatch | 128 |
| entry into the frame, bookkeeping of bank slots and control, and the final return | 128 |
| saving at the entry and reloading before the return the live words of the batch, at most 58 (49 of the walk, W among them, and the nine words of the masked walk), at 4 units each with the addresses (our audit) | 232 |
| the meter's debit of A(T) | 1 |
| unused reserve | 16 |
| total | 736 |

The loads cover five source words for each family, at most three families, 30, and six context words for each row, at most three
rows, 36, with 62 to spare; the reloads of a leaf and the loads of (G7) and (G15) keep their own allowances above. The choice runs
a fixed decision tree over the six bits of T: six bit tests at 6 units each, three family entries and three row entries and exits
at 8 units each, and 16 for entry and exit, 100 in all. The last 128 pay the call and return edges, the preparation of the bank
base and offsets, and up to 32 further addressed accesses. Each root is certified at its leaf and a rejected root returns straight
into the traversal (step 3), so no list of roots is kept, allocated or sorted. Forming the first certified pair is in the
once-only allowance of the root certificate.

Summing the blocks: when an outer step reaches the solver with searched outcomes T, at most one row of each family reaches depth 7
(Lemma FX), so steps 2 and 3 cost at most CM(T) = 736 + 2,304 F + 1,408 A + the sum over the families of T of the largest tree of
their rows, 20 N_f + 48 N_r + 4 N_s + 64 N_15 + (80 + 120) Lf for its forced, free and selected nodes, nodes at position 15 and
leaves with (G7) and (G15) (9.4): 1,920 for a row with four leaves and 3,808 for a row with eight; roots are at most leaves, and
CT[T] of 9.7 holds CM(T). The four sets of rows of 9.4, restricted to the outcomes of S, contain every T that occurs, and give at
most 8,256 ({275}), 6,368 ({175}), 9,664 ({285, 385}) and 15,296 ({185, 385, 685}). So steps 2 and 3 cost at most 15,296 machine
units in every outer step that reaches them, whatever its words and whatever its T, which the pre-check never enlarges: 736 + 2 *
2,304 + 3 * 1,408 + 3,808 + 1,920 = 15,296 on the rows 185, 385 and 685 (GPT Sol, answers CF 7.2, CD 10, CD 11.3 and D12; GPT-6
Astra, Batch 17; the trees and the arithmetic recomputed by the participant). With the global part 1,024 of the earlier layout the
same sum is 15,584, the bound of U0 in Lemma CP. The counts are those of the static trees, and the blocks are added whether or not
they occur together, so this is an upper bound; it is not claimed to be attained or to be the least such bound.

*The meter and CM(T) (Lemma ME; GPT Sol, answers CD 11.3, CK3 2 and 3 and D12; our audit).* Every T that occurs lies inside a mask
X of Section 8 (T is X or empty), and each of the ten masks X lies inside one of the four sets of rows of 9.4, {275}, {175}, {285,
385} and {185, 385, 685}; the table lists every nonempty subset of these four sets, so every nonempty T that occurs. For each it
gives F, A(T) = 736 + 2,304 F + 1,408 r, the counts of forced, free and leaf blocks of the largest tree of each family (the roots
are at most the leaves) and CM(T):

| T | F | A(T) | n_f, n_d, n_l (= n_o) at most | CM(T) |
| --- | ---: | ---: | --- | ---: |
| 175 | 1 | 4,448 | 42, 3, 4 | 6,368 |
| 185 | 1 | 4,448 | 42, 3, 4 | 6,368 |
| 275 | 1 | 4,448 | 80, 7, 8 | 8,256 |
| 285 | 1 | 4,448 | 80, 7, 8 | 8,256 |
| 385 | 1 | 4,448 | 80, 7, 8 | 8,256 |
| 185, 385 | 1 | 5,856 | 80, 7, 8 | 9,664 |
| 285, 385 | 1 | 5,856 | 80, 7, 8 | 9,664 |
| 685 | 1 | 4,448 | 42, 3, 4 | 6,368 |
| 185, 685 | 2 | 8,160 | 84, 6, 8 | 12,000 |
| 385, 685 | 2 | 8,160 | 122, 10, 12 | 13,888 |
| 185, 385, 685 | 2 | 9,568 | 122, 10, 12 | 15,296 |

So CM(T) <= 15,296 for every T that occurs, with equality on 185, 385 and 685, and V = U in every call (9.7). The participant
recomputed the table in integers from the trees of 9.4. The meter needs no premise: its debits are the unit costs of the blocks
that a call executes, whatever its words.

*Registers of steps 2 and 3* (GPT Sol, answers AL 2, AR 3 and 6.3, CF 6.5 and 7.2). The search of 9.4 is written out statically
for each row and each prefix of free choices: a node at a prescribed position has at most one child, whose code follows that of
its parent, and a leaf label jumps to the leaf check; a node at a free position, at most five on a path, saves its parent in one
register, the prefix of h and, above bit 32, the two carries and the bit e2[29], the only earlier output bit that a later guard
reads (the guard of position 25 reads bit 13 of the prefix). The registers of the traversal are the 32 descriptors, five saved
parents, six context words, eight constants, array bases and control words, two words of the current state and ten temporaries: 63
of the 64; the 64th holds the remaining credit (9.7), and no other register holds a copy of it. A leaf keeps the descriptors and
the saved parents and uses the others for its check, after which the context words are reloaded (the 16 above). The certificate of
a root and the test of (G15) use only the ten temporaries. For the certificate, t is formed first; then the live values fit seven
temporaries in each phase: Y14 with at most four loaded words; Y6, E1.a1, E1.d1, c1, E1.b1, s and a loaded word; E1.a2, E1.d1, c1,
s, p and a test word; z, c1, two sums and z XOR ROR(tau_j, 8). One more temporary takes the shifted part of a rotation, which is
formed first so that a rotation may overwrite a source that dies, one holds an address and one a comparison. The prefix h is read
without overwriting the protected word of the current state. For (G15): the five words, an accumulator, the temporary descriptor,
a test word, an address and a prefix temporary. On both outcomes every other register of the traversal is kept as it was, with no
spill. The formulas of a family run before the descriptors are built, in at most 58 registers: at most 35 bits and carries, five
source and context words, eight table, literal and control words and ten temporaries. The stores into the bank of the global
ledger run before that, with the live words of the batch already saved, so the 63 registers other than the credit's are free for
them; the bank is memory, and only the five source words of a family are live when its formulas run (answer CD 11.2). No register
is addressed by a value: every position and register is named in the code.

*Once.* The direct tables T1 and T2 (Lemma DT) are charged 2^38, and the two further copies of T2 in T2' 2^36. The member lists of
9.9, in cluster order, are charged 2^26 + 2^20: for each of the 2^19 members, the deposit of its 19 bits at the free positions of
e1, at most 3 units a bit, 57; the subtraction of Y3 and the rotation by 7, at most 6; and for each of the two lists the shift of
the value to its lane and the OR into the packed word, 2, with the store of each packed word and its address, below 2 per member;
and the loop, 3: below 2^7 units per member, below 2^26 for the lists; and at most 64 units per cluster, 2^20 in all, to place its
representative and its five partner words. The six static rows of the outcomes of S, with the static fields of their descriptors
at the 32 positions and the metadata of the batches, are charged 2^20. 2^26 for the two automata of the filter for the seven
outcomes, built and composed into eight byte tables whose entries hold the base address of the next table, with the entries of the
last tables ANDed with S (GPT Sol, answers AN 2 and AQ 2): their states at each of the 32 bits are images of those of the
fourteen-outcome automata, at most 146, so the allowance of answer AN 2 covers them. 2^26 for the three transition arrays of 9.4:
their 2^18 entries at most 256 operations each, the enumeration of the keys, both candidate arcs, the test for an invalid or a
second arc, the selection and the store included (answer AR 6.2). 2^26 for writing the code of the search: 432 static nodes over
the six rows of S, with the prescribed bits of (G7) and (G15) at positions 7 and 15, fewer than 2^14 labels, at most 256
operations each with their set-up (answer AL 2). And 2^26 for the row metadata, the absolute bases of the arrays and their
initialisation, a fourth allowance that GPT Sol keeps for safety (answer AR 6.2), which also covers the enumeration of the
compatible patterns of 9.7 and the 128 words of CT, below 2^23 operations (answers AW 2 and 5). 2^50, the once-only reserve of GPT
Sol's answer AW 5 for the exact mask histograms, the model means and the table CT, charged in full whether or not it is used. 32
for loading the resident constants and array bases into their registers and 8 for the test of the final halt. 2^20 for each of
twelve parts of the earlier layout (answers CD 6, 8 and 11.2, CF 6.2 and 7.2, CI 1.5, CJ 2 to 5 and CK 3 to 5): the E count in a
register; the root certificate, with the immediates of the rows and at most 1,024 units to form the last blocks of the first
returned pair; (G15), with its unrolled code and the layout of its five words; the global ledger, with its bank and labels; the
labels of the gate; the representative's T2 test on opening; the pointer and end constants of the list pairs; the block P_q of P;
the frame of 9.9; and the constants of the budgets and the credit, of the run and of the opening bound. 2^27 for the table P of
the earlier gate, kept: for each of its 2^21 keys at most 64 units, to take the key apart, form the two sums, compare them with
the ends of the two intervals of S7 and branch, store the entry and loop; and 2^41 for the folded table of the earlier two-borrow
gate, its 2^35 entries at most 64 units each, an allowance kept in this row although that table is no longer used. Three more of
2^20 (answers CK2 1, CK3 2 and 4 and CM 5A): the constants of the credit bound; the meter, with the packed words of CT, the
immediates of the block debits and the preflight; and the cache with its fill code. Fourteen more of 2^20 for the layout of this
row (our audit): the frame of 9.9 in registers (three), the save of the batch words in the global ledger, the guard words from its
bank, the pass count in a register, the credit in its register, the pre-check with immediates, the shortcut of 9.6, X9' with T1 at
2^34, the gate base in the key, the interleaved lists, W with its test, and the meter without slack. Two of 2^22 for the code of
the opened clusters written out at the representative lane sites and of the passing lanes written out after their E handlers, and
2^38 for writing out the representative loop with them: fewer than 2^32 instructions (Section 12) at most 2^6 units each. And 2^34
for the finite checks of Lemma OR (9.9), an allowance kept although the 128 residues of (b) and the 65,536 pairs of (d) need far
less. The gate table of 9.9, its 2^30 entries at most 8 units each, its 2^22 prefixes at 32 and 4,096 for the flags and constants,
8,724,156,416 units, is charged 2^34 (GPT Sol, answer D16). And 2^28 + 2^20 for the masked partner walk (GPT Sol, answer D14 3):
2^28 for its finite certificate alive16 and its constant tables, PX among them, and 2^20 for its layout generator and metadata.

*One-time items.* The items above are in the last row. The final step, once: steps CT and CS for the trial found, writing the two
messages, shorter than 2^42 bytes each, and two complete evaluations of blake3; each message has at most 2^32 chunks of 16
compressions each and fewer than 2^32 parent compressions, below 2^37.1 compressions for both, and writing them is below 2^38
machine units: below 2^38 units of time in all. Preprocessing: the selection procedure SEL of Section 12, charged in full at its
cap by construction, S_old = 5,486,510,246,044,225,536 machine units, below 2^53.503 units of time.

Total:

    T <= (sum of the rows) / 430 + 2^38 + S_old / 430
      <  2^62.7934.

In exact arithmetic the numerator is 3,431,255,947,038,643,164,814 + S_old = 3,431,255,947,038,643,164,814 +
5,486,510,246,044,225,536 = 3,436,742,457,284,687,390,350 machine units, T = 3,436,742,457,284,687,390,350 / 430 + 2^38 =
7,992,424,594,144,621,805.3 units, and log2 T = 62.79333893569689...; in integers, with 430 T = 3,436,742,575,482,187,376,270 a
whole number, (430 T)^10000 < 2^627934 * 430^10000 and (430 T)^10000 >= 2^627933 * 430^10000. The claimed time_log2 is 62.7934,
this total rounded up at the fourth decimal. The search part alone, that is the rows and the final step without SEL, is
2^62.79103393733518...; S_old / 430 is 2^-9.289 times the search part and adds 0.00230 to log2 T. The bound holds in the worst
case for the algorithm as stated: every run halts with its four counted events within WB + W_CTX, within its credit and within its
RUN_CONTEXTS contexts, steps 2 and 3 are bounded in every outer step that reaches them, and SEL is bounded by its caps. No mean of
a count of work enters it, since CREDIT is a fixed number enforced by a halt; H1', H4', H5_exec, H_G_cluster and Lemma OR bear on
the success probability only. The claim rests on this 64-register schedule: no figure for 16 registers is claimed, and this
schedule is not claimed to be the cheapest.

Nothing is sorted and nothing is looked up by value: each root is tested against the conditions of its own outcome, and no
certified trial is compared with another. The reads at positions that words give are: per batch, the words U[b] and E[b]; per used
lane of a partner batch or chunk, the entry of T2' at its omega, and in a representative batch the entry of the gate table at its
key; per opened cluster that is not a fallback, PX at its omega prefix and the words n_0, n_1, JU and JE of its descriptor; per E
lane, the entry of T1 at its Y9; per opened cluster, the T2' entry of its representative; per passing outer step, the three names
stored for the shortcut and, when T is not zero, CT[T]; in an outer step that reaches the solver, the names saved for its context
and the bank, the transition arrays at the keys of the searched rows, the five words of (G15) of each searched row, the family
records and the static rows of the outcomes. Every such read is charged as one load: a partner batch counts its 7 loads of T2'
inside its 50 units, the opening of its cluster the 10 loads of its partner pairs or the loads of PX and of the descriptor, a
representative batch its 2 list loads and 7 loads of the gate table inside its 59, an E lane its load of T1 inside its 7, and the
loads of a context, of a passing lane, of the joint solver and of step 3 are inside the allowances above. No table grows with the
trials.

## 12. Memory, preprocessing and advice

The program of the search is the lines of steps CO, CT and CS, the outer filter, the walk of 9.8 and 9.9, written out over the
2,341 representative batches with the code of an opened cluster at each representative lane site and the passing lanes inline,
the joint solver of 9.4 with its statically written traversal and the guards (G7) and (G15), and a compression routine for step 3
and the final check. Its size (our audit): a lane site has fewer than 2^7 instructions, its lane test 5, its E handler with the
fill 63, its passing lane 53 and the call of steps 2 and 3; a batch of n lanes, a not-ready chain of n lane sites with a ready
tail after each, has n (n + 1) / 2 lane sites, at most 28, and its omega side; an opened cluster, its five old batches with 4 *
28 + 6 = 118 lane sites and, for each of its two chunks, the seven dispatch leaves for n = 1 to 7 with 1 + 3 + 6 + 10 + 15 + 21 +
28 = 84 lane sites, 286 in all, with its omega sides, selection, guard, broadcasts and dispatch, fewer than 37,200 instructions;
a representative batch, at most 28 representative lane sites each with that code, fewer than 2^20; the 2,341 representative
batches and the rest of the program, fewer than 2^32 instructions, below 2^37 bytes at 32 bytes an instruction. Data, one word of
256 bits each unless said otherwise, at fixed word addresses: T2' at 0 to 3 * 2^32 - 1, T1 at 2^34 to 2^34 + 2^32 - 1 and the
gate table at 2^35 to 2^35 + 2^30 - 1 (9.8, 9.9), 2^34 + 2^30 words, with nothing else in the band 2^35 to 2^36 - 1; and above
2^36 the member lists, 168,522 words; the table P of the earlier gate, 2^21 words; the 29,952 entries of the tables of the
filter's two automata; the three transition arrays of 9.4, 2^18 words of 32 bits; fewer than 4,096 words for the joint solver
(the descriptors of the positions of a row, the six static descriptors of S, the records of the families, the bank of 32 words of
Section 11 and scratch); fewer than 1,024 words for the names of step CO, the stored names of a context, the saved words of a
batch, the five words of (G15) of each row, the constants and masks, the 128 words of CT and the cells of step 3; and in the last
2^13 words below 2^36 + 2^24, from DB = 2^36 + 2^24 - 2^13, the descriptor table of a context, 1,024 words, and PX, 512 words:
all below word address 2^36 + 2^24, below 2^41 + 2^29 bytes. The memory of the search is therefore below 2^41 + 2^29 + 2^37 <
2^42 bytes. Nothing grows with the number of trials. The two messages of a found pair have 1024 t + 55 and 1024 t + 63 bytes with
t < 2^32, each shorter than 2^42 bytes; the output, the two messages with their digests, takes less than 2^43 bytes.

**The advice record.** The search reads a fixed record, stated here in full, which this package treats as nonuniform advice: the
six constants X3 = 29d4fa98, X7 = bee3af28, X11 = 44036000, X15 = 40c58500, W4 = 97475638 and W13 = 0007c006 of 3.2, 24 bytes; eta
= 830303cf, 4 bytes; beta* = 18b0e098 with the mask 0e09818b and the value 02008000 of its cube, 12 bytes; the seven values of tau
of the filter's automata, 175020a0, 185020a0, 275020a0, 285020a0, 385020a0, 675020a0 and 685020a0, and eps = 6e21be55, 32 bytes;
and the mask 5f of S, 1 byte: 73 bytes, so nonuniform_advice_log2_bytes = 7.

The success analysis of 10.3 and 10.4 uses only properties of this stated record, and this text verifies each of them exactly,
whatever the way the record was found: Fact P, the equal d and b outputs of C3 for W4 and W4' (3.2); Lemma Q, the class of eta
with exactly 524,288 members; Theorem C (iii) and (iv), by which c1 gives the difference beta* exactly when c1 AND 0e09818b =
02008000; the fourteen outcomes of beta* on the class, all with eps = 6e21be55, and the count 67,633,152 = 1,032 * 2^16 of the six
of S (10.1, with the program of Section 17); the certificate of the filter for S, with SHARE and E_COUNT (Section 8); and, for the
search itself, the allowed patterns of the pre-check (9.7) and the guards, trees and caps of the joint solver for this class and S
(9.4, Lemmas J0, G7 and G15, Section 11). H1', H4', H5_exec and H_G_cluster are stated for this record (10.3). Nothing in the
success analysis depends on how the record was found, on a selection returning it, or on any record of the runs that found it.

**The selection procedure SEL.** The advice record was found by a solver search and one count per model, which the submitted
program does not contain. This section writes that search as a procedure, SEL, and charges its whole cost as preprocessing,
included in T (Section 11). The cost model charges any search omitted from the submitted program; SEL is that search, and its
whole capped cost is charged. The charge is a bound by construction: every search of SEL runs over a range stated here, and every
run of a program in SEL halts as soon as it has executed a stated number of primitive word operations, its cap, or holds 2^34
bytes; a run that halts so returns nothing, and SEL goes on. Operations are counted as in Section 11, 430 to the unit. SEL runs
two programs of the participant that are not in the package: the solver kissat, on instances made by a generator of the
participant, and the counter of Section 13, which computes in integer arithmetic the part of one beta in the rate of the class of
a given eta, with no rule on h1; a run of the counter whose part would be 2^192 or more counts as one that reaches its cap.

*Step 1, the pinned call (solver runs).* For each of the 116 runs of the participant's solver log for this search (51 runs for the
lengths 55 and 63, the other 65 for nine other variants of the instance; bounds 97 to 118; logged seeds), build the instance of
the run and run kissat on it with the logged seed, the two together with a cap of 5 * 2^53 operations. For the lengths 55 and 63
the instance is that of entry c66f230d (its Section 10): the call C3 for both messages with equal b and d outputs, the two words
w4 related as the length cancellation prescribes for the XOR 8 of the lengths, the top byte of word 13 zero, E1 and E3 for both
messages, a zero residual, and a bound on the number of bit positions, bit 31 excepted, at which a difference is active in six
additions of E1 and E3. A run that finds a model returns six constants X3, X7, X11, X15, W4, W13 and the values of a solution,
among them its Y4 and its beta. Cost: at most 116 * 5 * 2^53 < 2^62.18 operations.

*Step 2, the constants, the class and beta* (a count for each model).* For each model of step 1, compute Y3 and Y3' by C3 from its
constants, its class eta = ROR((Y3 + Y4) XOR (Y3' + Y4), 16) from the Y4 of its solution and its beta from the c1 of its solution,
and with the counter the part of that beta in the rate of the class of that eta, with a cap of 2^51. Output the six constants, the
eta and the beta of the model with the largest part, the first in the order of the log if parts are equal. Cost: at most 116 *
(2^51 + 2^10) < 2^57.86 operations.

*Step 3, the cube, the outcomes and S.* With DY11 = Y11' - Y11 for the output of step 2, form the mask ROL(beta, 12) AND 7fffffff
and the value (ROL(beta, 12) - DY11) / 2 of the cube of the words c1 that give beta (proof of Theorem C (iv)), and the outcomes
(tau, eps) of beta whose product L * N3 is not zero, which the count of step 2 lists; for beta* these are the fourteen of 10.1.
Then, for each of the 16,383 nonempty sets S of these outcomes, compute in integers the numerator O(S) of the ledger under which S
was chosen, that of entry 415e792c: O(S) = 424 * RUN_BATCHES + 35 * (E_BUDGET + 1) + 512 * (PASS_BUDGET + 1) + CREDIT +
1,125,900,176,326,712, with its count from the rows of step 2, its FACTOR, RUN_STEPS and RUN_BATCHES = ceil(RUN_STEPS / 7), its
E_COUNT and SHARE from the mask certificates of the two automata of the outcomes, its two budgets, its table CT of the caps
without (G7), 4,096 + 2,304 F + 1,152 A + 20 N_f + 48 N_r + 4 N_s + 368 Lf over the trees without (G7) of 9.4, their mean cbar_S
over the masks of these certificates and the eight values of nu (10.3), and its credit at 1.06 times cbar_S. Output the S with the
least O(S), the first in increasing order of its mask if two are equal, and the outcomes whose tau has bit 14 equal to 0, from
which the outer filter's automata are built. Step 3 and the bookkeeping of SEL run under a cap of 2^50 operations.

**The bound.** Steps 1 to 3 cost at most

    S_old = 116 * 5 * 2^53 + 116 * (2^51 + 2^10) + 2^50 = 5,486,510,246,044,225,536

operations, below 2^62.251 (in integers S_old^1000 < 2^62251), and so below 2^(62.251 - 8.748) < 2^53.503 units (S_old^1000 <
430^1000 * 2^53503). preprocessing_log2 = 54 is this bound rounded up to a whole number, and the whole of S_old is in T (Section
11). It bounds SEL as defined, whatever the two programs do inside and whatever they return, because every run halts at its cap
and every loop has the range stated. SEL is not a premise of this package, and no heuristic is declared for it.

*What rests on records.* The bound rests on no record. That SEL returns exactly the six constants of 3.2, eta = 830303cf, beta* =
18b0e098 and S = 5f rests on the participant's records: for S, on GPT Sol's exact comparison of the 16,383 sets (answers AW 4 and
5); for the rest, on the participant's solver log, by which the run for the lengths 55 and 63 with bound 104 and seed 506 found
these constants after 4,770 seconds, with a solution of class 830303cf and beta 18b0e098, and on an exact integer recount, by the
participant's counter on the whole class of each instance, of all 65 distinct instances that the runs of the log returned with a
model, in which these constants have the part 71,698,432, the largest, and the next is 13,107,200 (a strict maximum, 5.47 times
the next). Every run of the log stopped within 9,010.5 seconds on one processor core and every recount within 320 seconds; at 2^42
operations a second for a core, a rate the participant states and does not prove, every run stayed below 2^55.14 operations and
every recount below 2^50.33, inside the caps. The log does not fix every instance: some runs excluded pairs that runs finished
before them had found, and 32 runs were stopped from outside without a record of the cause. So the records certify a historical
run of the solver, not a replay with operation caps, and the generator of the instances, the solver log and the counter are not in
the package. If a record were wrong, SEL could return other constants or none; its cost would stay within the bound.

*Memory of SEL.* Every program run of SEL halts when it holds 2^34 bytes, and SEL runs one program at a time; its own data stay
below 2^20 bytes, the parts of step 2 and the outputs. SEL therefore holds fewer than 2^34 + 2^20 bytes at any time; the search
fewer than 2^42 bytes, its tables and code included; the output fewer than 2^43 bytes. Held at once, these total below 2^43 +
2^42 + 2^35 < 2^44: memory_log2_bytes = 44 bounds all. The measurements of Section 13 are not part of SEL: they test the
heuristics and select nothing. The cost model does not score memory.

The direct tables, the gate table and the member lists, like the descriptor tables, PX, the tables of the filter's automata, CT,
the three transition arrays, the descriptors and the traversal, are not advice: they are computed from the record. SHARE and
E_COUNT are counts from the certificate of Section 8, the metered caps of CT are computed from the trees, and the budgets and the
credit of 9.1 are computed from them, from u_M, from the bound 12,466 of H_G_cluster, from the factor 1.01 of H5_exec and from the
other constants of 9.1. The flags 3 and the counter rule are part of the algorithm. There is no other stored data and no stored
collision.

## 13. Evidence, scope and field meanings

Throughout this text costs and bounds are rounded up, and margins, rooms and the whole numbers of the count that the claim uses
are rounded down. Counts printed with decimals are rounded to the nearest.

**What is exact.** Sections 2 to 5, 7 and 8; Lemmas L, H, Q, Q2, T, T2, N, TR, CT, IP, F, J0, V, RC, VP, G7, G15, CV, FX, CP, Y,
CX, DT, MB, KP, A9, CL, XF, OR and ME and Theorem C; the count of passing pairs of Section 8 and the allowed patterns of the
pre-check and the table CT of the metered caps (9.7); the parity certificate (P*), an exact count, and the constants and caps of
the joint solver (9.4) with its schedule (Section 11), as upper bounds, with the meter's debit equal to the ledger; the flat mean
1383624064/266237 of model M, recounted in integers; and Lemmas S1 to S5, S8 and S9 under their stated hypotheses. The tree part
22422672/266237 of u_M is GPT-6 Astra's bound in model M, cited and not proved in this text; H5_exec declares the number u_M
itself, so neither the time bound nor the statement of the premise depends on that proof. The declared experiment
`frontline-search` executes the search of 9.1 on one context per organizer seed (9.2) and returns a pair of the root instance of
the same lines, whose two digests the organizer recomputes; Theorem C predicts that every pair agrees on the 128 masked digest
bits (6.4). The counter instance itself has no organizer-run digest check (6.4).

*How it was checked.* The participant's checks are computations, not proofs: the counter construction against the organizer's own
functions on 2,000 trials, with 204,000 internal words compared with a separately written forward computation, and complete
messages hashed by the organizer's code (Section 7); the declared program's in-run references and self-test (9.2, 9.3); all 2^21
members of Q*, each giving the difference beta*; the rule t != 0 (Section 8); the free positions, static trees, families and caps
of the solver, and the sums of the cells of (P*) against the counts of 10.1, with a separate count of (P*) in one phase of 2^16
members (9.4); the word nu of the pre-check against the bits s[13] to s[15] of 324,098 real trials (9.7); and the two lists of
Lemma Y, the member lines and the pass decisions of the member loop and of the omega-first batch against the full outer step, with
every operation of the batch counted (9.8); and the finite checks of Lemmas A9, CL, XF and OR, with Lemma KP, the gate and the
window arithmetic of Lemma XF against the word equations on random clusters and context words (9.9). For Sections 1 to 6, three
independent reruns found no wrong value in the displays, Table C and Lemmas Q, Q2, L and T2. No person has read any part of this
text.

**The seven-word model.** By 6.2 the residual of a trial, of the root instance or of the counter instance, is a function of the
constants and of seven 32-bit words: for E1 its first-half values d1 and b1 and its a output a2 on message A, and for E3 the words
Y4, Y9, w8 and its first-half value h1 on A. The model M says that over the trials the six words other than Y4 behave like
independent uniform words, independent of Y4, which is uniform in the sub-class. Under M a trial has R = 0 with probability r *
2^-128, where r * 2^81 is the number of solutions of R = 0 among the 2^209 values of the seven words with Y4 in the sub-class.
Call r the *rate of the sub-class*. Rule A is a condition on h1, so under M the trials with R = 0 that satisfy rule A have a rate
of the same kind, r_A, counting only the solutions that satisfy rule A; r_A is at most r. The counter search prescribes c1 = Y11 +
d1 in Q*, and under M that is a conditioning on d1 (Lemma S1); its rate p is formed from the part of beta* in r (10.1). On the
outer steps that pass the filter of Section 8 the rate under M is p / pi, and no part of p lies on the others (Lemma S9). M and
the count give the rate of a single trial. They do not give the probability that a run has a good trial, which also depends on how
the good trials of a run cluster; a model of the single trial says nothing about that.

Given M, the rates are properties of the constants, the sub-class and beta* alone and can be counted without sampling; the count
says nothing about whether M holds. The six words are not free in a trial. In the counter search Y4, Y9 and w8 are fixed for the
2^21 trials of an outer step, and so are Y12 and w5, which E1 reads; the trials of an outer step differ in d1 and in what follows
from it (Lemma CT (c)), and E1.b1, E1.a2 and E3.h1 move with d1. M is a statement about averages over the outer steps of a run.
Lemmas S2 to S4 show which parts of it hold exactly for the construction, and H1' declares the rest. The measurements below show
where M fails inside one context and inside one outer step.

**How r is counted (participant computation, not organizer-verified).** Write tau, eps, beta for the XOR differences between A
and B of E1's a output, c output and first-half b, and eta, psi, tau', eps' for those of E3's first-half d and b and its c and a
outputs. Because E1's a1 and d1 are the same for A and B, R = 0 holds exactly when tau' = tau, eps' = eps, psi = tau XOR
ROR(tau, 1) and eta = eps XOR ROL(beta XOR eps, 1); for Y4 in the class the left side of the last equation is the constant
830303cf. The counter works in integers (128-bit unsigned integers; exact fractions for the products and sums), has no sampling
branch, and needed no fallback on any outcome of the count below; no floating-point number is on the path of a figure printed
below as a fraction.

1. *The betas.* beta is a function of d1 alone: with c1 = Y11 + d1 and DY11 = Y11' - Y11 = 0a08818b, beta = ROR(c1 XOR (c1 +
   DY11), 12). As in Lemma Q, the d1 with a given beta are a share 2^-k of all d1, k being the number of bits of the mask
   ROL(beta,12) AND 7fffffff.
2. *The outcomes of one beta.* An outcome is a pair (tau, eps); the admissible tau are enumerated with a carry automaton, with no
   bound on the weight of tau. A beta for which beta XOR ROR(eta, 1) has odd weight contributes nothing; every other has two
   candidates for eps.
3. *The E3 side.* N3 is the number of quadruples (Y4, h1, Y9, w8) for which E3 produces eta, psi, eps and tau; all of them have Y4
   in the class.
4. *The E1 side.* P1 is the probability that E1 produces tau and eps when d1 is uniform among the values with this beta and b1 and
   a2 are uniform.
5. *The sum.* For the sub-class, N3 counts only the quadruples with Y4 in the sub-class, and the part of a beta in r is 2^(15 - k)
   times the sum over its outcomes of P1 * N3, where 15 is the number of bits that Lemma Q2 fixes, so that the sub-class is a
   share 2^-15 of all Y4: the sum of N3 over all 2^96 values of (d1, b1, a2) is r * 2^81, and 2^96 / 2^81 = 2^15. r is the sum of
   the parts over all betas. Parts are not negative, so the sum over any set of betas is a lower bound for r. For r_A, N3 counts
   only the quadruples whose h1 satisfies rule A.

**The count of the class and of the sub-class (participant computation).** The count runs over the 60 words beta that have a part
in the rate of the whole class, the list of entry c66f230d: of the 133,742 words that occur as beta, the 4,550 with k at most 14
were enumerated, and for the 129,192 others a SAT solver was asked whether the whole system has a solution with that beta and
answered no for 129,147, without certificates. The integer enumeration of GPT Sol 6.1 over every beta finds the same 60. For the
whole class the rate is 85074516985129/524288 = 162,266,763.66, from 60 betas and 453 outcomes with a nonzero product. For the
sub-class of the root instance it is r = 194382080300609/1048576 = 185,377,197.55, about 2^27.47, so that under M a trial of the
root instance has R = 0 with probability about 2^-100.53. A few betas carry most of the count (beta* = 18b0e098 alone 36.5% of r,
the four heaviest 98.8%), so the count rests on few paths; the claim of this package uses only the part of beta* on the class
(10.1).

**Checks of the counter (participant computations).** (1) Complete enumeration with 8-bit words of every quadruple (Y4, h1, Y9,
w8) through both executions of E3 and every triple of the E1 side, over random constants, classes, sub-classes with up to three
more fixed bits of e1 and rules with parities of three bits: five runs, 1,472,040 and 5,332,992 integers, none different from the
counter. (2) At 32 bits two functions compute the E3 side with its split by the rule and agree on all 687 outcomes both counted;
the other 285 (16 with a nonzero product) were counted by one alone. The E1 count agrees with the earlier calculator on 972 of 972
outcomes. (3) For the whole class, a helper agent that audited entry c66f230d counted both factors of all 453 outcomes with two
programs written from the definitions of 6.2 and 6.3 alone: the same total, 85074516985129/524288, and the same parts for 60 of 60
betas.

**Real messages in the counter arrangement.** This and the next paragraph report participant measurements of the counter
arrangement; the organizer's harness does not run them, and they are untrusted evidence for it. On a graphics card a helper agent
ran the counter construction on real 32-bit messages, with random outer words and 2^12 consecutive members of Q* per outer step:
2^45 trials with Y4 in the sub-class and 2^44 with Y4 in the whole class, and the same counters on the seven-word model with c1 in
Q* (2^44 and 2^43 model trials); on a processor, four runs of 2^20 outer steps with 2^16 members each. Every real trial had the
difference beta* (2^45 of 2^45). Against the exact figures of the model:

| Event | Model, exact | Real counter trials |
| --- | --- | --- |
| tau listed for beta* | 2^-10.696 per trial | 2^-10.696 per trial |
| listed E1 outcome (beta*, tau, eps), sub-class | 10,176.0 | 10,129, that is 2^-31.694 per trial |
| listed E1 outcome, both classes together | 15,264 | 15,139 (-0.8% +- 0.8%) |
| rule A | 2^-8 | 2^-8.000 |
| listed E1 outcome and rule A, both classes | 59.6 | 55 |
| listed partial E3 event, whole class | 3,569 | 3,626 |
| E1 test of Lemma N passed (n = 0) | | 2^-26.02 per trial |

The ratios of the real to the model runs, in the sub-class with Poisson errors: listed E1 outcome 1.009 +- 0.017; listed tau
1.0001; rule A 1.0000; E1 test 0.9998 +- 0.0024; listed tau and rule A 0.9999 +- 0.0002; listed E1 outcome and rule A 0.90 +-
0.25; listed partial E3 event 1.057 +- 0.020, where the true error is larger because these events cluster by outer step (whole
class 0.971 +- 0.028); each of the four residual words zero 1.019, 1.009, 0.984 and 0.990, each +- 0.006 to 0.021. In the
arrangement of entry 64c075ac the same events of beta* are rarer by the factor of the prescription: c1 lies in Q* with probability
2^-11 there, and the listed E1 outcome of beta* has 2^-42.69 per trial, against 1 and 2^-31.69 here. So the E1 side of a counter
trial carries the factor 2^11 that the count predicts, and the E3 side is unchanged. On the processor the number of trials of one
outer step that satisfy rule A has a variance 572 times its mean, and that of the listed tau 247 times: single outer steps differ
strongly, and only averages over outer steps agree with M. No event here is deeper than about 2^-40, the listed E1 outcome with
rule A; none is the joint event of H1', at about 2^-91.

**A scaled-down end-to-end run of the counter arrangement.** The whole counter search was run on an eight-bit version of the hash:
2-round BLAKE3 with 8-bit words, 2-bit toy bytes, 64-byte blocks and 1,024-byte chunks, with eight sets of toy constants fixed
before any counted run and the class of each. The messages are F || A and F || B of 1024 t + 55 and 1024 t + 63 toy bytes with t =
1 to 255, F being t chunks of zero bytes; the last chunk is compressed with counter t and flags 3, and t = 0 is dropped (79.3
million of 20.3 billion trials, one in 256, as expected). The inner word d1 runs over the values of the heaviest beta of each set,
the toy form of c1 in Q*. Both last-chunk compressions of every trial were evaluated in full and all eight words compared, with no
rule and no filter; every collision was rebuilt as two complete messages and confirmed by two independent toy tree hashes, one of
them written after the organizer's code. The predictions are exact model counts for each set. Over the eight sets:

| Arrangement | Collisions found | Predicted | Trials per collision |
| --- | ---: | ---: | ---: |
| root instance (counter 0, flags 11) | 67 | 64.0 | 8.8 * 10^8 |
| counter, d1 in the set of the heaviest beta | 251 | 255.0 | 8.1 * 10^7 |
| counter, d1 not restricted (control) | 54 | 47.8 | 8.2 * 10^8 |

All 372 collisions are collisions of complete messages, and no trial failed a check. The realised fraction of the predicted gain
of the prescription is (251 / 255.0) / (67 / 64.0) = 0.94 +- 0.13, that is -0.09 +- 0.20 bit: no loss is detected. The control
shows that the counter alone, without the prescription, changes nothing. This tests the mechanism with real collisions. It does
not test the size of the factor at 32 bits, which the toy cannot reach (its factors are 3.9 to 31.8 on the eight sets, against
853.61 here), and it has no rule A, no sub-class and no packed batch.

*The preregistered rerun, the evidence for the factor 10/11 of H1'.* A protocol file (PREREG.txt of the participant, SHA-256
c5895dd64b07710f9fb386b0f9d4f6b5cb38b14b502a4cc80e51c60584432a4e, rechecked after the run) fixed the code, a graphics-card port of
the toy search that reproduced the 251 collisions above line for line, the eight sets, the exact model counts, the seeds, the size
and the rule: margin m is supported when the one-sided 97.7 per cent exact Poisson lower bound on found / predicted is at least
1/m. One run, no interim look, 3,235,715,578,385 counted trials of the counter arrangement: 40,882 collisions against 40,800.63
predicted, 1.00199 +- 0.00496 (z = +0.40), lower bound 0.99213 >= 1/1.1, all confirmed as complete toy messages by an independent
Python tree hash. It is 8-bit evidence under the model's uniform free words; it does not test the 32-bit factor, the filter or the
solver (research/impl/toy8_prereg of the participant, not part of the package).

**Real counter trials on the whole class.** A participant measurement made for the class, untrusted evidence like the paragraphs
before it, which the organizer's harness does not run. On a graphics card a helper agent ran the counter construction on real
32-bit messages in two classes of one build: the whole class of eta (all 2^19 members, no rule, the filter of the fourteen
outcomes of beta*), and as a control the sub-class of entry 26ebba63 with rule A and the seven-outcome filter. Each run walked
2^35 uniform random outer steps and enumerated all of Q* in 2^25 of its passing outer steps, 2^46 trials per class; the passing
steps kept are the first in the order of the card's atomic counter, which does not depend on their content, and the pass share
uses every walked step. Before the runs, the filter tables were compared with the program's construction, 1,000 members of each
class with the member lists, and a sweep of all 2^32 values of tau and of eps at beta* showed that the counters list exactly the
fourteen and the seven outcomes of 10.1; no trial lacked the difference beta*. The counters are the E1 outcome and the filter;
errors are clustered by outer step. The model per trial is the sum of L_j over the listed outcomes times 2^-85 (2^-96 for the
triples times 2^11 for c1 in Q*).

| Event | Exact model | Measured | z |
| --- | --- | --- | --- |
| E1 outcome among the seven of entry 59f8915e, whole class | 53 * 2^-38 = 2^-32.2721 per trial | 2^-32.2692 (13,595 events), 1.0020 +- 0.0086 of the model | +0.23 |
| the same, sub-class control | 2^-32.2721 | 2^-32.2540 (13,739 events), 1.0126 +- 0.0086 | +1.46 |
| ratio whole class / sub-class, the seven | 1 | 0.9895 +- 0.0120 | -0.87 |
| E1 outcome among all fourteen, whole class | 79.5 * 2^-38 = 2^-31.6871 | 2^-31.6888 (20,328 events), 0.9988 +- 0.0070 | -0.17 |
| share of the seven new outcomes among the fourteen, whole class | 1/3 | 0.3312 +- 0.0033 | -0.64 |
| fourteen-outcome filter passes, whole class | 2^-7.5320 (exact) | 2^-7.5321, 0.99990 +- 0.00007 | -1.38 |
| seven-outcome filter passes, sub-class control | 2^-9.8132 (exact) | 2^-9.8130, 1.00012 +- 0.00016 | +0.74 |

Every measured quantity matches the exact model within 1.5 clustered standard errors, and the clustered error of each E1 rate
equals its Poisson value: no excess clustering of E1 outcomes by outer step. For this package the first row is the one that bears
on the rate: the E1 rate of the seven outcomes of entry 59f8915e, with members drawn from the whole class and no rule, in trials
of passing outer steps of the fourteen-outcome filter, which contain every passing outer step of the filter for S (Lemma F); it
equals the rate of the same seven outcomes on the sub-class with rule A, as the model says. The counter covered the seven outcomes
together: the E1 event of S, six of them, is a sub-event of the measured event, with model rate 52 * 2^-38 per trial, 52/53 of it,
and it was not counted on its own. The run has no counter of the E3 side and none of the joint event: the E3 count of these
outcomes on the class (N3_j four times that of the sub-class, 10.1) and the joint event of H1', about 2^-91 per trial, are not
measured, and the seven-outcome filter was run only in the sub-class control. These measurements bear on H1' and H4'; they reach
no collision.

**Real outer steps for the pre-check and the budgets.** Participant measurements made for our entry 415e792c, untrusted evidence
like the paragraphs before it, which the organizer's harness does not run. Helper agents walked real outer steps of the counter
construction on the whole class (all 2^19 members, no rule), drawn from Python's generator, with the participant's program of the
class measurement (step CO and the automata of the fourteen outcomes, their masks restricted to S), and computed nu by (V) on
every outer step whose X is not zero. Errors are binomial over outer steps, which are independent.

| Event per outer step | Nominal share | Count | Ratio to nominal | z |
| --- | --- | ---: | --- | ---: |
| I_E, mask of (2) meets S; 60,000,000 steps | 2^-4.199822 | 3,266,224 | 1.0004 +- 0.0005 | +0.72 |
| I_2, X not zero; the same steps | 2^-9.978162 | 59,367 | 0.9980 +- 0.0041 | -0.49 |
| I_3, T not zero; the same steps | 2^-11.978162 | 15,055 | 1.0123 +- 0.0082 | +1.50 |
| I_2; 30,000,000 other steps (seed 7) | 2^-9.978162 | 29,688 | 0.9981 +- 0.0058 | -0.32 |
| I_3 among those passing steps | 1/4 | 7,452 (0.25101) | 1.0040 +- 0.0101 | +0.40 |

On the 60,000,000 steps the share of passing outer steps that survive the pre-check is 0.2536 +- 0.0018 (z = +2.0); over both runs
it is 22,507 of 89,055, 0.2527 +- 0.0015 (z = +1.9), and the count of I_3 is 1.0089 +- 0.0067 of its nominal value. On the
30,000,000 steps, among the outer steps that pass the fourteen-outcome filter, nu has chi-square 9.99 on 7 degrees of freedom
against the uniform law, and 16.04 on 14 against the group of the mask. I_3 has no budget in this package, and it bears on H5_exec
only through the mean of the ledger, measured below. These are two runs of one generator, made after the design; they are not a
proof that the sampler's nu is uniform or independent of its masks. The program of the 60,000,000 steps is
research/pkg21/work/E/lean_share.py of the participant, not part of the package.

**Real outer steps walked by contexts (the member loop).** A participant measurement made for this package, untrusted evidence
like the paragraphs before it, which the organizer's harness does not run. The participant's reimplementation of the member loop
of entry e9b6649e (9.8; research/impl/memberloop of the participant, its own SplitMix64 generator, one run made after the design)
walked 120,000 contexts, each with all 2^19 members of the class, 62,914,560,000 outer steps, on a graphics card, and counted per
context the passing outer steps and the lanes whose mask of (2) is not zero. With m = 2^19 and p the exact share:

| per context | passing outer steps | lanes with a nonzero mask of (2) |
| --- | ---: | ---: |
| mean count, against m p | 519.013 against 519.809 (0.99847) | 28,491.98 against 28,529.72 (0.99868) |
| z, with the standard error of the 120,000 counts | -1.36 | -1.21 |
| ratio (E[n(n-1)]/E[n]) / ((m - 1) p_hat), p_hat the observed share | 1.152 | 1.144 |

Both shares agree with their exact values within the error of the clustered counts, as Lemma CX (c) says the means must. The same
reimplementation checked the two lists of Lemma Y and compared the 25 member lines and the masks with the full step CO on 100,000
pairs, and the omega-first batch was compared with the full member loop on every outer step of a run of 62,914,560,000 outer steps
(9.8).

**Clustering by context at every depth (participant measurements).** Untrusted evidence for part (ii) of H1' (10.3), made after
the design and not preregistered. For each event below, every listed good trial meets it; n is its count in one context of m =
2^19 members, p_hat its observed share per member, and the ratio (E[n(n-1)]/E[n]) / ((m - 1) p_hat) is 1 when the members of a
context are independent. Each run has a control arm: as many blocks of 2^19 independent outer steps (eight fresh words each), with
the same statistic. All arithmetic is exact on 32-bit words, on a graphics card. Before the runs, 23,000 vectors were compared
with the participant's Python code on Y9, omega, C2.c1, C2.b1, both masks, nu and the pre-check, with no difference; every outer
step that the pre-check kept (15.6 million per arm) was rebuilt on the processor and passed to the Python solver with (G7) and the
pre-check, and every root to the certificate; in the root runs the recorded steps reproduced the counts of every block, and a
re-run of the first 32,768 blocks was byte-identical.

| event of an outer step, per context | contexts | ratio, contexts | ratio, control |
| --- | ---: | ---: | ---: |
| condition (1) alone | 120,000 | 1.000175 | 1.0000 |
| condition (2) alone | 120,000 | 1.1433 +- 0.0008 | 1.0000 |
| passes the filter | 120,000 | 1.1513 +- 0.0009 | 1.0000 |
| passes and the pre-check keeps an outcome | 120,000 | 1.1572 +- 0.0010 | 1.0000 |
| the solver reaches a leaf | 120,000 | 1.153 +- 0.003 | 0.998 +- 0.002 |
| the solver returns a root | 46,104,576 | 1.2486 +- 0.0806 | 1.0367 +- 0.0718 |

The errors are over groups of contexts (12 groups of 10,000; for the root a jackknife over 100 groups). Relative to the event
above it, the pre-check adds a factor 1.00518 +- 0.0002 and the leaf 0.996 +- 0.002, and at the cuts of the solver between the
leaf and the root the ratio stays between 1.14 and 1.25 with no step beyond its error. Contexts with two outer steps that return a
root: 252 against 201.4 for independent members and about 248 at a ratio of 1.233; in the control 208 against 200.3; none with
three in either arm. The clustering comes from condition (2): omega = Y3 + y + w8, and w8 depends on the context only. No root of
these runs passed the certificate of step 3 (0 of the 763 roots of the 120,000-context runs): no listed good trial is observed,
and the ratio of listed good trials themselves is not measured. The runs are research/impl/memberloop/deep and
research/impl/memberloop/roots of the participant (seeds 1001 and 3003 for the contexts, 2002 and 4004 for the controls), not part
of the package.

**Clustering of the deepest events across members: a preregistered run.** Untrusted participant evidence for part (ii) of H1'
(10.3). Before any step ran, a protocol file, PREREG.txt of the participant (SHA-256
248838947f505b89c3927b7da829548acef92a540e474a9eefe3bd04c06cb92e, rechecked after the run), fixed the events, the arms, the
statistics, the decision rule, the size rule and the seeds. Each arm has 262,144 contexts, each walking all 2^19 members with 512
values of c1 per outer step, a random affine subspace of Q*, so 2^46 trials per arm, from two generators (Philox4x32-10 and
SHA-256 in counter mode); the control arm draws fresh outer words for every outer step. For the count n of an event in a context,
the ratio (E[n(n-1)]/E[n]) / ((m - 1) p) splits into a part from pairs within one outer step and the cross-member factor Rx from
pairs of different members, which is 1 for independent members. The graphics-card code matched a Python reference on 1,179,648
trials with no difference, and all 32,199 recorded hits of the two deepest events were recomputed with real compressions.

| event, per trial | share | Rx, contexts | upper limit U | Rx, control |
| --- | ---: | ---: | ---: | ---: |
| listed E1 outcome: tau in S, eps = eps*, beta = beta* | 2^-32.29 | 0.999 +- 0.054 | 1.162 | 1.068 +- 0.064 |
| (J1) and (J2) of the E3 half, for an outcome of S | 2^-34.58 | 0.90 +- 0.24 | 1.94 | 1.12 +- 0.27 |
| R24: low 24 bits of the difference of chaining-value word 1 zero | 2^-23.76 | 1.0002 +- 0.0001 | 1.0006 | 1.0001 +- 0.0001 |

U is Rx plus three standard errors (a jackknife over 128 groups of contexts), or the 99.865 per cent Poisson limit when fewer than
30 cross-member pairs occur (13 for the E3 event). Only the filter events cluster by context: test (2) 1.1439 +- 0.0004 and the
pass 1.1522 +- 0.0005, against 1.0000 in the control. Every upper limit lies at least 43 bits below the factor 2^43.86 that part
(ii) allows. Limits: the joint event, about 2^-91 per trial, is not reachable and the two halves are measured separately, so
carrying Rx near 1 to it remains the premise. The run is research/impl/memberloop/prereg8 of the participant, not part of the
package.

**The shares of H4': a preregistered sample (prereg7).** A participant measurement, untrusted evidence, which the organizer's
harness does not run. Before any outer step of the main sample was drawn, a protocol file, PREREG.txt of the participant (SHA-256
92d16cda1cd13aacb287470b968ff2d914362b12fefb680c94960280a7471131), fixed the sampler, the seeds, the checks and a timing rule for
the sample size; its primary statistic, a moment of another credit, is not used by this package. The sampler is the program's
outer step of the whole class (all 2^19 members, no rule), translated line by line into a graphics-card kernel, with the words
from Philox4x32-10 keyed by seeds derived by SHA-256, none of which a scan of the participant's 36,311 files found elsewhere. On
separate seeds the kernel matched the unchanged Python code on every field of 65,536 outer steps, and in the main run on the first
4,096 outer steps of each of its eight streams; nu by (V) matched a separate computation in every outer step. The sample ran once,
with no interim look, on 2^39 = 549,755,813,888 outer steps: 545,067,537 passed the filter for S against 545,059,418 expected (z =
+0.35), 29,915,698,553 had a nonzero mask of (2) against 29,915,578,368, and the pre-check kept 136,255,727 of the passing outer
steps, 0.249980 (z = -1.10). The factors of H4' are the least that these counts support (10.3). This is evidence from one
pseudorandom generator, not a proof. The sampler, the analysis and the protocol are research/pkg19/as_subset/prereg7 of the
participant, not part of the package.

**H5_exec on the declared program: a preregistered sample of whole contexts (participant measurement).** Untrusted evidence, and
the first preregistered evidence for this premise. A protocol file of the participant (PREREG.txt, SHA-256
3b3fdad4108a5be903c8af5b504b538828debdb803d7dda5ffa728dec66da8b7), recorded before the first context ran, fixed the statistics and
the one-sided level 1 - 10^-6. The program was the declared program of our preceding layout (SHA-256
4f87cfe2937913258697ab7348840a526ebd1944e0d4d9c00d3ca5c06a15995c), whose joint solver, guards and pre-check are those of 9.2 and
whose ledger is U0 of 9.7, with read-only counters added; the counted copy gave output byte-identical to the program on four
requests of 256 trials. It walked 51,549 whole contexts of 2^19 outer steps each, from two generators (a SHA-256 counter, 25,779
contexts; SplitMix64, 25,770), which agree on every mean per context (largest |z| 2.25). The ledger U0 averaged 1.294334 +-
0.002348 per outer step over 6,671,108 calls (5,243.71 per call, largest 12,764 against the cap 15,584 of this ledger, Lemma FX),
with the one-sided upper bound 1.30550, below 1.01 u_M = 1.322107 and below u_M = 1.3090 itself. In the same sample the earlier
two-borrow gate opened on 0.448301 +- 0.000124 of the clusters (one-sided upper bound 0.44889), consistent with the bound of its
own Lemma OR, and every exception count was 0 over 692,644,553 in-run checks: guard rejects, calls with the ledger above C_G(T),
meter breaches, lost or extra roots, skipped passes and mismatches; a second analysis of the run files confirmed these figures.
Limits: the words come from two pseudorandom generators, not from the law of model M, and the ledger counts each executed block at
its upper unit cost. The files are research/frontline/stack_regression/prereg of the participant, not part of the package.

**The ledger of H5_exec on real outer steps (participant measurement).** Untrusted evidence, made after the design and not
preregistered. The prereg7 kernel with one added filter kernel listed every outer step with T not zero among 2^32 outer steps,
with fresh Philox4x32-10 words for every step, once with the lines of the searched instance (flags 3) and once with flags 11;
every listed step was recomputed in Python with no difference in T or nu, and a Python scan of the first 524,288 steps of one
stream gave exactly the listed steps. A participant reimplementation of the joint solver of 9.4 with (G7) and (G15), which matched
the traversal with (G7) alone node for node on all 649,242 rows that survived setup when (G15) was off, ran every call and added
the ledger U0 of 9.7 from its counts:

| Quantity | flags 3 | flags 11 |
| --- | ---: | ---: |
| calls (T not zero) among 2^32 outer steps | 1,063,703 | 1,065,105 |
| mean of U0 per call (standard deviation) | 5,242.8 (946.9) | 5,243.7 (947.1) |
| largest U0 of a call; calls above 15,584 | 11,740; 0 | 12,704; 0 |
| mean of U0 per outer step | 1.298456 | 1.300374 |

The standard error of each mean per outer step is about 0.0013. In model M a call has probability 279,070,422,111 / 2^50 and U at
most 5281.18 per call on average (10.3). Both means per outer step lie below u_M = 1.3090 and well below 1.01 u_M = 1.322107; 99.1
per cent of U0 is its part A(T) + 288, a function of T, whose cells matched the model's shares within their errors. Limits: the
ledger counts each executed block at its upper unit cost, not executed instructions; the solver is a reimplementation, not the
declared program, whose own 1,031 calls over the 4,096 trials of 9.2 averaged 5,195.5 units of U0; and the words come from one
pseudorandom generator. The programs are research/fifties/solverwork of the participant, not part of the package.

**The fills of H_G_cluster: a sample of 2^24 contexts (participant measurement).** Untrusted evidence. A protocol file, PREREG.txt
of the participant (SHA-256 d67f35a873ebbc55779ce5b7cb0b9c11d851a00baaedcea5af07805c3f61760d), sealed before any context of the
main sample existed, fixed the statistic, G(C) of 9.9 counted exactly over the 2,341 representative batches and the partner
batches of every cluster in the order of 9.9, the size rule, the seeds and the analysis. It was written to test a lower bound,
9,368.37, which the sample rejects; the bound 12,466 of H_G_cluster is the one-sided Hoeffding bound of the same sample (10.3),
not a preregistered value. The outer words come from SHAKE256. A graphics-card program counted G; on 4,096 contexts it agreed, in
G, the E lanes and the opened clusters of every context, with a Python mirror built only from the declared program's own functions
(the context lines, the packed operands, the cluster map, the omega side, the gate and T2); omega was compared with step CO on all
2^19 members of each of those contexts and T2 with the program's rule on all 2^32 inputs, with no difference; and the declared
walk itself was cross-checked on its trial batches of 2,048 contexts. In every context of the main sample G equalled the same
count with the gate ignored: no member with a nonzero mask of (2) lay in a closed cluster.

| Quantity | Value |
| --- | --- |
| contexts | 16,777,216 (2^24) |
| sum of G | 208,495,306,067 |
| mean of G per context | 12,427.289 (standard error 1.276) |
| smallest and largest G | 0 and 31,214 |
| mean fills of representative and of partner batches | 277.65 and 12,149.64 |
| one-sided bounds on the mean: empirical Bernstein and bounded KL (delta 0.00135), Hoeffding (delta exp(-7), range 84,261) | 12,432.25; 12,453.82; 12,465.77 |

The sampler, the programs and the analysis are research/frontline/hg/prereg_ck2 of the participant, not part of the package.

**What does not exist.**

- No organizer-run digest check of the counter instance (6.4, Section 7): its checks are participant computations with the
  organizer's functions imported (Section 7) and the declared program's in-run step-CT compressions (9.2).
- No measurement of the joint event of H1', at about 2^-91 per trial; the deepest counter events measured are the listed E1
  outcome at 2^-31.7 and that outcome together with rule A, 55 events at about 2^-39.8. No separate count of the E1 rate of the
  six outcomes of S: it is a sub-event of the measured seven.
- No proof of the open parts that H1' declares (10.3), of the shares of the two counts of H4', of the mean of the ledger of
  H5_exec or of the mean of G of H_G_cluster; these are measured (above), the shares on a preregistered sample of 2^39 real outer
  steps.
- No measurement of rho_x or of the clustering ratio v of listed good trials by context (10.3), which no run of feasible size can
  observe; the ratio was measured for the events that every listed good trial meets, from the filter to the roots of the solver,
  and its cross-member part, preregistered, for the two halves of a listed good trial (above).
- No scaled-down run of the counter search with the outer filter or the joint solver, and no complete message of a found pair; the
  complete messages hashed (Section 7) are trials, with t from 1 to 16,383.
- No run of the search at full scale, and no root of the search itself: the declared program walks 32 clusters of one context per
  trial (9.2); its solver calls return planted roots only. Its units are added per event from the ledger; every row of Section 11
  is bounded in words, except the 67 of a batch of 9.8, which participant programs executed and counted, and the omega side, key,
  carry word, gate tests, byte guard, descriptor selection, broadcasts, chunk addressing, lane tests, E lane, fill, shortcut,
  pre-check and preflight of this row, which a participant tool counted in the declared program as it ran (Section 11).

**Limits of the evidence.** H1' is an assumption (10.3); beyond it:

- M fails inside one context and one outer step: the count of rule A per outer step has a variance 572 times its mean. Where it
  was measured it holds on averages over outer steps. The counter search fixes Y4, Y9, w8, Y12 and w5 for the 2^21 trials of an
  outer step; a context, in turn, holds its seven outer words fixed for all its 2^19 outer steps. Success therefore comes from
  many independent contexts, 2^50.115 of them, with 2^69.115 outer steps walked, about 2^59.14 of them passing and 2^57.14
  reaching the solver, and it rests on the premise that a context rarely holds more than one listed good trial.
- The shares of H4', the ledger of H5_exec and the fills of H_G_cluster are measured on pseudorandom generators, and the quarter
  share of the pre-check and u_M are exact only in model M; none of them is proved for the sampler. Lemmas F and VP need no law of
  the words, and the time bound needs none either: a reached budget or an exhausted credit halts the run, which lowers the success
  probability and not the time bound.
- The model is checked on real messages to about 2^-40, not at 2^-91; the scaled-down whole-collision runs of the counter
  arrangement are level (0.94 +- 0.13 of the predicted gain; preregistered, 1.00199 +- 0.00496 of the predicted count).
- The constants and the class were chosen by the count, and beta* with them, so they favour any choice that the model overrates; S
  was chosen by the charge. The six outcomes of S carry 41.7 per cent of the count of the class, with one value of eps. Most
  measurements of this section are on the sub-class and the seven outcomes of entry 26ebba63; on the whole class the E1 side of
  those seven outcomes, which contain S, was measured (2^46 trials), and their E3 side was not.
- The count rests on programs that are not in the package and on a list of values of beta that is complete only by uncertified
  solver answers and the other model's enumeration.
- Helper agents of the participant wrote and checked the counter construction, the filter and this text, and another AI model
  proved Lemmas IP, F, S1 to S5, S8 and S9 and derived the count of passing pairs; no person has read it.

The required baseline_improved identifier blake3-r2-nominal-v2 names the organizer's nominal display reference 128, not an
established attack, qualified baseline or security bound; the claimed 62.7934 lies below it. Whether a qualified result improves
the Yukon incumbent is decided separately; no Pareto dominance claim follows.

## 15. Earlier entries

One line each: the entry of the participant, its time_log2, its ruling or status when this text was written, and what this text
keeps from it.

| entry | time_log2 | ruling | kept in this text |
| --- | ---: | --- | --- |
| c66f230d | 97.6 | in review | the constants, eta, Fact P, Lemmas L, H, Q, T and N |
| 64c075ac | 92.53 | not evaluable | the root instance of Sections 4 to 6 and the machine of 6.5 |
| e7b17fd1 | 84.98 | in review | the counter construction, Lemmas TR, CT, IP, S1 to S5 and S8 |
| 26ebba63 | 71.39 | in review | the program and the experiments, the filter, the joint solver, H1', H4' |
| 59f8915e | 67.8004 | in review | the whole class, (P*), Lemma J0, the families of the solver |
| 415e792c | 66.8050 | in review | S and the pre-check |
| a402a477 | 63.9522 | passed | the counter search with the cluster gate and the omega-first batch, its budgets and the declared program |
| 50d28015 | 63.1880 | passed | the work register, the shortcut, the metered credit, the layout of 9.8 and the program, which this text extends |
| 89b451ff | 62.9459 | passed | the masked partner walk with Lemma XF, F1, P1, the source bank and the cap transfer |
| 0bc5f130 | 66.8751 | in review | the guard (G7) with its trees, ledger and caps |
| 11ccf5a7 | 70.21 | not evaluable | nothing |
| e85fffe8 | 75.4217 | not evaluable | nothing; the advice record of Section 12 |
| 78ac164c | 71.7481 | not evaluable | nothing; the advice record of Section 12 |

## 16. Credit

One line per contributor. Apart from the helper agents of the participant, nobody named here has reviewed this package, and a
credit is not an endorsement.

- **hecmas**, entry e9b6649e (65.3643): the member loop over contexts, the two direct tables of the filter and the restatement of
  the premises for contexts (9.8, 10.3, described in the participant's words).
- **Th0rgal**, entry 77818485: setting the credit of the solver at an exact model mean of its work, here of the executed ledger
  (9.1, 10.3); earlier, the member values built once per outer step (entry df8bd46d) and three coding steps of 6.5 (entry
  8c81a219).
- **GPT Sol 6.1 (OpenAI)**, an AI model run by the participant: the cluster gate with Lemmas KP and A9, its layout and charges
  (answer CI 1), its opened-cluster budget (answer CJ 1) and tight layout (CJ 2 to 5), the least factors of H4' on our sample and
  the reserves over contexts (CK), the stacked ledger and its once reserves (CK2), the metered credit with its meter, preflight
  reserve, the ratio of Lemma ME and the premise H5_exec (CK3), the cached Y9 of a batch with its frames, fill budget and the
  premise H_G_cluster, and the stacked row (CM), the omega-first batch and its audit, the E count in a register with the frame of
  a passing lane and the global ledger of 1,024 (answers CA and CD), the root certificate with Lemma RC and the guard (G15) with
  Lemma G15 (CF 6 and 7), the guard (G7) with Lemma G7 (AX 1), the pre-check and the budgets (AW), the joint solver with its
  certificates, guards and caps (AE to AT), Lemmas F and S9 (AC), Lemmas IP, S1 to S5 and S8, the sub-class and rule A of the root
  instance, and, in its local answers, the fold F1 and the shortcut P1 (D9), the row and specification of entry 89b451ff that this
  row keeps (D11 and D12), the source bank, immediate list addresses, the context bound and the cap transfer with Lemma CP (D13),
  the masked partner walk with Lemma XF and its class specialization (D14), the straddle gate with Lemmas CL and OR and its
  six-operation key (D14 and D16), and the row of this text with its audit of the masked opening (D18).
- **GPT-6 Astra (OpenAI)**, an AI model run by the participant: the exact flat mean and the bound in model M on the mean of the
  solver's ledger, u_M (Batch 11), cited in 9.1 and 10.3 and not reproduced here; one row per family, Lemma FX (Batch 17).
- **Jbenisek**, the participant who files this package: the half-collision, the class search and the counter construction of the
  participant's entries from 17bba2ae on (Section 15), among them the guard (G7) in this solver (0bc5f130).
- **The participant who filed entry dd91b2f6**: dropping the sub-class and rule A in the solver design, and the fourteen outcomes
  of beta* on the class; nothing of that entry is used.
- **winglock**: searching only a sub-class of members chosen by an exact count (entry 18a7fc52), which the sub-class of the root
  instance follows.
- **5kyguy**: keeping masks in registers across the loop over the members (entry 404d14df).
- **0xshikhar**, entry 73d5265f: keeping the frame words and the counts of the walk in registers (9.8, 9.9).
- **tekkac**: the lane layout of 6.5, seven 36-bit lanes with a masked rotation (public ticket 2bf40fb).
- **Grok (xAI)**, run by the participant: the four cuts of the masked opening of this row, the two chunks priced together, the
  bookkeeping, the descriptor selection and the chunk addressing (job 58), as GPT Sol audited them (answer D18); the deletion of
  the scalar rebuild, the cursor and the context schedule (job 53), as GPT Sol certified them (answer D13); earlier, the hostile
  review of entry c66f230d.
- **GPT-6 Luna**, on the owner's server: a search for better pinned constants, which found none.
- **A model reached through the service Venice**: a statement on prior art, unverified and used in no proof or figure.
- **Helper agents of the participant**, instances of the AI model that wrote this text: the reimplementation of the member loop
  and its measurements, the omega-first batch with its op-counting simulation, the cache and the meter of the declared program,
  our audit of the layout of this row (the work register, the shortcut, the pre-check without a table, the table addresses, the
  gate key, the written-out code and the meter without slack), the combination sweep from which the masked partner walk came, the
  build of this row with its op count of the declared program, the integer recounts, the price with its integer test, the count of
  Section 17, the measurements of Section 13, and this text.

## 17. The counting program for 67,633,152

The program below computes the part of beta* = 18b0e098 in the rate of the class of eta (Section 10.1), outcome by outcome, in
exact integer arithmetic, with the standard library only: every tau (taus), both roots eps (eps_roots), the E1 count L_j (L_count)
and the E3 count N3_j (N3_count), each as an exact carry count over all bit positions, with Y4 over all 524,288 members of the
class (Lemma Q) and no rule on h1. Nothing is sampled, capped or delegated to a solver. It is the program printed by entry
26ebba63 with these changes only: the header comment, the member list (the class in place of the sub-class) with its size check,
the empty rule, and the final check. Run as `python3 -B count.py`, it printed the outcome table below in about 2.5 minutes (Python
3.14). Its column L*N3/2^81 is four times the last column of the table of 10.1; its column "rule A" is the count with the empty
rule and equals N3 in every row. Its self-test, a brute force at width 6 that follows the listing in the file, ran 12 seeds with
no mismatch. The program prints all fourteen outcomes of beta* on the class and their sum; this package lists the six outcomes of
S, and only their rows are shown below, in the program's order. They sum to 270,532,608 = 4 * 67,633,152 on the program's scale
2^81, that is 67,633,152 on the scale 2^83 of a trial with Y4 uniform in the class (10.1). The eight rows that are left out,
675020a0 and the seven with tau ending in 5060a0, sum to 16,261,120 = 4 * 4,065,280 and are listed, with their L_j and N3_j, in
the table of 10.1; the sum and check lines of the program, which follow the rows, are those of all fourteen.

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

Output of that run, the outcome table restricted to the six rows of this package (the program's other lines are unchanged):

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
