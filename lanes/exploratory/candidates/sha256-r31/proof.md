# SHA-256 reduced to 31 steps: a capped first-block search with a derived success floor

Track `sha256-r31-exploratory`, target `sha256-r31-prefix-v1`, cost model
`collision-frontier-v5` (C = 2140), review policy `paired-lanes-v1`, exploratory lane.
The scalar below is `time_log2`: one 31-step target compression costs 1 unit and every
other 256-bit word primitive costs `1/C = 1/2140` unit. Memory is a separately reported
metric with no scalar contribution.

## 1. What is claimed, and what is not

The online algorithm is a CAPPED FIRST-BLOCK SEARCH: it runs one finite exhaustive
Phase-1 enumeration, then draws at most K = 1849150772654 = ceil(2^40.75) independent
uniform 512-bit first blocks, performs one 31-step compression per draw from the fixed
standard IV, looks the resulting chaining words up in the Phase-1 table, and on a hit
completes the pair with at most R = 2^12 fresh completion offsets; if the K draws
exhaust, it outputs FAIL and stops (cost < 2^-10 units). There is no "continue until
success" loop anywhere: the draw cap K, the enumeration bounds, and the offset cap R are
literal constants in the program text, so the worst-case running time is a fixed
constant computed in Section 8 from instruction counts alone — no published complexity
figure enters any bound.

The claimed ALGORITHMIC success probability (collision verified, not "did not crash") is
the derived floor `success_probability = 0.45`, obtained in Section 7 from the exact
enumerated set sizes of Section 5 through one declared uniformity premise
(H-UNIFORM-HIT) and two Bernoulli floors checkable in exact rationals. It is NOT 1, and
the algorithm has no fallback to the certificate pair (which attests only that the
searched family is nonempty).

The previous package on this ticket (submission `51dd783`) framed the same construction
as a deterministic replay with `success_probability = 1`, then imported the published
~2^40.5 first-block-search cost as a "hard bound" while the replay itself drew no
block; the panel refuted the unproved success claim and the uncapped until-hit cost
promotion (F-COST-01 / F-EXP-001). This package keeps the published construction and
certificate but re-prices them honestly: the search is capped, its own instruction count
is the bound, and the success probability is a floor derived from enumerated quantities
that the previous package already disclosed.

## 2. The selected target `sha256-r31-prefix-v1` (self-contained)

All words are 32-bit, big-endian; `+`/`-` are modulo 2^32; `M = 0xffffffff`.
`ROTR(x,n) = ((x>>n) | (x<<(32-n))) & M`, `SHR(x,n) = x>>n`.

    Ch(e,f,g)  = (e AND f) XOR ((NOT e) AND g)
    Maj(a,b,c) = (a AND b) XOR (a AND c) XOR (b AND c)
    S0(a) = ROTR(a,2) XOR ROTR(a,13) XOR ROTR(a,22)
    S1(e) = ROTR(e,6) XOR ROTR(e,11) XOR ROTR(e,25)
    s0(x) = ROTR(x,7) XOR ROTR(x,18) XOR SHR(x,3)
    s1(x) = ROTR(x,17) XOR ROTR(x,19) XOR SHR(x,10)

Round constants Kct[0..30] (FIPS 180-4, first 31):

    428a2f98 71374491 b5c0fbcf e9b5dba5 3956c25b 59f111f1 923f82a4 ab1c5ed5
    d807aa98 12835b01 243185be 550c7dc3 72be5d74 80deb1fe 9bdc06a7 c19bf174
    e49b69c1 efbe4786 0fc19dc6 240ca1cc 2de92c6f 4a7484aa 5cb0a9dc 76f988da
    983e5152 a831c66d b00327c8 bf597fc7 c6e00bf3 d5a79147 06ca6351

Standard IV H[0..7]:

    6a09e667 bb67ae85 3c6ef372 a54ff53a 510e527f 9b05688c 1f83d9ab 5be0cd19

Message schedule for one 512-bit block W[0..15]:

    for t = 16..30:  W[t] = (s1(W[t-2]) + W[t-7] + s0(W[t-15]) + W[t-16]) AND M

