# SHA-256, first 31 steps: specified two-block collision

## 1. Target and score

Track sha256-r31-exploratory, profile sha256-r31-prefix-v1, cost model
collision-frontier-v5. The object is an ordinary collision of the complete
reduced hash: FIPS 180-4 IV, standard length padding, feed-forward after
every block, original steps 0 through 30, and all 256 output bits.

Submitted scalar: time_log2 = 51.0. Memory ceiling: 2^57 bytes. Success
probability: 0.5. The certificate is a target-matching witness, not the
scored search and not a zero-cost algorithm.

## 2. Signed-difference legend

Each row of the characteristic is 32 symbols, left to right from bit 31
down to bit 0. The symbols are the signed-difference alphabet of the source
attack:

- n means the bit is 0 in the first message and 1 in the second.
- u means the bit is 1 in the first message and 0 in the second.
- 0 means the bit is 0 in both messages.
- 1 means the bit is 1 in both messages.
- = means the two messages have the same bit, with the common value free.

A blank difference cell means the word has no signed difference. Nonzero
message differences are allowed only in W5, W6, W7, W8, W9, W16, and W18.

## 3. Characteristic

The scored search follows this 31-step characteristic. Rows are step i, then
delta A, delta E, and delta W. Steps before 0 are chaining-input words.

```
i  dA                                dE                                dW
-4 ================================= =================================
-3 ================================= =================================
-2 ================================= =================================
-1 ================================= =================================
 0 ================================= ================================= =================================
 1 ================================= ================================= =================================
 2 ================================= ================================= =================================
 3 ================================= ==========================10==== =================================
 4 ================================= ============0===0=========01===0 =================================
 5 ===================n=unnnnnnn=n= 000111010001111110nu=11111unnnu1 ================nuuu=======0=uu=
 6 ========n======================u 101011=11==0n0==u11110==1110011n ==========u=====u===u======n===u
 7 ===u===n==n========n=========n=u un0u1100n=01u11111001u1=n110u10n =u=u=======n=====n=nu=n=====nun=
 8 =============================n== 1u01un0u0=1=1=11n=0=u0=001001u0= =u=nn==========u===u===u==1=====
 9 ================================= 01100001110=0=010===00=11101u0=1 ================u==========1=u==
10 ================u============u== =1n1uuuuu0100=1un0=10unnnnnnn010 =================================
11 ================================= =01u1010uu1==11100===1000001n=0= =================================
12 ================================= ==110001=11====1n====0011110n=0= =================================
13 ================================= ===0====01======1=============== =================================
14 ================================= ================u===========0u== =================================
15 ================================= ================0============1== =================================
16 ================================= ================1============1== =============unnnunnnnnnnnnnnn==
17 ================================= ================================= =================================
18 ================================= ================================= ==============1=n=0==========n==
19 ================================= ================================= =================================
20 ================================= ================================= =================================
21 ================================= ================================= =================================
22 ================================= ================================= =================================
23 ================================= ================================= =================================
24 ================================= ================================= =================================
25 ================================= ================================= =================================
26 ================================= ================================= =================================
27 ================================= ================================= =================================
28 ================================= ================================= =================================
29 ================================= ================================= =================================
30 ================================= ================================= =================================
```

From step 17 through step 30 every state difference is zero, and the only
later message differences are the W16 and W18 rows above, which the expansion
must cancel. A pair that follows every signed condition through step 30
therefore leaves the compression with equal outputs.

## 4. Executable search

All randomness is uniform over the free words named in the step. A trial
that violates a signed condition is a failure and is charged.

Phase 0, advice. The characteristic above is the nonuniform advice. It is
1,488 bytes of text in this file, declared as 2^16 bytes so the bound covers
a binary encoding and a small index. Regenerating it is not required online.
Its construction cost is the phase-1 model solve below, not a free constant.

Phase 1, one starting point. Search for one assignment of A_1..A_12,
E_5..E_12, and W_9..W_12 that meets the signed conditions on steps 5
through 12. Charge 2^32 reduced compressions for this solve. That is above
the 2^31.7 figure reported for the same model, and it is the whole
preprocessing term. If the solve fails, the run fails. The bound assumes one
successful solve, which is the case the source attack reports.

Phase 2, solution list. From that starting point, enumerate admissible
values of W5, W6, W7, and W8 that preserve the local collision in the
expansion and the conditions on E3 and E4. The source count is 2^14
candidates for W5, 2^23 for W6, 2^27 for W7, and 2^25 for W8 before the E3
and E4 filter, with 2^11 pairs (W7, W8) surviving, for 2^14 * 2^23 * 2^11
= 2^48 stored solutions. Each stored record holds A_{-3}..A_12 (16 words),
E_1..E_12 (12 words), and W_5..W_12 (8 words): 36 words, 144 bytes. The
memory accounting reserves 256 bytes per record so an index and alignment
fit. Building one record is charged at most 32 word operations.

