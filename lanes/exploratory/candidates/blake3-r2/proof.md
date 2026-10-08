# A staged S8 search on the 55/63-byte half-collision of 2-round BLAKE3 in
the order S2K14 with one stage-A test per four positions, an early exit in
stage C, X14 = 0, uniformly sampled premises and near-premise budgets

The scalar below is `time_log2` under `collision-frontier-v5` (C = 430).

**Credits.** This package (v106) is winglock's ef052659 (93.5322) with one
change, taken from GordoAR: the factor F of H1 (i) is set at margin 1.400
over the exact model count, F = 185,350,144 * 5/7 = 132,392,960, instead of
at margin 2.000, and V is the smallest number of outer-step values vd that
certifies success 0.39 with this F under the success bound of Section 7,
V = 1,057,885. GordoAR made this choice first, on Subflatus3's promoted
52bb50ee machine (6a600434, 93.73) and on Subflatus3's 5ca02dfb machine
(3f8e4e89, 93.0451); we
apply it unchanged to ef052659, recompute V, the budgets and the ledger
with ef052659's own code, and add a preregistered uniform sample of the
premises of H1 (ii) drawn from this package's run (Section 8.2). ef052659
is Subflatus3's 5ca02dfb (93.5576: winglock's c19feef with the lane stride
2^14 and the paired stage-A test by Subflatus3) with two changes by
winglock: one stage-A test for four positions instead of two, with a hit
tree (Section 5), and an early exit in stage C with a rare continuation and
a third budget (Sections 3, 4, 5, 7). The quad test generalizes
Subflatus3's pair test (Lemma P of 5ca02dfb), and its proof follows that of
Lemma P. Everything else is the
work of 5ca02dfb and its predecessors, credited as 5ca02dfb credits them:
the lane stride 2^14 (order S2K14, first submitted by Subflatus3 as
ef81f589), the four D slots, the preregistered 2^35-batch uniform sample of
this order and its premises 0.377 and 1.003 (Section 8.2, Appendix B), and
the pair test, from Subflatus3's 5ca02dfb and ef81f589. From winglock's
c19feef: the loop order S2K (an X2 table built once per outer step, batches
of seven X2 values of one member with C2.a1 = (7g + l) 2^k + i, so that
C2.d1 advances by one addition per batch and rule A folds into a block
constant: Lemma A3), the pass-flag stage tests (Lemmas A3, F2), Y9 and Y13
in stage C, one-operation budget counts with a halt test per group, the
per-batch uniform sample design and `rtuni4.c` (Appendix A). From
winglock's earlier 18a7fc52, d26a3c5f, 2bb5d604, 098e66f4 and 21252124:
the sub-class S8, the beta filter and Lemma B, Lemmas D and D', the exact S8
count, the branch-free 64-register residual computation (stage C, now the
continuation), the beta filter as the stage-B test, a fresh random word per
outer step, the exact model values of the two stage events, the Chernoff
bound on the budgets (Theorem 2) and D3.d1 = X3 (X14 = 0). From Jbenisek's
c66f230d (co-author tekkac): the 55/63-byte length cancellation, the six
pinned constants, Lemmas L and H, the class of Y4 (eta = 830303cf), rule A
and Lemma N. From Jbenisek's 60f94c5c: the three-level construction (steps
O, M, Y and T of Section 2), a table built once per outer step and reused by
the inner loops, and the staged batch with a halting budget. From
Subflatus3's 52bb50ee: the stage-B part of H1 (ii) stated as a run average
supported by a preregistered uniform sample, with the lower-tail Chernoff
bound (Lemma C') and the empirical Bernstein bound as the decision rule.
From Subflatus3's 1d5e54ce: sampling single uniform batches of the run
(Lemma U), used again here for the new premise. From leech1996's 5266c5ce:
budgets just above the premises (delta = 1/6000 in Theorem 2), used for
all three budgets. Building member-dependent values once per outer step was
first published by Th0rgal in df8bd46d. The seven 36-bit lanes and the
masked rotation are from ticket 2bf40fb (tekkac); the complement
propagation follows 8c81a219 (Th0rgal). Subflatus3, Jbenisek, tekkac,
Th0rgal and leech1996 are co-authors of this submission, with GordoAR
(for the margin 1.400). Text carried over from 5ca02dfb and c19feef keeps its
wording; where it says "we" about a measurement or a choice of S8, the
filter or the counts, that work is winglock's; Subflatus3's work is named
as such. Text
carried over from ef052659 keeps its wording too: where it says "this
version", it means ef052659, whose program, samples and checks this package
inherits; what this package changes or adds is marked v106, and every
number that depends on V (N, the batches, the budgets, the exponents of
Theorem 2, lambda, the success bound and the time) is v106's. The sample
program of ef052659 (`eaq.c`, Appendix C) contains Subflatus3's `sbs2k.c`
verbatim, and v106's (`eaq106.c`, Appendix E) is `eaq.c` with one constant
changed. "v104" and "v106" in file names and file comments are our
internal labels for ef052659 and this package. We do not use the
sub-class, the eight-condition rule, the E1 test stage or the budget
premises of 60f94c5c.

**Change from ef052659 (93.5322) in v106: GordoAR's margin.**

- **Factor.** F = 132,392,960 = 185,350,144 * 5/7 = 2^26.9803
  (132,392,960 * 7 = 185,350,144 * 5 exactly), margin 1.400 over the exact
  model count of Section 8.1; ef052659, 5ca02dfb and c19feef use
  F = 92,675,072, margin 2.000. GordoAR's 6a600434 and 3f8e4e89 use 1.400;
  the choice is theirs.
- **V.** With this F, lambda = N F 2^-128 = V F 2^-48. The bound of
  Section 7, P(success) >= 1 - exp(-lambda) - 0.002 minus the three budget
  terms, is at least 0.39 for V = 1,057,885 (lambda = 0.4975807, success
  0.3900002) and not for V = 1,057,884 (0.3899999); so V = 1,057,885
  (ef052659: 1,512,538), N = V * 2^80 = 2^100.0128 trials in
  V * 2^32 = 2^52.0128 outer steps and 2^97.2054 batches.
- **Budgets.** E_B, E_C and E_R are the same formulas in N (Section 4) and
  fall by the factor 1,057,885 / 1,512,538 = 0.6994 to 2^93.4711, 2^89.0173
  and 2^76.0130. The exponents of Theorem 2 fall by the same factor: stage
  B 3.16 * 10^6, stage C 1.44 * 10^5, continuation 17.55 (ef052659: 25.1),
  and the success bound of Section 7 subtracts exp(-17.55) = 2.4 * 10^-8
  for the last.
- **Unchanged.** The program differs from ef052659's only in its two ledger
  constants V_RANGE and F_H1, which organizer mode and the self-test do not
  read: the 2,000-case self-test output is byte-identical to ef052659's, and
  a runner run on the public seed gives the same observations (Section 6).
  The operations per trial (3.349608), the order, the stage tests, the
  counted pieces and the premise values theta_B = 0.377, theta_C = 1.003
  and rho_R = 2^-24 are ef052659's.
- **Premises on this run.** H1 (ii) states averages over the run's own
  batches (Lemma U). The run now has vd below 1,057,885, while 5ca02dfb's
  and ef052659's samples drew vd below 1,512,538, a larger index space that
  contains this run's (69.94% of its outer steps). v106's preregistered
  uniform sample of 2^35 batches drawn from this run (Section 8.2) passes
  all three tests at the unchanged values: stage B 0.376590 p_B, rule A
  with the filter 0.99997 * 2^-11 and the early-exit event
  2^-32.19 per trial.

The claim falls from 93.5322 to **93.01972** (time_log2 93.0197120).
5ca02dfb's ledger at this V and F gives exactly 2^93.045076, the claim
93.0451 of GordoAR's 3f8e4e89; ef052659's two changes take 0.0254 off it,
as they took 0.0254 off 5ca02dfb's 93.5576.

**Margin 1.400 is the thinnest margin used in this lineage** (2.000 in
c19feef, 5ca02dfb and ef052659). It is a choice, not a measurement: the
factor F of H1 (i) is assumed, and the count it is set against is exact
under the model M but untested at the 2^-100.5 rate of the event good. The
evidence that the real rate is not far below M's is unchanged from
ef052659 (Section 8.1): the E1 part has real/model 1.0086 over 2^33.8 real
trials, partial E3 events of about 2^-38 match M per outcome on real trials
(including the ratios between S8 and the rest of the class), and with
D3.d1 = X3 the rates of random D3.d1 hold down to the 2^-14 event (the
2^-30 event at 0.82 +- 0.13). Since V is minimal, a real rate of the full
event below 1/1.4 = 0.714 of M's would put the success bound below 0.39
(at margin 2.000 that took a rate below about 0.5 of M's); no measurement
resolves the full event. The weakest real-trial check, the 2^-30 event at
ratio 0.82 +- 0.13, lies 0.8 standard errors above 0.714 (pooled with the
random-D3.d1 counts, 0.87 +- 0.09: 1.7 standard errors). If a factor 0.82
applied to the full event and S8's advantage under M were entirely an
artifact of its selection (the class rate, 1.089 F), the count would be
0.89 F, below F: margin 2.000 absorbed that case (1.275 F), margin 1.400
does not.

**Changes of ef052659 from 5ca02dfb (93.5576)** (carried over; "this
version" is ef052659). The trials, the event good, S8, the count, the order
S2K14 and its batches, stage B (66 operations) and the table word (94) are
unchanged, and so are the two premises of H1 (ii) that 5ca02dfb set; a new
uniform sample of this version reproduces both (Section 8.2). (ef052659
also kept 5ca02dfb's V, F and lambda; v106 changes them as above.)

- **Quad test.** In 5ca02dfb positions i, i + 1 of a group share one test
  of (pA OR pA') AND B32 (Lemma P). Here positions 4q .. 4q + 3 share one
  test: U3 = pA0 OR pA1, U12 = pA2 OR pA3, U15 = U3 OR U12, x15 = U15 AND
  B32, compare with 0 and branch (6 operations; Lemma P4). Stage A costs 70
  operations per four positions, 17.5 per batch instead of 18. When the
  test is taken, a hit tree of masked zero tests on built OR words finds the
  set of batches with a passing lane and their flag words xA = pA AND B32;
  its cost is at most 10 operations per stage-B entry (7 to 10 for a
  single batch, 29 for four, including a 10-operation spill of the fourth
  batch's words at that leaf), charged against the existing
  stage-B budget (5ca02dfb: 6). The batches that enter stage B are exactly
  those of 5ca02dfb, with the same xA, so no premise changes.
- **Early exit in stage C.** Stage C computes first only the test word
  W4 = P ^ ROR(P, 1) ^ ROR(g1 ^ g1', 12) of Lemma D' (Lemma E: f1 ^ f1' =
  ROR(g1 ^ g1', 12) because Y4 is shared) and tests whether some lane with
  rule A and the filter has W4 = 0 (61 operations; 5ca02dfb: 119 plus a
  6-operation spill). Only then a continuation recomputes the batch, the
  full residual of Lemmas D and D' and the exact test R = 0 on those lanes
  (at most 235 operations, including its own register spills), counted down
  from a third budget E_R. R = 0 implies W4 = 0, so completeness is
  unchanged. The block accumulator and the per-group block test are gone
  (the exact test is in the continuation).
- **Third premise.** H1 (ii) gains a third run average: the probability
  that a trial satisfies rule A, passes the filter and has W4 = 0 is at most
  rho_R = 2^-24, with E_R = ceil(6001/6000 * rho_R * N) = 2^76.0130 (v106's
  N; 2^76.5288 in ef052659). A
  preregistered uniform sample of 2^35 batches of this order (2^37.8
  trials; Section 8.2) measured 2^-31.90 per trial (60
  events) and passed both tests at 2^-24 (Lemma C' exponent 1015,
  empirical Bernstein bound 2^-28.04); rho_R was fixed before that sample,
  after development runs that measured 2^-30.5. The claim moves little with
  rho_R: at v106's V, 93.0199 at 2^-20, 93.0213 at 2^-16, 93.0441 at 2^-12.
- **Registers.** 40 resident (5ca02dfb: 47): the masks B_16 (ROR 16 reads
  A_16 twice) and the accumulator are gone, eight words are kept in memory
  and loaded where read (A_1, B_1 and DY3; S15, w5, w5 + delta per outer
  step; y and e1 per member), and three per-outer registers give C2.d1 of
  the quad's batches. Peak 64 of 64, counted over every path of the quad
  code (Section 5).

The charge per trial falls from 3.4095 to 3.3496 (stage A from
2.57149 to 2.50006; stage B 0.70846 unchanged; hit tests from 0.06441 to
0.10734; stage C from 0.06123 to 0.02988; continuation 0.00001), and
ef052659's claim from 93.5576 to 93.5322; at v106's V and F the same
charges give 93.0451 (5ca02dfb's machine, GordoAR's 3f8e4e89) and 93.01972
(this package).

**Exact part.** For every choice of eight 32-bit words the construction gives
a 55-byte message A and a 63-byte message B whose complete 2-round digests
agree on digest words 0, 2, 5 and 7 (Theorem 1). One of the eight words is
the round-1 state word Y4; the search keeps Y4 in S8. The batches of the
order S2K14 cover every trial exactly once (Section 4). The stage tests are
exact: stage A passes a lane iff its trial satisfies rule A (Lemma A3), the
quad test is taken iff some lane taking part in one of its four batches
passes rule A and the hit tree sends exactly those batches to stage B
(Lemma P4), stage B passes a lane iff it satisfies rule A and the filter
(Lemma F2), stage C computes W4 exactly and every trial with R = 0 has
W4 = 0 (Lemmas D', E), and the continuation computes the residual exactly
(Lemmas D, D'). Given H1 (ii), a budget halts the run with probability below
exp(-3.1 * 10^6) (stage B), exp(-1.4 * 10^5) (stage C) and exp(-17.5)
(continuation) (Theorem 2, a Chernoff bound over independent outer steps;
no independence inside an outer step, a member, a group or a batch is used).

**Heuristic part.** The search runs N = V * 2^80 pairs (V = 1,057,885,
N = 2^100.01). H1 (i) assumes a trial is *good* (R = 0, rule A, beta
filter) with probability at least F * 2^-128, F = 132,392,960 = 2^26.9803,
the exact model count 185,350,144 divided by 1.4 (margin 1.400, GordoAR's
choice; Section 8; `count_s8.py`, Appendix D, recomputes this integer with
the shipped program's constants).
H1 (ii) states three run averages: the share of batches (of the order S2K14)
entering stage B is at most 0.377 p_B (p_B = 0.1992731, its exact value
under the model M), the rate of rule A with the filter is at most
1.003 * 2^-11, and the rate of rule A with the filter and W4 = 0 is at most
2^-24 per trial; the first two were set by 5ca02dfb's preregistered decision
rule from its uniform sample and are reproduced by ef052659's, the third
was fixed before ef052659's preregistered sample and passed its tests; v106's
preregistered sample, drawn from this package's run, passes all three.
Total charged time 2^93.0197120, claimed 93.01972 (rounded up). With the
uniform rate
instead, the same search needs 2^127 trials and gives about 120.2. No full
collision is exhibited.

## 1. Target

H is unkeyed BLAKE3-256 with rounds 0 and 1 of every compression. A message
of n <= 64 bytes is one chunk of one block and one root compression: flags
CHUNK_START | CHUNK_END | ROOT = 11, counter 0, block length n, the message
followed by 64 - n zero bytes read as sixteen little-endian words w0..w15.
The state starts v[0..7] = IV, v[8..11] = IV[0..3], v[12..15] = (0, 0, n, 11),
with IV = 6a09e667 bb67ae85 3c6ef372 a54ff53a 510e527f 9b05688c 1f83d9ab
5be0cd19. Arithmetic is modulo 2^32. G(a,b,c,d,x,y) is

    a1 = A + B + x       d1 = ROR(D ^ a1, 16)   c1 = C + d1    b1 = ROR(B ^ c1, 12)
    a2 = a1 + b1 + y     d2 = ROR(d1 ^ a2, 8)   c2 = c1 + d2   b2 = ROR(b1 ^ c2, 7)

with outputs (a2, b2, c2, d2). Round 0 and round 1, with the permutation
P = (2,6,3,10,7,0,4,13,1,11,12,5,9,14,15,8) applied once between them:

    round 0  K0=G(0,4,8,12;w0,w1)  K1=G(1,5,9,13;w2,w3)  K2=G(2,6,10,14;w4,w5)  K3=G(3,7,11,15;w6,w7)
             D0=G(0,5,10,15;w8,w9) D1=G(1,6,11,12;w10,w11) D2=G(2,7,8,13;w12,w13) D3=G(3,4,9,14;w14,w15)
    round 1  C0=G(0,4,8,12;w2,w6)  C1=G(1,5,9,13;w3,w10) C2=G(2,6,10,14;w7,w0)  C3=G(3,7,11,15;w4,w13)
             E0=G(0,5,10,15;w1,w11) E1=G(1,6,11,12;w12,w5) E2=G(2,7,8,13;w9,w14) E3=G(3,4,9,14;w15,w8)

S is the state after K0..K3, X after round 0, Y after C0..C3, Z the final
state. The digest is o[i] = Z[i] ^ Z[i+8] for i = 0..7. Messages here have
55 and 63 bytes: complete hash, standard IV, flags, true length and
feed-forward, full 256-bit digest.

**Fact 1 (inverting G).** Each assignment of G can be solved for any one of
its terms (b1 = ROL(b2,7) ^ c2, c1 = c2 - d2, d1 = ROL(d2,8) ^ a2,
B = ROL(b1,12) ^ c1, C = c1 - d1, a1 = ROL(d1,16) ^ D, y = a2 - a1 - b1,
x = a1 - A - B). Fourteen words are an execution of one call exactly when
the eight assignments hold.

## 2. The half-collision (c66f230d) and the three-level construction (60f94c5c)

**Lemma L.** Put K = IV2 + IV6 = 5bf2cd1d and, for any w4, w5,
w4' = ((K + w4) ^ 8) - K and w5' = w5 + w4 - w4'. K2 with length 55 and
words (w4, w5) leaves the same four words as K2 with length 63 and
(w4', w5'). *Proof.* With a1 = K + w4 the second execution has first value
a1 ^ 8 and d1 = ROR(63 ^ a1 ^ 8, 16) = ROR(55 ^ a1, 16), the same; c1, b1
follow; the fifth value is (a1 ^ 8) + b1 + w5' = a1 + b1 + w5. QED. No other
round-0 call reads v[14], w4 or w5, so messages of 55 and 63 bytes that
share all other words have the same X. Both messages are honest byte
strings exactly when bytes 55..63 of the block are zero: w14 = w15 = 0 and
the top byte of w13 is zero (the 63-byte message ends in eight zero bytes).

**Fact P.** Constants X3 = 29d4fa98, X7 = bee3af28, X11 = 44036000,
X15 = 40c58500, W4 = 97475638, W13 = 0007c006 (top byte 0). Then
W4' = 97475640, delta = W4 - W4' = fffffff8, and C3 = G(X3, X7, X11, X15;
w4, W13) gives with w4 = W4 the outputs a = Y3 = 8127c181, b = 76f7aefd,
c = Y11 = 7af77f38, d = bbfbdffe, and with w4 = W4' the outputs
a = Y3' = 7edf3e7e, b = 76f7aefd, c = Y11' = 850000c3, d = bbfbdffe. (A
finite computation; the b and d outputs agree.)

**Lemma H.** If two executions have the same X, share all words except w4,
w5, have (X3, X7, X11, X15) as above, w13 = W13 and w4 = W4 resp. W4', then
the digests agree on words 0, 2, 5, 7. *Proof.* C0, C1, C2 are identical;
C3 differs only in Y3, Y11 (Fact P). E0 and E2 read neither Y3, Y11, w4 nor
w5, so Z[0,5,10,15] and Z[2,7,8,13] agree, and o0, o2, o5, o7 use only
these. QED. The **residual** R is the XOR of the two digests on words 1, 3,
4, 6; these come from E1 and E3 only. A pair collides iff R = 0.

**The construction (60f94c5c).** Eight free words: the
six words of an *outer step* (vc, vd, D3.d1, S15, S9, w5), where vc = C0.c1
and vd = C0.d1 are the third and second values of the round-1 call C0 and
D3.d1 is the second value of D3; the *middle word* X2; and the *member*
y = Y4. For a call, a1, d1, c1, b1 are its first four values (Fact 1). Every
line is one assignment of the named call solved for its left side;
w4 = W4, w13 = W13, w14 = w15 = 0. All statements of this section hold for
every value of the eight words. The algorithm of Section 4 fixes
D3.d1 = X3, so that X14 = ROR(D3.d1 ^ X3, 8) = 0 and X9 = D3.c1 + X14 = D3.c1
in every outer step (as in 21252124).

**Step O (outer step; reads only the six words).**

    K2:  ka2 = K + W4; kd2 = ROR(ka2 ^ 55,16); kc2 = IV2 + kd2; kb2 = ROR(IV6 ^ kc2,12)       (constants)
         S2 = ka2 + kb2 + w5; S14 = ROR(kd2 ^ S2,8); S10 = kc2 + S14; S6 = ROR(kb2 ^ S10,7)
    D3:  D3.a1 = ROL(D3.d1,16) ^ S14; D3.c1 = S9 + D3.d1; D3.b1 = X3 - D3.a1; S4 = ROL(D3.b1,12) ^ D3.c1
         S3 = D3.a1 - S4; X14 = ROR(D3.d1 ^ X3,8); X9 = D3.c1 + X14; X4 = ROR(D3.b1 ^ X9,7)
    K3:  K3.d1 = ROL(S15,8) ^ S3; K3.c1 = IV3 + K3.d1; K3.b1 = ROR(IV7 ^ K3.c1,12); S11 = K3.c1 + S15
         S7 = ROR(K3.b1 ^ S11,7); K3.a1 = ROL(K3.d1,16) ^ 11; w6 = K3.a1 - IV3 - IV7; w7 = S3 - K3.a1 - K3.b1
    C0, D2:  X8 = vc - vd; vb = ROR(X4 ^ vc,12); D2.b1 = ROL(X7,7) ^ X8; D2.c1 = ROL(D2.b1,12) ^ S7; X13 = X8 - D2.c1

**Step M (middle; reads the outer step and X2, not y).**

    D2:  D2.a1 = X2 - D2.b1 - W13; D2.d1 = ROL(X13,8) ^ X2; S13 = ROL(D2.d1,16) ^ D2.a1
         S8 = D2.c1 - D2.d1; w12 = D2.a1 - S2 - S7
    K1:  K1.c1 = S9 - S13; K1.d1 = K1.c1 - IV1; K1.a1 = ROL(K1.d1,16); K1.b1 = ROR(IV5 ^ K1.c1,12)
         S1 = ROL(S13,8) ^ K1.d1; S5 = ROR(K1.b1 ^ S9,7); w2 = K1.a1 - IV1 - IV5; w3 = S1 - K1.a1 - K1.b1
    K0:  K0.b1 = ROL(S4,7) ^ S8; K0.c1 = ROL(K0.b1,12) ^ IV4; K0.d1 = K0.c1 - IV0; K0.a1 = ROL(K0.d1,16)
         S12 = S8 - K0.c1; S0 = ROL(S12,8) ^ K0.d1; w0 = K0.a1 - IV0 - IV4; w1 = S0 - K0.a1 - K0.b1

**Step Y (member; reads the outer step and y, not X2).**

    C0:  Y8 = ROL(y,7) ^ vb; Y12 = Y8 - vc; Y0 = ROL(Y12,8) ^ vd; va = Y0 - vb - w6; X12 = ROL(vd,16) ^ va
    D1:  gc = X11 - X12; gb = ROR(S6 ^ gc,12); X6 = ROR(gb ^ X11,7); gd = gc - S11; X1 = ROL(X12,8) ^ gd

**Step T (the trial).**

    C0:  X0 = va - X4 - w2
    D0:  fd = ROL(X15,8) ^ X0; fc = S10 + fd; X10 = fc + X15; fb = ROR(S5 ^ fc,12)
         X5 = ROR(fb ^ X10,7); fa = ROL(fd,16) ^ S15; w8 = fa - S0 - S5; w9 = X0 - fa - fb
    D1:  ga = ROL(gd,16) ^ S12; w10 = ga - S1 - S6; w11 = X1 - ga - gb

**Step S2.** w4 = W4 in A and w4' = W4' in B; w5' = w5 + (W4 - W4') = w5 + delta,
that is w5 - 8 (Lemma L); w13 = W13 and w14 = w15 = 0 in both.
**Step S3.** A = first 55 bytes of LE(w0..w15); B = first 63 bytes of the
same words with w4', w5'.

**Lemma S/F/Y.** For all eight words: K0, K1, K2 (length 55), K3 map the
initial state to (S0..S15); D0, D1, D2, D3 map S to (X0, X5, X10, X15),
(X1, X6, X11, X12), (X2, X7, X8, X13), (X3, X4, X9, X14); and C0 on
(X0, X4, X8, X12; w2, w6) has values va, vd, vc, vb and outputs
(Y0, y, Y8, Y12). The lines of step O read only the six words, those of
step M not y, those of step Y not X2. *Proof.* Each call's eight
assignments are lines above solved for one term, in order: K2 (all eight
forwards), D3 (D3.a1, D3.c1, D3.b1 from a2 = X3, S4, S3, X14, X9, X4), K3
(K3.d1, K3.c1, K3.b1, S11, S7, K3.a1, w6, w7), D2 (X8 with C0, D2.b1, D2.c1,
X13, D2.a1, D2.d1, S13, S8, w12), K1 (K1.c1, K1.d1, K1.a1, K1.b1, S1, S5,
w2, w3), K0 (K0.b1, K0.c1, K0.d1, K0.a1, S12, S0, w0, w1), C0 (vb, X8, Y8,
Y12, Y0, va, X12, X0), D1 (gc, gb, X6, gd, X1, ga, w10, w11), D0 (fd, fc,
X10, fb, X5, fa, w8, w9). Every name is assigned once and only from earlier
lines or the eight words; X3, X7, X11, X15 enter as the a output of D3, the
b output of D2, the c output of D1 and the d output of D0. By Fact 1 the
names are the executions of the calls. The lemma is also
checked on real messages by both experiments and the self-test
(Sections 5, 6). QED.

**Theorem 1.** For all eight words, A and B are distinct messages of 55 and
63 bytes whose complete 2-round digests agree on words 0, 2, 5, 7, and
Y4 = y in both. *Proof.* Bytes 55..63 of the block are zero (w13 top byte,
w14, w15), so A and B are honest messages with these blocks. By Lemma
S/F/Y round 0 on A leaves X with (X3, X7, X11, X15) the constants; by Lemma
L B has the same X; Lemma H gives the four digest words; C0 reads only
shared words, so Y4 = y in both. The lengths differ. QED. Each of the eight
words is a value of the forward computation of A (two values of C0, one of
D3, two state words of S, a message word, a word of X and Y4), so distinct
eight-word inputs give distinct messages A.

## 3. Class, sub-class S8, rule A, the beta filter and the residual words

**Class (Lemma Q, c66f230d).** E3's first assignment is e1 = Y3 + Y4 (for B
Y3' + Y4, w15 = 0) and its second h1 = ROR(Y14 ^ e1, 16), so
eta = h1 ^ h1' = ROR(e1 ^ (e1 + DY3), 16) with DY3 = Y3' - Y3 = fdb77cfd is a
function of Y4. With eta = 830303cf, the class is the set of Y4 with
(e1 AND 03cf8303) = 030c0303: since (e ^ x) - e = 2((~e) AND x) - x, the
condition e1 ^ (e1 + DY3) = x = ROL(eta,16) = 03cf8303 reads
2((~e1) AND x) = DY3 + x = 01870000, which fixes the 13 bits of e1 on x
(bit 31 is not in x) and leaves 19 free; 524,288 members.

**Sub-class S8 (winglock, 2bb5d604).** S8 is the set of class members whose e1 = Y3 + Y4
also has bits 2 and 3 equal to 1 and bit 21 equal to bit 26: 2^16 = 65,536
members (three linear conditions on free bits of e1). Member number i,
0 <= i < 2^16, has e1 = 030c0303 | 0000000c with the bits of i placed at the
free positions in the order 14, 30, 31, 4, 5, 6, 7, 10, 11, 12, 13, 20,
21, 27, 28, 29, then bit 26 set equal to bit 21; Y4 = e1 - Y3. (The order
is that of 2bb5d604, fixed before any stage measurement and not changed
since. In the order S2K14 of Section 4 a batch holds one member, so the
member order does not decide which trials share a batch.)

**Lemma T.** For a context and y in S8 (a subset of the class), the pair
of Theorem 1 has eta = 830303cf. (Fact P gives the a inputs Y3, Y3' of E3;
Y14 and w15 are shared.)

**Rule A (c66f230d).** h1 (E3, message A) satisfies rule A when bits 0, 16,
17 are 0, bit 1 is 1 and bits 2, 3 differ (probability 2^-5 for a uniform
word). **Lemma A.** With z = a2 ^ d1 of C2, ROL(h1, 24) = z ^ ROL(e1, 8)
(sixth assignment of C2: Y14 = ROR(z, 8)). The e1 bits entering (0, 1, 16,
17, 18, 19) are fixed by the class to 1, 1, 0, 0, 1, 1, so rule A holds iff
z24 = 0, z25 = 1, z8 = 1, z9 = 1 and z26 != z27.

**Lemma N (c66f230d).** With beta = b1 ^ b1' and eps = c2 ^ c2' of E1 and
n = eps ^ ROL(beta ^ eps, 1) ^ eta, n = D3 ^ ROL(D6, 8), where D3, D6 are
the XOR differences of digest words 3 and 6. So R = 0 implies n = 0.
*Proof.* o3 = Z3 ^ Z11 is E3's a and E1's c output, so D3 = (e2 ^ e2') ^ eps;
o6 = Z6 ^ Z14 is E1's b and E3's d output, b2 ^ b2' = ROR(beta ^ eps, 7)
and h2 ^ h2' = ROR(eta ^ e2 ^ e2', 8); rotating D6 left by 8 and adding D3
cancels e2 ^ e2'. QED.

**Beta filter (winglock, 2bb5d604).** E1's a1 and d1 are shared by A and B, c1 = Y11 + d1
and c1' = Y11' + d1 = c1 + DY11 with DY11 = 0a08818b, so
beta = ROR(c1 ^ (c1 + DY11), 12) is a function of c1. The filter passes a
trial when (c1 AND 00098188) = 00008000 (6 bits, rate 2^-6). Let
T6 = {18b0e098, 18b1a098, 18d0e098, 18d1a098, 18b3e098, 18d3e098}.

**Lemma B.** Every c1 with beta in T6 passes the filter. *Proof.* Put
x = ROL(beta, 12). Bit i of c1 ^ (c1 + D) is D_i ^ carry_i, so the carries
are carry_i = x_i ^ D_i; carry_{i+1} = maj(c1_i, D_i, carry_i), so where
D_i = carry_i the next carry must equal D_i (else no c1), and where
D_i != carry_i bit i of c1 equals carry_{i+1}. For each beta in T6 the
carries are consistent and the fixed bits of c1 include 3, 7, 8, 15, 16, 19
with values 0, 0, 0, 1, 0, 0. This is a finite computation on six words
(function `beta_conditions` of the program; the experiment `class-filter`
returns it as `lemma_b = 6`). It was also checked over all 2^32 values of
c1: exactly 2^21, 2^21, 2^21, 2^21, 2^19, 2^19 values give the six betas,
all of them pass, and 2^26 values pass the filter in all. QED.

**Lemma D (residual words, winglock).** For a trial write (a1, d1, c1, b1, a2,
d2, c2, b2) for E1 and (e1, h1, g1, f1, e2, h2, g2, f2) for E3 on message A,
primes for B. Then Z1, Z12, Z11, Z6 are E1's a2, d2, c2, b2 and Z3, Z14, Z9,
Z4 are E3's e2, h2, g2, f2, so the XOR differences of digest words 1, 3, 4, 6
are

    D1 = (a2 ^ a2') ^ (g2 ^ g2')          D3 = (e2 ^ e2') ^ (c2 ^ c2')
    D4 = ROR(f1 ^ f1' ^ g2 ^ g2', 7) ^ (d2 ^ d2')
    D6 = ROR(b1 ^ b1' ^ c2 ^ c2', 7) ^ (h2 ^ h2')

and R = 0 iff all four are 0. In E1, a1 and d1 are shared, c1' = Y11' + d1,
b1' = ROR(Y6 ^ c1', 12) and a2' = a1 + b1' + w5 + delta. In E3, Y4, Y9, Y14
and w8 are shared, e1' = Y3' + Y4 and h1' = h1 ^ eta with eta = 830303cf
(Lemma T), so g1' = Y9 + h1'. *Proof.* The output assignments of G and the
digest o[i] = Z[i] ^ Z[i+8]; f2 = ROR(f1 ^ g2, 7), b2 = ROR(b1 ^ c2, 7), and
ROR distributes over XOR. QED.

**Lemma D' (test words, winglock).** With P = a2 ^ a2', the word
W4 = (f1 ^ f1') ^ P ^ ROR(P, 1) equals ROL(D4, 7) ^ D1, so R = 0 iff
D1 = D3 = W4 = D6 = 0. *Proof.* d1 is shared, so d2 ^ d2' =
ROR(d1 ^ a2, 8) ^ ROR(d1 ^ a2', 8) = ROR(P, 8) and ROL(D4, 7) =
f1 ^ f1' ^ g2 ^ g2' ^ ROR(P, 1); XOR with D1 = P ^ g2 ^ g2' gives W4. The map
(D1, D4) -> (D1, ROL(D4, 7) ^ D1) is invertible. QED. Also
e2' = e1' + f1' + w8 = (e1 + w8) + f1' + DY3 with DY3 = Y3' - Y3, and
w8 = fa - S0 - S5 with fa = ROL(fd, 16) ^ S15 (D0, step T).

**Lemma E (early-exit word, new).** For every trial, W4 = P ^ ROR(P, 1) ^
ROR(g1 ^ g1', 12), with P = a2 ^ a2' of E1 and g1 = Y9 + h1, g1' = Y9 + h1'
of E3; so R = 0 implies W4 = 0. *Proof.* E3 is G(Y3, Y4, Y9, Y14; w15, w8),
whose fourth assignment is f1 = ROR(Y4 ^ g1, 12); for B it reads
f1' = ROR(Y4 ^ g1', 12) with the same Y4 (Theorem 1). ROR distributes over
XOR, so f1 ^ f1' = ROR(g1 ^ g1', 12), and Lemma D' gives the formula and,
since R = 0 iff D1 = D3 = W4 = D6 = 0, the implication. QED. Stage C
(Section 5) computes this W4 for all seven lanes from C1 and E3 to g1, g1'
(Y1, Y13, Y9, h1, h1') and E1 to a2, a2'; it needs neither f1, f1', e2, h2,
g2 nor the words D1, D3, D6. The self-test compares it with ROL(D4, 7) ^ D1
of the two real digests in every lane.


**Lemma A3 (stage-A test with a folded constant, c19feef).** For 32-bit words
a2, d1 put z = a2 ^ d1, j = (d1 >> 24) AND 15 and

    K' = (d1 AND 00000300) + F(j),   F(j) = 2^26 + (1 - j_0) 2^24 + j_1 2^25 + (j_2 XOR j_3) 2^27

(j_k the bits of j, that is bits 24 + k of d1). Then z satisfies the five
conditions of Lemma A (z8 = 1, z9 = 1, z24 = 0, z25 = 1, z26 != z27) iff
bits 8, 9, 24, 25 and 27 of s = (a2 + K') mod 2^32 are all 1. *Proof.* K'
has no bits below 8, so no carry enters bit 8, and s_8 = a2_8 XOR d1_8 =
z8. If z8 = 1 no carry leaves bit 8 (a2_8 and K'_8 = d1_8 differ), so
s_9 = z9, and if z9 = 1 no carry leaves bit 9; K' is 0 on bits 10..23, so
no carry reaches bit 24. Then s_24 = a2_24 XOR (1 - d1_24) = 1 - z24, and a
carry leaves bit 24 only if a2_24 = 1 and d1_24 = 0, i.e. z24 = 1; if
z24 = 0, s_25 = a2_25 XOR d1_25 = z25, and a carry leaves bit 25 only if
a2_25 = d1_25 = 1, i.e. z25 = 0. If z25 = 1, bit 26 receives no carry and
K'_26 = 1, so s_26 = 1 - a2_26 and the carry into bit 27 is a2_26; with
K'_27 = d1_26 XOR d1_27, s_27 = a2_27 XOR d1_26 XOR d1_27 XOR a2_26 =
z26 XOR z27. So if all five conditions hold, the five bits of s are 1; and
if the five bits of s are 1, the argument read in order (s_8 = z8 = 1,
s_9 = z9 = 1, s_24 = 1 - z24 = 1, s_25 = z25 = 1, s_27 = z26 XOR z27 = 1)
gives the five conditions. QED. Lemma A3 was also checked exhaustively
(all 64 patterns of the six bits of d1 and all 2^20 values of bits 8..27 of
a2, each with four fillings of the other bits: `lemmaA3_check.c`, no
disagreement in 2^28 cases) and the shipped self-test repeats it on 16,384
constructed cases.

*Use in stage A.* In the order S2K14 (Section 4) a lane holds the trial
with C2.a1 = r 2^14 + i (r = 7g + l < 2^18, i < 2^14), so C2.d1 =
ROR(C2.a1, 16) = i 2^16 + D with D = ROR(r 2^14, 16) = (r >> 2) +
(r AND 3) 2^30 (r >> 2 < 2^16, so the three parts occupy bits 0..15,
16..29 and 30, 31 and no addition carries): its bits 8, 9 are bits 10, 11
of r (those of D) and its bits 24..27 are bits 8..11 of i, constant for the
256 positions i of a block. The stage-A register is
Z = T1 + X6K + b1 with T1 = X2 + w7 + w0 (table word, below 2^32),
X6K = X6 + K' (member register plus the block's constant) and b1 = C2.b1;
since C2.a2 = C2.a1 + b1 + w0 and C2.a1 = X2 + X6 + w7, Z = C2.a2 + K'
(mod 2^32), and Z < 2^36. With ALLA = 0B000300 (bits 8, 9, 24, 25, 27),
pA = (Z AND ALLA) + (2^32 - ALLA) has bit 32 equal to 1 iff Z AND ALLA =
ALLA (Z AND ALLA <= ALLA < 2^28), i.e. iff the trial satisfies rule A
(Lemmas A, A3), and pA < 2^33.

**Lemma F2 (stage-B test, c19feef).** Let KF = MF AND NOT VF = 00090188 (bits
3, 7, 8, 16, 19). Then (c1 AND MF) = VF iff ((c1 + KF) mod 2^32) AND MF =
MF. *Proof.* Write s = c1 + KF. KF has no bits below 3, so s_3 = 1 - c1_3,
with a carry out of bit 3 iff c1_3 = 1. If c1_3 = 0, bits 4..6 receive no
carry and are those of c1, and the same argument gives s_7 = 1 - c1_7 and
then s_8 = 1 - c1_8 (each without carry when the bit of c1 is 0), s_15 =
c1_15 (KF_15 = 0, no carry), s_16 = 1 - c1_16, s_19 = 1 - c1_19. So when
c1 passes the filter (bits 3, 7, 8, 16, 19 zero and bit 15 one) the six
bits of s are 1; conversely if they are 1, reading the bits in increasing
order gives c1_3 = 0 (no carry in), hence no carry out, c1_7 = 0, ..., and
c1_15 = 1, c1_16 = c1_19 = 0. QED. (Also checked on 3 * 2^20 cases by
`lemma_check.py`, no disagreement.) The stage-B register is C1K = D1 +
(Y11 + KF) = c1 + KF (mod 2^32); pF = (C1K AND MF) + (2^32 - MF) has bit
32 equal to 1 iff the trial passes the filter, and xF = pF AND xA (xA from
stage A: bits 32 only) has bit 32 of a lane equal to 1 iff the lane passes
rule A and the filter.

**Stage decisions.** With B32 the word holding 2^32 in every lane,
xA = pA AND B32 holds exactly the seven bits 32; xA is nonzero iff some lane
passes rule A (c19feef tested it per batch; 5ca02dfb per pair, Lemma P; here
per quad, Lemma P4 of Section 5), the compare-and-branch of stage B (xF
against 0) is taken iff some lane passes rule A and the filter, and that of
stage C ((((W4 AND M) + M) AND xF) against xF) iff some lane passes rule A
and the filter and has W4 = 0. In the last group of a member (g = 37,449)
B32 holds 2^32 only in lane 0, the one distinct trial of that group, so
lanes 1..6 (which repeat trials of group 0, Section 4) take no part in any
decision.

## 4. Algorithm

Constants: V = 1,057,885 values of vd (v106: the smallest V that certifies
success 0.39 with F = 132,392,960, Section 7); N = V * 2^80 = 2^100.0128
trials in V * 2^62 * 37,450 batches; p_B = 36,631,290,006,031 / 183,824,600,268,800 =
0.1992731 (Section 8.2); premises theta_B = 0.377, theta_C = 1.003 and
rho_R = 2^-24 of H1 (ii) (Section 8.2) and the budgets (the factor
6001/6000 is from 5266c5ce)

    E_B = ceil(theta_B * 6001/6000 * p_B * V * 2^62 * 37,450) = 13,728,159,670,934,448,543,084,476,720 = 2^93.4711
    E_C = ceil(theta_C * 6001/6000 * N * 2^-11)             = 626,442,868,337,775,176,894,157,573 = 2^89.0173
    E_R = ceil(rho_R * 6001/6000 * N)                        = 76,241,352,643,458,196,807,790 = 2^76.0130

(V * 2^62 * 37,450 = 2^97.21 is the number of batches: V * 2^32 outer steps
of 2^16 members, 37,450 groups and 2^14 positions, about N / 7. 5ca02dfb's
proof writes 2^64 in this product, a misprint carried over from c19feef's
order with 2^16 positions; its E_B, mu_H and ledger use 2^62, as ours do.)

*Order S2K14.* Fix an outer step and a member y, and let c = X6 + w7 (X6
from step Y, w7 from step O). For a group g < 37,450, a lane l < 7 and a
position i < 2^14 put r = 7g + l and

    C2.a1 = r 2^14 + i,   X2 = (C2.a1 - c) mod 2^32,   C2.d1 = ROR(C2.a1, 16) = i 2^16 + D_r,   D_r = (r >> 2) + (r AND 3) 2^30

(C2.a1 = X2 + X6 + w7 by step T, and X14 = 0, so C2.d1 = ROR(C2.a1, 16)).
For r < 2^18 and i < 2^14 the map (r, i) -> X2 is a bijection onto all
2^32 values, so the groups g < 37,449 (r up to 262,142 = 7 * 37,449 - 1)
and lane 0 of the last group (r = 262,143 = 2^18 - 1) hold every trial of
the member exactly once; lanes 1..6 of the last group are given
r - 2^18 = 0..5, i.e. they repeat the trials of lanes 0..5 of group 0 at
the same position, and they are masked out of every stage decision
(Section 3). A *batch* is (outer step, member, group, position); there are
2^16 * 37,450 * 2^14 = 37,450 * 2^30 batches per outer step; 37,449 of
every 37,450 hold seven distinct trials and the rest one. (c19feef's order
S2K is the same with 2^16 in place of 2^14: 9,363 groups of 2^16
positions, D_r = r.) Since 7 (g + 4) = 7g + 28 and 28 = 4 * 7, D of group
g + 4 is D of group g plus 7 in every lane (r AND 3 is unchanged and
r >> 2 grows by 7), so four D slots, one per residue of g mod 4, each
advanced by 7 after use, supply D for every group but the last.

1. Once: the list of the 65,536 members of S8 in the order of Section 3,
   the 64 block constants F_b = F(b AND 15) and G_b = 2^32 + 1 - F_b
   (Lemma A3), the four words D0S_k = (D_{7k}, .., D_{7k+6}) (k < 4), DLAST
   = (D_{262143}, D_0, .., D_5) and B32_01 (2^32 in lane 0); the budget
   registers cB = E_B, cC = E_C and the budget word cR = E_R in memory.
2. For each vd < V and each w5 in 0..2^32-1 (an *outer step*): draw one
   fresh uniform 256-bit word and take vc, S15, S9 from its 32-bit words 0
   to 2; set D3.d1 = X3 (so X14 = 0); run step O. Build the *X2 table*: for
   a = 0, 1, .., 2^32 + 2^14 - 1 the table word T[a], whose lane l holds, for
   X2 = (a + l 2^14) mod 2^32, the eight words -w2, X2 + w7 + w0, S5, w3,
   S12, w12 - S1 - S6, -S1 - S6 and -S0 - S5 of step M. Then for each member
   y: the member step (step Y for y, c = X6 + w7, the member registers,
   the four D slots := D0S_0..D0S_3). Then for each group g = 0, .., 37,449:
   - halt the run with failure if cB < 2^14 or cC < 2^14;
   - set the group registers from the lanes D_r of C2.d1 at i = 0 (read
     from D slot g mod 4, which is then advanced by 7; the last group
     DLAST, and B32 := B32_01 for it);
   - for each quad of positions (4q, .., 4q + 3), q = 0, 1, .., 4,095
     (before positions 256 b, b < 64, the block constants F_b, G_b enter
     two registers; a quad never straddles a block) take the batches of its
     four positions; the batch at position i has as lane l the trial (vd,
     w5, X2 = ((7g + l) 2^14 + i - c) mod 2^32, y) and reads the table word
     a = base_g + i, base_g = (7g 2^14 - c) mod 2^32 (a < 2^32 + 2^14).
     Every batch runs stage A; the quad runs one quad test, taken iff some
     lane taking part in one of its four batches passes rule A (Lemma P4).
     If it is taken, the hit tree finds the batches of the quad with a
     passing lane taking part; each of them, in order of position,
     subtracts 1 from cB and runs stage B. If some lane passes rule A and
     the filter, it subtracts 1 from cC and runs stage C, which computes the
     word W4 of Lemma E for all seven lanes and tests whether some lane that
     passes rule A and the filter has W4 = 0 (the early-exit test). If so, the
     *continuation*: halt the run with failure if cR = 0; else subtract 1
     from cR, recompute the batch from its table words (stages A and B and
     the words D1, D3, W4, D6 of Lemmas D and D') and test whether some lane
     that passes rule A and the filter has all four words zero; if so, step
     3.
3. Take the first such lane, recompute its trial in scalar form from (vd,
   w5, X2, y) (steps O, M, Y, T), build A, B (S2, S3), evaluate both
   complete digests, compare, output the pair if they are equal, and halt
   in either case.
4. Halt with failure when all trials are done.

There are N = V * 2^32 * 2^16 * 2^32 trials, the same as in c19feef, all
distinct pairs for every value of the coins (vc, S15, S9 of each outer
step) (Theorem 1: two trials differ in vd, w5, X2 or y, and each is a value
of the forward computation of A). Step 3 runs at most once. Each group has
at most 2^14 entries of stages B and C and starts only if both registers
hold at least 2^14, so at most E_B batches complete stage B and at most E_C
complete stage C, and the registers never go below 0; a continuation starts
only if cR > 0, so at most E_R continuations run.

**Completeness.** Let a trial be good (R = 0, rule A, filter). It is held
by a lane that takes part in the decisions (lane 0 of the last group, or
a lane of another group), so the quad test of its quad is taken and the hit
tree sends its batch to stage B (Lemmas A3, P4), it enters stage C (Lemma
F2), its word W4 is 0 (Lemma E), so the early-exit test branches to the
continuation, which computes its four words exactly (Lemmas D, D', Section
5), and the exact test is taken, and step 3 outputs a pair with equal complete
digests (R = 0 is equality of the two digests, Lemmas H, D'), unless a
budget has halted the run before. A trial with R = 0 that fails rule A or
the filter is not looked for; Section 7 does not count it.

**What the shipped program holds.** It contains the counted pieces (the
outer step with its random word, the table entry and one table word, the
member step, the end of a group and the set-up of the next, the block
update, the counted quad (stage A of its four positions, the quad test, the
hit tree with the spill of its leaf, stages B and C of each batch of the
leaf, the continuation with its register spill) with the three budgets),
the member list, the block constants, the D slot words, and the ledger with
E_B, E_C and E_R. The loops over vd, w5, a, y, g, b and q and step 3 are
defined by this text; their counts are in Section 9.

## 5. The counted pieces on a 64-register machine

A packed 256-bit word holds seven 36-bit lanes (offsets 0, 36, .., 216),
each representing a value modulo 2^32 with four guard bits. A rotation by
r is PROR = ((z >> r) AND A_r) OR ((z << (32 - r)) AND B_r), 5 operations,
reading only the low 32 bits of each lane; for r = 16 it is
((z >> 16) AND A_16) OR ((z AND A_16) << 16), also 5 operations (A_16 =
2^16 - 1 per lane, so the second part stays below 2^32 and no B_16 is
needed). x - y with constant x is (y XOR M) + (x + 1) (M = 2^32 - 1 per
lane); subtracting a constant is adding its negation. Every executed
primitive (add, xor, and, or, shift, compare, branch, load, store, random
word) counts 1; shift amounts, load offsets and branch targets are
instruction fields. The machine model is the 256-bit word RAM of the cost
model with 64 registers.

**The quad and its stages.** The loads are the eight words of the table
entry a (at offsets 8 i + q from the group's pointer, instruction fields in
the unrolled group body) and eight words kept in memory (A_1, B_1 and DY3,
stored once; S15, w5 and w5 + delta, stored by the outer step; y and
e1 = y + Y3, stored by the member step), loaded where they are read; every
other operand is a register. Every execution of a stage executes the same
operations. Positions 4q .. 4q + 3 (j = 0..3) form a quad; E = (S10 + X15) +
C2.d1 of the next position.

| Stage | Computes | Ops |
|---|---|---:|
| A | per position j: load -w2 (1); X0 = XA + (-w2), fd = X0 ^ ROL(X15,8) (2); c1 = fd + E = X10 + C2.d1 (1); E = E + 2^16 for the next position (1) | 5 |
| A | C2: b1 = ROR(X6 ^ c1, 12) (6); load X2 + w7 + w0 (1); Z = (X2 + w7 + w0) + X6K + b1 = C2.a2 + K' (2) | 9 |
| A | rule-A flag (Lemma A3): tA = Z AND ALLA, pA_j = tA + (2^32 - ALLA) (2) | 2 |
| A | quad test, once per quad (Lemma P4; a quarter charged to each batch): U3 = pA_0 OR pA_1, U12 = pA_2 OR pA_3, U15 = U3 OR U12 (3), x15 = U15 AND B32 (1); compare with 0, branch (2) | 1.5 |
| H | hit tree, only after a taken quad test: per test, the OR of two built words if new (1), AND B32 (1), compare with 0, branch (2); the flag words of the leaf; at leaf {0,1,2,3} the spill of batch 3's five words (10) | at most 10 per stage-B entry |
| B | budget: cB = cB - 1 (1) | 1 |
| B | C2.d1 = E + DN_j, DN_j = -(S10 + X15) - (4 - j) 2^16 (1); C2.a2 = Z + nKp, nKp = 2^33 - K' (1); z = a2 ^ d1 (1); X10 = fd + (S10 + X15) (1) | 4 |
| B | Y14 = ROR(z,8) (5), Y10 = c1 + Y14 (1), Y6 = ROR(b1 ^ Y10,7) (6); fc = X10 + (-X15) (1); load S5 (1); X5 = ROR(ROR(fc ^ S5,12) ^ X10,7) (12) | 26 |
| B | load w3 (1); C1: a1 = X1 + X5 + w3 (2), d1 = ROR(a1 ^ X13,16) (6), c1 = d1 + X9 (1), b1 = ROR(c1 ^ X5,12) (6) | 16 |
| B | load S12 (1); ga = R ^ S12 (1); sY = a1 + b1 + ga = Y1 + S1 + S6 (2); load w12 - S1 - S6 (1); E1: a1 = sY + Y6 + (w12 - S1 - S6) (2); d1 = ROR(a1 ^ Y12,16) (6); C1K = d1 + (Y11 + KF) (1) | 14 |
| B | test of rule A and the filter (Lemma F2): wF = C1K AND MF, pF = wF + (2^32 - MF), xF = pF AND xA (3); compare with 0, branch (2) | 5 |
| C | budget: cC = cC - 1 (1); load -S1 - S6 (1); Y1 = sY + (-S1 - S6) (1); Y13 = ROR(C1.d1 ^ Y1,8) (6); Y9 = C1.c1 + Y13 (1); load e1 (1); h1 = ROR(Y14 ^ e1,16) (6), h1' = h1 ^ eta (1); g1 = Y9 + h1, g1' = Y9 + h1' (2) | 20 |
| C | G = g1 ^ g1' (1), ROR(G, 12) = f1 ^ f1' (5; Lemma E) | 6 |
| C | E1 for A and B: c1 = d1 + Y11, b1 = ROR(c1 ^ Y6, 12) (7), c1' = d1 + Y11', b1' (7); load w5 (1), a2 = a1 + b1 + w5 (2); load w5 + delta (1), a2' (2); P = a2 ^ a2' (1) | 21 |
| C | load A_1, B_1 (2); W4 = ROR(P,1) ^ P ^ ROR(G,12) (7) | 9 |
| C | early exit (Lemma E): T = W4 AND M, u = T + M, v = u AND xF (3); compare v with xF, branch (2) | 5 |
| K | continuation, only when the early-exit test finds a lane with W4 = 0: budget word cR (load, compare with 0 and branch to the halt, subtract 1, store: 5); the batch recomputed: stage A to its flag word (18), stage B without the count (65), C1 and E3 to g1, g1' (19), E1 to P (21), d2, d2', c2, c2', Q (15), ROR(b1 ^ b1' ^ Q, 7) (7), f1, f1' (13 with the load of y), fa = ROL(fd,16) ^ S15 (7 with its load), e1 + w8, e2, e2' (7 with the loads of -S0 - S5 and DY3), h2, h2', g2, g2' (14), D1, D3 (4), W4 (10 with the loads of A_1, B_1), D6 (2), OR of the four (3), the exact test (5); the waiting batches' words stored and reloaded (at most 20) | at most 235 |
| | **stage A 70 per quad (17.5 per batch), stage B 66, stage C 61, hit tree at most 10 per stage-B entry, continuation at most 235** | |

ALLA = 0B000300, MF = 00098188, KF = 00090188 in every lane. The quad-test
branch is taken (to the out-of-line hit tree and the stages of the quad)
iff some lane taking part in one of the four batches passes rule A
(Lemma P4); the stage-B branch falls through to stage C iff some lane passes
rule A and the filter; the stage-C branch is taken (to the continuation)
iff some lane passing rule A and the filter has W4 = 0; the continuation's
branch is taken (to step 3) iff some such lane has all four words zero.
Every other path jumps on to the next batch of the leaf or the next quad.

*E across the quad.* Stage A adds 2^16 to E after each position's c1, so
after the quad E is 4 * 2^16 past the quad's first position on every path
and batch j's C2.d1 = E + DN_j with the four per-outer registers DN_j =
-(S10 + X15) - (4 - j) 2^16 (DN_3 is 5ca02dfb's -S10 - X15 - 2^16; DN_0,
DN_1, DN_2 are new). The self-test checks E - (S10 + X15) = ROR(C2.a1, 16)
in every lane of every batch and E after the quad.

*The quad test (Lemma P4).* Let pA_0, .., pA_3 be the flag words of the four
batches of a quad. **Lemma P4.** For every set W of batches of the quad,
bit 32 of (OR over j in W of pA_j) in a lane is the OR of the flags of the
batches in W,
and (OR over j in W of pA_j) AND B32 is zero iff no lane taking part in the
decisions passes rule A in a batch of W; in particular the quad test is
taken iff at least one batch of the quad has such a lane, and
pA_j AND B32 is c19feef's per-batch flag word xA. *Proof.* As Lemma P of
5ca02dfb: tA = Z AND ALLA lies in [0, ALLA], so pA_j lies in
[2^32 - ALLA, 2^32] and equals 2^32 iff tA = ALLA, i.e. (Lemma A3) iff
rule A holds; bits 33..35 are 0, so no lane is polluted and OR acts on each
bit separately. B32 has bit 32 set exactly in the lanes taking part (all
seven lanes, or lane 0 in the last group; the four positions of a quad lie
in one group and one block, since 4 divides 256). QED.

*The hit tree.* After a taken quad test the leaf S (the set of batches of
the quad with a passing lane taking part) is found by tests of words
x_W = U_W AND B32, U_W = OR over j in W of pA_j, each nonzero iff S meets W
(Lemma P4): test x3 (W = {0,1}). If x3 != 0: test x1 (pA_0); if x1 != 0,
form U14 = pA_1 OR U12 and test x14 ({1,2,3}); if x14 != 0 test x2, then
x4, then x8 (not needed when x2 = x4 = 0, which leaves S = {0,3}), which
leaves S in {0,1,2,3}, {0,1,2}, {0,1,3}, {0,1}, {0,2,3}, {0,2} or {0,3};
if x14 = 0, S = {0}. If x1 = 0 (so batch 1 has a passing
lane): test x12; if nonzero test x4 and x8 (S = {1,2,3}, {1,2} or {1,3}),
else S = {1}. If x3 = 0: test x4 and x8 (S = {2,3}, {2} or {3}). For each
batch j of S the flag word xA_j = pA_j AND B32 is a tested word x_W with
W meeting S in j only (the other batches of W have no flagged lane taking
part), or, for S = {3}, computed (1 operation). The hit operations per leaf
are 10 ({0}), 9 ({1}), 9 ({2}), 7 ({3}), 19 ({0,1}), 19 ({0,2}), 16
({0,3}), 15 ({1,2}), 12 ({1,3}), 9 ({2,3}), 19 for each three-batch leaf
except 15 ({1,2,3}), and 19 + 10 for {0,1,2,3}, whose 10 are the store of
batch 3's words zK, c1, b1, fd, xA after the tree and their reload before
its stage B (a register spill, see Registers); so each taken quad test
costs at most 10 operations per batch of its leaf, that is per stage-B
entry. An exhaustive search over trees of such tests built on the words
pA_j, U3 and U12 (the study's `hittree2.py`, a development tool, not
shipped) found no tree whose maximum per stage-B entry is below 10; the
tree is shipped as `TREE` and its correctness is checked by the pattern
tests below. The batches entering stage B are therefore exactly those that
c19feef's and 5ca02dfb's flows send there, with the same xA; stages B and C
and the budgets of stages B and C see exactly what they saw, and the
premises of H1 (ii) about these entries apply unchanged.

*Cost of the quad flow.* Not taken: 70 operations (4 * 16 for the four
positions up to their flags, 6 for the test). Taken: the same 70, then the
hit tree (at most 10 per stage-B entry, total at most 10 E_B for the run),
stage B for each batch of the leaf (66 each, at most E_B), stage C for each
batch with a lane passing rule A and the filter (61 each, at most E_C), the
continuation for each batch whose early-exit test finds a lane with W4 = 0 (at most 235 each, at
most E_R). Section 9 charges stage B at 76, stage C at 61 and the
continuation at 235 operations per budgeted entry. In the unrolled group
body the code for a quad holds the out-of-line hit tree and, for each of
its 15 leaves, stages B, C and the continuation of each batch of the leaf.

The lines of steps M, Y and T that the batch evaluates are those of Section
2 with the table and member words in place of their names: XA + (-w2) = va
- X4 - w2 = X0, R ^ S12 = ROL(gd,16) ^ S12 = ga, sY + (w12 - S1 - S6) + Y6 =
Y1 + Y6 + w12, and X6, X1, Y12, y as they stand; w9 and w11 are not needed
for R. Stage C is 5ca02dfb's stage C up to g1, g1' and a2, a2', followed by
the word of Lemma E instead of the four words of Lemma D'; the continuation
is 5ca02dfb's full stage C (without its accumulator) on the recomputed
batch.

*The early exit and the continuation.* After stage C a lane holds W4 of
Lemma E below 2^36; T = W4 AND M is its low 32 bits, bit 32 of u = T + M is 1
iff T != 0, and v = u AND xF equals xF iff every lane with rule A and the
filter has W4 != 0. So the branch (v against xF) is taken iff some lane
passing rule A and the filter has W4 = 0, which every good trial has
(Lemma E). The continuation recomputes the batch from E, the table words of
its position and the resident words (E is 4 * 2^16 past the quad's first
position, so C2.d1 = E + DN_j and c1 = fd + C2.d1 + (S10 + X15)), keeps
nothing of stage C, computes D1, D3, W4 = ROL(D4, 7) ^ D1 and D6 (Lemmas D,
D'), T = D1 OR D3 OR W4 OR D6, and tests the lanes of its own xF in the same
way: taken iff some lane with rule A and the filter has R = 0. Before it,
the words of the leaf's later batches that are in registers are stored,
and they are reloaded after it.

*The block update (4 operations per 256 positions).* Load F_b, X6K = X6R +
F_b; load G_b, nKp = NR + G_b. With X6R = X6 + (D AND 0300) and NR =
(D AND 0300) XOR M = 2^32 - 1 - (D AND 0300) (group set-up), X6K = X6 + K'
and nKp = 2^33 - K' for the K' of Lemma A3 of every lane at the 256
positions of block b (C2.d1 bits 8, 9 are those of D, bits 24..27 are
b AND 15, Section 3).

*The group set-up (13 operations; last group 11).* Budget halt test: cB and
cC each compared with 2^14 (an immediate) and a branch to the halt (4);
load the lanes D = (D_{7g+l}) from D slot g mod 4 (the slot's address is an
instruction field of copy g mod 4 of the group code; last group: load
DLAST, and load B32_01 into B32; 1 + 1); E = D + (S10 + X15) (1); load 0300
(1), DM = D AND 0300 (1), X6R = X6 + DM (1), NR = DM XOR M (1); except in
the last group, load 7, D + 7, store into the same D slot (3), which then
holds D of group g + 4 (Section 4). 5ca02dfb's set-up also loaded the
accumulator (1); there is none here. The self-test checks the stored word
against D + 7, and the shipped program's `dslot_test` replays the four
slots over all 37,449 full groups from D0S (every value read equals
(D_{7g+l})) and checks that the (r, i) of the groups cover all 2^32 values
of C2.a1 once.

*The group end (8 operations; after the last group 1).* The table pointer
p = 8 base_g (8 words per table entry) becomes (p + 7 * 2^17) AND
(2^35 - 1) = 8 base_{g+1} (2; the X2 table occupies word addresses 0 to
8 (2^32 + 2^14) - 1, entry a at words 8a to 8a + 7, so p is the absolute
address of entry base_g); the group counter is loaded, incremented,
stored and compared with 37,449, and a branch selects the last group's
code (its prologue loads DLAST and B32_01) (5); otherwise a jump to the
next copy ((g + 1) mod 4) of the group code (1). After the last group of a
member B32 is restored (load, 1). There is no block test (5ca02dfb: 4 per
group).

*Budgets.* cB and cC are registers holding E_B and E_C at the start of the
run; an entry of stage B or C subtracts 1 (1 operation); before each group
the run halts with failure if either holds less than 2^14. A group has at
most 2^14 entries of each stage, so no register goes below 0, stage B is
completed at most E_B times and stage C at most E_C times, and the run halts
only after more than E_B - 2^14 (or E_C - 2^14) entries. cR is a word in
memory holding E_R; each continuation loads it, halts the run with failure
if it is 0, subtracts 1 and stores it (5 operations, in the 235), so at most
E_R continuations run and the run halts on this budget only at the
(E_R + 1)-th.

*Lane bounds.* Static per-lane upper bounds for all inputs are tracked by
the program for every addition: below 4.25, 7.0, 9.0 and 9.0 times 2^32 in
stage A, stage B, stage C and the continuation, 2.0 and 1.99 times 2^32 in
the group set-up and the block update and 6.0 times 2^32 in the table word,
all below 2^36, so no carry leaves a lane (E = k4 + D + i 2^16 with
k4, D < 2^32 and i <= 2^14 stays below 2^33 + 2^30 in a group); XOR, AND and
PROR read only the low 32 bits of lanes or mask the rest. Table words,
member registers and the words kept in memory are reduced below 2^32 when
they are formed.

*Registers.* 40 registers are resident during the batches: the 7 rotation
masks A_16, A_12, B_12, A_8, B_8, A_7, B_7, 13 global constants (M,
ROL(X15,8), -X15, Y11, Y11', Y11 + KF, eta, ALLA, 2^32 - ALLA, B32, MF,
2^32 - MF, 2^16), 7 per outer step (S10 + X15, X13, X9 and DN_0..DN_3;
X14 = 0 needs none), 5 per member (XA = va - X4, X6, X1, R = ROL(gd,16),
Y12), 5 per group and block (E, X6R, NR, X6K, nKp), the table pointer and
the two budget registers. 5ca02dfb had 47: B_16, A_1, B_1, DY3, S15, w5,
w5 + delta, y, e1 and the accumulator are not resident here, and DN_0,
DN_1, DN_2 are new. The program counts registers on every path of the quad
code: for each of the 15 leaves the forced path (stage A, the quad test,
the tree to that leaf, its spill, and stages B, C and the continuation for
every batch of the leaf, the later batches' words stored before each
continuation and reloaded after it), counting the resident registers plus
every value (SSA version) live from its write to its last read; at an
instruction shared by several paths (stage A, the quad test and the tree
nodes, each identified by its place in the tree) it counts the union of the
values live on any of them. Every path of the staged flow is a subsequence
of the forced path of its leaf (it omits some stages C and continuations
with their stores and reloads), and dropping instructions can only shorten
live ranges, so the count bounds every path. The peak is 64 of 64, at the
quad test: the four batches' words zK, c1, b1, fd, the four flag words,
U3, U12, U15 and x15 are live. In stage B of batch 0 at leaf {0,1,2,3} the
three later batches' fifteen words would give 65; storing batch 3's five
words after the tree and reloading them before its stage B (the spill in
the hit tree's 29 operations) gives 64 there (without it, 65: broken copy
below). The other leaves peak at 60 (three batches) and 57 (one or two);
the continuation itself needs 57. The table build uses at most 36 registers,
the scalar member and outer steps fewer. A peak of 64 live values is enough
for an assignment to 64 registers without further spills: in program order
each new value takes a register that holds no live value; the shared
instructions are assigned once, with the union of the live sets, and every
path after a branch starts from values live at the branch, so a free
register always exists; a reload after the spill or a continuation writes
the register its word had before the store, which holds no live value then.

**The X2 table (per outer step).** Entry (28 operations): the nine masks for
rotations by 24, 20, 16, 12 and 7 (no B_16), M, 1 and six IV-derived
constants, the nine words of step O that step M reads, the X2 word (lanes
l 2^14 - 1) are loaded, and the pointer is reset. Each table word (94
operations): X2 = X2 + 1 per lane, AND M (2); the 21 lines of step M in all
seven lanes; the eight words -w2, X2 + w7 + w0, S5, w3, S12,
w12 - S1 - S6, -S1 - S6, -S0 - S5 reduced below 2^32 and stored (8 stores);
next word, compare, branch (3). 2^32 + 2^14 words per outer step (the last
2^14 repeat the first, so that a group's 2^14 consecutive entries never
wrap).

**The member step (per member, 120 operations, scalar).** Load y from the
member list and nine scalar words stored by step O (10); the lines of step
Y in scalar form (each 32-bit addition or subtraction counted 2 with its
mask, rotation 4, XOR 1); c = X6 + w7 and the pointer 8 ((-c) mod 2^32) of
group 0; e1 = y + Y3; the five member registers XA, X6, X1, R, Y12, each
broadcast to seven lanes (7 operations each), y and e1 broadcast and stored
(8 each); the four D slots := D0S_0..D0S_3 (load, store each: 8) and the
group counter := 0 (store); next member (3).

**The outer step (324 operations).** One fresh uniform 256-bit word (1) and
its words 0 to 2 as vc, S15, S9 (AND; shift and AND twice: 5); D3.d1 = X3
is an instruction constant (so ROL(D3.d1,16) is one too, X14 = 0 is not
computed and X9 = D3.c1); step O in scalar form (as above); the nine
packed words of the table entry and the ten per-outer words of the batch
(S10 + X15, X13, X9, S15, w5, w5 + delta, DN_0..DN_3), each broadcast to
seven lanes and stored (8 operations each); the nine scalar words of the
member step (C0.b1, -C0.c1, C0.d1, -C0.b1 - w6, ROL(C0.d1,16), S6, -S11,
-X4, w7), computed and stored; the next-w5 loop step and two stores (6);
after the table build, the loads of the seven per-outer registers and of
the 20 global batch constants (27; 5ca02dfb listed 7 and not the reload of
the constants, which the table build displaces).

*Self-test of the shipped program.* `python3 experiments/s8stage.py
--selftest 2000 9`, run from the repository root, builds 2,000 cases (the
context words from SHAKE-256 of the seed, then D3.d1 = X3 as in the
algorithm; the random word of the outer step holding the three coin words
in words 0 to 2 and random words 3 to 7; a member number (every seventh case
0 or 65,535), a group (every fourth case the last group, every ninth group
0, otherwise uniform below 37,449) and a position i (every sixth case 0,
16,383 or the first of a block); in every fifth case each context word is
0, 2^32 - 1 or random before D3.d1 is set). Each case runs the counted
outer step from the random word, the member step, for g > 0 the end of
group g - 1 from base_{g-1}, the set-up of group g (from the D-slot word
(D_{7g+l})), the block update of the position's block, the table entry and
the counted table words of the four positions of the quad that holds i
(from the previous word's X2 lanes), the counted quad forced (stage A, the
quad test, the hit tree to the leaf {0,1,2,3}, its spill, and stages B, C
and the continuation of all four batches computed whatever the decisions;
budgets changed only as in the staged flow), the same quad once more in the
staged flow on a copy of the machine, and after the last group its end;
every tenth case also runs the fifteen forced leaf paths on copies. It
checks: the outer step takes exactly the three coin words from the random
word, D3.d1 = X3 and X14 = 0, and every word it stores equals step O; the
member registers and stored words equal step Y and c, the pointer equals
8 base_g; E, X6R, NR and the stored next D (D + 7) equal their definitions,
X6K = X6 + K' and nKp = 2^33 - K' in every lane; each table word equals
step M for the seven X2 values a + l 2^14; E - (S10 + X15) = ROR(C2.a1, 16)
and C2.a1 = (7g + l) 2^14 + i + j in every lane of batch j, and E after the
quad; and for every lane of the four batches it builds the trial's messages
A, B by steps O, M, Y, T, S2, S3, compresses them with the program's own
2-round compression and with `verifier/blake3.py blake3(m, 2)`, and checks:
X3, X7, X11, X15 after round 0 are the constants, digest words 0, 2, 5, 7
agree, Y4 = member in S8 for both, eta = 830303cf; bit 32 of pA_j is 1 iff
h1 of E3 satisfies rule A; bit 32 of xF (stage B and continuation) is 1 iff
the lane takes part in the decisions and satisfies rule A and the filter on
c1 of E1; W4 of stage C equals ROL(D4, 7) ^ D1 and the continuation's four
words equal D1, D3, ROL(D4, 7) ^ D1 and D6, computed from the XOR of the two
digests on words 1, 3, 4, 6, their OR equals T, and bit 32 of the lane's
indicator is 1 iff the digests differ; the quad decision equals 'some lane
taking part in one of the four batches passes rule A' and each batch's
decisions equal 'some lane taking part passes rule A', '.. and the filter',
'.. and has W4 = 0' and '.. and has equal digests'; the staged flow on the
copy reaches the leaf of the batches with a passing lane, makes the same
decisions, subtracts from cB, cC and cR exactly once per entry, executes 70
stage-A operations for the quad, 66 per stage-B entry, 61 per stage-C
entry, at most 10 hit-tree operations per stage-B entry and at most 235 per
continuation, and leaves E, cB, cC and cR equal to the forced run's. On the
leaf paths it checks that each reaches its leaf, executes 70, the hit-tree
operations listed above, 66 and 61 per batch and at most 235 per
continuation, and that the register count of all fifteen paths (with the
union at shared instructions) is at most 64. The D-slot test
(`dslot_test`) replays the four slots from D0S over all 37,449 full groups,
checks DLAST, checks D_r = (r AND 3) 2^30 + (r >> 2) on every 97th r, and
checks that the groups' r values are exactly 0 .. 2^18 - 1. Result (run for
this package, shipped program SHA-256 92c95d72...6a5b4af): 56,000 of 56,000 lanes right with the verifier, 56,000 of 56,000 flags right, 8,000 of 8,000 batch decisions
(each with its quad decision), 2,000 of 2,000 piece checks (including the staged-flow comparison) and
group-operation counts right (500 last-group cases; in the staged flow 494 batches entered stage B, 15 stage C and
none the continuation); in every forced quad 70 stage-A, 29 hit-tree, 264 stage-B (66 per batch) and 244 stage-C
(61 per batch) operations and continuations of at most 235; on the leaf paths of the 200 cases with them the
hit-tree counts listed above, 66 and 61 operations per batch, continuations of 215 to 235 operations and register
peaks of 57 to 64 (64 with the union at shared instructions); 4 in every block update, 13 / 8 (11 / 1 in the last
group) in every group set-up and end; 324, 120, 94 and 28 operations in every outer step, member step, table word
and table entry; static bounds as above; peaks of 64 and 36 registers (40 resident); D-slot test right; 17.4 s.

Pattern tests on constructed words: the stage-A flags and the quad test
(each lane with a random C2.d1 and its K', passing lanes with the five
conditions on z set, failing lanes with one of them violated or random,
guard bits random; all 128 patterns on each batch with the other three
failing, and on batch 0 with random patterns on the others: the quad
decision and the four flag words) 640 of 640; the hit tree (every set S of
batches with a passing lane taking part, including the empty set, three
random lane patterns each, with all-lane and last-group B32: the quad
decision, the leaf and every flag word) 96 of 96; the early-exit test (all
128 x 128 pairs of W4-zero and xF lane patterns, random guard bits) 16,384
of 16,384; the exact test likewise on the OR of four words zero on random
supersets of a pattern, 16,384 of 16,384; the stage-B test (all 16,384
pairs of rule-A and filter patterns of the seven lanes) 16,384 of 16,384;
Lemma A3 on 16,384 constructed cases (all 64 x 64 patterns of the six bits
of d1 and a2, four fillings) with no disagreement; the budget registers (a
register holding E = 2^14 k + r, k < 3, r = 0, 1, 2^14 - 1, decremented per
entry with 2^14 or a random number of entries per group and tested before
each group, never goes below 0, completes at most E entries and halts only
when fewer than 2^14 remain; the budget word cR holding E < 4 allows exactly
E continuations and then halts) right. The 65,536 member numbers give
65,536 distinct members of S8; Lemma B holds for 6 of 6 betas. Exit status 0
only if all of these hold, and only if `verifier/blake3.py` was imported. No
real lane with R = 0 or with W4 = 0 occurs at this size; the taken branches
are covered by the pattern tests and the forced paths. Runs on this version
(all reported): on drafts of the program, self-tests of 3 cases (seed dev0; it failed only its register check, peak 65,
before the spill at leaf {0,1,2,3} was added), 20, 11, 6 and 200 cases (seeds dev1 to dev4, all checks right; the
outputs of the 11- and 6-case runs were not saved, and the 6-case output was read only in part; the 200-case run was
on a draft equal to the shipped program); on the shipped
program the 2,000-case self-test above (seed 9), once. An abandoned draft of an earlier session of ours (register
peak 71) had one 4-case self-test; nothing of it is used.

*Broken copies.* Nine deliberately broken copies of the program, each changing one line (or one expression in two places),
were run with `--selftest 100 broken`; eight fail (exit status 1): the quad test without batch 3 (U12 =
pA_2 OR pA_2: 396 of 400 batch decisions, 99 of 100 piece checks right); the hit tree with leaves {0,2,3} and
{0,2} swapped (leaf paths and the tree's pattern tests wrong); the early-exit word from g1 ^ h1' instead of
g1 ^ g1' (0 of 2,800 lanes right); the words DN_j off by one position, -k4 - (3 - j) 2^16, in the outer step and
its check alike (0 of 2,800 lanes right); no spill at leaf {0,1,2,3} (peak 65 registers, hit-tree count 19
instead of 29); the continuation's flag word without rule A (B32 AND B32: 2,769 of 2,800 flags right); E + 2^16
only for positions 0..2 of a quad (0 of 2,800 lanes and 0 of 100 piece checks right); and the last group keeping
the all-lane B32 (383 of 400 decisions, 75 of 100 piece checks right). The first version of the DN copy only
renamed the four DN registers, which changes nothing (the program defines their values through the same names), and
passed (exit status 0); it is reported and was replaced by the off-by-one copy above. 5ca02dfb's broken copies of
the S2K14 bookkeeping and c19feef's of its own program concern code that this package does not change; the pair
flow they also covered is replaced by the quad flow tested here. As in 5ca02dfb, a copy whose early exit tested all
lanes instead of the lanes of xF would not be caught (W4 = 0 never occurs on real lanes at this size); the test's
operands are fixed in the shipped code and listed in Section 5.

## 6. Experiments (organizer-run)

`experiments/s8stage.py`, standard library only, seeds expanded by
SHAKE-256, no BLAKE3 import in organizer mode.

- `half-collision`: per seed, the context words (vc, vd, S15, S9, w5, X2;
  D3.d1 = X3 as in the algorithm) and a member number of S8; returns the
  pair of Theorem 1. Event: digest words 0, 2, 5, 7 agree (exact, all
  seeds). Observations: the program locates the batch of the order S2K14
  that holds this trial (C2.a1 = X2 + X6 + w7 = r 2^14 + i, g =
  floor(r / 7)) and runs the counted outer step (from a 256-bit word whose
  words 0 to 2 are the three coin words), the member step, the end of
  group g - 1 (g > 0) and the set-up of group g, the block update, the
  table entry and the table words of the quad of positions (i AND NOT 3 ..
  i OR 3) that holds it, the counted quad (forced, as in the self-test:
  leaf {0,1,2,3} with stages B, C and the continuation of all four
  batches) and the same quad in the staged flow on a copy of the machine
  (compared as in the self-test): stage_a_ops 70 (per quad), stage_b_ops
  66, stage_c_ops 61, hit_spill_ops 29 (the leaf {0,1,2,3}), cont_ops 235
  (the largest continuation of the forced quad), outer_ops 324,
  table_word_ops 94, member_ops 120, block_ops 4, group_ops_right 1
  (set-up and ends with the counts of Section 5), pieces_right 1 (every
  word the pieces leave equals the construction, and the staged-flow
  comparison holds), lanes_right 28 (W4, the continuation's four words, T
  and the indicator equal to the forward computation, four batches),
  flags_right 28 (the stage-A flag equal to rule A and both stage-B flags
  equal to rule A with the filter, of the forward computation),
  decisions_right 4 (each batch's four decisions and the quad decision
  right), member_in_s8 1 (predicted for every seed).
- `class-filter`: per seed, the context words and member as above, a group
  g < 37,449 and twelve consecutive positions 256 b + 252 .. 256 b + 263
  (b < 63, both from SHAKE-256 of the seed), three quads, so that the run
  crosses a block boundary between two quads and makes two block updates;
  the twelve batches (84 trials: seven values of X2 per position) run as
  three counted quads (each also in the staged flow on a copy, compared),
  after the counted pieces; returns the pair of lane 0 of the first batch
  (same event). Observations per seed: trials 84, y4_equal 84, eta_equal
  84, lanes_right 84, flags_right 84, decisions_right 12, pieces_right 1,
  group_ops_right 1, block_updates 2, lemma_b 6 (predicted for every seed),
  and the counts rule_a_lanes, filter_lanes, filter_and_rule_a_lanes
  (rates near 2^-5, 2^-6, 2^-11 per trial), and the staged flow's
  stage_b_batches, stage_c_batches and cont_batches (at most the first, the
  third and the third count of the seed). Each seed is one outer step and
  member, whose trials are not independent. The expected totals per run of
  256 seeds under M are 672, 336 and 10.5 lanes and 612.2 and about 10.5
  batches; rule A clusters, so no per-run range is predicted. The premises
  of H1 (ii) are run averages; the stage-B ratio of one run
  (stage_b_batches / 612.2) has expectation about 0.377 and a large
  run-to-run spread (the replays below; each seed is one member and twelve
  consecutive positions, so its batches are clustered); one run is not
  evidence for or against it. A continuation (W4 = 0 on a lane with rule A
  and the filter, about 2^-30 per trial) is not expected in any run.

Coverage: the organizer experiments almost never reach the last group
(half-collision: probability 2^-18 per seed; class-filter uses
g < 37,449), so the masking of lanes 1..6 in the last group is tested by
the self-test (500 of its 2,000 cases are last-group cases) and by a broken
copy (Section 5), not by these experiments; the branch from the early-exit test to
the continuation and the continuation's exact test are tested by the forced quad (every lane's words
against the real digests) and the pattern tests.

*Replays (preregistered; participant-run local replays using the
repository's `experiments/runner.py`).* Before any replay of the shipped
program (SHA-256 92c95d72...6a5b4af), the program, the manifest
(21810ecc...1fb44), the harness (our v103 harness, unchanged: it runs
`experiments/runner.py` of the repository with `verifier/blake3.py` as
digest; 1185392d...24b9bde), the launcher (one run after another) and the
list of 41 nonces (the public seed, and holdout_nonce = the first 32 hex
digits of SHA-256 of 'blake3-r2-v104 replay NN', NN = 01 to 40; our own
nonces, not organizer holdouts; list 183b2349...5ada5b9) were fixed and
hashed (frozen_sha256.txt 901ea288...7d3b55, with the UTC time
2026-10-08T13:50:23Z in frozen_meta.txt 3ba8976c...2610ae), and all 41 runs
were then made one after another (2026-10-08T13:54:39Z to 13:59:06Z,
under the heavy-job lock; 1-minute load at most 5.45); no other replay of
the shipped program was made. In every run both experiments have 256 of
256 successes, no repeated pair, and every predicted observation exact for
every seed. Totals of 21,504 lanes per run: rule A 517 to 838 (mean 661.0,
sd 88.0, above the binomial value because of clustering), filter 301 to 376
(mean 338.9), both 1 to 21 (mean 9.7, sd 3.8); batches entering stage B 178
to 293 of 3,072 (mean 227.7, sd 26.6), stage C 1 to 19 (mean 9.4), never
more than the lanes with rule A or with both, and the continuation in no
run; on the public seed 573, 363, 9, 204, 9 and 0. As ratios to M over the
41 runs (standard error from the run-to-run sd): batches entering stage B
0.372 +- 0.007 of 612.2, rule A and the filter 0.927 +- 0.057 of 10.5, rule
A 0.984 +- 0.020 of 672. Each run's seeds are clustered (one member and
twelve consecutive positions per seed), and the run-to-run spread is large;
these runs cannot resolve the margins of (ii), which rest on the uniform
samples of Section 8.2. One execution of class-filter takes 2.33 to 2.46 s
on our machine, half-collision under 0.9 s (the runner's limit is 20 s).
Run outputs are hashed in RUN_HASHES_REPLAY.sha256 (runlog.jsonl
18f7ba40...b4d05). Before the replay plan was frozen, one development run
of the runner on the public seed was made with the program as shipped and
5ca02dfb's manifest, before ours was written (the program does not read the
manifest's text): both experiments 256 of 256 with every predicted
observation exact (totals 573, 363, 9, 204, 9 and 0, identical to the
public-seed replay). The replays of 5ca02dfb's pair program are not
evidence for this program and are not used.

*v106.* The replays above ran ef052659's shipped program (SHA-256
92c95d72...6a5b4af). This package's program (41a0d8ae...f5777a1) differs
from it only in the two ledger constants V_RANGE and F_H1, which organizer
mode never reads, so its organizer output is the same function of the
request. One run of the same harness on the public seed with this
package's program and ef052659's manifest (the shipped manifest differs
from it only in one sentence of the class-filter hypothesis, about these
replays, which the runner does not execute) gave both experiments 256 of 256
successes, no repeated pair, every predicted observation exact, and the
observation totals of ef052659's public-seed replay (573, 363, 9, 204, 9
and 0). No other runner run was made for v106; the 40 holdout-style
replays were not repeated.

Observations are the program's own and untrusted; they check the
generator, the class, the order S2K14, the stage tests and the counted
pieces against a forward computation of real messages. They do not measure
H1.

## 7. Success probability

The probability space is the V * 2^32 random words of step 2, one per outer
step, independent and uniform (each supplies vc, S15 and S9; D3.d1 = X3 is
fixed). Outer step k (k = 1, .., V * 2^32) is a fixed pair (vd, w5), and
all its trials, its batches in the order S2K14, its stage decisions and
residuals are a function of that pair and its own random word r_k.

**H1 (score-critical; the only premise).** Over the random words of the
algorithm:

(i) the N = V * 2^80 trials behave with respect to "good" (R = 0, rule A
and the beta filter) like independent events of probability at least
F * 2^-128 each, F = 132,392,960 (the exact count 185,350,144 of
Section 8 divided by 1.4, margin 1.400, GordoAR's choice; 2^26.9803), to
the extent that the probability that no trial is good is at most
exp(-lambda) + 0.002 with lambda = N * F * 2^-128 = 0.4975807; and

(ii) averaged over the V * 2^62 * 37,450 batches of the run (V =
1,057,885) in the order S2K14 of Section 4, the probability that a batch has a trial taking part
in its decisions that satisfies rule A (and so enters stage B) is at most
theta_B p_B with theta_B = 0.377; averaged over the N trials, the
probability that a trial satisfies rule A and passes the filter is at most
theta_C 2^-11 with theta_C = 1.003; and averaged over the N trials, the
probability that a trial satisfies rule A, passes the filter and has
W4 = 0 (Lemma E) is at most rho_R = 2^-24. Under the same seven-word model M
that gives the count of (i), with the distinct trials of a batch
independent as in (i), the first two probabilities are exactly p_B =
(37,449 (1 - (31/32)^7) + 1 - 31/32) / 37,450 = 0.1992731 and 2^-11
(Section 8.2: 2^27 of the 2^32 words h1 satisfy rule A, 2^26 of the 2^32
words c1 pass the filter, h1 and c1 = d1 + Y11 are independent uniform
words of M, and for each member and position 37,449 groups give batches of
seven distinct trials and the last group one of one). The value of theta_B
lies below 1 because rule A clusters (trials that share C2's inputs or
parts of them); theta_B and theta_C are not values of M: they were set by
5ca02dfb's preregistered decision rule (Lemma C' and the empirical
Bernstein bound, each at 2^-64, on a grid) from a uniform sample of 2^35
batches of this order whose runs, seeds and analysis were fixed by its
preregistration, and no other run was used to set them; this version's
preregistered uniform sample of 2^35 batches reproduces both (the same two
tests pass at both values, Section 8.2). rho_R is not a value of M either
(the 32-bit word W4 of a trial with rule A and the filter is zero far more
often than 2^-32, Section 8.2): it was fixed before this version's
preregistered sample, after development runs that measured about 2^-30.5,
and that sample passed Lemma C' and the empirical Bernstein bound at 2^-24
(each at 2^-64; measured 2^-31.90 per trial). Those two samples drew vd
below 1,512,538, the V of 5ca02dfb and ef052659, so for this package's run
(vd below 1,057,885) they sample a larger index space that contains it;
v106's preregistered sample of 2^35 batches, drawn from this run, passes
the same tests at all three values (Section 8.2).

Part (ii) is a statement about first moments only. It says nothing about
how passing trials are distributed inside a batch, a group, a member or an
outer step; rule A is known to cluster, and nothing below depends on the
contrary.

**Lemma C (Chernoff bound).** Let X_1, .., X_n be independent random
variables with values in [0, 1], and mu_H >= E[X_1 + .. + X_n]. Then for
0 < delta <= 1, P(X_1 + .. + X_n >= (1 + delta) mu_H) <= exp(-delta^2 mu_H / 3).
*Proof.* For t > 0 and x in [0, 1], e^(tx) <= 1 + x (e^t - 1) (convexity),
so E e^(t X_k) <= 1 + (e^t - 1) E X_k <= exp((e^t - 1) E X_k), and by
independence E e^(t sum X_k) <= exp((e^t - 1) mu_H). Markov's inequality
with t = ln(1 + delta) gives P(sum >= (1 + delta) mu_H) <=
exp(mu_H (delta - (1 + delta) ln(1 + delta))), and
(1 + delta) ln(1 + delta) >= delta + delta^2 / 3 for 0 <= delta <= 1. QED.

**Theorem 2 (budgets).** Let S_B, S_C and S_R be the numbers of batches
that would enter stage B, stage C and the continuation in a run without
budgets. If H1 (ii) holds, then P(S_B > E_B - 2^14) <= exp(-3.1 * 10^6),
P(S_C > E_C - 2^14) <= exp(-1.4 * 10^5) and P(S_R > E_R) <= exp(-17.5).

*Proof.* Write S_B = sum over k of S_k, S_k the number of batches of outer
step k that enter stage B. S_k is a function of r_k, so S_1, S_2, .. are
independent, and 0 <= S_k <= m = 37,450 * 2^30, the number of batches of
an outer step. By Lemmas A3 and P4 and the masking of Section 3 a batch
enters stage B iff one of the trials taking part in its decisions
satisfies rule A, so E S_B is the sum over all V * 2^62 * 37,450 batches of
the probability of this event, at most theta_B p_B V 2^62 37,450 by
H1 (ii). Put X_k = S_k / m and mu_H = theta_B p_B V 2^62 37,450 / m =
3.413 * 10^14. E_B - 2^14 = (1 + delta) mu_H m with delta = 1.66667 * 10^-4
(just below 1/6000, 5266c5ce), so Lemma C gives P(S_B > E_B - 2^14) <=
P(sum X_k >= (1 + delta) mu_H) <= exp(-delta^2 mu_H / 3) = exp(-3.16 * 10^6).
For stage C, a batch enters only if one of its trials satisfies rule A and
the filter (Lemma F2), so S_k is at most the number of such trials of outer
step k (a union bound, valid for any dependence between the trials of a
batch; the repeated lanes of the last group take no part) and
E S_C <= theta_C * 2^-11 * N by H1 (ii); mu_H = theta_C 2^-11 N / m =
1.558 * 10^13, E_C - 2^14 = (1 + delta) mu_H m gives delta = 1.66667 *
10^-4, and the bound is exp(-1.44 * 10^5). For the continuation, a batch
enters only if one of its trials taking part satisfies rule A and the
filter and has W4 = 0 (Section 5), so by the same union bound
E S_R <= rho_R N; mu_H = rho_R N / m = 1.8957 * 10^9, E_R = (1 + delta)
mu_H m with delta = 1.66667 * 10^-4, and the bound is
exp(-delta^2 mu_H / 3) = exp(-17.55). QED. (`python3 experiments/s8stage.py
--ledger` prints E_B, E_C, E_R, mu_H, delta and the three exponents.)

**Success.** The run with budgets executes exactly as the run without them
until it halts at a group's budget test or at a continuation's; the first
halts only when a register holds less than 2^14, i.e. after more than
E_B - 2^14 entries of stage B or more than E_C - 2^14 of stage C, the second
only at the (E_R + 1)-th continuation; so no budget halt occurs if
S_B <= E_B - 2^14, S_C <= E_C - 2^14 and S_R <= E_R. If moreover some trial
is good, the completeness argument of Section 4 shows that step 3 outputs a
pair of distinct messages of 55 and 63 bytes with equal complete digests.
So, under H1,

    P(success) >= 1 - (exp(-lambda) + 0.002) - exp(-3.1 * 10^6) - exp(-1.4 * 10^5) - exp(-17.55)
               >= 1 - exp(-0.4975807) - 0.002 - 2.4 * 10^-8 = 0.3900002 >= 0.39.

(`--ledger` prints success 0.3900001832. With V = 1,057,884 the same bound
gives 0.3899999 < 0.39, so V = 1,057,885 is the smallest value that
certifies 0.39 at this F.)

The time of Section 9 holds for every value of the coins: stages B and C
and the continuation are charged at their budgets. Sensitivity: with a good-trial rate
f * 2^-128 the same search reaches 0.39 only for f >= 132,392,880 =
2^26.98025 (lambda >= 0.4975804), a factor 1.0000006 below F: V is minimal,
so the whole margin of H1 (i) is the factor 1.4 between the model count
and F. With the uniform rate (f = 1) it needs 2^127 trials and gives about
120.2.

## 8. Evidence for H1

### 8.1 Part (i): the count of good trials

**The seven-word model M (c66f230d).** By Section 3, R depends on the
constants and seven words: for E1 d1, b1, a2 (message A; a1 and d1 are
shared), for E3 Y4, Y9, w8 and h1. Y4 runs over S8 equally often. M says the
other six behave over the trials like independent uniform words. Under M a
trial is good with probability r * 2^-128, where r * 2^-128 is the share of
solutions of R = 0 with rule A and the filter among (Y4 in S8) x 2^192.
Using the conditions of Lemma N and its E3 analogue, R = 0 iff, with
tau = a2 ^ a2', eps = c2 ^ c2', beta of E1 and eta, psi the first-half d, b
differences of E3: E3's c and a output differences equal tau and eps,
psi = tau ^ ROR(tau, 1), and eta = eps ^ ROL(beta ^ eps, 1).

**How r is counted (shipped: `python3 count_s8.py`, Appendix D).**
For a beta, an outcome is (tau, eps).
N1 is the number of (d1, b1, a2) in 2^96 with this beta (Lemma B carry
conditions on c1) giving the outcome; N3 is the number of
(Y4 in S8, h1, Y9, w8) in 2^16 * 2^96 for which E3 produces eta, psi, eps,
tau and h1 satisfies the rule. Both are counted exactly by carry automata
over the 32 bit positions in exact integer arithmetic; no sampling and
no fallback. Then r = sum over outcomes of N1 * N3 / (2^16 * 2^64). Parts
are non-negative, so any subset of betas or outcomes gives a lower bound.
N1 (function `N1`): for each pattern pa of a2 on tau the number of b1
patterns on beta with DELTA + (beta - 2 Sb) = tau - 2 pa (two candidates
by `solve_sub`), times, for each pattern px of d1 ^ a2 on tau, a 16-state
automaton over (d1, d2 = ROR(d1 ^ a2, 8)) whose state is the four carries of
c1 = d1 + Y11, c1 + DY11, c1 + d2 and c1' + d2'; free bits of b1 off beta
give the factor 2^(32 - |beta|). N3 (function `N3`): for each pattern of
Y4 ^ g1 on P = ROL(psi, 12) the e2 patterns on eps from the E3 carry
condition, the h1 patterns on eta (rule A applied) with their g1 pattern,
and a 4-state automaton over (g1, h2) for the c-output difference tau;
members of S8 enter through their bits on P. The program lists the 85
outcomes of the six betas (the tau values; eps is fixed by beta) and prints
N1, N3 and the part of each.

**The count.** For the six betas of T6 (all with an eps; they fix 11, 11,
11, 11, 13, 13 bits of c1) the outcomes are enumerated without a bound on
the weight of tau, and:

| beta | outcomes (full class) | part, full class | outcomes (S8) | part, S8, rule A |
|---|---:|---:|---:|---:|
| 18b0e098 | 14 | 71,698,432 | 7 | 67,698,688 |
| 18d0e098 | 19 | 54,005,760 | 12 | 50,790,400 |
| 18b1a098 | 16 | 25,692,160 | 16 | 51,384,320 |
| 18d1a098 | 18 | 8,429,568 | 12 | 13,246,464 |
| 18b3e098 | 8 | 1,566,720 | 4 | 1,474,560 |
| 18d3e098 | 10 | 838,656 | 6 | 755,712 |
| T6 | 85 | 162,231,296 | 57 | **185,350,144** |

For the heaviest beta 18b0e098 (eps = 6e21be55) the seven nonzero S8
outcomes are (N1, N3 with rule A, part): tau 285020a0: 2^51, 12 * 2^50,
25,165,824; 185020a0: 2^51, 8 * 2^50, 16,777,216; 385020a0: 2^50,
16 * 2^50, 16,777,216; 175020a0: 2^49, 12 * 2^50, 6,291,456; 685020a0:
2^49, 3 * 2^50, 1,572,864; 275020a0: 2^49, 2 * 2^50, 1,048,576; 675020a0:
2^47, 2^49, 65,536; sum 67,698,688. Its seven other outcomes (tau with
bit 14 set) have N3 = 0 in S8.

The S8 total is the same exact integer with and without rule A: among
these outcomes no S8 solution violates rule A. The claimed factor
F = 132,392,960 is 185,350,144 * 5/7 (margin 1.400; ef052659 and 5ca02dfb:
185,350,144 / 2). All 15 betas with k <= 14 and the same counter give
185,355,230.33 for S8 with rule A (162,263,084.49 for the full class without
rule; 144,123,339.49 with rule A).

*Checks of the count.* (i) Three counting programs agree exactly: winglock's C
counter, the shipped Python port (5ca02dfb's and c19feef's `--count` mode,
moved unchanged into `count_s8.py` of Appendix D because of the runner's
64 KiB source limit: all 85 outcomes, 57 nonzero, the six parts and
185,350,144 in about 2 minutes; `count_s8.py all` also gives the same total
without rule A), and a counter written independently
by another helper agent, which gives 183,119,872 for the four heaviest
betas in S8 with and without rule A (1.383 F from these four alone).
A fourth, sampling estimator written by winglock's review agent (Monte Carlo over
(y, h1, g1) for E3 and (c1, b1) for E1, exact automaton over e2 and a2)
gives 185,477,038 +- 878,331 (ratio 1.0007 +- 0.0047), with all 57 nonzero
outcomes within noise and the 28 zero outcomes zero. Per member of S8 the
exact factor (all 15 betas, rule A) lies between 184.57M and 186.14M, so
every member is above 1.39 F. (ii) The full-class parts and outcome
numbers equal the published table of c66f230d for all six betas
(computed there by a different program and recounted by another AI model);
the full-class rule-A splits for all 15 betas, 162,243,466.25 /
144,123,339.49 / 123,244,351.65 for 4 / 5 / 6 conditions, equal c66f230d's
published splits minus their parts for betas with k >= 15. (iii) Brute
force at 8-bit word size (rotations 4, 3, 2, 1) against the same counter:
52 random constant sets, 1,372,942 E1 outcomes and 19,258 E3 outcomes and
all 9 nonzero R = 0 totals equal; 48 further sets: 22,892 outcomes with the
per-member split (329,346 comparisons), the per-h1-pattern split
(1,471,448) and rule restrictions (22,892) all equal, no mismatch. (iv) The
count was rerun with `count_s8.py` on ef052659's shipped program (111 s;
exit status 0) and again, for v106, on this package's shipped program:
85 outcomes, 57 nonzero, the six parts 67,698,688, 51,384,320, 50,790,400, 13,246,464, 1,474,560 and
755,712, and r = 185,350,144 = 1.4 F, exactly as above (113 s; exit status
0; it prints claimed_F 132,392,960 and margin_over_F 1.4).

**Real trials in the order of 2bb5d604 (participant measurements, C programs
on steps S1/T of c66f230d).**
In 4,096 random contexts with all 65,536 S8 members (2^28 trials): rule A
holds for 2^-4.9993 of the trials; the filter passes for 2^-6.006 of the
rule-A trials (model 2^-6). Over 896 draws of the seed words with 256
contexts each (229,376 contexts), rule A holds for 2^-5.0002 of the
trials, rule A and the filter for 2^-10.9997.

*Deeper events.* With real (c1, b1) from steps S1/T and a2 counted exactly,
the E1 part of the count has real/model 1.0086 over 2^33.8 S8 trials. For
E3 with real (y, h1, g1) and e2 counted exactly, partial events (rule A,
the g1 difference and the e2 carry conditions, probability about 2^-38 per
trial) match the model per outcome. The S8 advantage appears on real
trials: per outcome, the ratio of this partial event between S8 and the
other seven eighths of the class is, where the counter's per-member ratio
is 1, 2.333 and 7, 0.99-1.03, 2.20-2.47 and 5.15-8.66 on real trials
(2^33.8 each) and 0.98-1.02, 2.18-2.44 and 5.75-10.00 on draws from the
model itself. The full E3 event has too few hits at this sample size (25
to 38 nonzero trials in 2^33.8) to resolve the ratio: the same estimator
gives 0.80 +- 0.20 on real trials and 0.51 +- 0.15 on model draws, so it
tests neither direction. On 2^26 S8 trials against
2^28.8 trials of the other seven eighths of the class, the low 13 bits of
E3's g1 and e2 are uniform and homogeneous (chi-square z between -1.8 and
1.4); h1 restricted to the eta bits is not uniform (z = 11.6), and an
unrelated control 1/8 subset of the class shows the same (z = 21.3), so
this is the per-context clustering already reported for rule A by
c66f230d, not a property of S8.

**Real trials in the order of 60f94c5c (winglock's participant measurement for an
unsubmitted branch-free draft in this order, `rt2l.c`, a C program whose
event counts equal those of the
shipped program's forward computation on 65,536 trials).** Run layout: per
run, the four coin words, 4 outer steps (vd = 0, w5 = 0..3), 2^16
consecutive values of X2 and all 65,536 members of S8, 2^34 trials; six
runs. The same program in the order of 2bb5d604 (six runs, 4 values of vd,
2^16 consecutive X14, all members) gives the comparison. Over 2^36.585
trials each:

| event | this order | real/model | other order | this/other |
|---|---:|---:|---:|---:|
| rule A | 2^-5.0000 | 1.0000 | 2^-5.0003 | 1.0002 +- 0.0000 |
| filter | 2^-5.9999 | 1.0000 | 2^-6.0000 | 1.0000 +- 0.0000 |
| rule A and filter | 2^-10.9999 | 1.0001 +- 0.0001 | 2^-11.0001 | 1.0001 +- 0.0002 |
| beta in T6 (model 2^-8.8301, exact) | 2^-8.8299 | 1.0001 +- 0.0001 | 2^-8.8301 | 1.0001 +- 0.0001 |
| beta in T6 and rule A | 2^-13.8300 | 1.0001 +- 0.0004 | 2^-13.8297 | 0.9998 +- 0.0005 |
| low 12 bits of n zero (Lemma N word) | 2^-10.9277 | | 2^-10.9276 | 0.9999 +- 0.0002 |
| beta in T6 and low 8 bits of n zero | 2^-15.4461 | | 2^-15.4455 | 0.9996 +- 0.0009 |
| E3: g1 ^ g1' = ROL(psi,12), tau 285020a0 | 2^-14.0004 | | 2^-14.0000 | 0.9998 +- 0.0006 |
| low 16 bits of D1 and of D3 zero | 2^-30.40 (73) | | 2^-30.28 (79) | 0.92 +- 0.16 |

The events without a closed-form model value have the same rate in both
orders; the deeper checks above (E1 part, E3 partial events at 2^-38) were
made in the order of 2bb5d604 with random D3.d1. The stages and the batching
do not change which trials are run or their residuals, only which are
examined together; a fresh random word per outer step changes the coin words
from one per run to one set per outer step, which the measurements of 8.2
use.

**With D3.d1 = X3 (21252124, c19feef, 5ca02dfb and this version).** The table above has D3.d1
random. With D3.d1 = X3, X14 = 0 in every trial, so C2 runs with d = 0 and
C2.d1 = ROR(a1, 16); C2's outputs Y2, Y6, Y10 and Y14 (Y6 enters E1, Y14
enters E3) still vary with X2, X6 and X10, but no longer with a coin in the
d input. X9 = D3.c1 = S9 + X3 varies only with the coin S9; D3.a1, D3.b1,
S4, S3, X4 and the words derived from them vary with w5 and S9. Within one
outer step these words were fixed in the random-D3.d1 configuration as
well; what changes is that X14 no longer varies across outer steps and that
X9 and X4 no longer depend on a separate coin. A review of 21252124 noted
that the E3 checks had not been repeated in this configuration. c19feef's
preregistered sample (`rtuni4.c`, Appendix A; its units are uniform
batches of the order S2K, which contain the same trials as the run of this
package, so these per-trial rates are rates of this run's trials as well)
therefore counts, on every trial, all events of the table above, in the
algorithm's configuration (2^38 trials, mode fixed) and in a control with
random D3.d1 (2^36, mode rand):

| event | D3.d1 = X3 (2^38) | random D3.d1 (2^36) | ratio +- Poisson s.e. (understates the error of clustered events) |
|---|---:|---:|---:|
| rule A (model 2^-5) | 2^-5.0000 | 2^-5.0000 | 1.0000 +- 0.0000 |
| filter (model 2^-6) | 2^-6.0000 | 2^-6.0000 | 1.0000 +- 0.0000 |
| rule A and filter (model 2^-11) | 2^-11.0002 | 2^-10.9999 | 0.9998 +- 0.0002 |
| beta in T6 (model 2^-8.8301) | 2^-8.8301 | 2^-8.8301 | 1.0000 +- 0.0001 |
| beta in T6 and rule A | 2^-13.8303 | 2^-13.8300 | 0.9998 +- 0.0005 |
| low 12 bits of n zero | 2^-10.9275 | 2^-10.9272 | 0.9998 +- 0.0002 |
| beta in T6 and low 8 bits of n zero | 2^-15.4467 | 2^-15.4462 | 0.9996 +- 0.0009 |
| E3: g1 ^ g1' = ROL(psi,12), tau 285020a0 | 2^-14.0002 | 2^-14.0004 | 1.0002 +- 0.0005 |
| low 16 bits of D1 and of D3 zero | 2^-30.50 (181) | 2^-30.22 (55) | 0.82 +- 0.13 |

The E1 events and the 2^-14 E3 event (which involves Y14 through h1 and
Y9 through g1) keep the rates of random D3.d1 within their standard errors
(ratios 0.9996 to 1.0002) and agree with the values of the table above
(2^-8.8299, 2^-13.8300, 2^-10.9277, 2^-15.4461, 2^-14.0004). The 2^-30 event
on the low halves of the digest differences D1 and D3 (which involves E1 and
E3 to the end of both calls) has 181 hits with D3.d1 = X3 against 55 in the
smaller control: ratio 0.82 +- 0.13, 1.4 standard errors below 1. Pooled
with the random-D3.d1 counts of the table above (73 and 79 hits in
2^36.585 trials each; 207 hits in 2^38.0 trials, rate 2^-30.31) the ratio
is 0.87 +- 0.09. This is consistent with equal rates at this sample size;
we report it as the weakest of these checks (even a factor 0.82 at this
level would lie inside the margin 1.400 of F, whose floor is 1/1.4 =
0.714, but H1 (i) does not rely on that). The E1-part ratio (1.0086) and the per-outcome 2^-38 E3 partial
events were not repeated with D3.d1 = X3; H1 (i) assumes they keep their
rates.

The configuration also changes how rule A clusters inside a batch: in
c19feef's sample the stage-B share of the order S2K is 0.5765 p_B with
D3.d1 = X3 (2^38 trials) and 0.6320 p_B with random D3.d1 (2^36 trials;
0.6319 to 0.6320 in each of the 8 control runs), while the per-trial
rule-A rate is equal (ratio 1.0000 +- 0.0000 in the table above). The
batching matters as much: the same trials batched in the order S2K14 give
0.37659 p_B (Section 8.2), and the per-trial rate of rule A with the filter
measured on S2K14 batches (1.00006 * 2^-11) agrees with c19feef's on S2K
batches (0.99987).
This is a second-moment difference (rule-A outcomes of the trials of a
batch coincide more often with D3.d1 = X3); part (ii) measures it directly
in the algorithm's configuration, and H1 (i) assumes it does not extend to
the 2^-128 event good. The rare events of
the table are counted per trial, so their ratios are first-moment
comparisons of the same kind as for rule A.

### 8.2 Part (ii): the stage events

**Exact values under M.** Rule A reads bits 0, 1, 2, 3, 16 and 17 of h1;
of the 64 patterns of these bits exactly 2 satisfy it (bits 0, 16, 17 zero,
bit 1 one, bits 2 and 3 different), so 2 * 2^26 = 2^27 of the 2^32 words h1
do. The filter reads bits 3, 7, 8, 15, 16 and 19 of c1 (the mask 00098188);
exactly one pattern passes, so 2^26 of the 2^32 words c1 do. Under M, h1 and
the E1 word d1 are independent and uniform, and c1 = d1 + Y11 is uniform, so
a trial satisfies rule A with probability 2^27 / 2^32 = 2^-5 and rule A and
the filter with 2^27 * 2^26 / 2^64 = 2^-11 exactly. With the distinct trials
of a batch independent under M (as in H1 (i)), a batch of seven distinct
trials enters stage B with probability 1 - (31/32)^7 = 0.1992775 and the
batch of the last group (one distinct trial) with 1/32; for each member
and position there are 37,449 groups of the first kind and one of the
second, so the share over all batches of the run under M is p_B =
(37,449 (1 - (31/32)^7) + 1/32) / 37,450 = 36,631,290,006,031 /
183,824,600,268,800 = 0.1992731. `python3 experiments/s8stage.py --ledger`
(and `count_s8.py`, next to the count of 8.1) enumerates the 64 + 64
patterns and prints the integers 2^27, 2^26 and 2^53 and the fraction p_B;
the ledger uses the same fraction. The quad test (Section 5, Lemma P4) and
the early exit do not change which batches enter stage B or C: a batch
enters stage B in the quad flow iff it has a lane taking part with rule A,
exactly as under the per-batch test of the samples' design, and stage C
iff it also has one with the filter; so the shares measured below for the
order S2K14 are the shares of this algorithm. A batch enters the
continuation only if it has a lane taking part with rule A, the filter and
W4 = 0 (Section 5). H1 (ii) asserts theta_B = 0.377 times p_B, theta_C =
1.003 times 2^-11 and rho_R = 2^-24 as run averages; the budgets are
6001/6000 times these (5266c5ce). The third event has no exact value under
M that we use: W4 (Lemma E) is a 32-bit word, but on the trials with rule
A and the filter it is zero far more often than 2^-32 (about 2^-21 below),
because P and g1 ^ g1' are XOR differences of structured additions; rho_R
rests on the samples only.

**What a uniform sample measures (Lemma U, 1d5e54ce).** Draw an outer step
uniformly (vd uniform below V, w5 uniform, fresh coins vc, S15, S9 with the
distribution of the run's random word; D3.d1 = X3), a member y uniformly
from S8, a group g uniformly below 37,450 and a position i uniformly below
2^14. This is one batch of the run drawn uniformly from the
V * 2^62 * 37,450 batches (for fixed coins every batch has probability
1 / (V 2^62 37,450), and the coins are drawn as in the run), so the
indicator b that it enters stage B has mean exactly the run average that
H1 (ii) bounds (the expectation over the coins of the share of batches
entering stage B), x = c / 7, with c (0 to 7) the number of its trials
taking part in the decisions that satisfy rule A and the filter, has mean
exactly (262,144 / 262,150) times the run's per-trial rate of rule A with
the filter (a uniform batch holds (37,449 * 7 + 1) / 37,450 = 262,144 /
37,450 distinct trials on average, and every trial of the run lies in
exactly one batch as a lane taking part), and likewise r = w / 7, with w the
number of its trials taking part that satisfy rule A and the filter and
have W4 = 0, has mean exactly (262,144 / 262,150) times the run's per-trial
rate of that event. Independent draws give i.i.d.
variables in [0, 1]: this is sampling from the run's own index space, not a
model. Sampling single batches rather than whole outer steps is Lemma U of
1d5e54ce; c19feef used it for the order S2K.

For this package V = 1,057,885 (v106). The samples of 5ca02dfb and
ef052659 below drew vd below 1,512,538, their V: their units are uniform
batches of a larger run that contains this one (vd below 1,057,885 holds
69.94% of its outer steps), so they estimate the averages over that run,
not exactly over this one. v106's sample below draws vd below 1,057,885
and is a uniform sample of this run, to which Lemma U applies exactly.

**Lemma C' (lower-tail Chernoff bound; first used in 52bb50ee).**
Let X_1, .., X_n be independent random variables with values in [0, 1] and
mu = E[X_1 + .. + X_n]. Then for 0 < delta < 1,
P(X_1 + .. + X_n <= (1 - delta) mu) <= exp(-delta^2 mu / 2). *Proof.* For
t > 0 and x in [0, 1], e^(-tx) <= 1 - x (1 - e^(-t)) (convexity), so
E e^(-t X_k) <= exp(-(1 - e^(-t)) E X_k), and by independence
E e^(-t sum X_k) <= exp(-(1 - e^(-t)) mu). Markov's inequality applied to
e^(-t sum X_k) with t = -ln(1 - delta) gives P(sum <= (1 - delta) mu) <=
exp(-mu (delta + (1 - delta) ln(1 - delta))), and
(1 - delta) ln(1 - delta) >= -delta + delta^2 / 2 for 0 <= delta < 1. QED.
*Consequence.* If the run average m is at least m0 and S is the observed
sum of n shares with S < n m0, then P(sum <= S) <= exp(-(n m - S)^2 /
(2 n m)), which is decreasing in m for n m > S, so at most
exp(-(n m0 - S)^2 / (2 n m0)). The empirical Bernstein inequality (Maurer
and Pontil 2009, Theorem 4; cited, not proved; Lemma C' does not depend on
it) gives, for i.i.d. variables in [0, 1] with unbiased sample variance V,
E Z <= mean + sqrt(2 V ln(2/delta) / n) + 7 ln(2/delta) / (3 (n - 1)) with
probability at least 1 - delta over the sample.

**5ca02dfb's sample (Subflatus3's participant measurement, `sbs2k.c`,
Appendix B; preregistered; it set theta_B and theta_C).** (In this
paragraph, its preregistration and its decision, "the counted program" and
"the shipped program" are 5ca02dfb's; the text is 5ca02dfb's.) `sbs2k.c` draws units as above (SplitMix64;
vd by rejection below V from 21-bit draws, then w5, vc, S15, S9, the member
index below 2^16, g by rejection below 37,450 from 16-bit draws and i below
2^14) and computes the seven lanes of the batch forwards: for lane l with
r = 7g + l < 2^18 (the last group: lane 0 only), C2.a1 = r 2^14 + i and
X2 = C2.a1 - X6 - w7, then steps O, M, Y and T, C2, C1, E1 and E3 of message
A, rule A on h1 of E3 and the filter on c1 of E1. Its per-trial code is
shared verbatim with Subflatus3's `sbbatch.c` (1d5e54ce), whose context
mode was checked there against an independent forward computation on all
batch decisions of five full contexts. Before the plan was frozen,
`crosscheck_s2k.py` compared `sbs2k --context` with the counted program:
for 24 contexts (seeds 1..24; a random outer step with D3.d1 = X3, a
random member, a random group, 8 of the contexts in the last group, and
4,000 consecutive positions each; 480,000 lanes) the stage-B decision and
c of every batch, read from `s8stage.forward` (the counted program's own
2-round compression of the trial's real messages, with C2.a1 = (7g + l)
2^14 + i), were equal to those of `sbs2k` (equal FNV hashes over all
batches, 5,502 batches entering stage B and 238 lanes with rule A and the
filter), and every 50th lane's digest was also compared with
`verifier/blake3.py` (9,600 digests, all equal). After freezing, three
more contexts (seeds 31..33, 45,000 lanes, one in the last group) were
compared with the frozen binary and the frozen counted program: equal.

*Preregistration.* Before any run of the sample, the counted program (the
program with the placeholder PREMISE = (1, 501/500), SHA-256
cb0a9741...ff87e78; it differs from the shipped program only in that line),
`sbs2k.c` (17f5d91c...6a208) and its binary (e745aa7f...5182c),
`crosscheck_s2k.py`, the analysis `summarize.py` (7af8060f...ce220), the
seed rule `make_seeds.py` (23ee2cbe...aa075), the seeds, the launcher
`run.sh` and the plan were fixed and hashed (PLAN.sha256, SHA-256
186f9fc8...e213d16b, frozen 2026-10-07 15:39 PT). Seeds: run NN (NN =
01..32) uses the first 16 hex digits of SHA-256('subflatus3 S2K14 sample
NN') as a decimal SplitMix64 seed; the seed rule checks that the 32
streams (2^35 states each, more than one run's draws) are pairwise
disjoint and disjoint from the streams of seeds 1..9 used in development
runs. Plan: 32 runs `./sbs2k 1073741824 SEED` (2^35 units, 2^37.8
trials), at most 8 at once, nice -n 10, each started only while the
1-minute load average was at most 12. Decision rule (fixed before the runs,
`summarize.py`; delta = 2^-64 for both tests):

- stage B: theta_B is the smallest k/1,000, 300 <= k <= 600, such that the
  observed sum S_B < n theta_B p_B, the Lemma C' bound
  exp(-(n m0 - S_B)^2 / (2 n m0)) at m0 = theta_B p_B is at most 2^-64,
  and the empirical Bernstein bound on E b at delta = 2^-64 is at most
  theta_B p_B;
- stage C: theta_C is the smallest k/1,000, 1,000 <= k <= 1,249, with the
  same two tests on x at m0 = theta_C 2^-11 (262,144 / 262,150);
- STOP (no premise, no submission from this order) if any run is missing
  or wrong or no grid value passes; budgets 6001/6000 times the premises.

Both tests are monotone in theta, so the smallest passing grid value is an
upper confidence bound rounded up to the grid: the event that the rule
returns a theta with theta * (model value) below the true run average is
contained in the event that the largest grid value below the true average
passes, whose probability is at most 2^-64 by Lemma C' alone (and at most
2^-64 by the empirical Bernstein bound alone); no multiplicity cost arises.
This rule is stricter than c19feef's (which accepted a Lemma C' exponent of
20, e^-20 = 2^-28.9).

| event (32 runs, 34,359,738,368 units, 2^37.8 trials) | count | unit mean +- s.e. | empirical Bernstein (2^-64) | Lemma C' at the premise | premise | budget |
|---|---:|---:|---:|---:|---:|---:|
| batch enters stage B | 2,578,501,699 batches | 0.376590 +- 0.000007 of p_B | 0.376658 p_B | exp(-1525) at 0.377 p_B | **0.377 p_B** | 0.3770628 p_B |
| rule A and filter (x = c/7 per batch) | 117,444,366 trials (sum of c^2: 123,009,796) | 1.00006 +- 0.00009 of 2^-11 | 1.00096 | exp(-72.5) at 1.003 | **1.003 * 2^-11** | 1.0031672 * 2^-11 |
| batch enters stage C (not in (ii)) | 114,707,210 batches | 0.0033384 per batch | | | | |

**Decision (5ca02dfb).** All 32 runs were present (started 2026-10-07 15:39:37 to
15:48:44 PT, all ended with exit status 0 by 15:51:41 PT; 1-minute load at
most 11.75 at every start). The stage-B grid value 0.376 fails (S_B is above
n * 0.376 p_B) and 0.377 passes both tests (empirical Bernstein bound
0.376658 p_B; Lemma C' exponent 1525), so theta_B = 0.377. For stage C,
1.001 and 1.002 fail the Lemma C' test (2^-64 needs an exponent of 44.4)
and 1.003 passes both (exponent 72.5; empirical Bernstein bound 1.00096),
so theta_C = 1.003. No STOP condition occurred. The budgets are 0.377 *
6001/6000 = 0.3770628 p_B and 1.003 * 6001/6000 = 1.0031672 * 2^-11. Per run
(2^30 units each) the stage-B share lies between 0.37649 and 0.37665 p_B
and the rate of rule A with the filter between 0.99927 and 1.00083 of
2^-11; the largest c of one batch was 5. The 917,361 units in the last
group (about 1/37,450) hold one distinct trial each, as the run's last
groups do. The only change to 5ca02dfb's program after its sample was its
PREMISE line, from the placeholder to (377/1000, 1003/1000). These two
values are this package's theta_B and theta_C unchanged.

**The sample of this version (participant measurement, `eaq.c`, Appendix
C; preregistered; it tests rho_R and reproduces theta_B and theta_C).**
`eaq.c` contains Subflatus3's `sbs2k.c` verbatim up to and including its
per-trial function and adds `trial_w4`, the same lines extended by Y9 =
C1.c1 + ROR(C1.d1 ^ Y1, 8), g1 = Y9 + h1, g1' = Y9 + (h1 ^ eta), c1' = d1 +
Y11', b1' = ROR(Y6 ^ c1', 12), a2' = a1 + b1' + w5 + delta and, for a lane
with rule A and the filter, W4 = P ^ ROR(P, 1) ^ ROR(g1 ^ g1', 12) (Lemma
E). A unit is one batch drawn uniformly with exactly `sbs2k`'s draws
(SplitMix64 starting at state SEED; vd by rejection below V from 21-bit
draws, then w5, vc, S15, S9, the member index below 2^16, g by rejection
below 37,450 from 16-bit draws and i below 2^14; D3.d1 = X3); per unit it
records b, c and w (Lemma U above). Before the plan was frozen,
`crosscheck_ea.py` compared `eaq --context` with the counted program of
this version on the same 24 contexts as 5ca02dfb's cross-check (seeds
1..24, 4,000 consecutive positions each, 8 in the last group; 480,000
lanes): the stage-B decision, c, w and an FNV hash over the batches' (b, c)
and the W4 of every lane with rule A and the filter, read from
`s8stage.forward` as ROL(D4, 7) ^ D1 of the two real digests (Lemma D'),
were equal for all 24 (238 lanes with rule A and the filter, whose W4
entered the hashes), and every 50th lane's digests were also compared with
`verifier/blake3.py` (9,600, all equal). After freezing, the 3 contexts
31..33 (60,000 lanes, one in the last group) were compared with the frozen
binary and the frozen counted program: equal.

*Preregistration.* Before any run of the sample, the counted program (the
shipped program, SHA-256 92c95d72...6a5b4af: its PREMISE line already holds
(377/1000, 1003/1000, 1/2^24), so the sample sets no number the program
reads), `eaq.c` (bef43dcd...aa36da0), its binary (10d77093...5225e3d),
`crosscheck_ea.py` (486ad203...4b4518), the analysis `summarize_ea.py`
(ca822181...fb9740), the seed rule `make_seeds_ea.py` (7851a272...e1590),
the launcher `run_ea.sh` (7c8c2382...25a79), the freeze script and the plan
were fixed and hashed (PREREG_v104_EA.txt, SHA-256 23a2e3a0...caa1bea,
frozen 2026-10-08T13:38:49Z); the seed file was written after the freeze
by the frozen rule (SEEDS_EA.txt, f0d62bcf...e849a8). The same seeds, which
the hash rule fixes, had been printed once before the freeze while the rule
was written, and served as run labels in the synthetic test of the analysis
(run list (c) below); no unit was drawn from them before the freeze, as the
preregistration states. Seeds: run NN (NN = 01..32) uses the
first 16 hex digits of SHA-256('blake3-r2-v104 EA sample NN') as a decimal
SplitMix64 start state; the seed rule checks that the 32 streams (2^35
states each) are pairwise disjoint and disjoint from 5ca02dfb's 32 sample
streams and development seeds 1..9, from our `eaq` development runs and
from the study's development runs, so the two samples share no unit. Plan:
32 runs `./eaq 1073741824 SEED` (2^35 units, 2^37.8 trials), under the
machine's heavy-job lock, at most 8 at once, nice -n 10, each started only
while the 1-minute load average was at most 12. Decision rule (fixed before
the runs, `summarize_ea.py`; delta = 2^-64 for every test; a value m0
passes when the observed sum is below n m0, the Lemma C' exponent
(n m0 - S)^2 / (2 n m0) is at least 64 ln 2 and the empirical Bernstein
bound is at most m0):

- (R) m0 = 2^-24 (262,144 / 262,150) must pass for r = w/7;
- (B), (C) the premises inherited from 5ca02dfb must pass as a
  reproduction: m0 = 0.377 p_B for b and m0 = 1.003 * 2^-11
  (262,144 / 262,150) for x = c/7;
- PROCEED iff all three pass; otherwise STOP (no package from this
  design). Both tests are monotone in m0, so each pass is an upper
  confidence bound at the tested value with error probability at most
  2^-64 per test; no grid search enters the decision.

| event (32 runs, 34,359,738,368 units, 240,512,672,372 = 2^37.8073 trials) | count | unit mean +- s.e. | empirical Bernstein (2^-64) | Lemma C' at the value tested | tested value |
|---|---:|---:|---:|---:|---:|
| batch enters stage B | 2,578,478,067 batches | 0.376587 +- 0.000007 of p_B | 0.376654 p_B | exp(-1551) | 0.377 p_B: passes |
| rule A and filter (x = c/7 per batch) | 117,436,528 trials (sum of c^2: 123,000,380) | 0.99999 +- 0.00009 of 2^-11 | 1.00089 | exp(-75.8) | 1.003 * 2^-11: passes |
| rule A, filter and W4 = 0 (r = w/7 per batch) | 60 trials (60 batches; w <= 1) | 2^-31.90 per trial (2.49 * 10^-10) | 2^-28.04 (3.61 * 10^-9) | exp(-1015) | 2^-24: passes |
| batch enters stage C (not in (ii)) | 114,699,895 batches | 0.0033382 per batch | | | |

**Decision.** All 32 runs were present (started 2026-10-08T13:45:09Z to
13:47:57Z, all ended with exit status 0 by 13:48:41Z; 1-minute load at most
9.64 at every start), each with 2^30 units and its seed. All three tests
passed: PROCEED. rho_R = 2^-24 is the premise of H1 (ii) for the early exit,
and the budget E_R is 6001/6000 times it; theta_B = 0.377 and theta_C =
1.003, set by 5ca02dfb's sample, are reproduced by this independent sample
(the smallest passing values on the 1/1000 grid, reported for information,
are again 0.377 and 1.003; for r the smallest passing 2^-k is 2^-28). Per
run (2^30 units each) the stage-B share lies between 0.37645 and 0.37665
p_B and the rate of rule A with the filter between 0.99852 and 1.00094 of
2^-11; the largest c of one batch was 5, the largest w 1. The 916,034 units
in the last group hold one distinct trial each. Among the 117,436,528 lanes
with rule A and the filter, W4 = 0 in 60 (2^-20.90 per such lane), and the
low 8, 16 and 24 bits of W4 are zero in 3,195,833, 156,443 and 2,531
(2^-5.20, 2^-9.55, 2^-15.50 per such lane): W4 is far from uniform on these
lanes, which is why rho_R is a measured run average and not a model value.
Nothing in the program changed after the sample. Run outputs, the log and
the analysis output are hashed in RUN_HASHES_EA.sha256 (SHA-256
07b74b86...aa863).

**v106's transfer sample (participant measurement, `eaq106.c`, Appendix E;
preregistered; it tests the three premises on this package's run).**
`eaq106.c` is ef052659's `eaq.c` with one line changed, VRANGE = 1,057,885
(was 1,512,538), and a new header comment. A unit is one batch of this run
drawn uniformly with exactly `eaq`'s draws (SplitMix64 starting at state
SEED; vd by rejection below 1,057,885 from 21-bit draws, then w5, vc, S15,
S9, the member index below 2^16, g by rejection below 37,450 from 16-bit
draws and i below 2^14; D3.d1 = X3); per unit it records b, c and w as
above. Before the plan was frozen, `crosscheck_ts.py` (`crosscheck_ea.py`
with the context's vd below 1,057,885) compared `eaq106 --context` with
this package's counted program on 24 contexts (seeds 41..64, 4,000
consecutive positions each, 8 in the last group; 480,000 lanes): the
stage-B decision, c, w and the FNV hash over the batches and the W4 of the
243 lanes with rule A and the filter were equal for all 24, and 9,600
digests were also compared with `verifier/blake3.py` (all equal).

*Preregistration.* Before any run of the sample, this package's program
(the shipped program, SHA-256 41a0d8ae...f5777a1; its PREMISE line is
ef052659's, so the sample sets no number the program reads), `eaq106.c`
(56d99d41...776cff8), its binary (93f15dbc...9e9de), `crosscheck_ts.py`
(6d936133...a6295), the analysis `summarize_ts.py` (cf2b1e05...3566f;
`summarize_ea.py` with the seed file, the program name and the decision
label changed), the seed rule `make_seeds_ts.py` (7c1eb793...74874), the
launcher `run_ts.sh` (b36e350c...d8432), the freeze script and the plan
were fixed and hashed (PREREG_v106_TS.txt, SHA-256 21b56d46...e585a7,
frozen 2026-10-08T15:54:25Z); the seed file was written after the freeze
by the frozen rule (SEEDS_TS.txt, 76b49220...2669b). Seeds: run NN (NN =
01..32) uses the first 16 hex digits of SHA-256('blake3-r2-v106 TS sample
NN') as a decimal SplitMix64 start state; the rule checks that the 32
streams (2^35 states each) are pairwise disjoint and disjoint from
ef052659's 32 sample streams, from every stream its rule lists and from
v106's one development run, so this sample shares no unit with the two
earlier samples. Plan: 32 runs `./eaq106 1073741824 SEED` (2^35 units)
under the machine's heavy-job lock, at most 8 at once, nice -n 10, each
started only while the 1-minute load average was at most 12. Decision rule
(fixed before the runs, `summarize_ts.py`; the tests of ef052659's sample,
delta = 2^-64 for every test): (B) m0 = 0.377 p_B must pass for b, (C)
m0 = 1.003 * 2^-11 (262,144 / 262,150) for x = c/7 and (R) m0 = 2^-24
(262,144 / 262,150) for r = w/7; PROCEED iff all three pass, otherwise
STOP (no package on these premises). The sample sets and changes no
premise value; no grid search enters the decision.

| event (32 runs, 34,359,738,368 units, 240,512,663,240 = 2^37.8073 trials; vd below 1,057,885) | count | unit mean +- s.e. | empirical Bernstein (2^-64) | Lemma C' at the value tested | tested value |
|---|---:|---:|---:|---:|---:|
| batch enters stage B | 2,578,500,728 batches | 0.376590 +- 0.000007 of p_B | 0.376658 p_B | exp(-1526) | 0.377 p_B: passes |
| rule A and filter (x = c/7 per batch) | 117,434,659 trials (sum of c^2: 122,996,491) | 0.99997 +- 0.00009 of 2^-11 | 1.00087 | exp(-76.6) | 1.003 * 2^-11: passes |
| rule A, filter and W4 = 0 (r = w/7 per batch) | 49 trials (49 batches; w <= 1) | 2^-32.19 per trial (2.04 * 10^-10) | 2^-28.07 (3.54 * 10^-9) | exp(-1016) | 2^-24: passes |
| batch enters stage C (not in (ii)) | 114,699,083 batches | 0.0033382 per batch | | | |

**Decision (v106).** All 32 runs were present (started 2026-10-08T16:34:01Z
to 2026-10-08T17:07:16Z, all ended with exit status 0 by
2026-10-08T17:08:05Z; 1-minute load at most 9.11 at every start), each with
2^30 units and its seed. Runs 01 to 16 ran from 16:34Z to 16:36Z; the
launcher was then killed while runs 17 to 21 were running, before they wrote
any output, and the resumed launcher restarted them with the same seeds at
17:06Z, as the preregistration requires, and ran 22 to 32 (the log records
both starts). All three tests passed: PROCEED. On this run the stage-B share
is 0.376590 p_B (ef052659's sample, vd below 1,512,538: 0.376587; difference
+0.3 combined standard errors), rule A with the filter 0.99997 of 2^-11
(ef052659's: 0.99999; -0.1 combined standard errors) and rule A, the filter
and W4 = 0 hold on 49 trials, 2^-32.19 per trial (ef052659's: 60, 2^-31.90).
Per run (2^30 units each) the stage-B share lies between 0.37652 and 0.37667
p_B and the rate of rule A with the filter between 0.99850 and 1.00083 of
2^-11; the largest c of one batch was 5, the largest w 1. The 917,556 units
in the last group hold one distinct trial each. Among the lanes with rule A
and the filter the low 8, 16 and 24 bits of W4 are zero at 2^-5.20, 2^-9.55
and 2^-15.55 per lane (ef052659's: 2^-5.20, 2^-9.55, 2^-15.50). The smallest
passing values on the grids, reported for information, are 0.377 and 1.003
for B and C and 2^-28 for r. Nothing in the program changed after the
sample. Run outputs, the log and the analysis output are hashed in
RUN_HASHES_TS.sha256 (SHA-256 d5dd6ac1...c9024).

**The early-exit premise: development runs (disclosed; not used for the
premise).** The quad size 4 and rho_R = 2^-24 were chosen after the
exploratory runs of this version's study (all disclosed, none part of the
sample): `w4rate.c` (the head of c19feef's `rtuni4.c` with the W4 word; one
run of 2 * 10^6 units and eight of 6 * 10^6 units, each unit an outer step,
a member and 64 random X2: 3.07 * 10^9 trials, 1,500,673 lanes with rule A
and the filter, W4 = 0 on 2 of them, about 2^-30.5 per trial; low 8, 16, 24
bits zero at 2^-5.2, 2^-9.5, 2^-15.2 per such lane); `scan.c` (the
stage-B share of other lane layouts and of k consecutive positions sharing
a test: no layout below the stride 2^14's 0.376, and a test over four
positions taken for 0.148 of the quads, which only an alternative not used
here would have needed); the counted prototype `s8q.py` on 5ca02dfb's
machine (pair and quad flows with the early exit: every lane exact against
real digests on 400 + 400 + 400 + 200 + 200 cases, decisions and E
bookkeeping exact); and `hittree2.py` (an exhaustive search over hit trees:
optimum 10 per stage-B entry for four positions). rho_R = 2^-24 was set
about 2^6.5 above the development estimate so that the preregistered test
would decide it with a wide margin; the claim moves by less than 0.0002
for any rho_R up to 2^-20 (at v106's V: 93.0199 at 2^-20, 93.0213 at
2^-16, 93.0441 at 2^-12; Section 9).

**Other orders and earlier samples (reported, not used).** The stage-B
share depends on which trials share a batch. In c19feef's order S2K (seven
consecutive high halves of C2.a1) it is 0.576501 +- 0.000008 p_B (c19feef's
preregistered 2^38-trial sample with `rtuni4.c`, Appendix A), with random
D3.d1 0.6320; in 21252124's order (seven consecutive members of one
context) 0.53912 +- 0.00022 p_B (21252124's preregistered sample;
Subflatus3's per-batch sample in 1d5e54ce, 0.53929). c19feef's sample also
gives rule A with the filter at 0.99987 +- 0.00009 of 2^-11 on S2K batches,
a per-trial rate of the same trials, consistent with 5ca02dfb's and ours.

**The stride scan (Subflatus3's, exploratory, disclosed by 5ca02dfb; not
used for any premise).** Before the counted program of ef81f589 existed, the lane stride was
chosen with `explore.c` (Subflatus3; the per-trial code of `sbbatch.c` with
a configurable lane layout; seed 0 for the scans, seeds below 10 for the
exact layouts). It measured the stage-B share, relative to the full-batch
model value 1 - (31/32)^7, of uniform batches whose seven lanes are
C2.a1 = base + l S: for S = 2^k, k = 0..29 (10^6 units each) the share was
0.3766 at k = 14, 0.4652 at k = 15, 0.5183 at k = 13, 0.5775 at k = 16 and
at least 0.5857 for every other k; for S = m 2^k with odd m < 32 and k = 11
to 14 (4 * 10^5 units each) no stride was below 2^14 (0.3736; next 0.5173
at 2^13). On the exact layouts C2.a1 = (7g + l) 2^k + i with the last
group masked it gave 0.5770 for k = 16 (c19feef's order) and 0.3771 +-
0.0007 for k = 14 (a few runs of 2^20 to 2^22 units). The stride 2^14 was
chosen after these runs, for its share and because it keeps Lemma A3 and
the one-addition update of C2.d1. The premise rests only on the
preregistered sample above, whose runs, seeds, analysis and decision rule
were fixed by its preregistration.

**Scope and limitations of H1.** The factor F = 132,392,960 is assumed; it
is the exact model count 185,350,144 divided by 1.4 (margin 1.400,
GordoAR's choice, the thinnest margin used in this lineage, which used
2.000 before; V is minimal, so the margin is all of the slack), and the
organizer experiments do not measure it. M is untested at probability 2^-100.5
(the R = 0 rate 185,350,144 * 2^-128); it was compared with real trials on
events of probability down to about 2^-38 per trial here (E1 part, E3
partial events; and 2^-30 with D3.d1 = X3, Section 8.1) and down to about
2^-40 for one call by c66f230d; the full event is far below anything
measured. M fails inside one context (rule-A share varies by context); only
averages are measured. The constants, the class and rule A were chosen by
c66f230d to maximize a count of the same kind; S8 was chosen by winglock from the
exact per-member factors of all 524,288 class members. Recomputed for an
earlier version, S8 is the best of all 8,992,320 sub-classes of 2^16
members given by three independent conditions, each fixing one free bit of
e1 or the XOR of two (three of them describe S8 itself). The selection
matters: the full class with rule A and no sub-class already counts
144,123,339 over all 15 betas (1.089 F; betas outside T6 add under 32,000),
so S8 supplies a factor 1.29 of the margin 1.400: if S8's advantage under M
were entirely an artifact of this selection, S8 trials would have the class
rate, and the class count with rule A (1.089 F) is still at least F. The
filter was chosen to contain T6. A choice that is best under M says nothing
about M and may favour parameters where M overstates; the real-trial ratios
of 8.1 are the check we have; the order of enumeration (Section 2) and the
batching (Section 4) were not chosen with any count of good trials (the
batching changes which trials are examined together, not which are run).
37% of the S8 count (44% in the full class) comes from one beta, 18b0e098.
The trials of one outer step share its three coin words (outer steps have
independent coins; D3.d1 = X3 in all of them); trials of one context (outer
step and X2) differ only in Y4, and trials with the same outer step and
member share Y12 and w5, two of E1's inputs, over all 2^32 values of X2,
while E1's a1 varies with Y1 and Y6; for part (i) independence is assumed.
Part (ii) is a first-moment statement: its run averages are estimated
without bias from uniform samples of 2^35 batches (2^37.8 trials) of this
order, three of them: 5ca02dfb's and ef052659's, which drew vd below
1,512,538, and v106's, drawn from this run (stage B at 0.376590, 0.376587
and 0.376590 p_B against the asserted 0.377 p_B, a margin of about
1.0011; rule A with the filter at 1.00006, 0.99999 and 0.99997 * 2^-11
against 1.003 * 2^-11; rule A with the filter and W4 = 0 at 2^-31.90 and
2^-32.19 per trial against 2^-24, a margin of about 2^7.9), and the
run has 2^100.0 trials; no independence is assumed
for it, and the budgets follow from it by Theorem 2. The sample's probabilities are over a seeded generator's
choices, the program is a participant program and all samples ran on the
participant side; the organizer experiments see the stage events only in
21,504 clustered lanes per run, and no continuation at all.

**Run selection.** No organizer-run count or frequency supports F, the
averages of H1 (ii) or the success probability. Every predicted observation
of Section 6 is an exact per-seed predicate, so no choice among runs can
make it pass; the rule-A, filter and stage-entry totals are reported for
information, every replay of the shipped program included (Section 6). No
parameter, version, seed or nonce was chosen on replay outcomes: S8, the
filter and the count come from the model count, the margin 1.400 of F from
GordoAR's 6a600434 and 3f8e4e89 (V then follows from the success bound of
Section 7), the stage tests from Lemma A and the
filter, D3.d1 = X3 from the operation count (21252124), the order S2K from
c19feef's operation count and pilot, the stride 2^14 from Subflatus3's
stride scan, theta_B and theta_C from 5ca02dfb's preregistered sample (as
5ca02dfb reports it, Section 8.2 above). For this version: the quad test,
the hit tree, the early exit and the register plan were chosen by operation
counts (Section 5); the quad size 4 and rho_R = 2^-24 were chosen after the
development runs listed below, and both were fixed, with every number the
program reads, before this version's preregistered sample; nothing was
changed after it (v106 then changed only the ledger constants V_RANGE and
F_H1, which no sample reads, before its own sample). All runs made for this version: (a) the study's development runs (`scan.c`, `w4rate.c`, the prototype `s8q.py` with its
register profile `kpeak.py`, `hittree2.py` and the exact-ledger scripts; this section above); (b) on drafts of the
program: the self-tests listed in Section 5, `--ledger`, and one development runner run on the public seed (both
experiments 256 of 256, every predicted observation exact); (c) for the sampler before the preregistration: the timing
runs `eaq 2000000 5` and `eaq 16777216 6` (W4 = 0 on no lane; outputs not saved), the 24-context cross-check, one
test of `summarize_ea.py` on synthetic run files (labelled with the seeds), and two executions of `make_seeds_ea.py` while it was written (the
first stopped at its disjointness check on an overlap of two earlier development streams, which it no longer
compares; the second printed the seeds, which are fixed by the rule); (d) the 32 runs of the preregistered sample,
and after freezing the 3-context cross-check; (e) on the shipped program: the 2,000-case self-test, `--ledger`, the
exact ledgers of the stricter readings and sensitivities of Section 9 (`ledger_parts.py`), `count_s8.py`, the nine
broken copies of Section 5 and the 41 preregistered replays of Section 6.
All runs made for v106: (f) `--ledger` on this package's program, a scan
of V with ef052659's ledger code (V = 1,057,885 is the smallest value with
success at least 0.39), the exact ledgers and sensitivities of Section 9
(`ledger_parts.py`), the exact integer certificates of the claim at the
fourth and fifth decimal, and a second `--ledger` run (output identical;
none of these samples anything); (g) for the transfer sample before its
preregistration: one smoke run `eaq106 4194304 106` (stage B in 315,385 of
4,194,304 units, 14,186 lanes with rule A and the filter, W4 = 0 on none),
one `--context` comparison of `eaq` and `eaq106` (equal), the 24-context
cross-check and one test of `summarize_ts.py` on synthetic run files
(ef052659's 32 outputs relabelled); (h) the 32 runs of the transfer
sample and its frozen analysis, run once after all 32 had ended; (i) on
the shipped program: the 2,000-case self-test (seed 9;
output byte-identical to ef052659's), `count_s8.py` and one runner run on
the public seed. The broken copies and the 40 holdout-style replays were
not repeated for v106 (its program differs from ef052659's only in the two
ledger constants).
No run was discarded or selected, and none was repeated, with one
disclosed exception in v106's transfer sample: its launcher was stopped
(SIGTERM) at 2026-10-08T16:36Z, when the session building this package was
stopped, while runs 17 to 21 were running; they had written no output
(their output files were empty and the program prints only at its end), so
nothing of them was seen. As the preregistration requires, the resumed
launcher restarted them with the same seeds at 17:06Z and then ran 22 to
32; the log records both starts. The runs made for
5ca02dfb, ef81f589 and c19feef are listed in those packages (5ca02dfb's
list: the stride scan; development self-tests, ledgers, runner runs and
broken copies; three sampler timing runs, the 24-context cross-check and a
test of its analysis; its 32 sample runs and the 3-context cross-check; on
the per-batch S2K14 program `--ledger`, stricter-reading ledgers, a
2,000-case self-test, `--count` and 41 replays; for the pair test
self-tests of 60, 40, 20 and 2,000 cases, a 4,000-pair staged-flow script,
the register profile, two runner runs, six broken copies, `--count` and 41
replays).

*Run records (SHA-256 prefixes of the saved outputs; participant files).*
(a) the study's run list DEV_RUNS.txt 0c242fae and its hash list a0cfe34b
(the `w4rate.c` outputs 55e957be, the four-position scan bf8d29fd, the
prototype runs); (b) draft self-tests of 3, 20 and 200 cases 580d4e7a,
306e8d5b, c858ef0c (11 and 6 cases: not saved), development runner run
c42626af; (c) cross-check before the freeze 660584da, synthetic analysis
test fe75130c; (d) preregistration 23a2e3a0, frozen files 28501b35, seeds
f0d62bcf, run outputs and log RUN_HASHES_EA.sha256 07b74b86, analysis
output 6a5735a2, cross-check after the freeze fcfc6dee; (e) self-test
35a68d11, `--ledger` 2a1d4430, stricter readings 49e02f36, `count_s8.py`
c2c8eca7, broken copies 3518a3ef and 55a2e260, replay plan 901ea288,
replay log 18f7ba40 and output hashes 6cef4597; the abandoned draft of an
earlier session fc99e70e. For v106: (f) `--ledger` 73e29e3d, stricter
readings 7e1c3d67, certificate 2a246e76 (fourth decimal) and 99f44e26 (fifth); (g) smoke run e4e1b00b,
cross-check 98e22a40, synthetic analysis test 96d71699 (its synthetic seed file; the printed output was not saved); (h)
preregistration 21b56d46, frozen files 1c0911e8, seeds 76b49220, run
outputs and log d5dd6ac1, analysis output 700520ae; (i) self-test
35a68d11 (equal to ef052659's), `count_s8.py` 04965081, runner run
7967914a.

## 9. Charged time

Per outer step (vd, w5), 2^48 trials, fixed work:

    324 + 28 + (2^32 + 2^14) * 94 + 2^16 * (120 + 37,449 * 21 + 12 + 37,450 * (64 * 4 + 2^12 * 70))
      = 704,787,131,171,168 operations

(the outer step with its random word; the table entry and 2^32 + 2^14
table words; per member the member step, 37,449 groups with set-up and end
(13 + 8) and the last group (11 + 1), and in every group 64 block updates
and stage A of 2^12 quads of batches, 70 operations per quad including the
quad test). Every group body is straight-line code: the 2^14 positions are
unrolled (each position reads its own table words at its own offsets from
the group's pointer), and the hit tree and, for each of its 15 leaves,
stages B and C and the continuation of each batch of the leaf are out of
line and duplicated for each quad, each copy's last instruction jumping on
(to the next batch of the leaf or the next quad), so an entry costs exactly
the 66 and 61 operations of Section 5, plus at most 10 of the hit tree per
stage-B entry and at most 235 per continuation, and no loop operation is
executed inside a group. There are four copies of the group body (one per
D slot, Section 5), each under 2^12 * 2^14 instructions (per quad: stage A
and the test, the tree, and for the 15 leaves 32 batch copies of stages B,
C and the continuation, under 2^14 instructions), so the code is below
2^28 instructions (Section 10); all groups and members run these bodies
(only the pointer, the registers and, in the last group, B32 differ).
Stages B and C and the continuation are charged at their budgets, whatever
the coins: E_B * (66 + 10), E_C * 61 and E_R * 235 operations for the run
(a group starts only if 2^14 entries of stages B and C are left, and a
continuation only if cR > 0, so no entry beyond a budget is executed).

- Fixed work: 704,787,131,171,168 * V * 2^32 = 2.50391 * N operations
  (stage A 2.50006, block updates 0.00223, table 0.00143, groups, members
  and outer steps 1.9 * 10^-4 per trial).
- Stage B with the hit tree: E_B * 76 = 0.81581 * N (0.377 * 6001/6000 * p_B
  * 37,450 / 2^18 * 76; of this 0.70846 for stage B and 0.10734 for the hit
  tree).
- Stage C: E_C * 61 = 0.02988 * N (1.003 * 6001/6000 * 2^-11 * 61).
- Continuation: E_R * 235 = 0.000014 * N (2^-24 * 6001/6000 * 235).
- Per value of vd: next value, end test and loop entry, under 2^6.
- The member list (65,536 words), the block constants (128 words), D0S,
  DLAST, B32_01, the three global words kept in memory and the three budgets:
  under 2^22 operations once.
- Step 3: at most once: the trial recomputed in scalar form, its two
  messages built and 2 compressions, under 2^25 operations (5ca02dfb's
  bound, which also covered recomputing a whole group).
- Writing the code once: the four unrolled group bodies (with the last
  group's prologue) have under 2^28 instructions (Section 10), each written
  by a generator loop in under 2^4 operations: under 2^32 operations, 2^23.3
  units. The formula below and the program's `--ledger` omit this term; it
  multiplies T by less than 1 + 2^-69, so T and time_log2 are unchanged.
- Preprocessing: 2^86 units, declared below.

    T = (704,787,131,171,168 * V * 2^32 + 76 E_B + 61 E_C + 235 E_R + 2^6 V + 2^22 + 2^25) / 430 + 2 + 2^86
      = 2^93.019712 (3.349608 operations per trial: 2^93.0086 without the
                2^86 + 2 units, which add 0.0112)

time_log2 = 93.0197119938..., claimed **93.01972** (rounded up at the
fifth decimal; T^100000 < 2^9301972 and T^100000 > 2^9301971, checked in
exact integers). `python3 experiments/s8stage.py --ledger` computes T in
exact rational arithmetic (it prints 93.019712 and, at four decimals,
93.0198). The claim holds for any total up to 3.349626 operations per
trial. Under stricter readings: the budget registers cB and cC kept in
memory (load, subtract, store: 2 more operations per entry) give 2^93.0293;
a loop over the quads (pointer add, compare, branch: 3 operations per quad)
instead of the unrolled group body gives 2^93.0648; all eight stage-C words
loaded instead of five gives 2^93.0204. The hit-tree charge 10 per stage-B
entry is not a reading but a bound: every taken quad test costs at most 10
times the number of its stage-B entries (Section 5). Sensitivity to the
early-exit premise: rho_R = 2^-20, 2^-16 and 2^-12 give 93.0199, 93.0213
and 93.0441 (all below 93.0451); a continuation charged at 1,000
operations gives 2^93.019731. For comparison, 5ca02dfb's ledger gives
2^93.557577 at its own V and F (its claim) and 2^93.045076 at v106's V and
F (the claim 93.0451 of GordoAR's 3f8e4e89); ef052659's ledger at its V
and F gives 2^93.532155 (its claim), and c19feef gives 2^93.735734.

**Preprocessing (declared charge).** The program stores the six constants
of Fact P, eta, the rule-A words, the filter words, the stage-test words,
the block constants, the S8 conditions and the hit tree. The constants were
found by c66f230d with solver searches and chosen with model counts; rule
A, S8 and the filter were chosen with counts of the same kind (S8 by
winglock from the exact per-member factors of all 524,288 class members,
best of 8,992,320 candidate sub-classes); the order of the construction and
the staged batch were found by 60f94c5c, the loop order S2K by c19feef
(with its pilot), the stride 2^14 and the pair test by Subflatus3 (with the
stride scan of Section 8.2), the quad test, the hit tree (exhaustive
search), the early exit and rho_R by winglock in ef052659 (with the
development runs and the sample of Section 8.2, under 2^50 word
operations in all), the margin 1.400 of F by GordoAR (6a600434,
3f8e4e89), V and the transfer sample by v106 (under 2^50 word operations),
and the premise and budget conventions by 52bb50ee and 5266c5ce. We do not
reconstruct this work from run records. We charge a declared upper bound
of 2^86 units (2^94.75 word operations) for all of it, v106's, GordoAR's,
ef052659's, 5ca02dfb's, c19feef's and its predecessors', c66f230d's, 60f94c5c's,
52bb50ee's and 5266c5ce's, including every count and measurement of
Section 8 (the samples of Section 8.2 included). It is more than 2^34 times
c66f230d's own estimate of their selection (below 2^60 operations, from
running times on one desktop machine and one graphics card), and more than
2^3.5 times ten years at 2^63 operations per second (over four times the
peak rate of the fastest listed supercomputer, about 2^61.3 FP64
operations per second), so it exceeds any computation physically performed
for this selection before the submission date. This is a declared
upper-bound charge, not a premise: H1 does not depend on it, and no part of
the success bound uses it. The charge moves the scalar by 0.0112. The
stored values themselves need no search to check: Fact P, Lemma Q, Lemma B,
Lemma A3's constants, the stage-test words and the hit tree are finite
computations repeated by the self-test and the experiments.

## 10. Memory and advice

Search memory: the X2 table of an outer step, (2^32 + 2^14) * 8 * 32 bytes
(under 2^41 bytes); code below 2^28 instructions, under 2^32 bytes (the
four unrolled group bodies with, per quad, the out-of-line hit tree and,
for each of its 15 leaves, stages B and C and the continuation of each
batch of the leaf); the member list, block constants, constants, the
stored words of step O and of the member step, budget registers and the
budget word, spilled words and temporaries below 2^20 bytes: below 2^42
bytes in all. For the preprocessing we use no reported peak: every byte it
stores is written by one of its charged word operations, so it stored at
most 32 * 2^94.75 = 2^99.75 bytes; memory_log2_bytes = 100 is this bound
and covers the search (the cost model gives memory no scalar contribution).
Advice: the six constants, eta, the rule-A, stage-test and filter words, the
block-constant rule and the S8 conditions, below 64 bytes
(nonuniform_advice_log2_bytes = 6); the hit tree, like the loop order, is
part of the code. preprocessing_log2 = 86 as charged above.

## Appendix A. c19feef's measuring programs (order S2K)

These are winglock's c19feef files, reproduced unchanged (as 5ca02dfb
reproduced them) because Section 8.1 uses the per-trial rates of their
sample and Section 8.2 reports their S2K numbers; no premise of this
package is set from them (the "shipped
program" and "v103" in their text are c19feef's). They are c19feef's
preregistered files (SHA-256: rtuni4.c 4bbd2090...b8263,
rtunicheck4.py 75d45d2d...f2a7, summarize4.py 9dd193a4...aaa23; the binary
fdb899c5...db76, the seed rule make_seeds4.py d3b5ae59...d520 and the
launcher run_holdout4.sh 3feebe35...b218 are listed in the frozen
preregistration, SHA-256 e2247e2b...1f4d). `rtuni4.c` is compiled with `cc -O3
-march=native` and run as `./rtuni4 unit 1227227136 SEED fixed` (32 seeds)
and `./rtuni4 unit 1227227136 SEED rand` (8 seeds). It computes the trials
forwards with the lines of steps O, M, Y and T, the member list of S8 and
the batches of the order S2K, and tests rule A on h1 of E3 and the filter
on c1 of E1 of message A, exactly as the counted program's forward
computation does (checked by `rtunicheck4.py`, which also runs every tenth
unit through the counted pieces; it imported the counted program
3aef733e...e27518, the shipped program before its PREMISE line was set,
which differs from the shipped program only in that line, although its
docstring below says 'the shipped program'). Its per-trial formulas are
those of 21252124's `rtuni2.c` and v101's `rt2l.c`.

```c
/* rtuni4.c -- uniform per-batch sample of the H1 (ii) stage events of v103 in the order S2K (D3.d1 = X3, X14 = 0),
   with E1 and E3 partial events for H1 (i).  Per-trial formulas are those of rtuni3.c / rtuni2.c (v102: steps O, M, Y,
   T of 60f94c5c, C2, C1, E1, rule A on h1 of E3, the filter on c1 of E1) and rt2l.c (v101: E3 events G and D16).

   Unit = one batch of the run, drawn uniformly: fresh coins C0.c1, D3.d1 (used only in MODE rand), S15, S9, then w5,
   vd uniform below V = 1,512,538, member m < 2^16, group g < 9,363, position i < 2^16 -- nine SplitMix64 draws, in
   this order.  Lane l (l < 7; in the last group g = 9,362 only l < 2, the distinct trials) is the trial with
   X2 = ((7g + l) 2^16 + i - X6_m - w7) mod 2^32, i.e. C2.a1 = (7g + l) 2^16 + i.  Units are i.i.d.;
   b = 1{some lane satisfies rule A} (the batch enters stage B), c = number of lanes with rule A and the filter (0..7).
   Events per trial: A rule A, F filter, AF both, T6 beta in T6, T6A, N12 (low 12 bits of the Lemma N word zero),
   T6N8 (beta in T6 and low 8 bits of n zero), G (E3: g1 ^ g1' = ROL(psi,12), psi = tau ^ ROR(tau,1), tau = 285020a0),
   D16 (low 16 bits of the digest differences D1 and D3 zero).

   usage: rtuni4 unit NUNITS SEED MODE   -> one JSON line of sums          (MODE fixed | rand)
          rtuni4 dump NUNITS SEED MODE   -> one line per unit (for rtunicheck4.py)
   SEED is decimal; the stream starts at SEED * 0x1234567 + 77 (mod 2^64), as in rtuni2 and rtuni3.                */
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>
typedef uint32_t u32; typedef uint64_t u64;
static inline u32 ror(u32 x,int r){ return (x>>r)|(x<<(32-r)); }
static inline u32 rol(u32 x,int r){ return (x<<r)|(x>>(32-r)); }
static const u32 IV[8]={0x6a09e667,0xbb67ae85,0x3c6ef372,0xa54ff53a,0x510e527f,0x9b05688c,0x1f83d9ab,0x5be0cd19};
static const u32 X3=0x29d4fa98,X7=0xbee3af28,X11=0x44036000,X15=0x40c58500,W4=0x97475638,W13=0x0007c006;
static const u32 Y3=0x8127c181,Y3P=0x7edf3e7e,Y11=0x7af77f38,Y11P=0x850000c3,ETA=0x830303cf;
static const u32 T6[6]={0x18b0e098,0x18b1a098,0x18d0e098,0x18d1a098,0x18b3e098,0x18d3e098};
static inline int inT6(u32 b){ for(int i=0;i<6;i++) if(b==T6[i]) return 1; return 0; }
static u64 sm; static inline u64 rnd(void){ u64 z=(sm+=0x9E3779B97F4A7C15ULL); z=(z^(z>>30))*0xBF58476D1CE4E5B9ULL; z=(z^(z>>27))*0x94D049BB133111EBULL; return z^(z>>31); }
static u32 S8[65536];
static void members(void){
  int ord[16]={14,30,31,4,5,6,7,10,11,12,13,20,21,27,28,29};
  for(u32 i=0;i<65536;i++){ u32 e1=0x030c0303|0xc; for(int t=0;t<16;t++) if(i>>t&1) e1|=1u<<ord[t]; if(e1>>21&1) e1|=1u<<26; S8[i]=e1-Y3; }
}
static inline int ruleA(u32 h){ return !(h&1) && !((h>>16)&1) && !((h>>17)&1) && ((h>>1)&1) && (((h>>2)^(h>>3))&1); }
#define G1(a,d,c,b,x,y) do{ a=a+b+x; d=ror(d^a,16); c=c+d; b=ror(b^c,12); a=a+b+y; d=ror(d^a,8); c=c+d; b=ror(b^c,7);}while(0)
static u32 K2A,K2B,K2C,K2D,DELTA,PSI_R;
typedef struct { u32 c0c,c0d,s15,w5,S2,S6,S10,S11,S7,S4,X4,X9,X13,X14,w6,w7,Cb,D2b,D2c,s9; } Outer;
typedef struct { u32 X2,w0,w2,w3,w12,S0,S1,S5,S12; } Ctx;
typedef struct { u32 y,Y12,ca,X6,dd,X1; } Mem;
typedef struct { u64 A,F,AF,T6,T6A,N12,T6N8,G,D16,nt; } Cnt;
static inline void outer_draw(Outer*o,int fixed){   /* rtuni2's per-outer-step draws and words, same order */
  u32 c0c=(u32)rnd(), d3r=(u32)rnd(), s15=(u32)rnd(), s9=(u32)rnd();
  u32 d3d=fixed?X3:d3r;
  u32 w5=(u32)rnd(), c0d=(u32)(rnd()%1512538ULL);
  u32 S2=K2A+K2B+w5, S14=ror(K2D^S2,8), S10=K2C+S14, S6=ror(K2B^S10,7);
  u32 d3a=rol(d3d,16)^S14, d3c=s9+d3d, d3b=X3-d3a, S4=rol(d3b,12)^d3c, S3=d3a-S4, X14=ror(d3d^X3,8), X9=d3c+X14, X4=ror(d3b^X9,7);
  u32 k3d=rol(s15,8)^S3, k3c=IV[3]+k3d, k3b=ror(IV[7]^k3c,12), S11=k3c+s15, S7=ror(k3b^S11,7), k3a=rol(k3d,16)^11;
  u32 w6=k3a-IV[3]-IV[7], w7=S3-k3a-k3b, X8=c0c-c0d, Cb=ror(X4^c0c,12), D2b=rol(X7,7)^X8, D2c=rol(D2b,12)^S7, X13=X8-D2c;
  o->c0c=c0c; o->c0d=c0d; o->s15=s15; o->w5=w5; o->S2=S2; o->S6=S6; o->S10=S10; o->S11=S11; o->S7=S7; o->S4=S4; o->X4=X4;
  o->X9=X9; o->X13=X13; o->X14=X14; o->w6=w6; o->w7=w7; o->Cb=Cb; o->D2b=D2b; o->D2c=D2c; o->s9=s9;
}
static inline void ctx_of(const Outer*o,u32 X2,Ctx*x){   /* step M for one X2 (rtuni2's per-X2 words, and S0) */
  u32 d2a=X2-o->D2b-W13, d2d=rol(o->X13,8)^X2, S13=rol(d2d,16)^d2a, S8v=o->D2c-d2d, w12=d2a-o->S2-o->S7;
  u32 k1c=o->s9-S13, k1d=k1c-IV[1], k1a=rol(k1d,16), k1b=ror(IV[5]^k1c,12), S1=rol(S13,8)^k1d, S5=ror(k1b^o->s9,7);
  u32 w2=k1a-IV[1]-IV[5], w3=S1-k1a-k1b;
  u32 k0b=rol(o->S4,7)^S8v, k0c=rol(k0b,12)^IV[4], k0d=k0c-IV[0], k0a=rol(k0d,16), S12=S8v-k0c, w0=k0a-IV[0]-IV[4];
  u32 S0=rol(S12,8)^k0d;
  x->X2=X2; x->w0=w0; x->w2=w2; x->w3=w3; x->w12=w12; x->S0=S0; x->S1=S1; x->S5=S5; x->S12=S12;
}
static inline void mem_of(const Outer*o,u32 m,Mem*v){    /* step Y for member m (rtuni2's table row) */
  u32 y=S8[m], Y8=rol(y,7)^o->Cb, Y12=Y8-o->c0c, Y0=rol(Y12,8)^o->c0d, ca=Y0-o->Cb-o->w6, X12=rol(o->c0d,16)^ca;
  u32 dc=X11-X12, db=ror(o->S6^dc,12), X6=ror(db^X11,7), dd=dc-o->S11, X1=rol(X12,8)^dd;
  v->y=y; v->Y12=Y12; v->ca=ca; v->X6=X6; v->dd=dd; v->X1=X1;
}
/* one trial: rtuni2's inner-loop body, then E1 and E3 of both messages as rt2l.c; returns 1 for rule A, 2 for the filter */
static inline int trial(const Outer*o,const Ctx*x,const Mem*v,Cnt*c){
  u32 X0=v->ca-o->X4-x->w2, fd=rol(X15,8)^X0, fc=o->S10+fd, X10=fc+X15, fb=ror(x->S5^fc,12), X5=ror(fb^X10,7);
  u32 ga=rol(v->dd,16)^x->S12, w10=ga-x->S1-o->S6, w8=(rol(fd,16)^o->s15)-x->S0-x->S5;
  u32 a2=x->X2,b2=v->X6,c2=X10,d2=o->X14; G1(a2,d2,c2,b2,o->w7,x->w0); u32 Y6=b2,Y14=d2;
  u32 e1=Y3+v->y, h1=ror(Y14^e1,16); int A=ruleA(h1);
  u32 a=v->X1,b=X5,cc=o->X9,d=o->X13; G1(a,d,cc,b,x->w3,w10); u32 Y1=a,Y9=cc;
  u32 ea1=Y1+Y6+x->w12, ed1=ror(v->Y12^ea1,16), ec1=Y11+ed1; int F=((ec1&0x00098188)==0x00008000);
  u32 ec1p=Y11P+ed1, eb1=ror(Y6^ec1,12), eb1p=ror(Y6^ec1p,12), ea2=ea1+eb1+o->w5, ea2p=ea1+eb1p+o->w5+DELTA;
  u32 ec2=ec1+ror(ed1^ea2,8), ec2p=ec1p+ror(ed1^ea2p,8), beta=eb1^eb1p, eps=ec2^ec2p, n=eps^rol(beta^eps,1)^ETA;
  u32 e1p=Y3P+v->y, h1p=h1^ETA, g1=Y9+h1, g1p=Y9+h1p, f1=ror(v->y^g1,12), f1p=ror(v->y^g1p,12);
  u32 e2=e1+f1+w8, e2p=e1p+f1p+w8, h2=ror(h1^e2,8), h2p=ror(h1p^e2p,8), g2=g1+h2, g2p=g1p+h2p;
  u32 D1=(ea2^ea2p)^(g2^g2p), D3=(e2^e2p)^eps;
  int t6=inT6(beta); c->T6+=t6; c->T6A+=t6&A; c->N12+=((n&0xfff)==0); c->T6N8+=t6&((n&0xff)==0);
  c->G+=((g1^g1p)==PSI_R); c->D16+=((D1&0xffff)==0)&&((D3&0xffff)==0);
  c->A+=A; c->F+=F; c->AF+=A&F; c->nt++;
  return A|(F<<1);
}
int main(int argc,char**argv){
  if(argc<5){ fprintf(stderr,"usage: rtuni4 unit|dump NUNITS SEED MODE\n"); return 1; }
  int dump=!strcmp(argv[1],"dump"), unit=!strcmp(argv[1],"unit");
  if(!(dump||unit)){ fprintf(stderr,"usage\n"); return 1; }
  const char*seeds=argv[3], *mode=argv[4];
  if(strcmp(mode,"fixed") && strcmp(mode,"rand")){ fprintf(stderr,"mode\n"); return 1; }
  int fixed=!strcmp(mode,"fixed");
  sm=strtoull(seeds,0,10)*0x1234567ULL+77;
  members();
  u32 K=IV[2]+IV[6]; DELTA=W4-(((K+W4)^8)-K); K2A=K+W4; K2D=ror(K2A^55,16); K2C=IV[2]+K2D; K2B=ror(IV[6]^K2C,12);
  { u32 tau=0x285020a0, psi=tau^ror(tau,1); PSI_R=rol(psi,12); }
  Cnt c; memset(&c,0,sizeof c); Outer o; Ctx x; Mem v;
  long NU=atol(argv[2]); u64 SB=0,SC=0,C1=0,C2=0,cmax=0,last=0;
  for(long u=0;u<NU;u++){
    outer_draw(&o,fixed);
    u32 m=(u32)(rnd()&0xffff), g=(u32)(rnd()%9363ULL), i=(u32)(rnd()&0xffff);
    mem_of(&o,m,&v);
    u32 cK=v.X6+o.w7; int nl=(g==9362)?2:7; int aA=0; u64 k=0; Cnt c0=c;
    for(int l=0;l<nl;l++){
      u32 X2=((7*g+(u32)l)<<16)+i-cK;
      ctx_of(&o,X2,&x);
      int r=trial(&o,&x,&v,&c); aA|=r&1; k+=(r==3);
    }
    SB+=aA; SC+=(k>0); C1+=k; C2+=k*k; if(k>cmax) cmax=k; last+=(g==9362);
    if(dump) printf("%u %u %u %u %u %u %d %llu %llu %llu %llu %llu %llu %llu %llu %llu\n",o.c0c,o.c0d,o.w5,m,g,i,aA,(unsigned long long)k,
                    (unsigned long long)(c.A-c0.A),(unsigned long long)(c.F-c0.F),(unsigned long long)(c.T6-c0.T6),(unsigned long long)(c.T6A-c0.T6A),
                    (unsigned long long)(c.N12-c0.N12),(unsigned long long)(c.T6N8-c0.T6N8),(unsigned long long)(c.G-c0.G),(unsigned long long)(c.D16-c0.D16));
  }
  if(!dump)
    printf("{\"units\":%ld,\"seed\":%s,\"mode\":\"%s\",\"trials\":%llu,\"SB\":%llu,\"SC\":%llu,\"C1\":%llu,\"C2\":%llu,\"cmax\":%llu,\"lastgroup\":%llu,"
           "\"A\":%llu,\"F\":%llu,\"AF\":%llu,\"T6\":%llu,\"T6A\":%llu,\"N12\":%llu,\"T6N8\":%llu,\"G\":%llu,\"D16\":%llu}\n",NU,seeds,mode,
           (unsigned long long)c.nt,(unsigned long long)SB,(unsigned long long)SC,(unsigned long long)C1,(unsigned long long)C2,
           (unsigned long long)cmax,(unsigned long long)last,(unsigned long long)c.A,(unsigned long long)c.F,(unsigned long long)c.AF,
           (unsigned long long)c.T6,(unsigned long long)c.T6A,(unsigned long long)c.N12,(unsigned long long)c.T6N8,
           (unsigned long long)c.G,(unsigned long long)c.D16);
  return 0;
}
```

```python
"""Cross-check of rtuni4 (unit and dump modes) against the shipped program's forward computation of real messages.
Draws NUNITS units exactly as rtuni4 draws them (SplitMix64 from SEED * 0x1234567 + 77: C0.c1, D3.d1, S15, S9, w5,
vd mod V, m = low 16 bits, g mod 9,363, i = low 16 bits), builds the batch's distinct trials in the order S2K
(X2 = ((7g + l) 2^16 + i - X6_m - w7) mod 2^32), computes both messages and their 2-round compressions with
s8stage.trial_words / s8stage.trace, and compares, unit by unit, the drawn words, the stage-B flag, c and the per-unit
counts of A, F, T6, T6A, N12, T6N8, G and D16 with `rtuni4 dump NUNITS SEED MODE`; in mode fixed, every tenth unit is
also run through the counted program (s8stage.Case: outer step, member step, group set-up, block update, the three
stages of the batch at position i) and its two stage decisions are compared with (b, c > 0).
usage: python3 rtunicheck4.py NUNITS SEED MODE DIR_OF_s8stage.py"""
import sys, json, subprocess
sys.path.insert(0, sys.argv[4])
import s8stage as s
M = (1 << 64) - 1; M32 = 0xffffffff
class SM:
    def __init__(self, seed): self.s = (seed * 0x1234567 + 77) & M
    def __call__(self):
        self.s = (self.s + 0x9E3779B97F4A7C15) & M; z = self.s
        z = ((z ^ (z >> 30)) * 0xBF58476D1CE4E5B9) & M; z = ((z ^ (z >> 27)) * 0x94D049BB133111EB) & M; return (z ^ (z >> 31)) & M
nu, seed, mode = int(sys.argv[1]), int(sys.argv[2]), sys.argv[3]
tau = 0x285020a0; PSI_R = s.rol(tau ^ s.ror(tau, 1), 12)
r = SM(seed)
lines = subprocess.run(['./rtuni4', 'dump', str(nu), str(seed), mode], capture_output=True, text=True).stdout.split('\n')
bad = 0; tot = dict(units=0, SB=0, C1=0, A=0, AF=0, G=0, lastgroup=0); prog_n = prog_bad = 0
for u in range(nu):
    c0c, d3r, s15, s9 = [r() & M32 for _ in range(4)]
    w5 = r() & M32; vd = r() % 1512538; m = r() & 0xffff; g = r() % s.NBATCH; i = r() & 0xffff
    d3d = s.X3 if mode == 'fixed' else d3r
    o = s.outer([c0c, vd, d3d, s15, s9, w5]); y = s.member(m)
    c = (s.member_vals(o, y)['X6'] + o['w7']) & M32
    ev = dict(A=0, F=0, T6=0, T6A=0, N12=0, T6N8=0, G=0, D16=0); anyA = 0; k = 0
    for l in range(2 if g == s.NBATCH - 1 else 7):
        X2 = (((7 * g + l) << 16) + i - c) & M32
        v = s.middle(o, X2)
        A_, B_, w, wp = s.trial_words(v, y); ta, tb = s.trace(w, 55), s.trace(wp, 63)
        h1 = ta[(1, 'E3')][1]; a = int(s.ruleA_h1(h1)); E1a, E1b = ta[(1, 'E1')], tb[(1, 'E1')]
        f = int((E1a[2] & s.MF) == s.VF); beta = E1a[3] ^ E1b[3]; eps = E1a[6] ^ E1b[6]; n = eps ^ s.rol(beta ^ eps, 1) ^ s.ETA
        t6 = int(beta in s.T6); D1 = ta['digest'][1] ^ tb['digest'][1]; D3 = ta['digest'][3] ^ tb['digest'][3]
        ev['A'] += a; ev['F'] += f; ev['T6'] += t6; ev['T6A'] += t6 & a; ev['N12'] += (n & 0xfff) == 0
        ev['T6N8'] += t6 & ((n & 0xff) == 0); ev['G'] += (ta[(1, 'E3')][2] ^ tb[(1, 'E3')][2]) == PSI_R
        ev['D16'] += (D1 & 0xffff) == 0 and (D3 & 0xffff) == 0
        anyA |= a; k += a & f
    exp = [c0c, vd, w5, m, g, i, anyA, k] + [int(ev[e]) for e in ('A', 'F', 'T6', 'T6A', 'N12', 'T6N8', 'G', 'D16')]
    got = [int(t) for t in lines[u].split()]
    if got != exp: bad += 1
    if mode == 'fixed' and u % 10 == 0:
        cs = s.Case([c0c, vd, s.X3, s15, s9, w5, 0], m, g); out = cs.batch(i, True)[3]
        prog_n += 1; prog_bad += not (cs.ok and out['decA'] == bool(anyA) and out['decB'] == (k > 0))
    tot['units'] += 1; tot['SB'] += anyA; tot['C1'] += k; tot['A'] += ev['A']; tot['AF'] += k; tot['G'] += ev['G']
    tot['lastgroup'] += g == s.NBATCH - 1
summ = json.loads(subprocess.run(['./rtuni4', 'unit', str(nu), str(seed), mode], capture_output=True, text=True).stdout)
sum_ok = all(summ[k] == tot[k] for k in ('SB', 'C1', 'A', 'AF', 'G', 'lastgroup')) and summ['units'] == nu
print(json.dumps({'nunits': nu, 'seed': seed, 'mode': mode, 'totals': tot, 'mismatches': bad, 'unit_mode_sums_equal': sum_ok,
                  'program_units': prog_n, 'program_mismatches': prog_bad, 'equal': bad == 0 and sum_ok and prog_bad == 0}))
```

```python
"""Analysis of the v103 S2K sample (fixed before the runs).  usage: python3 summarize4.py RUNDIR SEEDS4.txt
Run files RUNDIR/NN.json, one line of `rtuni4 unit U SEED MODE` each (NN = hKK fixed, cKK control).
Unit k = one uniform batch of the run in the order S2K: b_k = 1{batch enters stage B} in {0,1}; x_k = c_k / 7 in [0,1],
c_k = trials of the batch with rule A and the filter (at most 7 distinct trials).  Units are i.i.d.; E b_k = run
stage-B share, E x_k = KAP * (run per-trial rate of rule A and filter), KAP = 65,536 / 65,541 exactly.
Bounds, delta = 2^-64: empirical Bernstein (Maurer and Pontil 2009, Thm 4)
  E <= mean + sqrt(2 Vn ln(2/delta) / n) + 7 ln(2/delta) / (3 (n - 1)),  Vn = unbiased sample variance;
Lemma C' (lower-tail Chernoff, [0,1] variables): P(sum <= S) <= exp(-(n theta' - S)^2 / (2 n theta')) for n theta' > S.
Decision (fixed runs only; all runs present, else STOP):
  stage B: premise theta_B = smallest k/10000, 5500 <= k <= 10100, with EB_B <= theta_B p_B and the Lemma C' exponent
  at theta' = theta_B p_B >= 20.  If none passes: STOP (no stage-B premise ships for the order S2K).
  stage C: premise theta_C = smallest k/1000, 1001 <= k <= 1249, with EB_x <= theta_C KAP 2^-11 and the Lemma C'
  exponent at theta' = theta_C KAP 2^-11 >= 20.  If none passes: 5/4 (v102's premise; the trial set is the same).
  Budgets: premise * 6001/6000 each.  Both tests are monotone in theta, so the smallest passing grid value keeps the
  error probabilities at 2^-64 (EB) and e^-20 (Lemma C') with no multiplicity cost.
Also reported (H1 (i), not part of the decision): pooled rates of the per-trial events in mode fixed and mode rand
(control) and their ratio with a Poisson standard error."""
import json, glob, math, sys, os
from fractions import Fraction as Fr
rundir, seedsf = sys.argv[1], sys.argv[2]
pB = Fr(32052445611625, 160855115169792); KAP = Fr(65536, 65541)
L = 65 * math.log(2)
seeds = {}
for line in open(seedsf):
    if line.strip() and not line.startswith('#'):
        nn, sd, mode = line.split(); seeds[nn] = (sd, mode)
R = {'fixed': [], 'rand': []}
for nn, (sd, mode) in sorted(seeds.items()):
    f = os.path.join(rundir, nn + '.json')
    if os.path.exists(f):
        r = json.load(open(f)); assert r['mode'] == mode and str(r['seed']) == sd, f; R[mode].append(r)
F = R['fixed']
n = sum(r['units'] for r in F); t = sum(r['trials'] for r in F)
SB = sum(r['SB'] for r in F); C1 = sum(r['C1'] for r in F); C2 = sum(r['C2'] for r in F); SC = sum(r['SC'] for r in F)
def eb(S1, S2, n):
    m = S1 / n; v = (S2 - n * m * m) / (n - 1)
    return m, v, m + math.sqrt(2 * v * L / n) + 7 * L / (3 * (n - 1))
def chern(S, n, th):
    mu = n * th
    return (mu - S) ** 2 / (2 * mu) if S < mu else 0.0
pBf = float(pB); kf = float(KAP)
mB, vB, ebB = eb(SB, SB, n); mX, vX, ebX = eb(C1 / 7, C2 / 49, n)
nf = sum(1 for v in seeds.values() if v[1] == 'fixed')
complete = len(F) == nf and len(R['rand']) == len(seeds) - nf
out = {'runs_fixed': len(F), 'runs_rand': len(R['rand']), 'complete': complete, 'units': n, 'trials': t,
       'trials_log2': round(math.log2(t), 4),
       'stageB': {'SB': SB, 'mean_over_pB': round(mB / pBf, 6), 'se_over_pB': round(math.sqrt(vB / n) / pBf, 7),
                  'emp_bernstein_2^-64_over_pB': round(ebB / pBf, 6),
                  'per_run_over_pB': [round(r['SB'] / r['units'] / pBf, 5) for r in F]},
       'stageC': {'C1': C1, 'C2': C2, 'SC': SC, 'rate_over_2^-11': round(C1 / t * 2048, 6),
                  'unit_mean_over_KAP_2^-11': round(mX / kf * 2048, 6), 'se': round(math.sqrt(vX / n) / kf * 2048, 7),
                  'emp_bernstein_2^-64_over_2^-11': round(ebX / kf * 2048, 6),
                  'per_run_over_2^-11': [round(r['C1'] / r['trials'] * 2048, 4) for r in F]}}
EV = ('A', 'F', 'AF', 'T6', 'T6A', 'N12', 'T6N8', 'G', 'D16')
ext = {}
for mode in ('fixed', 'rand'):
    tt = sum(r['trials'] for r in R[mode]); ext[mode] = {'trials': tt, **{e: sum(r[e] for r in R[mode]) for e in EV}}
for e in EV:
    a, ta, b, tb = ext['fixed'][e], ext['fixed']['trials'], ext['rand'][e], ext['rand']['trials']
    if a and b and ta and tb:
        ratio = (a / ta) / (b / tb)
        ext[e + '_fixed_log2'] = round(math.log2(a / ta), 4); ext[e + '_rand_log2'] = round(math.log2(b / tb), 4)
        ext[e + '_ratio'] = [round(ratio, 4), round(ratio * math.sqrt(1 / a + 1 / b), 4)]
out['h1i_events'] = ext
thB = None
for k in range(5500, 10101):
    th = k / 10000
    if ebB <= th * pBf and chern(SB, n, th * pBf) >= 20: thB = Fr(k, 10000); break
thC = None
for k in range(1001, 1250):
    th = k / 1000
    if ebX <= th * kf / 2048 and chern(C1 / 7, n, th * kf / 2048) >= 20: thC = Fr(k, 1000); break
stop = (not complete) or thB is None
tC = thC if thC else Fr(5, 4)
out['decision'] = {'STOP': stop, 'stageB_premise': str(thB) if thB else None,
                   'stageB_budget': str(thB * Fr(6001, 6000)) if thB else None,
                   'stageB_chern_exp_at_premise': round(chern(SB, n, float(thB) * pBf), 2) if thB else None,
                   'stageC_premise': str(tC), 'stageC_from_sample': thC is not None, 'stageC_budget': str(tC * Fr(6001, 6000)),
                   'stageC_chern_exp_at_premise': round(chern(C1 / 7, n, float(tC) * kf / 2048), 2),
                   'program_line': 'PREMISE = (Fraction(%d, %d), Fraction(%d, %d))' % (
                       (thB or Fr(0)).numerator, (thB or Fr(1)).denominator, tC.numerator, tC.denominator)}
print(json.dumps(out, indent=1))
```

## Appendix B. 5ca02dfb's measuring programs (Subflatus3; Section 8.2)

These are Subflatus3's files of 5ca02dfb, reproduced unchanged (from
5ca02dfb's proof.md, its Appendix B) because theta_B and theta_C of this
package were set from their sample, and `eaq.c` of Appendix C contains
`sbs2k.c` verbatim; "this version", "the shipped program" and the paths in
their text are 5ca02dfb's. They are the preregistered files of the S2K14 sample (SHA-256: sbs2k.c
17f5d91c7163922f87655aaf95d2cd21703a1c3a1c8a9ece6e64c8e6e1f6a208, summarize.py 7af8060f5cf794bed384830a0eae0eef9bd3aa8030ad6bd320af0eb7d4fce220, make_seeds.py 23ee2cbe44d2c0350afbb3494e92070ebdff3ddd448cec3dc4eb5aacf93aa075, crosscheck_s2k.py 65def85352d34ccb12e5116cc54797c292948faea6b6c3b31a704fb2c68c414b; the binary
e745aa7f325ef1de6198b11ae99bcfc05623fb832e29c32f7938747b5f05182c, the seeds, the launcher run.sh and the plan are listed in PLAN.sha256,
SHA-256 186f9fc8...e213d16b). `sbs2k.c` is compiled with `gcc -O3
-march=native` and run as `./sbs2k 1073741824 SEED` (32 seeds). Its
per-trial code (members, outer, rowY, middle, trial) is shared verbatim
with `sbbatch.c` and `sbmeas.c` of Subflatus3's 1d5e54ce and 52bb50ee.
`summarize.py` and `crosscheck_s2k.py` import the counted program from the
candidate's `experiments/` directory (for p_B and for the forward
computation); the cross-check also reads `verifier/blake3.py`.

```c
/* sbs2k.c (Subflatus3): stage events of the order S2K14 on uniform batches of the run.  Shared code below is
   taken verbatim from sbbatch.c / sbmeas.c (52bb50ee, 1d5e54ce).  sbmeas.c -- independent measurement of the stage events of the 098e66f search
   (steps O, M, Y, T; sub-class S8; batches of seven consecutive members, the last
   batch holding members 65534 and 65535) on a uniform sample of the run.
   usage: sbmeas NOUTER NX2 SEED            -> one line per outer step + totals
          sbmeas --context c0..c6           -> per-member flags for one context (cross-check)
   Per outer step: vd uniform below V = 1512538, w5, C0.c1, D3.d1, S15, S9 uniform 32-bit
   words, then NX2 uniform values of X2; all from SplitMix64(SEED).
   Rule A is tested on h1 = ROR(Y14 ^ (Y3 + y), 16) of E3, read from a forward
   evaluation of C2; the filter on c1 of E1, read from forward C1 and E1.       */
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>
typedef uint32_t u32; typedef uint64_t u64;
static inline u32 ror(u32 x, int r) { return (x >> r) | (x << (32 - r)); }
static inline u32 rol(u32 x, int r) { return (x << r) | (x >> (32 - r)); }
static const u32 IV[8] = {0x6A09E667, 0xBB67AE85, 0x3C6EF372, 0xA54FF53A, 0x510E527F, 0x9B05688C, 0x1F83D9AB, 0x5BE0CD19};
#define X3 0x29d4fa98u
#define X7 0xbee3af28u
#define X11 0x44036000u
#define X15 0x40c58500u
#define W4 0x97475638u
#define W13 0x0007c006u
#define Y3 0x8127c181u
#define Y11 0x7af77f38u
#define VRANGE 1512538u
#define NMEM 65536
#define NB 9363
static u64 sm;
static u64 next64(void) { u64 z = (sm += 0x9E3779B97F4A7C15ull); z = (z ^ (z >> 30)) * 0xBF58476D1CE4E5B9ull; z = (z ^ (z >> 27)) * 0x94D049BB133111EBull; return z ^ (z >> 31); }
static u32 next32(void) { return (u32)(next64() >> 32); }
static u32 mem_y[NMEM];
static void members(void) {
  static const int ord[16] = {14, 30, 31, 4, 5, 6, 7, 10, 11, 12, 13, 20, 21, 27, 28, 29};
  for (int i = 0; i < NMEM; i++) { u32 e1 = 0x030c0303u | 0xcu;
    for (int t = 0; t < 16; t++) if ((i >> t) & 1) e1 |= 1u << ord[t];
    if ((e1 >> 21) & 1) e1 |= 1u << 26; mem_y[i] = e1 - Y3; }
}
typedef struct { u32 S2, S4, S6, S7, S9, S10, S11, S15, X4, X9, X13, X14, D2b1, D2c1, vb, vc, vd, w5, w6, w7; } Outer;
typedef struct { u32 w0, w2, w3, w12, S0, S1, S5, S12; } Mid;
static void outer(Outer *o, u32 vc, u32 vd, u32 D3d1, u32 S15, u32 S9, u32 w5) {
  u32 K = IV[2] + IV[6];
  u32 ka2 = K + W4, kd2 = ror(ka2 ^ 55, 16), kc2 = IV[2] + kd2, kb2 = ror(IV[6] ^ kc2, 12);
  u32 S2 = ka2 + kb2 + w5, S14 = ror(kd2 ^ S2, 8), S10 = kc2 + S14, S6 = ror(kb2 ^ S10, 7);
  u32 D3a1 = rol(D3d1, 16) ^ S14, D3c1 = S9 + D3d1, D3b1 = X3 - D3a1, S4 = rol(D3b1, 12) ^ D3c1;
  u32 S3 = D3a1 - S4, X14 = ror(D3d1 ^ X3, 8), X9 = D3c1 + X14, X4 = ror(D3b1 ^ X9, 7);
  u32 K3d1 = rol(S15, 8) ^ S3, K3c1 = IV[3] + K3d1, K3b1 = ror(IV[7] ^ K3c1, 12), S11 = K3c1 + S15;
  u32 S7 = ror(K3b1 ^ S11, 7), K3a1 = rol(K3d1, 16) ^ 11, w6 = K3a1 - IV[3] - IV[7], w7 = S3 - K3a1 - K3b1;
  u32 X8 = vc - vd, vb = ror(X4 ^ vc, 12), D2b1 = rol(X7, 7) ^ X8, D2c1 = rol(D2b1, 12) ^ S7, X13 = X8 - D2c1;
  Outer t = {S2, S4, S6, S7, S9, S10, S11, S15, X4, X9, X13, X14, D2b1, D2c1, vb, vc, vd, w5, w6, w7}; *o = t;
}
static void middle(const Outer *o, u32 X2, Mid *m) {
  u32 D2a1 = X2 - o->D2b1 - W13, D2d1 = rol(o->X13, 8) ^ X2, S13 = rol(D2d1, 16) ^ D2a1;
  u32 S8 = o->D2c1 - D2d1, w12 = D2a1 - o->S2 - o->S7;
  u32 K1c1 = o->S9 - S13, K1d1 = K1c1 - IV[1], K1a1 = rol(K1d1, 16), K1b1 = ror(IV[5] ^ K1c1, 12);
  u32 S1 = rol(S13, 8) ^ K1d1, S5 = ror(K1b1 ^ o->S9, 7), w2 = K1a1 - IV[1] - IV[5], w3 = S1 - K1a1 - K1b1;
  u32 K0b1 = rol(o->S4, 7) ^ S8, K0c1 = rol(K0b1, 12) ^ IV[4], K0d1 = K0c1 - IV[0], K0a1 = rol(K0d1, 16);
  u32 S12 = S8 - K0c1, S0 = rol(S12, 8) ^ K0d1, w0 = K0a1 - IV[0] - IV[4];
  Mid t = {w0, w2, w3, w12, S0, S1, S5, S12}; *m = t;
}

/* step Y for one member */
typedef struct { u32 va, X6, X1, gd, Y12; } Row;
static void rowY(const Outer *o, u32 y, Row *r) {
  u32 Y8 = rol(y, 7) ^ o->vb, Y12 = Y8 - o->vc, Y0 = rol(Y12, 8) ^ o->vd, va = Y0 - o->vb - o->w6, X12 = rol(o->vd, 16) ^ va;
  u32 gc = X11 - X12, gb = ror(o->S6 ^ gc, 12), X6 = ror(gb ^ X11, 7), gd = gc - o->S11, X1 = rol(X12, 8) ^ gd;
  r->va = va; r->X6 = X6; r->X1 = X1; r->gd = gd; r->Y12 = Y12;
}
static inline int ruleA(u32 h1) { return (h1 & 1) == 0 && ((h1 >> 16) & 3) == 0 && ((h1 >> 1) & 1) == 1 && (((h1 >> 2) ^ (h1 >> 3)) & 1); }
static inline int filt(u32 c1) { return (c1 & 0x00098188u) == 0x00008000u; }
/* bit0 = rule A on h1 of E3, bit1 = filter on c1 of E1 (only when rule A holds); forward G evaluations */
static inline int trial(const Outer *o, u32 X2, const Mid *m, const Row *r, u32 y) {
  u32 X0 = r->va - o->X4 - m->w2;
  u32 fd = rol(X15, 8) ^ X0, fc = o->S10 + fd, X10 = fc + X15;
  u32 X6 = r->X6;
  u32 a1 = X2 + X6 + o->w7, d1 = ror(o->X14 ^ a1, 16), c1 = X10 + d1, b1 = ror(X6 ^ c1, 12);
  u32 a2 = a1 + b1 + m->w0, Y14 = ror(d1 ^ a2, 8), Y10 = c1 + Y14, Y6 = ror(b1 ^ Y10, 7);
  u32 h1 = ror(Y14 ^ (Y3 + y), 16);
  if (!ruleA(h1)) return 0;
  u32 fb = ror(m->S5 ^ fc, 12), X5 = ror(fb ^ X10, 7);
  u32 ga = rol(r->gd, 16) ^ m->S12, w10 = ga - m->S1 - o->S6;
  u32 p1 = r->X1 + X5 + m->w3, q1 = ror(o->X13 ^ p1, 16), r1 = o->X9 + q1, s1 = ror(X5 ^ r1, 12), Y1 = p1 + s1 + w10;
  u32 e_a1 = Y1 + Y6 + m->w12, e_d1 = ror(r->Y12 ^ e_a1, 16), e_c1 = Y11 + e_d1;
  return 1 | (filt(e_c1) << 1);
}

#define KS 14
#define NRV (1u << (32 - KS))
#define NGROUP ((NRV + 6) / 7)          /* 37,450 */
/* batch (member index mi, group g, position i) of an outer step: bit0 = enters stage B, bits 8.. = number of counted
   lanes with rule A and the filter.  Lane l is C2.a1 = (7g + l) 2^KS + i; the last group counts lane 0 only. */
static int batch2k(const Outer *o, u32 mi, u32 g, u32 i) {
  Row r; u32 y = mem_y[mi]; rowY(o, y, &r); int eb = 0, c = 0;
  for (u32 l = 0; l < 7; l++) {
    u32 rr = 7 * g + l; if (rr >= NRV) break;
    u32 a1 = (rr << KS) + i, X2 = a1 - r.X6 - o->w7; Mid m; middle(o, X2, &m);
    int f = trial(o, X2, &m, &r, y); eb |= f & 1; c += f == 3;
  }
  return eb | (c << 8);
}
/* usage: sbs2k NUNITS SEED                 one unit = one batch drawn uniformly from the run (Lemma U)
          sbs2k --context c0 c1 c2 c3 c4 c5 MI G I0 NPOS   decisions of NPOS consecutive positions (cross-check)
   unit: vd uniform below V; w5, vc, S15, S9 uniform; D3.d1 = X3; member index uniform below 2^16; group uniform below
   37,450; position uniform below 2^14; SplitMix64(SEED); units independent. */
int main(int argc, char **argv) {
  members();
  if (argc == 12 && !strcmp(argv[1], "--context")) {
    u32 c[6]; for (int k = 0; k < 6; k++) c[k] = (u32)strtoul(argv[2 + k], 0, 0);
    u32 mi = strtoul(argv[8], 0, 0), g = strtoul(argv[9], 0, 0), i0 = strtoul(argv[10], 0, 0), np = strtoul(argv[11], 0, 0);
    Outer o; outer(&o, c[0], c[1], X3, c[3], c[4], c[5]);
    long nB = 0, nC = 0; u64 h = 1469598103934665603ull;
    for (u32 i = i0; i < i0 + np; i++) { int f = batch2k(&o, mi, g, i); nB += f & 1; nC += f >> 8; h = (h ^ (u64)(f & 1) ^ ((u64)(f >> 8) << 1)) * 1099511628211ull; }
    printf("stageB_batches %ld ruleA_filter_lanes %ld hash %016llx\n", nB, nC, (unsigned long long)h);
    return 0;
  }
  if (argc != 3) { fprintf(stderr, "usage\n"); return 2; }
  u64 n = strtoull(argv[1], 0, 10); sm = strtoull(argv[2], 0, 10);
  u64 kB = 0, kC = 0, kC2 = 0, kC1 = 0, cmax = 0, last = 0;
  for (u64 k = 0; k < n; k++) {
    u32 vd; do vd = next32() & 0x1fffff; while (vd >= VRANGE);
    u32 w5 = next32(), vc = next32(), S15 = next32(), S9 = next32(), mi = next32() & 0xffff;
    u32 g; do g = next32() & 0xffff; while (g >= NGROUP);
    u32 i = next32() & ((1u << KS) - 1);
    Outer o; outer(&o, vc, vd, X3, S15, S9, w5);
    int f = batch2k(&o, mi, g, i); u64 cc = (u64)(f >> 8); kB += f & 1; kC += cc; kC2 += cc * cc; kC1 += cc > 0; if (cc > cmax) cmax = cc; last += g == NGROUP - 1;
  }
  printf("units %llu stageB %llu ruleA_filter_lanes %llu ruleA_filter_sq %llu stageC %llu cmax %llu lastgroup %llu seed %s\n",
         (unsigned long long)n, (unsigned long long)kB, (unsigned long long)kC, (unsigned long long)kC2, (unsigned long long)kC1,
         (unsigned long long)cmax, (unsigned long long)last, argv[2]);
  return 0;
}
```

```python
# summarize.py
"""Analysis and decision rule of the S2K14 sample (fixed before the runs). Reads out_01..out_32.txt; STOP unless all 32
runs are present with 2^30 units and the seed of seeds.txt. delta = 2^-64 for both tests.
Stage B (b = 1 iff the batch enters stage B; mean = the run's stage-B batch share): theta_B = smallest k/1000,
300 <= k <= 600, with S_B < n theta_B p_B, Lemma C' bound exp(-(n m0 - S)^2 / (2 n m0)) <= 2^-64 at m0 = theta_B p_B,
and empirical Bernstein (Maurer-Pontil Thm 4) upper bound at 2^-64 <= theta_B p_B.
Stage C (x = c/7, c = counted lanes with rule A and the filter; mean = (262144/262150) * run's per-trial rate):
theta_C = smallest k/1000, 1000 <= k <= 1249, same two tests at m0 = theta_C 2^-11 (262144/262150).
STOP if no grid value passes. Budgets: 6001/6000 times the premises (program)."""
import sys, math, json
from fractions import Fraction
sys.path.insert(0, '/workspace/hashsmash-blake3-r2-challenge/lanes/exploratory/candidates/blake3-r2/experiments')
import s8stage as P
seeds = dict(l.split() for l in open('seeds.txt'))
S = {'units': 0, 'stageB': 0, 'ruleA_filter_lanes': 0, 'ruleA_filter_sq': 0, 'stageC': 0, 'lastgroup': 0}; cmax = 0; per = []
for nn in sorted(seeds):
    t = open('out_%s.txt' % nn).read().split()
    d = dict(zip(t[0::2], t[1::2]))
    if int(d['units']) != 1 << 30 or d['seed'] != seeds[nn]: sys.exit('STOP: run %s' % nn)
    for k in S: S[k] += int(d[k])
    cmax = max(cmax, int(d['cmax'])); per.append((nn, int(d['stageB']), int(d['ruleA_filter_lanes'])))
n = S['units']; assert n == 32 << 30
pB = P.stage_rates()[1]; LD = 64 * math.log(2); ld = math.log(2) + 64 * math.log(2)   # ln(2/delta)
def tests(sum1, sum2, m0):
    mean = sum1 / n; V = (sum2 - sum1 * sum1 / n) / (n - 1)
    eb = mean + math.sqrt(2 * V * ld / n) + 7 * ld / (3 * (n - 1))
    ex = (n * m0 - sum1) ** 2 / (2 * n * m0) if sum1 < n * m0 else 0.0
    return eb, ex
out = {'units': n, 'counts': S, 'cmax': cmax, 'p_B': float(pB)}
sB = S['stageB']; out['stageB_share_of_pB'] = sB / n / float(pB); out['stageB_se_of_pB'] = math.sqrt(sB / n * (1 - sB / n) / n) / float(pB)
thB = None
for k in range(300, 601):
    eb, ex = tests(sB, sB, float(Fraction(k, 1000) * pB))
    if eb <= float(Fraction(k, 1000) * pB) and ex >= LD: thB = Fraction(k, 1000); out['B'] = {'theta': str(thB), 'eb_of_pB': eb / float(pB), 'lemmaC_exponent': ex}; break
fC = Fraction(262144, 262150) / 2048; sC, sC2 = S['ruleA_filter_lanes'] / 7, S['ruleA_filter_sq'] / 49
out['ruleA_filter_rate_of_2^-11'] = sC / n / float(fC)
thC = None
for k in range(1000, 1250):
    eb, ex = tests(sC, sC2, float(Fraction(k, 1000) * fC))
    if eb <= float(Fraction(k, 1000) * fC) and ex >= LD: thC = Fraction(k, 1000); out['C'] = {'theta': str(thC), 'eb_of_2^-11': eb / float(fC), 'lemmaC_exponent': ex}; break
out['per_run_stageB_of_pB'] = [min(b for _, b, _ in per) / (1 << 30) / float(pB), max(b for _, b, _ in per) / (1 << 30) / float(pB)]
out['per_run_rate_of_2^-11'] = [min(c for _, _, c in per) / 7 / (1 << 30) / float(fC), max(c for _, _, c in per) / 7 / (1 << 30) / float(fC)]
out['decision'] = 'STOP' if thB is None or thC is None else 'PREMISE = (Fraction(%d, %d), Fraction(%d, %d))' % (thB.numerator, thB.denominator, thC.numerator, thC.denominator)
print(json.dumps(out, indent=1))
```

```python
# make_seeds.py
"""Seed rule of the S2K14 sample: seed NN (NN = 01..32) = first 16 hex digits of SHA-256('subflatus3 S2K14 sample NN'),
as a decimal integer. Checks that the 32 SplitMix64 streams (states seed + k * 0x9E3779B97F4A7C15, k <= 2^35 > the at
most ~2^33.3 draws of one run of 2^30 units) are pairwise disjoint, and disjoint from the streams of the seeds 1..9 used
in development runs."""
import hashlib
G = 0x9E3779B97F4A7C15; GI = pow(G, -1, 1 << 64); L = 1 << 35
seeds = [int(hashlib.sha256(b'subflatus3 S2K14 sample %02d' % k).hexdigest()[:16], 16) for k in range(1, 33)]
allst = seeds + list(range(1, 10))
for a in range(len(allst)):
    for b in range(len(allst)):
        if a != b:
            d = ((allst[b] - allst[a]) * GI) % (1 << 64)    # stream b starts d steps after stream a
            assert L <= d <= (1 << 64) - L, (a, b)
for k, s in enumerate(seeds, 1): print('%02d %d' % (k, s))
```

```python
# crosscheck_s2k.py
"""Cross-check sbs2k --context against the shipped program experiments/s8stage.py: for one context (six outer words with
D3.d1 = X3, member index MI, group G) and NPOS consecutive positions, the stage-B decision and the number of counted lanes
with rule A and the filter are read from s8stage.forward (forward 2-round compressions of message A) with
C2.a1 = (7G + l) 2^14 + i, X2 = C2.a1 - X6 - w7; every 50th lane's digest is compared with verifier/blake3.py."""
import sys, subprocess, random, struct
R = '/workspace/hashsmash-blake3-r2-challenge'
sys.path.insert(0, R); sys.path.insert(0, R + '/lanes/exploratory/candidates/blake3-r2/experiments')
from verifier.blake3 import blake3
import s8stage as P
seed, npos = int(sys.argv[1]), int(sys.argv[2]); rng = random.Random(seed)
cw = [rng.getrandbits(32) for _ in range(6)]; cw[1] %= 1512538; cw[2] = P.X3
mi = rng.randrange(1 << 16); g = P.NBATCH - 1 if seed % 3 == 0 else rng.randrange(P.NBATCH); i0 = rng.randrange(P.NPOS - npos)
o = P.outer(cw); y = P.member(mi); c = (P.member_vals(o, y)['X6'] + o['w7']) & P.M32
h = 1469598103934665603; nB = nC = ver = 0; n = 0
for i in range(i0, i0 + npos):
    eb = cc = 0
    for l in range(7):
        r = 7 * g + l
        if r >= P.NRV: break
        X2 = (((r << P.KS) + i) - c) & P.M32; f = P.forward(P.middle(o, X2), y); n += 1
        if n % 50 == 0: assert struct.unpack('<8I', blake3(f['A'], 2)) == f['dA']; ver += 1
        eb |= int(f['ruleA']); cc += int(f['ruleA'] and f['filt'])
    h = ((h ^ eb ^ (cc << 1)) * 1099511628211) % (1 << 64); nB += eb; nC += cc
out = subprocess.run(['/workspace/hashsmash-blake3-r2-staging/layout/s2k14_sample/sbs2k', '--context'] + [str(x) for x in cw] + [str(mi), str(g), str(i0), str(npos)],
                     capture_output=True, text=True).stdout.strip()
py = 'stageB_batches %d ruleA_filter_lanes %d hash %016x' % (nB, nC, h)
print('seed', seed, 'g', g, 'mi', mi, 'i0', i0, 'lanes', n, '| py', py, '| c', out, '| verifier', ver, 'EQUAL' if out == py else 'MISMATCH')
```

## Appendix C. The measuring programs of this version (Section 8.2)

(These are ef052659's files; they draw vd below 1,512,538, ef052659's V.
v106's sample program, which draws vd below 1,057,885, is in Appendix E.)
These are the preregistered files of this version's sample (SHA-256: eaq.c bef43dcd1d088a3027c35cd6f54ad686486407ef820f02a5fde9ab2b9aa36da0, summarize_ea.py ca82218138e45049c82d954703e20833a465d861fd3236157703dc25fbfb9740, make_seeds_ea.py 7851a272bc28e21db16ae50c46050396a97702830085d685621f75bffc6e1590, crosscheck_ea.py 486ad203173fcef079bc5b1b734f2cd37cd07ec264d80f08520b55f6db2b4518, run_ea.sh 7c8c2382e25108ecc66562e569a8ba0a0781653aa6ede7973b0e7de52ca25a79; the binary of eaq.c 10d770933c4eb1c04bbbd5348ce7811d12b84dcf49bffcacb58a2c78b5225e3d; the plan, the frozen counted program (equal to the shipped program, 92c95d72208ab367193b93a2c3c9a4c209815fe06233a04a039896deb6a5b4af), the seeds and the freeze script are listed in PREREG_v104_EA.txt, SHA-256 23a2e3a0076f717eb5ca3c6660b59b9d408c710b32276b74fd72bdd16caa1bea). `eaq.c` is compiled with `cc -O3 -march=native` and run as `./eaq 1073741824 SEED` (32 seeds, by `run_ea.sh`). After its own five-line header comment it continues with Subflatus3's `sbs2k.c` of Appendix B verbatim up to and including `trial()`. `summarize_ea.py` imports the counted program (for p_B) from the directory given as its argument, and `crosscheck_ea.py` imports it for the forward computation and reads `verifier/blake3.py`; `make_seeds_ea.py` writes SEEDS_EA.txt.

```c
/* eaq.c (blake3-r2 v104): the stage events of H1 (ii), including the early-exit event (rule A, the filter and W4 = 0),
   on uniform batches of the run in the order S2K14 (Lemma U).  Everything up to and including trial() below is
   Subflatus3's sbs2k.c (5ca02dfb, proof.md Appendix B; SHA-256 17f5d91c...6a208) verbatim, with its own header comment;
   new here: trial_w4(), batch_w4() and main().
   ---------------------------------------------------------------------------------------------------------------- */
/* sbs2k.c (Subflatus3): stage events of the order S2K14 on uniform batches of the run.  Shared code below is
   taken verbatim from sbbatch.c / sbmeas.c (52bb50ee, 1d5e54ce).  sbmeas.c -- independent measurement of the stage events of the 098e66f search
   (steps O, M, Y, T; sub-class S8; batches of seven consecutive members, the last
   batch holding members 65534 and 65535) on a uniform sample of the run.
   usage: sbmeas NOUTER NX2 SEED            -> one line per outer step + totals
          sbmeas --context c0..c6           -> per-member flags for one context (cross-check)
   Per outer step: vd uniform below V = 1512538, w5, C0.c1, D3.d1, S15, S9 uniform 32-bit
   words, then NX2 uniform values of X2; all from SplitMix64(SEED).
   Rule A is tested on h1 = ROR(Y14 ^ (Y3 + y), 16) of E3, read from a forward
   evaluation of C2; the filter on c1 of E1, read from forward C1 and E1.       */
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>
typedef uint32_t u32; typedef uint64_t u64;
static inline u32 ror(u32 x, int r) { return (x >> r) | (x << (32 - r)); }
static inline u32 rol(u32 x, int r) { return (x << r) | (x >> (32 - r)); }
static const u32 IV[8] = {0x6A09E667, 0xBB67AE85, 0x3C6EF372, 0xA54FF53A, 0x510E527F, 0x9B05688C, 0x1F83D9AB, 0x5BE0CD19};
#define X3 0x29d4fa98u
#define X7 0xbee3af28u
#define X11 0x44036000u
#define X15 0x40c58500u
#define W4 0x97475638u
#define W13 0x0007c006u
#define Y3 0x8127c181u
#define Y11 0x7af77f38u
#define VRANGE 1512538u
#define NMEM 65536
#define NB 9363
static u64 sm;
static u64 next64(void) { u64 z = (sm += 0x9E3779B97F4A7C15ull); z = (z ^ (z >> 30)) * 0xBF58476D1CE4E5B9ull; z = (z ^ (z >> 27)) * 0x94D049BB133111EBull; return z ^ (z >> 31); }
static u32 next32(void) { return (u32)(next64() >> 32); }
static u32 mem_y[NMEM];
static void members(void) {
  static const int ord[16] = {14, 30, 31, 4, 5, 6, 7, 10, 11, 12, 13, 20, 21, 27, 28, 29};
  for (int i = 0; i < NMEM; i++) { u32 e1 = 0x030c0303u | 0xcu;
    for (int t = 0; t < 16; t++) if ((i >> t) & 1) e1 |= 1u << ord[t];
    if ((e1 >> 21) & 1) e1 |= 1u << 26; mem_y[i] = e1 - Y3; }
}
typedef struct { u32 S2, S4, S6, S7, S9, S10, S11, S15, X4, X9, X13, X14, D2b1, D2c1, vb, vc, vd, w5, w6, w7; } Outer;
typedef struct { u32 w0, w2, w3, w12, S0, S1, S5, S12; } Mid;
static void outer(Outer *o, u32 vc, u32 vd, u32 D3d1, u32 S15, u32 S9, u32 w5) {
  u32 K = IV[2] + IV[6];
  u32 ka2 = K + W4, kd2 = ror(ka2 ^ 55, 16), kc2 = IV[2] + kd2, kb2 = ror(IV[6] ^ kc2, 12);
  u32 S2 = ka2 + kb2 + w5, S14 = ror(kd2 ^ S2, 8), S10 = kc2 + S14, S6 = ror(kb2 ^ S10, 7);
  u32 D3a1 = rol(D3d1, 16) ^ S14, D3c1 = S9 + D3d1, D3b1 = X3 - D3a1, S4 = rol(D3b1, 12) ^ D3c1;
  u32 S3 = D3a1 - S4, X14 = ror(D3d1 ^ X3, 8), X9 = D3c1 + X14, X4 = ror(D3b1 ^ X9, 7);
  u32 K3d1 = rol(S15, 8) ^ S3, K3c1 = IV[3] + K3d1, K3b1 = ror(IV[7] ^ K3c1, 12), S11 = K3c1 + S15;
  u32 S7 = ror(K3b1 ^ S11, 7), K3a1 = rol(K3d1, 16) ^ 11, w6 = K3a1 - IV[3] - IV[7], w7 = S3 - K3a1 - K3b1;
  u32 X8 = vc - vd, vb = ror(X4 ^ vc, 12), D2b1 = rol(X7, 7) ^ X8, D2c1 = rol(D2b1, 12) ^ S7, X13 = X8 - D2c1;
  Outer t = {S2, S4, S6, S7, S9, S10, S11, S15, X4, X9, X13, X14, D2b1, D2c1, vb, vc, vd, w5, w6, w7}; *o = t;
}
static void middle(const Outer *o, u32 X2, Mid *m) {
  u32 D2a1 = X2 - o->D2b1 - W13, D2d1 = rol(o->X13, 8) ^ X2, S13 = rol(D2d1, 16) ^ D2a1;
  u32 S8 = o->D2c1 - D2d1, w12 = D2a1 - o->S2 - o->S7;
  u32 K1c1 = o->S9 - S13, K1d1 = K1c1 - IV[1], K1a1 = rol(K1d1, 16), K1b1 = ror(IV[5] ^ K1c1, 12);
  u32 S1 = rol(S13, 8) ^ K1d1, S5 = ror(K1b1 ^ o->S9, 7), w2 = K1a1 - IV[1] - IV[5], w3 = S1 - K1a1 - K1b1;
  u32 K0b1 = rol(o->S4, 7) ^ S8, K0c1 = rol(K0b1, 12) ^ IV[4], K0d1 = K0c1 - IV[0], K0a1 = rol(K0d1, 16);
  u32 S12 = S8 - K0c1, S0 = rol(S12, 8) ^ K0d1, w0 = K0a1 - IV[0] - IV[4];
  Mid t = {w0, w2, w3, w12, S0, S1, S5, S12}; *m = t;
}

/* step Y for one member */
typedef struct { u32 va, X6, X1, gd, Y12; } Row;
static void rowY(const Outer *o, u32 y, Row *r) {
  u32 Y8 = rol(y, 7) ^ o->vb, Y12 = Y8 - o->vc, Y0 = rol(Y12, 8) ^ o->vd, va = Y0 - o->vb - o->w6, X12 = rol(o->vd, 16) ^ va;
  u32 gc = X11 - X12, gb = ror(o->S6 ^ gc, 12), X6 = ror(gb ^ X11, 7), gd = gc - o->S11, X1 = rol(X12, 8) ^ gd;
  r->va = va; r->X6 = X6; r->X1 = X1; r->gd = gd; r->Y12 = Y12;
}
static inline int ruleA(u32 h1) { return (h1 & 1) == 0 && ((h1 >> 16) & 3) == 0 && ((h1 >> 1) & 1) == 1 && (((h1 >> 2) ^ (h1 >> 3)) & 1); }
static inline int filt(u32 c1) { return (c1 & 0x00098188u) == 0x00008000u; }
/* bit0 = rule A on h1 of E3, bit1 = filter on c1 of E1 (only when rule A holds); forward G evaluations */
static inline int trial(const Outer *o, u32 X2, const Mid *m, const Row *r, u32 y) {
  u32 X0 = r->va - o->X4 - m->w2;
  u32 fd = rol(X15, 8) ^ X0, fc = o->S10 + fd, X10 = fc + X15;
  u32 X6 = r->X6;
  u32 a1 = X2 + X6 + o->w7, d1 = ror(o->X14 ^ a1, 16), c1 = X10 + d1, b1 = ror(X6 ^ c1, 12);
  u32 a2 = a1 + b1 + m->w0, Y14 = ror(d1 ^ a2, 8), Y10 = c1 + Y14, Y6 = ror(b1 ^ Y10, 7);
  u32 h1 = ror(Y14 ^ (Y3 + y), 16);
  if (!ruleA(h1)) return 0;
  u32 fb = ror(m->S5 ^ fc, 12), X5 = ror(fb ^ X10, 7);
  u32 ga = rol(r->gd, 16) ^ m->S12, w10 = ga - m->S1 - o->S6;
  u32 p1 = r->X1 + X5 + m->w3, q1 = ror(o->X13 ^ p1, 16), r1 = o->X9 + q1, s1 = ror(X5 ^ r1, 12), Y1 = p1 + s1 + w10;
  u32 e_a1 = Y1 + Y6 + m->w12, e_d1 = ror(r->Y12 ^ e_a1, 16), e_c1 = Y11 + e_d1;
  return 1 | (filt(e_c1) << 1);
}

/* trial() extended (new): bit0 = rule A, bit1 = filter (only with rule A), bit2 = W4 == 0 (only with both); *w4 = the
   test word W4 = P ^ ROR(P, 1) ^ ROR(g1 ^ g1', 12) of a lane with rule A and the filter (Lemma E of v104), with
   P = a2 ^ a2' of E1 (a2' = a1 + b1' + w5 + delta, b1' = ROR(Y6 ^ (Y11' + d1), 12)) and g1 = Y9 + h1, g1' = Y9 + (h1 ^ eta)
   of E3 (Y9 = C1's c output = r1 + ROR(q1 ^ Y1, 8)). */
#define Y3P 0x7edf3e7eu
#define Y11P 0x850000c3u
#define ETA 0x830303cfu
#define DELTA 0xfffffff8u
static inline int trial_w4(const Outer *o, u32 X2, const Mid *m, const Row *r, u32 y, u32 *w4) {
  u32 X0 = r->va - o->X4 - m->w2;
  u32 fd = rol(X15, 8) ^ X0, fc = o->S10 + fd, X10 = fc + X15;
  u32 X6 = r->X6;
  u32 a1 = X2 + X6 + o->w7, d1 = ror(o->X14 ^ a1, 16), c1 = X10 + d1, b1 = ror(X6 ^ c1, 12);
  u32 a2 = a1 + b1 + m->w0, Y14 = ror(d1 ^ a2, 8), Y10 = c1 + Y14, Y6 = ror(b1 ^ Y10, 7);
  u32 h1 = ror(Y14 ^ (Y3 + y), 16);
  if (!ruleA(h1)) return 0;
  u32 fb = ror(m->S5 ^ fc, 12), X5 = ror(fb ^ X10, 7);
  u32 ga = rol(r->gd, 16) ^ m->S12, w10 = ga - m->S1 - o->S6;
  u32 p1 = r->X1 + X5 + m->w3, q1 = ror(o->X13 ^ p1, 16), r1 = o->X9 + q1, s1 = ror(X5 ^ r1, 12), Y1 = p1 + s1 + w10;
  u32 e_a1 = Y1 + Y6 + m->w12, e_d1 = ror(r->Y12 ^ e_a1, 16), e_c1 = Y11 + e_d1;
  if (!filt(e_c1)) return 1;
  u32 Y9 = r1 + ror(q1 ^ Y1, 8), g1 = Y9 + h1, g1p = Y9 + (h1 ^ ETA);
  u32 e_b1 = ror(Y6 ^ e_c1, 12), e_b1p = ror(Y6 ^ (Y11P + e_d1), 12);
  u32 P = (e_a1 + e_b1 + o->w5) ^ (e_a1 + e_b1p + o->w5 + DELTA);
  *w4 = P ^ ror(P, 1) ^ ror(g1 ^ g1p, 12);
  return 3 | ((*w4 == 0) << 2);
}

#define KS 14
#define NRV (1u << (32 - KS))
#define NGROUP ((NRV + 6) / 7)          /* 37,450 */
typedef struct { int eb, c, w, z8, z16, z24; u64 h; } Bat;
/* batch (member mi, group g, position i): eb = enters stage B, c = counted lanes with rule A and the filter, w = those
   with W4 = 0, z8/z16/z24 = those with the low 8/16/24 bits of W4 zero, h = FNV hash of (eb, c, the W4 of each such
   lane in lane order).  Lane l is C2.a1 = (7g + l) 2^KS + i; the last group counts lane 0 only (as batch2k). */
static void batch_w4(const Outer *o, u32 mi, u32 g, u32 i, Bat *b) {
  Row r; u32 y = mem_y[mi]; rowY(o, y, &r); memset(b, 0, sizeof *b); b->h = 1469598103934665603ull;
  for (u32 l = 0; l < 7; l++) {
    u32 rr = 7 * g + l; if (rr >= NRV) break;
    u32 a1 = (rr << KS) + i, X2 = a1 - r.X6 - o->w7, w4 = 0; Mid m; middle(o, X2, &m);
    int f = trial_w4(o, X2, &m, &r, y, &w4); b->eb |= f & 1;
    if ((f & 3) == 3) { b->c++; b->w += f >> 2; b->z8 += !(w4 & 0xff); b->z16 += !(w4 & 0xffff); b->z24 += !(w4 & 0xffffff);
                        b->h = (b->h ^ w4) * 1099511628211ull; }
  }
  b->h = (b->h ^ (u64)b->eb ^ ((u64)b->c << 1)) * 1099511628211ull;
}
/* usage: eaq NUNITS SEED          one unit = one batch drawn uniformly from the run (Lemma U), exactly sbs2k's draws
          eaq --context c0 c1 c2 c3 c4 c5 MI G I0 NPOS   per-batch values of NPOS consecutive positions (cross-check)
   unit: vd uniform below V (rejection from 21-bit draws), then w5, vc, S15, S9, member index below 2^16, group below
   37,450 (rejection from 16-bit draws), position below 2^14; SplitMix64 from SEED; D3.d1 = X3; units independent.
   Output (one line): units, stage-B batches, sum c, sum c^2, sum w, sum w^2, batches with w > 0, sums of z8, z16,
   z24, stage-C batches (c > 0), largest c, largest w, last-group units, seed. */
int main(int argc, char **argv) {
  members();
  if (argc == 12 && !strcmp(argv[1], "--context")) {
    u32 c[6]; for (int k = 0; k < 6; k++) c[k] = (u32)strtoul(argv[2 + k], 0, 0);
    u32 mi = strtoul(argv[8], 0, 0), g = strtoul(argv[9], 0, 0), i0 = strtoul(argv[10], 0, 0), np = strtoul(argv[11], 0, 0);
    Outer o; outer(&o, c[0], c[1], X3, c[3], c[4], c[5]);
    long nB = 0, nC = 0, nW = 0; u64 h = 1469598103934665603ull; Bat b;
    for (u32 i = i0; i < i0 + np; i++) { batch_w4(&o, mi, g, i, &b); nB += b.eb; nC += b.c; nW += b.w; h = (h ^ b.h) * 1099511628211ull; }
    printf("stageB_batches %ld ruleA_filter_lanes %ld w4zero_lanes %ld hash %016llx\n", nB, nC, nW, (unsigned long long)h);
    return 0;
  }
  if (argc != 3) { fprintf(stderr, "usage\n"); return 2; }
  u64 n = strtoull(argv[1], 0, 10); sm = strtoull(argv[2], 0, 10);
  u64 kB = 0, kC = 0, kC2 = 0, kW = 0, kW2 = 0, kW1 = 0, z8 = 0, z16 = 0, z24 = 0, kC1 = 0, cmax = 0, wmax = 0, last = 0; Bat b;
  for (u64 k = 0; k < n; k++) {
    u32 vd; do vd = next32() & 0x1fffff; while (vd >= VRANGE);
    u32 w5 = next32(), vc = next32(), S15 = next32(), S9 = next32(), mi = next32() & 0xffff;
    u32 g; do g = next32() & 0xffff; while (g >= NGROUP);
    u32 i = next32() & ((1u << KS) - 1);
    Outer o; outer(&o, vc, vd, X3, S15, S9, w5);
    batch_w4(&o, mi, g, i, &b);
    kB += b.eb; kC += b.c; kC2 += (u64)b.c * b.c; kW += b.w; kW2 += (u64)b.w * b.w; kW1 += b.w > 0; kC1 += b.c > 0;
    z8 += b.z8; z16 += b.z16; z24 += b.z24; if ((u64)b.c > cmax) cmax = b.c; if ((u64)b.w > wmax) wmax = b.w; last += g == NGROUP - 1;
  }
  printf("units %llu stageB %llu ruleA_filter_lanes %llu ruleA_filter_sq %llu w4zero_lanes %llu w4zero_sq %llu w4zero_batches %llu "
         "w4low8 %llu w4low16 %llu w4low24 %llu stageC %llu cmax %llu wmax %llu lastgroup %llu seed %s\n",
         (unsigned long long)n, (unsigned long long)kB, (unsigned long long)kC, (unsigned long long)kC2, (unsigned long long)kW,
         (unsigned long long)kW2, (unsigned long long)kW1, (unsigned long long)z8, (unsigned long long)z16, (unsigned long long)z24,
         (unsigned long long)kC1, (unsigned long long)cmax, (unsigned long long)wmax, (unsigned long long)last, argv[2]);
  return 0;
}
```

```python
"""summarize_ea.py (v104): analysis and decision rule of the early-exit sample, fixed before the runs.
Reads runs/NN.txt (one output line of `eaq 1073741824 SEED` each) for the 32 lines of SEEDS_EA.txt; STOP unless all 32 runs
are present with 2^30 units and their seeds.  Unit k = one uniform batch of the run in the order S2K14 (Lemma U):
b = 1{enters stage B}, x = c/7 (c = counted lanes with rule A and the filter), r = w/7 (w = those with W4 = 0); units are
i.i.d. in [0, 1]; E b = the run's stage-B share, E x = KAP * (per-trial rate of rule A and filter), E r = KAP * (per-trial
rate of rule A, filter and W4 = 0), KAP = 262,144 / 262,150.  delta = 2^-64 for every test:
  empirical Bernstein (Maurer and Pontil 2009, Thm 4): E <= mean + sqrt(2 V ln(2/delta) / n) + 7 ln(2/delta) / (3 (n - 1));
  Lemma C' (lower-tail Chernoff): P(sum <= S) <= exp(-(n m0 - S)^2 / (2 n m0)) for S < n m0; passes if the exponent >= 64 ln 2.
A value m0 passes when S < n m0, the Lemma C' exponent at m0 is >= 64 ln 2 and the empirical Bernstein bound is <= m0.
Decision: PROCEED iff (R) m0 = 2^-24 KAP passes for r (the premise rho_R = 2^-24 of the program, fixed before this
sample), and the premises inherited from 5ca02dfb pass as a reproduction: (B) m0 = 0.377 p_B for b, (C) m0 = 1.003 * 2^-11
KAP for x.  Otherwise STOP (no package from this design).  Also reported, not part of the decision: estimates, standard
errors, bounds, the smallest passing values on grids (B, C: k/1000; R: 2^-k), per-run ranges, W4 low-bit-zero counts.
usage: python3 summarize_ea.py PROGDIR"""
import sys, math, json, os
from fractions import Fraction
sys.path.insert(0, sys.argv[1]); import s8stage as P
seeds = {l.split()[0]: l.split()[1] for l in open('SEEDS_EA.txt') if l.strip() and not l.startswith('#')}
K = ('units', 'stageB', 'ruleA_filter_lanes', 'ruleA_filter_sq', 'w4zero_lanes', 'w4zero_sq', 'w4zero_batches', 'w4low8', 'w4low16',
     'w4low24', 'stageC', 'lastgroup'); S = dict.fromkeys(K, 0); per = []; cmax = wmax = 0
for nn in sorted(seeds):
    f = 'runs/%s.txt' % nn
    if not os.path.exists(f): sys.exit('STOP: run %s missing' % nn)
    t = open(f).read().split(); d = dict(zip(t[0::2], t[1::2]))
    if int(d['units']) != 1 << 30 or d['seed'] != seeds[nn]: sys.exit('STOP: run %s' % nn)
    for k in K: S[k] += int(d[k])
    cmax = max(cmax, int(d['cmax'])); wmax = max(wmax, int(d['wmax'])); per.append((nn, int(d['stageB']), int(d['ruleA_filter_lanes'])))
n = S['units']; assert n == 32 << 30 and len(per) == 32
trials = 7 * n - 6 * S['lastgroup']
pB = P.stage_rates()[1]; KAP = Fraction(262144, 262150); LD = 64 * math.log(2); ld = 65 * math.log(2)
def tests(s1, s2, m0):
    mean = s1 / n; V = (s2 - s1 * s1 / n) / (n - 1)
    eb = mean + math.sqrt(2 * V * ld / n) + 7 * ld / (3 * (n - 1))
    ex = (n * m0 - s1) ** 2 / (2 * n * m0) if s1 < n * m0 else 0.0
    return eb, ex, eb <= m0 and ex >= LD
xs = {'B': (S['stageB'], S['stageB']), 'C': (S['ruleA_filter_lanes'] / 7, S['ruleA_filter_sq'] / 49),
      'R': (S['w4zero_lanes'] / 7, S['w4zero_sq'] / 49)}
unit = {'B': float(pB), 'C': float(KAP) / 2048, 'R': float(KAP)}
prem = {'B': 0.377, 'C': 1.003, 'R': 2.0 ** -24}
out = {'units': n, 'trials': trials, 'trials_log2': round(math.log2(trials), 4), 'counts': S, 'cmax': cmax, 'wmax': wmax}
dec = True
for e in 'BCR':
    s1, s2 = xs[e]; m0 = prem[e] * unit[e]; eb, ex, ok = tests(s1, s2, m0); dec = dec and ok
    se = math.sqrt(max((s2 - s1 * s1 / n) / (n - 1), 0) / n)
    grid = None
    for k in (range(300, 1250) if e != 'R' else range(40, 0, -1)):
        v = k / 1000 if e != 'R' else 2.0 ** -k
        if tests(s1, s2, v * unit[e])[2]: grid = k; break
    out[e] = {'premise_tested': prem[e], 'mean_over_unit': s1 / n / unit[e], 'se_over_unit': se / unit[e],
              'emp_bernstein_over_unit': eb / unit[e], 'lemmaC_exponent_at_premise': ex, 'passes': ok,
              'smallest_passing_grid_value (info)': (grid / 1000 if e != 'R' else '2^-%d' % grid) if grid else None}
out['R']['rate_per_trial'] = S['w4zero_lanes'] / trials; out['R']['rate_per_AF_lane'] = S['w4zero_lanes'] / max(S['ruleA_filter_lanes'], 1)
out['R']['rate_per_trial_log2'] = math.log2(S['w4zero_lanes'] / trials) if S['w4zero_lanes'] else None
out['W4_low_bits_zero_per_AF_lane_log2'] = {b: math.log2(S['w4low%d' % b] / S['ruleA_filter_lanes']) for b in (8, 16, 24) if S['w4low%d' % b]}
out['per_run_stageB_over_pB'] = [min(b for _, b, _ in per) / (1 << 30) / float(pB), max(b for _, b, _ in per) / (1 << 30) / float(pB)]
out['per_run_AF_over_2^-11'] = [min(c for _, _, c in per) / 7 / (1 << 30) / unit['C'], max(c for _, _, c in per) / 7 / (1 << 30) / unit['C']]
out['decision'] = 'PROCEED (rho_R = 2^-24; premises 0.377 and 1.003 reproduced)' if dec else 'STOP'
print(json.dumps(out, indent=1))
```

```python
"""make_seeds_ea.py (v104): seeds of the preregistered early-exit sample, drawn only after the preregistration is frozen.
Run NN (NN = 01..32): SEED = first 16 hex digits of SHA-256('blake3-r2-v104 EA sample NN') as a decimal integer; eaq starts
SplitMix64 at state SEED.  Checks that the 32 streams (2^35 states each, more than one run's draws: 2^30 units of about
9.1 draws) are pairwise disjoint and each disjoint from: Subflatus3's 32 S2K14 sample streams and development seeds 1..9
(5ca02dfb, state = seed, 2^35 each); our eaq development runs (seeds 5, 6, state = seed); the study's scan.c and
w4rate.c runs (state = seed * 0x1234567 + 77; seeds 1-5, 7, 11-18, 21, 22, 24, 28, 31-38), 2^32 states each.
usage: python3 make_seeds_ea.py > SEEDS_EA.txt"""
import hashlib
M = 1 << 64; G = 0x9E3779B97F4A7C15; GI = pow(G, -1, M)
def h(label): return int(hashlib.sha256(label.encode()).hexdigest()[:16], 16)
def pos(state): return state * GI % M          # index of a start state in the SplitMix64 Weyl sequence
runs = [('%02d' % k, h('blake3-r2-v104 EA sample %02d' % k)) for k in range(1, 33)]
streams = [(pos(s), 1 << 35, 'v104 ' + n) for n, s in runs]
streams += [(pos(h('subflatus3 S2K14 sample %02d' % k)), 1 << 35, '5ca02dfb %02d' % k) for k in range(1, 33)]
streams += [(pos(s), 1 << 35, '5ca02dfb dev %d' % s) for s in range(1, 10)]
streams += [(pos(s), 1 << 32, 'eaq dev %d' % s) for s in (5, 6)]
streams += [(pos((s * 0x1234567 + 77) % M), 1 << 32, 'study %d' % s) for s in
            sorted(set([1, 2, 3, 4, 5, 7] + list(range(11, 19)) + [21, 22, 24, 28] + list(range(31, 39))))]
bad = 0
for i in range(len(streams)):
    for j in range(i + 1, len(streams)):
        (pi, li, ni), (pj, lj, nj) = streams[i], streams[j]
        if not (ni.startswith('v104') or nj.startswith('v104')): continue    # earlier streams among themselves: not checked
        d = (pj - pi) % M
        if not (d >= li and M - d >= lj): bad += 1; print('# OVERLAP', ni, nj)
assert bad == 0
print("# v104 EA sample seeds: SHA-256('blake3-r2-v104 EA sample NN')[:16] as decimal; 32 runs of eaq 1073741824 SEED;")
print("# SplitMix64 streams checked pairwise disjoint and disjoint from all earlier streams listed in make_seeds_ea.py")
for n, s in runs: print(n, s)
```

```python
"""crosscheck_ea.py (v104): eaq --context against the counted program experiments/s8stage.py.  For one context (six outer
words with D3.d1 = X3, member index MI, group G) and NPOS consecutive positions: per batch the stage-B decision, the
counted lanes with rule A and the filter, those with W4 = 0, and the FNV hash over (eb, c, the W4 of each such lane),
where W4 is read from s8stage.forward as residual_words(f)['R4'] = ROL(D4, 7) ^ D1 of the two real digests (Lemma D');
every 50th lane's digests are compared with verifier/blake3.py.  usage: crosscheck_ea.py SEED NPOS PROGDIR ROOT EAQ"""
import sys, subprocess, random, struct
seed, npos, progdir, root, eaq = int(sys.argv[1]), int(sys.argv[2]), sys.argv[3], sys.argv[4], sys.argv[5]
sys.path.insert(0, root); sys.path.insert(0, progdir)
from verifier.blake3 import blake3
import s8stage as P
rng = random.Random(seed); F = 1099511628211; MASK = (1 << 64) - 1
cw = [rng.getrandbits(32) for _ in range(6)]; cw[1] %= 1512538; cw[2] = P.X3
mi = rng.randrange(1 << 16); g = P.NBATCH - 1 if seed % 3 == 0 else rng.randrange(P.NBATCH); i0 = rng.randrange(P.NPOS - npos)
o = P.outer(cw); y = P.member(mi); c = (P.member_vals(o, y)['X6'] + o['w7']) & P.M32
h = 1469598103934665603; nB = nC = nW = ver = n = 0
for i in range(i0, i0 + npos):
    eb = cc = ww = 0; hb = 1469598103934665603
    for l in range(7):
        r = 7 * g + l
        if r >= P.NRV: break
        X2 = (((r << P.KS) + i) - c) & P.M32; f = P.forward(P.middle(o, X2), y); n += 1
        if n % 50 == 0:
            assert struct.unpack('<8I', blake3(f['A'], 2)) == f['dA'] and struct.unpack('<8I', blake3(f['B'], 2)) == f['dB']; ver += 1
        eb |= int(f['ruleA'])
        if f['ruleA'] and f['filt']:
            w4 = P.residual_words(f)['R4']; cc += 1; ww += w4 == 0; hb = ((hb ^ w4) * F) & MASK
    hb = ((hb ^ eb ^ (cc << 1)) * F) & MASK; h = ((h ^ hb) * F) & MASK; nB += eb; nC += cc; nW += ww
out = subprocess.run([eaq, '--context'] + [str(x) for x in cw] + [str(mi), str(g), str(i0), str(npos)], capture_output=True, text=True).stdout.strip()
py = 'stageB_batches %d ruleA_filter_lanes %d w4zero_lanes %d hash %016x' % (nB, nC, nW, h)
print('seed', seed, 'g', g, 'mi', mi, 'i0', i0, 'lanes', n, '| py', py, '| c', out, '| verifier', ver, 'EQUAL' if out == py else 'MISMATCH')
```

```bash
#!/bin/bash
# v104 EA sample: one run `eaq 1073741824 SEED` per line of SEEDS_EA.txt (32 runs).  Refuses unless the preregistration is
# frozen (PREREG_v104_EA.sha256 and FROZEN_EA.sha256 check) and SEEDS_EA.txt equals the output of the frozen
# make_seeds_ea.py.  Stability: nice -n 10; a run starts only while the 1-minute load average is at most 12 and fewer than
# MAXP (<= 10) of our runs are running.  Resumable: a run with a complete output file is never started again.  Every start
# and end is logged with UTC time in runs/LOG.txt.  usage (from sample/): ./run_ea.sh [MAXP]
set -u
cd "$(dirname "$0")" || exit 1
U=1073741824; MAXP=${1:-8}; [ "$MAXP" -gt 10 ] && MAXP=10
shasum -a 256 -c PREREG_v104_EA.sha256 >/dev/null 2>&1 || { echo "PREREG not frozen or changed"; exit 1; }
shasum -a 256 -c FROZEN_EA.sha256 >/dev/null 2>&1 || { echo "frozen files changed"; exit 1; }
python3 make_seeds_ea.py | cmp -s - SEEDS_EA.txt || { echo "SEEDS_EA.txt differs from the frozen rule"; exit 1; }
mkdir -p runs
load1() { sysctl -n vm.loadavg | awk '{print $2}'; }
while read -r NN SEED; do
  out="runs/${NN}.txt"
  if [ -s "$out" ] && grep -q '^units ' "$out"; then continue; fi
  while :; do
    nrun=$(jobs -rp | wc -l | tr -d ' ')
    if awk -v l="$(load1)" 'BEGIN{exit !(l <= 12)}' && [ "$nrun" -lt "$MAXP" ]; then break; fi
    sleep 15
  done
  echo "$(date -u +%FT%TZ) start $NN $SEED load $(load1)" >> runs/LOG.txt
  ( nice -n 10 ./eaq "$U" "$SEED" > "$out.part" 2> "runs/${NN}.err" && mv "$out.part" "$out"
    echo "$(date -u +%FT%TZ) end $NN exit $?" >> runs/LOG.txt ) &
  sleep 2
done < <(grep -v '^#' SEEDS_EA.txt)
wait
echo "$(date -u +%FT%TZ) all started runs finished" >> runs/LOG.txt
```

## Appendix D. count_s8.py: the exact model count (Section 8.1)

`count_s8.py` (SHA-256 0632efa59ac3bd71b5edc1b355b3af3e0dba8dcf36c761bc437e0b9a46bf4295) is the `--count` mode of 5ca02dfb's and c19feef's shipped program (its functions popc, subs, pext, solve_sub, aut1, N1, aut3, N3, model_count and the OUTCOMES table, unchanged except that, for v106, the two printed fields claimed_F and margin_over_F read F_H1 from the shipped program instead of ef052659's literal 92,675,072; ef052659's file had SHA-256 f3dcea2e563cac124b634b5de3e619763c089964f1179caa20e28e9ba40b85f8), moved out of the shipped program because the runner admits at most 64 KiB of experiment source; it takes its constants (the member list, rule A, Y11, DY11, delta, eta, DY3 and stage_rates) from the shipped `experiments/s8stage.py`. Save the block below as `count_s8.py` in the candidate directory (next to `experiments/`) and run `python3 count_s8.py` (about 2 minutes; `python3 count_s8.py all` also counts without rule A). Its run for this package printed the 85 outcomes, 57 nonzero, the six parts and r_ruleA = 185,350,144 = 1.4 F (claimed_F 132392960, margin_over_F 1.4), exit status 0 (Section 8.1).

```python
#!/usr/bin/env python3
"""count_s8.py -- the exact model count of proof.md Section 8.1 (H1 (i)): the --count mode of 5ca02dfb's and c19feef's
shipped program, moved here verbatim (the runner's 64 KiB source limit); constants from experiments/s8stage.py
(v106: claimed_F and margin_over_F read F_H1 from it).
usage (from the candidate directory): python3 count_s8.py [all]"""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), 'experiments'))
from s8stage import *

# == exact model count of proof.md Section 8 (participant mode --count) ==
# A Python port of the participant's C counter (carry automata, exact integers, no sampling).
# The listed outcomes (tau per beta of T6, with its eps) are the 85 outcomes of the six betas;
# parts are non-negative, so the sum over any listed subset is a lower bound on r.
OUTCOMES = {
    0x18b0e098: (0x6e21be55, '175020a0 175060a0 185020a0 185060a0 275020a0 275060a0 285020a0 285060a0 385020a0 385060a0 '
                             '675020a0 675060a0 685020a0 685060a0'),
    0x18b1a098: (0x6e203e55, '185060a0 189060a0 18d060a0 195060a0 285060a0 289060a0 28d060a0 295060a0 385060a0 389060a0 '
                             '38d060a0 395060a0 685060a0 689060a0 68d060a0 695060a0'),
    0x18d0e098: (0x6e61be55, '175020a0 175060a0 17d020a0 185020a0 185060a0 275020a0 275060a0 27d020a0 285020a0 285060a0 '
                             '2850a0a0 385020a0 385060a0 675020a0 675060a0 67d020a0 685020a0 685060a0 6850a0a0'),
    0x18d1a098: (0x6e603e55, '185060a0 18d060a0 195060a0 285060a0 2850a0a0 28d060a0 28d0a0a0 295060a0 2950a0a0 385060a0 '
                             '38d060a0 395060a0 685060a0 6850a0a0 68d060a0 68d0a0a0 695060a0 6950a0a0'),
    0x18b3e098: (0x6e23be55, '185020a0 185060a0 195020a0 195060a0 285020a0 285060a0 295020a0 295060a0'),
    0x18d3e098: (0x6e63be55, '185020a0 185060a0 195020a0 195060a0 285020a0 285060a0 2850a0a0 295020a0 295060a0 2950a0a0'),
}

def popc(x): return bin(x).count('1')

def subs(m):
    """submasks of m in increasing order (the k-th one has pext index k)"""
    s = 0
    while True:
        yield s
        if s == m: return
        s = (s - m) & m

def pext(x, m):
    r = k = 0
    while m:
        lo = m & -m
        if x & lo: r |= 1 << k
        k += 1; m ^= lo
    return r

def solve_sub(Mk, D):
    """subsets S of Mk with sum_{i in Mk} (1 - 2[i in S]) 2^i == D mod 2^32"""
    t = (Mk - D) & M32
    if t & 1: return []
    return [s for s in (t >> 1, (t >> 1) | 1 << 31) if not s & ~Mk]

def aut1(Bc, nu, eps, fm1, fv1, fm2, fv2):
    """#(d1, d2): c1 = d1 + Y11, c1 + DY11 == c1 ^ Bc, (c1 + d2) ^ ((c1 ^ Bc) + (d2 ^ nu)) == eps,
    d1 = fv1 on fm1, d2 = fv2 on fm2 (16-state carry automaton over the 32 bit positions)"""
    st = {0: 1}
    for i in range(32):
        y, dy, bb, nb, e = (Y11 >> i) & 1, (DY11 >> i) & 1, (Bc >> i) & 1, (nu >> i) & 1, (eps >> i) & 1
        d1s = ((fv1 >> i) & 1,) if (fm1 >> i) & 1 else (0, 1)
        d2s = ((fv2 >> i) & 1,) if (fm2 >> i) & 1 else (0, 1)
        ns = {}
        for s, n in st.items():
            for d1 in d1s:
                t = d1 + y + (s & 1); c1 = t & 1; t2 = c1 + dy + ((s >> 1) & 1)
                if (t2 & 1) != c1 ^ bb: continue
                for d2 in d2s:
                    u = c1 + d2 + ((s >> 2) & 1); v = (c1 ^ bb) + (d2 ^ nb) + (s >> 3)
                    if (u ^ v) & 1 != e: continue
                    k = (t >> 1) | (t2 >> 1) << 1 | (u >> 1) << 2 | (v >> 1) << 3
                    ns[k] = ns.get(k, 0) + n
        st = ns
    return sum(st.values())

def N1(beta, tau, eps):
    """#(d1, b1, a2) in 2^96 (E1, message A) giving beta, tau = a2 ^ a2' and eps = c2 ^ c2'"""
    Bc, nu, tot = rol(beta, 12), ror(tau, 8), 0
    for pa in subs(tau):                                               # bits of a2 on tau
        w = len(solve_sub(beta, (tau - 2 * pa - DELTA) & M32))         # patterns of b1 on beta
        if w:
            for px in subs(tau):                                       # bits of d1 ^ a2 on tau
                tot += w * aut1(Bc, nu, eps, tau, pa ^ px, nu, ror(px, 8))
    return tot << (32 - popc(beta))

def aut3(Pm, Q, tau, pg, Irot, hv):
    """#(g1, h2): g1 = pg on Pm, h2 = hv on Irot, (g1 + h2) ^ ((g1 ^ Pm) + (h2 ^ Q)) == tau"""
    st = [1, 0, 0, 0]
    for i in range(32):
        p, q, t = (Pm >> i) & 1, (Q >> i) & 1, (tau >> i) & 1
        gs = ((pg >> i) & 1,) if p else (0, 1)
        hs = ((hv >> i) & 1,) if (Irot >> i) & 1 else (0, 1)
        ns = [0, 0, 0, 0]
        for s in range(4):
            if st[s]:
                for g in gs:
                    for h in hs:
                        u = g + h + (s & 1); v = (g ^ p) + (h ^ q) + (s >> 1)
                        if (u ^ v) & 1 == t: ns[(u >> 1) | (v >> 1) << 1] += st[s]
        st = ns
    return sum(st)

def N3(tau, eps, members, full):
    """(#rule A, #all or None) of (Y4 in members, h1, g1, e2) in E3 giving eta, psi = tau ^ ROR(tau,1), eps, tau"""
    psi = tau ^ ror(tau, 1); Pm = rol(psi, 12); Q = ror(ETA ^ eps, 8); I = ETA & eps; Irot = ror(I, 8)
    sh = 32 - popc(ETA | eps)
    me = [[pext(p & I, I) for p in solve_sub(eps, (DY3 + psi - 2 * ror(q, 12)) & M32)] for q in subs(Pm)]
    cnt = {}
    for y in members:
        k = pext(y, Pm); cnt[k] = cnt.get(k, 0) + 1
    NI = 1 << popc(I); groups = {}                                     # g1 pattern -> #h1 patterns per (I bits, rule A)
    for ph in subs(ETA):
        for sg in solve_sub(Pm, (ETA - 2 * ph) & M32):
            g = groups.setdefault(sg, [[0, 0] for _ in range(NI)]); g[pext(ph & I, I)][ruleA_h1(ph)] += 1
    tr = ta = 0
    for pg, phs in groups.items():
        if not full and not any(c[1] for c in phs): continue
        pgi = pext(pg, Pm)
        Fin = [aut3(Pm, Q, tau, pg, Irot, ror(m, 8)) << sh for m in subs(I)]
        Hm = [0] * NI
        for x, c in cnt.items():
            for b in me[x ^ pgi]: Hm[b] += c
        for a in range(NI):
            if phs[a][0] or phs[a][1]:
                s = sum(Hm[b] * Fin[a ^ b] for b in range(NI) if Hm[b])
                ta += s * (phs[a][0] + phs[a][1]); tr += s * phs[a][1]
    return tr, ta if full else None

def model_count(full):
    """r for S8 and the six betas of T6: sum of N1 * N3 / 2^80 (2^16 members, 2^64 for h1, g1, e2 of E3)"""
    S8 = [member(i) for i in range(NMEM)]
    tot_r = tot_a = nz = 0; parts = {}
    for beta, (eps, taus) in OUTCOMES.items():
        pr = pa = 0
        for t in taus.split():
            tau = int(t, 16); n1 = N1(beta, tau, eps); n3r, n3a = N3(tau, eps, S8, full) if n1 else (0, 0 if full else None)
            nz += n1 * n3r > 0; pr += n1 * n3r; pa += n1 * (n3a or 0)
            row = {'beta': '%08x' % beta, 'tau': t, 'eps': '%08x' % eps, 'N1': n1, 'N3_ruleA': n3r}
            if full: row['N3_all'] = n3a
            print(json.dumps(row), flush=True)
        parts['%08x' % beta] = (pr >> 80, pa >> 80, pr % (1 << 80) == 0 and pa % (1 << 80) == 0)
        tot_r += pr; tot_a += pa
    res = {'outcomes': sum(len(v[1].split()) for v in OUTCOMES.values()), 'nonzero_ruleA': nz,
           'part_ruleA': {k: v[0] for k, v in parts.items()}, 'part_all': {k: v[1] for k, v in parts.items()},
           'integral': all(v[2] for v in parts.values()), 'r_ruleA': tot_r / 2 ** 80, 'r_all': tot_a / 2 ** 80,
           'claimed_F': F_H1, 'margin_over_F': tot_r / 2 ** 80 / F_H1}
    if not full: del res['part_all'], res['r_all']
    sr = stage_rates()[0]; res['stage_rates'] = sr
    print(json.dumps(res))
    return 0 if tot_r == 185350144 << 80 and (not full or tot_a == tot_r) and sr['exact'] else 1



if __name__ == '__main__':
    raise SystemExit(model_count(sys.argv[1:] == ['all']))
```

## Appendix E. v106's transfer sample programs (Section 8.2)

These are the preregistered files of v106's sample (SHA-256: eaq106.c 56d99d413dd4e15bf114351bb8899bf5c65d0de6ecff972d3dee8604f776cff8, its binary 93f15dbcc50cfaca5a3562a23ea11e5c8808896a01c395a74f5125e3de29e9de, summarize_ts.py cf2b1e055bc63cc0edae72e70a8a77aee5da7742247eebbc652ce9781933566f, make_seeds_ts.py 7c1eb79396a1e467f186870f91201b00054d955efa9c791cfb2a01dc90a74874, crosscheck_ts.py 6d93613305073ac44c63cbde7f0858077431ac8d271eafb13e4b1abf843a6295, run_ts.sh b36e350c9d36e45da468f823db94932c188f25374c4a5c80b32cf20eaa2d8432, freeze_ts.sh b2931a3ce37406db1f7219560f2ee88a1bdf75d79f990fb78848d9a324809f8c, the frozen counted program, equal to this package's shipped program, 41a0d8ae77bebad58fd5c0210a6d7c4e7cc2f9ff08e7d3acf29a0985cf5777a1; all listed in PREREG_v106_TS.txt, SHA-256 21b56d46aa3720d23155a00e50bdf9b5f605886d440096fc00c2daafb7e585a7; the seed file SEEDS_TS.txt 76b49220debfe123514e7290f2f5e1648a3635e9584527cafaa7bb6993f2669b). `eaq106.c`, `summarize_ts.py` and `crosscheck_ts.py` are ef052659's `eaq.c`, `summarize_ea.py` and `crosscheck_ea.py` of Appendix C with the changes shown below as unified diffs (nothing else differs); `make_seeds_ts.py` and `run_ts.sh` are given in full. `eaq106.c` is compiled with `cc -O3 -march=native` and run as `./eaq106 1073741824 SEED` (32 seeds, by `run_ts.sh`); `summarize_ts.py` imports the counted program (for p_B) from the directory given as its argument.

```diff
--- eaq.c
+++ eaq106.c
@@ -1,3 +1,7 @@
+/* eaq106.c (blake3-r2 v106): v104's eaq.c (proof.md Appendix C; SHA-256 bef43dcd...aa36da0) with one change: VRANGE is
+   1057885, the V of v106 (outer steps vd < 1,057,885), instead of v104's 1512538, so that a unit is one batch drawn
+   uniformly from the run of v106 (Lemma U).  Everything else, including the comments below, is v104's eaq.c verbatim.
+   ---------------------------------------------------------------------------------------------------------------- */
 /* eaq.c (blake3-r2 v104): the stage events of H1 (ii), including the early-exit event (rule A, the filter and W4 = 0),
    on uniform batches of the run in the order S2K14 (Lemma U).  Everything up to and including trial() below is
    Subflatus3's sbs2k.c (5ca02dfb, proof.md Appendix B; SHA-256 17f5d91c...6a208) verbatim, with its own header comment;
@@ -29,7 +33,7 @@
 #define W13 0x0007c006u
 #define Y3 0x8127c181u
 #define Y11 0x7af77f38u
-#define VRANGE 1512538u
+#define VRANGE 1057885u
 #define NMEM 65536
 #define NB 9363
 static u64 sm;
--- summarize_ea.py
+++ summarize_ts.py
@@ -1,5 +1,5 @@
-"""summarize_ea.py (v104): analysis and decision rule of the early-exit sample, fixed before the runs.
-Reads runs/NN.txt (one output line of `eaq 1073741824 SEED` each) for the 32 lines of SEEDS_EA.txt; STOP unless all 32 runs
+"""summarize_ts.py (v106): v104's summarize_ea.py for the transfer sample (units of the v106 run, vd < 1,057,885).
+Reads runs/NN.txt (one output line of `eaq106 1073741824 SEED` each) for the 32 lines of SEEDS_TS.txt; STOP unless all 32 runs
 are present with 2^30 units and their seeds.  Unit k = one uniform batch of the run in the order S2K14 (Lemma U):
 b = 1{enters stage B}, x = c/7 (c = counted lanes with rule A and the filter), r = w/7 (w = those with W4 = 0); units are
 i.i.d. in [0, 1]; E b = the run's stage-B share, E x = KAP * (per-trial rate of rule A and filter), E r = KAP * (per-trial
@@ -15,7 +15,7 @@
 import sys, math, json, os
 from fractions import Fraction
 sys.path.insert(0, sys.argv[1]); import s8stage as P
-seeds = {l.split()[0]: l.split()[1] for l in open('SEEDS_EA.txt') if l.strip() and not l.startswith('#')}
+seeds = {l.split()[0]: l.split()[1] for l in open('SEEDS_TS.txt') if l.strip() and not l.startswith('#')}
 K = ('units', 'stageB', 'ruleA_filter_lanes', 'ruleA_filter_sq', 'w4zero_lanes', 'w4zero_sq', 'w4zero_batches', 'w4low8', 'w4low16',
      'w4low24', 'stageC', 'lastgroup'); S = dict.fromkeys(K, 0); per = []; cmax = wmax = 0
 for nn in sorted(seeds):
@@ -54,5 +54,5 @@
 out['W4_low_bits_zero_per_AF_lane_log2'] = {b: math.log2(S['w4low%d' % b] / S['ruleA_filter_lanes']) for b in (8, 16, 24) if S['w4low%d' % b]}
 out['per_run_stageB_over_pB'] = [min(b for _, b, _ in per) / (1 << 30) / float(pB), max(b for _, b, _ in per) / (1 << 30) / float(pB)]
 out['per_run_AF_over_2^-11'] = [min(c for _, _, c in per) / 7 / (1 << 30) / unit['C'], max(c for _, _, c in per) / 7 / (1 << 30) / unit['C']]
-out['decision'] = 'PROCEED (rho_R = 2^-24; premises 0.377 and 1.003 reproduced)' if dec else 'STOP'
+out['decision'] = 'PROCEED (premises 0.377, 1.003 and 2^-24 pass on the units of the v106 run)' if dec else 'STOP'
 print(json.dumps(out, indent=1))
--- crosscheck_ea.py
+++ crosscheck_ts.py
@@ -1,4 +1,4 @@
-"""crosscheck_ea.py (v104): eaq --context against the counted program experiments/s8stage.py.  For one context (six outer
+"""crosscheck_ts.py (v106): v104's crosscheck_ea.py with vd below 1,057,885 (this version's V); eaq106 --context against the counted program experiments/s8stage.py.  For one context (six outer
 words with D3.d1 = X3, member index MI, group G) and NPOS consecutive positions: per batch the stage-B decision, the
 counted lanes with rule A and the filter, those with W4 = 0, and the FNV hash over (eb, c, the W4 of each such lane),
 where W4 is read from s8stage.forward as residual_words(f)['R4'] = ROL(D4, 7) ^ D1 of the two real digests (Lemma D');
@@ -9,7 +9,7 @@
 from verifier.blake3 import blake3
 import s8stage as P
 rng = random.Random(seed); F = 1099511628211; MASK = (1 << 64) - 1
-cw = [rng.getrandbits(32) for _ in range(6)]; cw[1] %= 1512538; cw[2] = P.X3
+cw = [rng.getrandbits(32) for _ in range(6)]; cw[1] %= 1057885; cw[2] = P.X3
 mi = rng.randrange(1 << 16); g = P.NBATCH - 1 if seed % 3 == 0 else rng.randrange(P.NBATCH); i0 = rng.randrange(P.NPOS - npos)
 o = P.outer(cw); y = P.member(mi); c = (P.member_vals(o, y)['X6'] + o['w7']) & P.M32
 h = 1469598103934665603; nB = nC = nW = ver = n = 0
```

```python
"""make_seeds_ts.py (v106): seeds of the preregistered transfer sample, drawn only after the preregistration is frozen.
Run NN (NN = 01..32): SEED = first 16 hex digits of SHA-256('blake3-r2-v106 TS sample NN') as a decimal integer; eaq106
starts SplitMix64 at state SEED.  Checks that the 32 streams (2^35 states each, more than one run's draws: 2^30 units of
about 9.7 draws) are pairwise disjoint and each disjoint from every stream listed in v104's make_seeds_ea.py (Subflatus3's
32 S2K14 sample streams and development seeds 1..9, v104's eaq development seeds 5 and 6, the b3r2_1008 study's scan.c and
w4rate.c runs), from v104's 32 EA sample streams, and from this version's eaq106 development run (seed 106, 2^32 states).
usage: python3 make_seeds_ts.py > SEEDS_TS.txt"""
import hashlib
M = 1 << 64; G = 0x9E3779B97F4A7C15; GI = pow(G, -1, M)
def h(label): return int(hashlib.sha256(label.encode()).hexdigest()[:16], 16)
def pos(state): return state * GI % M          # index of a start state in the SplitMix64 Weyl sequence
runs = [('%02d' % k, h('blake3-r2-v106 TS sample %02d' % k)) for k in range(1, 33)]
streams = [(pos(s), 1 << 35, 'v106 ' + n) for n, s in runs]
streams += [(pos(h('blake3-r2-v104 EA sample %02d' % k)), 1 << 35, 'v104 EA %02d' % k) for k in range(1, 33)]
streams += [(pos(h('subflatus3 S2K14 sample %02d' % k)), 1 << 35, '5ca02dfb %02d' % k) for k in range(1, 33)]
streams += [(pos(s), 1 << 35, '5ca02dfb dev %d' % s) for s in range(1, 10)]
streams += [(pos(s), 1 << 32, 'eaq dev %d' % s) for s in (5, 6)]
streams += [(pos(106), 1 << 32, 'eaq106 dev 106')]
streams += [(pos((s * 0x1234567 + 77) % M), 1 << 32, 'study %d' % s) for s in
            sorted(set([1, 2, 3, 4, 5, 7] + list(range(11, 19)) + [21, 22, 24, 28] + list(range(31, 39))))]
bad = 0
for i in range(len(streams)):
    for j in range(i + 1, len(streams)):
        (pi, li, ni), (pj, lj, nj) = streams[i], streams[j]
        if not (ni.startswith('v106') or nj.startswith('v106')): continue    # earlier streams among themselves: not checked
        d = (pj - pi) % M
        if not (d >= li and M - d >= lj): bad += 1; print('# OVERLAP', ni, nj)
assert bad == 0
print("# v106 TS sample seeds: SHA-256('blake3-r2-v106 TS sample NN')[:16] as decimal; 32 runs of eaq106 1073741824 SEED;")
print("# SplitMix64 streams checked pairwise disjoint and disjoint from all earlier streams listed in make_seeds_ts.py")
for n, s in runs: print(n, s)
```

```bash
#!/bin/bash
# v106 transfer sample: one run `eaq106 1073741824 SEED` per line of SEEDS_TS.txt (32 runs).  Refuses unless the
# preregistration is frozen (PREREG_v106_TS.sha256 and FROZEN_TS.sha256 check) and SEEDS_TS.txt equals the output of the
# frozen make_seeds_ts.py.  Takes the machine-wide heavy-job lock (research/heavy.lock; waits for it, released on exit).
# Stability: nice -n 10; a run starts only while the 1-minute load average is at most 12 and fewer than MAXP (<= 10) of
# our runs are running.  Resumable: a run with a complete output file is never started again.  Every start and end is
# logged with UTC time in runs/LOG.txt.  usage (from sample/): ./run_ts.sh LOCKDIR [MAXP]
set -u
cd "$(dirname "$0")" || exit 1
L="$1"; U=1073741824; MAXP=${2:-8}; [ "$MAXP" -gt 10 ] && MAXP=10
shasum -a 256 -c PREREG_v106_TS.sha256 >/dev/null 2>&1 || { echo "PREREG not frozen or changed"; exit 1; }
shasum -a 256 -c FROZEN_TS.sha256 >/dev/null 2>&1 || { echo "frozen files changed"; exit 1; }
python3 make_seeds_ts.py | cmp -s - SEEDS_TS.txt || { echo "SEEDS_TS.txt differs from the frozen rule"; exit 1; }
mkdir -p runs
echo "$(date -u +%FT%TZ) waiting for the heavy-job lock" >> runs/LOG.txt
until mkdir "$L" 2>/dev/null; do sleep 30; done
trap 'rmdir "$L"; echo "$(date -u +%FT%TZ) lock released" >> runs/LOG.txt' EXIT
echo "$(date -u +%FT%TZ) lock acquired (b3r2 v106 TS sample)" >> runs/LOG.txt
load1() { sysctl -n vm.loadavg | awk '{print $2}'; }
while read -r NN SEED; do
  out="runs/${NN}.txt"
  if [ -s "$out" ] && grep -q '^units ' "$out"; then continue; fi
  while :; do
    nrun=$(jobs -rp | wc -l | tr -d ' ')
    if awk -v l="$(load1)" 'BEGIN{exit !(l <= 12)}' && [ "$nrun" -lt "$MAXP" ]; then break; fi
    sleep 15
  done
  echo "$(date -u +%FT%TZ) start $NN $SEED load $(load1)" >> runs/LOG.txt
  ( nice -n 10 ./eaq106 "$U" "$SEED" > "$out.part" 2> "runs/${NN}.err" && mv "$out.part" "$out"
    echo "$(date -u +%FT%TZ) end $NN exit $?" >> runs/LOG.txt ) &
  sleep 2
done < <(grep -v '^#' SEEDS_TS.txt)
wait
echo "$(date -u +%FT%TZ) all started runs finished" >> runs/LOG.txt
```