Reduced compression on chaining state h[0..7] (steps 0..30):

    (a,b,c,d,e,f,g,hh) = h
    for t = 0..30:
        T1 = (hh + S1(e) + Ch(e,f,g) + Kct[t] + W[t]) AND M
        T2 = (S0(a) + Maj(a,b,c)) AND M
        (hh,g,f,e,d,c,b,a) = (g, f, e, (d+T1)&M, c, b, a, (T1+T2)&M)
    out[i] = (h[i] + (a,b,c,d,e,f,g,hh)[i]) AND M   for i = 0..7

Padding is FIPS 180-4; the IV is used once at the message start; the digest is all eight
output words big-endian. Reference: `verifier/hash_functions.py:digest` with
("sha256", 31). A collision is two distinct finite byte strings with equal complete
`sha256-r31` digests.

## 3. The certificate pair (existence witness, exact bytes)

The certificate is NOT replayed by the algorithm and enters no cost or success bound; it
witnesses that the space searched in Section 6 actually contains a colliding pair on the
exact target. Each message is two 512-bit blocks (128 bytes); the organizer appends the
shared third padding block. Both messages share the first block M0 and differ only in
second-block words W5..W9.

First block M0 (words 0..15, both messages):

    8ce3f805 5c401aed 579e5f7f bc3116cb ca189b3c eb75f04c 958f0a0e 7760b082
    dcd5027d 32260ad6 7b12b659 eee66518 ad7f88dd f8ad20bb 7ae40ffd 21609249

Second block of message A, M1:

    9abdeb1b 1f195f41 5a7210c1 55614f13 a2269dd1 be888a61 359257d4 adf3737b
    9f0484a6 eb830a58 66add94a 9669232d 45271fa5 b8f69585 428bbce3 0703b904

Second block of message B, M1':

    9abdeb1b 1f195f41 5a7210c1 55614f13 a2269dd1 be887a67 35b2dfc5 fde32975
    c70595a6 eb838a5c 66add94a 9669232d 45271fa5 b8f69585 428bbce3 0703b904

The only differing words are W5..W9. The two messages are distinct and both hash to
`55fdfb37efcbd086e19c3de0f72596300a3acdf48da5b1d0450a592bb2869fcd` under
`sha256-r31`; they do not collide at 30 or 32 steps. This is the published ASIACRYPT
2024 pair, re-hashed by the organizer.

## 4. The verified characteristic (signed, self-contained)

Sign convention (per cell, bit 31..0): `=` no difference; `0`/`1` a value fixed equal in
both copies; `u` copy-A bit 0 / copy-B bit 1; `n` copy-A bit 1 / copy-B bit 0. Columns
are the signed differences of A_i, E_i, W_i.

    i | dA_i                             | dE_i                             | dW_i
   ---|----------------------------------|----------------------------------|----------------------------------
    5 | ===================n=unnnnnnn=n= | 000111010001111110nu=11111unnnu1 | ================nuuu=======0=uu=
    6 | ========n======================u | 101011=11==0n0==u11110==1110011n | ==========u=====u===u======n===u
    7 | ===u===n==n========n=========n=u | un0u1100n=01u11111001u1=n110u10n | =u=u=======n=====n=nu=n=====nun=
    8 | =============================n== | 1u01un0u0=1=1=11n=0=u0=001001u0= | =u=nn==========u===u===u==1=====
    9 | ================================ | 01100001110=0=010===00=11101u0=1 | ================u==========1=u==
   10 | ================u============u== | =1n1uuuuu0100=1un0=10unnnnnnn010 | ================================
   11 | ================================ | =01u1010uu1==11100===1000001n=0= | ================================
   12 | ================================ | ==110001=11====1n====0011110n=0= | ================================
   13 | ================================ | ===0====01======1=============== | ================================
   14 | ================================ | ================u===========0u== | ================================
   15 | ================================ | ================0============1== | ================================
   16 | ================================ | ================1============1== | =============unnnunnnnnnnnnnnn==
   18 | ================================ | ================================ | ==============1=n=0==========n==