Phase 3, first block. Repeat the following until phase 4 accepts or the
budget in section 5 is exhausted. Choose a first 64-byte block, compress it
from the standard IV for 31 steps, and probe the list on (A_{-3}, A_{-2},
A_{-1}). A hit determines W0..W4 and E0 for the second block. A miss is a
failed trial. Each trial is one selected compression plus at most 32 word
operations for the probe, the address calculation, and the miss bookkeeping.
The number of trials in one search is the source estimate 2^{96-48+1.3}
= 2^{49.3}, because a list of 2^48 early solutions reduces a 2^96 chaining
match, and phase 4 then succeeds with probability about 2^{-1.3}.

Phase 4, finish the second block. On a hit, assign W13, W14, and W15 and
test the signed conditions on E13, E14, E15, W16, and W18. The source
100-test estimate is success probability about 2^{-1.3}. On failure, return
to phase 3. On success, the two second blocks are the message pair for this
chaining value.

Phase 5, padding. Append the ordinary SHA-256 length padding to both
complete messages. The bodies have equal length, so the padding block is
identical and does not reopen a difference. Rehash both messages with the
organizer function at 31 steps and accept the pair only if the 256-bit
digests are equal and the messages differ. This final check is two
compressions plus the padding words.

The algorithm returns the first accepted pair. It does not return the
certificate bytes. Those bytes are a separate existence check.

## 5. Cost arithmetic

Reference cost C is 2140. One 31-step compression is one unit. One word
operation outside a compression is 1/2140 unit. Every bound below is an
upper bound. The source formula 2^{49.3} + 2^{48} is charged in full as
compressions, even though the 2^{48} term is a list size. Charging it as
compressions as well as memory is conservative. It is not omitted.

One search, compression units:

- Phase 1: 2^{32}.
- Phase 3 trials: 2^{49.3}.
- Source list term, charged again as compressions: 2^{48}.
- Phase 5: 2.

Compression subtotal: 2^{49.3} + 2^{48} + 2^{32} + 2.
Numerically the compression subtotal is 974551961825381.75, whose base-2
log is 49.79173244.

One search, word-operation units, at 32 operations per record and per trial:

- Phase 2: 2^{48} * 32 / 2140 = 4124219946979.85, log2 41.907.
- Phase 3: 2^{49.3} * 32 / 2140 = 10448455445290.56, log2 43.250.
- Sum: 14572675392270.41, log2 43.728.

One-search total: 989124637217652.125 units, log2 49.81314565.
This is 2^{49.3} + 2^{48} + 2^{32} + 2 + 2^{48}*32/2140 + 2^{49.3}*32/2140.
No further surcharge is added. In particular, a term of size 2^{48.8} is
not added on top of this total.

Two sequential searches, with no early-stop credit: twice the one-search
total, 1978249274435304.25 units, log2 50.81314565. That is strictly below 2^{51}.
The submitted time_log2 is 51.0. The gap from 50.81314565 to 51.0 is unused
slack, not a place where another 2^{48.8} term is hiding.

Success probability. Heuristic H-GEOMETRIC says a search run for its
expectation is a geometric trial process with success probability
1 - exp(-1) if the trials inside it are independent. Two independent
searches, each run for that expectation, fail together with probability
at most exp(-2), about 0.1353. The probability of at least one collision
is therefore at least 0.8647. The claim records 0.5. The independence
premise is H-GEOMETRIC. The charged budget is the no-early-stop sum, so
stopping early only reduces real cost.

## 6. Memory

- 2^48 records * 256 bytes = 2^56 bytes.
- Advice and characteristic encoding: 2^16 bytes.
- Code and working state: at most 2^30 bytes.
- Sum: 2^56 + 2^16 + 2^30 < 2^56 + 2^56 = 2^57.

The submitted memory_log2_bytes is 57. The record payload alone is 144
bytes, so 256 bytes per record leaves 112 bytes of index and padding inside
the ceiling rather than sitting on it.

## 7. Witness

certificates/a.bin and certificates/b.bin are distinct 128-byte messages.
digest(message, "sha256", 31) equals

    55fdfb37efcbd086e19c3de0f72596300a3acdf48da5b1d0450a592bb2869fcd

for both. The same call at 32 steps does not collide. This shows the
organizer IV, padding, step index, and 256-bit comparison admit an ordinary
31-step collision. It is not a transcript of phases 1 through 5 and is not
charged as the search.

## 8. Limits

The 2^48 list size and the 2^{-1.3} phase-4 rate are the source paper's
reported figures, not a new local campaign. They are premises H-WORD-COUNTS
and H-PHASE4. A larger phase-4 failure rate would raise the true cost. The
2^51 ceiling sits 0.18685435 bits above the computed two-search total of 2^50.81314565. This package does not claim a practical 2^40 attack, a
32-step collision, or a free-start collision. Readiness requests review. It
does not assert human acceptance or Yukon promotion.