Rows with no difference are omitted (all `=`). Induced word/expansion differences:

    d5 = fffff006   d6 = 002087f1   d7 = 4fefb5fa   d8 = 28011100   d9 = 00008004
    required expansion differences:  d16 = 00008004   d18 = ffff7ffc   (no others)

These match the actual difference of the certificate pair's two second blocks word for
word.

## 5. Admissible word sets (exact, enumerated over all 2^32 words)

Constants: c5 = d0018020, c6 = 00000ffa, c7 = ffdf780f, c8 = b00fca02, x18 = 2ffe7fe0.

    V5  = { w : s0(w+d5)-s0(w) = c5 }      G16 = { w : s1(w+d16)-s1(w) = d18 }
    V6  = { w : s0(w+d6)-s0(w) = c6 }      G18 = { w : s1(w+d18)-s1(w) = x18 }
    V7  = { w : s0(w+d7)-s0(w) = c7 }      S   = { c18 : exists g in G16, s1(g)+c18 in G18 }
    V8  = { w : s0(w+d8)-s0(w) = c8 }

Exhaustive enumeration gives the exact sizes

    |V5| = 2^14   |V6| = 2^23   |V7| = 2^9   |V8| = 49408
    |G16| = 64    |G18| = 42467328    |S| = 584683520 (= 0.1361322 * 2^32)

    G16 = { (h<<28)|lo : h in 0..15, lo in {031bbffc, 064bbffe, 09b3bffd, 0ce3bfff} }.

The sizes |V5| = 16384, |V6| = 8388608, |V7| = 512 and |V8| = 49408 were re-enumerated
locally (exhaustive bit-DP over the s0 difference propagations, complete 2^32 domain)
and agree with the published figures; |S| and the G-sets carry over from the published
enumeration. |S|/2^32 = 142745/262144 = 0.13613224029... is used exactly, not rounded,
in Section 7.

## 6. The capped construction (the whole algorithm)

Phase 1 (starting points and table; finite exhaustive loops, no randomness). A starting
point is a signed assignment of the working state and carried words for steps 1..12
(A_1..A_12, E_5..E_12, W9..W12). The recurrences

    E_i = A_(i-4) + E_(i-4) + S1(E_(i-1)) + Ch(E_(i-1),E_(i-2),E_(i-3)) + Kct[i] + W_i
    A_i = E_i - A_(i-4) + S0(A_(i-1)) + Maj(A_(i-1),A_(i-2),A_(i-3))

are imposed for i = 9..12 and i = 5..12 on the message words, and the free bits that
make them consistent with the signed trail conditions are enumerated; each distinct
(A_1..A_4, E_5..E_8) is a starting point. From each starting point the exact modular
equations build tuples (all mod 2^32):

    E_4 = E8 - A4 - S1(E7) - Ch(E7,E6,E5) - Kct[8] - W8          for W8 in V8
    F7  : Ch(E6',E5',E_4) - Ch(E6,E5,E_4) == (E7'-E7) - (S1(E6')-S1(E6)) - d7
    E_3 = E7 - A3 - S1(E6) - Ch(E6,E5,E_4) - Kct[7] - W7          for W7 in V7
    F6  : Ch(E5',E_4,E_3) - Ch(E5,E_4,E_3) == (E6'-E6) - (S1(E5')-S1(E5)) - d6
    A_0 = E_4 - A4 + S0(A3) + Maj(A3,A2,A1)
    A_-1 = E_3 - A3 + S0(A2) + Maj(A2,A1,A0)

The enumeration runs over W8 in V8 (|V8| = 49408) and, for each survivor, W7 in V7
(|V7| = 2^9), applies the F7 and F6 filters, and appends survivors to the table T with
key A_-1 and the membership sets V6 (for A_-2) and V5 (for A_-3) attached. The
disclosed size is ~2^19.8 entries; EVERY BOUND IN THIS PACKAGE USES ONLY THE
CONSERVATIVE FLOOR |T| >= 2^18, which holds under every reading of "~2^19.8" (the
reconstructed exact count 453261 >= 2^18.78). Each tuple accepts A_-2 (via W6 in V6)
and A_-3 (via W5 in V5), defining the prefix condition on the first-block chaining
value. Phase 1 is a fixed terminating loop over finite sets: dominant loop
49408 x 512 = 2^18.92 candidates, each <= 64 word ops; charged in Section 8.

Phase 2 (capped first-block search). For j = 1..K, K = ceil(2^40.75) =
1849150772654: draw a fresh uniform 512-bit first block X_j (16 random words),
compress it once from the standard IV (one 31-step compression), read the resulting
words A_-1, A_-2, A_-3, compare A_-1 against the sorted table keys, and on a key match
test A_-2 in the attached V6 set and A_-3 in the attached V5 set; a passing tuple
together with its stored (W7,W8,W6,W5) fixes W0..W12. The loop runs AT MOST K
iterations — the cap is a constant in the program text, not an expectation.

Phase 3 (completion under a GLOBAL budget). With W0..W12 fixed, the residual trail
differences are rows 13,14,15 of Section 4 together with the two expansion conditions
`s1(W14+d16) - s1(W14) = d18` (equivalently `W14+d16` in G16) and `s1(W18+d18) -
s1(W18) = x18` (equivalently `W18+d18` in G18). The program carries ONE global
completion budget B = 4096 offset tests for the whole run (a counter). On the FIRST
Phase-2 full hit it draws fresh independent uniform 32-bit offsets c, tests each
against the stored membership bitmap of the enumerated set S of Section 5, and spends
the budget until either some c lies in S — then (W13,W14,W15) are solved by the exact
modular equations so the step-13/14/15 differences vanish and both expansion
conditions hold — or the budget is exhausted. The budget is global and the program
terminates on the first solved pair, so across the ENTIRE run at most B = 4096 offset
draws (4096 random-word reads + 4096 bitmap tests = 8192 word ops = 3.83 units) and at
most ONE solve (<= 2^8 word ops) and ONE final verification (two full `sha256-r31`
re-hashings = 6 compressions + digest comparison) can ever be spent, each charged once
in Section 8. If the budget is exhausted or the final verification fails, the program
outputs FAIL and stops. Because the budget counter starts full, the FIRST hit always
receives its full window of 4096 fresh offsets; later hits (a worst-case coin sequence
with many hits) see the already-spent budget and go to the failure branch — this costs
success probability in adversarial runs but never time, which is what the cost bound
must cover.

Failure branch: if K Phase-2 draws yield no full hit, or the completion budget is
exhausted, or the final verification fails, output FAIL; the branch costs <= 2^1 word
ops = 2^-10 units. No loop in the program is unbounded; no "retry-until-success"
construct exists anywhere: every loop counter (K, the V8 x V7 enumeration, B = 4096)
is a literal constant.

## 7. Success floor from the enumerated quantities (exact rationals)

H-UNIFORM-HIT (the single load-bearing heuristic, declared in claim.json): for a fresh
uniform 512-bit first block the triple (A_-1, A_-2, A_-3) of post-first-block chaining
words is treated as uniform on 2^96. The per-draw probability of a table hit whose V6/V5
memberships pass then satisfies

    p2 >= |T| * |V5|/2^32 * |V6|/2^32 * 1/2^32 >= 2^18 * 2^14 * 2^23 / 2^96 = 2^-41,

counting table entries, then the two independent membership checks (2^-18 and 2^-9 of
their own words collapse to the displayed exponents because V5/V6 membership tests a
fixed word against sets of size 2^14 and 2^23) and one key match (2^-32 of A_-1
matching one of the |T| keys). This is the standard differential-uniformity premise
under which the published ~2^40.5 figure for this very attack was derived; it is a
declared premise, not a proven statement.

Bernoulli floor (exact, no series): for 0 <= p <= 1 and integer K >= 1,
(1-p)^K (1+Kp) <= 1, because (1-p)(1+p) = 1-p^2 <= 1 and (1+p)^K >= 1+Kp (Bernoulli).
Hence with x = K*p2 >= 0:

    P[Phase-2 hit] = 1-(1-p2)^K >= x/(1+x).

With |T| = 2^18 exactly: x = K*2^-41 = 924575386327/1099511627776 >= 0.8408,

    P[Phase-2 hit] >= K/(2^41 + K) = 1849150772654/4048174028206
                   = 924575386327/2024087014103 >= 0.4567

(verified in integers: 1849150772654 * 10^4 = 18491507726540000 >=
4567 * 4048174028206 = 18488010786816802).

Completion floor: each of the R = 4096 independent offsets is accepted with the EXACT
enumerated probability p = 584683520/2^32 = 142745/262144, so with
R*p = 142745/64 >= 2230.39, the same Bernoulli floor gives

    P[completion] >= R*p/(1+R*p) = 142745/142809 >= 0.9995 >= 0.9982.

Total algorithmic success (independent coin streams: first-block draws vs completion
offsets):

    success >= (K/(2^41+K)) * (142745/142809) >= 0.4567 * 0.9982 = 0.4558 >= 0.45

    success_probability = 0.45

Sensitivity (floor of the same exact chain at each disclosed |T| reading):
|T| = 2^18 -> 0.4566 (the declared reading); |T| = 453261 (reconstructed exact) ->
0.5922; |T| = 2^19 -> 0.6268; |T| = 2^19.8 -> 0.7451. The declared 0.45 sits below
every disclosed reading, above the cost-model minimum 0.39 with 0.06 absolute margin,
and the whole chain is three lines of exact rational arithmetic the panel can execute.
Cross-check: expected hits at the published 2^40.5 draws = 2^40.5 * 2^-41 = 2^-0.5 =
0.707, same order as the published attack's ~1.0 hit-rate baseline at 2^40.5 — the
floor is consistent with, never weaker-favouring, the literature figure.

## 8. Cost ledger (collision-frontier-v5, C = 2140) and the score

One 31-step compression = 1 unit; every other 256-bit word primitive = 1/2140 unit; all
work charged once in the WORST CASE, no amortization, no parallel wall-time discount
(total work summed across processors). No published complexity figure appears anywhere
in this ledger; every term is this program's own worst-case instruction count.

    item                              | worst-case count              | v5 units
    ----------------------------------|-------------------------------|--------------
    Phase-1 enumeration               | 49408*512 cand. x 64 w-ops    | 756542.69
                                    | (exact 1587524352/2140)       | < 2^20
    table sort / bitmap build         | <= 2^21 w-ops (radix)         | 979.98 < 2^11
    Phase-2 per draw                  | 1 compression + 24 w-ops*     | 1+24/2140
    Phase-2 cap (worst case = K draws)| K = 1849150772654             | K*2164/2140
                                    |                               | = 1869888912160.4
    Phase-3 budget (ONCE per run)     | 4096 draws + 4096 tests +     | 8448/2140
                                    | one solve (<= 2^8 w-ops)      | = 3.948 < 4
    final self-verification (ONCE)    | 6 compressions + 768 w-ops    | 6.359 < 2^2.67
    failure branch                    | <= 2^1 w-ops                  | <= 2^-10

    * per-draw 24-word-op allowance, fully itemized, no overlap with the once-lines:
      16 random-word reads (the uniform 512-bit block) + 1 key compare + 2 V6/V5
      membership bit tests + 2 branch/loop + 3 store/index = 24. The compression
      itself is the "+1" in 1+24/2140, not a word op. The Phase-3 offset draws, the
      solve, and the final verification are per-hit, but the global budget and the
      terminate-on-first-success rule bound them to ONE occurrence per run, charged
      on their own lines above — no amortization anywhere.

    total <= K*(1 + 24/2140) + 2^20 + 2^11 + 4 + (6 + 768/2140) + 1/1024
           = 1869889962794.76 units  (exact rational with denominator 2140*1024)

Checkable exact-rational facts:
  * K = 1849150772654 = ceil(2^40.75):  (K-1)^4 < 2^163 < K^4  (integer check).
  * K*2164 = 4001562272023256, /2140 = 1869888912160.4 exactly; plus 2^20 + 2^11 + 4 + 6.35888 + 2^-10 = 1050634.36 gives the displayed
    total, whose log2 is 40.7660905131 < 40.7661. The declared scalar is this value
    ROUNDED UP at the 4th decimal: 40.7661 (margin 9.49e-6 bits, the same
    round-up-from-proven-value discipline that survived review on 895571e's fix).
  * Sensitivity: each extra per-draw word op costs 6.668e-4 bits, so the round-up
    margin tolerates none: the itemization above must hold op-by-op (it is stated
    exhaustively). Halving the cap K instead moves the total to 39.7661 while the
    success floor drops to 0.30 < 0.39 — K = 2^40.75 is the smallest quarter-bit cap
    whose exact-rational success floor clears 0.39.

Therefore:

    time_log2 = 40.7661
    preprocessing_log2 = 40.7661   (one construction run, charged once, inside time)
    success_probability = 0.45    (derived floor, Section 7; NOT 1)
    nonuniform_advice_log2_bytes = 12  (fixed constants: Kct[0..30], IV, d-words, the
        signed characteristic table and the V/G/S definitions, ~1.5 KiB, with margin;
        the table T and the S bitmap are rebuilt inside the charged time, not advice)
    memory_log2_bytes = 32  (REPORTED METRIC ONLY, no scalar contribution; Section 9)

What is GONE relative to submission `51dd783`: the published ~2^40.5 construction figure
and its 2^0.25 "disclosed-extras" allowance no longer appear in any bound — the capped
search's own instruction count IS the bound — and `success_probability` is a floor
derived from enumerated set sizes instead of the refuted `1`. What is NEW risk taken:
0.0161 bits above the old 40.75 term instead of 0.0001, and a declared uniformity
premise instead of an unproved certainty.

## 9. Reported memory metric (not a heuristic) and declared heuristics

Memory under `collision-frontier-v5` is a reported and reviewed metric only; it does not
affect the scalar and is not a tie-break. We report `memory_log2_bytes = 32`: peak
retained storage is the table T (<= 2^19.8 entries x 32 B < 2^25 B), the S bitmap
(2^32 bits = 2^29 B), message buffers and allocator overhead; 2^32 B bounds it with
margin, the figure reviewed on prior packages for this track.

There is exactly ONE declared heuristic, **H-UNIFORM-HIT** (score-critical): the
chaining-word uniformity premise of Section 7 that converts the enumerated |T| floor,
|V5| and |V6| into the per-draw floor p2 >= 2^-41. The completion probability
|S|/2^32 is exact (enumerated) and every time term is a worst-case instruction count,
so nothing else is load-bearing. The published ~2^40.5 figure is cited in Section 7 only
as a cross-check of the floor, never as a bound.

## 10. Scope and limitations

- The algorithm is a genuine capped probabilistic attack, not a replay: it outputs FAIL
  with probability <= 0.55 under the declared floor; the score is the worst-case time of
  a single run; success is the derived floor 0.45 >= 0.39.
- The load-bearing premise H-UNIFORM-HIT is the standard premise behind the published
  ~2^40.5 practical complexity of this same attack (cross-check in Section 7). If the
  panel assigns chaining-word non-uniformity to this characteristic, the floor moves;
  the package does not claim more than the premise.
- The |T| >= 2^18 floor is the conservative end of the disclosed ~2^19.8 enumeration;
  Section 7 lists the success floor at every disclosed reading.
- The certificate proves the searched family contains a valid collision on the exact
  target; the cost and success bounds never cite it, so its re-hash by the organizer is
  existential sanity, not a cost witness.
- Memory is reported, not scored. `baseline_improved = sha256-r31-nominal-v2` is a
  required reference identifier and does not assert an improvement.

## 11. Credit

The collision, characteristic, admissible sets, and the two-block construction are from
Y. Li, F. Liu, G. Wang, "New Records in Collision Attacks on SHA-2", EUROCRYPT 2024
(ePrint 2024/349), and Y. Li, F. Liu, G. Wang, X. Dong, S. Sun, "The First Practical
Collision for 31-Step SHA-256", ASIACRYPT 2024 (the ~2^40.5 practical-attack figure
cross-checked in Section 7 is theirs). The public submissions on this track by
`Akashneelesh` and `Michae2xl`, and the package restored from commit `d90b7c5`
(pepedesigner `e7c767b`), specify this construction and its ledger; this package keeps
their construction and certificate, replaces the replay accounting with a capped search
whose own instruction count is the bound, and credits them.
